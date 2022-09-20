from PyQt5.QtWidgets import QDialog, QApplication

from participantUI.participantinfodialog_ui import Ui_Dialog

class ParticipantInfoDialog(QDialog):
    def __init__(self, participant_id):
        super().__init__()

        self.participant_info = {'id': participant_id,
                                 'age': None,
                                 'gender': None}

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.idLineEdit.setText(str(participant_id))

        self.ui.ageSpinBox.valueChanged.connect(self._set_age)

        for radio_button in [self.ui.femaleRadioButton, self.ui.maleRadioButton, self.ui.otherRadioButton, self.ui.unknownRadioButton]:
            radio_button.toggled.connect(self._set_gender)

        self.show()

    def _set_age(self):
        self.participant_info['age'] = self.ui.ageSpinBox.value()

    def _set_gender(self):
        if self.ui.femaleRadioButton.isChecked():
            self.participant_info['gender'] = 'female'
        elif self.ui.maleRadioButton.isChecked():
            self.participant_info['gender'] = 'male'
        elif self.ui.otherRadioButton.isChecked():
            self.participant_info['gender'] = 'other'
        elif self.ui.unknownRadioButton.isChecked():
            self.participant_info['gender'] = 'unknown'
        else:
            self.participant_info['gender'] = None