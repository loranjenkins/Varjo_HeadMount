import sys
import os
import random
from PyQt5.QtWidgets import QDialog, QApplication
from participantUI.participantdialog import ParticipantInfoDialog

def write_participant_numbers(numbers: list):
    path_to_file = os.path.join('C:\\Users\localadmin\PycharmProjects\Varjo_HeadMount', 'data', 'participants#_vehicle1.txt')

    with open(path_to_file, 'a') as f:
        for number in numbers:
            f.write(str(number) + '\n')

def get_used_participant_numbers():
    all_numbers = []

    path_to_file = os.path.join('C:\\Users\localadmin\PycharmProjects\Varjo_HeadMount', 'data', 'participants#_vehicle1.txt')

    if os.path.exists(path_to_file):
        with open(path_to_file, 'r') as f:
            for line in f:
                all_numbers.append(int(line))
    else:
        with open(os.path.join('C:\\Users\localadmin\PycharmProjects\Varjo_HeadMount', 'data', 'participants#_vehicle1.txt'), 'w'):
            pass

    return all_numbers

def save_participant_info(path, number):
    with open(os.path.join(path, 'participant#1.txt'), 'a') as f:
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

    experiment_number = 1

    app = QApplication(sys.argv)
    right_dialog = ParticipantInfoDialog(participant_numbers['vehicle_1'])


    right_dialog.accepted.connect(lambda: save_participant_info('C:\\Users\localadmin\PycharmProjects\Varjo_HeadMount\data\participantinfo', right_dialog.participant_info))


    sys.exit(app.exec_())

    # right_dialog.rejected.connect(
    #     lambda: save_participant_info(os.path.join('C:\\Users\localadmin\PycharmProjects\Varjo_HeadMount', 'data', 'experiment_'),
    #                                   right_dialog.participant_info))