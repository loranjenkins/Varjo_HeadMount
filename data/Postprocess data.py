import pandas as pd
import datetime
import os
current_directory = os.getcwd()
print(current_directory)

data_base = pd.read_csv(
    r'C:\Users\localadmin\PycharmProjects\Varjo_HeadMount\data\varjo_gaze_output_2022-08-10_15-12-29-922.csv',
    sep=',')

def get_timestamps(data, intcolumnname):
    time = []
    for i in range(len(data.iloc[:, intcolumnname])):
        epoch_in_nanoseconds = data.iloc[i, intcolumnname]
        epoch_in_seconds = epoch_in_nanoseconds / 1000000000
        # we need to remove doubles??
        datetimes = datetime.datetime.fromtimestamp(epoch_in_seconds)
        time.append(datetimes)
    return time

time_in_datetime = get_timestamps(data_base, 0)
print(list(time_in_datetime))
print(list(data_base['raw_timestamp'])
time_in_seconds_trail = [(a - time_in_datetime[0]).total_seconds() for a in time_in_datetime]
print(time_in_seconds_trail)