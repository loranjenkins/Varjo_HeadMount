from PyQt5.QtWidgets import QDialog, QApplication

from participantUI.participantinfodialog_ui import Ui_Dialog

class ParticipantInfoDialog(QDialog):
    def __init__(self, participant_id):
        super().__init__()

        self.participant_info = {'id': participant_id}

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.idLineEdit.setText(str(participant_id))

        self.show()


