import os
import ctypes
from datetime import datetime
import pandas as pd

class Matrix4x4(ctypes.Structure):
    _fields_ = [
        ('value', ctypes.c_double * 16),
    ]

class varjo_ViewInfo(ctypes.Structure):
    _fields_ = [
        ('enabled', ctypes.c_int32),
        ('preferredHeight', ctypes.c_int32),
        ('preferredWidth', ctypes.c_int32),
        ('projectionMatrix', ctypes.c_double * 16),
        ('reserved', ctypes.c_int32),
        ('viewMatrix', ctypes.c_double * 16),
    ]

class varjo_FrameInfo(ctypes.Structure):
    _fields_ = [
        ('displayTime', ctypes.c_int64),
        ('frameNumber', ctypes.c_int64),
        ('views', varjo_ViewInfo),
    ]

class varjo_Ray(ctypes.Structure):
    _fields_ = [
        ('forward', ctypes.c_double * 3),
        ('origin', ctypes.c_double * 3),
    ]

class varjo_Gaze(ctypes.Structure):
    _fields_ = [
        ('captureTime', ctypes.c_int64),
        ('focusDistance', ctypes.c_double),
        ('frameNumber', ctypes.c_int64),
        ('gaze', varjo_Ray),
        ('leftEye', varjo_Ray),
        ('leftPupilSize', ctypes.c_double),
        ('leftStatus', ctypes.c_int64),
        ('rightEye', varjo_Ray),
        ('rightPupilSize', ctypes.c_double),
        ('rightStatus', ctypes.c_int64),
        ('stability', ctypes.c_double),
        ('status', ctypes.c_int64),
    ]

if __name__ == '__main__':

    # import dll and define return types for all functions
    _dll_handle = ctypes.windll.LoadLibrary(
        os.path.join('C:\\', 'Users', 'localadmin', 'Desktop', 'varjo-sdk', 'bin', 'VarjoLib.dll'))

    _dll_handle.varjo_FrameGetPose.restype = Matrix4x4
    _dll_handle.varjo_GetCurrentTime.restype = ctypes.c_uint64
    _dll_handle.varjo_IsAvailable.restype = ctypes.c_bool
    _dll_handle.varjo_GetErrorDesc.restype = ctypes.POINTER(
        ctypes.c_char * 50)
    _dll_handle.varjo_GetError.restype = ctypes.c_int64
    _dll_handle.varjo_GetViewCount.restype = ctypes.c_int32
    _dll_handle.varjo_SessionInit.restype = ctypes.POINTER(ctypes.c_void_p)
    _dll_handle.varjo_FrameGetDisplayTime.restype = ctypes.c_int64
    _dll_handle.varjo_GetCurrentTime.restype = ctypes.c_int64
    # _dll_handle.varjo_ViewInfo.restype = ctypes.POINTER(ViewInfo)

    # _dll_handle.varjo_PropertyKey_HMDConnected.restype = ctypes.c_int64


    #Initialize running session on varjo base
    varjo_session_pointer = _dll_handle.varjo_SessionInit()

    #Check if session is initialized correctly
    GetError = _dll_handle.varjo_GetError(varjo_session_pointer)
    print(_dll_handle.varjo_IsAvailable())
    print(_dll_handle.varjo_GetError(varjo_session_pointer))
    print('-------------------------')
    print(_dll_handle.varjo_GetErrorDesc(GetError).contents.value.decode())
    print('-------------------------')
    print(_dll_handle.varjo_GetViewCount(varjo_session_pointer))

    #Initialize Pointer
    _dll_handle.varjo_CreateFrameInfo.restype = ctypes.POINTER(varjo_FrameInfo)
    varjo_frameinfo_pointer = _dll_handle.varjo_CreateFrameInfo(varjo_session_pointer)

    #Forward gaze functions
    _dll_handle.varjo_GazeInit.restype = ctypes.c_void_p
    _dll_handle.varjo_RequestGazeCalibration.restype = ctypes.c_void_p
    _dll_handle.varjo_GetGaze.restype = varjo_Gaze

    _dll_handle.varjo_GazeInit(varjo_session_pointer)
    _dll_handle.varjo_RequestGazeCalibration(varjo_session_pointer)


    # Varjo_live_dict = {'FrameDisplayTime': [], 'GetCurrentTime': [], 'DateTimeMilliseconds': [], 'HMD_rotation': [], 'gaze_forward': [], 'epoch': []}
    Varjo_live_dict = {'epoch_vehicle2': [], 'HMD_rotation_vehicle2': [],'gaze_forward_vehicle2': []}

    # Collect data in loop and write to csv
    trigger = True
    while trigger == True:
        try:
            _dll_handle.varjo_WaitSync(varjo_session_pointer, varjo_frameinfo_pointer)
            matrix = _dll_handle.varjo_FrameGetPose(varjo_session_pointer, ctypes.c_int64(2))
            matrix = list(matrix.value)
            HMD_rotation = matrix[10]
            Varjo_live_dict['HMD_rotation_vehicle2'].append(HMD_rotation)

            gaze = _dll_handle.varjo_GetGaze(varjo_session_pointer)
            gaze_forward = list(gaze.gaze.forward)
            Varjo_live_dict['gaze_forward_vehicle2'].append(gaze_forward)

            time_now = datetime.utcnow()
            epoch_time = int((time_now - datetime(1970, 1, 1)).total_seconds()*1000000000)
            Varjo_live_dict['epoch_vehicle2'].append(epoch_time)

            # gaze_stability = gaze.stability
            # Varjo_live_dict['gaze_stability'].append(gaze_stability)
            # epoch = _dll_handle.varjo_FrameGetDisplayTime(varjo_session_pointer)
            # Varjo_live_dict['FrameDisplayTime'].append(epoch)
            #
            # time = _dll_handle.varjo_GetCurrentTime(varjo_session_pointer)
            # Varjo_live_dict['GetCurrentTime'].append(time)
            #
            # dt = datetime.fromtimestamp(time / 1000000000)
            # Varjo_live_dict['DateTimeMilliseconds'].append(dt)

            print('Epoch:', epoch_time, 'Pose:', HMD_rotation)

        except:
            trigger = False


    df = pd.DataFrame.from_dict(Varjo_live_dict)
    df.to_csv('C:\\Users\localadmin\PycharmProjects\Varjo_HeadMount\data\Varjo_data_vehicle2{}.csv'.format(datetime.now().strftime("%Y-%m-%d %H%M%S")), index=False)

    _dll_handle.varjo_SessionShutDown(varjo_session_pointer)