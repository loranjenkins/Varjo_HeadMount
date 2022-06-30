import os

import ctypes
import sys

from VarjoHeadMount._state import Session, SessionInit

# import dll and define return types for all functions
_sys_arch = 'x64' if sys.maxsize > 2 ** 32 else 'x86'
_dll_handle = ctypes.windll.LoadLibrary(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib', _sys_arch, 'VarjoLib.dll'))

_dll_handle.varjo_FrameGetDisplayTime.restype = ctypes.POINTER(Session)  # nanoseconds from epoch
_dll_handle.varjo_FrameGetPose.restype = ctypes.POINTER(Session)  # pose matrix


def get_time(POINTER) -> State:
    """
    Call this function to get nanoseconds from epoch
    """

    return _dll_handle.FrameGetDisplayTime()

def get_headpose(POINTER, posetype: int):
    """
    Call this function to get headpose matrix
    """

    return _dll_handle.varjo_FrameGetPose(ctypes.c_int(posetype))



#####comments olger
# If we complete this, is it possible record in varjo base with XY gaze and frame seconds and allign this data for headset pose

#since we cannot get the video from api?


# we get both already from standaard application output
# _dll_handle.varjo_FrameGetDisplayTime.restype = ctypes.POINTER()        #nanoseconds from epoch
# _dll_handle.varjo_GetGaze.restype = ctypes.POINTER()        #all the needed eye data
