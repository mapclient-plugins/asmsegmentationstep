
'''
MAP Client Plugin Step
'''
import os

from PySide import QtGui
from PySide import QtCore

from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint
from mapclientplugins.asmsegmentationstep.configuredialog import ConfigureDialog
from mapclientplugins.asmsegmentationstep.mayaviasmsegmentationviewerwidget import MayaviASMSegmentationViewerWidget
from mapclientplugins.asmsegmentationstep import asmseg

# from configuredialog import ConfigureDialog
# from mayaviasmsegmentationviewerwidget import MayaviASMSegmentationViewerWidget
# import asmseg

import configobj
import copy

class ASMSegmentationStep(WorkflowStepMountPoint):
    '''
    Skeleton step which is intended to be a helpful starting point
    for new steps.
    '''

    def __init__(self, location):
        super(ASMSegmentationStep, self).__init__('ASM Segmentation', location)
        self._configured = False # A step cannot be executed until it has been configured.
        self._category = 'Segmentation'
        # Add any other initialisation code here:
        # Ports:
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#gias-scan'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'ju#fieldworkmodel'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'ju#principalcomponents'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#provides',
                      'ju#fieldworkmode'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#provides',
                      'ju#geometrictransform'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#provides',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#pointcloud'))
        self._config = {}
        self._config['identifier'] = ''
        self._config['paramFileLoc'] = ''
        self._config['ppcFileLoc'] = ''
        self._config['GUI'] = 'True'

        self._gui = True
        self._scan = None
        self._shapepcs = None
        self._model = None
        self._modelInit = None
        self._modelFinal = None
        self._transformFinal = None
        self._pointCloudFinal = None
        self._segParams = None
        self._asmOutput = None

    def execute(self):
        '''
        Add your code here that will kick off the execution of the step.
        Make sure you call the _doneExecution() method when finished.  This method
        may be connected up to a button in a widget for example.
        '''
        # Put your execute step code here before calling the '_doneExecution' method.

        # load params file
        self._loadParams()

        if self._gui:
            # start gui
            self._widget = MayaviASMSegmentationViewerWidget(self)
            
            # self._widget._ui.registerButton.clicked.connect(self._register)
            # self._widget._ui.acceptButton.clicked.connect(self._doneExecution)
            # self._widget._ui.abortButton.clicked.connect(self._abort)
            # self._widget._ui.resetButton.clicked.connect(self._reset)
            self._widget.setModal(True)
            self._setCurrentWidget(self._widget)
        else:
            self._segment()
            self._doneExecution()

    def _loadParams(self):
        if self._config['paramFileLoc']=='':
            paramFileLoc = os.path.join(os.path.dirname(__file__), 'default_params.ini')
            self._segParams = configobj.ConfigObj(paramFileLoc, unrepr=True)
        else:
            self._segParams = configobj.ConfigObj(self._config['paramFileLoc'], unrepr=True)

        self._segParams['data_files']['ppc_filename'] = self._config['ppcFileLoc']

    def _segment(self):
        segModel, segPoints,\
        segTransform, asmOutput = asmseg.segment(
                                                 self._scan,
                                                 self._model,
                                                 self._shapepcs, 
                                                 self._segParams
                                                 )
        self._modelFinal = segModel
        self._model = segModel
        self._pointCloudFinal = segPoints
        self._transformFinal = segTransform
        self._asmOutput = asmOutput

    def setPortData(self, index, dataIn):
        '''
        Add your code here that will set the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        uses port for this step then the index can be ignored.
        '''
        if index == 0:
            self._scan = dataIn # ju#scan
        elif index == 1:
            self._model = dataIn # ju#fieldworkmodel
            self._modelInit = copy.deepcopy(self._model)
            self._modelFinal = copy.deepcopy(self._model)
        else:
            self._shapepcs = dataIn # ju#principalcomponents

    def getPortData(self, index):
        '''
        Add your code here that will return the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        provides port for this step then the index can be ignored.
        '''
        if index == 3:
            return self._modelFinal
        elif index == 4:
            return self._transformFinal
        else:
            return self._pointCloudFinal

    def configure(self):
        '''
        This function will be called when the configure icon on the step is
        clicked.  It is appropriate to display a configuration dialog at this
        time.  If the conditions for the configuration of this step are complete
        then set:
            self._configured = True
        '''
        dlg = ConfigureDialog()
        dlg.identifierOccursCount = self._identifierOccursCount
        dlg.setConfig(self._config)
        dlg.validate()
        dlg.setModal(True)
        
        if dlg.exec_():
            self._config = dlg.getConfig()
        
        self._configured = dlg.validate()
        self._configuredObserver()

    def getIdentifier(self):
        '''
        The identifier is a string that must be unique within a workflow.
        '''
        return self._config['identifier']

    def setIdentifier(self, identifier):
        '''
        The framework will set the identifier for this step when it is loaded.
        '''
        self._config['identifier'] = identifier

    def serialize(self, location):
        '''
        Add code to serialize this step to disk.  The filename should
        use the step identifier (received from getIdentifier()) to keep it
        unique within the workflow.  The suggested name for the file on
        disk is:
            filename = getIdentifier() + '.conf'
        '''
        configuration_file = os.path.join(location, self.getIdentifier() + '.conf')
        conf = QtCore.QSettings(configuration_file, QtCore.QSettings.IniFormat)
        conf.beginGroup('config')
        conf.setValue('identifier', self._config['identifier'])
        conf.setValue('paramFileLoc', self._config['paramFileLoc'])
        conf.setValue('ppcFileLoc', self._config['ppcFileLoc'])
        if self._gui:
            self._config['GUI'] = 'True'
        else:
            self._config['GUI'] = 'False'
        conf.setValue('GUI', self._config['GUI'])
        conf.endGroup()


    def deserialize(self, location):
        '''
        Add code to deserialize this step from disk.  As with the serialize 
        method the filename should use the step identifier.  Obviously the 
        filename used here should be the same as the one used by the
        serialize method.
        '''
        configuration_file = os.path.join(location, self.getIdentifier() + '.conf')
        conf = QtCore.QSettings(configuration_file, QtCore.QSettings.IniFormat)
        conf.beginGroup('config')
        self._config['identifier'] = conf.value('identifier', '')
        self._config['paramFileLoc'] = conf.value('paramFileLoc', '')
        self._config['ppcFileLoc'] = conf.value('ppcFileLoc', '')
        self._config['GUI'] = conf.value('GUI', 'True')
        conf.endGroup()

        d = ConfigureDialog()
        d.identifierOccursCount = self._identifierOccursCount
        d.setConfig(self._config)
        self._configured = d.validate()

        if self._config['GUI']=='True':
            self._gui = True
        else:
            self._gui = False


