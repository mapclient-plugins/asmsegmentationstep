'''
MAP Client, a program to generate detailed musculoskeletal models for OpenSim.
    Copyright (C) 2012  University of Auckland
    
This file is part of MAP Client. (http://launchpad.net/mapclient)

    MAP Client is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MAP Client is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MAP Client.  If not, see <http://www.gnu.org/licenses/>..
'''
import os
os.environ['ETS_TOOLKIT'] = 'qt4'

from PySide.QtGui import QDialog, QFileDialog, QDialogButtonBox,\
                         QAbstractItemView, QTableWidgetItem,\
                         QDoubleValidator
from PySide.QtCore import Qt
from PySide.QtCore import QThread, Signal

from mapclientplugins.asmsegmentationtep.ui_mayaviasmsegmentationviewerwidget import Ui_Dialog
from traits.api import HasTraits, Instance, on_trait_change, \
    Int, Dict

from mappluginutils.mayaviviewer import MayaviViewerObjectsContainer, MayaviViewerDataPoints,\
    MayaviViewerFieldworkModel, MayaviViewerLandmark, MayaviViewerImagePlane, colours

import copy

class _ExecThread(QThread):
    update = Signal(tuple)

    def __init__(self, func):
        QThread.__init__(self)
        self.func = func

    def run(self):
        output = self.func()
        self.update.emit(output)

class MayaviASMSegmentationViewerWidget(QDialog):
    '''
    Configure dialog to present the user with the options to configure this step.
    '''
    defaultColor = colours['bone']
    objectTableHeaderColumns = {'visible':0}
    backgroundColour = (0.0,0.0,0.0)
    _pointCloudRenderArgs = {'mode':'point', 'scale_factor':0.5, 'color':(0,1,0)}
    _modelInitRenderArgs = {'color':(1,0,0)}
    _modelFinalRenderArgs = {'color':(1,1,0)}
    # _landmarkRenderArgs = {'mode':'sphere', 'scale_factor':5.0, 'color':(0,1,0)}
    # _imageRenderArgs = {'vmax':2000, 'vmin':-200}
    _GFD = [8,8]

    def __init__(self, step, parent=None):
        '''
        Constructor
        '''
        QDialog.__init__(self, parent)
        self._ui = Ui_Dialog()
        self._ui.setupUi(self)

        self._scene = self._ui.MayaviScene.visualisation.scene
        self._scene.background = self.backgroundColour

        self.selectedObjectName = None
        self._step = step

        self._worker = _ExecThread(self._step._segment)
        self._worker.update.connect(self._fitUpdate)

        self._initViewerObjects()
        self._setupGui()
        self._initialiseSettings()
        self._makeConnections()
        self._initialiseObjectTable()
        self._refresh()

        # for k, v in self._config.items():
        #     print k+': ', v

    def _makeConnections(self):
        self._ui.tableWidget.itemClicked.connect(self._tableItemClicked)
        self._ui.tableWidget.itemChanged.connect(self._visibleBoxChanged)
        self._ui.screenshotSaveButton.clicked.connect(self._saveScreenShot)
        
        # self._ui.fitButton.clicked.connect(self._fit)
        self._ui.segButton.clicked.connect(self._worker.start)
        self._ui.segButton.clicked.connect(self._segLockUI)

        self._ui.resetButton.clicked.connect(self._reset)
        self._ui.abortButton.clicked.connect(self._abort)
        self._ui.acceptButton.clicked.connect(self._accept)

        self._ui.spinBoxPCsToFit.valueChanged.connect(self._saveConfig)
        self._ui.spinBoxSurfDisc.valueChanged.connect(self._saveConfig)
        self._ui.doubleSpinBoxMWeight.valueChanged.connect(self._saveConfig)
        self._ui.spinBoxMaxfev.valueChanged.connect(self._saveConfig)
        self._ui.lineEditXTol.textChanged.connect(self._saveConfig)

    def _initViewerObjects(self):
        self._objects = MayaviViewerObjectsContainer()
        self._objects.addObject('image', 
                                MayaviViewerImagePlane('image',
                                                       self._step.image,
                                                       renderArgs=self._imageRenderArgs))
        self._objects.addObject('Initial Model',
                                MayaviViewerFieldworkModel('Initial Model',
                                                           self._step.modelInit,
                                                           self._GFD,
                                                           renderArgs=self._modelInitRenderArgs))
        self._objects.addObject('Segmented Model',
                                MayaviViewerFieldworkModel('Segmented Model',
                                                           self._modelFinal,
                                                           self._GFD,
                                                           renderArgs=self._modelFinalRenderArgs))
        self._objects.addObject('Segmented Points',
                                MayaviViewerDataPoints('Segmented Points',
                                                           self._pointCloudFinal,
                                                           renderArgs=self._pointCloudRenderArgs))
        # for ln in self._landmarkNames:
        #     self._objects.addObject(ln, MayaviViewerLandmark(ln,
        #                                                      self._landmarks[ln],
        #                                                      renderArgs=self._landmarkRenderArgs
        #                                                      )
        #                             )


    def _setupGui(self):
        for m in self._distModes:
            self._ui.comboBoxDistanceMode.addItem(m)

        self._ui.lineEditXTol.setValidator(QDoubleValidator())
        self._ui.spinBoxPCsToFit.setSingleStep(1)
        self._ui.spinBoxSurfDisc.setSingleStep(1)
        self._ui.doubleSpinBoxMWeight.setSingleStep(0.1)
        self._ui.spinBoxMaxfev.setMaximum(10000)
        self._ui.spinBoxMaxfev.setSingleStep(100)

    def _saveConfig(self):
        pass
        # self._step._config['PCs to Fit'] = str(self._ui.spinBoxPCsToFit.value())
        # self._step._config['Surface Discretisation'] = str(self._ui.spinBoxSurfDisc.value())
        # self._step._config['Mahalanobis Weight'] = str(self._ui.doubleSpinBoxMWeight.value())
        # self._step._config['Max Func Evaluations'] = str(self._ui.spinBoxMaxfev.value())
        # self._step._config['xtol'] = self._ui.lineEditXTol.text()
        # self._step._config['Fit Scale'] = self._ui.checkBoxFitSize.isChecked()
        # self._step._config['Landmarks'] = self._ui.lineEditLandmarks.text()
        # self._step._config['Landmark Weights'] = self._ui.lineEditLandmarkWeights.text()

    def _initialiseSettings(self):
        pass
        # self._ui.comboBoxDistanceMode.setCurrentIndex(self._distModes.index(self._config['Distance Mode']))
        # self._ui.spinBoxPCsToFit.setValue(int(self._config['PCs to Fit']))
        # self._ui.doubleSpinBoxMWeight.setValue(float(self._config['Mahalanobis Weight']))
        # self._ui.spinBoxSurfDisc.setValue(int(self._config['Surface Discretisation']))
        # self._ui.spinBoxMaxfev.setValue(int(self._config['Max Func Evaluations']))
        # self._ui.lineEditXTol.setText(self._config['xtol'])
        # self._ui.checkBoxFitSize.setChecked(bool(self._config['Fit Scale']))
        # self._ui.lineEditLandmarks.setText(self._config['Landmarks'])
        # self._ui.lineEditLandmarkWeights.setText(self._config['Landmark Weights'])

    def _initialiseObjectTable(self):

        self._ui.tableWidget.setRowCount(self._objects.getNumberOfObjects())
        self._ui.tableWidget.verticalHeader().setVisible(False)
        self._ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._ui.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        
        self._addObjectToTable(0, 'image', self._objects.getObject('image'))
        self._addObjectToTable(1, 'Initial Model', self._objects.getObject('Initial Model'))
        self._addObjectToTable(2, 'Segmented Model', self._objects.getObject('Segmented Model'), checked=False)
        self._addObjectToTable(2, 'Segmented Points', self._objects.getObject('Segmented Points'), checked=False)
        # if self._landmarks is not None:
        #     r = 3
        #     for ln in self._landmarkNames:
        #         self._addObjectToTable(r, ln, self._objects.getObject(ln))
        #         r += 1

        self._ui.tableWidget.resizeColumnToContents(self.objectTableHeaderColumns['visible'])
        
    def _addObjectToTable(self, row, name, obj, checked=True):
        typeName = obj.typeName
        # print typeName
        # print name
        tableItem = QTableWidgetItem(name)
        if checked:
            tableItem.setCheckState(Qt.Checked)
        else:
            tableItem.setCheckState(Qt.Unchecked)

        self._ui.tableWidget.setItem(row, self.objectTableHeaderColumns['visible'], tableItem)

    def _tableItemClicked(self):
        selectedRow = self._ui.tableWidget.currentRow()
        self.selectedObjectName = self._ui.tableWidget.item(selectedRow, self.objectTableHeaderColumns['visible']).text()
        # self._populateScalarsDropDown(self.selectedObjectName)
        # print selectedRow
        # print self.selectedObjectName

    def _visibleBoxChanged(self, tableItem):

        # checked changed item is actually the checkbox
        if tableItem.column()==self.objectTableHeaderColumns['visible']:
            # get visible status
            name = tableItem.text()
            visible = tableItem.checkState().name=='Checked'

            # print 'visibleboxchanged name', name
            # print 'visibleboxchanged visible', visible

            # toggle visibility
            obj = self._objects.getObject(name)
            # print obj.name
            if obj.sceneObject:
                # print 'changing existing visibility'
                obj.setVisibility(visible)
            else:
                # print 'drawing new'
                obj.draw(self._scene)

    def _getSelectedObjectName(self):
        return self.selectedObjectName

    def _getSelectedScalarName(self):
        return 'none'

    def drawObjects(self):
        for name in self._objects.getObjectNames():
            self._objects.getObject(name).draw(self._scene)

    def _segUpdate(self, output):
        GFFitted, transformFitted, RMSEFitted, errorsFitted = output

        # update error fields
        self._ui.RMSELineEdit.setText(str(RMSEFitted))
        self._ui.meanErrorLineEdit.setText(str(errorsFitted.mean()))
        self._ui.SDLineEdit.setText(str(errorsFitted.std()))

        # update fitted GF
        fittedObj = self._objects.getObject('GF Fitted')
        fittedObj.updateGeometry(GFFitted.get_field_parameters(), self._scene)
        fittedTableItem = self._ui.tableWidget.item(2, self.objectTableHeaderColumns['visible'])
        fittedTableItem.setCheckState(Qt.Checked)

        # unlock reg ui
        self._fitUnlockUI()

    def _fitLockUI(self):
        # self._ui.comboBoxDistanceMode.setEnabled(False)
        # self._ui.spinBoxPCsToFit.setEnabled(False)
        # self._ui.spinBoxSurfDisc.setEnabled(False)
        # self._ui.doubleSpinBoxMWeight.setEnabled(False)
        # self._ui.spinBoxMaxfev.setEnabled(False)
        # self._ui.lineEditXTol.setEnabled(False)
        # self._ui.checkBoxFitSize.setEnabled(False)
        # self._ui.lineEditLandmarks.setEnabled(False)
        # self._ui.lineEditLandmarkWeights.setEnabled(False)
        self._ui.segButton.setEnabled(False)
        self._ui.resetButton.setEnabled(False)
        self._ui.acceptButton.setEnabled(False)
        self._ui.abortButton.setEnabled(False)

    def _fitUnlockUI(self):
        # self._ui.comboBoxDistanceMode.setEnabled(True)
        # self._ui.spinBoxPCsToFit.setEnabled(True)
        # self._ui.spinBoxSurfDisc.setEnabled(True)
        # self._ui.doubleSpinBoxMWeight.setEnabled(True)
        # self._ui.spinBoxMaxfev.setEnabled(True)
        # self._ui.lineEditXTol.setEnabled(True)
        # self._ui.checkBoxFitSize.setEnabled(True)
        # self._ui.lineEditLandmarks.setEnabled(True)
        # self._ui.lineEditLandmarkWeights.setEnabled(True)
        self._ui.segButton.setEnabled(True)
        self._ui.resetButton.setEnabled(True)
        self._ui.acceptButton.setEnabled(True)
        self._ui.abortButton.setEnabled(True)

    def _fitCallback(self, output):
        GFParamsFitted = output[1]
        fittedObj = self._objects.getObject('GF Fitted')
        fittedObj.updateGeometry(GFParamsFitted, self._scene)
        fittedTableItem = self._ui.tableWidget.item(2, self.objectTableHeaderColumns['visible'])
        fittedTableItem.setCheckState(Qt.Checked)

    def _reset(self):
        self._resetCallback()
        fittedObj = self._objects.getObject('GF Fitted')
        fittedObj.updateGeometry(self._GFUnfitted.field_parameters.copy(), self._scene)
        fittedTableItem = self._ui.tableWidget.item(2, self.objectTableHeaderColumns['visible'])
        fittedTableItem.setCheckState(Qt.Unchecked)

        # clear error fields
        self._ui.RMSELineEdit.clear()
        self._ui.meanErrorLineEdit.clear()
        self._ui.SDLineEdit.clear()

    def _accept(self):
        self._close()

    def _abort(self):
        self._reset()
        self._close()

    def _close(self):
        for name in self._objects.getObjectNames():
            self._objects.getObject(name).remove()

        self._objects._objects = {}
        self._objects == None

        # for r in xrange(self._ui.tableWidget.rowCount()):
        #     self._ui.tableWidget.removeRow(r)

    def _refresh(self):
        for r in range(self._ui.tableWidget.rowCount()):
            tableItem = self._ui.tableWidget.item(r, self.objectTableHeaderColumns['visible'])
            name = tableItem.text()
            visible = tableItem.checkState().name=='Checked'
            obj = self._objects.getObject(name)
            # print obj.name
            if obj.sceneObject:
                # print 'changing existing visibility'
                obj.setVisibility(visible)
            else:
                # print 'drawing new'
                obj.draw(self._scene)

    def _saveScreenShot(self):
        filename = self._ui.screenshotFilenameLineEdit.text()
        width = int(self._ui.screenshotPixelXLineEdit.text())
        height = int(self._ui.screenshotPixelYLineEdit.text())
        self._scene.mlab.savefig( filename, size=( width, height ) )
