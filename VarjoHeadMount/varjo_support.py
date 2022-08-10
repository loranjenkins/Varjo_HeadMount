import os
import ctypes

if __name__ == '__main__':

    # import dll and define return types for all functions
    _dll_handle = ctypes.windll.LoadLibrary(
        os.path.join('C:\\', 'Users', 'localadmin', 'Desktop', 'varjo-sdk', 'bin', 'VarjoLib.dll'))

    _dll_handle.varjo_SessionInit.restype = ctypes.POINTER(ctypes.c_void_p)
    _dll_handle.varjo_GetCurrentTime.restype = ctypes.c_int64


    # Initialize session
    varjo_session_pointer = _dll_handle.varjo_SessionInit()

    trigger = True
    while trigger == True:
        try:
            time = _dll_handle.varjo_GetCurrentTime(varjo_session_pointer)
            print('Time since epoch in nanosecond:', time)

        except:
            trigger = False

    _dll_handle.varjo_SessionShutDown(varjo_session_pointer)
