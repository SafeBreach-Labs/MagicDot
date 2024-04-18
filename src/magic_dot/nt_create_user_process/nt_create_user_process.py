import ctypes
import os
from ctypes import *
from ctypes.wintypes import *

from magic_dot.file_utils import nt_path, dos_path
from . import ntdll

class UNICODE_STRING(Structure):
    _fields_ = [('Length', USHORT), 
				('MaximumLength', USHORT), 
				('Buffer', POINTER(WCHAR))]
    
    def get_string(self):
        return ctypes.string_at(self.Buffer, self.Length).decode('utf-16-le')
     
     
# class _RTL_USER_PROCESS_PARAMETERS(Structure):
#     _fields_ = [
#     ("MaximumLength", ULONG),
#     ("Length", ULONG),
#     ("Flags", ULONG),
#     ("DebugFlags", ULONG),
#     ("ConsoleHandle", HANDLE),
#     ("Reserved1", BYTE * 16),
#     ("Reserved2", c_void_p * 10),
#     ("ImagePathName", UNICODE_STRING),
#     ("CommandLine", UNICODE_STRING),
# ]
# PRTL_USER_PROCESS_PARAMETERS = POINTER(_RTL_USER_PROCESS_PARAMETERS)
# RTL_USER_PROCESS_PARAMETERS = _RTL_USER_PROCESS_PARAMETERS

RTL_USER_PROCESS_PARAMETERS_NORMALIZED = 1

PS_ATTRIBUTE_IMAGE_NAME = 0x20005
THREAD_ALL_ACCESS = 0x1fffff
PROCESS_ALL_ACCESS = 0x1fffff

PROCESS_CREATE_FLAGS_CREATE_SUSPENDED = 0x00000200
THREAD_CREATE_FLAGS_CREATE_SUSPENDED = 0x00000001

CONSOLE_HANDLE_CREATE_NO_WINDOW = -3


def RtlInitUnicodeString(dst_unicode_str, src_wchar_buffer):
	memset(addressof(dst_unicode_str), 0, sizeof(dst_unicode_str))
	dst_unicode_str.Buffer = cast(src_wchar_buffer, POINTER(WCHAR))
	dst_unicode_str.Length = sizeof(src_wchar_buffer) - 2 # Excluding terminating NULL character
	dst_unicode_str.MaximumLength = dst_unicode_str.Length


def nt_create_user_process(exe_path, custom_cmdline=None, current_directory=None, hide_console_window: bool = False, nt_process_create_flags: int = 0, nt_thread_create_flags: int = 0) -> HANDLE:
    exe_path = dos_path(exe_path)
    
    if None == custom_cmdline:
        custom_cmdline = exe_path
    
    if None == current_directory:
        current_directory = os.path.dirname(exe_path)

    nt_exe_path_unicode_buffer = create_unicode_buffer(nt_path(exe_path))
    nt_exe_path_unicode_string = UNICODE_STRING()
    RtlInitUnicodeString(nt_exe_path_unicode_string, nt_exe_path_unicode_buffer)

    cmdline_unicode_buffer = create_unicode_buffer(custom_cmdline)
    cmdline_unicode_string = UNICODE_STRING()
    RtlInitUnicodeString(cmdline_unicode_string, cmdline_unicode_buffer)

    current_directory_unicode_buffer = create_unicode_buffer(current_directory)
    current_directory_unicode_string = UNICODE_STRING()
    RtlInitUnicodeString(current_directory_unicode_string, current_directory_unicode_buffer)

    process_parameters = ntdll.PRTL_USER_PROCESS_PARAMETERS()

    ctypes.windll.ntdll.RtlCreateProcessParametersEx.restype = c_ulong
    nt_status = ctypes.windll.ntdll.RtlCreateProcessParametersEx(byref(process_parameters), byref(nt_exe_path_unicode_string), None, byref(current_directory_unicode_string), byref(cmdline_unicode_string), None, None, None, None, None, RTL_USER_PROCESS_PARAMETERS_NORMALIZED)
    if nt_status != 0:
        raise OSError(f"RtlCreateProcessParametersEx returned an error nt status: {hex(nt_status)}")

    if hide_console_window:
        process_parameters.contents.ConsoleHandle = CONSOLE_HANDLE_CREATE_NO_WINDOW

    create_info = ntdll.PS_CREATE_INFO()
    memset(byref(create_info), 0, sizeof(create_info))
    create_info.Size = sizeof(create_info)
    create_info.State = ntdll.PsCreateInitialState


    attribute_list = cast(create_string_buffer(sizeof(ntdll.PS_ATTRIBUTE) + sizeof(c_uint64)), ntdll.PPS_ATTRIBUTE_LIST)
    memset(attribute_list, 0, sizeof(ntdll.PS_ATTRIBUTE))
    attribute_list.contents.TotalLength = sizeof(ntdll.PS_ATTRIBUTE_LIST) - sizeof(ntdll.PS_ATTRIBUTE)
    attribute_list.contents.Attributes[0].Attribute = PS_ATTRIBUTE_IMAGE_NAME
    attribute_list.contents.Attributes[0].Size = nt_exe_path_unicode_string.Length
    attribute_list.contents.Attributes[0].Value = cast(nt_exe_path_unicode_string.Buffer, ctypes.c_void_p).value

    process_handle = HANDLE()
    thread_handle = HANDLE()

    ctypes.windll.ntdll.NtCreateUserProcess.restype = c_ulong
    nt_status = ctypes.windll.ntdll.NtCreateUserProcess(byref(process_handle), byref(thread_handle), PROCESS_ALL_ACCESS, THREAD_ALL_ACCESS, None, None, nt_process_create_flags, nt_thread_create_flags, process_parameters, byref(create_info), attribute_list)
    if nt_status != 0:
        raise OSError(f"NtCreateUserProcess returned an error nt status: {hex(nt_status)}")

    return process_handle

