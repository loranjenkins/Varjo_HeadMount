import os
import time
import ctypes
import sys


#
# from VarjoHeadMount._state import Session, SessionInit
#
# # import dll and define return types for all functions
# _sys_arch = 'x64' if sys.maxsize > 2 ** 32 else 'x86'
# _dll_handle = ctypes.windll.LoadLibrary(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib', _sys_arch, 'VarjoLib.dll'))
#
# _dll_handle.varjo_FrameGetDisplayTime.restype = ctypes.POINTER(Session)  # nanoseconds from epoch
# _dll_handle.varjo_FrameGetPose.restype = ctypes.POINTER(Session)  # pose matrix
#
#
# def get_time(POINTER) -> State:
#     """
#     Call this function to get nanoseconds from epoch
#     """
#
#     return _dll_handle.FrameGetDisplayTime()
#
# def get_headpose(POINTER, posetype: int):
#     """
#     Call this function to get headpose matrix
#     """
#
#     return _dll_handle.varjo_FrameGetPose(ctypes.c_int(posetype))
import numpy as np


class Matrix4x4(ctypes.Structure):
    _fields_ = [
        ('value', ctypes.c_double * 16),
    ]


if __name__ == '__main__':
    # import dll and define return types for all functions
    _dll_handle = ctypes.windll.LoadLibrary(
        os.path.join('C:\\', 'Users', 'localadmin', 'Desktop', 'varjo-sdk', 'bin', 'VarjoLib.dll'))

    _dll_handle.varjo_FrameGetPose.restype = Matrix4x4
    _dll_handle.varjo_GetCurrentTime.restype = ctypes.c_uint64
    _dll_handle.varjo_IsGazeAllowed.restype = ctypes.c_bool
    _dll_handle.varjo_GetVersion.restype = ctypes.c_int64
    _dll_handle.varjo_IsAvailable.restype = ctypes.c_bool
    _dll_handle.varjo_GetErrorDesc.restype = ctypes.POINTER(ctypes.c_char * 50) #search ctypes convert pointer to char array
    _dll_handle.varjo_GetError.restype = ctypes.c_int64

    _dll_handle.varjo_PropertyKey_HMDConnected = ctypes.c_int64
    _dll_handle.varjo_GetPropertyBool.restype = ctypes.c_bool

    _dll_handle.varjo_GetError.restype = ctypes.c_int64

    varjo_session_pointer = _dll_handle.varjo_SessionInit()
    a = _dll_handle.varjo_GetError(varjo_session_pointer)

    print(_dll_handle.varjo_IsAvailable())
    print(_dll_handle.varjo_GetError(varjo_session_pointer)) #1 means error
    print('-------------------------')
    print(_dll_handle.varjo_GetErrorDesc(a).contents.value.decode())
    print('-------------------------')
    # print(_dll_handle.varjo_GetVersion())
    # print(_dll_handle.varjo_RequestGazeCalibration(varjo_session_pointer))



    matrix = _dll_handle.varjo_FrameGetPose(varjo_session_pointer, ctypes.c_int(2))

    print(_dll_handle.varjo_GetPropertyBool(varjo_session_pointer, ctypes.c_bool()))

    # for i in range(5):
    #     # _dll_handle.varjo_RequestGazeCalibration(varjo_session_pointer)
    #     # print(_dll_handle.varjo_GetCurrentTime(varjo_session_pointer))
    #     # print(_dll_handle.varjo_GetViewCount(varjo_session_pointer))
    #     print(_dll_handle.varjo_IsGazeAllowed(varjo_session_pointer))
    #     # print(_dll_handle.varjo_FrameGetDisplayTime(varjo_session_pointer))
    #     # print(list(matrix.value))
    #     time.sleep(1)

    _dll_handle.varjo_SessionShutDown(varjo_session_pointer)


