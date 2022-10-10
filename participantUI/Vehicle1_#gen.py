from datetime import datetime
import sys
import os
import random
from pathlib import Path

from PyQt5.QtWidgets import QDialog, QApplication
from participantUI.participantdialog import ParticipantInfoDialog

def write_participant_numbers(numbers: list):
    script_dir = Path(__file__).parent.parent

    path_to_file = os.path.join(script_dir, 'data', 'participantinfo', 'all_participants#_vehicle1.txt')

    with open(path_to_file, 'a') as f:
        for number in numbers:
            f.write(str(number) + '\n')

def get_used_participant_numbers():
    script_dir = Path(__file__).parent.parent

    all_numbers = []

    path_to_file = os.path.join(script_dir, 'data', 'participantinfo', 'all_participants#_vehicle1.txt')

    if os.path.exists(path_to_file):
        with open(path_to_file, 'r') as f:
            for line in f:
                all_numbers.append(int(line))
    else:
        with open(os.path.join(script_dir, 'data', 'participantinfo', 'all_participants#_vehicle1.txt'), 'w'):
            pass

    return all_numbers

def save_participant_info(path, number):
    with open(os.path.join(path, 'participant#_vehicle1_{}.txt'.format(datetime.now().strftime("%Y-%m-%d %H-%M-%S"))), 'a') as f:
        f.write(str(number) + '\n')

if __name__ == '__main__':


    # generate participant numbers
    all_used_numbers = get_used_participant_numbers()
    participant_numbers = {'vehicle_1': []}

    for key in participant_numbers:
        participant_numbers[key] = random.randint(1000, 9999)
        while participant_numbers[key] in all_used_numbers:
            participant_numbers[key] = random.randint(1000, 9999)

    write_participant_numbers(participant_numbers.values())

    app = QApplication(sys.argv)
    right_dialog = ParticipantInfoDialog(participant_numbers['vehicle_1'])

    right_dialog.accepted.connect(lambda: save_participant_info('C:\\Users\localadmin\PycharmProjects\Varjo_HeadMount\data\participantinfo', right_dialog.participant_info))

    sys.exit(app.exec_())

