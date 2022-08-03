if __name__ == '__main__':
    # import dll and define return types for all functions
    _dll_handle = ctypes.windll.LoadLibrary(
        os.path.join('C:\\', 'Users', 'localadmin', 'Desktop', 'varjo-sdk', 'bin', 'VarjoLib.dll'))

    _dll_handle.varjo_IsAvailable.restype = ctypes.c_bool
    _dll_handle.varjo_GetErrorDesc.restype = ctypes.POINTER(ctypes.c_char * 50)

    _dll_handle.varjo_GetError.restype = ctypes.c_int64


    varjo_session_pointer = _dll_handle.varjo_SessionInit()

    error = _dll_handle.varjo_GetError(varjo_session_pointer)

    print(_dll_handle.varjo_IsAvailable())
    print(_dll_handle.varjo_GetError(varjo_session_pointer))  # 1 means error
    print('-------------------------')
    print(_dll_handle.varjo_GetErrorDesc(error).contents.value.decode())
    print('-------------------------')

    _dll_handle.varjo_SessionShutDown(varjo_session_pointer)