
import os
from PySide import QtGui
from mapclientplugins.asmsegmentationstep.ui_configuredialog import Ui_Dialog
# from ui_configuredialog import Ui_Dialog

INVALID_STYLE_SHEET = 'background-color: rgba(239, 0, 0, 50)'
DEFAULT_STYLE_SHEET = ''

class ConfigureDialog(QtGui.QDialog):
    '''
    Configure dialog to present the user with the options to configure this step.
    '''

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QtGui.QDialog.__init__(self, parent)
        
        self._ui = Ui_Dialog()
        self._ui.setupUi(self)

        # Keep track of the previous identifier so that we can track changes
        # and know how many occurrences of the current identifier there should
        # be.
        self._previousIdentifier = ''
        self._previousConfig = ''
        self._previousPPC = ''
        # Set a place holder for a callable that will get set from the step.
        # We will use this method to decide whether the identifier is unique.
        self.identifierOccursCount = None

        self._makeConnections()

    def _makeConnections(self):
        self._ui.idLineEdit.textChanged.connect(self.validate)
        self._ui.configButton.clicked.connect(self._configClicked)
        self._ui.configLineEdit.textChanged.connect(self._configEdited)
        self._ui.ppcButton.clicked.connect(self._ppcClicked)
        self._ui.ppcLineEdit.textChanged.connect(self._ppcEdited)

    def accept(self):
        '''
        Override the accept method so that we can confirm saving an
        invalid configuration.
        '''
        result = QtGui.QMessageBox.Yes
        if not self.validate():
            result = QtGui.QMessageBox.warning(self, 'Invalid Configuration',
                'This configuration is invalid.  Unpredictable behaviour may result if you choose \'Yes\', are you sure you want to save this configuration?)',
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if result == QtGui.QMessageBox.Yes:
            QtGui.QDialog.accept(self)

    def validate(self):
        '''
        Validate the configuration dialog fields.  For any field that is not valid
        set the style sheet to the INVALID_STYLE_SHEET.  Return the outcome of the 
        overall validity of the configuration.
        '''
        # Determine if the current identifier is unique throughout the workflow
        # The identifierOccursCount method is part of the interface to the workflow framework.
        idValue = self.identifierOccursCount(self._ui.idLineEdit.text())
        idValid = (idValue == 0) or (idValue == 1 and self._previousIdentifier == self._ui.idLineEdit.text())
        if idValid:
            self._ui.idLineEdit.setStyleSheet(DEFAULT_STYLE_SHEET)
        else:
            self._ui.idLineEdit.setStyleSheet(INVALID_STYLE_SHEET)

        # if empty, can use default
        if self._ui.configLineEdit.text()!='':
            configValid = os.path.exists(self._ui.configLineEdit.text())
        else:
            configValid = True
        if configValid:
            self._ui.configLineEdit.setStyleSheet(DEFAULT_STYLE_SHEET)
        else:
            self._ui.configLineEdit.setStyleSheet(INVALID_STYLE_SHEET)
            
        ppcValid = os.path.exists(self._ui.ppcLineEdit.text())
        if ppcValid:
            self._ui.ppcLineEdit.setStyleSheet(DEFAULT_STYLE_SHEET)
        else:
            self._ui.ppcLineEdit.setStyleSheet(INVALID_STYLE_SHEET)

        valid = idValid and configValid and ppcValid
        self._ui.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(idValid)

        return valid

    def getConfig(self):
        '''
        Get the current value of the configuration from the dialog.  Also
        set the _previousIdentifier value so that we can check uniqueness of the
        identifier over the whole of the workflow.
        '''
        self._previousIdentifier = self._ui.idLineEdit.text()
        self._previousConfig = self._ui.configLineEdit.text()
        self._previousPPC = self._ui.ppcLineEdit.text()
        config = {}
        config['identifier'] = self._ui.idLineEdit.text()
        config['paramFileLoc'] = self._ui.configLineEdit.text()
        config['ppcFileLoc'] = self._ui.ppcLineEdit.text()
        if self._ui.guiCheckBox.isChecked():
            config['GUI'] = 'True'
        else:
            config['GUI'] = 'False'
        return config

    def setConfig(self, config):
        '''
        Set the current value of the configuration for the dialog.  Also
        set the _previousIdentifier value so that we can check uniqueness of the
        identifier over the whole of the workflow.
        '''
        self._previousIdentifier = config['identifier']
        self._ui.idLineEdit.setText(config['identifier'])
        self._ui.configLineEdit.setText(config['paramFileLoc'])
        self._ui.ppcLineEdit.setText(config['ppcFileLoc'])
        if config['GUI']=='True':
            self._ui.guiCheckBox.setChecked(bool(True))
        else:
            self._ui.guiCheckBox.setChecked(bool(False))

    def _configClicked(self):
        location = QtGui.QFileDialog.getOpenFileName(self, 'Select File Location', self._previousConfig)
        if location[0]:
            self._previousConfig = location[0]
            self._ui.configLineEdit.setText(location[0])

    def _configEdited(self):
        self.validate()

    def _ppcClicked(self):
        location = QtGui.QFileDialog.getOpenFileName(self, 'Select File Location', self._previousPPC)
        if location[0]:
            self._previousConfig = location[0]
            self._ui.ppcLineEdit.setText(location[0])

    def _ppcEdited(self):
        self.validate()
