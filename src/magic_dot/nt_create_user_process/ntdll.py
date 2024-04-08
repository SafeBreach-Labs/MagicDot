# -*- coding: utf-8 -*-
#
# TARGET arch is: []
# WORD_SIZE is: 4
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 8
#
import ctypes


class AsDictMixin:
    @classmethod
    def as_dict(cls, self):
        result = {}
        if not isinstance(self, AsDictMixin):
            # not a structure, assume it's already a python object
            return self
        if not hasattr(cls, "_fields_"):
            return result
        # sys.version_info >= (3, 5)
        # for (field, *_) in cls._fields_:  # noqa
        for field_tuple in cls._fields_:  # noqa
            field = field_tuple[0]
            if field.startswith('PADDING_'):
                continue
            value = getattr(self, field)
            type_ = type(value)
            if hasattr(value, "_length_") and hasattr(value, "_type_"):
                # array
                if not hasattr(type_, "as_dict"):
                    value = [v for v in value]
                else:
                    type_ = type_._type_
                    value = [type_.as_dict(v) for v in value]
            elif hasattr(value, "contents") and hasattr(value, "_type_"):
                # pointer
                try:
                    if not hasattr(type_, "as_dict"):
                        value = value.contents
                    else:
                        type_ = type_._type_
                        value = type_.as_dict(value.contents)
                except ValueError:
                    # nullptr
                    value = None
            elif isinstance(value, AsDictMixin):
                # other structure
                value = type_.as_dict(value)
            result[field] = value
        return result


class Structure(ctypes.Structure, AsDictMixin):

    def __init__(self, *args, **kwds):
        # We don't want to use positional arguments fill PADDING_* fields

        args = dict(zip(self.__class__._field_names_(), args))
        args.update(kwds)
        super(Structure, self).__init__(**args)

    @classmethod
    def _field_names_(cls):
        if hasattr(cls, '_fields_'):
            return (f[0] for f in cls._fields_ if not f[0].startswith('PADDING'))
        else:
            return ()

    @classmethod
    def get_type(cls, field):
        for f in cls._fields_:
            if f[0] == field:
                return f[1]
        return None

    @classmethod
    def bind(cls, bound_fields):
        fields = {}
        for name, type_ in cls._fields_:
            if hasattr(type_, "restype"):
                if name in bound_fields:
                    if bound_fields[name] is None:
                        fields[name] = type_()
                    else:
                        # use a closure to capture the callback from the loop scope
                        fields[name] = (
                            type_((lambda callback: lambda *args: callback(*args))(
                                bound_fields[name]))
                        )
                    del bound_fields[name]
                else:
                    # default callback implementation (does nothing)
                    try:
                        default_ = type_(0).restype().value
                    except TypeError:
                        default_ = None
                    fields[name] = type_((
                        lambda default_: lambda *args: default_)(default_))
            else:
                # not a callback function, use default initialization
                if name in bound_fields:
                    fields[name] = bound_fields[name]
                    del bound_fields[name]
                else:
                    fields[name] = type_()
        if len(bound_fields) != 0:
            raise ValueError(
                "Cannot bind the following unknown callback(s) {}.{}".format(
                    cls.__name__, bound_fields.keys()
            ))
        return cls(**fields)


class Union(ctypes.Union, AsDictMixin):
    pass



c_int128 = ctypes.c_ubyte*16
c_uint128 = c_int128
void = None
if ctypes.sizeof(ctypes.c_longdouble) == 8:
    c_long_double_t = ctypes.c_longdouble
else:
    c_long_double_t = ctypes.c_ubyte*8

class FunctionFactoryStub:
    def __getattr__(self, _):
      return ctypes.CFUNCTYPE(lambda y:y)

# libraries['FIXME_STUB'] explanation
# As you did not list (-l libraryname.so) a library that exports this function
# This is a non-working stub instead. 
# You can either re-run clan2py with -l /path/to/library.so
# Or manually fix this by comment the ctypes.CDLL loading
_libraries = {}
_libraries['FIXME_STUB'] = FunctionFactoryStub() #  ctypes.CDLL('FIXME_STUB')
def string_cast(char_pointer, encoding='utf-8', errors='strict'):
    value = ctypes.cast(char_pointer, ctypes.c_char_p).value
    if value is not None and encoding is not None:
        value = value.decode(encoding, errors=errors)
    return value


def char_pointer_cast(string, encoding='utf-8'):
    if encoding is not None:
        try:
            string = string.encode(encoding)
        except AttributeError:
            # In Python3, bytes has no encode attribute
            pass
    string = ctypes.c_char_p(string)
    return ctypes.cast(string, ctypes.POINTER(ctypes.c_char))





NTSTATUS = ctypes.c_int32
PNTSTATUS = ctypes.POINTER(ctypes.c_int32)
KPRIORITY = ctypes.c_int32
PKPRIORITY = ctypes.POINTER(ctypes.c_int32)
LOGICAL = ctypes.c_uint32
PLOGICAL = ctypes.POINTER(ctypes.c_uint32)
class struct__CLIENT_ID(Structure):
    pass

struct__CLIENT_ID._pack_ = 1 # source:False
struct__CLIENT_ID._fields_ = [
    ('UniqueProcess', ctypes.POINTER(None)),
    ('UniqueThread', ctypes.POINTER(None)),
]

CLIENT_ID = struct__CLIENT_ID
PCLIENT_ID = ctypes.POINTER(struct__CLIENT_ID)

# values for enumeration 'KPROCESSOR_MODE'
KPROCESSOR_MODE__enumvalues = {
    0: 'KernelMode',
    1: 'UserMode',
}
KernelMode = 0
UserMode = 1
KPROCESSOR_MODE = ctypes.c_uint32 # enum

# values for enumeration '_KTHREAD_STATE'
_KTHREAD_STATE__enumvalues = {
    0: 'Initialized',
    1: 'Ready',
    2: 'Running',
    3: 'Standby',
    4: 'Terminated',
    5: 'Waiting',
    6: 'Transition',
    7: 'DeferredReady',
    8: 'GateWaitObsolete',
    9: 'WaitingForProcessInSwap',
    10: 'MaximumThreadState',
}
Initialized = 0
Ready = 1
Running = 2
Standby = 3
Terminated = 4
Waiting = 5
Transition = 6
DeferredReady = 7
GateWaitObsolete = 8
WaitingForProcessInSwap = 9
MaximumThreadState = 10
_KTHREAD_STATE = ctypes.c_uint32 # enum
KTHREAD_STATE = _KTHREAD_STATE
KTHREAD_STATE__enumvalues = _KTHREAD_STATE__enumvalues
PKTHREAD_STATE = ctypes.POINTER(_KTHREAD_STATE)

# values for enumeration '_KWAIT_REASON'
_KWAIT_REASON__enumvalues = {
    0: 'Executive',
    1: 'FreePage',
    2: 'PageIn',
    3: 'PoolAllocation',
    4: 'DelayExecution',
    5: 'Suspended',
    6: 'UserRequest',
    7: 'WrExecutive',
    8: 'WrFreePage',
    9: 'WrPageIn',
    10: 'WrPoolAllocation',
    11: 'WrDelayExecution',
    12: 'WrSuspended',
    13: 'WrUserRequest',
    14: 'WrEventPair',
    15: 'WrQueue',
    16: 'WrLpcReceive',
    17: 'WrLpcReply',
    18: 'WrVirtualMemory',
    19: 'WrPageOut',
    20: 'WrRendezvous',
    21: 'WrKeyedEvent',
    22: 'WrTerminated',
    23: 'WrProcessInSwap',
    24: 'WrCpuRateControl',
    25: 'WrCalloutStack',
    26: 'WrKernel',
    27: 'WrResource',
    28: 'WrPushLock',
    29: 'WrMutex',
    30: 'WrQuantumEnd',
    31: 'WrDispatchInt',
    32: 'WrPreempted',
    33: 'WrYieldExecution',
    34: 'WrFastMutex',
    35: 'WrGuardedMutex',
    36: 'WrRundown',
    37: 'WrAlertByThreadId',
    38: 'WrDeferredPreempt',
    39: 'MaximumWaitReason',
}
Executive = 0
FreePage = 1
PageIn = 2
PoolAllocation = 3
DelayExecution = 4
Suspended = 5
UserRequest = 6
WrExecutive = 7
WrFreePage = 8
WrPageIn = 9
WrPoolAllocation = 10
WrDelayExecution = 11
WrSuspended = 12
WrUserRequest = 13
WrEventPair = 14
WrQueue = 15
WrLpcReceive = 16
WrLpcReply = 17
WrVirtualMemory = 18
WrPageOut = 19
WrRendezvous = 20
WrKeyedEvent = 21
WrTerminated = 22
WrProcessInSwap = 23
WrCpuRateControl = 24
WrCalloutStack = 25
WrKernel = 26
WrResource = 27
WrPushLock = 28
WrMutex = 29
WrQuantumEnd = 30
WrDispatchInt = 31
WrPreempted = 32
WrYieldExecution = 33
WrFastMutex = 34
WrGuardedMutex = 35
WrRundown = 36
WrAlertByThreadId = 37
WrDeferredPreempt = 38
MaximumWaitReason = 39
_KWAIT_REASON = ctypes.c_uint32 # enum
KWAIT_REASON = _KWAIT_REASON
KWAIT_REASON__enumvalues = _KWAIT_REASON__enumvalues

# values for enumeration '_EVENT_TYPE'
_EVENT_TYPE__enumvalues = {
    0: 'NotificationEvent',
    1: 'SynchronizationEvent',
}
NotificationEvent = 0
SynchronizationEvent = 1
_EVENT_TYPE = ctypes.c_uint32 # enum
EVENT_TYPE = _EVENT_TYPE
EVENT_TYPE__enumvalues = _EVENT_TYPE__enumvalues

# values for enumeration '_TIMER_TYPE'
_TIMER_TYPE__enumvalues = {
    0: 'NotificationTimer',
    1: 'SynchronizationTimer',
}
NotificationTimer = 0
SynchronizationTimer = 1
_TIMER_TYPE = ctypes.c_uint32 # enum
TIMER_TYPE = _TIMER_TYPE
TIMER_TYPE__enumvalues = _TIMER_TYPE__enumvalues

# values for enumeration '_WAIT_TYPE'
_WAIT_TYPE__enumvalues = {
    0: 'WaitAll',
    1: 'WaitAny',
    2: 'WaitNotification',
    3: 'WaitDequeue',
}
WaitAll = 0
WaitAny = 1
WaitNotification = 2
WaitDequeue = 3
_WAIT_TYPE = ctypes.c_uint32 # enum
WAIT_TYPE = _WAIT_TYPE
WAIT_TYPE__enumvalues = _WAIT_TYPE__enumvalues

# values for enumeration '_SECTION_INHERIT'
_SECTION_INHERIT__enumvalues = {
    1: 'ViewShare',
    2: 'ViewUnmap',
}
ViewShare = 1
ViewUnmap = 2
_SECTION_INHERIT = ctypes.c_uint32 # enum
SECTION_INHERIT = _SECTION_INHERIT
SECTION_INHERIT__enumvalues = _SECTION_INHERIT__enumvalues

# values for enumeration '_HARDERROR_RESPONSE_OPTION'
_HARDERROR_RESPONSE_OPTION__enumvalues = {
    0: 'OptionAbortRetryIgnore',
    1: 'OptionOk',
    2: 'OptionOkCancel',
    3: 'OptionRetryCancel',
    4: 'OptionYesNo',
    5: 'OptionYesNoCancel',
    6: 'OptionShutdownSystem',
    7: 'OptionOkNoWait',
    8: 'OptionCancelTryContinue',
}
OptionAbortRetryIgnore = 0
OptionOk = 1
OptionOkCancel = 2
OptionRetryCancel = 3
OptionYesNo = 4
OptionYesNoCancel = 5
OptionShutdownSystem = 6
OptionOkNoWait = 7
OptionCancelTryContinue = 8
_HARDERROR_RESPONSE_OPTION = ctypes.c_uint32 # enum
HARDERROR_RESPONSE_OPTION = _HARDERROR_RESPONSE_OPTION
HARDERROR_RESPONSE_OPTION__enumvalues = _HARDERROR_RESPONSE_OPTION__enumvalues
PHARDERROR_RESPONSE_OPTION = ctypes.POINTER(_HARDERROR_RESPONSE_OPTION)

# values for enumeration '_HARDERROR_RESPONSE'
_HARDERROR_RESPONSE__enumvalues = {
    0: 'ResponseReturnToCaller',
    1: 'ResponseNotHandled',
    2: 'ResponseAbort',
    3: 'ResponseCancel',
    4: 'ResponseIgnore',
    5: 'ResponseNo',
    6: 'ResponseOk',
    7: 'ResponseRetry',
    8: 'ResponseYes',
    9: 'ResponseTryAgain',
    10: 'ResponseContinue',
}
ResponseReturnToCaller = 0
ResponseNotHandled = 1
ResponseAbort = 2
ResponseCancel = 3
ResponseIgnore = 4
ResponseNo = 5
ResponseOk = 6
ResponseRetry = 7
ResponseYes = 8
ResponseTryAgain = 9
ResponseContinue = 10
_HARDERROR_RESPONSE = ctypes.c_uint32 # enum
HARDERROR_RESPONSE = _HARDERROR_RESPONSE
HARDERROR_RESPONSE__enumvalues = _HARDERROR_RESPONSE__enumvalues
PHARDERROR_RESPONSE = ctypes.POINTER(_HARDERROR_RESPONSE)
class struct__UNICODE_STRING(Structure):
    pass

struct__UNICODE_STRING._pack_ = 1 # source:False
struct__UNICODE_STRING._fields_ = [
    ('Length', ctypes.c_uint16),
    ('MaximumLength', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('Buffer', ctypes.POINTER(ctypes.c_uint16)),
]

UNICODE_STRING = struct__UNICODE_STRING
PUNICODE_STRING = ctypes.POINTER(struct__UNICODE_STRING)
PCUNICODE_STRING = ctypes.POINTER(struct__UNICODE_STRING)
PWCHAR = ctypes.POINTER(ctypes.c_uint16)
USHORT = ctypes.c_uint16
RtlInitEmptyUnicodeString = _libraries['FIXME_STUB'].RtlInitEmptyUnicodeString
RtlInitEmptyUnicodeString.restype = None
RtlInitEmptyUnicodeString.argtypes = [PUNICODE_STRING, PWCHAR, USHORT]
class struct__STRING(Structure):
    pass

struct__STRING._pack_ = 1 # source:False
struct__STRING._fields_ = [
    ('Length', ctypes.c_uint16),
    ('MaximumLength', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('Buffer', ctypes.POINTER(ctypes.c_char)),
]

ANSI_STRING = struct__STRING
PANSI_STRING = ctypes.POINTER(struct__STRING)
class struct__SYSTEM_SESSION_PROCESS_INFORMATION(Structure):
    pass

struct__SYSTEM_SESSION_PROCESS_INFORMATION._pack_ = 1 # source:False
struct__SYSTEM_SESSION_PROCESS_INFORMATION._fields_ = [
    ('SessionId', ctypes.c_uint32),
    ('SizeOfBuf', ctypes.c_uint32),
    ('Buffer', ctypes.POINTER(None)),
]

SYSTEM_SESSION_PROCESS_INFORMATION = struct__SYSTEM_SESSION_PROCESS_INFORMATION
PSYSTEM_SESSION_PROCESS_INFORMATION = ctypes.POINTER(struct__SYSTEM_SESSION_PROCESS_INFORMATION)
class struct__SYSTEM_KERNEL_DEBUGGER_INFORMATION(Structure):
    pass

struct__SYSTEM_KERNEL_DEBUGGER_INFORMATION._pack_ = 1 # source:False
struct__SYSTEM_KERNEL_DEBUGGER_INFORMATION._fields_ = [
    ('KernelDebuggerEnabled', ctypes.c_ubyte),
    ('KernelDebuggerNotPresent', ctypes.c_ubyte),
]

SYSTEM_KERNEL_DEBUGGER_INFORMATION = struct__SYSTEM_KERNEL_DEBUGGER_INFORMATION
PSYSTEM_KERNEL_DEBUGGER_INFORMATION = ctypes.POINTER(struct__SYSTEM_KERNEL_DEBUGGER_INFORMATION)
class struct__SYSTEM_KERNEL_DEBUGGER_INFORMATION_EX(Structure):
    pass

struct__SYSTEM_KERNEL_DEBUGGER_INFORMATION_EX._pack_ = 1 # source:False
struct__SYSTEM_KERNEL_DEBUGGER_INFORMATION_EX._fields_ = [
    ('DebuggerAllowed', ctypes.c_ubyte),
    ('DebuggerEnabled', ctypes.c_ubyte),
    ('DebuggerPresent', ctypes.c_ubyte),
]

SYSTEM_KERNEL_DEBUGGER_INFORMATION_EX = struct__SYSTEM_KERNEL_DEBUGGER_INFORMATION_EX
PSYSTEM_KERNEL_DEBUGGER_INFORMATION_EX = ctypes.POINTER(struct__SYSTEM_KERNEL_DEBUGGER_INFORMATION_EX)
class struct__LDT_INFORMATION(Structure):
    pass

class struct__LDT_ENTRY(Structure):
    pass

class union_union_1(Union):
    pass

class struct_struct_1(Structure):
    pass

struct_struct_1._pack_ = 1 # source:False
struct_struct_1._fields_ = [
    ('BaseMid', ctypes.c_uint32, 8),
    ('Type', ctypes.c_uint32, 5),
    ('Dpl', ctypes.c_uint32, 2),
    ('Pres', ctypes.c_uint32, 1),
    ('LimitHi', ctypes.c_uint32, 4),
    ('Sys', ctypes.c_uint32, 1),
    ('Reserved_0', ctypes.c_uint32, 1),
    ('Default_Big', ctypes.c_uint32, 1),
    ('Granularity', ctypes.c_uint32, 1),
    ('BaseHi', ctypes.c_uint32, 8),
]

class struct_struct_2(Structure):
    pass

struct_struct_2._pack_ = 1 # source:False
struct_struct_2._fields_ = [
    ('BaseMid', ctypes.c_ubyte),
    ('Flags1', ctypes.c_ubyte),
    ('Flags2', ctypes.c_ubyte),
    ('BaseHi', ctypes.c_ubyte),
]

union_union_1._pack_ = 1 # source:False
union_union_1._fields_ = [
    ('Bytes', struct_struct_2),
    ('Bits', struct_struct_1),
]

struct__LDT_ENTRY._pack_ = 1 # source:False
struct__LDT_ENTRY._fields_ = [
    ('LimitLow', ctypes.c_uint16),
    ('BaseLow', ctypes.c_uint16),
    ('HighWord', union_union_1),
]

struct__LDT_INFORMATION._pack_ = 1 # source:False
struct__LDT_INFORMATION._fields_ = [
    ('Start', ctypes.c_uint32),
    ('Length', ctypes.c_uint32),
    ('LdtEntries', struct__LDT_ENTRY * 1),
]

PROCESS_LDT_INFORMATION = struct__LDT_INFORMATION
PPROCESS_LDT_INFORMATION = ctypes.POINTER(struct__LDT_INFORMATION)
class struct__KERNEL_USER_TIMES(Structure):
    pass

class union__LARGE_INTEGER(Union):
    pass

class struct_struct_3(Structure):
    pass

struct_struct_3._pack_ = 1 # source:False
struct_struct_3._fields_ = [
    ('LowPart', ctypes.c_uint32),
    ('HighPart', ctypes.c_int32),
]

class struct_struct_4(Structure):
    pass

struct_struct_4._pack_ = 1 # source:False
struct_struct_4._fields_ = [
    ('LowPart', ctypes.c_uint32),
    ('HighPart', ctypes.c_int32),
]

union__LARGE_INTEGER._pack_ = 1 # source:False
union__LARGE_INTEGER._anonymous_ = ('_0',)
union__LARGE_INTEGER._fields_ = [
    ('_0', struct_struct_3),
    ('u', struct_struct_4),
    ('QuadPart', ctypes.c_int64),
]

struct__KERNEL_USER_TIMES._pack_ = 1 # source:False
struct__KERNEL_USER_TIMES._fields_ = [
    ('CreateTime', union__LARGE_INTEGER),
    ('ExitTime', union__LARGE_INTEGER),
    ('KernelTime', union__LARGE_INTEGER),
    ('UserTime', union__LARGE_INTEGER),
]

KERNEL_USER_TIMES = struct__KERNEL_USER_TIMES
PKERNEL_USER_TIMES = ctypes.POINTER(struct__KERNEL_USER_TIMES)
class struct__SYSTEM_THREAD_INFORMATION(Structure):
    pass

struct__SYSTEM_THREAD_INFORMATION._pack_ = 1 # source:False
struct__SYSTEM_THREAD_INFORMATION._fields_ = [
    ('KernelTime', union__LARGE_INTEGER),
    ('UserTime', union__LARGE_INTEGER),
    ('CreateTime', union__LARGE_INTEGER),
    ('WaitTime', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('StartAddress', ctypes.POINTER(None)),
    ('ClientId', CLIENT_ID),
    ('Priority', ctypes.c_int32),
    ('BasePriority', ctypes.c_int32),
    ('ContextSwitches', ctypes.c_uint32),
    ('ThreadState', ctypes.c_uint32),
    ('WaitReason', KWAIT_REASON),
    ('PADDING_1', ctypes.c_ubyte * 4),
]

SYSTEM_THREAD_INFORMATION = struct__SYSTEM_THREAD_INFORMATION
PSYSTEM_THREAD_INFORMATION = ctypes.POINTER(struct__SYSTEM_THREAD_INFORMATION)
class struct__SYSTEM_PROCESS_INFORMATION(Structure):
    pass

struct__SYSTEM_PROCESS_INFORMATION._pack_ = 1 # source:False
struct__SYSTEM_PROCESS_INFORMATION._fields_ = [
    ('NextEntryOffset', ctypes.c_uint32),
    ('NumberOfThreads', ctypes.c_uint32),
    ('WorkingSetPrivateSize', union__LARGE_INTEGER),
    ('HardFaultCount', ctypes.c_uint32),
    ('NumberOfThreadsHighWatermark', ctypes.c_uint32),
    ('CycleTime', ctypes.c_uint64),
    ('CreateTime', union__LARGE_INTEGER),
    ('UserTime', union__LARGE_INTEGER),
    ('KernelTime', union__LARGE_INTEGER),
    ('ImageName', UNICODE_STRING),
    ('BasePriority', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('UniqueProcessId', ctypes.POINTER(None)),
    ('InheritedFromUniqueProcessId', ctypes.POINTER(None)),
    ('HandleCount', ctypes.c_uint32),
    ('SessionId', ctypes.c_uint32),
    ('UniqueProcessKey', ctypes.c_uint64),
    ('PeakVirtualSize', ctypes.c_uint64),
    ('VirtualSize', ctypes.c_uint64),
    ('PageFaultCount', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('PeakWorkingSetSize', ctypes.c_uint64),
    ('WorkingSetSize', ctypes.c_uint64),
    ('QuotaPeakPagedPoolUsage', ctypes.c_uint64),
    ('QuotaPagedPoolUsage', ctypes.c_uint64),
    ('QuotaPeakNonPagedPoolUsage', ctypes.c_uint64),
    ('QuotaNonPagedPoolUsage', ctypes.c_uint64),
    ('PagefileUsage', ctypes.c_uint64),
    ('PeakPagefileUsage', ctypes.c_uint64),
    ('PrivatePageCount', ctypes.c_uint64),
    ('ReadOperationCount', union__LARGE_INTEGER),
    ('WriteOperationCount', union__LARGE_INTEGER),
    ('OtherOperationCount', union__LARGE_INTEGER),
    ('ReadTransferCount', union__LARGE_INTEGER),
    ('WriteTransferCount', union__LARGE_INTEGER),
    ('OtherTransferCount', union__LARGE_INTEGER),
    ('Threads', struct__SYSTEM_THREAD_INFORMATION * 1),
]

SYSTEM_PROCESS_INFORMATION = struct__SYSTEM_PROCESS_INFORMATION
PSYSTEM_PROCESS_INFORMATION = ctypes.POINTER(struct__SYSTEM_PROCESS_INFORMATION)
class struct__PROCESS_SESSION_INFORMATION(Structure):
    pass

struct__PROCESS_SESSION_INFORMATION._pack_ = 1 # source:False
struct__PROCESS_SESSION_INFORMATION._fields_ = [
    ('SessionId', ctypes.c_uint32),
]

PROCESS_SESSION_INFORMATION = struct__PROCESS_SESSION_INFORMATION
PPROCESS_SESSION_INFORMATION = ctypes.POINTER(struct__PROCESS_SESSION_INFORMATION)
class struct__FILE_BASIC_INFORMATION(Structure):
    pass

struct__FILE_BASIC_INFORMATION._pack_ = 1 # source:False
struct__FILE_BASIC_INFORMATION._fields_ = [
    ('CreationTime', union__LARGE_INTEGER),
    ('LastAccessTime', union__LARGE_INTEGER),
    ('LastWriteTime', union__LARGE_INTEGER),
    ('ChangeTime', union__LARGE_INTEGER),
    ('FileAttributes', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

FILE_BASIC_INFORMATION = struct__FILE_BASIC_INFORMATION
PFILE_BASIC_INFORMATION = ctypes.POINTER(struct__FILE_BASIC_INFORMATION)
class struct__FILE_STANDARD_INFORMATION(Structure):
    pass

struct__FILE_STANDARD_INFORMATION._pack_ = 1 # source:False
struct__FILE_STANDARD_INFORMATION._fields_ = [
    ('AllocationSize', union__LARGE_INTEGER),
    ('EndOfFile', union__LARGE_INTEGER),
    ('NumberOfLinks', ctypes.c_uint32),
    ('DeletePending', ctypes.c_ubyte),
    ('Directory', ctypes.c_ubyte),
    ('PADDING_0', ctypes.c_ubyte * 2),
]

FILE_STANDARD_INFORMATION = struct__FILE_STANDARD_INFORMATION
PFILE_STANDARD_INFORMATION = ctypes.POINTER(struct__FILE_STANDARD_INFORMATION)
class struct__FILE_POSITION_INFORMATION(Structure):
    _pack_ = 1 # source:False
    _fields_ = [
    ('CurrentByteOffset', union__LARGE_INTEGER),
     ]

FILE_POSITION_INFORMATION = struct__FILE_POSITION_INFORMATION
PFILE_POSITION_INFORMATION = ctypes.POINTER(struct__FILE_POSITION_INFORMATION)
class struct__THREAD_BASIC_INFORMATION(Structure):
    pass

struct__THREAD_BASIC_INFORMATION._pack_ = 1 # source:False
struct__THREAD_BASIC_INFORMATION._fields_ = [
    ('ExitStatus', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('TebBaseAddress', ctypes.POINTER(None)),
    ('ClientId', CLIENT_ID),
    ('AffinityMask', ctypes.c_uint64),
    ('Priority', ctypes.c_int32),
    ('BasePriority', ctypes.c_int32),
]

THREAD_BASIC_INFORMATION = struct__THREAD_BASIC_INFORMATION
PTHREAD_BASIC_INFORMATION = ctypes.POINTER(struct__THREAD_BASIC_INFORMATION)
class struct__MEMORY_REGION_INFORMATION(Structure):
    pass

class union_union_2(Union):
    pass

class struct_struct_6(Structure):
    pass

struct_struct_6._pack_ = 1 # source:False
struct_struct_6._fields_ = [
    ('Private', ctypes.c_uint32, 1),
    ('MappedDataFile', ctypes.c_uint32, 1),
    ('MappedImage', ctypes.c_uint32, 1),
    ('MappedPageFile', ctypes.c_uint32, 1),
    ('MappedPhysical', ctypes.c_uint32, 1),
    ('DirectMapped', ctypes.c_uint32, 1),
    ('Reserved', ctypes.c_uint32, 26),
]

union_union_2._pack_ = 1 # source:False
union_union_2._fields_ = [
    ('RegionType', ctypes.c_uint32),
    ('s', struct_struct_6),
]

struct__MEMORY_REGION_INFORMATION._pack_ = 1 # source:False
struct__MEMORY_REGION_INFORMATION._fields_ = [
    ('AllocationBase', ctypes.POINTER(None)),
    ('AllocationProtect', ctypes.c_uint32),
    ('u', union_union_2),
    ('RegionSize', ctypes.c_uint64),
    ('CommitSize', ctypes.c_uint64),
]

MEMORY_REGION_INFORMATION = struct__MEMORY_REGION_INFORMATION
PMEMORY_REGION_INFORMATION = ctypes.POINTER(struct__MEMORY_REGION_INFORMATION)
class struct__SECTION_BASIC_INFORMATION(Structure):
    pass

struct__SECTION_BASIC_INFORMATION._pack_ = 1 # source:False
struct__SECTION_BASIC_INFORMATION._fields_ = [
    ('BaseAddress', ctypes.POINTER(None)),
    ('AllocationAttributes', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('MaximumSize', union__LARGE_INTEGER),
]

SECTION_BASIC_INFORMATION = struct__SECTION_BASIC_INFORMATION
PSECTION_BASIC_INFORMATION = ctypes.POINTER(struct__SECTION_BASIC_INFORMATION)
class struct__SECTION_IMAGE_INFORMATION(Structure):
    pass

class union_union_3(Union):
    pass

class struct_struct_7(Structure):
    pass

struct_struct_7._pack_ = 1 # source:False
struct_struct_7._fields_ = [
    ('ComPlusNativeReady', ctypes.c_ubyte, 1),
    ('ComPlusILOnly', ctypes.c_ubyte, 1),
    ('ImageDynamicallyRelocated', ctypes.c_ubyte, 1),
    ('ImageMappedFlat', ctypes.c_ubyte, 1),
    ('BaseBelow4gb', ctypes.c_ubyte, 1),
    ('ComPlusPrefer32bit', ctypes.c_ubyte, 1),
    ('Reserved', ctypes.c_ubyte, 2),
]

union_union_3._pack_ = 1 # source:False
union_union_3._fields_ = [
    ('ImageFlags', ctypes.c_ubyte),
    ('s3', struct_struct_7),
]

class union_union_9(Union):
    pass

class struct_struct_8(Structure):
    pass

struct_struct_8._pack_ = 1 # source:False
struct_struct_8._fields_ = [
    ('MajorOperatingSystemVersion', ctypes.c_uint16),
    ('MinorOperatingSystemVersion', ctypes.c_uint16),
]

union_union_9._pack_ = 1 # source:False
union_union_9._fields_ = [
    ('s2', struct_struct_8),
    ('OperatingSystemVersion', ctypes.c_uint32),
]

class union_union_10(Union):
    pass

class struct_struct_11(Structure):
    pass

struct_struct_11._pack_ = 1 # source:False
struct_struct_11._fields_ = [
    ('SubSystemMinorVersion', ctypes.c_uint16),
    ('SubSystemMajorVersion', ctypes.c_uint16),
]

union_union_10._pack_ = 1 # source:False
union_union_10._fields_ = [
    ('s1', struct_struct_11),
    ('SubSystemVersion', ctypes.c_uint32),
]

struct__SECTION_IMAGE_INFORMATION._pack_ = 1 # source:False
struct__SECTION_IMAGE_INFORMATION._fields_ = [
    ('TransferAddress', ctypes.POINTER(None)),
    ('ZeroBits', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('MaximumStackSize', ctypes.c_uint64),
    ('CommittedStackSize', ctypes.c_uint64),
    ('SubSystemType', ctypes.c_uint32),
    ('u1', union_union_10),
    ('u2', union_union_9),
    ('ImageCharacteristics', ctypes.c_uint16),
    ('DllCharacteristics', ctypes.c_uint16),
    ('Machine', ctypes.c_uint16),
    ('ImageContainsCode', ctypes.c_ubyte),
    ('u3', union_union_3),
    ('LoaderFlags', ctypes.c_uint32),
    ('ImageFileSize', ctypes.c_uint32),
    ('CheckSum', ctypes.c_uint32),
]

SECTION_IMAGE_INFORMATION = struct__SECTION_IMAGE_INFORMATION
PSECTION_IMAGE_INFORMATION = ctypes.POINTER(struct__SECTION_IMAGE_INFORMATION)
class struct__SECTION_INTERNAL_IMAGE_INFORMATION(Structure):
    pass

class union_union_13(Union):
    pass

class struct_struct_12(Structure):
    pass

struct_struct_12._pack_ = 1 # source:False
struct_struct_12._fields_ = [
    ('ImageReturnFlowGuardEnabled', ctypes.c_uint32, 1),
    ('ImageReturnFlowGuardStrict', ctypes.c_uint32, 1),
    ('ImageExportSuppressionEnabled', ctypes.c_uint32, 1),
    ('Reserved', ctypes.c_uint32, 29),
]

union_union_13._pack_ = 1 # source:False
union_union_13._fields_ = [
    ('ExtendedFlags', ctypes.c_uint32),
    ('s', struct_struct_12),
]

struct__SECTION_INTERNAL_IMAGE_INFORMATION._pack_ = 1 # source:False
struct__SECTION_INTERNAL_IMAGE_INFORMATION._fields_ = [
    ('SectionInformation', SECTION_IMAGE_INFORMATION),
    ('u', union_union_13),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

SECTION_INTERNAL_IMAGE_INFORMATION = struct__SECTION_INTERNAL_IMAGE_INFORMATION
PSECTION_INTERNAL_IMAGE_INFORMATION = ctypes.POINTER(struct__SECTION_INTERNAL_IMAGE_INFORMATION)
class struct__OBJECT_ATTRIBUTES(Structure):
    pass

struct__OBJECT_ATTRIBUTES._pack_ = 1 # source:False
struct__OBJECT_ATTRIBUTES._fields_ = [
    ('Length', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('RootDirectory', ctypes.POINTER(None)),
    ('ObjectName', ctypes.POINTER(struct__UNICODE_STRING)),
    ('Attributes', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('SecurityDescriptor', ctypes.POINTER(None)),
    ('SecurityQualityOfService', ctypes.POINTER(None)),
]

OBJECT_ATTRIBUTES = struct__OBJECT_ATTRIBUTES
POBJECT_ATTRIBUTES = ctypes.POINTER(struct__OBJECT_ATTRIBUTES)
class struct__LDR_RESOURCE_INFO(Structure):
    pass

struct__LDR_RESOURCE_INFO._pack_ = 1 # source:False
struct__LDR_RESOURCE_INFO._fields_ = [
    ('Type', ctypes.c_uint64),
    ('Name', ctypes.c_uint64),
    ('Language', ctypes.c_uint64),
]

LDR_RESOURCE_INFO = struct__LDR_RESOURCE_INFO
PLDR_RESOURCE_INFO = ctypes.POINTER(struct__LDR_RESOURCE_INFO)
class struct__LDR_ENUM_RESOURCE_INFO(Structure):
    pass

struct__LDR_ENUM_RESOURCE_INFO._pack_ = 1 # source:False
struct__LDR_ENUM_RESOURCE_INFO._fields_ = [
    ('Type', ctypes.c_uint64),
    ('Name', ctypes.c_uint64),
    ('Language', ctypes.c_uint64),
    ('Data', ctypes.POINTER(None)),
    ('Size', ctypes.c_uint64),
    ('Reserved', ctypes.c_uint64),
]

LDR_ENUM_RESOURCE_INFO = struct__LDR_ENUM_RESOURCE_INFO
PLDR_ENUM_RESOURCE_INFO = ctypes.POINTER(struct__LDR_ENUM_RESOURCE_INFO)
class struct__RTL_PROCESS_MODULE_INFORMATION(Structure):
    pass

struct__RTL_PROCESS_MODULE_INFORMATION._pack_ = 1 # source:False
struct__RTL_PROCESS_MODULE_INFORMATION._fields_ = [
    ('Section', ctypes.POINTER(None)),
    ('MappedBase', ctypes.POINTER(None)),
    ('ImageBase', ctypes.POINTER(None)),
    ('ImageSize', ctypes.c_uint32),
    ('Flags', ctypes.c_uint32),
    ('LoadOrderIndex', ctypes.c_uint16),
    ('InitOrderIndex', ctypes.c_uint16),
    ('LoadCount', ctypes.c_uint16),
    ('OffsetToFileName', ctypes.c_uint16),
    ('FullPathName', ctypes.c_ubyte * 256),
]

RTL_PROCESS_MODULE_INFORMATION = struct__RTL_PROCESS_MODULE_INFORMATION
PRTL_PROCESS_MODULE_INFORMATION = ctypes.POINTER(struct__RTL_PROCESS_MODULE_INFORMATION)
class struct__RTL_PROCESS_MODULES(Structure):
    pass

struct__RTL_PROCESS_MODULES._pack_ = 1 # source:False
struct__RTL_PROCESS_MODULES._fields_ = [
    ('NumberOfModules', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('Modules', struct__RTL_PROCESS_MODULE_INFORMATION * 1),
]

RTL_PROCESS_MODULES = struct__RTL_PROCESS_MODULES
PRTL_PROCESS_MODULES = ctypes.POINTER(struct__RTL_PROCESS_MODULES)
class struct__RTL_PROCESS_MODULE_INFORMATION_EX(Structure):
    pass

struct__RTL_PROCESS_MODULE_INFORMATION_EX._pack_ = 1 # source:False
struct__RTL_PROCESS_MODULE_INFORMATION_EX._fields_ = [
    ('NextOffset', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 6),
    ('BaseInfo', RTL_PROCESS_MODULE_INFORMATION),
    ('ImageChecksum', ctypes.c_uint32),
    ('TimeDateStamp', ctypes.c_uint32),
    ('DefaultBase', ctypes.POINTER(None)),
]

RTL_PROCESS_MODULE_INFORMATION_EX = struct__RTL_PROCESS_MODULE_INFORMATION_EX
PRTL_PROCESS_MODULE_INFORMATION_EX = ctypes.POINTER(struct__RTL_PROCESS_MODULE_INFORMATION_EX)
class struct__SYSTEM_HANDLE_TABLE_ENTRY_INFO(Structure):
    pass

struct__SYSTEM_HANDLE_TABLE_ENTRY_INFO._pack_ = 1 # source:False
struct__SYSTEM_HANDLE_TABLE_ENTRY_INFO._fields_ = [
    ('UniqueProcessId', ctypes.c_uint16),
    ('CreatorBackTraceIndex', ctypes.c_uint16),
    ('ObjectTypeIndex', ctypes.c_ubyte),
    ('HandleAttributes', ctypes.c_ubyte),
    ('HandleValue', ctypes.c_uint16),
    ('Object', ctypes.POINTER(None)),
    ('GrantedAccess', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

SYSTEM_HANDLE_TABLE_ENTRY_INFO = struct__SYSTEM_HANDLE_TABLE_ENTRY_INFO
PSYSTEM_HANDLE_TABLE_ENTRY_INFO = ctypes.POINTER(struct__SYSTEM_HANDLE_TABLE_ENTRY_INFO)
class struct__SYSTEM_HANDLE_INFORMATION(Structure):
    pass

struct__SYSTEM_HANDLE_INFORMATION._pack_ = 1 # source:False
struct__SYSTEM_HANDLE_INFORMATION._fields_ = [
    ('NumberOfHandles', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('Handles', struct__SYSTEM_HANDLE_TABLE_ENTRY_INFO * 1),
]

SYSTEM_HANDLE_INFORMATION = struct__SYSTEM_HANDLE_INFORMATION
PSYSTEM_HANDLE_INFORMATION = ctypes.POINTER(struct__SYSTEM_HANDLE_INFORMATION)
class struct__SYSTEM_HANDLE_TABLE_ENTRY_INFO_EX(Structure):
    pass

struct__SYSTEM_HANDLE_TABLE_ENTRY_INFO_EX._pack_ = 1 # source:False
struct__SYSTEM_HANDLE_TABLE_ENTRY_INFO_EX._fields_ = [
    ('Object', ctypes.POINTER(None)),
    ('UniqueProcessId', ctypes.c_uint64),
    ('HandleValue', ctypes.c_uint64),
    ('GrantedAccess', ctypes.c_uint32),
    ('CreatorBackTraceIndex', ctypes.c_uint16),
    ('ObjectTypeIndex', ctypes.c_uint16),
    ('HandleAttributes', ctypes.c_uint32),
    ('Reserved', ctypes.c_uint32),
]

SYSTEM_HANDLE_TABLE_ENTRY_INFO_EX = struct__SYSTEM_HANDLE_TABLE_ENTRY_INFO_EX
PSYSTEM_HANDLE_TABLE_ENTRY_INFO_EX = ctypes.POINTER(struct__SYSTEM_HANDLE_TABLE_ENTRY_INFO_EX)
class struct__SYSTEM_HANDLE_INFORMATION_EX(Structure):
    pass

struct__SYSTEM_HANDLE_INFORMATION_EX._pack_ = 1 # source:False
struct__SYSTEM_HANDLE_INFORMATION_EX._fields_ = [
    ('NumberOfHandles', ctypes.c_uint64),
    ('Reserved', ctypes.c_uint64),
    ('Handles', struct__SYSTEM_HANDLE_TABLE_ENTRY_INFO_EX * 1),
]

SYSTEM_HANDLE_INFORMATION_EX = struct__SYSTEM_HANDLE_INFORMATION_EX
PSYSTEM_HANDLE_INFORMATION_EX = ctypes.POINTER(struct__SYSTEM_HANDLE_INFORMATION_EX)
class struct__OBJECT_BASIC_INFORMATION(Structure):
    pass

struct__OBJECT_BASIC_INFORMATION._pack_ = 1 # source:False
struct__OBJECT_BASIC_INFORMATION._fields_ = [
    ('Attributes', ctypes.c_uint32),
    ('GrantedAccess', ctypes.c_uint32),
    ('HandleCount', ctypes.c_uint32),
    ('PointerCount', ctypes.c_uint32),
    ('PagedPoolCharge', ctypes.c_uint32),
    ('NonPagedPoolCharge', ctypes.c_uint32),
    ('Reserved', ctypes.c_uint32 * 3),
    ('NameInfoSize', ctypes.c_uint32),
    ('TypeInfoSize', ctypes.c_uint32),
    ('SecurityDescriptorSize', ctypes.c_uint32),
    ('CreationTime', union__LARGE_INTEGER),
]

OBJECT_BASIC_INFORMATION = struct__OBJECT_BASIC_INFORMATION
POBJECT_BASIC_INFORMATION = ctypes.POINTER(struct__OBJECT_BASIC_INFORMATION)
class struct__OBJECT_NAME_INFORMATION(Structure):
    _pack_ = 1 # source:False
    _fields_ = [
    ('Name', UNICODE_STRING),
     ]

OBJECT_NAME_INFORMATION = struct__OBJECT_NAME_INFORMATION
POBJECT_NAME_INFORMATION = ctypes.POINTER(struct__OBJECT_NAME_INFORMATION)
class struct__OBJECT_TYPE_INFORMATION(Structure):
    pass

class struct__GENERIC_MAPPING(Structure):
    pass

struct__GENERIC_MAPPING._pack_ = 1 # source:False
struct__GENERIC_MAPPING._fields_ = [
    ('GenericRead', ctypes.c_uint32),
    ('GenericWrite', ctypes.c_uint32),
    ('GenericExecute', ctypes.c_uint32),
    ('GenericAll', ctypes.c_uint32),
]

struct__OBJECT_TYPE_INFORMATION._pack_ = 1 # source:False
struct__OBJECT_TYPE_INFORMATION._fields_ = [
    ('TypeName', UNICODE_STRING),
    ('TotalNumberOfObjects', ctypes.c_uint32),
    ('TotalNumberOfHandles', ctypes.c_uint32),
    ('TotalPagedPoolUsage', ctypes.c_uint32),
    ('TotalNonPagedPoolUsage', ctypes.c_uint32),
    ('TotalNamePoolUsage', ctypes.c_uint32),
    ('TotalHandleTableUsage', ctypes.c_uint32),
    ('HighWaterNumberOfObjects', ctypes.c_uint32),
    ('HighWaterNumberOfHandles', ctypes.c_uint32),
    ('HighWaterPagedPoolUsage', ctypes.c_uint32),
    ('HighWaterNonPagedPoolUsage', ctypes.c_uint32),
    ('HighWaterNamePoolUsage', ctypes.c_uint32),
    ('HighWaterHandleTableUsage', ctypes.c_uint32),
    ('InvalidAttributes', ctypes.c_uint32),
    ('GenericMapping', struct__GENERIC_MAPPING),
    ('ValidAccessMask', ctypes.c_uint32),
    ('SecurityRequired', ctypes.c_ubyte),
    ('MaintainHandleCount', ctypes.c_ubyte),
    ('TypeIndex', ctypes.c_ubyte),
    ('ReservedByte', ctypes.c_char),
    ('PoolType', ctypes.c_uint32),
    ('DefaultPagedPoolCharge', ctypes.c_uint32),
    ('DefaultNonPagedPoolCharge', ctypes.c_uint32),
]

OBJECT_TYPE_INFORMATION = struct__OBJECT_TYPE_INFORMATION
POBJECT_TYPE_INFORMATION = ctypes.POINTER(struct__OBJECT_TYPE_INFORMATION)
class struct__OBJECT_TYPES_INFORMATION(Structure):
    pass

struct__OBJECT_TYPES_INFORMATION._pack_ = 1 # source:False
struct__OBJECT_TYPES_INFORMATION._fields_ = [
    ('NumberOfTypes', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('TypeInformation', struct__OBJECT_TYPE_INFORMATION * 1),
]

OBJECT_TYPES_INFORMATION = struct__OBJECT_TYPES_INFORMATION
POBJECT_TYPES_INFORMATION = ctypes.POINTER(struct__OBJECT_TYPES_INFORMATION)
class struct__OBJECT_HANDLE_FLAG_INFORMATION(Structure):
    pass

struct__OBJECT_HANDLE_FLAG_INFORMATION._pack_ = 1 # source:False
struct__OBJECT_HANDLE_FLAG_INFORMATION._fields_ = [
    ('Inherit', ctypes.c_ubyte),
    ('ProtectFromClose', ctypes.c_ubyte),
]

OBJECT_HANDLE_FLAG_INFORMATION = struct__OBJECT_HANDLE_FLAG_INFORMATION
POBJECT_HANDLE_FLAG_INFORMATION = ctypes.POINTER(struct__OBJECT_HANDLE_FLAG_INFORMATION)
class struct__DBGKM_EXCEPTION(Structure):
    pass

class struct__EXCEPTION_RECORD(Structure):
    pass

struct__EXCEPTION_RECORD._pack_ = 1 # source:False
struct__EXCEPTION_RECORD._fields_ = [
    ('ExceptionCode', ctypes.c_uint32),
    ('ExceptionFlags', ctypes.c_uint32),
    ('ExceptionRecord', ctypes.POINTER(struct__EXCEPTION_RECORD)),
    ('ExceptionAddress', ctypes.POINTER(None)),
    ('NumberParameters', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('ExceptionInformation', ctypes.c_uint64 * 15),
]

struct__DBGKM_EXCEPTION._pack_ = 1 # source:False
struct__DBGKM_EXCEPTION._fields_ = [
    ('ExceptionRecord', struct__EXCEPTION_RECORD),
    ('FirstChance', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

DBGKM_EXCEPTION = struct__DBGKM_EXCEPTION
PDBGKM_EXCEPTION = ctypes.POINTER(struct__DBGKM_EXCEPTION)
class struct__DBGKM_CREATE_THREAD(Structure):
    pass

struct__DBGKM_CREATE_THREAD._pack_ = 1 # source:False
struct__DBGKM_CREATE_THREAD._fields_ = [
    ('SubSystemKey', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('StartAddress', ctypes.POINTER(None)),
]

DBGKM_CREATE_THREAD = struct__DBGKM_CREATE_THREAD
PDBGKM_CREATE_THREAD = ctypes.POINTER(struct__DBGKM_CREATE_THREAD)
class struct__DBGKM_CREATE_PROCESS(Structure):
    pass

struct__DBGKM_CREATE_PROCESS._pack_ = 1 # source:False
struct__DBGKM_CREATE_PROCESS._fields_ = [
    ('SubSystemKey', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('FileHandle', ctypes.POINTER(None)),
    ('BaseOfImage', ctypes.POINTER(None)),
    ('DebugInfoFileOffset', ctypes.c_uint32),
    ('DebugInfoSize', ctypes.c_uint32),
    ('InitialThread', DBGKM_CREATE_THREAD),
]

DBGKM_CREATE_PROCESS = struct__DBGKM_CREATE_PROCESS
PDBGKM_CREATE_PROCESS = ctypes.POINTER(struct__DBGKM_CREATE_PROCESS)
class struct__DBGKM_EXIT_THREAD(Structure):
    pass

struct__DBGKM_EXIT_THREAD._pack_ = 1 # source:False
struct__DBGKM_EXIT_THREAD._fields_ = [
    ('ExitStatus', ctypes.c_int32),
]

DBGKM_EXIT_THREAD = struct__DBGKM_EXIT_THREAD
PDBGKM_EXIT_THREAD = ctypes.POINTER(struct__DBGKM_EXIT_THREAD)
class struct__DBGKM_EXIT_PROCESS(Structure):
    pass

struct__DBGKM_EXIT_PROCESS._pack_ = 1 # source:False
struct__DBGKM_EXIT_PROCESS._fields_ = [
    ('ExitStatus', ctypes.c_int32),
]

DBGKM_EXIT_PROCESS = struct__DBGKM_EXIT_PROCESS
PDBGKM_EXIT_PROCESS = ctypes.POINTER(struct__DBGKM_EXIT_PROCESS)
class struct__DBGKM_LOAD_DLL(Structure):
    pass

struct__DBGKM_LOAD_DLL._pack_ = 1 # source:False
struct__DBGKM_LOAD_DLL._fields_ = [
    ('FileHandle', ctypes.POINTER(None)),
    ('BaseOfDll', ctypes.POINTER(None)),
    ('DebugInfoFileOffset', ctypes.c_uint32),
    ('DebugInfoSize', ctypes.c_uint32),
    ('NamePointer', ctypes.POINTER(None)),
]

DBGKM_LOAD_DLL = struct__DBGKM_LOAD_DLL
PDBGKM_LOAD_DLL = ctypes.POINTER(struct__DBGKM_LOAD_DLL)
class struct__DBGKM_UNLOAD_DLL(Structure):
    pass

struct__DBGKM_UNLOAD_DLL._pack_ = 1 # source:False
struct__DBGKM_UNLOAD_DLL._fields_ = [
    ('BaseAddress', ctypes.POINTER(None)),
]

DBGKM_UNLOAD_DLL = struct__DBGKM_UNLOAD_DLL
PDBGKM_UNLOAD_DLL = ctypes.POINTER(struct__DBGKM_UNLOAD_DLL)

# values for enumeration '_DBG_STATE'
_DBG_STATE__enumvalues = {
    0: 'DbgIdle',
    1: 'DbgReplyPending',
    2: 'DbgCreateThreadStateChange',
    3: 'DbgCreateProcessStateChange',
    4: 'DbgExitThreadStateChange',
    5: 'DbgExitProcessStateChange',
    6: 'DbgExceptionStateChange',
    7: 'DbgBreakpointStateChange',
    8: 'DbgSingleStepStateChange',
    9: 'DbgLoadDllStateChange',
    10: 'DbgUnloadDllStateChange',
}
DbgIdle = 0
DbgReplyPending = 1
DbgCreateThreadStateChange = 2
DbgCreateProcessStateChange = 3
DbgExitThreadStateChange = 4
DbgExitProcessStateChange = 5
DbgExceptionStateChange = 6
DbgBreakpointStateChange = 7
DbgSingleStepStateChange = 8
DbgLoadDllStateChange = 9
DbgUnloadDllStateChange = 10
_DBG_STATE = ctypes.c_uint32 # enum
DBG_STATE = _DBG_STATE
DBG_STATE__enumvalues = _DBG_STATE__enumvalues
PDBG_STATE = ctypes.POINTER(_DBG_STATE)
class struct__DBGUI_CREATE_THREAD(Structure):
    pass

struct__DBGUI_CREATE_THREAD._pack_ = 1 # source:False
struct__DBGUI_CREATE_THREAD._fields_ = [
    ('HandleToThread', ctypes.POINTER(None)),
    ('NewThread', DBGKM_CREATE_THREAD),
]

DBGUI_CREATE_THREAD = struct__DBGUI_CREATE_THREAD
PDBGUI_CREATE_THREAD = ctypes.POINTER(struct__DBGUI_CREATE_THREAD)
class struct__DBGUI_CREATE_PROCESS(Structure):
    pass

struct__DBGUI_CREATE_PROCESS._pack_ = 1 # source:False
struct__DBGUI_CREATE_PROCESS._fields_ = [
    ('HandleToProcess', ctypes.POINTER(None)),
    ('HandleToThread', ctypes.POINTER(None)),
    ('NewProcess', DBGKM_CREATE_PROCESS),
]

DBGUI_CREATE_PROCESS = struct__DBGUI_CREATE_PROCESS
PDBGUI_CREATE_PROCESS = ctypes.POINTER(struct__DBGUI_CREATE_PROCESS)
class struct__DBGUI_WAIT_STATE_CHANGE(Structure):
    pass

class union_union_14(Union):
    pass

union_union_14._pack_ = 1 # source:False
union_union_14._fields_ = [
    ('Exception', DBGKM_EXCEPTION),
    ('CreateThread', DBGUI_CREATE_THREAD),
    ('CreateProcessInfo', DBGUI_CREATE_PROCESS),
    ('ExitThread', DBGKM_EXIT_THREAD),
    ('ExitProcess', DBGKM_EXIT_PROCESS),
    ('LoadDll', DBGKM_LOAD_DLL),
    ('UnloadDll', DBGKM_UNLOAD_DLL),
    ('PADDING_0', ctypes.c_ubyte * 152),
]

struct__DBGUI_WAIT_STATE_CHANGE._pack_ = 1 # source:False
struct__DBGUI_WAIT_STATE_CHANGE._fields_ = [
    ('NewState', DBG_STATE),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('AppClientId', CLIENT_ID),
    ('StateInfo', union_union_14),
]

DBGUI_WAIT_STATE_CHANGE = struct__DBGUI_WAIT_STATE_CHANGE
PDBGUI_WAIT_STATE_CHANGE = ctypes.POINTER(struct__DBGUI_WAIT_STATE_CHANGE)
class struct__DBGSS_THREAD_DATA(Structure):
    pass

struct__DBGSS_THREAD_DATA._pack_ = 1 # source:False
struct__DBGSS_THREAD_DATA._fields_ = [
    ('Next', ctypes.POINTER(struct__DBGSS_THREAD_DATA)),
    ('ThreadHandle', ctypes.POINTER(None)),
    ('ProcessHandle', ctypes.POINTER(None)),
    ('ProcessId', ctypes.c_uint32),
    ('ThreadId', ctypes.c_uint32),
    ('HandleMarked', ctypes.c_ubyte),
    ('PADDING_0', ctypes.c_ubyte * 7),
]

DBGSS_THREAD_DATA = struct__DBGSS_THREAD_DATA
PDBGSS_THREAD_DATA = ctypes.POINTER(struct__DBGSS_THREAD_DATA)
RTL_ATOM = ctypes.c_uint16
PRTL_ATOM = ctypes.POINTER(ctypes.c_uint16)
SECURITY_STATUS = ctypes.c_int32
class struct__RTL_SPLAY_LINKS(Structure):
    pass

struct__RTL_SPLAY_LINKS._pack_ = 1 # source:False
struct__RTL_SPLAY_LINKS._fields_ = [
    ('Parent', ctypes.POINTER(struct__RTL_SPLAY_LINKS)),
    ('LeftChild', ctypes.POINTER(struct__RTL_SPLAY_LINKS)),
    ('RightChild', ctypes.POINTER(struct__RTL_SPLAY_LINKS)),
]

RTL_SPLAY_LINKS = struct__RTL_SPLAY_LINKS
PRTL_SPLAY_LINKS = ctypes.POINTER(struct__RTL_SPLAY_LINKS)
class struct__PREFIX_TABLE_ENTRY(Structure):
    pass

struct__PREFIX_TABLE_ENTRY._pack_ = 1 # source:False
struct__PREFIX_TABLE_ENTRY._fields_ = [
    ('NodeTypeCode', ctypes.c_int16),
    ('NameLength', ctypes.c_int16),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('NextPrefixTree', ctypes.POINTER(struct__PREFIX_TABLE_ENTRY)),
    ('Links', RTL_SPLAY_LINKS),
    ('Prefix', ctypes.POINTER(struct__STRING)),
]

PREFIX_TABLE_ENTRY = struct__PREFIX_TABLE_ENTRY
PPREFIX_TABLE_ENTRY = ctypes.POINTER(struct__PREFIX_TABLE_ENTRY)
class struct__PREFIX_TABLE(Structure):
    pass

struct__PREFIX_TABLE._pack_ = 1 # source:False
struct__PREFIX_TABLE._fields_ = [
    ('NodeTypeCode', ctypes.c_int16),
    ('NameLength', ctypes.c_int16),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('NextPrefixTree', ctypes.POINTER(struct__PREFIX_TABLE_ENTRY)),
]

PREFIX_TABLE = struct__PREFIX_TABLE
PPREFIX_TABLE = ctypes.POINTER(struct__PREFIX_TABLE)
class struct__RTL_BITMAP(Structure):
    pass

struct__RTL_BITMAP._pack_ = 1 # source:False
struct__RTL_BITMAP._fields_ = [
    ('SizeOfBitMap', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('Buffer', ctypes.POINTER(ctypes.c_uint32)),
]

RTL_BITMAP = struct__RTL_BITMAP
PRTL_BITMAP = ctypes.POINTER(struct__RTL_BITMAP)
class struct__RTL_BITMAP_RUN(Structure):
    pass

struct__RTL_BITMAP_RUN._pack_ = 1 # source:False
struct__RTL_BITMAP_RUN._fields_ = [
    ('StartingIndex', ctypes.c_uint32),
    ('NumberOfBits', ctypes.c_uint32),
]

RTL_BITMAP_RUN = struct__RTL_BITMAP_RUN
PRTL_BITMAP_RUN = ctypes.POINTER(struct__RTL_BITMAP_RUN)

# values for enumeration 'RTL_BSD_ITEM_TYPE'
RTL_BSD_ITEM_TYPE__enumvalues = {
    0: 'RtlBsdItemVersionNumber',
    1: 'RtlBsdItemProductType',
    2: 'RtlBsdItemAabEnabled',
    3: 'RtlBsdItemAabTimeout',
    4: 'RtlBsdItemBootGood',
    5: 'RtlBsdItemBootShutdown',
    6: 'RtlBsdItemMax',
}
RtlBsdItemVersionNumber = 0
RtlBsdItemProductType = 1
RtlBsdItemAabEnabled = 2
RtlBsdItemAabTimeout = 3
RtlBsdItemBootGood = 4
RtlBsdItemBootShutdown = 5
RtlBsdItemMax = 6
RTL_BSD_ITEM_TYPE = ctypes.c_uint32 # enum
PRTL_BSD_ITEM_TYPE = ctypes.POINTER(RTL_BSD_ITEM_TYPE)
class struct__RTL_PROCESS_VERIFIER_OPTIONS(Structure):
    pass

struct__RTL_PROCESS_VERIFIER_OPTIONS._pack_ = 1 # source:False
struct__RTL_PROCESS_VERIFIER_OPTIONS._fields_ = [
    ('SizeStruct', ctypes.c_uint32),
    ('Option', ctypes.c_uint32),
    ('OptionData', ctypes.c_ubyte * 1),
    ('PADDING_0', ctypes.c_ubyte * 3),
]

RTL_PROCESS_VERIFIER_OPTIONS = struct__RTL_PROCESS_VERIFIER_OPTIONS
PRTL_PROCESS_VERIFIER_OPTIONS = ctypes.POINTER(struct__RTL_PROCESS_VERIFIER_OPTIONS)
class struct__RTL_DEBUG_INFORMATION(Structure):
    pass

class struct__RTL_PROCESS_LOCKS(Structure):
    pass

class struct__RTL_PROCESS_BACKTRACES(Structure):
    pass

class struct__RTL_PROCESS_HEAPS(Structure):
    pass

class union_union_15(Union):
    pass

union_union_15._pack_ = 1 # source:False
union_union_15._fields_ = [
    ('Modules', ctypes.POINTER(struct__RTL_PROCESS_MODULES)),
    ('ModulesEx', ctypes.POINTER(struct__RTL_PROCESS_MODULE_INFORMATION_EX)),
]

struct__RTL_DEBUG_INFORMATION._pack_ = 1 # source:False
struct__RTL_DEBUG_INFORMATION._anonymous_ = ('_0',)
struct__RTL_DEBUG_INFORMATION._fields_ = [
    ('SectionHandleClient', ctypes.POINTER(None)),
    ('ViewBaseClient', ctypes.POINTER(None)),
    ('ViewBaseTarget', ctypes.POINTER(None)),
    ('ViewBaseDelta', ctypes.c_uint64),
    ('EventPairClient', ctypes.POINTER(None)),
    ('EventPairTarget', ctypes.POINTER(None)),
    ('TargetProcessId', ctypes.POINTER(None)),
    ('TargetThreadHandle', ctypes.POINTER(None)),
    ('Flags', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('OffsetFree', ctypes.c_uint64),
    ('CommitSize', ctypes.c_uint64),
    ('ViewSize', ctypes.c_uint64),
    ('_0', union_union_15),
    ('BackTraces', ctypes.POINTER(struct__RTL_PROCESS_BACKTRACES)),
    ('Heaps', ctypes.POINTER(struct__RTL_PROCESS_HEAPS)),
    ('Locks', ctypes.POINTER(struct__RTL_PROCESS_LOCKS)),
    ('SpecificHeap', ctypes.POINTER(None)),
    ('TargetProcessHandle', ctypes.POINTER(None)),
    ('VerifierOptions', ctypes.POINTER(struct__RTL_PROCESS_VERIFIER_OPTIONS)),
    ('ProcessHeap', ctypes.POINTER(None)),
    ('CriticalSectionHandle', ctypes.POINTER(None)),
    ('CriticalSectionOwnerThread', ctypes.POINTER(None)),
    ('Reserved', ctypes.POINTER(None) * 4),
]

class struct__RTL_HEAP_INFORMATION(Structure):
    pass

class struct__RTL_HEAP_TAG(Structure):
    pass

class struct__RTL_HEAP_ENTRY(Structure):
    pass

struct__RTL_HEAP_INFORMATION._pack_ = 1 # source:False
struct__RTL_HEAP_INFORMATION._fields_ = [
    ('BaseAddress', ctypes.POINTER(None)),
    ('Flags', ctypes.c_uint32),
    ('EntryOverhead', ctypes.c_uint16),
    ('CreatorBackTraceIndex', ctypes.c_uint16),
    ('BytesAllocated', ctypes.c_uint64),
    ('BytesCommitted', ctypes.c_uint64),
    ('NumberOfTags', ctypes.c_uint32),
    ('NumberOfEntries', ctypes.c_uint32),
    ('NumberOfPseudoTags', ctypes.c_uint32),
    ('PseudoTagGranularity', ctypes.c_uint32),
    ('Reserved', ctypes.c_uint32 * 5),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('Tags', ctypes.POINTER(struct__RTL_HEAP_TAG)),
    ('Entries', ctypes.POINTER(struct__RTL_HEAP_ENTRY)),
]

struct__RTL_PROCESS_HEAPS._pack_ = 1 # source:False
struct__RTL_PROCESS_HEAPS._fields_ = [
    ('NumberOfHeaps', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('Heaps', struct__RTL_HEAP_INFORMATION * 1),
]

struct__RTL_HEAP_TAG._pack_ = 1 # source:False
struct__RTL_HEAP_TAG._fields_ = [
    ('NumberOfAllocations', ctypes.c_uint32),
    ('NumberOfFrees', ctypes.c_uint32),
    ('BytesAllocated', ctypes.c_uint64),
    ('TagIndex', ctypes.c_uint16),
    ('CreatorBackTraceIndex', ctypes.c_uint16),
    ('TagName', ctypes.c_uint16 * 24),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

class union_union_17(Union):
    pass

class struct_struct_18(Structure):
    pass

struct_struct_18._pack_ = 1 # source:False
struct_struct_18._fields_ = [
    ('CommittedSize', ctypes.c_uint64),
    ('FirstBlock', ctypes.POINTER(None)),
]

class struct_struct_16(Structure):
    pass

struct_struct_16._pack_ = 1 # source:False
struct_struct_16._fields_ = [
    ('Settable', ctypes.c_uint64),
    ('Tag', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

union_union_17._pack_ = 1 # source:False
union_union_17._fields_ = [
    ('s1', struct_struct_16),
    ('s2', struct_struct_18),
]

struct__RTL_HEAP_ENTRY._pack_ = 1 # source:False
struct__RTL_HEAP_ENTRY._fields_ = [
    ('Size', ctypes.c_uint64),
    ('Flags', ctypes.c_uint16),
    ('AllocatorBackTraceIndex', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('u', union_union_17),
]

RTL_DEBUG_INFORMATION = struct__RTL_DEBUG_INFORMATION
PRTL_DEBUG_INFORMATION = ctypes.POINTER(struct__RTL_DEBUG_INFORMATION)
PPS_APC_ROUTINE = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(None), ctypes.POINTER(None))
class struct__RTLP_CURDIR_REF(Structure):
    pass

PRTLP_CURDIR_REF = ctypes.POINTER(struct__RTLP_CURDIR_REF)
class struct__RTL_RELATIVE_NAME_U(Structure):
    pass

struct__RTL_RELATIVE_NAME_U._pack_ = 1 # source:False
struct__RTL_RELATIVE_NAME_U._fields_ = [
    ('RelativeName', UNICODE_STRING),
    ('ContainingDirectory', ctypes.POINTER(None)),
    ('CurDirRef', ctypes.POINTER(struct__RTLP_CURDIR_REF)),
]

RTL_RELATIVE_NAME_U = struct__RTL_RELATIVE_NAME_U
PRTL_RELATIVE_NAME_U = ctypes.POINTER(struct__RTL_RELATIVE_NAME_U)

# values for enumeration '_RTL_PATH_TYPE'
_RTL_PATH_TYPE__enumvalues = {
    0: 'RtlPathTypeUnknown',
    1: 'RtlPathTypeUncAbsolute',
    2: 'RtlPathTypeDriveAbsolute',
    3: 'RtlPathTypeDriveRelative',
    4: 'RtlPathTypeRooted',
    5: 'RtlPathTypeRelative',
    6: 'RtlPathTypeLocalDevice',
    7: 'RtlPathTypeRootLocalDevice',
}
RtlPathTypeUnknown = 0
RtlPathTypeUncAbsolute = 1
RtlPathTypeDriveAbsolute = 2
RtlPathTypeDriveRelative = 3
RtlPathTypeRooted = 4
RtlPathTypeRelative = 5
RtlPathTypeLocalDevice = 6
RtlPathTypeRootLocalDevice = 7
_RTL_PATH_TYPE = ctypes.c_uint32 # enum
RTL_PATH_TYPE = _RTL_PATH_TYPE
RTL_PATH_TYPE__enumvalues = _RTL_PATH_TYPE__enumvalues
class struct__CURDIR(Structure):
    pass

struct__CURDIR._pack_ = 1 # source:False
struct__CURDIR._fields_ = [
    ('DosPath', UNICODE_STRING),
    ('Handle', ctypes.POINTER(None)),
]

CURDIR = struct__CURDIR
PCURDIR = ctypes.POINTER(struct__CURDIR)
class struct__RTL_DRIVE_LETTER_CURDIR(Structure):
    pass

struct__RTL_DRIVE_LETTER_CURDIR._pack_ = 1 # source:False
struct__RTL_DRIVE_LETTER_CURDIR._fields_ = [
    ('Flags', ctypes.c_uint16),
    ('Length', ctypes.c_uint16),
    ('TimeStamp', ctypes.c_uint32),
    ('DosPath', UNICODE_STRING),
]

RTL_DRIVE_LETTER_CURDIR = struct__RTL_DRIVE_LETTER_CURDIR
PRTL_DRIVE_LETTER_CURDIR = ctypes.POINTER(struct__RTL_DRIVE_LETTER_CURDIR)
class struct__LDR_SERVICE_TAG_RECORD(Structure):
    pass

struct__LDR_SERVICE_TAG_RECORD._pack_ = 1 # source:False
struct__LDR_SERVICE_TAG_RECORD._fields_ = [
    ('Next', ctypes.POINTER(struct__LDR_SERVICE_TAG_RECORD)),
    ('ServiceTag', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

LDR_SERVICE_TAG_RECORD = struct__LDR_SERVICE_TAG_RECORD
PLDR_SERVICE_TAG_RECORD = ctypes.POINTER(struct__LDR_SERVICE_TAG_RECORD)
class struct__LDRP_CSLIST(Structure):
    pass

class struct__SINGLE_LIST_ENTRY(Structure):
    pass

struct__LDRP_CSLIST._pack_ = 1 # source:False
struct__LDRP_CSLIST._fields_ = [
    ('Tail', ctypes.POINTER(struct__SINGLE_LIST_ENTRY)),
]

struct__SINGLE_LIST_ENTRY._pack_ = 1 # source:False
struct__SINGLE_LIST_ENTRY._fields_ = [
    ('Next', ctypes.POINTER(struct__SINGLE_LIST_ENTRY)),
]

LDRP_CSLIST = struct__LDRP_CSLIST
PLDRP_CSLIST = ctypes.POINTER(struct__LDRP_CSLIST)

# values for enumeration '_LDR_DDAG_STATE'
_LDR_DDAG_STATE__enumvalues = {
    -5: 'LdrModulesMerged',
    -4: 'LdrModulesInitError',
    -3: 'LdrModulesSnapError',
    -2: 'LdrModulesUnloaded',
    -1: 'LdrModulesUnloading',
    0: 'LdrModulesPlaceHolder',
    1: 'LdrModulesMapping',
    2: 'LdrModulesMapped',
    3: 'LdrModulesWaitingForDependencies',
    4: 'LdrModulesSnapping',
    5: 'LdrModulesSnapped',
    6: 'LdrModulesCondensed',
    7: 'LdrModulesReadyToInit',
    8: 'LdrModulesInitializing',
    9: 'LdrModulesReadyToRun',
}
LdrModulesMerged = -5
LdrModulesInitError = -4
LdrModulesSnapError = -3
LdrModulesUnloaded = -2
LdrModulesUnloading = -1
LdrModulesPlaceHolder = 0
LdrModulesMapping = 1
LdrModulesMapped = 2
LdrModulesWaitingForDependencies = 3
LdrModulesSnapping = 4
LdrModulesSnapped = 5
LdrModulesCondensed = 6
LdrModulesReadyToInit = 7
LdrModulesInitializing = 8
LdrModulesReadyToRun = 9
_LDR_DDAG_STATE = ctypes.c_int32 # enum
LDR_DDAG_STATE = _LDR_DDAG_STATE
LDR_DDAG_STATE__enumvalues = _LDR_DDAG_STATE__enumvalues
class struct__LDR_DDAG_NODE(Structure):
    pass

class union_union_19(Union):
    _pack_ = 1 # source:False
    _fields_ = [
    ('Dependencies', LDRP_CSLIST),
    ('RemovalLink', struct__SINGLE_LIST_ENTRY),
     ]

class struct__LIST_ENTRY(Structure):
    pass

struct__LIST_ENTRY._pack_ = 1 # source:False
struct__LIST_ENTRY._fields_ = [
    ('Flink', ctypes.POINTER(struct__LIST_ENTRY)),
    ('Blink', ctypes.POINTER(struct__LIST_ENTRY)),
]

struct__LDR_DDAG_NODE._pack_ = 1 # source:False
struct__LDR_DDAG_NODE._anonymous_ = ('_0',)
struct__LDR_DDAG_NODE._fields_ = [
    ('Modules', struct__LIST_ENTRY),
    ('ServiceTagList', ctypes.POINTER(struct__LDR_SERVICE_TAG_RECORD)),
    ('LoadCount', ctypes.c_uint32),
    ('LoadWhileUnloadingCount', ctypes.c_uint32),
    ('LowestLink', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('_0', union_union_19),
    ('IncomingDependencies', LDRP_CSLIST),
    ('State', LDR_DDAG_STATE),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('CondenseLink', struct__SINGLE_LIST_ENTRY),
    ('PreorderNumber', ctypes.c_uint32),
    ('PADDING_2', ctypes.c_ubyte * 4),
]

LDR_DDAG_NODE = struct__LDR_DDAG_NODE
PLDR_DDAG_NODE = ctypes.POINTER(struct__LDR_DDAG_NODE)
class struct__LDR_DEPENDENCY_RECORD(Structure):
    pass

struct__LDR_DEPENDENCY_RECORD._pack_ = 1 # source:False
struct__LDR_DEPENDENCY_RECORD._fields_ = [
    ('DependencyLink', struct__SINGLE_LIST_ENTRY),
    ('DependencyNode', ctypes.POINTER(struct__LDR_DDAG_NODE)),
    ('IncomingDependencyLink', struct__SINGLE_LIST_ENTRY),
    ('IncomingDependencyNode', ctypes.POINTER(struct__LDR_DDAG_NODE)),
]

LDR_DEPENDENCY_RECORD = struct__LDR_DEPENDENCY_RECORD
PLDR_DEPENDENCY_RECORD = ctypes.POINTER(struct__LDR_DEPENDENCY_RECORD)

# values for enumeration '_LDR_DLL_LOAD_REASON'
_LDR_DLL_LOAD_REASON__enumvalues = {
    0: 'LoadReasonStaticDependency',
    1: 'LoadReasonStaticForwarderDependency',
    2: 'LoadReasonDynamicForwarderDependency',
    3: 'LoadReasonDelayloadDependency',
    4: 'LoadReasonDynamicLoad',
    5: 'LoadReasonAsImageLoad',
    6: 'LoadReasonAsDataLoad',
    -1: 'LoadReasonUnknown',
}
LoadReasonStaticDependency = 0
LoadReasonStaticForwarderDependency = 1
LoadReasonDynamicForwarderDependency = 2
LoadReasonDelayloadDependency = 3
LoadReasonDynamicLoad = 4
LoadReasonAsImageLoad = 5
LoadReasonAsDataLoad = 6
LoadReasonUnknown = -1
_LDR_DLL_LOAD_REASON = ctypes.c_int32 # enum
LDR_DLL_LOAD_REASON = _LDR_DLL_LOAD_REASON
LDR_DLL_LOAD_REASON__enumvalues = _LDR_DLL_LOAD_REASON__enumvalues
PLDR_DLL_LOAD_REASON = ctypes.POINTER(_LDR_DLL_LOAD_REASON)
class struct__RTL_BALANCED_NODE(Structure):
    pass

class union_union_21(Union):
    pass

class struct_struct_20(Structure):
    pass

struct_struct_20._pack_ = 1 # source:False
struct_struct_20._fields_ = [
    ('Left', ctypes.POINTER(struct__RTL_BALANCED_NODE)),
    ('Right', ctypes.POINTER(struct__RTL_BALANCED_NODE)),
]

union_union_21._pack_ = 1 # source:False
union_union_21._fields_ = [
    ('Children', ctypes.POINTER(struct__RTL_BALANCED_NODE) * 2),
    ('s', struct_struct_20),
]

class union_union_22(Union):
    pass

union_union_22._pack_ = 1 # source:False
union_union_22._fields_ = [
    ('Red', ctypes.c_ubyte, 1),
    ('Balance', ctypes.c_ubyte, 2),
    ('ParentValue', ctypes.c_uint64),
]

struct__RTL_BALANCED_NODE._pack_ = 1 # source:False
struct__RTL_BALANCED_NODE._anonymous_ = ('_0',)
struct__RTL_BALANCED_NODE._fields_ = [
    ('_0', union_union_21),
    ('u', union_union_22),
]

RTL_BALANCED_NODE = struct__RTL_BALANCED_NODE
PRTL_BALANCED_NODE = ctypes.POINTER(struct__RTL_BALANCED_NODE)
class struct__LDR_DATA_TABLE_ENTRY(Structure):
    pass

class struct__ACTIVATION_CONTEXT(Structure):
    pass

class struct__LDRP_LOAD_CONTEXT(Structure):
    pass

class union_union_24(Union):
    pass

class struct_struct_23(Structure):
    pass

struct_struct_23._pack_ = 1 # source:False
struct_struct_23._fields_ = [
    ('PackagedBinary', ctypes.c_uint32, 1),
    ('MarkedForRemoval', ctypes.c_uint32, 1),
    ('ImageDll', ctypes.c_uint32, 1),
    ('LoadNotificationsSent', ctypes.c_uint32, 1),
    ('TelemetryEntryProcessed', ctypes.c_uint32, 1),
    ('ProcessStaticImport', ctypes.c_uint32, 1),
    ('InLegacyLists', ctypes.c_uint32, 1),
    ('InIndexes', ctypes.c_uint32, 1),
    ('ShimDll', ctypes.c_uint32, 1),
    ('InExceptionTable', ctypes.c_uint32, 1),
    ('ReservedFlags1', ctypes.c_uint32, 2),
    ('LoadInProgress', ctypes.c_uint32, 1),
    ('LoadConfigProcessed', ctypes.c_uint32, 1),
    ('EntryProcessed', ctypes.c_uint32, 1),
    ('ProtectDelayLoad', ctypes.c_uint32, 1),
    ('ReservedFlags3', ctypes.c_uint32, 2),
    ('DontCallForThreads', ctypes.c_uint32, 1),
    ('ProcessAttachCalled', ctypes.c_uint32, 1),
    ('ProcessAttachFailed', ctypes.c_uint32, 1),
    ('CorDeferredValidate', ctypes.c_uint32, 1),
    ('CorImage', ctypes.c_uint32, 1),
    ('DontRelocate', ctypes.c_uint32, 1),
    ('CorILOnly', ctypes.c_uint32, 1),
    ('ReservedFlags5', ctypes.c_uint32, 3),
    ('Redirected', ctypes.c_uint32, 1),
    ('ReservedFlags6', ctypes.c_uint32, 2),
    ('CompatDatabaseProcessed', ctypes.c_uint32, 1),
]

union_union_24._pack_ = 1 # source:False
union_union_24._fields_ = [
    ('FlagGroup', ctypes.c_ubyte * 4),
    ('Flags', ctypes.c_uint32),
    ('s', struct_struct_23),
]

class union_union_25(Union):
    _pack_ = 1 # source:False
    _fields_ = [
    ('InInitializationOrderLinks', struct__LIST_ENTRY),
    ('InProgressLinks', struct__LIST_ENTRY),
     ]

struct__LDR_DATA_TABLE_ENTRY._pack_ = 1 # source:False
struct__LDR_DATA_TABLE_ENTRY._anonymous_ = ('_0',)
struct__LDR_DATA_TABLE_ENTRY._fields_ = [
    ('InLoadOrderLinks', struct__LIST_ENTRY),
    ('InMemoryOrderLinks', struct__LIST_ENTRY),
    ('_0', union_union_25),
    ('DllBase', ctypes.POINTER(None)),
    ('EntryPoint', ctypes.POINTER(None)),
    ('SizeOfImage', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('FullDllName', UNICODE_STRING),
    ('BaseDllName', UNICODE_STRING),
    ('u', union_union_24),
    ('ObsoleteLoadCount', ctypes.c_uint16),
    ('TlsIndex', ctypes.c_uint16),
    ('HashLinks', struct__LIST_ENTRY),
    ('TimeDateStamp', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('EntryPointActivationContext', ctypes.POINTER(struct__ACTIVATION_CONTEXT)),
    ('Lock', ctypes.POINTER(None)),
    ('DdagNode', ctypes.POINTER(struct__LDR_DDAG_NODE)),
    ('NodeModuleLink', struct__LIST_ENTRY),
    ('LoadContext', ctypes.POINTER(struct__LDRP_LOAD_CONTEXT)),
    ('ParentDllBase', ctypes.POINTER(None)),
    ('SwitchBackContext', ctypes.POINTER(None)),
    ('BaseAddressIndexNode', RTL_BALANCED_NODE),
    ('MappingInfoIndexNode', RTL_BALANCED_NODE),
    ('OriginalBase', ctypes.c_uint64),
    ('LoadTime', union__LARGE_INTEGER),
    ('BaseNameHashValue', ctypes.c_uint32),
    ('LoadReason', LDR_DLL_LOAD_REASON),
    ('ImplicitPathOptions', ctypes.c_uint32),
    ('ReferenceCount', ctypes.c_uint32),
    ('DependentLoadFlags', ctypes.c_uint32),
    ('SigningLevel', ctypes.c_ubyte),
    ('PADDING_2', ctypes.c_ubyte * 3),
]

LDR_DATA_TABLE_ENTRY = struct__LDR_DATA_TABLE_ENTRY
PLDR_DATA_TABLE_ENTRY = ctypes.POINTER(struct__LDR_DATA_TABLE_ENTRY)
class struct__INITIAL_TEB(Structure):
    pass

class struct_struct_26(Structure):
    pass

struct_struct_26._pack_ = 1 # source:False
struct_struct_26._fields_ = [
    ('OldStackBase', ctypes.POINTER(None)),
    ('OldStackLimit', ctypes.POINTER(None)),
]

struct__INITIAL_TEB._pack_ = 1 # source:False
struct__INITIAL_TEB._fields_ = [
    ('OldInitialTeb', struct_struct_26),
    ('StackBase', ctypes.POINTER(None)),
    ('StackLimit', ctypes.POINTER(None)),
    ('StackAllocationBase', ctypes.POINTER(None)),
]

INITIAL_TEB = struct__INITIAL_TEB
PINITIAL_TEB = ctypes.POINTER(struct__INITIAL_TEB)
class struct__IO_STATUS_BLOCK(Structure):
    pass

class union_union_27(Union):
    pass

union_union_27._pack_ = 1 # source:False
union_union_27._fields_ = [
    ('Status', ctypes.c_int32),
    ('Pointer', ctypes.POINTER(None)),
]

struct__IO_STATUS_BLOCK._pack_ = 1 # source:False
struct__IO_STATUS_BLOCK._anonymous_ = ('_0',)
struct__IO_STATUS_BLOCK._fields_ = [
    ('_0', union_union_27),
    ('Information', ctypes.c_uint64),
]

IO_STATUS_BLOCK = struct__IO_STATUS_BLOCK
PIO_STATUS_BLOCK = ctypes.POINTER(struct__IO_STATUS_BLOCK)
PIO_APC_ROUTINE = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(struct__IO_STATUS_BLOCK), ctypes.c_uint32)
class struct__FILE_IO_COMPLETION_INFORMATION(Structure):
    pass

struct__FILE_IO_COMPLETION_INFORMATION._pack_ = 1 # source:False
struct__FILE_IO_COMPLETION_INFORMATION._fields_ = [
    ('KeyContext', ctypes.POINTER(None)),
    ('ApcContext', ctypes.POINTER(None)),
    ('IoStatusBlock', IO_STATUS_BLOCK),
]

FILE_IO_COMPLETION_INFORMATION = struct__FILE_IO_COMPLETION_INFORMATION
PFILE_IO_COMPLETION_INFORMATION = ctypes.POINTER(struct__FILE_IO_COMPLETION_INFORMATION)
class struct__FILE_COMPLETION_INFORMATION(Structure):
    pass

struct__FILE_COMPLETION_INFORMATION._pack_ = 1 # source:False
struct__FILE_COMPLETION_INFORMATION._fields_ = [
    ('Port', ctypes.POINTER(None)),
    ('Key', ctypes.POINTER(None)),
]

FILE_COMPLETION_INFORMATION = struct__FILE_COMPLETION_INFORMATION
PFILE_COMPLETION_INFORMATION = ctypes.POINTER(struct__FILE_COMPLETION_INFORMATION)
PRIORITY_CLASS = ctypes.c_ubyte
class struct__PROCESS_PRIORITY_CLASS(Structure):
    pass

struct__PROCESS_PRIORITY_CLASS._pack_ = 1 # source:False
struct__PROCESS_PRIORITY_CLASS._fields_ = [
    ('Foreground', ctypes.c_ubyte),
    ('PriorityClass', ctypes.c_ubyte),
]

PROCESS_PRIORITY_CLASS = struct__PROCESS_PRIORITY_CLASS
PPROCESS_PRIORITY_CLASS = ctypes.POINTER(struct__PROCESS_PRIORITY_CLASS)
class struct__PS_ATTRIBUTE(Structure):
    pass

class union_union_28(Union):
    pass

union_union_28._pack_ = 1 # source:False
union_union_28._fields_ = [
    ('Value', ctypes.c_uint64),
    ('ValuePtr', ctypes.POINTER(None)),
]

struct__PS_ATTRIBUTE._pack_ = 1 # source:False
struct__PS_ATTRIBUTE._anonymous_ = ('_0',)
struct__PS_ATTRIBUTE._fields_ = [
    ('Attribute', ctypes.c_uint64),
    ('Size', ctypes.c_uint64),
    ('_0', union_union_28),
    ('ReturnLength', ctypes.POINTER(ctypes.c_uint64)),
]

PS_ATTRIBUTE = struct__PS_ATTRIBUTE
PPS_ATTRIBUTE = ctypes.POINTER(struct__PS_ATTRIBUTE)
class struct__PS_ATTRIBUTE_LIST(Structure):
    pass

struct__PS_ATTRIBUTE_LIST._pack_ = 1 # source:False
struct__PS_ATTRIBUTE_LIST._fields_ = [
    ('TotalLength', ctypes.c_uint64),
    ('Attributes', struct__PS_ATTRIBUTE * 2),
]

PS_ATTRIBUTE_LIST = struct__PS_ATTRIBUTE_LIST
PPS_ATTRIBUTE_LIST = ctypes.POINTER(struct__PS_ATTRIBUTE_LIST)
class struct__PS_MEMORY_RESERVE(Structure):
    pass

struct__PS_MEMORY_RESERVE._pack_ = 1 # source:False
struct__PS_MEMORY_RESERVE._fields_ = [
    ('ReserveAddress', ctypes.POINTER(None)),
    ('ReserveSize', ctypes.c_uint64),
]

PS_MEMORY_RESERVE = struct__PS_MEMORY_RESERVE
PPS_MEMORY_RESERVE = ctypes.POINTER(struct__PS_MEMORY_RESERVE)

# values for enumeration '_PS_ATTRIBUTE_NUM'
_PS_ATTRIBUTE_NUM__enumvalues = {
    0: 'PsAttributeParentProcess',
    1: 'PsAttributeDebugPort',
    2: 'PsAttributeToken',
    3: 'PsAttributeClientId',
    4: 'PsAttributeTebAddress',
    5: 'PsAttributeImageName',
    6: 'PsAttributeImageInfo',
    7: 'PsAttributeMemoryReserve',
    8: 'PsAttributePriorityClass',
    9: 'PsAttributeErrorMode',
    10: 'PsAttributeStdHandleInfo',
    11: 'PsAttributeHandleList',
    12: 'PsAttributeGroupAffinity',
    13: 'PsAttributePreferredNode',
    14: 'PsAttributeIdealProcessor',
    15: 'PsAttributeUmsThread',
    16: 'PsAttributeMitigationOptions',
    17: 'PsAttributeProtectionLevel',
    18: 'PsAttributeSecureProcess',
    19: 'PsAttributeJobList',
    20: 'PsAttributeChildProcessPolicy',
    21: 'PsAttributeAllApplicationPackagesPolicy',
    22: 'PsAttributeWin32kFilter',
    23: 'PsAttributeSafeOpenPromptOriginClaim',
    24: 'PsAttributeBnoIsolation',
    25: 'PsAttributeDesktopAppPolicy',
    26: 'PsAttributeMax',
}
PsAttributeParentProcess = 0
PsAttributeDebugPort = 1
PsAttributeToken = 2
PsAttributeClientId = 3
PsAttributeTebAddress = 4
PsAttributeImageName = 5
PsAttributeImageInfo = 6
PsAttributeMemoryReserve = 7
PsAttributePriorityClass = 8
PsAttributeErrorMode = 9
PsAttributeStdHandleInfo = 10
PsAttributeHandleList = 11
PsAttributeGroupAffinity = 12
PsAttributePreferredNode = 13
PsAttributeIdealProcessor = 14
PsAttributeUmsThread = 15
PsAttributeMitigationOptions = 16
PsAttributeProtectionLevel = 17
PsAttributeSecureProcess = 18
PsAttributeJobList = 19
PsAttributeChildProcessPolicy = 20
PsAttributeAllApplicationPackagesPolicy = 21
PsAttributeWin32kFilter = 22
PsAttributeSafeOpenPromptOriginClaim = 23
PsAttributeBnoIsolation = 24
PsAttributeDesktopAppPolicy = 25
PsAttributeMax = 26
_PS_ATTRIBUTE_NUM = ctypes.c_uint32 # enum
PS_ATTRIBUTE_NUM = _PS_ATTRIBUTE_NUM
PS_ATTRIBUTE_NUM__enumvalues = _PS_ATTRIBUTE_NUM__enumvalues

# values for enumeration '_PS_STD_HANDLE_STATE'
_PS_STD_HANDLE_STATE__enumvalues = {
    0: 'PsNeverDuplicate',
    1: 'PsRequestDuplicate',
    2: 'PsAlwaysDuplicate',
    3: 'PsMaxStdHandleStates',
}
PsNeverDuplicate = 0
PsRequestDuplicate = 1
PsAlwaysDuplicate = 2
PsMaxStdHandleStates = 3
_PS_STD_HANDLE_STATE = ctypes.c_uint32 # enum
PS_STD_HANDLE_STATE = _PS_STD_HANDLE_STATE
PS_STD_HANDLE_STATE__enumvalues = _PS_STD_HANDLE_STATE__enumvalues
class struct__PS_STD_HANDLE_INFO(Structure):
    pass

class union_union_29(Union):
    pass

class struct_struct_30(Structure):
    pass

struct_struct_30._pack_ = 1 # source:False
struct_struct_30._fields_ = [
    ('StdHandleState', ctypes.c_uint32, 2),
    ('PseudoHandleMask', ctypes.c_uint32, 3),
    ('PADDING_0', ctypes.c_uint32, 27),
]

union_union_29._pack_ = 1 # source:False
union_union_29._fields_ = [
    ('Flags', ctypes.c_uint32),
    ('s', struct_struct_30),
]

struct__PS_STD_HANDLE_INFO._pack_ = 1 # source:False
struct__PS_STD_HANDLE_INFO._anonymous_ = ('_0',)
struct__PS_STD_HANDLE_INFO._fields_ = [
    ('_0', union_union_29),
    ('StdHandleSubsystemType', ctypes.c_uint32),
]

PS_STD_HANDLE_INFO = struct__PS_STD_HANDLE_INFO
PPS_STD_HANDLE_INFO = ctypes.POINTER(struct__PS_STD_HANDLE_INFO)
class struct__PS_BNO_ISOLATION_PARAMETERS(Structure):
    pass

struct__PS_BNO_ISOLATION_PARAMETERS._pack_ = 1 # source:False
struct__PS_BNO_ISOLATION_PARAMETERS._fields_ = [
    ('IsolationPrefix', UNICODE_STRING),
    ('HandleCount', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('Handles', ctypes.POINTER(ctypes.POINTER(None))),
    ('IsolationEnabled', ctypes.c_ubyte),
    ('PADDING_1', ctypes.c_ubyte * 7),
]

PS_BNO_ISOLATION_PARAMETERS = struct__PS_BNO_ISOLATION_PARAMETERS
PPS_BNO_ISOLATION_PARAMETERS = ctypes.POINTER(struct__PS_BNO_ISOLATION_PARAMETERS)

# values for enumeration '_PS_MITIGATION_OPTION'
_PS_MITIGATION_OPTION__enumvalues = {
    0: 'PS_MITIGATION_OPTION_NX',
    1: 'PS_MITIGATION_OPTION_SEHOP',
    2: 'PS_MITIGATION_OPTION_FORCE_RELOCATE_IMAGES',
    3: 'PS_MITIGATION_OPTION_HEAP_TERMINATE',
    4: 'PS_MITIGATION_OPTION_BOTTOM_UP_ASLR',
    5: 'PS_MITIGATION_OPTION_HIGH_ENTROPY_ASLR',
    6: 'PS_MITIGATION_OPTION_STRICT_HANDLE_CHECKS',
    7: 'PS_MITIGATION_OPTION_WIN32K_SYSTEM_CALL_DISABLE',
    8: 'PS_MITIGATION_OPTION_EXTENSION_POINT_DISABLE',
    9: 'PS_MITIGATION_OPTION_PROHIBIT_DYNAMIC_CODE',
    10: 'PS_MITIGATION_OPTION_CONTROL_FLOW_GUARD',
    11: 'PS_MITIGATION_OPTION_BLOCK_NON_MICROSOFT_BINARIES',
    12: 'PS_MITIGATION_OPTION_FONT_DISABLE',
    13: 'PS_MITIGATION_OPTION_IMAGE_LOAD_NO_REMOTE',
    14: 'PS_MITIGATION_OPTION_IMAGE_LOAD_NO_LOW_LABEL',
    15: 'PS_MITIGATION_OPTION_IMAGE_LOAD_PREFER_SYSTEM32',
    16: 'PS_MITIGATION_OPTION_RETURN_FLOW_GUARD',
    17: 'PS_MITIGATION_OPTION_LOADER_INTEGRITY_CONTINUITY',
    18: 'PS_MITIGATION_OPTION_STRICT_CONTROL_FLOW_GUARD',
    19: 'PS_MITIGATION_OPTION_RESTRICT_SET_THREAD_CONTEXT',
}
PS_MITIGATION_OPTION_NX = 0
PS_MITIGATION_OPTION_SEHOP = 1
PS_MITIGATION_OPTION_FORCE_RELOCATE_IMAGES = 2
PS_MITIGATION_OPTION_HEAP_TERMINATE = 3
PS_MITIGATION_OPTION_BOTTOM_UP_ASLR = 4
PS_MITIGATION_OPTION_HIGH_ENTROPY_ASLR = 5
PS_MITIGATION_OPTION_STRICT_HANDLE_CHECKS = 6
PS_MITIGATION_OPTION_WIN32K_SYSTEM_CALL_DISABLE = 7
PS_MITIGATION_OPTION_EXTENSION_POINT_DISABLE = 8
PS_MITIGATION_OPTION_PROHIBIT_DYNAMIC_CODE = 9
PS_MITIGATION_OPTION_CONTROL_FLOW_GUARD = 10
PS_MITIGATION_OPTION_BLOCK_NON_MICROSOFT_BINARIES = 11
PS_MITIGATION_OPTION_FONT_DISABLE = 12
PS_MITIGATION_OPTION_IMAGE_LOAD_NO_REMOTE = 13
PS_MITIGATION_OPTION_IMAGE_LOAD_NO_LOW_LABEL = 14
PS_MITIGATION_OPTION_IMAGE_LOAD_PREFER_SYSTEM32 = 15
PS_MITIGATION_OPTION_RETURN_FLOW_GUARD = 16
PS_MITIGATION_OPTION_LOADER_INTEGRITY_CONTINUITY = 17
PS_MITIGATION_OPTION_STRICT_CONTROL_FLOW_GUARD = 18
PS_MITIGATION_OPTION_RESTRICT_SET_THREAD_CONTEXT = 19
_PS_MITIGATION_OPTION = ctypes.c_uint32 # enum
PS_MITIGATION_OPTION = _PS_MITIGATION_OPTION
PS_MITIGATION_OPTION__enumvalues = _PS_MITIGATION_OPTION__enumvalues

# values for enumeration '_PS_CREATE_STATE'
_PS_CREATE_STATE__enumvalues = {
    0: 'PsCreateInitialState',
    1: 'PsCreateFailOnFileOpen',
    2: 'PsCreateFailOnSectionCreate',
    3: 'PsCreateFailExeFormat',
    4: 'PsCreateFailMachineMismatch',
    5: 'PsCreateFailExeName',
    6: 'PsCreateSuccess',
    7: 'PsCreateMaximumStates',
}
PsCreateInitialState = 0
PsCreateFailOnFileOpen = 1
PsCreateFailOnSectionCreate = 2
PsCreateFailExeFormat = 3
PsCreateFailMachineMismatch = 4
PsCreateFailExeName = 5
PsCreateSuccess = 6
PsCreateMaximumStates = 7
_PS_CREATE_STATE = ctypes.c_uint32 # enum
PS_CREATE_STATE = _PS_CREATE_STATE
PS_CREATE_STATE__enumvalues = _PS_CREATE_STATE__enumvalues
class struct__PS_CREATE_INFO(Structure):
    pass

class union_union_31(Union):
    pass

class struct_struct_32(Structure):
    pass

class union_union_33(Union):
    pass

class struct_struct_34(Structure):
    pass

struct_struct_34._pack_ = 1 # source:False
struct_struct_34._fields_ = [
    ('ProtectedProcess', ctypes.c_ubyte, 1),
    ('AddressSpaceOverride', ctypes.c_ubyte, 1),
    ('DevOverrideEnabled', ctypes.c_ubyte, 1),
    ('ManifestDetected', ctypes.c_ubyte, 1),
    ('ProtectedProcessLight', ctypes.c_ubyte, 1),
    ('SpareBits1', ctypes.c_ubyte, 3),
    ('SpareBits2', ctypes.c_ubyte, 8),
    ('SpareBits3', ctypes.c_ushort, 16),
]

union_union_33._pack_ = 1 # source:False
union_union_33._fields_ = [
    ('OutputFlags', ctypes.c_uint32),
    ('s2', struct_struct_34),
]

struct_struct_32._pack_ = 1 # source:False
struct_struct_32._fields_ = [
    ('u2', union_union_33),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('FileHandle', ctypes.POINTER(None)),
    ('SectionHandle', ctypes.POINTER(None)),
    ('UserProcessParametersNative', ctypes.c_uint64),
    ('UserProcessParametersWow64', ctypes.c_uint32),
    ('CurrentParameterFlags', ctypes.c_uint32),
    ('PebAddressNative', ctypes.c_uint64),
    ('PebAddressWow64', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('ManifestAddress', ctypes.c_uint64),
    ('ManifestSize', ctypes.c_uint32),
    ('PADDING_2', ctypes.c_ubyte * 4),
]

class struct_struct_35(Structure):
    pass

struct_struct_35._pack_ = 1 # source:False
struct_struct_35._fields_ = [
    ('FileHandle', ctypes.POINTER(None)),
]

class struct_struct_36(Structure):
    pass

struct_struct_36._pack_ = 1 # source:False
struct_struct_36._fields_ = [
    ('IFEOKey', ctypes.POINTER(None)),
]

class struct_struct_37(Structure):
    pass

class union_union_38(Union):
    pass

class struct_struct_39(Structure):
    pass

struct_struct_39._pack_ = 1 # source:False
struct_struct_39._fields_ = [
    ('WriteOutputOnExit', ctypes.c_ubyte, 1),
    ('DetectManifest', ctypes.c_ubyte, 1),
    ('IFEOSkipDebugger', ctypes.c_ubyte, 1),
    ('IFEODoNotPropagateKeyState', ctypes.c_ubyte, 1),
    ('SpareBits1', ctypes.c_ubyte, 4),
    ('SpareBits2', ctypes.c_ubyte, 8),
    ('ProhibitedImageCharacteristics', ctypes.c_ushort, 16),
]

union_union_38._pack_ = 1 # source:False
union_union_38._fields_ = [
    ('InitFlags', ctypes.c_uint32),
    ('s1', struct_struct_39),
]

struct_struct_37._pack_ = 1 # source:False
struct_struct_37._fields_ = [
    ('u1', union_union_38),
    ('AdditionalFileAccess', ctypes.c_uint32),
]

class struct_struct_40(Structure):
    pass

struct_struct_40._pack_ = 1 # source:False
struct_struct_40._fields_ = [
    ('DllCharacteristics', ctypes.c_uint16),
]

union_union_31._pack_ = 1 # source:False
union_union_31._fields_ = [
    ('InitState', struct_struct_37),
    ('FailSection', struct_struct_35),
    ('ExeFormat', struct_struct_40),
    ('ExeName', struct_struct_36),
    ('SuccessState', struct_struct_32),
]

struct__PS_CREATE_INFO._pack_ = 1 # source:False
struct__PS_CREATE_INFO._anonymous_ = ('_0',)
struct__PS_CREATE_INFO._fields_ = [
    ('Size', ctypes.c_uint64),
    ('State', PS_CREATE_STATE),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('_0', union_union_31),
]

PS_CREATE_INFO = struct__PS_CREATE_INFO
PPS_CREATE_INFO = ctypes.POINTER(struct__PS_CREATE_INFO)

# values for enumeration '_MEMORY_RESERVE_TYPE'
_MEMORY_RESERVE_TYPE__enumvalues = {
    0: 'MemoryReserveUserApc',
    1: 'MemoryReserveIoCompletion',
    2: 'MemoryReserveTypeMax',
}
MemoryReserveUserApc = 0
MemoryReserveIoCompletion = 1
MemoryReserveTypeMax = 2
_MEMORY_RESERVE_TYPE = ctypes.c_uint32 # enum
MEMORY_RESERVE_TYPE = _MEMORY_RESERVE_TYPE
MEMORY_RESERVE_TYPE__enumvalues = _MEMORY_RESERVE_TYPE__enumvalues
class struct__PROCESS_HANDLE_TRACING_ENABLE(Structure):
    pass

struct__PROCESS_HANDLE_TRACING_ENABLE._pack_ = 1 # source:False
struct__PROCESS_HANDLE_TRACING_ENABLE._fields_ = [
    ('Flags', ctypes.c_uint32),
]

PROCESS_HANDLE_TRACING_ENABLE = struct__PROCESS_HANDLE_TRACING_ENABLE
PPROCESS_HANDLE_TRACING_ENABLE = ctypes.POINTER(struct__PROCESS_HANDLE_TRACING_ENABLE)
class struct__PROCESS_HANDLE_TRACING_ENABLE_EX(Structure):
    pass

struct__PROCESS_HANDLE_TRACING_ENABLE_EX._pack_ = 1 # source:False
struct__PROCESS_HANDLE_TRACING_ENABLE_EX._fields_ = [
    ('Flags', ctypes.c_uint32),
    ('TotalSlots', ctypes.c_uint32),
]

PROCESS_HANDLE_TRACING_ENABLE_EX = struct__PROCESS_HANDLE_TRACING_ENABLE_EX
PPROCESS_HANDLE_TRACING_ENABLE_EX = ctypes.POINTER(struct__PROCESS_HANDLE_TRACING_ENABLE_EX)

# values for enumeration '_PROCESSINFOCLASS'
_PROCESSINFOCLASS__enumvalues = {
    0: 'ProcessBasicInformation',
    1: 'ProcessQuotaLimits',
    2: 'ProcessIoCounters',
    3: 'ProcessVmCounters',
    4: 'ProcessTimes',
    5: 'ProcessBasePriority',
    6: 'ProcessRaisePriority',
    7: 'ProcessDebugPort',
    8: 'ProcessExceptionPort',
    9: 'ProcessAccessToken',
    10: 'ProcessLdtInformation',
    11: 'ProcessLdtSize',
    12: 'ProcessDefaultHardErrorMode',
    13: 'ProcessIoPortHandlers',
    14: 'ProcessPooledUsageAndLimits',
    15: 'ProcessWorkingSetWatch',
    16: 'ProcessUserModeIOPL',
    17: 'ProcessEnableAlignmentFaultFixup',
    18: 'ProcessPriorityClass',
    19: 'ProcessWx86Information',
    20: 'ProcessHandleCount',
    21: 'ProcessAffinityMask',
    22: 'ProcessPriorityBoost',
    23: 'ProcessDeviceMap',
    24: 'ProcessSessionInformation',
    25: 'ProcessForegroundInformation',
    26: 'ProcessWow64Information',
    27: 'ProcessImageFileName',
    28: 'ProcessLUIDDeviceMapsEnabled',
    29: 'ProcessBreakOnTermination',
    30: 'ProcessDebugObjectHandle',
    31: 'ProcessDebugFlags',
    32: 'ProcessHandleTracing',
    33: 'ProcessIoPriority',
    34: 'ProcessExecuteFlags',
    35: 'ProcessResourceManagement',
    36: 'ProcessCookie',
    37: 'ProcessImageInformation',
    38: 'ProcessCycleTime',
    39: 'ProcessPagePriority',
    40: 'ProcessInstrumentationCallback',
    41: 'ProcessThreadStackAllocation',
    42: 'ProcessWorkingSetWatchEx',
    43: 'ProcessImageFileNameWin32',
    44: 'ProcessImageFileMapping',
    45: 'ProcessAffinityUpdateMode',
    46: 'ProcessMemoryAllocationMode',
    47: 'ProcessGroupInformation',
    48: 'ProcessTokenVirtualizationEnabled',
    49: 'ProcessConsoleHostProcess',
    50: 'ProcessWindowInformation',
    51: 'ProcessHandleInformation',
    52: 'ProcessMitigationPolicy',
    53: 'ProcessDynamicFunctionTableInformation',
    54: 'ProcessHandleCheckingMode',
    55: 'ProcessKeepAliveCount',
    56: 'ProcessRevokeFileHandles',
    57: 'ProcessWorkingSetControl',
    58: 'ProcessHandleTable',
    59: 'ProcessCheckStackExtentsMode',
    60: 'ProcessCommandLineInformation',
    61: 'ProcessProtectionInformation',
    62: 'ProcessMemoryExhaustion',
    63: 'ProcessFaultInformation',
    64: 'ProcessTelemetryIdInformation',
    65: 'ProcessCommitReleaseInformation',
    66: 'ProcessDefaultCpuSetsInformation',
    67: 'ProcessAllowedCpuSetsInformation',
    68: 'ProcessSubsystemProcess',
    69: 'ProcessJobMemoryInformation',
    70: 'ProcessInPrivate',
    71: 'ProcessRaiseUMExceptionOnInvalidHandleClose',
    72: 'ProcessIumChallengeResponse',
    73: 'ProcessChildProcessInformation',
    74: 'ProcessHighGraphicsPriorityInformation',
    75: 'ProcessSubsystemInformation',
    76: 'ProcessEnergyValues',
    77: 'ProcessActivityThrottleState',
    78: 'ProcessActivityThrottlePolicy',
    79: 'ProcessWin32kSyscallFilterInformation',
    80: 'ProcessDisableSystemAllowedCpuSets',
    81: 'ProcessWakeInformation',
    82: 'ProcessEnergyTrackingState',
    83: 'MaxProcessInfoClass',
}
ProcessBasicInformation = 0
ProcessQuotaLimits = 1
ProcessIoCounters = 2
ProcessVmCounters = 3
ProcessTimes = 4
ProcessBasePriority = 5
ProcessRaisePriority = 6
ProcessDebugPort = 7
ProcessExceptionPort = 8
ProcessAccessToken = 9
ProcessLdtInformation = 10
ProcessLdtSize = 11
ProcessDefaultHardErrorMode = 12
ProcessIoPortHandlers = 13
ProcessPooledUsageAndLimits = 14
ProcessWorkingSetWatch = 15
ProcessUserModeIOPL = 16
ProcessEnableAlignmentFaultFixup = 17
ProcessPriorityClass = 18
ProcessWx86Information = 19
ProcessHandleCount = 20
ProcessAffinityMask = 21
ProcessPriorityBoost = 22
ProcessDeviceMap = 23
ProcessSessionInformation = 24
ProcessForegroundInformation = 25
ProcessWow64Information = 26
ProcessImageFileName = 27
ProcessLUIDDeviceMapsEnabled = 28
ProcessBreakOnTermination = 29
ProcessDebugObjectHandle = 30
ProcessDebugFlags = 31
ProcessHandleTracing = 32
ProcessIoPriority = 33
ProcessExecuteFlags = 34
ProcessResourceManagement = 35
ProcessCookie = 36
ProcessImageInformation = 37
ProcessCycleTime = 38
ProcessPagePriority = 39
ProcessInstrumentationCallback = 40
ProcessThreadStackAllocation = 41
ProcessWorkingSetWatchEx = 42
ProcessImageFileNameWin32 = 43
ProcessImageFileMapping = 44
ProcessAffinityUpdateMode = 45
ProcessMemoryAllocationMode = 46
ProcessGroupInformation = 47
ProcessTokenVirtualizationEnabled = 48
ProcessConsoleHostProcess = 49
ProcessWindowInformation = 50
ProcessHandleInformation = 51
ProcessMitigationPolicy = 52
ProcessDynamicFunctionTableInformation = 53
ProcessHandleCheckingMode = 54
ProcessKeepAliveCount = 55
ProcessRevokeFileHandles = 56
ProcessWorkingSetControl = 57
ProcessHandleTable = 58
ProcessCheckStackExtentsMode = 59
ProcessCommandLineInformation = 60
ProcessProtectionInformation = 61
ProcessMemoryExhaustion = 62
ProcessFaultInformation = 63
ProcessTelemetryIdInformation = 64
ProcessCommitReleaseInformation = 65
ProcessDefaultCpuSetsInformation = 66
ProcessAllowedCpuSetsInformation = 67
ProcessSubsystemProcess = 68
ProcessJobMemoryInformation = 69
ProcessInPrivate = 70
ProcessRaiseUMExceptionOnInvalidHandleClose = 71
ProcessIumChallengeResponse = 72
ProcessChildProcessInformation = 73
ProcessHighGraphicsPriorityInformation = 74
ProcessSubsystemInformation = 75
ProcessEnergyValues = 76
ProcessActivityThrottleState = 77
ProcessActivityThrottlePolicy = 78
ProcessWin32kSyscallFilterInformation = 79
ProcessDisableSystemAllowedCpuSets = 80
ProcessWakeInformation = 81
ProcessEnergyTrackingState = 82
MaxProcessInfoClass = 83
_PROCESSINFOCLASS = ctypes.c_uint32 # enum
PROCESSINFOCLASS = _PROCESSINFOCLASS
PROCESSINFOCLASS__enumvalues = _PROCESSINFOCLASS__enumvalues

# values for enumeration '_SYSTEM_INFORMATION_CLASS'
_SYSTEM_INFORMATION_CLASS__enumvalues = {
    0: 'SystemBasicInformation',
    1: 'SystemProcessorInformation',
    2: 'SystemPerformanceInformation',
    3: 'SystemTimeOfDayInformation',
    4: 'SystemPathInformation',
    5: 'SystemProcessInformation',
    6: 'SystemCallCountInformation',
    7: 'SystemDeviceInformation',
    8: 'SystemProcessorPerformanceInformation',
    9: 'SystemFlagsInformation',
    10: 'SystemCallTimeInformation',
    11: 'SystemModuleInformation',
    12: 'SystemLocksInformation',
    13: 'SystemStackTraceInformation',
    14: 'SystemPagedPoolInformation',
    15: 'SystemNonPagedPoolInformation',
    16: 'SystemHandleInformation',
    17: 'SystemObjectInformation',
    18: 'SystemPageFileInformation',
    19: 'SystemVdmInstemulInformation',
    20: 'SystemVdmBopInformation',
    21: 'SystemFileCacheInformation',
    22: 'SystemPoolTagInformation',
    23: 'SystemInterruptInformation',
    24: 'SystemDpcBehaviorInformation',
    25: 'SystemFullMemoryInformation',
    26: 'SystemLoadGdiDriverInformation',
    27: 'SystemUnloadGdiDriverInformation',
    28: 'SystemTimeAdjustmentInformation',
    29: 'SystemSummaryMemoryInformation',
    30: 'SystemMirrorMemoryInformation',
    31: 'SystemPerformanceTraceInformation',
    32: 'SystemObsolete0',
    33: 'SystemExceptionInformation',
    34: 'SystemCrashDumpStateInformation',
    35: 'SystemKernelDebuggerInformation',
    36: 'SystemContextSwitchInformation',
    37: 'SystemRegistryQuotaInformation',
    38: 'SystemExtendServiceTableInformation',
    39: 'SystemPrioritySeperation',
    40: 'SystemVerifierAddDriverInformation',
    41: 'SystemVerifierRemoveDriverInformation',
    42: 'SystemProcessorIdleInformation',
    43: 'SystemLegacyDriverInformation',
    44: 'SystemCurrentTimeZoneInformation',
    45: 'SystemLookasideInformation',
    46: 'SystemTimeSlipNotification',
    47: 'SystemSessionCreate',
    48: 'SystemSessionDetach',
    49: 'SystemSessionInformation',
    50: 'SystemRangeStartInformation',
    51: 'SystemVerifierInformation',
    52: 'SystemVerifierThunkExtend',
    53: 'SystemSessionProcessInformation',
    54: 'SystemLoadGdiDriverInSystemSpace',
    55: 'SystemNumaProcessorMap',
    56: 'SystemPrefetcherInformation',
    57: 'SystemExtendedProcessInformation',
    58: 'SystemRecommendedSharedDataAlignment',
    59: 'SystemComPlusPackage',
    60: 'SystemNumaAvailableMemory',
    61: 'SystemProcessorPowerInformation',
    62: 'SystemEmulationBasicInformation',
    63: 'SystemEmulationProcessorInformation',
    64: 'SystemExtendedHandleInformation',
    65: 'SystemLostDelayedWriteInformation',
    66: 'SystemBigPoolInformation',
    67: 'SystemSessionPoolTagInformation',
    68: 'SystemSessionMappedViewInformation',
    69: 'SystemHotpatchInformation',
    70: 'SystemObjectSecurityMode',
    71: 'SystemWatchdogTimerHandler',
    72: 'SystemWatchdogTimerInformation',
    73: 'SystemLogicalProcessorInformation',
    74: 'SystemWow64SharedInformationObsolete',
    75: 'SystemRegisterFirmwareTableInformationHandler',
    76: 'SystemFirmwareTableInformation',
    77: 'SystemModuleInformationEx',
    78: 'SystemVerifierTriageInformation',
    79: 'SystemSuperfetchInformation',
    80: 'SystemMemoryListInformation',
    81: 'SystemFileCacheInformationEx',
    82: 'SystemThreadPriorityClientIdInformation',
    83: 'SystemProcessorIdleCycleTimeInformation',
    84: 'SystemVerifierCancellationInformation',
    85: 'SystemProcessorPowerInformationEx',
    86: 'SystemRefTraceInformation',
    87: 'SystemSpecialPoolInformation',
    88: 'SystemProcessIdInformation',
    89: 'SystemErrorPortInformation',
    90: 'SystemBootEnvironmentInformation',
    91: 'SystemHypervisorInformation',
    92: 'SystemVerifierInformationEx',
    93: 'SystemTimeZoneInformation',
    94: 'SystemImageFileExecutionOptionsInformation',
    95: 'SystemCoverageInformation',
    96: 'SystemPrefetchPatchInformation',
    97: 'SystemVerifierFaultsInformation',
    98: 'SystemSystemPartitionInformation',
    99: 'SystemSystemDiskInformation',
    100: 'SystemProcessorPerformanceDistribution',
    101: 'SystemNumaProximityNodeInformation',
    102: 'SystemDynamicTimeZoneInformation',
    103: 'SystemCodeIntegrityInformation',
    104: 'SystemProcessorMicrocodeUpdateInformation',
    105: 'SystemProcessorBrandString',
    106: 'SystemVirtualAddressInformation',
    107: 'SystemLogicalProcessorAndGroupInformation',
    108: 'SystemProcessorCycleTimeInformation',
    109: 'SystemStoreInformation',
    110: 'SystemRegistryAppendString',
    111: 'SystemAitSamplingValue',
    112: 'SystemVhdBootInformation',
    113: 'SystemCpuQuotaInformation',
    114: 'SystemNativeBasicInformation',
    115: 'SystemSpare1',
    116: 'SystemLowPriorityIoInformation',
    117: 'SystemTpmBootEntropyInformation',
    118: 'SystemVerifierCountersInformation',
    119: 'SystemPagedPoolInformationEx',
    120: 'SystemSystemPtesInformationEx',
    121: 'SystemNodeDistanceInformation',
    122: 'SystemAcpiAuditInformation',
    123: 'SystemBasicPerformanceInformation',
    124: 'SystemQueryPerformanceCounterInformation',
    125: 'SystemSessionBigPoolInformation',
    126: 'SystemBootGraphicsInformation',
    127: 'SystemScrubPhysicalMemoryInformation',
    128: 'SystemBadPageInformation',
    129: 'SystemProcessorProfileControlArea',
    130: 'SystemCombinePhysicalMemoryInformation',
    131: 'SystemEntropyInterruptTimingCallback',
    132: 'SystemConsoleInformation',
    133: 'SystemPlatformBinaryInformation',
    134: 'SystemThrottleNotificationInformation',
    135: 'SystemHypervisorProcessorCountInformation',
    136: 'SystemDeviceDataInformation',
    137: 'SystemDeviceDataEnumerationInformation',
    138: 'SystemMemoryTopologyInformation',
    139: 'SystemMemoryChannelInformation',
    140: 'SystemBootLogoInformation',
    141: 'SystemProcessorPerformanceInformationEx',
    142: 'SystemSpare0',
    143: 'SystemSecureBootPolicyInformation',
    144: 'SystemPageFileInformationEx',
    145: 'SystemSecureBootInformation',
    146: 'SystemEntropyInterruptTimingRawInformation',
    147: 'SystemPortableWorkspaceEfiLauncherInformation',
    148: 'SystemFullProcessInformation',
    149: 'SystemKernelDebuggerInformationEx',
    150: 'SystemBootMetadataInformation',
    151: 'SystemSoftRebootInformation',
    152: 'SystemElamCertificateInformation',
    153: 'SystemOfflineDumpConfigInformation',
    154: 'SystemProcessorFeaturesInformation',
    155: 'SystemRegistryReconciliationInformation',
    156: 'SystemEdidInformation',
    157: 'SystemManufacturingInformation',
    158: 'SystemEnergyEstimationConfigInformation',
    159: 'SystemHypervisorDetailInformation',
    160: 'SystemProcessorCycleStatsInformation',
    161: 'SystemVmGenerationCountInformation',
    162: 'SystemTrustedPlatformModuleInformation',
    163: 'SystemKernelDebuggerFlags',
    164: 'SystemCodeIntegrityPolicyInformation',
    165: 'SystemIsolatedUserModeInformation',
    166: 'SystemHardwareSecurityTestInterfaceResultsInformation',
    167: 'SystemSingleModuleInformation',
    168: 'SystemAllowedCpuSetsInformation',
    169: 'SystemDmaProtectionInformation',
    170: 'SystemInterruptCpuSetsInformation',
    171: 'SystemSecureBootPolicyFullInformation',
    172: 'SystemCodeIntegrityPolicyFullInformation',
    173: 'SystemAffinitizedInterruptProcessorInformation',
    174: 'SystemRootSiloInformation',
    175: 'SystemCpuSetInformation',
    176: 'SystemCpuSetTagInformation',
    177: 'SystemWin32WerStartCallout',
    178: 'SystemSecureKernelProfileInformation',
    179: 'SystemCodeIntegrityPlatformManifestInformation',
    180: 'SystemInterruptSteeringInformation',
    181: 'SystemSupportedProcessorArchitectures',
    182: 'SystemMemoryUsageInformation',
    183: 'SystemCodeIntegrityCertificateInformation',
    184: 'SystemPhysicalMemoryInformation',
    185: 'SystemControlFlowTransition',
    186: 'SystemKernelDebuggingAllowed',
    187: 'SystemActivityModerationExeState',
    188: 'SystemActivityModerationUserSettings',
    189: 'SystemCodeIntegrityPoliciesFullInformation',
    190: 'SystemCodeIntegrityUnlockInformation',
    191: 'SystemIntegrityQuotaInformation',
    192: 'SystemFlushInformation',
    193: 'MaxSystemInfoClass',
}
SystemBasicInformation = 0
SystemProcessorInformation = 1
SystemPerformanceInformation = 2
SystemTimeOfDayInformation = 3
SystemPathInformation = 4
SystemProcessInformation = 5
SystemCallCountInformation = 6
SystemDeviceInformation = 7
SystemProcessorPerformanceInformation = 8
SystemFlagsInformation = 9
SystemCallTimeInformation = 10
SystemModuleInformation = 11
SystemLocksInformation = 12
SystemStackTraceInformation = 13
SystemPagedPoolInformation = 14
SystemNonPagedPoolInformation = 15
SystemHandleInformation = 16
SystemObjectInformation = 17
SystemPageFileInformation = 18
SystemVdmInstemulInformation = 19
SystemVdmBopInformation = 20
SystemFileCacheInformation = 21
SystemPoolTagInformation = 22
SystemInterruptInformation = 23
SystemDpcBehaviorInformation = 24
SystemFullMemoryInformation = 25
SystemLoadGdiDriverInformation = 26
SystemUnloadGdiDriverInformation = 27
SystemTimeAdjustmentInformation = 28
SystemSummaryMemoryInformation = 29
SystemMirrorMemoryInformation = 30
SystemPerformanceTraceInformation = 31
SystemObsolete0 = 32
SystemExceptionInformation = 33
SystemCrashDumpStateInformation = 34
SystemKernelDebuggerInformation = 35
SystemContextSwitchInformation = 36
SystemRegistryQuotaInformation = 37
SystemExtendServiceTableInformation = 38
SystemPrioritySeperation = 39
SystemVerifierAddDriverInformation = 40
SystemVerifierRemoveDriverInformation = 41
SystemProcessorIdleInformation = 42
SystemLegacyDriverInformation = 43
SystemCurrentTimeZoneInformation = 44
SystemLookasideInformation = 45
SystemTimeSlipNotification = 46
SystemSessionCreate = 47
SystemSessionDetach = 48
SystemSessionInformation = 49
SystemRangeStartInformation = 50
SystemVerifierInformation = 51
SystemVerifierThunkExtend = 52
SystemSessionProcessInformation = 53
SystemLoadGdiDriverInSystemSpace = 54
SystemNumaProcessorMap = 55
SystemPrefetcherInformation = 56
SystemExtendedProcessInformation = 57
SystemRecommendedSharedDataAlignment = 58
SystemComPlusPackage = 59
SystemNumaAvailableMemory = 60
SystemProcessorPowerInformation = 61
SystemEmulationBasicInformation = 62
SystemEmulationProcessorInformation = 63
SystemExtendedHandleInformation = 64
SystemLostDelayedWriteInformation = 65
SystemBigPoolInformation = 66
SystemSessionPoolTagInformation = 67
SystemSessionMappedViewInformation = 68
SystemHotpatchInformation = 69
SystemObjectSecurityMode = 70
SystemWatchdogTimerHandler = 71
SystemWatchdogTimerInformation = 72
SystemLogicalProcessorInformation = 73
SystemWow64SharedInformationObsolete = 74
SystemRegisterFirmwareTableInformationHandler = 75
SystemFirmwareTableInformation = 76
SystemModuleInformationEx = 77
SystemVerifierTriageInformation = 78
SystemSuperfetchInformation = 79
SystemMemoryListInformation = 80
SystemFileCacheInformationEx = 81
SystemThreadPriorityClientIdInformation = 82
SystemProcessorIdleCycleTimeInformation = 83
SystemVerifierCancellationInformation = 84
SystemProcessorPowerInformationEx = 85
SystemRefTraceInformation = 86
SystemSpecialPoolInformation = 87
SystemProcessIdInformation = 88
SystemErrorPortInformation = 89
SystemBootEnvironmentInformation = 90
SystemHypervisorInformation = 91
SystemVerifierInformationEx = 92
SystemTimeZoneInformation = 93
SystemImageFileExecutionOptionsInformation = 94
SystemCoverageInformation = 95
SystemPrefetchPatchInformation = 96
SystemVerifierFaultsInformation = 97
SystemSystemPartitionInformation = 98
SystemSystemDiskInformation = 99
SystemProcessorPerformanceDistribution = 100
SystemNumaProximityNodeInformation = 101
SystemDynamicTimeZoneInformation = 102
SystemCodeIntegrityInformation = 103
SystemProcessorMicrocodeUpdateInformation = 104
SystemProcessorBrandString = 105
SystemVirtualAddressInformation = 106
SystemLogicalProcessorAndGroupInformation = 107
SystemProcessorCycleTimeInformation = 108
SystemStoreInformation = 109
SystemRegistryAppendString = 110
SystemAitSamplingValue = 111
SystemVhdBootInformation = 112
SystemCpuQuotaInformation = 113
SystemNativeBasicInformation = 114
SystemSpare1 = 115
SystemLowPriorityIoInformation = 116
SystemTpmBootEntropyInformation = 117
SystemVerifierCountersInformation = 118
SystemPagedPoolInformationEx = 119
SystemSystemPtesInformationEx = 120
SystemNodeDistanceInformation = 121
SystemAcpiAuditInformation = 122
SystemBasicPerformanceInformation = 123
SystemQueryPerformanceCounterInformation = 124
SystemSessionBigPoolInformation = 125
SystemBootGraphicsInformation = 126
SystemScrubPhysicalMemoryInformation = 127
SystemBadPageInformation = 128
SystemProcessorProfileControlArea = 129
SystemCombinePhysicalMemoryInformation = 130
SystemEntropyInterruptTimingCallback = 131
SystemConsoleInformation = 132
SystemPlatformBinaryInformation = 133
SystemThrottleNotificationInformation = 134
SystemHypervisorProcessorCountInformation = 135
SystemDeviceDataInformation = 136
SystemDeviceDataEnumerationInformation = 137
SystemMemoryTopologyInformation = 138
SystemMemoryChannelInformation = 139
SystemBootLogoInformation = 140
SystemProcessorPerformanceInformationEx = 141
SystemSpare0 = 142
SystemSecureBootPolicyInformation = 143
SystemPageFileInformationEx = 144
SystemSecureBootInformation = 145
SystemEntropyInterruptTimingRawInformation = 146
SystemPortableWorkspaceEfiLauncherInformation = 147
SystemFullProcessInformation = 148
SystemKernelDebuggerInformationEx = 149
SystemBootMetadataInformation = 150
SystemSoftRebootInformation = 151
SystemElamCertificateInformation = 152
SystemOfflineDumpConfigInformation = 153
SystemProcessorFeaturesInformation = 154
SystemRegistryReconciliationInformation = 155
SystemEdidInformation = 156
SystemManufacturingInformation = 157
SystemEnergyEstimationConfigInformation = 158
SystemHypervisorDetailInformation = 159
SystemProcessorCycleStatsInformation = 160
SystemVmGenerationCountInformation = 161
SystemTrustedPlatformModuleInformation = 162
SystemKernelDebuggerFlags = 163
SystemCodeIntegrityPolicyInformation = 164
SystemIsolatedUserModeInformation = 165
SystemHardwareSecurityTestInterfaceResultsInformation = 166
SystemSingleModuleInformation = 167
SystemAllowedCpuSetsInformation = 168
SystemDmaProtectionInformation = 169
SystemInterruptCpuSetsInformation = 170
SystemSecureBootPolicyFullInformation = 171
SystemCodeIntegrityPolicyFullInformation = 172
SystemAffinitizedInterruptProcessorInformation = 173
SystemRootSiloInformation = 174
SystemCpuSetInformation = 175
SystemCpuSetTagInformation = 176
SystemWin32WerStartCallout = 177
SystemSecureKernelProfileInformation = 178
SystemCodeIntegrityPlatformManifestInformation = 179
SystemInterruptSteeringInformation = 180
SystemSupportedProcessorArchitectures = 181
SystemMemoryUsageInformation = 182
SystemCodeIntegrityCertificateInformation = 183
SystemPhysicalMemoryInformation = 184
SystemControlFlowTransition = 185
SystemKernelDebuggingAllowed = 186
SystemActivityModerationExeState = 187
SystemActivityModerationUserSettings = 188
SystemCodeIntegrityPoliciesFullInformation = 189
SystemCodeIntegrityUnlockInformation = 190
SystemIntegrityQuotaInformation = 191
SystemFlushInformation = 192
MaxSystemInfoClass = 193
_SYSTEM_INFORMATION_CLASS = ctypes.c_uint32 # enum
SYSTEM_INFORMATION_CLASS = _SYSTEM_INFORMATION_CLASS
SYSTEM_INFORMATION_CLASS__enumvalues = _SYSTEM_INFORMATION_CLASS__enumvalues

# values for enumeration '_OBJECT_INFORMATION_CLASS'
_OBJECT_INFORMATION_CLASS__enumvalues = {
    0: 'ObjectBasicInformation',
    1: 'ObjectNameInformation',
    2: 'ObjectTypeInformation',
    3: 'ObjectTypesInformation',
    4: 'ObjectHandleFlagInformation',
    5: 'ObjectSessionInformation',
    6: 'ObjectSessionObjectInformation',
    7: 'MaxObjectInfoClass',
}
ObjectBasicInformation = 0
ObjectNameInformation = 1
ObjectTypeInformation = 2
ObjectTypesInformation = 3
ObjectHandleFlagInformation = 4
ObjectSessionInformation = 5
ObjectSessionObjectInformation = 6
MaxObjectInfoClass = 7
_OBJECT_INFORMATION_CLASS = ctypes.c_uint32 # enum
OBJECT_INFORMATION_CLASS = _OBJECT_INFORMATION_CLASS
OBJECT_INFORMATION_CLASS__enumvalues = _OBJECT_INFORMATION_CLASS__enumvalues

# values for enumeration '_THREADINFOCLASS'
_THREADINFOCLASS__enumvalues = {
    0: 'ThreadBasicInformation',
    1: 'ThreadTimes',
    2: 'ThreadPriority',
    3: 'ThreadBasePriority',
    4: 'ThreadAffinityMask',
    5: 'ThreadImpersonationToken',
    6: 'ThreadDescriptorTableEntry',
    7: 'ThreadEnableAlignmentFaultFixup',
    8: 'ThreadEventPair',
    9: 'ThreadQuerySetWin32StartAddress',
    10: 'ThreadZeroTlsCell',
    11: 'ThreadPerformanceCount',
    12: 'ThreadAmILastThread',
    13: 'ThreadIdealProcessor',
    14: 'ThreadPriorityBoost',
    15: 'ThreadSetTlsArrayAddress',
    16: 'ThreadIsIoPending',
    17: 'ThreadHideFromDebugger',
    18: 'ThreadBreakOnTermination',
    19: 'ThreadSwitchLegacyState',
    20: 'ThreadIsTerminated',
    21: 'ThreadLastSystemCall',
    22: 'ThreadIoPriority',
    23: 'ThreadCycleTime',
    24: 'ThreadPagePriority',
    25: 'ThreadActualBasePriority',
    26: 'ThreadTebInformation',
    27: 'ThreadCSwitchMon',
    28: 'ThreadCSwitchPmu',
    29: 'ThreadWow64Context',
    30: 'ThreadGroupInformation',
    31: 'ThreadUmsInformation',
    32: 'ThreadCounterProfiling',
    33: 'ThreadIdealProcessorEx',
    34: 'ThreadCpuAccountingInformation',
    35: 'ThreadSuspendCount',
    36: 'ThreadHeterogeneousCpuPolicy',
    37: 'ThreadContainerId',
    38: 'ThreadNameInformation',
    39: 'ThreadSelectedCpuSets',
    40: 'ThreadSystemThreadInformation',
    41: 'ThreadActualGroupAffinity',
    42: 'ThreadDynamicCodePolicyInfo',
    43: 'ThreadExplicitCaseSensitivity',
    44: 'ThreadWorkOnBehalfTicket',
    45: 'ThreadSubsystemInformation',
    46: 'ThreadDbgkWerReportActive',
    47: 'ThreadAttachContainer',
    48: 'MaxThreadInfoClass',
}
ThreadBasicInformation = 0
ThreadTimes = 1
ThreadPriority = 2
ThreadBasePriority = 3
ThreadAffinityMask = 4
ThreadImpersonationToken = 5
ThreadDescriptorTableEntry = 6
ThreadEnableAlignmentFaultFixup = 7
ThreadEventPair = 8
ThreadQuerySetWin32StartAddress = 9
ThreadZeroTlsCell = 10
ThreadPerformanceCount = 11
ThreadAmILastThread = 12
ThreadIdealProcessor = 13
ThreadPriorityBoost = 14
ThreadSetTlsArrayAddress = 15
ThreadIsIoPending = 16
ThreadHideFromDebugger = 17
ThreadBreakOnTermination = 18
ThreadSwitchLegacyState = 19
ThreadIsTerminated = 20
ThreadLastSystemCall = 21
ThreadIoPriority = 22
ThreadCycleTime = 23
ThreadPagePriority = 24
ThreadActualBasePriority = 25
ThreadTebInformation = 26
ThreadCSwitchMon = 27
ThreadCSwitchPmu = 28
ThreadWow64Context = 29
ThreadGroupInformation = 30
ThreadUmsInformation = 31
ThreadCounterProfiling = 32
ThreadIdealProcessorEx = 33
ThreadCpuAccountingInformation = 34
ThreadSuspendCount = 35
ThreadHeterogeneousCpuPolicy = 36
ThreadContainerId = 37
ThreadNameInformation = 38
ThreadSelectedCpuSets = 39
ThreadSystemThreadInformation = 40
ThreadActualGroupAffinity = 41
ThreadDynamicCodePolicyInfo = 42
ThreadExplicitCaseSensitivity = 43
ThreadWorkOnBehalfTicket = 44
ThreadSubsystemInformation = 45
ThreadDbgkWerReportActive = 46
ThreadAttachContainer = 47
MaxThreadInfoClass = 48
_THREADINFOCLASS = ctypes.c_uint32 # enum
THREADINFOCLASS = _THREADINFOCLASS
THREADINFOCLASS__enumvalues = _THREADINFOCLASS__enumvalues

# values for enumeration '_FSINFOCLASS'
_FSINFOCLASS__enumvalues = {
    1: 'FileFsVolumeInformation',
    2: 'FileFsLabelInformation',
    3: 'FileFsSizeInformation',
    4: 'FileFsDeviceInformation',
    5: 'FileFsAttributeInformation',
    6: 'FileFsControlInformation',
    7: 'FileFsFullSizeInformation',
    8: 'FileFsObjectIdInformation',
    9: 'FileFsDriverPathInformation',
    10: 'FileFsVolumeFlagsInformation',
    11: 'FileFsSectorSizeInformation',
    12: 'FileFsDataCopyInformation',
    13: 'FileFsMetadataSizeInformation',
    14: 'FileFsMaximumInformation',
}
FileFsVolumeInformation = 1
FileFsLabelInformation = 2
FileFsSizeInformation = 3
FileFsDeviceInformation = 4
FileFsAttributeInformation = 5
FileFsControlInformation = 6
FileFsFullSizeInformation = 7
FileFsObjectIdInformation = 8
FileFsDriverPathInformation = 9
FileFsVolumeFlagsInformation = 10
FileFsSectorSizeInformation = 11
FileFsDataCopyInformation = 12
FileFsMetadataSizeInformation = 13
FileFsMaximumInformation = 14
_FSINFOCLASS = ctypes.c_uint32 # enum
FS_INFORMATION_CLASS = _FSINFOCLASS
FS_INFORMATION_CLASS__enumvalues = _FSINFOCLASS__enumvalues
PFS_INFORMATION_CLASS = ctypes.POINTER(_FSINFOCLASS)

# values for enumeration '_MEMORY_INFORMATION_CLASS'
_MEMORY_INFORMATION_CLASS__enumvalues = {
    0: 'MemoryBasicInformation',
    1: 'MemoryWorkingSetInformation',
    2: 'MemoryMappedFilenameInformation',
    3: 'MemoryRegionInformation',
    4: 'MemoryWorkingSetExInformation',
    5: 'MemorySharedCommitInformation',
    6: 'MemoryImageInformation',
    7: 'MemoryRegionInformationEx',
    8: 'MemoryPrivilegedBasicInformation',
}
MemoryBasicInformation = 0
MemoryWorkingSetInformation = 1
MemoryMappedFilenameInformation = 2
MemoryRegionInformation = 3
MemoryWorkingSetExInformation = 4
MemorySharedCommitInformation = 5
MemoryImageInformation = 6
MemoryRegionInformationEx = 7
MemoryPrivilegedBasicInformation = 8
_MEMORY_INFORMATION_CLASS = ctypes.c_uint32 # enum
MEMORY_INFORMATION_CLASS = _MEMORY_INFORMATION_CLASS
MEMORY_INFORMATION_CLASS__enumvalues = _MEMORY_INFORMATION_CLASS__enumvalues

# values for enumeration '_SECTION_INFORMATION_CLASS'
_SECTION_INFORMATION_CLASS__enumvalues = {
    0: 'SectionBasicInformation',
    1: 'SectionImageInformation',
    2: 'SectionRelocationInformation',
    3: 'SectionOriginalBaseInformation',
    4: 'SectionInternalImageInformation',
    5: 'MaxSectionInfoClass',
}
SectionBasicInformation = 0
SectionImageInformation = 1
SectionRelocationInformation = 2
SectionOriginalBaseInformation = 3
SectionInternalImageInformation = 4
MaxSectionInfoClass = 5
_SECTION_INFORMATION_CLASS = ctypes.c_uint32 # enum
SECTION_INFORMATION_CLASS = _SECTION_INFORMATION_CLASS
SECTION_INFORMATION_CLASS__enumvalues = _SECTION_INFORMATION_CLASS__enumvalues

# values for enumeration '_KEY_INFORMATION_CLASS'
_KEY_INFORMATION_CLASS__enumvalues = {
    0: 'KeyBasicInformation',
    1: 'KeyNodeInformation',
    2: 'KeyFullInformation',
    3: 'KeyNameInformation',
    4: 'KeyCachedInformation',
    5: 'KeyFlagsInformation',
    6: 'KeyVirtualizationInformation',
    7: 'KeyHandleTagsInformation',
    8: 'KeyTrustInformation',
    9: 'KeyLayerInformation',
    10: 'MaxKeyInfoClass',
}
KeyBasicInformation = 0
KeyNodeInformation = 1
KeyFullInformation = 2
KeyNameInformation = 3
KeyCachedInformation = 4
KeyFlagsInformation = 5
KeyVirtualizationInformation = 6
KeyHandleTagsInformation = 7
KeyTrustInformation = 8
KeyLayerInformation = 9
MaxKeyInfoClass = 10
_KEY_INFORMATION_CLASS = ctypes.c_uint32 # enum
KEY_INFORMATION_CLASS = _KEY_INFORMATION_CLASS
KEY_INFORMATION_CLASS__enumvalues = _KEY_INFORMATION_CLASS__enumvalues
class struct__KEY_BASIC_INFORMATION(Structure):
    pass

struct__KEY_BASIC_INFORMATION._pack_ = 1 # source:False
struct__KEY_BASIC_INFORMATION._fields_ = [
    ('LastWriteTime', union__LARGE_INTEGER),
    ('TitleIndex', ctypes.c_uint32),
    ('NameLength', ctypes.c_uint32),
    ('Name', ctypes.c_uint16 * 1),
    ('PADDING_0', ctypes.c_ubyte * 6),
]

KEY_BASIC_INFORMATION = struct__KEY_BASIC_INFORMATION
PKEY_BASIC_INFORMATION = ctypes.POINTER(struct__KEY_BASIC_INFORMATION)
class struct__KEY_NODE_INFORMATION(Structure):
    pass

struct__KEY_NODE_INFORMATION._pack_ = 1 # source:False
struct__KEY_NODE_INFORMATION._fields_ = [
    ('LastWriteTime', union__LARGE_INTEGER),
    ('TitleIndex', ctypes.c_uint32),
    ('ClassOffset', ctypes.c_uint32),
    ('ClassLength', ctypes.c_uint32),
    ('NameLength', ctypes.c_uint32),
    ('Name', ctypes.c_uint16 * 1),
    ('PADDING_0', ctypes.c_ubyte * 6),
]

KEY_NODE_INFORMATION = struct__KEY_NODE_INFORMATION
PKEY_NODE_INFORMATION = ctypes.POINTER(struct__KEY_NODE_INFORMATION)
class struct__KEY_FULL_INFORMATION(Structure):
    pass

struct__KEY_FULL_INFORMATION._pack_ = 1 # source:False
struct__KEY_FULL_INFORMATION._fields_ = [
    ('LastWriteTime', union__LARGE_INTEGER),
    ('TitleIndex', ctypes.c_uint32),
    ('ClassOffset', ctypes.c_uint32),
    ('ClassLength', ctypes.c_uint32),
    ('SubKeys', ctypes.c_uint32),
    ('MaxNameLen', ctypes.c_uint32),
    ('MaxClassLen', ctypes.c_uint32),
    ('Values', ctypes.c_uint32),
    ('MaxValueNameLen', ctypes.c_uint32),
    ('MaxValueDataLen', ctypes.c_uint32),
    ('Class', ctypes.c_uint16 * 1),
    ('PADDING_0', ctypes.c_ubyte * 2),
]

KEY_FULL_INFORMATION = struct__KEY_FULL_INFORMATION
PKEY_FULL_INFORMATION = ctypes.POINTER(struct__KEY_FULL_INFORMATION)
class struct__KEY_NAME_INFORMATION(Structure):
    pass

struct__KEY_NAME_INFORMATION._pack_ = 1 # source:False
struct__KEY_NAME_INFORMATION._fields_ = [
    ('NameLength', ctypes.c_uint32),
    ('Name', ctypes.c_uint16 * 1),
    ('PADDING_0', ctypes.c_ubyte * 2),
]

KEY_NAME_INFORMATION = struct__KEY_NAME_INFORMATION
PKEY_NAME_INFORMATION = ctypes.POINTER(struct__KEY_NAME_INFORMATION)
class struct__KEY_CACHED_INFORMATION(Structure):
    pass

struct__KEY_CACHED_INFORMATION._pack_ = 1 # source:False
struct__KEY_CACHED_INFORMATION._fields_ = [
    ('LastWriteTime', union__LARGE_INTEGER),
    ('TitleIndex', ctypes.c_uint32),
    ('SubKeys', ctypes.c_uint32),
    ('MaxNameLen', ctypes.c_uint32),
    ('Values', ctypes.c_uint32),
    ('MaxValueNameLen', ctypes.c_uint32),
    ('MaxValueDataLen', ctypes.c_uint32),
    ('NameLength', ctypes.c_uint32),
    ('Name', ctypes.c_uint16 * 1),
    ('PADDING_0', ctypes.c_ubyte * 2),
]

KEY_CACHED_INFORMATION = struct__KEY_CACHED_INFORMATION
PKEY_CACHED_INFORMATION = ctypes.POINTER(struct__KEY_CACHED_INFORMATION)
class struct__KEY_FLAGS_INFORMATION(Structure):
    pass

struct__KEY_FLAGS_INFORMATION._pack_ = 1 # source:False
struct__KEY_FLAGS_INFORMATION._fields_ = [
    ('UserFlags', ctypes.c_uint32),
]

KEY_FLAGS_INFORMATION = struct__KEY_FLAGS_INFORMATION
PKEY_FLAGS_INFORMATION = ctypes.POINTER(struct__KEY_FLAGS_INFORMATION)
class struct__KEY_VIRTUALIZATION_INFORMATION(Structure):
    pass

struct__KEY_VIRTUALIZATION_INFORMATION._pack_ = 1 # source:False
struct__KEY_VIRTUALIZATION_INFORMATION._fields_ = [
    ('VirtualizationCandidate', ctypes.c_uint32, 1),
    ('VirtualizationEnabled', ctypes.c_uint32, 1),
    ('VirtualTarget', ctypes.c_uint32, 1),
    ('VirtualStore', ctypes.c_uint32, 1),
    ('VirtualSource', ctypes.c_uint32, 1),
    ('Reserved', ctypes.c_uint32, 27),
]

KEY_VIRTUALIZATION_INFORMATION = struct__KEY_VIRTUALIZATION_INFORMATION
PKEY_VIRTUALIZATION_INFORMATION = ctypes.POINTER(struct__KEY_VIRTUALIZATION_INFORMATION)
class struct__KEY_TRUST_INFORMATION(Structure):
    pass

struct__KEY_TRUST_INFORMATION._pack_ = 1 # source:False
struct__KEY_TRUST_INFORMATION._fields_ = [
    ('TrustedKey', ctypes.c_uint32, 1),
    ('Reserved', ctypes.c_uint32, 31),
]

KEY_TRUST_INFORMATION = struct__KEY_TRUST_INFORMATION
PKEY_TRUST_INFORMATION = ctypes.POINTER(struct__KEY_TRUST_INFORMATION)
class struct__KEY_LAYER_INFORMATION(Structure):
    pass

struct__KEY_LAYER_INFORMATION._pack_ = 1 # source:False
struct__KEY_LAYER_INFORMATION._fields_ = [
    ('IsTombstone', ctypes.c_uint32),
    ('IsSupersedeLocal', ctypes.c_uint32),
    ('IsSupersedeTree', ctypes.c_uint32),
    ('ClassIsInherited', ctypes.c_uint32),
    ('Reserved', ctypes.c_uint32),
]

KEY_LAYER_INFORMATION = struct__KEY_LAYER_INFORMATION
PKEY_LAYER_INFORMATION = ctypes.POINTER(struct__KEY_LAYER_INFORMATION)

# values for enumeration '_KEY_SET_INFORMATION_CLASS'
_KEY_SET_INFORMATION_CLASS__enumvalues = {
    0: 'KeyWriteTimeInformation',
    1: 'KeyWow64FlagsInformation',
    2: 'KeyControlFlagsInformation',
    3: 'KeySetVirtualizationInformation',
    4: 'KeySetDebugInformation',
    5: 'KeySetHandleTagsInformation',
    6: 'MaxKeySetInfoClass',
}
KeyWriteTimeInformation = 0
KeyWow64FlagsInformation = 1
KeyControlFlagsInformation = 2
KeySetVirtualizationInformation = 3
KeySetDebugInformation = 4
KeySetHandleTagsInformation = 5
MaxKeySetInfoClass = 6
_KEY_SET_INFORMATION_CLASS = ctypes.c_uint32 # enum
KEY_SET_INFORMATION_CLASS = _KEY_SET_INFORMATION_CLASS
KEY_SET_INFORMATION_CLASS__enumvalues = _KEY_SET_INFORMATION_CLASS__enumvalues
class struct__KEY_WRITE_TIME_INFORMATION(Structure):
    _pack_ = 1 # source:False
    _fields_ = [
    ('LastWriteTime', union__LARGE_INTEGER),
     ]

KEY_WRITE_TIME_INFORMATION = struct__KEY_WRITE_TIME_INFORMATION
PKEY_WRITE_TIME_INFORMATION = ctypes.POINTER(struct__KEY_WRITE_TIME_INFORMATION)
class struct__KEY_WOW64_FLAGS_INFORMATION(Structure):
    pass

struct__KEY_WOW64_FLAGS_INFORMATION._pack_ = 1 # source:False
struct__KEY_WOW64_FLAGS_INFORMATION._fields_ = [
    ('UserFlags', ctypes.c_uint32),
]

KEY_WOW64_FLAGS_INFORMATION = struct__KEY_WOW64_FLAGS_INFORMATION
PKEY_WOW64_FLAGS_INFORMATION = ctypes.POINTER(struct__KEY_WOW64_FLAGS_INFORMATION)
class struct__KEY_HANDLE_TAGS_INFORMATION(Structure):
    pass

struct__KEY_HANDLE_TAGS_INFORMATION._pack_ = 1 # source:False
struct__KEY_HANDLE_TAGS_INFORMATION._fields_ = [
    ('HandleTags', ctypes.c_uint32),
]

KEY_HANDLE_TAGS_INFORMATION = struct__KEY_HANDLE_TAGS_INFORMATION
PKEY_HANDLE_TAGS_INFORMATION = ctypes.POINTER(struct__KEY_HANDLE_TAGS_INFORMATION)
class struct__KEY_CONTROL_FLAGS_INFORMATION(Structure):
    pass

struct__KEY_CONTROL_FLAGS_INFORMATION._pack_ = 1 # source:False
struct__KEY_CONTROL_FLAGS_INFORMATION._fields_ = [
    ('ControlFlags', ctypes.c_uint32),
]

KEY_CONTROL_FLAGS_INFORMATION = struct__KEY_CONTROL_FLAGS_INFORMATION
PKEY_CONTROL_FLAGS_INFORMATION = ctypes.POINTER(struct__KEY_CONTROL_FLAGS_INFORMATION)
class struct__KEY_SET_VIRTUALIZATION_INFORMATION(Structure):
    pass

struct__KEY_SET_VIRTUALIZATION_INFORMATION._pack_ = 1 # source:False
struct__KEY_SET_VIRTUALIZATION_INFORMATION._fields_ = [
    ('VirtualTarget', ctypes.c_uint32, 1),
    ('VirtualStore', ctypes.c_uint32, 1),
    ('VirtualSource', ctypes.c_uint32, 1),
    ('Reserved', ctypes.c_uint32, 29),
]

KEY_SET_VIRTUALIZATION_INFORMATION = struct__KEY_SET_VIRTUALIZATION_INFORMATION
PKEY_SET_VIRTUALIZATION_INFORMATION = ctypes.POINTER(struct__KEY_SET_VIRTUALIZATION_INFORMATION)

# values for enumeration '_KEY_VALUE_INFORMATION_CLASS'
_KEY_VALUE_INFORMATION_CLASS__enumvalues = {
    0: 'KeyValueBasicInformation',
    1: 'KeyValueFullInformation',
    2: 'KeyValuePartialInformation',
    3: 'KeyValueFullInformationAlign64',
    4: 'KeyValuePartialInformationAlign64',
    5: 'KeyValueLayerInformation',
    6: 'MaxKeyValueInfoClass',
}
KeyValueBasicInformation = 0
KeyValueFullInformation = 1
KeyValuePartialInformation = 2
KeyValueFullInformationAlign64 = 3
KeyValuePartialInformationAlign64 = 4
KeyValueLayerInformation = 5
MaxKeyValueInfoClass = 6
_KEY_VALUE_INFORMATION_CLASS = ctypes.c_uint32 # enum
KEY_VALUE_INFORMATION_CLASS = _KEY_VALUE_INFORMATION_CLASS
KEY_VALUE_INFORMATION_CLASS__enumvalues = _KEY_VALUE_INFORMATION_CLASS__enumvalues
class struct__KEY_VALUE_BASIC_INFORMATION(Structure):
    pass

struct__KEY_VALUE_BASIC_INFORMATION._pack_ = 1 # source:False
struct__KEY_VALUE_BASIC_INFORMATION._fields_ = [
    ('TitleIndex', ctypes.c_uint32),
    ('Type', ctypes.c_uint32),
    ('NameLength', ctypes.c_uint32),
    ('Name', ctypes.c_uint16 * 1),
    ('PADDING_0', ctypes.c_ubyte * 2),
]

KEY_VALUE_BASIC_INFORMATION = struct__KEY_VALUE_BASIC_INFORMATION
PKEY_VALUE_BASIC_INFORMATION = ctypes.POINTER(struct__KEY_VALUE_BASIC_INFORMATION)
class struct__KEY_VALUE_FULL_INFORMATION(Structure):
    pass

struct__KEY_VALUE_FULL_INFORMATION._pack_ = 1 # source:False
struct__KEY_VALUE_FULL_INFORMATION._fields_ = [
    ('TitleIndex', ctypes.c_uint32),
    ('Type', ctypes.c_uint32),
    ('DataOffset', ctypes.c_uint32),
    ('DataLength', ctypes.c_uint32),
    ('NameLength', ctypes.c_uint32),
    ('Name', ctypes.c_uint16 * 1),
    ('PADDING_0', ctypes.c_ubyte * 2),
]

KEY_VALUE_FULL_INFORMATION = struct__KEY_VALUE_FULL_INFORMATION
PKEY_VALUE_FULL_INFORMATION = ctypes.POINTER(struct__KEY_VALUE_FULL_INFORMATION)
class struct__KEY_VALUE_PARTIAL_INFORMATION(Structure):
    pass

struct__KEY_VALUE_PARTIAL_INFORMATION._pack_ = 1 # source:False
struct__KEY_VALUE_PARTIAL_INFORMATION._fields_ = [
    ('TitleIndex', ctypes.c_uint32),
    ('Type', ctypes.c_uint32),
    ('DataLength', ctypes.c_uint32),
    ('Data', ctypes.c_ubyte * 1),
    ('PADDING_0', ctypes.c_ubyte * 3),
]

KEY_VALUE_PARTIAL_INFORMATION = struct__KEY_VALUE_PARTIAL_INFORMATION
PKEY_VALUE_PARTIAL_INFORMATION = ctypes.POINTER(struct__KEY_VALUE_PARTIAL_INFORMATION)
class struct__KEY_VALUE_PARTIAL_INFORMATION_ALIGN64(Structure):
    pass

struct__KEY_VALUE_PARTIAL_INFORMATION_ALIGN64._pack_ = 1 # source:False
struct__KEY_VALUE_PARTIAL_INFORMATION_ALIGN64._fields_ = [
    ('Type', ctypes.c_uint32),
    ('DataLength', ctypes.c_uint32),
    ('Data', ctypes.c_ubyte * 1),
    ('PADDING_0', ctypes.c_ubyte * 3),
]

KEY_VALUE_PARTIAL_INFORMATION_ALIGN64 = struct__KEY_VALUE_PARTIAL_INFORMATION_ALIGN64
PKEY_VALUE_PARTIAL_INFORMATION_ALIGN64 = ctypes.POINTER(struct__KEY_VALUE_PARTIAL_INFORMATION_ALIGN64)
class struct__KEY_VALUE_LAYER_INFORMATION(Structure):
    pass

struct__KEY_VALUE_LAYER_INFORMATION._pack_ = 1 # source:False
struct__KEY_VALUE_LAYER_INFORMATION._fields_ = [
    ('IsTombstone', ctypes.c_uint32),
    ('Reserved', ctypes.c_uint32),
]

KEY_VALUE_LAYER_INFORMATION = struct__KEY_VALUE_LAYER_INFORMATION
PKEY_VALUE_LAYER_INFORMATION = ctypes.POINTER(struct__KEY_VALUE_LAYER_INFORMATION)
class struct__KEY_VALUE_ENTRY(Structure):
    pass

struct__KEY_VALUE_ENTRY._pack_ = 1 # source:False
struct__KEY_VALUE_ENTRY._fields_ = [
    ('ValueName', ctypes.POINTER(struct__UNICODE_STRING)),
    ('DataLength', ctypes.c_uint32),
    ('DataOffset', ctypes.c_uint32),
    ('Type', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

KEY_VALUE_ENTRY = struct__KEY_VALUE_ENTRY
PKEY_VALUE_ENTRY = ctypes.POINTER(struct__KEY_VALUE_ENTRY)

# values for enumeration '_REG_ACTION'
_REG_ACTION__enumvalues = {
    0: 'KeyAdded',
    1: 'KeyRemoved',
    2: 'KeyModified',
}
KeyAdded = 0
KeyRemoved = 1
KeyModified = 2
_REG_ACTION = ctypes.c_uint32 # enum
REG_ACTION = _REG_ACTION
REG_ACTION__enumvalues = _REG_ACTION__enumvalues
class struct__REG_NOTIFY_INFORMATION(Structure):
    pass

struct__REG_NOTIFY_INFORMATION._pack_ = 1 # source:False
struct__REG_NOTIFY_INFORMATION._fields_ = [
    ('NextEntryOffset', ctypes.c_uint32),
    ('Action', REG_ACTION),
    ('KeyLength', ctypes.c_uint32),
    ('Key', ctypes.c_uint16 * 1),
    ('PADDING_0', ctypes.c_ubyte * 2),
]

REG_NOTIFY_INFORMATION = struct__REG_NOTIFY_INFORMATION
PREG_NOTIFY_INFORMATION = ctypes.POINTER(struct__REG_NOTIFY_INFORMATION)
class struct__KEY_PID_ARRAY(Structure):
    pass

struct__KEY_PID_ARRAY._pack_ = 1 # source:False
struct__KEY_PID_ARRAY._fields_ = [
    ('PID', ctypes.POINTER(None)),
    ('KeyName', UNICODE_STRING),
]

KEY_PID_ARRAY = struct__KEY_PID_ARRAY
PKEY_PID_ARRAY = ctypes.POINTER(struct__KEY_PID_ARRAY)
class struct__KEY_OPEN_SUBKEYS_INFORMATION(Structure):
    pass

struct__KEY_OPEN_SUBKEYS_INFORMATION._pack_ = 1 # source:False
struct__KEY_OPEN_SUBKEYS_INFORMATION._fields_ = [
    ('Count', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('KeyArray', struct__KEY_PID_ARRAY * 1),
]

KEY_OPEN_SUBKEYS_INFORMATION = struct__KEY_OPEN_SUBKEYS_INFORMATION
PKEY_OPEN_SUBKEYS_INFORMATION = ctypes.POINTER(struct__KEY_OPEN_SUBKEYS_INFORMATION)

# values for enumeration '_SYSDBG_COMMAND'
_SYSDBG_COMMAND__enumvalues = {
    0: 'SysDbgQueryModuleInformation',
    1: 'SysDbgQueryTraceInformation',
    2: 'SysDbgSetTracepoint',
    3: 'SysDbgSetSpecialCall',
    4: 'SysDbgClearSpecialCalls',
    5: 'SysDbgQuerySpecialCalls',
    6: 'SysDbgBreakPoint',
    7: 'SysDbgQueryVersion',
    8: 'SysDbgReadVirtual',
    9: 'SysDbgWriteVirtual',
    10: 'SysDbgReadPhysical',
    11: 'SysDbgWritePhysical',
    12: 'SysDbgReadControlSpace',
    13: 'SysDbgWriteControlSpace',
    14: 'SysDbgReadIoSpace',
    15: 'SysDbgWriteIoSpace',
    16: 'SysDbgReadMsr',
    17: 'SysDbgWriteMsr',
    18: 'SysDbgReadBusData',
    19: 'SysDbgWriteBusData',
    20: 'SysDbgCheckLowMemory',
    21: 'SysDbgEnableKernelDebugger',
    22: 'SysDbgDisableKernelDebugger',
    23: 'SysDbgGetAutoKdEnable',
    24: 'SysDbgSetAutoKdEnable',
    25: 'SysDbgGetPrintBufferSize',
    26: 'SysDbgSetPrintBufferSize',
    27: 'SysDbgGetKdUmExceptionEnable',
    28: 'SysDbgSetKdUmExceptionEnable',
    29: 'SysDbgGetTriageDump',
    30: 'SysDbgGetKdBlockEnable',
    31: 'SysDbgSetKdBlockEnable',
    32: 'SysDbgRegisterForUmBreakInfo',
    33: 'SysDbgGetUmBreakPid',
    34: 'SysDbgClearUmBreakPid',
    35: 'SysDbgGetUmAttachPid',
    36: 'SysDbgClearUmAttachPid',
    37: 'SysDbgGetLiveKernelDump',
}
SysDbgQueryModuleInformation = 0
SysDbgQueryTraceInformation = 1
SysDbgSetTracepoint = 2
SysDbgSetSpecialCall = 3
SysDbgClearSpecialCalls = 4
SysDbgQuerySpecialCalls = 5
SysDbgBreakPoint = 6
SysDbgQueryVersion = 7
SysDbgReadVirtual = 8
SysDbgWriteVirtual = 9
SysDbgReadPhysical = 10
SysDbgWritePhysical = 11
SysDbgReadControlSpace = 12
SysDbgWriteControlSpace = 13
SysDbgReadIoSpace = 14
SysDbgWriteIoSpace = 15
SysDbgReadMsr = 16
SysDbgWriteMsr = 17
SysDbgReadBusData = 18
SysDbgWriteBusData = 19
SysDbgCheckLowMemory = 20
SysDbgEnableKernelDebugger = 21
SysDbgDisableKernelDebugger = 22
SysDbgGetAutoKdEnable = 23
SysDbgSetAutoKdEnable = 24
SysDbgGetPrintBufferSize = 25
SysDbgSetPrintBufferSize = 26
SysDbgGetKdUmExceptionEnable = 27
SysDbgSetKdUmExceptionEnable = 28
SysDbgGetTriageDump = 29
SysDbgGetKdBlockEnable = 30
SysDbgSetKdBlockEnable = 31
SysDbgRegisterForUmBreakInfo = 32
SysDbgGetUmBreakPid = 33
SysDbgClearUmBreakPid = 34
SysDbgGetUmAttachPid = 35
SysDbgClearUmAttachPid = 36
SysDbgGetLiveKernelDump = 37
_SYSDBG_COMMAND = ctypes.c_uint32 # enum
SYSDBG_COMMAND = _SYSDBG_COMMAND
SYSDBG_COMMAND__enumvalues = _SYSDBG_COMMAND__enumvalues
PSYSDBG_COMMAND = ctypes.POINTER(_SYSDBG_COMMAND)

# values for enumeration '_DEBUGOBJECTINFOCLASS'
_DEBUGOBJECTINFOCLASS__enumvalues = {
    1: 'DebugObjectFlags',
    2: 'MaxDebugObjectInfoClass',
}
DebugObjectFlags = 1
MaxDebugObjectInfoClass = 2
_DEBUGOBJECTINFOCLASS = ctypes.c_uint32 # enum
DEBUGOBJECTINFOCLASS = _DEBUGOBJECTINFOCLASS
DEBUGOBJECTINFOCLASS__enumvalues = _DEBUGOBJECTINFOCLASS__enumvalues
PDEBUGOBJECTINFOCLASS = ctypes.POINTER(_DEBUGOBJECTINFOCLASS)

# values for enumeration '_FILE_INFORMATION_CLASS'
_FILE_INFORMATION_CLASS__enumvalues = {
    1: 'FileDirectoryInformation',
    2: 'FileFullDirectoryInformation',
    3: 'FileBothDirectoryInformation',
    4: 'FileBasicInformation',
    5: 'FileStandardInformation',
    6: 'FileInternalInformation',
    7: 'FileEaInformation',
    8: 'FileAccessInformation',
    9: 'FileNameInformation',
    10: 'FileRenameInformation',
    11: 'FileLinkInformation',
    12: 'FileNamesInformation',
    13: 'FileDispositionInformation',
    14: 'FilePositionInformation',
    15: 'FileFullEaInformation',
    16: 'FileModeInformation',
    17: 'FileAlignmentInformation',
    18: 'FileAllInformation',
    19: 'FileAllocationInformation',
    20: 'FileEndOfFileInformation',
    21: 'FileAlternateNameInformation',
    22: 'FileStreamInformation',
    23: 'FilePipeInformation',
    24: 'FilePipeLocalInformation',
    25: 'FilePipeRemoteInformation',
    26: 'FileMailslotQueryInformation',
    27: 'FileMailslotSetInformation',
    28: 'FileCompressionInformation',
    29: 'FileObjectIdInformation',
    30: 'FileCompletionInformation',
    31: 'FileMoveClusterInformation',
    32: 'FileQuotaInformation',
    33: 'FileReparsePointInformation',
    34: 'FileNetworkOpenInformation',
    35: 'FileAttributeTagInformation',
    36: 'FileTrackingInformation',
    37: 'FileIdBothDirectoryInformation',
    38: 'FileIdFullDirectoryInformation',
    39: 'FileValidDataLengthInformation',
    40: 'FileShortNameInformation',
    41: 'FileIoCompletionNotificationInformation',
    42: 'FileIoStatusBlockRangeInformation',
    43: 'FileIoPriorityHintInformation',
    44: 'FileSfioReserveInformation',
    45: 'FileSfioVolumeInformation',
    46: 'FileHardLinkInformation',
    47: 'FileProcessIdsUsingFileInformation',
    48: 'FileNormalizedNameInformation',
    49: 'FileNetworkPhysicalNameInformation',
    50: 'FileIdGlobalTxDirectoryInformation',
    51: 'FileIsRemoteDeviceInformation',
    52: 'FileUnusedInformation',
    53: 'FileNumaNodeInformation',
    54: 'FileStandardLinkInformation',
    55: 'FileRemoteProtocolInformation',
    56: 'FileRenameInformationBypassAccessCheck',
    57: 'FileLinkInformationBypassAccessCheck',
    58: 'FileVolumeNameInformation',
    59: 'FileIdInformation',
    60: 'FileIdExtdDirectoryInformation',
    61: 'FileReplaceCompletionInformation',
    62: 'FileHardLinkFullIdInformation',
    63: 'FileIdExtdBothDirectoryInformation',
    64: 'FileDispositionInformationEx',
    65: 'FileRenameInformationEx',
    66: 'FileRenameInformationExBypassAccessCheck',
    67: 'FileDesiredStorageClassInformation',
    68: 'FileStatInformation',
    69: 'FileMaximumInformation',
}
FileDirectoryInformation = 1
FileFullDirectoryInformation = 2
FileBothDirectoryInformation = 3
FileBasicInformation = 4
FileStandardInformation = 5
FileInternalInformation = 6
FileEaInformation = 7
FileAccessInformation = 8
FileNameInformation = 9
FileRenameInformation = 10
FileLinkInformation = 11
FileNamesInformation = 12
FileDispositionInformation = 13
FilePositionInformation = 14
FileFullEaInformation = 15
FileModeInformation = 16
FileAlignmentInformation = 17
FileAllInformation = 18
FileAllocationInformation = 19
FileEndOfFileInformation = 20
FileAlternateNameInformation = 21
FileStreamInformation = 22
FilePipeInformation = 23
FilePipeLocalInformation = 24
FilePipeRemoteInformation = 25
FileMailslotQueryInformation = 26
FileMailslotSetInformation = 27
FileCompressionInformation = 28
FileObjectIdInformation = 29
FileCompletionInformation = 30
FileMoveClusterInformation = 31
FileQuotaInformation = 32
FileReparsePointInformation = 33
FileNetworkOpenInformation = 34
FileAttributeTagInformation = 35
FileTrackingInformation = 36
FileIdBothDirectoryInformation = 37
FileIdFullDirectoryInformation = 38
FileValidDataLengthInformation = 39
FileShortNameInformation = 40
FileIoCompletionNotificationInformation = 41
FileIoStatusBlockRangeInformation = 42
FileIoPriorityHintInformation = 43
FileSfioReserveInformation = 44
FileSfioVolumeInformation = 45
FileHardLinkInformation = 46
FileProcessIdsUsingFileInformation = 47
FileNormalizedNameInformation = 48
FileNetworkPhysicalNameInformation = 49
FileIdGlobalTxDirectoryInformation = 50
FileIsRemoteDeviceInformation = 51
FileUnusedInformation = 52
FileNumaNodeInformation = 53
FileStandardLinkInformation = 54
FileRemoteProtocolInformation = 55
FileRenameInformationBypassAccessCheck = 56
FileLinkInformationBypassAccessCheck = 57
FileVolumeNameInformation = 58
FileIdInformation = 59
FileIdExtdDirectoryInformation = 60
FileReplaceCompletionInformation = 61
FileHardLinkFullIdInformation = 62
FileIdExtdBothDirectoryInformation = 63
FileDispositionInformationEx = 64
FileRenameInformationEx = 65
FileRenameInformationExBypassAccessCheck = 66
FileDesiredStorageClassInformation = 67
FileStatInformation = 68
FileMaximumInformation = 69
_FILE_INFORMATION_CLASS = ctypes.c_uint32 # enum
FILE_INFORMATION_CLASS = _FILE_INFORMATION_CLASS
FILE_INFORMATION_CLASS__enumvalues = _FILE_INFORMATION_CLASS__enumvalues
PFILE_INFORMATION_CLASS = ctypes.POINTER(_FILE_INFORMATION_CLASS)
class struct__SYSTEM_BASIC_INFORMATION(Structure):
    pass

struct__SYSTEM_BASIC_INFORMATION._pack_ = 1 # source:False
struct__SYSTEM_BASIC_INFORMATION._fields_ = [
    ('Reserved', ctypes.c_uint32),
    ('TimerResolution', ctypes.c_uint32),
    ('PageSize', ctypes.c_uint32),
    ('NumberOfPhysicalPages', ctypes.c_uint32),
    ('LowestPhysicalPageNumber', ctypes.c_uint32),
    ('HighestPhysicalPageNumber', ctypes.c_uint32),
    ('AllocationGranularity', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('MinimumUserModeAddress', ctypes.c_uint64),
    ('MaximumUserModeAddress', ctypes.c_uint64),
    ('ActiveProcessorsAffinityMask', ctypes.c_uint64),
    ('NumberOfProcessors', ctypes.c_char),
    ('PADDING_1', ctypes.c_ubyte * 7),
]

SYSTEM_BASIC_INFORMATION = struct__SYSTEM_BASIC_INFORMATION
PSYSTEM_BASIC_INFORMATION = ctypes.POINTER(struct__SYSTEM_BASIC_INFORMATION)
class struct__FILE_PIPE_PEEK_BUFFER(Structure):
    pass

struct__FILE_PIPE_PEEK_BUFFER._pack_ = 1 # source:False
struct__FILE_PIPE_PEEK_BUFFER._fields_ = [
    ('NamedPipeState', ctypes.c_uint32),
    ('ReadDataAvailable', ctypes.c_uint32),
    ('NumberOfMessages', ctypes.c_uint32),
    ('MessageLength', ctypes.c_uint32),
    ('Data', ctypes.c_char * 1),
    ('PADDING_0', ctypes.c_ubyte * 3),
]

FILE_PIPE_PEEK_BUFFER = struct__FILE_PIPE_PEEK_BUFFER
PFILE_PIPE_PEEK_BUFFER = ctypes.POINTER(struct__FILE_PIPE_PEEK_BUFFER)
class struct__NAMED_PIPE_CREATE_PARAMETERS(Structure):
    pass

struct__NAMED_PIPE_CREATE_PARAMETERS._pack_ = 1 # source:False
struct__NAMED_PIPE_CREATE_PARAMETERS._fields_ = [
    ('NamedPipeType', ctypes.c_uint32),
    ('ReadMode', ctypes.c_uint32),
    ('CompletionMode', ctypes.c_uint32),
    ('MaximumInstances', ctypes.c_uint32),
    ('InboundQuota', ctypes.c_uint32),
    ('OutboundQuota', ctypes.c_uint32),
    ('DefaultTimeout', union__LARGE_INTEGER),
    ('TimeoutSpecified', ctypes.c_ubyte),
    ('PADDING_0', ctypes.c_ubyte * 7),
]

NAMED_PIPE_CREATE_PARAMETERS = struct__NAMED_PIPE_CREATE_PARAMETERS
PNAMED_PIPE_CREATE_PARAMETERS = ctypes.POINTER(struct__NAMED_PIPE_CREATE_PARAMETERS)
class struct__FILE_NETWORK_OPEN_INFORMATION(Structure):
    pass

struct__FILE_NETWORK_OPEN_INFORMATION._pack_ = 1 # source:False
struct__FILE_NETWORK_OPEN_INFORMATION._fields_ = [
    ('CreationTime', union__LARGE_INTEGER),
    ('LastAccessTime', union__LARGE_INTEGER),
    ('LastWriteTime', union__LARGE_INTEGER),
    ('ChangeTime', union__LARGE_INTEGER),
    ('AllocationSize', union__LARGE_INTEGER),
    ('EndOfFile', union__LARGE_INTEGER),
    ('FileAttributes', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

FILE_NETWORK_OPEN_INFORMATION = struct__FILE_NETWORK_OPEN_INFORMATION
PFILE_NETWORK_OPEN_INFORMATION = ctypes.POINTER(struct__FILE_NETWORK_OPEN_INFORMATION)
class struct__SYSTEM_TIMEOFDAY_INFORMATION(Structure):
    pass

struct__SYSTEM_TIMEOFDAY_INFORMATION._pack_ = 1 # source:False
struct__SYSTEM_TIMEOFDAY_INFORMATION._fields_ = [
    ('BootTime', union__LARGE_INTEGER),
    ('CurrentTime', union__LARGE_INTEGER),
    ('TimeZoneBias', union__LARGE_INTEGER),
    ('TimeZoneId', ctypes.c_uint32),
    ('Reserved', ctypes.c_uint32),
    ('BootTimeBias', ctypes.c_uint64),
    ('SleepTimeBias', ctypes.c_uint64),
]

SYSTEM_TIMEOFDAY_INFORMATION = struct__SYSTEM_TIMEOFDAY_INFORMATION
PSYSTEM_TIMEOFDAY_INFORMATION = ctypes.POINTER(struct__SYSTEM_TIMEOFDAY_INFORMATION)
class struct__SYSTEM_CONSOLE_INFORMATION(Structure):
    pass

struct__SYSTEM_CONSOLE_INFORMATION._pack_ = 1 # source:False
struct__SYSTEM_CONSOLE_INFORMATION._fields_ = [
    ('DriverLoaded', ctypes.c_uint32, 1),
    ('Spare', ctypes.c_uint32, 31),
]

SYSTEM_CONSOLE_INFORMATION = struct__SYSTEM_CONSOLE_INFORMATION
PSYSTEM_CONSOLE_INFORMATION = ctypes.POINTER(struct__SYSTEM_CONSOLE_INFORMATION)
class struct__KSYSTEM_TIME(Structure):
    pass

struct__KSYSTEM_TIME._pack_ = 1 # source:False
struct__KSYSTEM_TIME._fields_ = [
    ('LowPart', ctypes.c_uint32),
    ('High1Time', ctypes.c_int32),
    ('High2Time', ctypes.c_int32),
]

KSYSTEM_TIME = struct__KSYSTEM_TIME
PKSYSTEM_TIME = ctypes.POINTER(struct__KSYSTEM_TIME)
class struct__PROCESS_ACCESS_TOKEN(Structure):
    pass

struct__PROCESS_ACCESS_TOKEN._pack_ = 1 # source:False
struct__PROCESS_ACCESS_TOKEN._fields_ = [
    ('Token', ctypes.POINTER(None)),
    ('Thread', ctypes.POINTER(None)),
]

PROCESS_ACCESS_TOKEN = struct__PROCESS_ACCESS_TOKEN
PPROCESS_ACCESS_TOKEN = ctypes.POINTER(struct__PROCESS_ACCESS_TOKEN)
PS_PROTECTED_TYPE = ctypes.c_ubyte
PS_PROTECTED_SIGNER = ctypes.c_ubyte
class struct__PS_PROTECTION(Structure):
    pass

class union_union_42(Union):
    pass

class struct_struct_43(Structure):
    pass

struct_struct_43._pack_ = 1 # source:False
struct_struct_43._fields_ = [
    ('Type', ctypes.c_ubyte, 3),
    ('Audit', ctypes.c_ubyte, 1),
    ('Signer', ctypes.c_ubyte, 4),
]

union_union_42._pack_ = 1 # source:False
union_union_42._fields_ = [
    ('s', struct_struct_43),
    ('Level', ctypes.c_ubyte),
]

struct__PS_PROTECTION._pack_ = 1 # source:False
struct__PS_PROTECTION._anonymous_ = ('_0',)
struct__PS_PROTECTION._fields_ = [
    ('_0', union_union_42),
]

PS_PROTECTION = struct__PS_PROTECTION
PPS_PROTECTION = ctypes.POINTER(struct__PS_PROTECTION)
class struct__RTL_BUFFER(Structure):
    pass

struct__RTL_BUFFER._pack_ = 1 # source:False
struct__RTL_BUFFER._fields_ = [
    ('Buffer', ctypes.POINTER(ctypes.c_ubyte)),
    ('StaticBuffer', ctypes.POINTER(ctypes.c_ubyte)),
    ('Size', ctypes.c_uint64),
    ('StaticSize', ctypes.c_uint64),
    ('ReservedForAllocatedSize', ctypes.c_uint64),
    ('ReservedForIMalloc', ctypes.POINTER(None)),
]

RTL_BUFFER = struct__RTL_BUFFER
PRTL_BUFFER = ctypes.POINTER(struct__RTL_BUFFER)
class struct__RTL_UNICODE_STRING_BUFFER(Structure):
    pass

struct__RTL_UNICODE_STRING_BUFFER._pack_ = 1 # source:False
struct__RTL_UNICODE_STRING_BUFFER._fields_ = [
    ('String', UNICODE_STRING),
    ('ByteBuffer', RTL_BUFFER),
    ('MinimumStaticBufferForTerminalNul', ctypes.c_ubyte * 2),
    ('PADDING_0', ctypes.c_ubyte * 6),
]

RTL_UNICODE_STRING_BUFFER = struct__RTL_UNICODE_STRING_BUFFER
PRTL_UNICODE_STRING_BUFFER = ctypes.POINTER(struct__RTL_UNICODE_STRING_BUFFER)
class struct__RTL_USER_PROCESS_PARAMETERS(Structure):
    pass

struct__RTL_USER_PROCESS_PARAMETERS._pack_ = 1 # source:False
struct__RTL_USER_PROCESS_PARAMETERS._fields_ = [
    ('MaximumLength', ctypes.c_uint32),
    ('Length', ctypes.c_uint32),
    ('Flags', ctypes.c_uint32),
    ('DebugFlags', ctypes.c_uint32),
    ('ConsoleHandle', ctypes.POINTER(None)),
    ('ConsoleFlags', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('StandardInput', ctypes.POINTER(None)),
    ('StandardOutput', ctypes.POINTER(None)),
    ('StandardError', ctypes.POINTER(None)),
    ('CurrentDirectory', CURDIR),
    ('DllPath', UNICODE_STRING),
    ('ImagePathName', UNICODE_STRING),
    ('CommandLine', UNICODE_STRING),
    ('Environment', ctypes.POINTER(ctypes.c_uint16)),
    ('StartingX', ctypes.c_uint32),
    ('StartingY', ctypes.c_uint32),
    ('CountX', ctypes.c_uint32),
    ('CountY', ctypes.c_uint32),
    ('CountCharsX', ctypes.c_uint32),
    ('CountCharsY', ctypes.c_uint32),
    ('FillAttribute', ctypes.c_uint32),
    ('WindowFlags', ctypes.c_uint32),
    ('ShowWindowFlags', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('WindowTitle', UNICODE_STRING),
    ('DesktopInfo', UNICODE_STRING),
    ('ShellInfo', UNICODE_STRING),
    ('RuntimeData', UNICODE_STRING),
    ('CurrentDirectories', struct__RTL_DRIVE_LETTER_CURDIR * 32),
    ('EnvironmentSize', ctypes.c_uint64),
    ('EnvironmentVersion', ctypes.c_uint64),
    ('PackageDependencyData', ctypes.POINTER(None)),
    ('ProcessGroupId', ctypes.c_uint32),
    ('LoaderThreads', ctypes.c_uint32),
]

RTL_USER_PROCESS_PARAMETERS = struct__RTL_USER_PROCESS_PARAMETERS
PRTL_USER_PROCESS_PARAMETERS = ctypes.POINTER(struct__RTL_USER_PROCESS_PARAMETERS)
class struct__RTL_USER_PROCESS_INFORMATION(Structure):
    pass

struct__RTL_USER_PROCESS_INFORMATION._pack_ = 1 # source:False
struct__RTL_USER_PROCESS_INFORMATION._fields_ = [
    ('Length', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('Process', ctypes.POINTER(None)),
    ('Thread', ctypes.POINTER(None)),
    ('ClientId', CLIENT_ID),
    ('ImageInformation', SECTION_IMAGE_INFORMATION),
]

RTL_USER_PROCESS_INFORMATION = struct__RTL_USER_PROCESS_INFORMATION
PRTL_USER_PROCESS_INFORMATION = ctypes.POINTER(struct__RTL_USER_PROCESS_INFORMATION)
GDI_HANDLE_BUFFER32 = ctypes.c_uint32 * 34
GDI_HANDLE_BUFFER64 = ctypes.c_uint32 * 60
GDI_HANDLE_BUFFER = ctypes.c_uint32 * 60
class struct__PEB_LDR_DATA(Structure):
    pass

struct__PEB_LDR_DATA._pack_ = 1 # source:False
struct__PEB_LDR_DATA._fields_ = [
    ('Length', ctypes.c_uint32),
    ('Initialized', ctypes.c_ubyte),
    ('PADDING_0', ctypes.c_ubyte * 3),
    ('SsHandle', ctypes.POINTER(None)),
    ('InLoadOrderModuleList', struct__LIST_ENTRY),
    ('InMemoryOrderModuleList', struct__LIST_ENTRY),
    ('InInitializationOrderModuleList', struct__LIST_ENTRY),
    ('EntryInProgress', ctypes.POINTER(None)),
    ('ShutdownInProgress', ctypes.c_ubyte),
    ('PADDING_1', ctypes.c_ubyte * 7),
    ('ShutdownThreadId', ctypes.POINTER(None)),
]

PEB_LDR_DATA = struct__PEB_LDR_DATA
PPEB_LDR_DATA = ctypes.POINTER(struct__PEB_LDR_DATA)
class struct__ACTIVATION_CONTEXT_STACK(Structure):
    pass

class struct__RTL_ACTIVATION_CONTEXT_STACK_FRAME(Structure):
    pass

struct__ACTIVATION_CONTEXT_STACK._pack_ = 1 # source:False
struct__ACTIVATION_CONTEXT_STACK._fields_ = [
    ('ActiveFrame', ctypes.POINTER(struct__RTL_ACTIVATION_CONTEXT_STACK_FRAME)),
    ('FrameListCache', struct__LIST_ENTRY),
    ('Flags', ctypes.c_uint32),
    ('NextCookieSequenceNumber', ctypes.c_uint32),
    ('StackId', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

ACTIVATION_CONTEXT_STACK = struct__ACTIVATION_CONTEXT_STACK
PACTIVATION_CONTEXT_STACK = ctypes.POINTER(struct__ACTIVATION_CONTEXT_STACK)
class struct__PEB(Structure):
    pass

class struct__RTL_CRITICAL_SECTION(Structure):
    pass

class union__ULARGE_INTEGER(Union):
    pass

class struct_struct_44(Structure):
    pass

struct_struct_44._pack_ = 1 # source:False
struct_struct_44._fields_ = [
    ('LowPart', ctypes.c_uint32),
    ('HighPart', ctypes.c_uint32),
]

class struct_struct_45(Structure):
    pass

struct_struct_45._pack_ = 1 # source:False
struct_struct_45._fields_ = [
    ('LowPart', ctypes.c_uint32),
    ('HighPart', ctypes.c_uint32),
]

union__ULARGE_INTEGER._pack_ = 1 # source:False
union__ULARGE_INTEGER._anonymous_ = ('_0',)
union__ULARGE_INTEGER._fields_ = [
    ('_0', struct_struct_44),
    ('u', struct_struct_45),
    ('QuadPart', ctypes.c_uint64),
]

class union_union_46(Union):
    pass

union_union_46._pack_ = 1 # source:False
union_union_46._fields_ = [
    ('KernelCallbackTable', ctypes.POINTER(None)),
    ('UserSharedInfoPtr', ctypes.POINTER(None)),
]

class union_union_47(Union):
    pass

class struct_struct_48(Structure):
    pass

struct_struct_48._pack_ = 1 # source:False
struct_struct_48._fields_ = [
    ('ImageUsesLargePages', ctypes.c_ubyte, 1),
    ('IsProtectedProcess', ctypes.c_ubyte, 1),
    ('IsImageDynamicallyRelocated', ctypes.c_ubyte, 1),
    ('SkipPatchingUser32Forwarders', ctypes.c_ubyte, 1),
    ('IsPackagedProcess', ctypes.c_ubyte, 1),
    ('IsAppContainer', ctypes.c_ubyte, 1),
    ('IsProtectedProcessLight', ctypes.c_ubyte, 1),
    ('IsLongPathAwareProcess', ctypes.c_ubyte, 1),
]

union_union_47._pack_ = 1 # source:False
union_union_47._fields_ = [
    ('BitField', ctypes.c_ubyte),
    ('s1', struct_struct_48),
]

class union_union_49(Union):
    pass

class struct_struct_50(Structure):
    pass

struct_struct_50._pack_ = 1 # source:False
struct_struct_50._fields_ = [
    ('ProcessInJob', ctypes.c_uint32, 1),
    ('ProcessInitializing', ctypes.c_uint32, 1),
    ('ProcessUsingVEH', ctypes.c_uint32, 1),
    ('ProcessUsingVCH', ctypes.c_uint32, 1),
    ('ProcessUsingFTH', ctypes.c_uint32, 1),
    ('ProcessPreviouslyThrottled', ctypes.c_uint32, 1),
    ('ProcessCurrentlyThrottled', ctypes.c_uint32, 1),
    ('ReservedBits0', ctypes.c_uint32, 25),
]

union_union_49._pack_ = 1 # source:False
union_union_49._fields_ = [
    ('CrossProcessFlags', ctypes.c_uint32),
    ('s2', struct_struct_50),
]

class union_union_51(Union):
    pass

class struct_struct_52(Structure):
    pass

struct_struct_52._pack_ = 1 # source:False
struct_struct_52._fields_ = [
    ('HeapTracingEnabled', ctypes.c_uint32, 1),
    ('CritSecTracingEnabled', ctypes.c_uint32, 1),
    ('LibLoaderTracingEnabled', ctypes.c_uint32, 1),
    ('SpareTracingBits', ctypes.c_uint32, 29),
]

union_union_51._pack_ = 1 # source:False
union_union_51._fields_ = [
    ('TracingFlags', ctypes.c_uint32),
    ('s3', struct_struct_52),
]

struct__PEB._pack_ = 1 # source:False
struct__PEB._fields_ = [
    ('InheritedAddressSpace', ctypes.c_ubyte),
    ('ReadImageFileExecOptions', ctypes.c_ubyte),
    ('BeingDebugged', ctypes.c_ubyte),
    ('u1', union_union_47),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('Mutant', ctypes.POINTER(None)),
    ('ImageBaseAddress', ctypes.POINTER(None)),
    ('Ldr', ctypes.POINTER(struct__PEB_LDR_DATA)),
    ('ProcessParameters', ctypes.POINTER(struct__RTL_USER_PROCESS_PARAMETERS)),
    ('SubSystemData', ctypes.POINTER(None)),
    ('ProcessHeap', ctypes.POINTER(None)),
    ('FastPebLock', ctypes.POINTER(struct__RTL_CRITICAL_SECTION)),
    ('AtlThunkSListPtr', ctypes.POINTER(None)),
    ('IFEOKey', ctypes.POINTER(None)),
    ('u2', union_union_49),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('u3', union_union_46),
    ('SystemReserved', ctypes.c_uint32 * 1),
    ('AtlThunkSListPtr32', ctypes.c_uint32),
    ('ApiSetMap', ctypes.POINTER(None)),
    ('TlsExpansionCounter', ctypes.c_uint32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('TlsBitmap', ctypes.POINTER(None)),
    ('TlsBitmapBits', ctypes.c_uint32 * 2),
    ('ReadOnlySharedMemoryBase', ctypes.POINTER(None)),
    ('SharedData', ctypes.POINTER(None)),
    ('ReadOnlyStaticServerData', ctypes.POINTER(ctypes.POINTER(None))),
    ('AnsiCodePageData', ctypes.POINTER(None)),
    ('OemCodePageData', ctypes.POINTER(None)),
    ('UnicodeCaseTableData', ctypes.POINTER(None)),
    ('NumberOfProcessors', ctypes.c_uint32),
    ('NtGlobalFlag', ctypes.c_uint32),
    ('CriticalSectionTimeout', union__LARGE_INTEGER),
    ('HeapSegmentReserve', ctypes.c_uint64),
    ('HeapSegmentCommit', ctypes.c_uint64),
    ('HeapDeCommitTotalFreeThreshold', ctypes.c_uint64),
    ('HeapDeCommitFreeBlockThreshold', ctypes.c_uint64),
    ('NumberOfHeaps', ctypes.c_uint32),
    ('MaximumNumberOfHeaps', ctypes.c_uint32),
    ('ProcessHeaps', ctypes.POINTER(ctypes.POINTER(None))),
    ('GdiSharedHandleTable', ctypes.POINTER(None)),
    ('ProcessStarterHelper', ctypes.POINTER(None)),
    ('GdiDCAttributeList', ctypes.c_uint32),
    ('PADDING_3', ctypes.c_ubyte * 4),
    ('LoaderLock', ctypes.POINTER(struct__RTL_CRITICAL_SECTION)),
    ('OSMajorVersion', ctypes.c_uint32),
    ('OSMinorVersion', ctypes.c_uint32),
    ('OSBuildNumber', ctypes.c_uint16),
    ('OSCSDVersion', ctypes.c_uint16),
    ('OSPlatformId', ctypes.c_uint32),
    ('ImageSubsystem', ctypes.c_uint32),
    ('ImageSubsystemMajorVersion', ctypes.c_uint32),
    ('ImageSubsystemMinorVersion', ctypes.c_uint32),
    ('PADDING_4', ctypes.c_ubyte * 4),
    ('ActiveProcessAffinityMask', ctypes.c_uint64),
    ('GdiHandleBuffer', ctypes.c_uint32 * 60),
    ('PostProcessInitRoutine', ctypes.POINTER(None)),
    ('TlsExpansionBitmap', ctypes.POINTER(None)),
    ('TlsExpansionBitmapBits', ctypes.c_uint32 * 32),
    ('SessionId', ctypes.c_uint32),
    ('PADDING_5', ctypes.c_ubyte * 4),
    ('AppCompatFlags', union__ULARGE_INTEGER),
    ('AppCompatFlagsUser', union__ULARGE_INTEGER),
    ('pShimData', ctypes.POINTER(None)),
    ('AppCompatInfo', ctypes.POINTER(None)),
    ('CSDVersion', UNICODE_STRING),
    ('ActivationContextData', ctypes.POINTER(None)),
    ('ProcessAssemblyStorageMap', ctypes.POINTER(None)),
    ('SystemDefaultActivationContextData', ctypes.POINTER(None)),
    ('SystemAssemblyStorageMap', ctypes.POINTER(None)),
    ('MinimumStackCommit', ctypes.c_uint64),
    ('FlsCallback', ctypes.POINTER(ctypes.POINTER(None))),
    ('FlsListHead', struct__LIST_ENTRY),
    ('FlsBitmap', ctypes.POINTER(None)),
    ('FlsBitmapBits', ctypes.c_uint32 * 4),
    ('FlsHighIndex', ctypes.c_uint32),
    ('PADDING_6', ctypes.c_ubyte * 4),
    ('WerRegistrationData', ctypes.POINTER(None)),
    ('WerShipAssertPtr', ctypes.POINTER(None)),
    ('pUnused', ctypes.POINTER(None)),
    ('pImageHeaderHash', ctypes.POINTER(None)),
    ('u4', union_union_51),
    ('PADDING_7', ctypes.c_ubyte * 4),
    ('CsrServerReadOnlySharedMemoryBase', ctypes.c_uint64),
    ('TppWorkerpListLock', ctypes.POINTER(None)),
    ('TppWorkerpList', struct__LIST_ENTRY),
    ('WaitOnAddressHashTable', ctypes.POINTER(None) * 128),
    ('TelemetryCoverageHeader', ctypes.POINTER(None)),
    ('CloudFileFlags', ctypes.c_uint32),
    ('PADDING_8', ctypes.c_ubyte * 4),
]

class struct__RTL_CRITICAL_SECTION_DEBUG(Structure):
    pass

struct__RTL_CRITICAL_SECTION._pack_ = 1 # source:False
struct__RTL_CRITICAL_SECTION._fields_ = [
    ('DebugInfo', ctypes.POINTER(struct__RTL_CRITICAL_SECTION_DEBUG)),
    ('LockCount', ctypes.c_int32),
    ('RecursionCount', ctypes.c_int32),
    ('OwningThread', ctypes.POINTER(None)),
    ('LockSemaphore', ctypes.POINTER(None)),
    ('SpinCount', ctypes.c_uint64),
]

struct__RTL_CRITICAL_SECTION_DEBUG._pack_ = 1 # source:False
struct__RTL_CRITICAL_SECTION_DEBUG._fields_ = [
    ('Type', ctypes.c_uint16),
    ('CreatorBackTraceIndex', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('CriticalSection', ctypes.POINTER(struct__RTL_CRITICAL_SECTION)),
    ('ProcessLocksList', struct__LIST_ENTRY),
    ('EntryCount', ctypes.c_uint32),
    ('ContentionCount', ctypes.c_uint32),
    ('Flags', ctypes.c_uint32),
    ('CreatorBackTraceIndexHigh', ctypes.c_uint16),
    ('SpareWORD', ctypes.c_uint16),
]

PEB = struct__PEB
PPEB = ctypes.POINTER(struct__PEB)
class struct__GDI_TEB_BATCH(Structure):
    pass

struct__GDI_TEB_BATCH._pack_ = 1 # source:False
struct__GDI_TEB_BATCH._fields_ = [
    ('Offset', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('HDC', ctypes.c_uint64),
    ('Buffer', ctypes.c_uint32 * 310),
]

GDI_TEB_BATCH = struct__GDI_TEB_BATCH
PGDI_TEB_BATCH = ctypes.POINTER(struct__GDI_TEB_BATCH)
class struct__TEB_ACTIVE_FRAME_CONTEXT(Structure):
    pass

struct__TEB_ACTIVE_FRAME_CONTEXT._pack_ = 1 # source:False
struct__TEB_ACTIVE_FRAME_CONTEXT._fields_ = [
    ('Flags', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('FrameName', ctypes.POINTER(ctypes.c_char)),
]

TEB_ACTIVE_FRAME_CONTEXT = struct__TEB_ACTIVE_FRAME_CONTEXT
PTEB_ACTIVE_FRAME_CONTEXT = ctypes.POINTER(struct__TEB_ACTIVE_FRAME_CONTEXT)
class struct__TEB_ACTIVE_FRAME(Structure):
    pass

struct__TEB_ACTIVE_FRAME._pack_ = 1 # source:False
struct__TEB_ACTIVE_FRAME._fields_ = [
    ('Flags', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('Previous', ctypes.POINTER(struct__TEB_ACTIVE_FRAME)),
    ('Context', ctypes.POINTER(struct__TEB_ACTIVE_FRAME_CONTEXT)),
]

TEB_ACTIVE_FRAME = struct__TEB_ACTIVE_FRAME
PTEB_ACTIVE_FRAME = ctypes.POINTER(struct__TEB_ACTIVE_FRAME)
class struct__TEB(Structure):
    pass

class struct__GUID(Structure):
    pass

struct__GUID._pack_ = 1 # source:False
struct__GUID._fields_ = [
    ('Data1', ctypes.c_uint32),
    ('Data2', ctypes.c_uint16),
    ('Data3', ctypes.c_uint16),
    ('Data4', ctypes.c_ubyte * 8),
]

class union_union_53(Union):
    pass

class struct_struct_54(Structure):
    pass

struct_struct_54._pack_ = 1 # source:False
struct_struct_54._fields_ = [
    ('SafeThunkCall', ctypes.c_uint16, 1),
    ('InDebugPrint', ctypes.c_uint16, 1),
    ('HasFiberData', ctypes.c_uint16, 1),
    ('SkipThreadAttach', ctypes.c_uint16, 1),
    ('WerInShipAssertCode', ctypes.c_uint16, 1),
    ('RanProcessInit', ctypes.c_uint16, 1),
    ('ClonedThread', ctypes.c_uint16, 1),
    ('SuppressDebugMsg', ctypes.c_uint16, 1),
    ('DisableUserStackWalk', ctypes.c_uint16, 1),
    ('RtlExceptionAttached', ctypes.c_uint16, 1),
    ('InitialThread', ctypes.c_uint16, 1),
    ('SessionAware', ctypes.c_uint16, 1),
    ('LoadOwner', ctypes.c_uint16, 1),
    ('LoaderWorker', ctypes.c_uint16, 1),
    ('SkipLoaderInit', ctypes.c_uint16, 1),
    ('SpareSameTebBits', ctypes.c_uint16, 1),
]

union_union_53._pack_ = 1 # source:False
union_union_53._fields_ = [
    ('SameTebFlags', ctypes.c_uint16),
    ('s2', struct_struct_54),
]

class union_union_55(Union):
    pass

union_union_55._pack_ = 1 # source:False
union_union_55._fields_ = [
    ('CrossTebFlags', ctypes.c_uint16),
    ('SpareCrossTebBits', ctypes.c_uint16, 16),
]

class union_union_56(Union):
    pass

class struct__PROCESSOR_NUMBER(Structure):
    pass

struct__PROCESSOR_NUMBER._pack_ = 1 # source:False
struct__PROCESSOR_NUMBER._fields_ = [
    ('Group', ctypes.c_uint16),
    ('Number', ctypes.c_ubyte),
    ('Reserved', ctypes.c_ubyte),
]

class struct_struct_57(Structure):
    pass

struct_struct_57._pack_ = 1 # source:False
struct_struct_57._fields_ = [
    ('ReservedPad0', ctypes.c_ubyte),
    ('ReservedPad1', ctypes.c_ubyte),
    ('ReservedPad2', ctypes.c_ubyte),
    ('IdealProcessor', ctypes.c_ubyte),
]

union_union_56._pack_ = 1 # source:False
union_union_56._fields_ = [
    ('CurrentIdealProcessor', struct__PROCESSOR_NUMBER),
    ('IdealProcessorValue', ctypes.c_uint32),
    ('s1', struct_struct_57),
]

class struct__NT_TIB(Structure):
    pass

class struct__EXCEPTION_REGISTRATION_RECORD(Structure):
    pass

class union_union_58(Union):
    pass

union_union_58._pack_ = 1 # source:False
union_union_58._fields_ = [
    ('FiberData', ctypes.POINTER(None)),
    ('Version', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

struct__NT_TIB._pack_ = 1 # source:False
struct__NT_TIB._anonymous_ = ('_0',)
struct__NT_TIB._fields_ = [
    ('ExceptionList', ctypes.POINTER(struct__EXCEPTION_REGISTRATION_RECORD)),
    ('StackBase', ctypes.POINTER(None)),
    ('StackLimit', ctypes.POINTER(None)),
    ('SubSystemTib', ctypes.POINTER(None)),
    ('_0', union_union_58),
    ('ArbitraryUserPointer', ctypes.POINTER(None)),
    ('Self', ctypes.POINTER(struct__NT_TIB)),
]

struct__TEB._pack_ = 1 # source:False
struct__TEB._fields_ = [
    ('NtTib', struct__NT_TIB),
    ('EnvironmentPointer', ctypes.POINTER(None)),
    ('ClientId', CLIENT_ID),
    ('ActiveRpcHandle', ctypes.POINTER(None)),
    ('ThreadLocalStoragePointer', ctypes.POINTER(None)),
    ('ProcessEnvironmentBlock', ctypes.POINTER(struct__PEB)),
    ('LastErrorValue', ctypes.c_uint32),
    ('CountOfOwnedCriticalSections', ctypes.c_uint32),
    ('CsrClientThread', ctypes.POINTER(None)),
    ('Win32ThreadInfo', ctypes.POINTER(None)),
    ('User32Reserved', ctypes.c_uint32 * 26),
    ('UserReserved', ctypes.c_uint32 * 5),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('WOW32Reserved', ctypes.POINTER(None)),
    ('CurrentLocale', ctypes.c_uint32),
    ('FpSoftwareStatusRegister', ctypes.c_uint32),
    ('ReservedForDebuggerInstrumentation', ctypes.POINTER(None) * 16),
    ('SystemReserved1', ctypes.POINTER(None) * 30),
    ('PlaceholderCompatibilityMode', ctypes.c_char),
    ('PlaceholderReserved', ctypes.c_char * 11),
    ('ProxiedProcessId', ctypes.c_uint32),
    ('ActivationStack', ACTIVATION_CONTEXT_STACK),
    ('WorkingOnBehalfTicket', ctypes.c_ubyte * 8),
    ('ExceptionCode', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('ActivationContextStackPointer', ctypes.POINTER(struct__ACTIVATION_CONTEXT_STACK)),
    ('InstrumentationCallbackSp', ctypes.c_uint64),
    ('InstrumentationCallbackPreviousPc', ctypes.c_uint64),
    ('InstrumentationCallbackPreviousSp', ctypes.c_uint64),
    ('TxFsContext', ctypes.c_uint32),
    ('InstrumentationCallbackDisabled', ctypes.c_ubyte),
    ('PADDING_2', ctypes.c_ubyte * 3),
    ('GdiTebBatch', GDI_TEB_BATCH),
    ('RealClientId', CLIENT_ID),
    ('GdiCachedProcessHandle', ctypes.POINTER(None)),
    ('GdiClientPID', ctypes.c_uint32),
    ('GdiClientTID', ctypes.c_uint32),
    ('GdiThreadLocalInfo', ctypes.POINTER(None)),
    ('Win32ClientInfo', ctypes.c_uint64 * 62),
    ('glDispatchTable', ctypes.POINTER(None) * 233),
    ('glReserved1', ctypes.c_uint64 * 29),
    ('glReserved2', ctypes.POINTER(None)),
    ('glSectionInfo', ctypes.POINTER(None)),
    ('glSection', ctypes.POINTER(None)),
    ('glTable', ctypes.POINTER(None)),
    ('glCurrentRC', ctypes.POINTER(None)),
    ('glContext', ctypes.POINTER(None)),
    ('LastStatusValue', ctypes.c_int32),
    ('PADDING_3', ctypes.c_ubyte * 4),
    ('StaticUnicodeString', UNICODE_STRING),
    ('StaticUnicodeBuffer', ctypes.c_uint16 * 261),
    ('PADDING_4', ctypes.c_ubyte * 6),
    ('DeallocationStack', ctypes.POINTER(None)),
    ('TlsSlots', ctypes.POINTER(None) * 64),
    ('TlsLinks', struct__LIST_ENTRY),
    ('Vdm', ctypes.POINTER(None)),
    ('ReservedForNtRpc', ctypes.POINTER(None)),
    ('DbgSsReserved', ctypes.POINTER(None) * 2),
    ('HardErrorMode', ctypes.c_uint32),
    ('PADDING_5', ctypes.c_ubyte * 4),
    ('Instrumentation', ctypes.POINTER(None) * 11),
    ('ActivityId', struct__GUID),
    ('SubProcessTag', ctypes.POINTER(None)),
    ('PerflibData', ctypes.POINTER(None)),
    ('EtwTraceData', ctypes.POINTER(None)),
    ('WinSockData', ctypes.POINTER(None)),
    ('GdiBatchCount', ctypes.c_uint32),
    ('u1', union_union_56),
    ('GuaranteedStackBytes', ctypes.c_uint32),
    ('PADDING_6', ctypes.c_ubyte * 4),
    ('ReservedForPerf', ctypes.POINTER(None)),
    ('ReservedForOle', ctypes.POINTER(None)),
    ('WaitingOnLoaderLock', ctypes.c_uint32),
    ('PADDING_7', ctypes.c_ubyte * 4),
    ('SavedPriorityState', ctypes.POINTER(None)),
    ('ReservedForCodeCoverage', ctypes.c_uint64),
    ('ThreadPoolData', ctypes.POINTER(None)),
    ('TlsExpansionSlots', ctypes.POINTER(ctypes.POINTER(None))),
    ('DeallocationBStore', ctypes.POINTER(None)),
    ('BStoreLimit', ctypes.POINTER(None)),
    ('MuiGeneration', ctypes.c_uint32),
    ('IsImpersonating', ctypes.c_uint32),
    ('NlsCache', ctypes.POINTER(None)),
    ('pShimData', ctypes.POINTER(None)),
    ('HeapVirtualAffinity', ctypes.c_uint16),
    ('LowFragHeapDataSlot', ctypes.c_uint16),
    ('PADDING_8', ctypes.c_ubyte * 4),
    ('CurrentTransactionHandle', ctypes.POINTER(None)),
    ('ActiveFrame', ctypes.POINTER(struct__TEB_ACTIVE_FRAME)),
    ('FlsData', ctypes.POINTER(None)),
    ('PreferredLanguages', ctypes.POINTER(None)),
    ('UserPrefLanguages', ctypes.POINTER(None)),
    ('MergedPrefLanguages', ctypes.POINTER(None)),
    ('MuiImpersonation', ctypes.c_uint32),
    ('u2', union_union_55),
    ('u3', union_union_53),
    ('TxnScopeEnterCallback', ctypes.POINTER(None)),
    ('TxnScopeExitCallback', ctypes.POINTER(None)),
    ('TxnScopeContext', ctypes.POINTER(None)),
    ('LockCount', ctypes.c_uint32),
    ('WowTebOffset', ctypes.c_int32),
    ('ResourceRetValue', ctypes.POINTER(None)),
    ('ReservedForWdf', ctypes.POINTER(None)),
    ('ReservedForCrt', ctypes.c_uint64),
    ('EffectiveContainerId', struct__GUID),
]


# values for enumeration '_EXCEPTION_DISPOSITION'
_EXCEPTION_DISPOSITION__enumvalues = {
    0: 'ExceptionContinueExecution',
    1: 'ExceptionContinueSearch',
    2: 'ExceptionNestedException',
    3: 'ExceptionCollidedUnwind',
}
ExceptionContinueExecution = 0
ExceptionContinueSearch = 1
ExceptionNestedException = 2
ExceptionCollidedUnwind = 3
_EXCEPTION_DISPOSITION = ctypes.c_uint32 # enum
class struct__CONTEXT(Structure):
    pass

struct__EXCEPTION_REGISTRATION_RECORD._pack_ = 1 # source:False
struct__EXCEPTION_REGISTRATION_RECORD._fields_ = [
    ('Next', ctypes.POINTER(struct__EXCEPTION_REGISTRATION_RECORD)),
    ('Handler', ctypes.CFUNCTYPE(_EXCEPTION_DISPOSITION, ctypes.POINTER(struct__EXCEPTION_RECORD), ctypes.POINTER(None), ctypes.POINTER(struct__CONTEXT), ctypes.POINTER(None))),
]

class struct__M128A(Structure):
    pass

struct__M128A._pack_ = 1 # source:False
struct__M128A._fields_ = [
    ('Low', ctypes.c_uint64),
    ('High', ctypes.c_int64),
]

class union_union_59(Union):
    pass

class struct__XSAVE_FORMAT(Structure):
    pass

struct__XSAVE_FORMAT._pack_ = 1 # source:False
struct__XSAVE_FORMAT._fields_ = [
    ('ControlWord', ctypes.c_uint16),
    ('StatusWord', ctypes.c_uint16),
    ('TagWord', ctypes.c_ubyte),
    ('Reserved1', ctypes.c_ubyte),
    ('ErrorOpcode', ctypes.c_uint16),
    ('ErrorOffset', ctypes.c_uint32),
    ('ErrorSelector', ctypes.c_uint16),
    ('Reserved2', ctypes.c_uint16),
    ('DataOffset', ctypes.c_uint32),
    ('DataSelector', ctypes.c_uint16),
    ('Reserved3', ctypes.c_uint16),
    ('MxCsr', ctypes.c_uint32),
    ('MxCsr_Mask', ctypes.c_uint32),
    ('FloatRegisters', struct__M128A * 8),
    ('XmmRegisters', struct__M128A * 16),
    ('Reserved4', ctypes.c_ubyte * 96),
]

class struct_struct_60(Structure):
    _pack_ = 1 # source:False
    _fields_ = [
    ('Header', struct__M128A * 2),
    ('Legacy', struct__M128A * 8),
    ('Xmm0', struct__M128A),
    ('Xmm1', struct__M128A),
    ('Xmm2', struct__M128A),
    ('Xmm3', struct__M128A),
    ('Xmm4', struct__M128A),
    ('Xmm5', struct__M128A),
    ('Xmm6', struct__M128A),
    ('Xmm7', struct__M128A),
    ('Xmm8', struct__M128A),
    ('Xmm9', struct__M128A),
    ('Xmm10', struct__M128A),
    ('Xmm11', struct__M128A),
    ('Xmm12', struct__M128A),
    ('Xmm13', struct__M128A),
    ('Xmm14', struct__M128A),
    ('Xmm15', struct__M128A),
     ]

union_union_59._pack_ = 1 # source:False
union_union_59._anonymous_ = ('_0',)
union_union_59._fields_ = [
    ('FltSave', struct__XSAVE_FORMAT),
    ('_0', struct_struct_60),
    ('PADDING_0', ctypes.c_ubyte * 96),
]

struct__CONTEXT._pack_ = 1 # source:False
struct__CONTEXT._anonymous_ = ('_0',)
struct__CONTEXT._fields_ = [
    ('P1Home', ctypes.c_uint64),
    ('P2Home', ctypes.c_uint64),
    ('P3Home', ctypes.c_uint64),
    ('P4Home', ctypes.c_uint64),
    ('P5Home', ctypes.c_uint64),
    ('P6Home', ctypes.c_uint64),
    ('ContextFlags', ctypes.c_uint32),
    ('MxCsr', ctypes.c_uint32),
    ('SegCs', ctypes.c_uint16),
    ('SegDs', ctypes.c_uint16),
    ('SegEs', ctypes.c_uint16),
    ('SegFs', ctypes.c_uint16),
    ('SegGs', ctypes.c_uint16),
    ('SegSs', ctypes.c_uint16),
    ('EFlags', ctypes.c_uint32),
    ('Dr0', ctypes.c_uint64),
    ('Dr1', ctypes.c_uint64),
    ('Dr2', ctypes.c_uint64),
    ('Dr3', ctypes.c_uint64),
    ('Dr6', ctypes.c_uint64),
    ('Dr7', ctypes.c_uint64),
    ('Rax', ctypes.c_uint64),
    ('Rcx', ctypes.c_uint64),
    ('Rdx', ctypes.c_uint64),
    ('Rbx', ctypes.c_uint64),
    ('Rsp', ctypes.c_uint64),
    ('Rbp', ctypes.c_uint64),
    ('Rsi', ctypes.c_uint64),
    ('Rdi', ctypes.c_uint64),
    ('R8', ctypes.c_uint64),
    ('R9', ctypes.c_uint64),
    ('R10', ctypes.c_uint64),
    ('R11', ctypes.c_uint64),
    ('R12', ctypes.c_uint64),
    ('R13', ctypes.c_uint64),
    ('R14', ctypes.c_uint64),
    ('R15', ctypes.c_uint64),
    ('Rip', ctypes.c_uint64),
    ('_0', union_union_59),
    ('VectorRegister', struct__M128A * 26),
    ('VectorControl', ctypes.c_uint64),
    ('DebugControl', ctypes.c_uint64),
    ('LastBranchToRip', ctypes.c_uint64),
    ('LastBranchFromRip', ctypes.c_uint64),
    ('LastExceptionToRip', ctypes.c_uint64),
    ('LastExceptionFromRip', ctypes.c_uint64),
]

TEB = struct__TEB
PTEB = ctypes.POINTER(struct__TEB)

# values for enumeration '_ALTERNATIVE_ARCHITECTURE_TYPE'
_ALTERNATIVE_ARCHITECTURE_TYPE__enumvalues = {
    0: 'StandardDesign',
    1: 'NEC98x86',
    2: 'EndAlternatives',
}
StandardDesign = 0
NEC98x86 = 1
EndAlternatives = 2
_ALTERNATIVE_ARCHITECTURE_TYPE = ctypes.c_uint32 # enum
ALTERNATIVE_ARCHITECTURE_TYPE = _ALTERNATIVE_ARCHITECTURE_TYPE
ALTERNATIVE_ARCHITECTURE_TYPE__enumvalues = _ALTERNATIVE_ARCHITECTURE_TYPE__enumvalues
class struct__KUSER_SHARED_DATA(Structure):
    pass

class union_union_61(Union):
    pass

class struct_struct_62(Structure):
    pass

struct_struct_62._pack_ = 1 # source:False
struct_struct_62._fields_ = [
    ('NXSupportPolicy', ctypes.c_ubyte, 2),
    ('SEHValidationPolicy', ctypes.c_ubyte, 2),
    ('CurDirDevicesSkippedForDlls', ctypes.c_ubyte, 2),
    ('Reserved', ctypes.c_ubyte, 2),
]

union_union_61._pack_ = 1 # source:False
union_union_61._fields_ = [
    ('MitigationPolicies', ctypes.c_ubyte),
    ('s1', struct_struct_62),
]

class union_union_63(Union):
    pass

union_union_63._pack_ = 1 # source:False
union_union_63._fields_ = [
    ('TickCount', KSYSTEM_TIME),
    ('TickCountQuad', ctypes.c_uint64),
    ('ReservedTickCountOverlay', ctypes.c_uint32 * 3),
]

class union_union_64(Union):
    pass

class struct_struct_65(Structure):
    pass

struct_struct_65._pack_ = 1 # source:False
struct_struct_65._fields_ = [
    ('QpcBypassEnabled', ctypes.c_ubyte, 1),
    ('QpcShift', ctypes.c_ubyte, 1),
    ('PADDING_0', ctypes.c_uint8, 6),
]

union_union_64._pack_ = 1 # source:False
union_union_64._fields_ = [
    ('QpcData', ctypes.c_uint16),
    ('s3', struct_struct_65),
    ('PADDING_0', ctypes.c_ubyte),
]

class struct__XSTATE_CONFIGURATION(Structure):
    pass

class union_union_66(Union):
    pass

class struct_struct_67(Structure):
    pass

struct_struct_67._pack_ = 1 # source:False
struct_struct_67._fields_ = [
    ('OptimizedSave', ctypes.c_uint32, 1),
    ('CompactionEnabled', ctypes.c_uint32, 1),
    ('ExtendedFeatureDisable', ctypes.c_uint32, 1),
    ('PADDING_0', ctypes.c_uint32, 29),
]

union_union_66._pack_ = 1 # source:False
union_union_66._anonymous_ = ('_0',)
union_union_66._fields_ = [
    ('ControlFlags', ctypes.c_uint32),
    ('_0', struct_struct_67),
]

class struct__XSTATE_FEATURE(Structure):
    pass

struct__XSTATE_FEATURE._pack_ = 1 # source:False
struct__XSTATE_FEATURE._fields_ = [
    ('Offset', ctypes.c_uint32),
    ('Size', ctypes.c_uint32),
]

struct__XSTATE_CONFIGURATION._pack_ = 1 # source:False
struct__XSTATE_CONFIGURATION._anonymous_ = ('_0',)
struct__XSTATE_CONFIGURATION._fields_ = [
    ('EnabledFeatures', ctypes.c_uint64),
    ('EnabledVolatileFeatures', ctypes.c_uint64),
    ('Size', ctypes.c_uint32),
    ('_0', union_union_66),
    ('Features', struct__XSTATE_FEATURE * 64),
    ('EnabledSupervisorFeatures', ctypes.c_uint64),
    ('AlignedFeatures', ctypes.c_uint64),
    ('AllFeatureSize', ctypes.c_uint32),
    ('AllFeatures', ctypes.c_uint32 * 64),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('EnabledUserVisibleSupervisorFeatures', ctypes.c_uint64),
    ('ExtendedFeatureDisableFeatures', ctypes.c_uint64),
    ('AllNonLargeFeatureSize', ctypes.c_uint32),
    ('Spare', ctypes.c_uint32),
]

class union_union_68(Union):
    pass

class struct_struct_69(Structure):
    pass

struct_struct_69._pack_ = 1 # source:False
struct_struct_69._fields_ = [
    ('DbgErrorPortPresent', ctypes.c_uint32, 1),
    ('DbgElevationEnabled', ctypes.c_uint32, 1),
    ('DbgVirtEnabled', ctypes.c_uint32, 1),
    ('DbgInstallerDetectEnabled', ctypes.c_uint32, 1),
    ('DbgLkgEnabled', ctypes.c_uint32, 1),
    ('DbgDynProcessorEnabled', ctypes.c_uint32, 1),
    ('DbgConsoleBrokerEnabled', ctypes.c_uint32, 1),
    ('DbgSecureBootEnabled', ctypes.c_uint32, 1),
    ('DbgMultiSessionSku', ctypes.c_uint32, 1),
    ('DbgMultiUsersInSessionSku', ctypes.c_uint32, 1),
    ('SpareBits', ctypes.c_uint32, 22),
]

union_union_68._pack_ = 1 # source:False
union_union_68._fields_ = [
    ('SharedDataFlags', ctypes.c_uint32),
    ('s2', struct_struct_69),
]

struct__KUSER_SHARED_DATA._pack_ = 1 # source:False
struct__KUSER_SHARED_DATA._anonymous_ = ('_0',)
struct__KUSER_SHARED_DATA._fields_ = [
    ('TickCountLowDeprecated', ctypes.c_uint32),
    ('TickCountMultiplier', ctypes.c_uint32),
    ('InterruptTime', KSYSTEM_TIME),
    ('SystemTime', KSYSTEM_TIME),
    ('TimeZoneBias', KSYSTEM_TIME),
    ('ImageNumberLow', ctypes.c_uint16),
    ('ImageNumberHigh', ctypes.c_uint16),
    ('NtSystemRoot', ctypes.c_uint16 * 260),
    ('MaxStackTraceDepth', ctypes.c_uint32),
    ('CryptoExponent', ctypes.c_uint32),
    ('TimeZoneId', ctypes.c_uint32),
    ('LargePageMinimum', ctypes.c_uint32),
    ('AitSamplingValue', ctypes.c_uint32),
    ('AppCompatFlag', ctypes.c_uint32),
    ('RNGSeedVersion', ctypes.c_uint64),
    ('GlobalValidationRunlevel', ctypes.c_uint32),
    ('TimeZoneBiasStamp', ctypes.c_int32),
    ('NtBuildNumber', ctypes.c_uint32),
    ('NtProductType', ctypes.c_uint32),
    ('ProductTypeIsValid', ctypes.c_ubyte),
    ('Reserved0', ctypes.c_ubyte * 1),
    ('NativeProcessorArchitecture', ctypes.c_uint16),
    ('NtMajorVersion', ctypes.c_uint32),
    ('NtMinorVersion', ctypes.c_uint32),
    ('ProcessorFeatures', ctypes.c_ubyte * 64),
    ('Reserved1', ctypes.c_uint32),
    ('Reserved3', ctypes.c_uint32),
    ('TimeSlip', ctypes.c_uint32),
    ('AlternativeArchitecture', ALTERNATIVE_ARCHITECTURE_TYPE),
    ('BootId', ctypes.c_uint32),
    ('SystemExpirationDate', union__LARGE_INTEGER),
    ('SuiteMask', ctypes.c_uint32),
    ('KdDebuggerEnabled', ctypes.c_ubyte),
    ('u1', union_union_61),
    ('Reserved6', ctypes.c_ubyte * 2),
    ('ActiveConsoleId', ctypes.c_uint32),
    ('DismountCount', ctypes.c_uint32),
    ('ComPlusPackage', ctypes.c_uint32),
    ('LastSystemRITEventTickCount', ctypes.c_uint32),
    ('NumberOfPhysicalPages', ctypes.c_uint32),
    ('SafeBootMode', ctypes.c_ubyte),
    ('VirtualizationFlags', ctypes.c_ubyte),
    ('Reserved12', ctypes.c_ubyte * 2),
    ('u2', union_union_68),
    ('DataFlagsPad', ctypes.c_uint32 * 1),
    ('TestRetInstruction', ctypes.c_uint64),
    ('QpcFrequency', ctypes.c_int64),
    ('SystemCall', ctypes.c_uint32),
    ('SystemCallPad0', ctypes.c_uint32),
    ('SystemCallPad', ctypes.c_uint64 * 2),
    ('_0', union_union_63),
    ('TickCountPad', ctypes.c_uint32 * 1),
    ('Cookie', ctypes.c_uint32),
    ('CookiePad', ctypes.c_uint32 * 1),
    ('ConsoleSessionForegroundProcessId', ctypes.c_int64),
    ('TimeUpdateLock', ctypes.c_uint64),
    ('BaselineSystemTimeQpc', ctypes.c_uint64),
    ('BaselineInterruptTimeQpc', ctypes.c_uint64),
    ('QpcSystemTimeIncrement', ctypes.c_uint64),
    ('QpcInterruptTimeIncrement', ctypes.c_uint64),
    ('QpcSystemTimeIncrementShift', ctypes.c_ubyte),
    ('QpcInterruptTimeIncrementShift', ctypes.c_ubyte),
    ('UnparkedProcessorCount', ctypes.c_uint16),
    ('EnclaveFeatureMask', ctypes.c_uint32 * 4),
    ('Reserved8', ctypes.c_uint32),
    ('UserModeGlobalLogger', ctypes.c_uint16 * 16),
    ('ImageFileExecutionOptions', ctypes.c_uint32),
    ('LangGenerationCount', ctypes.c_uint32),
    ('Reserved4', ctypes.c_uint64),
    ('InterruptTimeBias', ctypes.c_uint64),
    ('QpcBias', ctypes.c_uint64),
    ('ActiveProcessorCount', ctypes.c_uint32),
    ('ActiveGroupCount', ctypes.c_ubyte),
    ('Reserved9', ctypes.c_ubyte),
    ('u3', union_union_64),
    ('TimeZoneBiasEffectiveStart', union__LARGE_INTEGER),
    ('TimeZoneBiasEffectiveEnd', union__LARGE_INTEGER),
    ('XState', struct__XSTATE_CONFIGURATION),
]

KUSER_SHARED_DATA = struct__KUSER_SHARED_DATA
PKUSER_SHARED_DATA = ctypes.POINTER(struct__KUSER_SHARED_DATA)
class struct__PROCESS_BASIC_INFORMATION(Structure):
    pass

struct__PROCESS_BASIC_INFORMATION._pack_ = 1 # source:False
struct__PROCESS_BASIC_INFORMATION._fields_ = [
    ('ExitStatus', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('PebBaseAddress', ctypes.POINTER(struct__PEB)),
    ('AffinityMask', ctypes.c_uint64),
    ('BasePriority', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('UniqueProcessId', ctypes.POINTER(None)),
    ('InheritedFromUniqueProcessId', ctypes.POINTER(None)),
]

PROCESS_BASIC_INFORMATION = struct__PROCESS_BASIC_INFORMATION
PPROCESS_BASIC_INFORMATION = ctypes.POINTER(struct__PROCESS_BASIC_INFORMATION)
class struct__PROCESS_EXTENDED_BASIC_INFORMATION(Structure):
    pass

class union_union_70(Union):
    pass

class struct_struct_71(Structure):
    pass

struct_struct_71._pack_ = 1 # source:False
struct_struct_71._fields_ = [
    ('IsProtectedProcess', ctypes.c_uint32, 1),
    ('IsWow64Process', ctypes.c_uint32, 1),
    ('IsProcessDeleting', ctypes.c_uint32, 1),
    ('IsCrossSessionCreate', ctypes.c_uint32, 1),
    ('IsFrozen', ctypes.c_uint32, 1),
    ('IsBackground', ctypes.c_uint32, 1),
    ('IsStronglyNamed', ctypes.c_uint32, 1),
    ('IsSecureProcess', ctypes.c_uint32, 1),
    ('IsSubsystemProcess', ctypes.c_uint32, 1),
    ('SpareBits', ctypes.c_uint32, 23),
]

union_union_70._pack_ = 1 # source:False
union_union_70._fields_ = [
    ('Flags', ctypes.c_uint32),
    ('s', struct_struct_71),
]

struct__PROCESS_EXTENDED_BASIC_INFORMATION._pack_ = 1 # source:False
struct__PROCESS_EXTENDED_BASIC_INFORMATION._fields_ = [
    ('Size', ctypes.c_uint64),
    ('BasicInfo', PROCESS_BASIC_INFORMATION),
    ('u', union_union_70),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

PROCESS_EXTENDED_BASIC_INFORMATION = struct__PROCESS_EXTENDED_BASIC_INFORMATION
PPROCESS_EXTENDED_BASIC_INFORMATION = ctypes.POINTER(struct__PROCESS_EXTENDED_BASIC_INFORMATION)
class struct__SYSTEM_EXTENDED_THREAD_INFORMATION(Structure):
    pass

struct__SYSTEM_EXTENDED_THREAD_INFORMATION._pack_ = 1 # source:False
struct__SYSTEM_EXTENDED_THREAD_INFORMATION._fields_ = [
    ('ThreadInfo', SYSTEM_THREAD_INFORMATION),
    ('StackBase', ctypes.POINTER(None)),
    ('StackLimit', ctypes.POINTER(None)),
    ('Win32StartAddress', ctypes.POINTER(None)),
    ('TebBase', ctypes.POINTER(struct__TEB)),
    ('Reserved2', ctypes.c_uint64),
    ('Reserved3', ctypes.c_uint64),
    ('Reserved4', ctypes.c_uint64),
]

SYSTEM_EXTENDED_THREAD_INFORMATION = struct__SYSTEM_EXTENDED_THREAD_INFORMATION
PSYSTEM_EXTENDED_THREAD_INFORMATION = ctypes.POINTER(struct__SYSTEM_EXTENDED_THREAD_INFORMATION)
RTL_HEAP_ENTRY = struct__RTL_HEAP_ENTRY
PRTL_HEAP_ENTRY = ctypes.POINTER(struct__RTL_HEAP_ENTRY)
RTL_HEAP_TAG = struct__RTL_HEAP_TAG
PRTL_HEAP_TAG = ctypes.POINTER(struct__RTL_HEAP_TAG)
RTL_HEAP_INFORMATION = struct__RTL_HEAP_INFORMATION
PRTL_HEAP_INFORMATION = ctypes.POINTER(struct__RTL_HEAP_INFORMATION)
RTL_PROCESS_HEAPS = struct__RTL_PROCESS_HEAPS
PRTL_PROCESS_HEAPS = ctypes.POINTER(struct__RTL_PROCESS_HEAPS)
PRTL_HEAP_COMMIT_ROUTINE = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(None), ctypes.POINTER(ctypes.POINTER(None)), ctypes.POINTER(ctypes.c_uint64))
class struct__RTL_HEAP_PARAMETERS(Structure):
    pass

struct__RTL_HEAP_PARAMETERS._pack_ = 1 # source:False
struct__RTL_HEAP_PARAMETERS._fields_ = [
    ('Length', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('SegmentReserve', ctypes.c_uint64),
    ('SegmentCommit', ctypes.c_uint64),
    ('DeCommitFreeBlockThreshold', ctypes.c_uint64),
    ('DeCommitTotalFreeThreshold', ctypes.c_uint64),
    ('MaximumAllocationSize', ctypes.c_uint64),
    ('VirtualMemoryThreshold', ctypes.c_uint64),
    ('InitialCommit', ctypes.c_uint64),
    ('InitialReserve', ctypes.c_uint64),
    ('CommitRoutine', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(None), ctypes.POINTER(ctypes.POINTER(None)), ctypes.POINTER(ctypes.c_uint64))),
    ('Reserved', ctypes.c_uint64 * 2),
]

RTL_HEAP_PARAMETERS = struct__RTL_HEAP_PARAMETERS
PRTL_HEAP_PARAMETERS = ctypes.POINTER(struct__RTL_HEAP_PARAMETERS)
class struct__RTL_HEAP_TAG_INFO(Structure):
    pass

struct__RTL_HEAP_TAG_INFO._pack_ = 1 # source:False
struct__RTL_HEAP_TAG_INFO._fields_ = [
    ('NumberOfAllocations', ctypes.c_uint32),
    ('NumberOfFrees', ctypes.c_uint32),
    ('BytesAllocated', ctypes.c_uint64),
]

RTL_HEAP_TAG_INFO = struct__RTL_HEAP_TAG_INFO
PRTL_HEAP_TAG_INFO = ctypes.POINTER(struct__RTL_HEAP_TAG_INFO)
class struct__RTL_HEAP_WALK_ENTRY(Structure):
    pass

class union_union_72(Union):
    pass

class struct_struct_73(Structure):
    pass

struct_struct_73._pack_ = 1 # source:False
struct_struct_73._fields_ = [
    ('Settable', ctypes.c_uint64),
    ('TagIndex', ctypes.c_uint16),
    ('AllocatorBackTraceIndex', ctypes.c_uint16),
    ('Reserved', ctypes.c_uint32 * 2),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

class struct_struct_74(Structure):
    pass

struct_struct_74._pack_ = 1 # source:False
struct_struct_74._fields_ = [
    ('CommittedSize', ctypes.c_uint32),
    ('UnCommittedSize', ctypes.c_uint32),
    ('FirstEntry', ctypes.POINTER(None)),
    ('LastEntry', ctypes.POINTER(None)),
]

union_union_72._pack_ = 1 # source:False
union_union_72._fields_ = [
    ('Block', struct_struct_73),
    ('Segment', struct_struct_74),
]

struct__RTL_HEAP_WALK_ENTRY._pack_ = 1 # source:False
struct__RTL_HEAP_WALK_ENTRY._anonymous_ = ('_0',)
struct__RTL_HEAP_WALK_ENTRY._fields_ = [
    ('DataAddress', ctypes.POINTER(None)),
    ('DataSize', ctypes.c_uint64),
    ('OverheadBytes', ctypes.c_ubyte),
    ('SegmentIndex', ctypes.c_ubyte),
    ('Flags', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('_0', union_union_72),
]

RTL_HEAP_WALK_ENTRY = struct__RTL_HEAP_WALK_ENTRY
PRTL_HEAP_WALK_ENTRY = ctypes.POINTER(struct__RTL_HEAP_WALK_ENTRY)
class struct__PROCESS_HEAP_INFORMATION(Structure):
    pass

struct__PROCESS_HEAP_INFORMATION._pack_ = 1 # source:False
struct__PROCESS_HEAP_INFORMATION._fields_ = [
    ('ReserveSize', ctypes.c_uint64),
    ('CommitSize', ctypes.c_uint64),
    ('NumberOfHeaps', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('FirstHeapInformationOffset', ctypes.c_uint64),
]

PROCESS_HEAP_INFORMATION = struct__PROCESS_HEAP_INFORMATION
PPROCESS_HEAP_INFORMATION = ctypes.POINTER(struct__PROCESS_HEAP_INFORMATION)
class struct__HEAP_INFORMATION(Structure):
    pass

struct__HEAP_INFORMATION._pack_ = 1 # source:False
struct__HEAP_INFORMATION._fields_ = [
    ('Address', ctypes.c_uint64),
    ('Mode', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('ReserveSize', ctypes.c_uint64),
    ('CommitSize', ctypes.c_uint64),
    ('FirstRegionInformationOffset', ctypes.c_uint64),
    ('NextHeapInformationOffset', ctypes.c_uint64),
]

HEAP_INFORMATION = struct__HEAP_INFORMATION
PHEAP_INFORMATION = ctypes.POINTER(struct__HEAP_INFORMATION)
class struct__HEAP_EXTENDED_INFORMATION(Structure):
    pass

struct__HEAP_EXTENDED_INFORMATION._pack_ = 1 # source:False
struct__HEAP_EXTENDED_INFORMATION._fields_ = [
    ('Process', ctypes.POINTER(None)),
    ('Heap', ctypes.c_uint64),
    ('Level', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('CallbackRoutine', ctypes.POINTER(None)),
    ('CallbackContext', ctypes.POINTER(None)),
    ('ProcessHeapInformation', PROCESS_HEAP_INFORMATION),
    ('HeapInformation', HEAP_INFORMATION),
]

HEAP_EXTENDED_INFORMATION = struct__HEAP_EXTENDED_INFORMATION
PHEAP_EXTENDED_INFORMATION = ctypes.POINTER(struct__HEAP_EXTENDED_INFORMATION)
PRTL_HEAP_LEAK_ENUMERATION_ROUTINE = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32, ctypes.POINTER(None), ctypes.POINTER(None), ctypes.c_uint64, ctypes.c_uint32, ctypes.POINTER(ctypes.POINTER(None)))
class struct__HEAP_DEBUGGING_INFORMATION(Structure):
    pass

struct__HEAP_DEBUGGING_INFORMATION._pack_ = 1 # source:False
struct__HEAP_DEBUGGING_INFORMATION._fields_ = [
    ('InterceptorFunction', ctypes.POINTER(None)),
    ('InterceptorValue', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 2),
    ('ExtendedOptions', ctypes.c_uint32),
    ('StackTraceDepth', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('MinTotalBlockSize', ctypes.c_uint64),
    ('MaxTotalBlockSize', ctypes.c_uint64),
    ('HeapLeakEnumerationRoutine', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32, ctypes.POINTER(None), ctypes.POINTER(None), ctypes.c_uint64, ctypes.c_uint32, ctypes.POINTER(ctypes.POINTER(None)))),
]

HEAP_DEBUGGING_INFORMATION = struct__HEAP_DEBUGGING_INFORMATION
PHEAP_DEBUGGING_INFORMATION = ctypes.POINTER(struct__HEAP_DEBUGGING_INFORMATION)
PRTL_ENUM_HEAPS_ROUTINE = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(None), ctypes.POINTER(None))
PUSER_THREAD_START_ROUTINE = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(None))
PLDR_IMPORT_MODULE_CALLBACK = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(ctypes.c_char))
class struct__LDR_IMPORT_CALLBACK_INFO(Structure):
    pass

struct__LDR_IMPORT_CALLBACK_INFO._pack_ = 1 # source:False
struct__LDR_IMPORT_CALLBACK_INFO._fields_ = [
    ('ImportCallbackRoutine', ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(ctypes.c_char))),
    ('ImportCallbackParameter', ctypes.POINTER(None)),
]

LDR_IMPORT_CALLBACK_INFO = struct__LDR_IMPORT_CALLBACK_INFO
PLDR_IMPORT_CALLBACK_INFO = ctypes.POINTER(struct__LDR_IMPORT_CALLBACK_INFO)
class struct__LDR_SECTION_INFO(Structure):
    pass

struct__LDR_SECTION_INFO._pack_ = 1 # source:False
struct__LDR_SECTION_INFO._fields_ = [
    ('SectionHandle', ctypes.POINTER(None)),
    ('DesiredAccess', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('ObjectAttributes', ctypes.POINTER(struct__OBJECT_ATTRIBUTES)),
    ('SectionPageProtection', ctypes.c_uint32),
    ('AllocationAttributes', ctypes.c_uint32),
]

LDR_SECTION_INFO = struct__LDR_SECTION_INFO
PLDR_SECTION_INFO = ctypes.POINTER(struct__LDR_SECTION_INFO)
class struct__LDR_VERIFY_IMAGE_INFO(Structure):
    pass

struct__LDR_VERIFY_IMAGE_INFO._pack_ = 1 # source:False
struct__LDR_VERIFY_IMAGE_INFO._fields_ = [
    ('Size', ctypes.c_uint32),
    ('Flags', ctypes.c_uint32),
    ('CallbackInfo', LDR_IMPORT_CALLBACK_INFO),
    ('SectionInfo', LDR_SECTION_INFO),
    ('ImageCharacteristics', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 6),
]

LDR_VERIFY_IMAGE_INFO = struct__LDR_VERIFY_IMAGE_INFO
PLDR_VERIFY_IMAGE_INFO = ctypes.POINTER(struct__LDR_VERIFY_IMAGE_INFO)

# values for enumeration '_SEMAPHORE_INFORMATION_CLASS'
_SEMAPHORE_INFORMATION_CLASS__enumvalues = {
    0: 'SemaphoreBasicInformation',
}
SemaphoreBasicInformation = 0
_SEMAPHORE_INFORMATION_CLASS = ctypes.c_uint32 # enum
SEMAPHORE_INFORMATION_CLASS = _SEMAPHORE_INFORMATION_CLASS
SEMAPHORE_INFORMATION_CLASS__enumvalues = _SEMAPHORE_INFORMATION_CLASS__enumvalues
class struct__SEMAPHORE_BASIC_INFORMATION(Structure):
    pass

struct__SEMAPHORE_BASIC_INFORMATION._pack_ = 1 # source:False
struct__SEMAPHORE_BASIC_INFORMATION._fields_ = [
    ('CurrentCount', ctypes.c_int32),
    ('MaximumCount', ctypes.c_int32),
]

SEMAPHORE_BASIC_INFORMATION = struct__SEMAPHORE_BASIC_INFORMATION
PSEMAPHORE_BASIC_INFORMATION = ctypes.POINTER(struct__SEMAPHORE_BASIC_INFORMATION)

# values for enumeration '_TIMER_INFORMATION_CLASS'
_TIMER_INFORMATION_CLASS__enumvalues = {
    0: 'TimerBasicInformation',
}
TimerBasicInformation = 0
_TIMER_INFORMATION_CLASS = ctypes.c_uint32 # enum
TIMER_INFORMATION_CLASS = _TIMER_INFORMATION_CLASS
TIMER_INFORMATION_CLASS__enumvalues = _TIMER_INFORMATION_CLASS__enumvalues
class struct__TIMER_BASIC_INFORMATION(Structure):
    pass

struct__TIMER_BASIC_INFORMATION._pack_ = 1 # source:False
struct__TIMER_BASIC_INFORMATION._fields_ = [
    ('RemainingTime', union__LARGE_INTEGER),
    ('TimerState', ctypes.c_ubyte),
    ('PADDING_0', ctypes.c_ubyte * 7),
]

TIMER_BASIC_INFORMATION = struct__TIMER_BASIC_INFORMATION
PTIMER_BASIC_INFORMATION = ctypes.POINTER(struct__TIMER_BASIC_INFORMATION)
PTIMER_APC_ROUTINE = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.c_uint32, ctypes.c_int32)

# values for enumeration '_TIMER_SET_INFORMATION_CLASS'
_TIMER_SET_INFORMATION_CLASS__enumvalues = {
    0: 'TimerSetCoalescableTimer',
    1: 'MaxTimerInfoClass',
}
TimerSetCoalescableTimer = 0
MaxTimerInfoClass = 1
_TIMER_SET_INFORMATION_CLASS = ctypes.c_uint32 # enum
TIMER_SET_INFORMATION_CLASS = _TIMER_SET_INFORMATION_CLASS
TIMER_SET_INFORMATION_CLASS__enumvalues = _TIMER_SET_INFORMATION_CLASS__enumvalues
class struct__TIMER_SET_COALESCABLE_TIMER_INFO(Structure):
    pass

class struct__COUNTED_REASON_CONTEXT(Structure):
    pass

struct__TIMER_SET_COALESCABLE_TIMER_INFO._pack_ = 1 # source:False
struct__TIMER_SET_COALESCABLE_TIMER_INFO._fields_ = [
    ('DueTime', union__LARGE_INTEGER),
    ('TimerApcRoutine', ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.c_uint32, ctypes.c_int32)),
    ('TimerContext', ctypes.POINTER(None)),
    ('WakeContext', ctypes.POINTER(struct__COUNTED_REASON_CONTEXT)),
    ('Period', ctypes.c_uint32),
    ('TolerableDelay', ctypes.c_uint32),
    ('PreviousState', ctypes.POINTER(ctypes.c_ubyte)),
]

TIMER_SET_COALESCABLE_TIMER_INFO = struct__TIMER_SET_COALESCABLE_TIMER_INFO
PTIMER_SET_COALESCABLE_TIMER_INFO = ctypes.POINTER(struct__TIMER_SET_COALESCABLE_TIMER_INFO)
class struct__TOKEN_SECURITY_ATTRIBUTE_FQBN_VALUE(Structure):
    pass

struct__TOKEN_SECURITY_ATTRIBUTE_FQBN_VALUE._pack_ = 1 # source:False
struct__TOKEN_SECURITY_ATTRIBUTE_FQBN_VALUE._fields_ = [
    ('Version', ctypes.c_uint64),
    ('Name', UNICODE_STRING),
]

TOKEN_SECURITY_ATTRIBUTE_FQBN_VALUE = struct__TOKEN_SECURITY_ATTRIBUTE_FQBN_VALUE
PTOKEN_SECURITY_ATTRIBUTE_FQBN_VALUE = ctypes.POINTER(struct__TOKEN_SECURITY_ATTRIBUTE_FQBN_VALUE)
class struct__TOKEN_SECURITY_ATTRIBUTE_OCTET_STRING_VALUE(Structure):
    pass

struct__TOKEN_SECURITY_ATTRIBUTE_OCTET_STRING_VALUE._pack_ = 1 # source:False
struct__TOKEN_SECURITY_ATTRIBUTE_OCTET_STRING_VALUE._fields_ = [
    ('pValue', ctypes.POINTER(None)),
    ('ValueLength', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

TOKEN_SECURITY_ATTRIBUTE_OCTET_STRING_VALUE = struct__TOKEN_SECURITY_ATTRIBUTE_OCTET_STRING_VALUE
PTOKEN_SECURITY_ATTRIBUTE_OCTET_STRING_VALUE = ctypes.POINTER(struct__TOKEN_SECURITY_ATTRIBUTE_OCTET_STRING_VALUE)
class struct__TOKEN_SECURITY_ATTRIBUTE_V1(Structure):
    pass

class union_union_75(Union):
    pass

union_union_75._pack_ = 1 # source:False
union_union_75._fields_ = [
    ('pInt64', ctypes.POINTER(ctypes.c_int64)),
    ('pUint64', ctypes.POINTER(ctypes.c_uint64)),
    ('pString', ctypes.POINTER(struct__UNICODE_STRING)),
    ('pFqbn', ctypes.POINTER(struct__TOKEN_SECURITY_ATTRIBUTE_FQBN_VALUE)),
    ('pOctetString', ctypes.POINTER(struct__TOKEN_SECURITY_ATTRIBUTE_OCTET_STRING_VALUE)),
]

struct__TOKEN_SECURITY_ATTRIBUTE_V1._pack_ = 1 # source:False
struct__TOKEN_SECURITY_ATTRIBUTE_V1._fields_ = [
    ('Name', UNICODE_STRING),
    ('ValueType', ctypes.c_uint16),
    ('Reserved', ctypes.c_uint16),
    ('Flags', ctypes.c_uint32),
    ('ValueCount', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('Values', union_union_75),
]

TOKEN_SECURITY_ATTRIBUTE_V1 = struct__TOKEN_SECURITY_ATTRIBUTE_V1
PTOKEN_SECURITY_ATTRIBUTE_V1 = ctypes.POINTER(struct__TOKEN_SECURITY_ATTRIBUTE_V1)
class struct__TOKEN_SECURITY_ATTRIBUTES_INFORMATION(Structure):
    pass

class union_union_76(Union):
    pass

union_union_76._pack_ = 1 # source:False
union_union_76._fields_ = [
    ('pAttributeV1', ctypes.POINTER(struct__TOKEN_SECURITY_ATTRIBUTE_V1)),
]

struct__TOKEN_SECURITY_ATTRIBUTES_INFORMATION._pack_ = 1 # source:False
struct__TOKEN_SECURITY_ATTRIBUTES_INFORMATION._fields_ = [
    ('Version', ctypes.c_uint16),
    ('Reserved', ctypes.c_uint16),
    ('AttributeCount', ctypes.c_uint32),
    ('Attribute', union_union_76),
]

TOKEN_SECURITY_ATTRIBUTES_INFORMATION = struct__TOKEN_SECURITY_ATTRIBUTES_INFORMATION
PTOKEN_SECURITY_ATTRIBUTES_INFORMATION = ctypes.POINTER(struct__TOKEN_SECURITY_ATTRIBUTES_INFORMATION)

# values for enumeration '_FILTER_BOOT_OPTION_OPERATION'
_FILTER_BOOT_OPTION_OPERATION__enumvalues = {
    0: 'FilterBootOptionOperationOpenSystemStore',
    1: 'FilterBootOptionOperationSetElement',
    2: 'FilterBootOptionOperationDeleteElement',
    3: 'FilterBootOptionOperationMax',
}
FilterBootOptionOperationOpenSystemStore = 0
FilterBootOptionOperationSetElement = 1
FilterBootOptionOperationDeleteElement = 2
FilterBootOptionOperationMax = 3
_FILTER_BOOT_OPTION_OPERATION = ctypes.c_uint32 # enum
FILTER_BOOT_OPTION_OPERATION = _FILTER_BOOT_OPTION_OPERATION
FILTER_BOOT_OPTION_OPERATION__enumvalues = _FILTER_BOOT_OPTION_OPERATION__enumvalues

# values for enumeration '_IO_SESSION_EVENT'
_IO_SESSION_EVENT__enumvalues = {
    0: 'IoSessionEventIgnore',
    1: 'IoSessionEventCreated',
    2: 'IoSessionEventTerminated',
    3: 'IoSessionEventConnected',
    4: 'IoSessionEventDisconnected',
    5: 'IoSessionEventLogon',
    6: 'IoSessionEventLogoff',
    7: 'IoSessionEventMax',
}
IoSessionEventIgnore = 0
IoSessionEventCreated = 1
IoSessionEventTerminated = 2
IoSessionEventConnected = 3
IoSessionEventDisconnected = 4
IoSessionEventLogon = 5
IoSessionEventLogoff = 6
IoSessionEventMax = 7
_IO_SESSION_EVENT = ctypes.c_uint32 # enum
IO_SESSION_EVENT = _IO_SESSION_EVENT
IO_SESSION_EVENT__enumvalues = _IO_SESSION_EVENT__enumvalues

# values for enumeration '_IO_SESSION_STATE'
_IO_SESSION_STATE__enumvalues = {
    0: 'IoSessionStateCreated',
    1: 'IoSessionStateInitialized',
    2: 'IoSessionStateConnected',
    3: 'IoSessionStateDisconnected',
    4: 'IoSessionStateDisconnectedLoggedOn',
    5: 'IoSessionStateLoggedOn',
    6: 'IoSessionStateLoggedOff',
    7: 'IoSessionStateTerminated',
    8: 'IoSessionStateMax',
}
IoSessionStateCreated = 0
IoSessionStateInitialized = 1
IoSessionStateConnected = 2
IoSessionStateDisconnected = 3
IoSessionStateDisconnectedLoggedOn = 4
IoSessionStateLoggedOn = 5
IoSessionStateLoggedOff = 6
IoSessionStateTerminated = 7
IoSessionStateMax = 8
_IO_SESSION_STATE = ctypes.c_uint32 # enum
IO_SESSION_STATE = _IO_SESSION_STATE
IO_SESSION_STATE__enumvalues = _IO_SESSION_STATE__enumvalues
class struct__PORT_MESSAGE(Structure):
    pass

PORT_MESSAGE = struct__PORT_MESSAGE
PPORT_MESSAGE = ctypes.POINTER(struct__PORT_MESSAGE)
class struct__TP_ALPC(Structure):
    pass

TP_ALPC = struct__TP_ALPC
PTP_ALPC = ctypes.POINTER(struct__TP_ALPC)
class struct__TP_CALLBACK_INSTANCE(Structure):
    pass

PTP_ALPC_CALLBACK = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct__TP_CALLBACK_INSTANCE), ctypes.POINTER(None), ctypes.POINTER(struct__TP_ALPC))
PTP_ALPC_CALLBACK_EX = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct__TP_CALLBACK_INSTANCE), ctypes.POINTER(None), ctypes.POINTER(struct__TP_ALPC), ctypes.POINTER(None))
class struct__TP_IO(Structure):
    pass

PTP_IO_CALLBACK = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct__TP_CALLBACK_INSTANCE), ctypes.POINTER(None), ctypes.POINTER(None), ctypes.POINTER(struct__IO_STATUS_BLOCK), ctypes.POINTER(struct__TP_IO))

# values for enumeration '_IO_COMPLETION_INFORMATION_CLASS'
_IO_COMPLETION_INFORMATION_CLASS__enumvalues = {
    0: 'IoCompletionBasicInformation',
}
IoCompletionBasicInformation = 0
_IO_COMPLETION_INFORMATION_CLASS = ctypes.c_uint32 # enum
IO_COMPLETION_INFORMATION_CLASS = _IO_COMPLETION_INFORMATION_CLASS
IO_COMPLETION_INFORMATION_CLASS__enumvalues = _IO_COMPLETION_INFORMATION_CLASS__enumvalues
class struct__IO_COMPLETION_BASIC_INFORMATION(Structure):
    pass

struct__IO_COMPLETION_BASIC_INFORMATION._pack_ = 1 # source:False
struct__IO_COMPLETION_BASIC_INFORMATION._fields_ = [
    ('Depth', ctypes.c_int32),
]

IO_COMPLETION_BASIC_INFORMATION = struct__IO_COMPLETION_BASIC_INFORMATION
PIO_COMPLETION_BASIC_INFORMATION = ctypes.POINTER(struct__IO_COMPLETION_BASIC_INFORMATION)

# values for enumeration '_WORKERFACTORYINFOCLASS'
_WORKERFACTORYINFOCLASS__enumvalues = {
    0: 'WorkerFactoryTimeout',
    1: 'WorkerFactoryRetryTimeout',
    2: 'WorkerFactoryIdleTimeout',
    3: 'WorkerFactoryBindingCount',
    4: 'WorkerFactoryThreadMinimum',
    5: 'WorkerFactoryThreadMaximum',
    6: 'WorkerFactoryPaused',
    7: 'WorkerFactoryBasicInformation',
    8: 'WorkerFactoryAdjustThreadGoal',
    9: 'WorkerFactoryCallbackType',
    10: 'WorkerFactoryStackInformation',
    11: 'WorkerFactoryThreadBasePriority',
    12: 'WorkerFactoryTimeoutWaiters',
    13: 'WorkerFactoryFlags',
    14: 'WorkerFactoryThreadSoftMaximum',
    15: 'MaxWorkerFactoryInfoClass',
}
WorkerFactoryTimeout = 0
WorkerFactoryRetryTimeout = 1
WorkerFactoryIdleTimeout = 2
WorkerFactoryBindingCount = 3
WorkerFactoryThreadMinimum = 4
WorkerFactoryThreadMaximum = 5
WorkerFactoryPaused = 6
WorkerFactoryBasicInformation = 7
WorkerFactoryAdjustThreadGoal = 8
WorkerFactoryCallbackType = 9
WorkerFactoryStackInformation = 10
WorkerFactoryThreadBasePriority = 11
WorkerFactoryTimeoutWaiters = 12
WorkerFactoryFlags = 13
WorkerFactoryThreadSoftMaximum = 14
MaxWorkerFactoryInfoClass = 15
_WORKERFACTORYINFOCLASS = ctypes.c_uint32 # enum
WORKERFACTORYINFOCLASS = _WORKERFACTORYINFOCLASS
WORKERFACTORYINFOCLASS__enumvalues = _WORKERFACTORYINFOCLASS__enumvalues
PWORKERFACTORYINFOCLASS = ctypes.POINTER(_WORKERFACTORYINFOCLASS)
class struct__WORKER_FACTORY_BASIC_INFORMATION(Structure):
    pass

struct__WORKER_FACTORY_BASIC_INFORMATION._pack_ = 1 # source:False
struct__WORKER_FACTORY_BASIC_INFORMATION._fields_ = [
    ('Timeout', union__LARGE_INTEGER),
    ('RetryTimeout', union__LARGE_INTEGER),
    ('IdleTimeout', union__LARGE_INTEGER),
    ('Paused', ctypes.c_ubyte),
    ('TimerSet', ctypes.c_ubyte),
    ('QueuedToExWorker', ctypes.c_ubyte),
    ('MayCreate', ctypes.c_ubyte),
    ('CreateInProgress', ctypes.c_ubyte),
    ('InsertedIntoQueue', ctypes.c_ubyte),
    ('Shutdown', ctypes.c_ubyte),
    ('PADDING_0', ctypes.c_ubyte),
    ('BindingCount', ctypes.c_uint32),
    ('ThreadMinimum', ctypes.c_uint32),
    ('ThreadMaximum', ctypes.c_uint32),
    ('PendingWorkerCount', ctypes.c_uint32),
    ('WaitingWorkerCount', ctypes.c_uint32),
    ('TotalWorkerCount', ctypes.c_uint32),
    ('ReleaseCount', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('InfiniteWaitGoal', ctypes.c_int64),
    ('StartRoutine', ctypes.POINTER(None)),
    ('StartParameter', ctypes.POINTER(None)),
    ('ProcessId', ctypes.POINTER(None)),
    ('StackReserve', ctypes.c_uint64),
    ('StackCommit', ctypes.c_uint64),
    ('LastThreadCreationStatus', ctypes.c_int32),
    ('PADDING_2', ctypes.c_ubyte * 4),
]

WORKER_FACTORY_BASIC_INFORMATION = struct__WORKER_FACTORY_BASIC_INFORMATION
PWORKER_FACTORY_BASIC_INFORMATION = ctypes.POINTER(struct__WORKER_FACTORY_BASIC_INFORMATION)
class struct__BOOT_ENTRY(Structure):
    pass

struct__BOOT_ENTRY._pack_ = 1 # source:False
struct__BOOT_ENTRY._fields_ = [
    ('Version', ctypes.c_uint32),
    ('Length', ctypes.c_uint32),
    ('Id', ctypes.c_uint32),
    ('Attributes', ctypes.c_uint32),
    ('FriendlyNameOffset', ctypes.c_uint32),
    ('BootFilePathOffset', ctypes.c_uint32),
    ('OsOptionsLength', ctypes.c_uint32),
    ('OsOptions', ctypes.c_ubyte * 1),
    ('PADDING_0', ctypes.c_ubyte * 3),
]

BOOT_ENTRY = struct__BOOT_ENTRY
PBOOT_ENTRY = ctypes.POINTER(struct__BOOT_ENTRY)
class struct__BOOT_ENTRY_LIST(Structure):
    pass

struct__BOOT_ENTRY_LIST._pack_ = 1 # source:False
struct__BOOT_ENTRY_LIST._fields_ = [
    ('NextEntryOffset', ctypes.c_uint32),
    ('BootEntry', BOOT_ENTRY),
]

BOOT_ENTRY_LIST = struct__BOOT_ENTRY_LIST
PBOOT_ENTRY_LIST = ctypes.POINTER(struct__BOOT_ENTRY_LIST)
class struct__BOOT_OPTIONS(Structure):
    pass

struct__BOOT_OPTIONS._pack_ = 1 # source:False
struct__BOOT_OPTIONS._fields_ = [
    ('Version', ctypes.c_uint32),
    ('Length', ctypes.c_uint32),
    ('Timeout', ctypes.c_uint32),
    ('CurrentBootEntryId', ctypes.c_uint32),
    ('NextBootEntryId', ctypes.c_uint32),
    ('HeadlessRedirection', ctypes.c_uint16 * 1),
    ('PADDING_0', ctypes.c_ubyte * 2),
]

BOOT_OPTIONS = struct__BOOT_OPTIONS
PBOOT_OPTIONS = ctypes.POINTER(struct__BOOT_OPTIONS)
class struct__FILE_PATH(Structure):
    pass

struct__FILE_PATH._pack_ = 1 # source:False
struct__FILE_PATH._fields_ = [
    ('Version', ctypes.c_uint32),
    ('Length', ctypes.c_uint32),
    ('Type', ctypes.c_uint32),
    ('FilePath', ctypes.c_ubyte * 1),
    ('PADDING_0', ctypes.c_ubyte * 3),
]

FILE_PATH = struct__FILE_PATH
PFILE_PATH = ctypes.POINTER(struct__FILE_PATH)
class struct__EFI_DRIVER_ENTRY(Structure):
    pass

struct__EFI_DRIVER_ENTRY._pack_ = 1 # source:False
struct__EFI_DRIVER_ENTRY._fields_ = [
    ('Version', ctypes.c_uint32),
    ('Length', ctypes.c_uint32),
    ('Id', ctypes.c_uint32),
    ('FriendlyNameOffset', ctypes.c_uint32),
    ('DriverFilePathOffset', ctypes.c_uint32),
]

EFI_DRIVER_ENTRY = struct__EFI_DRIVER_ENTRY
PEFI_DRIVER_ENTRY = ctypes.POINTER(struct__EFI_DRIVER_ENTRY)
class struct__EFI_DRIVER_ENTRY_LIST(Structure):
    pass

struct__EFI_DRIVER_ENTRY_LIST._pack_ = 1 # source:False
struct__EFI_DRIVER_ENTRY_LIST._fields_ = [
    ('NextEntryOffset', ctypes.c_uint32),
    ('DriverEntry', EFI_DRIVER_ENTRY),
]

EFI_DRIVER_ENTRY_LIST = struct__EFI_DRIVER_ENTRY_LIST
PEFI_DRIVER_ENTRY_LIST = ctypes.POINTER(struct__EFI_DRIVER_ENTRY_LIST)
PLIST_ENTRY = ctypes.POINTER(struct__LIST_ENTRY)
InitializeListHead = _libraries['FIXME_STUB'].InitializeListHead
InitializeListHead.restype = None
InitializeListHead.argtypes = [PLIST_ENTRY]
BOOLEAN = ctypes.c_ubyte
IsListEmpty = _libraries['FIXME_STUB'].IsListEmpty
IsListEmpty.restype = BOOLEAN
IsListEmpty.argtypes = [PLIST_ENTRY]
RemoveEntryList = _libraries['FIXME_STUB'].RemoveEntryList
RemoveEntryList.restype = BOOLEAN
RemoveEntryList.argtypes = [PLIST_ENTRY]
RemoveHeadList = _libraries['FIXME_STUB'].RemoveHeadList
RemoveHeadList.restype = PLIST_ENTRY
RemoveHeadList.argtypes = [PLIST_ENTRY]
RemoveTailList = _libraries['FIXME_STUB'].RemoveTailList
RemoveTailList.restype = PLIST_ENTRY
RemoveTailList.argtypes = [PLIST_ENTRY]
InsertTailList = _libraries['FIXME_STUB'].InsertTailList
InsertTailList.restype = None
InsertTailList.argtypes = [PLIST_ENTRY, PLIST_ENTRY]
InsertHeadList = _libraries['FIXME_STUB'].InsertHeadList
InsertHeadList.restype = None
InsertHeadList.argtypes = [PLIST_ENTRY, PLIST_ENTRY]
AppendTailList = _libraries['FIXME_STUB'].AppendTailList
AppendTailList.restype = None
AppendTailList.argtypes = [PLIST_ENTRY, PLIST_ENTRY]
PSINGLE_LIST_ENTRY = ctypes.POINTER(struct__SINGLE_LIST_ENTRY)
PopEntryList = _libraries['FIXME_STUB'].PopEntryList
PopEntryList.restype = PSINGLE_LIST_ENTRY
PopEntryList.argtypes = [PSINGLE_LIST_ENTRY]
PushEntryList = _libraries['FIXME_STUB'].PushEntryList
PushEntryList.restype = None
PushEntryList.argtypes = [PSINGLE_LIST_ENTRY, PSINGLE_LIST_ENTRY]
PHANDLE = ctypes.POINTER(ctypes.POINTER(None))
ACCESS_MASK = ctypes.c_uint32
HANDLE = ctypes.POINTER(None)
NtCreateProcess = _libraries['FIXME_STUB'].NtCreateProcess
NtCreateProcess.restype = NTSTATUS
NtCreateProcess.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, HANDLE, BOOLEAN, HANDLE, HANDLE, HANDLE]
ULONG = ctypes.c_uint32
NtCreateProcessEx = _libraries['FIXME_STUB'].NtCreateProcessEx
NtCreateProcessEx.restype = NTSTATUS
NtCreateProcessEx.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, HANDLE, ULONG, HANDLE, HANDLE, HANDLE, BOOLEAN]
NtCreateUserProcess = _libraries['FIXME_STUB'].NtCreateUserProcess
NtCreateUserProcess.restype = NTSTATUS
NtCreateUserProcess.argtypes = [PHANDLE, PHANDLE, ACCESS_MASK, ACCESS_MASK, POBJECT_ATTRIBUTES, POBJECT_ATTRIBUTES, ULONG, ULONG, PRTL_USER_PROCESS_PARAMETERS, PPS_CREATE_INFO, PPS_ATTRIBUTE_LIST]
PVOID = ctypes.POINTER(None)
NtSetInformationProcess = _libraries['FIXME_STUB'].NtSetInformationProcess
NtSetInformationProcess.restype = NTSTATUS
NtSetInformationProcess.argtypes = [HANDLE, PROCESSINFOCLASS, PVOID, ULONG]
PULONG = ctypes.POINTER(ctypes.c_uint32)
NtQueryInformationProcess = _libraries['FIXME_STUB'].NtQueryInformationProcess
NtQueryInformationProcess.restype = NTSTATUS
NtQueryInformationProcess.argtypes = [HANDLE, PROCESSINFOCLASS, PVOID, ULONG, PULONG]
NtQueryObject = _libraries['FIXME_STUB'].NtQueryObject
NtQueryObject.restype = NTSTATUS
NtQueryObject.argtypes = [HANDLE, OBJECT_INFORMATION_CLASS, PVOID, ULONG, PULONG]
NtQuerySystemInformation = _libraries['FIXME_STUB'].NtQuerySystemInformation
NtQuerySystemInformation.restype = NTSTATUS
NtQuerySystemInformation.argtypes = [SYSTEM_INFORMATION_CLASS, PVOID, ULONG, PULONG]
NtQuerySystemInformationEx = _libraries['FIXME_STUB'].NtQuerySystemInformationEx
NtQuerySystemInformationEx.restype = NTSTATUS
NtQuerySystemInformationEx.argtypes = [SYSTEM_INFORMATION_CLASS, PVOID, ULONG, PVOID, ULONG, PULONG]
NtSetSystemInformation = _libraries['FIXME_STUB'].NtSetSystemInformation
NtSetSystemInformation.restype = NTSTATUS
NtSetSystemInformation.argtypes = [SYSTEM_INFORMATION_CLASS, PVOID, ULONG]
NtSetInformationThread = _libraries['FIXME_STUB'].NtSetInformationThread
NtSetInformationThread.restype = NTSTATUS
NtSetInformationThread.argtypes = [HANDLE, THREADINFOCLASS, PVOID, ULONG]
NtQueryInformationThread = _libraries['FIXME_STUB'].NtQueryInformationThread
NtQueryInformationThread.restype = NTSTATUS
NtQueryInformationThread.argtypes = [HANDLE, THREADINFOCLASS, PVOID, ULONG, PULONG]
NtUnmapViewOfSection = _libraries['FIXME_STUB'].NtUnmapViewOfSection
NtUnmapViewOfSection.restype = NTSTATUS
NtUnmapViewOfSection.argtypes = [HANDLE, PVOID]
PLARGE_INTEGER = ctypes.POINTER(union__LARGE_INTEGER)
NtExtendSection = _libraries['FIXME_STUB'].NtExtendSection
NtExtendSection.restype = NTSTATUS
NtExtendSection.argtypes = [HANDLE, PLARGE_INTEGER]
NtSuspendThread = _libraries['FIXME_STUB'].NtSuspendThread
NtSuspendThread.restype = NTSTATUS
NtSuspendThread.argtypes = [HANDLE, PULONG]
NtResumeThread = _libraries['FIXME_STUB'].NtResumeThread
NtResumeThread.restype = NTSTATUS
NtResumeThread.argtypes = [HANDLE, PULONG]
NtSuspendProcess = _libraries['FIXME_STUB'].NtSuspendProcess
NtSuspendProcess.restype = NTSTATUS
NtSuspendProcess.argtypes = [HANDLE]
NtResumeProcess = _libraries['FIXME_STUB'].NtResumeProcess
NtResumeProcess.restype = NTSTATUS
NtResumeProcess.argtypes = [HANDLE]
NtGetCurrentProcessorNumber = _libraries['FIXME_STUB'].NtGetCurrentProcessorNumber
NtGetCurrentProcessorNumber.restype = ULONG
NtGetCurrentProcessorNumber.argtypes = []
NtSignalAndWaitForSingleObject = _libraries['FIXME_STUB'].NtSignalAndWaitForSingleObject
NtSignalAndWaitForSingleObject.restype = NTSTATUS
NtSignalAndWaitForSingleObject.argtypes = [HANDLE, HANDLE, BOOLEAN, PLARGE_INTEGER]
NtWaitForSingleObject = _libraries['FIXME_STUB'].NtWaitForSingleObject
NtWaitForSingleObject.restype = NTSTATUS
NtWaitForSingleObject.argtypes = [HANDLE, BOOLEAN, PLARGE_INTEGER]
NtWaitForMultipleObjects = _libraries['FIXME_STUB'].NtWaitForMultipleObjects
NtWaitForMultipleObjects.restype = NTSTATUS
NtWaitForMultipleObjects.argtypes = [ULONG, PHANDLE, WAIT_TYPE, BOOLEAN, PLARGE_INTEGER]
NtWaitForMultipleObjects32 = _libraries['FIXME_STUB'].NtWaitForMultipleObjects32
NtWaitForMultipleObjects32.restype = NTSTATUS
NtWaitForMultipleObjects32.argtypes = [ULONG, PHANDLE, WAIT_TYPE, BOOLEAN, PLARGE_INTEGER]
SECURITY_INFORMATION = ctypes.c_uint32
PSECURITY_DESCRIPTOR = ctypes.POINTER(None)
NtSetSecurityObject = _libraries['FIXME_STUB'].NtSetSecurityObject
NtSetSecurityObject.restype = NTSTATUS
NtSetSecurityObject.argtypes = [HANDLE, SECURITY_INFORMATION, PSECURITY_DESCRIPTOR]
NtQuerySecurityObject = _libraries['FIXME_STUB'].NtQuerySecurityObject
NtQuerySecurityObject.restype = NTSTATUS
NtQuerySecurityObject.argtypes = [HANDLE, SECURITY_INFORMATION, PSECURITY_DESCRIPTOR, ULONG, PULONG]
NtQueueApcThread = _libraries['FIXME_STUB'].NtQueueApcThread
NtQueueApcThread.restype = NTSTATUS
NtQueueApcThread.argtypes = [HANDLE, PPS_APC_ROUTINE, PVOID, PVOID, PVOID]
NtQueueApcThreadEx = _libraries['FIXME_STUB'].NtQueueApcThreadEx
NtQueueApcThreadEx.restype = NTSTATUS
NtQueueApcThreadEx.argtypes = [HANDLE, HANDLE, PPS_APC_ROUTINE, PVOID, PVOID, PVOID]
PSIZE_T = ctypes.POINTER(ctypes.c_uint64)
NtProtectVirtualMemory = _libraries['FIXME_STUB'].NtProtectVirtualMemory
NtProtectVirtualMemory.restype = NTSTATUS
NtProtectVirtualMemory.argtypes = [HANDLE, ctypes.POINTER(ctypes.POINTER(None)), PSIZE_T, ULONG, PULONG]
NtFlushBuffersFile = _libraries['FIXME_STUB'].NtFlushBuffersFile
NtFlushBuffersFile.restype = NTSTATUS
NtFlushBuffersFile.argtypes = [HANDLE, PIO_STATUS_BLOCK]
SIZE_T = ctypes.c_uint64
NtFlushInstructionCache = _libraries['FIXME_STUB'].NtFlushInstructionCache
NtFlushInstructionCache.restype = NTSTATUS
NtFlushInstructionCache.argtypes = [HANDLE, PVOID, SIZE_T]
NtFlushWriteBuffer = _libraries['FIXME_STUB'].NtFlushWriteBuffer
NtFlushWriteBuffer.restype = NTSTATUS
NtFlushWriteBuffer.argtypes = []
NtFsControlFile = _libraries['FIXME_STUB'].NtFsControlFile
NtFsControlFile.restype = NTSTATUS
NtFsControlFile.argtypes = [HANDLE, HANDLE, PIO_APC_ROUTINE, PVOID, PIO_STATUS_BLOCK, ULONG, PVOID, ULONG, PVOID, ULONG]
NtLockFile = _libraries['FIXME_STUB'].NtLockFile
NtLockFile.restype = NTSTATUS
NtLockFile.argtypes = [HANDLE, HANDLE, PIO_APC_ROUTINE, PVOID, PIO_STATUS_BLOCK, PLARGE_INTEGER, PLARGE_INTEGER, ULONG, BOOLEAN, BOOLEAN]
NtUnlockFile = _libraries['FIXME_STUB'].NtUnlockFile
NtUnlockFile.restype = NTSTATUS
NtUnlockFile.argtypes = [HANDLE, PIO_STATUS_BLOCK, PLARGE_INTEGER, PLARGE_INTEGER, ULONG]
NtFlushVirtualMemory = _libraries['FIXME_STUB'].NtFlushVirtualMemory
NtFlushVirtualMemory.restype = NTSTATUS
NtFlushVirtualMemory.argtypes = [HANDLE, ctypes.POINTER(ctypes.POINTER(None)), PSIZE_T, PIO_STATUS_BLOCK]
NtQueryVirtualMemory = _libraries['FIXME_STUB'].NtQueryVirtualMemory
NtQueryVirtualMemory.restype = NTSTATUS
NtQueryVirtualMemory.argtypes = [HANDLE, PVOID, MEMORY_INFORMATION_CLASS, PVOID, SIZE_T, PSIZE_T]
NtLockVirtualMemory = _libraries['FIXME_STUB'].NtLockVirtualMemory
NtLockVirtualMemory.restype = NTSTATUS
NtLockVirtualMemory.argtypes = [HANDLE, ctypes.POINTER(ctypes.POINTER(None)), PSIZE_T, ULONG]
NtUnlockVirtualMemory = _libraries['FIXME_STUB'].NtUnlockVirtualMemory
NtUnlockVirtualMemory.restype = NTSTATUS
NtUnlockVirtualMemory.argtypes = [HANDLE, ctypes.POINTER(ctypes.POINTER(None)), PSIZE_T, ULONG]
NtSystemDebugControl = _libraries['FIXME_STUB'].NtSystemDebugControl
NtSystemDebugControl.restype = NTSTATUS
NtSystemDebugControl.argtypes = [SYSDBG_COMMAND, PVOID, ULONG, PVOID, ULONG, PULONG]
NtYieldExecution = _libraries['FIXME_STUB'].NtYieldExecution
NtYieldExecution.restype = NTSTATUS
NtYieldExecution.argtypes = []
NtClose = _libraries['FIXME_STUB'].NtClose
NtClose.restype = NTSTATUS
NtClose.argtypes = [HANDLE]
NtQueryAttributesFile = _libraries['FIXME_STUB'].NtQueryAttributesFile
NtQueryAttributesFile.restype = NTSTATUS
NtQueryAttributesFile.argtypes = [POBJECT_ATTRIBUTES, PFILE_BASIC_INFORMATION]
NtQueryFullAttributesFile = _libraries['FIXME_STUB'].NtQueryFullAttributesFile
NtQueryFullAttributesFile.restype = NTSTATUS
NtQueryFullAttributesFile.argtypes = [POBJECT_ATTRIBUTES, PFILE_NETWORK_OPEN_INFORMATION]
NtQueryInformationFile = _libraries['FIXME_STUB'].NtQueryInformationFile
NtQueryInformationFile.restype = NTSTATUS
NtQueryInformationFile.argtypes = [HANDLE, PIO_STATUS_BLOCK, PVOID, ULONG, FILE_INFORMATION_CLASS]
NtSetInformationFile = _libraries['FIXME_STUB'].NtSetInformationFile
NtSetInformationFile.restype = NTSTATUS
NtSetInformationFile.argtypes = [HANDLE, PIO_STATUS_BLOCK, PVOID, ULONG, FILE_INFORMATION_CLASS]
NtSetQuotaInformationFile = _libraries['FIXME_STUB'].NtSetQuotaInformationFile
NtSetQuotaInformationFile.restype = NTSTATUS
NtSetQuotaInformationFile.argtypes = [HANDLE, PIO_STATUS_BLOCK, PVOID, ULONG]
NtSetVolumeInformationFile = _libraries['FIXME_STUB'].NtSetVolumeInformationFile
NtSetVolumeInformationFile.restype = NTSTATUS
NtSetVolumeInformationFile.argtypes = [HANDLE, PIO_STATUS_BLOCK, PVOID, ULONG, FS_INFORMATION_CLASS]
NtCreateFile = _libraries['FIXME_STUB'].NtCreateFile
NtCreateFile.restype = NTSTATUS
NtCreateFile.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, PIO_STATUS_BLOCK, PLARGE_INTEGER, ULONG, ULONG, ULONG, ULONG, PVOID, ULONG]
NtCreateNamedPipeFile = _libraries['FIXME_STUB'].NtCreateNamedPipeFile
NtCreateNamedPipeFile.restype = NTSTATUS
NtCreateNamedPipeFile.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, PIO_STATUS_BLOCK, ULONG, ULONG, ULONG, ULONG, ULONG, ULONG, ULONG, ULONG, ULONG, PLARGE_INTEGER]
NtCreateMailslotFile = _libraries['FIXME_STUB'].NtCreateMailslotFile
NtCreateMailslotFile.restype = NTSTATUS
NtCreateMailslotFile.argtypes = [PHANDLE, ULONG, POBJECT_ATTRIBUTES, PIO_STATUS_BLOCK, ULONG, ULONG, ULONG, PLARGE_INTEGER]
NtCancelIoFile = _libraries['FIXME_STUB'].NtCancelIoFile
NtCancelIoFile.restype = NTSTATUS
NtCancelIoFile.argtypes = [HANDLE, PIO_STATUS_BLOCK]
NtCancelIoFileEx = _libraries['FIXME_STUB'].NtCancelIoFileEx
NtCancelIoFileEx.restype = NTSTATUS
NtCancelIoFileEx.argtypes = [HANDLE, PIO_STATUS_BLOCK, PIO_STATUS_BLOCK]
NtCancelSynchronousIoFile = _libraries['FIXME_STUB'].NtCancelSynchronousIoFile
NtCancelSynchronousIoFile.restype = NTSTATUS
NtCancelSynchronousIoFile.argtypes = [HANDLE, PIO_STATUS_BLOCK, PIO_STATUS_BLOCK]
NtCreateSymbolicLinkObject = _libraries['FIXME_STUB'].NtCreateSymbolicLinkObject
NtCreateSymbolicLinkObject.restype = NTSTATUS
NtCreateSymbolicLinkObject.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, PUNICODE_STRING]
NtOpenSymbolicLinkObject = _libraries['FIXME_STUB'].NtOpenSymbolicLinkObject
NtOpenSymbolicLinkObject.restype = NTSTATUS
NtOpenSymbolicLinkObject.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES]
NtQuerySymbolicLinkObject = _libraries['FIXME_STUB'].NtQuerySymbolicLinkObject
NtQuerySymbolicLinkObject.restype = NTSTATUS
NtQuerySymbolicLinkObject.argtypes = [HANDLE, PUNICODE_STRING, PULONG]
PCONTEXT = ctypes.POINTER(struct__CONTEXT)
NtGetContextThread = _libraries['FIXME_STUB'].NtGetContextThread
NtGetContextThread.restype = NTSTATUS
NtGetContextThread.argtypes = [HANDLE, PCONTEXT]
NtSetContextThread = _libraries['FIXME_STUB'].NtSetContextThread
NtSetContextThread.restype = NTSTATUS
NtSetContextThread.argtypes = [HANDLE, PCONTEXT]
NtOpenProcess = _libraries['FIXME_STUB'].NtOpenProcess
NtOpenProcess.restype = NTSTATUS
NtOpenProcess.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, PCLIENT_ID]
NtTerminateProcess = _libraries['FIXME_STUB'].NtTerminateProcess
NtTerminateProcess.restype = NTSTATUS
NtTerminateProcess.argtypes = [HANDLE, NTSTATUS]
NtGetNextProcess = _libraries['FIXME_STUB'].NtGetNextProcess
NtGetNextProcess.restype = NTSTATUS
NtGetNextProcess.argtypes = [HANDLE, ACCESS_MASK, ULONG, ULONG, PHANDLE]
NtGetNextThread = _libraries['FIXME_STUB'].NtGetNextThread
NtGetNextThread.restype = NTSTATUS
NtGetNextThread.argtypes = [HANDLE, HANDLE, ACCESS_MASK, ULONG, ULONG, PHANDLE]
NtCreateDebugObject = _libraries['FIXME_STUB'].NtCreateDebugObject
NtCreateDebugObject.restype = NTSTATUS
NtCreateDebugObject.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, ULONG]
NtDebugActiveProcess = _libraries['FIXME_STUB'].NtDebugActiveProcess
NtDebugActiveProcess.restype = NTSTATUS
NtDebugActiveProcess.argtypes = [HANDLE, HANDLE]
NtContinue = _libraries['FIXME_STUB'].NtContinue
NtContinue.restype = NTSTATUS
NtContinue.argtypes = [PCONTEXT, BOOLEAN]
PEXCEPTION_RECORD = ctypes.POINTER(struct__EXCEPTION_RECORD)
NtRaiseException = _libraries['FIXME_STUB'].NtRaiseException
NtRaiseException.restype = NTSTATUS
NtRaiseException.argtypes = [PEXCEPTION_RECORD, PCONTEXT, BOOLEAN]
NtCreateThread = _libraries['FIXME_STUB'].NtCreateThread
NtCreateThread.restype = NTSTATUS
NtCreateThread.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, HANDLE, PCLIENT_ID, PCONTEXT, PINITIAL_TEB, BOOLEAN]
ULONG_PTR = ctypes.c_uint64
NtCreateThreadEx = _libraries['FIXME_STUB'].NtCreateThreadEx
NtCreateThreadEx.restype = NTSTATUS
NtCreateThreadEx.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, HANDLE, PUSER_THREAD_START_ROUTINE, PVOID, ULONG, ULONG_PTR, SIZE_T, SIZE_T, PPS_ATTRIBUTE_LIST]
NtAllocateReserveObject = _libraries['FIXME_STUB'].NtAllocateReserveObject
NtAllocateReserveObject.restype = NTSTATUS
NtAllocateReserveObject.argtypes = [PHANDLE, POBJECT_ATTRIBUTES, MEMORY_RESERVE_TYPE]
NtRegisterThreadTerminatePort = _libraries['FIXME_STUB'].NtRegisterThreadTerminatePort
NtRegisterThreadTerminatePort.restype = NTSTATUS
NtRegisterThreadTerminatePort.argtypes = [HANDLE]
PULONG_PTR = ctypes.POINTER(ctypes.c_uint64)
NtRaiseHardError = _libraries['FIXME_STUB'].NtRaiseHardError
NtRaiseHardError.restype = NTSTATUS
NtRaiseHardError.argtypes = [NTSTATUS, ULONG, ULONG, PULONG_PTR, HARDERROR_RESPONSE_OPTION, PHARDERROR_RESPONSE]
NtAllocateVirtualMemory = _libraries['FIXME_STUB'].NtAllocateVirtualMemory
NtAllocateVirtualMemory.restype = NTSTATUS
NtAllocateVirtualMemory.argtypes = [HANDLE, ctypes.POINTER(ctypes.POINTER(None)), ULONG_PTR, PSIZE_T, ULONG, ULONG]
NtFreeVirtualMemory = _libraries['FIXME_STUB'].NtFreeVirtualMemory
NtFreeVirtualMemory.restype = NTSTATUS
NtFreeVirtualMemory.argtypes = [HANDLE, ctypes.POINTER(ctypes.POINTER(None)), PSIZE_T, ULONG]
NtReadVirtualMemory = _libraries['FIXME_STUB'].NtReadVirtualMemory
NtReadVirtualMemory.restype = NTSTATUS
NtReadVirtualMemory.argtypes = [HANDLE, PVOID, PVOID, SIZE_T, PSIZE_T]
NtWriteVirtualMemory = _libraries['FIXME_STUB'].NtWriteVirtualMemory
NtWriteVirtualMemory.restype = NTSTATUS
NtWriteVirtualMemory.argtypes = [HANDLE, PVOID, ctypes.POINTER(None), SIZE_T, PSIZE_T]
NtAllocateUserPhysicalPages = _libraries['FIXME_STUB'].NtAllocateUserPhysicalPages
NtAllocateUserPhysicalPages.restype = NTSTATUS
NtAllocateUserPhysicalPages.argtypes = [HANDLE, PULONG_PTR, PULONG_PTR]
NtMapUserPhysicalPages = _libraries['FIXME_STUB'].NtMapUserPhysicalPages
NtMapUserPhysicalPages.restype = NTSTATUS
NtMapUserPhysicalPages.argtypes = [PVOID, ULONG_PTR, PULONG_PTR]
NtMapUserPhysicalPagesScatter = _libraries['FIXME_STUB'].NtMapUserPhysicalPagesScatter
NtMapUserPhysicalPagesScatter.restype = NTSTATUS
NtMapUserPhysicalPagesScatter.argtypes = [ctypes.POINTER(ctypes.POINTER(None)), ULONG_PTR, PULONG_PTR]
NtFreeUserPhysicalPages = _libraries['FIXME_STUB'].NtFreeUserPhysicalPages
NtFreeUserPhysicalPages.restype = NTSTATUS
NtFreeUserPhysicalPages.argtypes = [HANDLE, PULONG_PTR, PULONG_PTR]
NtQuerySection = _libraries['FIXME_STUB'].NtQuerySection
NtQuerySection.restype = NTSTATUS
NtQuerySection.argtypes = [HANDLE, SECTION_INFORMATION_CLASS, PVOID, SIZE_T, PSIZE_T]
NtAreMappedFilesTheSame = _libraries['FIXME_STUB'].NtAreMappedFilesTheSame
NtAreMappedFilesTheSame.restype = NTSTATUS
NtAreMappedFilesTheSame.argtypes = [PVOID, PVOID]
NtCreateSection = _libraries['FIXME_STUB'].NtCreateSection
NtCreateSection.restype = NTSTATUS
NtCreateSection.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, PLARGE_INTEGER, ULONG, ULONG, HANDLE]
NtOpenSection = _libraries['FIXME_STUB'].NtOpenSection
NtOpenSection.restype = NTSTATUS
NtOpenSection.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES]
NtMapViewOfSection = _libraries['FIXME_STUB'].NtMapViewOfSection
NtMapViewOfSection.restype = NTSTATUS
NtMapViewOfSection.argtypes = [HANDLE, HANDLE, ctypes.POINTER(ctypes.POINTER(None)), ULONG_PTR, SIZE_T, PLARGE_INTEGER, PSIZE_T, SECTION_INHERIT, ULONG, ULONG]
NtOpenSession = _libraries['FIXME_STUB'].NtOpenSession
NtOpenSession.restype = NTSTATUS
NtOpenSession.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES]
class struct__FILE_NOTIFY_INFORMATION(Structure):
    pass

struct__FILE_NOTIFY_INFORMATION._pack_ = 1 # source:False
struct__FILE_NOTIFY_INFORMATION._fields_ = [
    ('NextEntryOffset', ctypes.c_uint32),
    ('Action', ctypes.c_uint32),
    ('FileNameLength', ctypes.c_uint32),
    ('FileName', ctypes.c_uint16 * 1),
    ('PADDING_0', ctypes.c_ubyte * 2),
]

FILE_NOTIFY_INFORMATION = struct__FILE_NOTIFY_INFORMATION
NtNotifyChangeDirectoryFile = _libraries['FIXME_STUB'].NtNotifyChangeDirectoryFile
NtNotifyChangeDirectoryFile.restype = NTSTATUS
NtNotifyChangeDirectoryFile.argtypes = [HANDLE, HANDLE, PIO_APC_ROUTINE, PVOID, PIO_STATUS_BLOCK, FILE_NOTIFY_INFORMATION, ULONG, ULONG, BOOLEAN]
NtOpenFile = _libraries['FIXME_STUB'].NtOpenFile
NtOpenFile.restype = NTSTATUS
NtOpenFile.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, PIO_STATUS_BLOCK, ULONG, ULONG]
NtQueryDirectoryFile = _libraries['FIXME_STUB'].NtQueryDirectoryFile
NtQueryDirectoryFile.restype = NTSTATUS
NtQueryDirectoryFile.argtypes = [HANDLE, HANDLE, PIO_APC_ROUTINE, PVOID, PIO_STATUS_BLOCK, PVOID, ULONG, FILE_INFORMATION_CLASS, BOOLEAN, PUNICODE_STRING, BOOLEAN]
NtQueryEaFile = _libraries['FIXME_STUB'].NtQueryEaFile
NtQueryEaFile.restype = NTSTATUS
NtQueryEaFile.argtypes = [HANDLE, PIO_STATUS_BLOCK, PVOID, ULONG, BOOLEAN, PVOID, ULONG, PULONG, BOOLEAN]
NtSetEaFile = _libraries['FIXME_STUB'].NtSetEaFile
NtSetEaFile.restype = NTSTATUS
NtSetEaFile.argtypes = [HANDLE, PIO_STATUS_BLOCK, PVOID, ULONG]
NtLoadDriver = _libraries['FIXME_STUB'].NtLoadDriver
NtLoadDriver.restype = NTSTATUS
NtLoadDriver.argtypes = [PUNICODE_STRING]
NtUnloadDriver = _libraries['FIXME_STUB'].NtUnloadDriver
NtUnloadDriver.restype = NTSTATUS
NtUnloadDriver.argtypes = [PUNICODE_STRING]
NtReadFile = _libraries['FIXME_STUB'].NtReadFile
NtReadFile.restype = NTSTATUS
NtReadFile.argtypes = [HANDLE, HANDLE, PIO_APC_ROUTINE, PVOID, PIO_STATUS_BLOCK, PVOID, ULONG, PLARGE_INTEGER, PULONG]
class union__FILE_SEGMENT_ELEMENT(Union):
    pass

union__FILE_SEGMENT_ELEMENT._pack_ = 1 # source:False
union__FILE_SEGMENT_ELEMENT._fields_ = [
    ('Buffer', ctypes.POINTER(None)),
    ('Alignment', ctypes.c_uint64),
]

PFILE_SEGMENT_ELEMENT = ctypes.POINTER(union__FILE_SEGMENT_ELEMENT)
NtReadFileScatter = _libraries['FIXME_STUB'].NtReadFileScatter
NtReadFileScatter.restype = NTSTATUS
NtReadFileScatter.argtypes = [HANDLE, HANDLE, PIO_APC_ROUTINE, PVOID, PIO_STATUS_BLOCK, PFILE_SEGMENT_ELEMENT, ULONG, PLARGE_INTEGER, PULONG]
NtWriteFileGather = _libraries['FIXME_STUB'].NtWriteFileGather
NtWriteFileGather.restype = NTSTATUS
NtWriteFileGather.argtypes = [HANDLE, HANDLE, PIO_APC_ROUTINE, PVOID, PIO_STATUS_BLOCK, PFILE_SEGMENT_ELEMENT, ULONG, PLARGE_INTEGER, PULONG]
NtDeleteFile = _libraries['FIXME_STUB'].NtDeleteFile
NtDeleteFile.restype = NTSTATUS
NtDeleteFile.argtypes = [POBJECT_ATTRIBUTES]
NtWriteFile = _libraries['FIXME_STUB'].NtWriteFile
NtWriteFile.restype = NTSTATUS
NtWriteFile.argtypes = [HANDLE, HANDLE, PIO_APC_ROUTINE, PVOID, PIO_STATUS_BLOCK, PVOID, ULONG, PLARGE_INTEGER, PULONG]
NtDeviceIoControlFile = _libraries['FIXME_STUB'].NtDeviceIoControlFile
NtDeviceIoControlFile.restype = NTSTATUS
NtDeviceIoControlFile.argtypes = [HANDLE, HANDLE, PIO_APC_ROUTINE, PVOID, PIO_STATUS_BLOCK, ULONG, PVOID, ULONG, PVOID, ULONG]
NtSetInformationObject = _libraries['FIXME_STUB'].NtSetInformationObject
NtSetInformationObject.restype = NTSTATUS
NtSetInformationObject.argtypes = [HANDLE, OBJECT_INFORMATION_CLASS, PVOID, ULONG]
NtDuplicateObject = _libraries['FIXME_STUB'].NtDuplicateObject
NtDuplicateObject.restype = NTSTATUS
NtDuplicateObject.argtypes = [HANDLE, HANDLE, HANDLE, PHANDLE, ACCESS_MASK, ULONG, ULONG]
NtMakePermanentObject = _libraries['FIXME_STUB'].NtMakePermanentObject
NtMakePermanentObject.restype = NTSTATUS
NtMakePermanentObject.argtypes = [HANDLE]
NtMakeTemporaryObject = _libraries['FIXME_STUB'].NtMakeTemporaryObject
NtMakeTemporaryObject.restype = NTSTATUS
NtMakeTemporaryObject.argtypes = [HANDLE]
NtCreateDirectoryObject = _libraries['FIXME_STUB'].NtCreateDirectoryObject
NtCreateDirectoryObject.restype = NTSTATUS
NtCreateDirectoryObject.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES]
NtOpenDirectoryObject = _libraries['FIXME_STUB'].NtOpenDirectoryObject
NtOpenDirectoryObject.restype = NTSTATUS
NtOpenDirectoryObject.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES]
NtQueryDirectoryObject = _libraries['FIXME_STUB'].NtQueryDirectoryObject
NtQueryDirectoryObject.restype = NTSTATUS
NtQueryDirectoryObject.argtypes = [HANDLE, PVOID, ULONG, BOOLEAN, BOOLEAN, PULONG, PULONG]
NtCreatePrivateNamespace = _libraries['FIXME_STUB'].NtCreatePrivateNamespace
NtCreatePrivateNamespace.restype = NTSTATUS
NtCreatePrivateNamespace.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, PVOID]
NtOpenPrivateNamespace = _libraries['FIXME_STUB'].NtOpenPrivateNamespace
NtOpenPrivateNamespace.restype = NTSTATUS
NtOpenPrivateNamespace.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, PVOID]
NtDeletePrivateNamespace = _libraries['FIXME_STUB'].NtDeletePrivateNamespace
NtDeletePrivateNamespace.restype = NTSTATUS
NtDeletePrivateNamespace.argtypes = [HANDLE]
NtOpenThread = _libraries['FIXME_STUB'].NtOpenThread
NtOpenThread.restype = NTSTATUS
NtOpenThread.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, PCLIENT_ID]
NtTerminateThread = _libraries['FIXME_STUB'].NtTerminateThread
NtTerminateThread.restype = NTSTATUS
NtTerminateThread.argtypes = [HANDLE, NTSTATUS]
NtQuerySystemTime = _libraries['FIXME_STUB'].NtQuerySystemTime
NtQuerySystemTime.restype = NTSTATUS
NtQuerySystemTime.argtypes = [PLARGE_INTEGER]
NtSetSystemTime = _libraries['FIXME_STUB'].NtSetSystemTime
NtSetSystemTime.restype = NTSTATUS
NtSetSystemTime.argtypes = [PLARGE_INTEGER, PLARGE_INTEGER]
NtQueryTimerResolution = _libraries['FIXME_STUB'].NtQueryTimerResolution
NtQueryTimerResolution.restype = NTSTATUS
NtQueryTimerResolution.argtypes = [PULONG, PULONG, PULONG]
NtSetTimerResolution = _libraries['FIXME_STUB'].NtSetTimerResolution
NtSetTimerResolution.restype = NTSTATUS
NtSetTimerResolution.argtypes = [ULONG, BOOLEAN, PULONG]
NtQueryPerformanceCounter = _libraries['FIXME_STUB'].NtQueryPerformanceCounter
NtQueryPerformanceCounter.restype = NTSTATUS
NtQueryPerformanceCounter.argtypes = [PLARGE_INTEGER, PLARGE_INTEGER]
class struct__LUID(Structure):
    pass

struct__LUID._pack_ = 1 # source:False
struct__LUID._fields_ = [
    ('LowPart', ctypes.c_uint32),
    ('HighPart', ctypes.c_int32),
]

PLUID = ctypes.POINTER(struct__LUID)
NtAllocateLocallyUniqueId = _libraries['FIXME_STUB'].NtAllocateLocallyUniqueId
NtAllocateLocallyUniqueId.restype = NTSTATUS
NtAllocateLocallyUniqueId.argtypes = [PLUID]
PCHAR = ctypes.POINTER(ctypes.c_char)
NtSetUuidSeed = _libraries['FIXME_STUB'].NtSetUuidSeed
NtSetUuidSeed.restype = NTSTATUS
NtSetUuidSeed.argtypes = [PCHAR]
PULARGE_INTEGER = ctypes.POINTER(union__ULARGE_INTEGER)
NtAllocateUuids = _libraries['FIXME_STUB'].NtAllocateUuids
NtAllocateUuids.restype = NTSTATUS
NtAllocateUuids.argtypes = [PULARGE_INTEGER, PULONG, PULONG, PCHAR]
NtCreateEvent = _libraries['FIXME_STUB'].NtCreateEvent
NtCreateEvent.restype = NTSTATUS
NtCreateEvent.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, EVENT_TYPE, BOOLEAN]
NtOpenEvent = _libraries['FIXME_STUB'].NtOpenEvent
NtOpenEvent.restype = NTSTATUS
NtOpenEvent.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES]
PLONG = ctypes.POINTER(ctypes.c_int32)
NtSetEvent = _libraries['FIXME_STUB'].NtSetEvent
NtSetEvent.restype = NTSTATUS
NtSetEvent.argtypes = [HANDLE, PLONG]
NtResetEvent = _libraries['FIXME_STUB'].NtResetEvent
NtResetEvent.restype = NTSTATUS
NtResetEvent.argtypes = [HANDLE, PLONG]
NtClearEvent = _libraries['FIXME_STUB'].NtClearEvent
NtClearEvent.restype = NTSTATUS
NtClearEvent.argtypes = [HANDLE]
PSID = ctypes.POINTER(None)
NtQueryQuotaInformationFile = _libraries['FIXME_STUB'].NtQueryQuotaInformationFile
NtQueryQuotaInformationFile.restype = NTSTATUS
NtQueryQuotaInformationFile.argtypes = [HANDLE, PIO_STATUS_BLOCK, PVOID, ULONG, BOOLEAN, PVOID, ULONG, PSID, BOOLEAN]
NtQueryVolumeInformationFile = _libraries['FIXME_STUB'].NtQueryVolumeInformationFile
NtQueryVolumeInformationFile.restype = NTSTATUS
NtQueryVolumeInformationFile.argtypes = [HANDLE, PIO_STATUS_BLOCK, PVOID, ULONG, FS_INFORMATION_CLASS]
NtCreateKey = _libraries['FIXME_STUB'].NtCreateKey
NtCreateKey.restype = NTSTATUS
NtCreateKey.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, ULONG, PUNICODE_STRING, ULONG, PULONG]
NtCreateKeyTransacted = _libraries['FIXME_STUB'].NtCreateKeyTransacted
NtCreateKeyTransacted.restype = NTSTATUS
NtCreateKeyTransacted.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, ULONG, PUNICODE_STRING, ULONG, HANDLE, PULONG]
NtOpenKey = _libraries['FIXME_STUB'].NtOpenKey
NtOpenKey.restype = NTSTATUS
NtOpenKey.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES]
NtOpenKeyTransacted = _libraries['FIXME_STUB'].NtOpenKeyTransacted
NtOpenKeyTransacted.restype = NTSTATUS
NtOpenKeyTransacted.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, HANDLE]
NtOpenKeyEx = _libraries['FIXME_STUB'].NtOpenKeyEx
NtOpenKeyEx.restype = NTSTATUS
NtOpenKeyEx.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, ULONG]
NtOpenKeyTransactedEx = _libraries['FIXME_STUB'].NtOpenKeyTransactedEx
NtOpenKeyTransactedEx.restype = NTSTATUS
NtOpenKeyTransactedEx.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, ULONG, HANDLE]
NtDeleteKey = _libraries['FIXME_STUB'].NtDeleteKey
NtDeleteKey.restype = NTSTATUS
NtDeleteKey.argtypes = [HANDLE]
NtRenameKey = _libraries['FIXME_STUB'].NtRenameKey
NtRenameKey.restype = NTSTATUS
NtRenameKey.argtypes = [HANDLE, PUNICODE_STRING]
NtDeleteValueKey = _libraries['FIXME_STUB'].NtDeleteValueKey
NtDeleteValueKey.restype = NTSTATUS
NtDeleteValueKey.argtypes = [HANDLE, PUNICODE_STRING]
NtQueryKey = _libraries['FIXME_STUB'].NtQueryKey
NtQueryKey.restype = NTSTATUS
NtQueryKey.argtypes = [HANDLE, KEY_INFORMATION_CLASS, PVOID, ULONG, PULONG]
NtSetInformationKey = _libraries['FIXME_STUB'].NtSetInformationKey
NtSetInformationKey.restype = NTSTATUS
NtSetInformationKey.argtypes = [HANDLE, KEY_SET_INFORMATION_CLASS, PVOID, ULONG]
NtQueryValueKey = _libraries['FIXME_STUB'].NtQueryValueKey
NtQueryValueKey.restype = NTSTATUS
NtQueryValueKey.argtypes = [HANDLE, PUNICODE_STRING, KEY_VALUE_INFORMATION_CLASS, PVOID, ULONG, PULONG]
NtSetValueKey = _libraries['FIXME_STUB'].NtSetValueKey
NtSetValueKey.restype = NTSTATUS
NtSetValueKey.argtypes = [HANDLE, PUNICODE_STRING, ULONG, ULONG, PVOID, ULONG]
NtQueryMultipleValueKey = _libraries['FIXME_STUB'].NtQueryMultipleValueKey
NtQueryMultipleValueKey.restype = NTSTATUS
NtQueryMultipleValueKey.argtypes = [HANDLE, PKEY_VALUE_ENTRY, ULONG, PVOID, PULONG, PULONG]
NtEnumerateKey = _libraries['FIXME_STUB'].NtEnumerateKey
NtEnumerateKey.restype = NTSTATUS
NtEnumerateKey.argtypes = [HANDLE, ULONG, KEY_INFORMATION_CLASS, PVOID, ULONG, PULONG]
NtEnumerateValueKey = _libraries['FIXME_STUB'].NtEnumerateValueKey
NtEnumerateValueKey.restype = NTSTATUS
NtEnumerateValueKey.argtypes = [HANDLE, ULONG, KEY_VALUE_INFORMATION_CLASS, PVOID, ULONG, PULONG]
NtFlushKey = _libraries['FIXME_STUB'].NtFlushKey
NtFlushKey.restype = NTSTATUS
NtFlushKey.argtypes = [HANDLE]
NtCompactKeys = _libraries['FIXME_STUB'].NtCompactKeys
NtCompactKeys.restype = NTSTATUS
NtCompactKeys.argtypes = [ULONG, PHANDLE]
NtCompressKey = _libraries['FIXME_STUB'].NtCompressKey
NtCompressKey.restype = NTSTATUS
NtCompressKey.argtypes = [HANDLE]
NtLoadKey = _libraries['FIXME_STUB'].NtLoadKey
NtLoadKey.restype = NTSTATUS
NtLoadKey.argtypes = [POBJECT_ATTRIBUTES, POBJECT_ATTRIBUTES]
NtLoadKey2 = _libraries['FIXME_STUB'].NtLoadKey2
NtLoadKey2.restype = NTSTATUS
NtLoadKey2.argtypes = [POBJECT_ATTRIBUTES, POBJECT_ATTRIBUTES, ULONG]
NtLoadKeyEx = _libraries['FIXME_STUB'].NtLoadKeyEx
NtLoadKeyEx.restype = NTSTATUS
NtLoadKeyEx.argtypes = [POBJECT_ATTRIBUTES, POBJECT_ATTRIBUTES, ULONG, HANDLE, HANDLE, ACCESS_MASK, PHANDLE, PIO_STATUS_BLOCK]
NtReplaceKey = _libraries['FIXME_STUB'].NtReplaceKey
NtReplaceKey.restype = NTSTATUS
NtReplaceKey.argtypes = [POBJECT_ATTRIBUTES, HANDLE, POBJECT_ATTRIBUTES]
NtSaveKey = _libraries['FIXME_STUB'].NtSaveKey
NtSaveKey.restype = NTSTATUS
NtSaveKey.argtypes = [HANDLE, HANDLE]
NtSaveKeyEx = _libraries['FIXME_STUB'].NtSaveKeyEx
NtSaveKeyEx.restype = NTSTATUS
NtSaveKeyEx.argtypes = [HANDLE, HANDLE, ULONG]
NtSaveMergedKeys = _libraries['FIXME_STUB'].NtSaveMergedKeys
NtSaveMergedKeys.restype = NTSTATUS
NtSaveMergedKeys.argtypes = [HANDLE, HANDLE, HANDLE]
NtRestoreKey = _libraries['FIXME_STUB'].NtRestoreKey
NtRestoreKey.restype = NTSTATUS
NtRestoreKey.argtypes = [HANDLE, HANDLE, ULONG]
NtUnloadKey = _libraries['FIXME_STUB'].NtUnloadKey
NtUnloadKey.restype = NTSTATUS
NtUnloadKey.argtypes = [POBJECT_ATTRIBUTES]
NtUnloadKey2 = _libraries['FIXME_STUB'].NtUnloadKey2
NtUnloadKey2.restype = NTSTATUS
NtUnloadKey2.argtypes = [POBJECT_ATTRIBUTES, ULONG]
NtUnloadKeyEx = _libraries['FIXME_STUB'].NtUnloadKeyEx
NtUnloadKeyEx.restype = NTSTATUS
NtUnloadKeyEx.argtypes = [POBJECT_ATTRIBUTES, HANDLE]
NtNotifyChangeKey = _libraries['FIXME_STUB'].NtNotifyChangeKey
NtNotifyChangeKey.restype = NTSTATUS
NtNotifyChangeKey.argtypes = [HANDLE, HANDLE, PIO_APC_ROUTINE, PVOID, PIO_STATUS_BLOCK, ULONG, BOOLEAN, PVOID, ULONG, BOOLEAN]
NtNotifyChangeMultipleKeys = _libraries['FIXME_STUB'].NtNotifyChangeMultipleKeys
NtNotifyChangeMultipleKeys.restype = NTSTATUS
NtNotifyChangeMultipleKeys.argtypes = [HANDLE, ULONG, POBJECT_ATTRIBUTES, HANDLE, PIO_APC_ROUTINE, PVOID, PIO_STATUS_BLOCK, ULONG, BOOLEAN, PVOID, ULONG, BOOLEAN]
NtQueryOpenSubKeys = _libraries['FIXME_STUB'].NtQueryOpenSubKeys
NtQueryOpenSubKeys.restype = NTSTATUS
NtQueryOpenSubKeys.argtypes = [POBJECT_ATTRIBUTES, PULONG]
NtQueryOpenSubKeysEx = _libraries['FIXME_STUB'].NtQueryOpenSubKeysEx
NtQueryOpenSubKeysEx.restype = NTSTATUS
NtQueryOpenSubKeysEx.argtypes = [POBJECT_ATTRIBUTES, ULONG, PVOID, PULONG]
NtInitializeRegistry = _libraries['FIXME_STUB'].NtInitializeRegistry
NtInitializeRegistry.restype = NTSTATUS
NtInitializeRegistry.argtypes = [USHORT]
NtLockRegistryKey = _libraries['FIXME_STUB'].NtLockRegistryKey
NtLockRegistryKey.restype = NTSTATUS
NtLockRegistryKey.argtypes = [HANDLE]
NtLockProductActivationKeys = _libraries['FIXME_STUB'].NtLockProductActivationKeys
NtLockProductActivationKeys.restype = NTSTATUS
NtLockProductActivationKeys.argtypes = [ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint32)]
NtFreezeRegistry = _libraries['FIXME_STUB'].NtFreezeRegistry
NtFreezeRegistry.restype = NTSTATUS
NtFreezeRegistry.argtypes = [ULONG]
NtThawRegistry = _libraries['FIXME_STUB'].NtThawRegistry
NtThawRegistry.restype = NTSTATUS
NtThawRegistry.argtypes = []
NtDelayExecution = _libraries['FIXME_STUB'].NtDelayExecution
NtDelayExecution.restype = NTSTATUS
NtDelayExecution.argtypes = [BOOLEAN, PLARGE_INTEGER]
NtCallbackReturn = _libraries['FIXME_STUB'].NtCallbackReturn
NtCallbackReturn.restype = NTSTATUS
NtCallbackReturn.argtypes = [PVOID, ULONG, NTSTATUS]
NtFlushProcessWriteBuffers = _libraries['FIXME_STUB'].NtFlushProcessWriteBuffers
NtFlushProcessWriteBuffers.restype = None
NtFlushProcessWriteBuffers.argtypes = []
NtQueryDebugFilterState = _libraries['FIXME_STUB'].NtQueryDebugFilterState
NtQueryDebugFilterState.restype = NTSTATUS
NtQueryDebugFilterState.argtypes = [ULONG, ULONG]
NtSetDebugFilterState = _libraries['FIXME_STUB'].NtSetDebugFilterState
NtSetDebugFilterState.restype = NTSTATUS
NtSetDebugFilterState.argtypes = [ULONG, ULONG, BOOLEAN]
NtRemoveProcessDebug = _libraries['FIXME_STUB'].NtRemoveProcessDebug
NtRemoveProcessDebug.restype = NTSTATUS
NtRemoveProcessDebug.argtypes = [HANDLE, HANDLE]
NtWaitForDebugEvent = _libraries['FIXME_STUB'].NtWaitForDebugEvent
NtWaitForDebugEvent.restype = NTSTATUS
NtWaitForDebugEvent.argtypes = [HANDLE, BOOLEAN, PLARGE_INTEGER, PDBGUI_WAIT_STATE_CHANGE]
NtDebugContinue = _libraries['FIXME_STUB'].NtDebugContinue
NtDebugContinue.restype = NTSTATUS
NtDebugContinue.argtypes = [HANDLE, PCLIENT_ID, NTSTATUS]
NtSetInformationDebugObject = _libraries['FIXME_STUB'].NtSetInformationDebugObject
NtSetInformationDebugObject.restype = NTSTATUS
NtSetInformationDebugObject.argtypes = [HANDLE, DEBUGOBJECTINFOCLASS, PVOID, ULONG, PULONG]
NtOpenProcessToken = _libraries['FIXME_STUB'].NtOpenProcessToken
NtOpenProcessToken.restype = NTSTATUS
NtOpenProcessToken.argtypes = [HANDLE, ACCESS_MASK, PHANDLE]
NtOpenProcessTokenEx = _libraries['FIXME_STUB'].NtOpenProcessTokenEx
NtOpenProcessTokenEx.restype = NTSTATUS
NtOpenProcessTokenEx.argtypes = [HANDLE, ACCESS_MASK, ULONG, PHANDLE]
NtOpenThreadToken = _libraries['FIXME_STUB'].NtOpenThreadToken
NtOpenThreadToken.restype = NTSTATUS
NtOpenThreadToken.argtypes = [HANDLE, ACCESS_MASK, BOOLEAN, PHANDLE]
NtOpenThreadTokenEx = _libraries['FIXME_STUB'].NtOpenThreadTokenEx
NtOpenThreadTokenEx.restype = NTSTATUS
NtOpenThreadTokenEx.argtypes = [HANDLE, ACCESS_MASK, BOOLEAN, ULONG, PHANDLE]

# values for enumeration '_TOKEN_TYPE'
_TOKEN_TYPE__enumvalues = {
    1: 'TokenPrimary',
    2: 'TokenImpersonation',
}
TokenPrimary = 1
TokenImpersonation = 2
_TOKEN_TYPE = ctypes.c_uint32 # enum
TOKEN_TYPE = _TOKEN_TYPE
TOKEN_TYPE__enumvalues = _TOKEN_TYPE__enumvalues
class struct__TOKEN_USER(Structure):
    pass

class struct__SID_AND_ATTRIBUTES(Structure):
    pass

struct__SID_AND_ATTRIBUTES._pack_ = 1 # source:False
struct__SID_AND_ATTRIBUTES._fields_ = [
    ('Sid', ctypes.POINTER(None)),
    ('Attributes', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

struct__TOKEN_USER._pack_ = 1 # source:False
struct__TOKEN_USER._fields_ = [
    ('User', struct__SID_AND_ATTRIBUTES),
]

PTOKEN_USER = ctypes.POINTER(struct__TOKEN_USER)
class struct__TOKEN_GROUPS(Structure):
    pass

struct__TOKEN_GROUPS._pack_ = 1 # source:False
struct__TOKEN_GROUPS._fields_ = [
    ('GroupCount', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('Groups', struct__SID_AND_ATTRIBUTES * 1),
]

PTOKEN_GROUPS = ctypes.POINTER(struct__TOKEN_GROUPS)
class struct__TOKEN_PRIVILEGES(Structure):
    pass

class struct__LUID_AND_ATTRIBUTES(Structure):
    pass

struct__LUID_AND_ATTRIBUTES._pack_ = 1 # source:False
struct__LUID_AND_ATTRIBUTES._fields_ = [
    ('Luid', struct__LUID),
    ('Attributes', ctypes.c_uint32),
]

struct__TOKEN_PRIVILEGES._pack_ = 1 # source:False
struct__TOKEN_PRIVILEGES._fields_ = [
    ('PrivilegeCount', ctypes.c_uint32),
    ('Privileges', struct__LUID_AND_ATTRIBUTES * 1),
]

PTOKEN_PRIVILEGES = ctypes.POINTER(struct__TOKEN_PRIVILEGES)
class struct__TOKEN_OWNER(Structure):
    pass

struct__TOKEN_OWNER._pack_ = 1 # source:False
struct__TOKEN_OWNER._fields_ = [
    ('Owner', ctypes.POINTER(None)),
]

PTOKEN_OWNER = ctypes.POINTER(struct__TOKEN_OWNER)
class struct__TOKEN_PRIMARY_GROUP(Structure):
    pass

struct__TOKEN_PRIMARY_GROUP._pack_ = 1 # source:False
struct__TOKEN_PRIMARY_GROUP._fields_ = [
    ('PrimaryGroup', ctypes.POINTER(None)),
]

PTOKEN_PRIMARY_GROUP = ctypes.POINTER(struct__TOKEN_PRIMARY_GROUP)
class struct__TOKEN_DEFAULT_DACL(Structure):
    pass

class struct__ACL(Structure):
    pass

struct__TOKEN_DEFAULT_DACL._pack_ = 1 # source:False
struct__TOKEN_DEFAULT_DACL._fields_ = [
    ('DefaultDacl', ctypes.POINTER(struct__ACL)),
]

struct__ACL._pack_ = 1 # source:False
struct__ACL._fields_ = [
    ('AclRevision', ctypes.c_ubyte),
    ('Sbz1', ctypes.c_ubyte),
    ('AclSize', ctypes.c_uint16),
    ('AceCount', ctypes.c_uint16),
    ('Sbz2', ctypes.c_uint16),
]

PTOKEN_DEFAULT_DACL = ctypes.POINTER(struct__TOKEN_DEFAULT_DACL)
class struct__TOKEN_SOURCE(Structure):
    pass

struct__TOKEN_SOURCE._pack_ = 1 # source:False
struct__TOKEN_SOURCE._fields_ = [
    ('SourceName', ctypes.c_char * 8),
    ('SourceIdentifier', struct__LUID),
]

PTOKEN_SOURCE = ctypes.POINTER(struct__TOKEN_SOURCE)
NtCreateToken = _libraries['FIXME_STUB'].NtCreateToken
NtCreateToken.restype = NTSTATUS
NtCreateToken.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, TOKEN_TYPE, PLUID, PLARGE_INTEGER, PTOKEN_USER, PTOKEN_GROUPS, PTOKEN_PRIVILEGES, PTOKEN_OWNER, PTOKEN_PRIMARY_GROUP, PTOKEN_DEFAULT_DACL, PTOKEN_SOURCE]
NtDuplicateToken = _libraries['FIXME_STUB'].NtDuplicateToken
NtDuplicateToken.restype = NTSTATUS
NtDuplicateToken.argtypes = [HANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, BOOLEAN, TOKEN_TYPE, PHANDLE]
NtAdjustPrivilegesToken = _libraries['FIXME_STUB'].NtAdjustPrivilegesToken
NtAdjustPrivilegesToken.restype = NTSTATUS
NtAdjustPrivilegesToken.argtypes = [HANDLE, BOOLEAN, PTOKEN_PRIVILEGES, ULONG, PTOKEN_PRIVILEGES, PULONG]
NtAdjustGroupsToken = _libraries['FIXME_STUB'].NtAdjustGroupsToken
NtAdjustGroupsToken.restype = NTSTATUS
NtAdjustGroupsToken.argtypes = [HANDLE, BOOLEAN, PTOKEN_GROUPS, ULONG, PTOKEN_GROUPS, PULONG]
NtFilterToken = _libraries['FIXME_STUB'].NtFilterToken
NtFilterToken.restype = NTSTATUS
NtFilterToken.argtypes = [HANDLE, ULONG, PTOKEN_GROUPS, PTOKEN_PRIVILEGES, PTOKEN_GROUPS, PHANDLE]

# values for enumeration '_TOKEN_INFORMATION_CLASS'
_TOKEN_INFORMATION_CLASS__enumvalues = {
    1: 'TokenUser',
    2: 'TokenGroups',
    3: 'TokenPrivileges',
    4: 'TokenOwner',
    5: 'TokenPrimaryGroup',
    6: 'TokenDefaultDacl',
    7: 'TokenSource',
    8: 'TokenType',
    9: 'TokenImpersonationLevel',
    10: 'TokenStatistics',
    11: 'TokenRestrictedSids',
    12: 'TokenSessionId',
    13: 'TokenGroupsAndPrivileges',
    14: 'TokenSessionReference',
    15: 'TokenSandBoxInert',
    16: 'TokenAuditPolicy',
    17: 'TokenOrigin',
    18: 'TokenElevationType',
    19: 'TokenLinkedToken',
    20: 'TokenElevation',
    21: 'TokenHasRestrictions',
    22: 'TokenAccessInformation',
    23: 'TokenVirtualizationAllowed',
    24: 'TokenVirtualizationEnabled',
    25: 'TokenIntegrityLevel',
    26: 'TokenUIAccess',
    27: 'TokenMandatoryPolicy',
    28: 'TokenLogonSid',
    29: 'TokenIsAppContainer',
    30: 'TokenCapabilities',
    31: 'TokenAppContainerSid',
    32: 'TokenAppContainerNumber',
    33: 'TokenUserClaimAttributes',
    34: 'TokenDeviceClaimAttributes',
    35: 'TokenRestrictedUserClaimAttributes',
    36: 'TokenRestrictedDeviceClaimAttributes',
    37: 'TokenDeviceGroups',
    38: 'TokenRestrictedDeviceGroups',
    39: 'TokenSecurityAttributes',
    40: 'TokenIsRestricted',
    41: 'TokenProcessTrustLevel',
    42: 'TokenPrivateNameSpace',
    43: 'TokenSingletonAttributes',
    44: 'TokenBnoIsolation',
    45: 'TokenChildProcessFlags',
    46: 'TokenIsLessPrivilegedAppContainer',
    47: 'TokenIsSandboxed',
    48: 'TokenOriginatingProcessTrustLevel',
    49: 'MaxTokenInfoClass',
}
TokenUser = 1
TokenGroups = 2
TokenPrivileges = 3
TokenOwner = 4
TokenPrimaryGroup = 5
TokenDefaultDacl = 6
TokenSource = 7
TokenType = 8
TokenImpersonationLevel = 9
TokenStatistics = 10
TokenRestrictedSids = 11
TokenSessionId = 12
TokenGroupsAndPrivileges = 13
TokenSessionReference = 14
TokenSandBoxInert = 15
TokenAuditPolicy = 16
TokenOrigin = 17
TokenElevationType = 18
TokenLinkedToken = 19
TokenElevation = 20
TokenHasRestrictions = 21
TokenAccessInformation = 22
TokenVirtualizationAllowed = 23
TokenVirtualizationEnabled = 24
TokenIntegrityLevel = 25
TokenUIAccess = 26
TokenMandatoryPolicy = 27
TokenLogonSid = 28
TokenIsAppContainer = 29
TokenCapabilities = 30
TokenAppContainerSid = 31
TokenAppContainerNumber = 32
TokenUserClaimAttributes = 33
TokenDeviceClaimAttributes = 34
TokenRestrictedUserClaimAttributes = 35
TokenRestrictedDeviceClaimAttributes = 36
TokenDeviceGroups = 37
TokenRestrictedDeviceGroups = 38
TokenSecurityAttributes = 39
TokenIsRestricted = 40
TokenProcessTrustLevel = 41
TokenPrivateNameSpace = 42
TokenSingletonAttributes = 43
TokenBnoIsolation = 44
TokenChildProcessFlags = 45
TokenIsLessPrivilegedAppContainer = 46
TokenIsSandboxed = 47
TokenOriginatingProcessTrustLevel = 48
MaxTokenInfoClass = 49
_TOKEN_INFORMATION_CLASS = ctypes.c_uint32 # enum
TOKEN_INFORMATION_CLASS = _TOKEN_INFORMATION_CLASS
TOKEN_INFORMATION_CLASS__enumvalues = _TOKEN_INFORMATION_CLASS__enumvalues
NtSetInformationToken = _libraries['FIXME_STUB'].NtSetInformationToken
NtSetInformationToken.restype = NTSTATUS
NtSetInformationToken.argtypes = [HANDLE, TOKEN_INFORMATION_CLASS, PVOID, ULONG]
PBOOLEAN = ctypes.POINTER(ctypes.c_ubyte)
NtCompareTokens = _libraries['FIXME_STUB'].NtCompareTokens
NtCompareTokens.restype = NTSTATUS
NtCompareTokens.argtypes = [HANDLE, HANDLE, PBOOLEAN]
class struct__PRIVILEGE_SET(Structure):
    pass

struct__PRIVILEGE_SET._pack_ = 1 # source:False
struct__PRIVILEGE_SET._fields_ = [
    ('PrivilegeCount', ctypes.c_uint32),
    ('Control', ctypes.c_uint32),
    ('Privilege', struct__LUID_AND_ATTRIBUTES * 1),
]

PPRIVILEGE_SET = ctypes.POINTER(struct__PRIVILEGE_SET)
NtPrivilegeCheck = _libraries['FIXME_STUB'].NtPrivilegeCheck
NtPrivilegeCheck.restype = NTSTATUS
NtPrivilegeCheck.argtypes = [HANDLE, PPRIVILEGE_SET, PBOOLEAN]
NtImpersonateAnonymousToken = _libraries['FIXME_STUB'].NtImpersonateAnonymousToken
NtImpersonateAnonymousToken.restype = NTSTATUS
NtImpersonateAnonymousToken.argtypes = [HANDLE]
NtQuerySecurityAttributesToken = _libraries['FIXME_STUB'].NtQuerySecurityAttributesToken
NtQuerySecurityAttributesToken.restype = NTSTATUS
NtQuerySecurityAttributesToken.argtypes = [HANDLE, PUNICODE_STRING, ULONG, PTOKEN_SECURITY_ATTRIBUTES_INFORMATION, ULONG, PULONG]
PGENERIC_MAPPING = ctypes.POINTER(struct__GENERIC_MAPPING)
PACCESS_MASK = ctypes.POINTER(ctypes.c_uint32)
NtAccessCheck = _libraries['FIXME_STUB'].NtAccessCheck
NtAccessCheck.restype = NTSTATUS
NtAccessCheck.argtypes = [PSECURITY_DESCRIPTOR, HANDLE, ACCESS_MASK, PGENERIC_MAPPING, PPRIVILEGE_SET, PULONG, PACCESS_MASK, PNTSTATUS]
class struct__OBJECT_TYPE_LIST(Structure):
    pass

struct__OBJECT_TYPE_LIST._pack_ = 1 # source:False
struct__OBJECT_TYPE_LIST._fields_ = [
    ('Level', ctypes.c_uint16),
    ('Sbz', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('ObjectType', ctypes.POINTER(struct__GUID)),
]

POBJECT_TYPE_LIST = ctypes.POINTER(struct__OBJECT_TYPE_LIST)
NtAccessCheckByType = _libraries['FIXME_STUB'].NtAccessCheckByType
NtAccessCheckByType.restype = NTSTATUS
NtAccessCheckByType.argtypes = [PSECURITY_DESCRIPTOR, PSID, HANDLE, ACCESS_MASK, POBJECT_TYPE_LIST, ULONG, PGENERIC_MAPPING, PPRIVILEGE_SET, PULONG, PACCESS_MASK, PNTSTATUS]
NtAccessCheckByTypeResultList = _libraries['FIXME_STUB'].NtAccessCheckByTypeResultList
NtAccessCheckByTypeResultList.restype = NTSTATUS
NtAccessCheckByTypeResultList.argtypes = [PSECURITY_DESCRIPTOR, PSID, HANDLE, ACCESS_MASK, POBJECT_TYPE_LIST, ULONG, PGENERIC_MAPPING, PPRIVILEGE_SET, PULONG, PACCESS_MASK, PNTSTATUS]
NtCreateIoCompletion = _libraries['FIXME_STUB'].NtCreateIoCompletion
NtCreateIoCompletion.restype = NTSTATUS
NtCreateIoCompletion.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, ULONG]
NtOpenIoCompletion = _libraries['FIXME_STUB'].NtOpenIoCompletion
NtOpenIoCompletion.restype = NTSTATUS
NtOpenIoCompletion.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES]
NtQueryIoCompletion = _libraries['FIXME_STUB'].NtQueryIoCompletion
NtQueryIoCompletion.restype = NTSTATUS
NtQueryIoCompletion.argtypes = [HANDLE, IO_COMPLETION_INFORMATION_CLASS, PVOID, ULONG, PULONG]
NtSetIoCompletion = _libraries['FIXME_STUB'].NtSetIoCompletion
NtSetIoCompletion.restype = NTSTATUS
NtSetIoCompletion.argtypes = [HANDLE, PVOID, PVOID, NTSTATUS, ULONG_PTR]
NtSetIoCompletionEx = _libraries['FIXME_STUB'].NtSetIoCompletionEx
NtSetIoCompletionEx.restype = NTSTATUS
NtSetIoCompletionEx.argtypes = [HANDLE, HANDLE, PVOID, PVOID, NTSTATUS, ULONG_PTR]
NtRemoveIoCompletion = _libraries['FIXME_STUB'].NtRemoveIoCompletion
NtRemoveIoCompletion.restype = NTSTATUS
NtRemoveIoCompletion.argtypes = [HANDLE, ctypes.POINTER(ctypes.POINTER(None)), ctypes.POINTER(ctypes.POINTER(None)), PIO_STATUS_BLOCK, PLARGE_INTEGER]
NtRemoveIoCompletionEx = _libraries['FIXME_STUB'].NtRemoveIoCompletionEx
NtRemoveIoCompletionEx.restype = NTSTATUS
NtRemoveIoCompletionEx.argtypes = [HANDLE, PFILE_IO_COMPLETION_INFORMATION, ULONG, PULONG, PLARGE_INTEGER, BOOLEAN]
NtNotifyChangeSession = _libraries['FIXME_STUB'].NtNotifyChangeSession
NtNotifyChangeSession.restype = NTSTATUS
NtNotifyChangeSession.argtypes = [HANDLE, ULONG, PLARGE_INTEGER, IO_SESSION_EVENT, IO_SESSION_STATE, IO_SESSION_STATE, PVOID, ULONG]
NtCreateMutant = _libraries['FIXME_STUB'].NtCreateMutant
NtCreateMutant.restype = NTSTATUS
NtCreateMutant.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, BOOLEAN]
NtOpenMutant = _libraries['FIXME_STUB'].NtOpenMutant
NtOpenMutant.restype = NTSTATUS
NtOpenMutant.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES]
NtReleaseMutant = _libraries['FIXME_STUB'].NtReleaseMutant
NtReleaseMutant.restype = NTSTATUS
NtReleaseMutant.argtypes = [HANDLE, PLONG]
NtAlertThread = _libraries['FIXME_STUB'].NtAlertThread
NtAlertThread.restype = NTSTATUS
NtAlertThread.argtypes = [HANDLE]
NtAlertResumeThread = _libraries['FIXME_STUB'].NtAlertResumeThread
NtAlertResumeThread.restype = NTSTATUS
NtAlertResumeThread.argtypes = [HANDLE, PULONG]
NtTestAlert = _libraries['FIXME_STUB'].NtTestAlert
NtTestAlert.restype = NTSTATUS
NtTestAlert.argtypes = []
class struct__SECURITY_QUALITY_OF_SERVICE(Structure):
    pass


# values for enumeration '_SECURITY_IMPERSONATION_LEVEL'
_SECURITY_IMPERSONATION_LEVEL__enumvalues = {
    0: 'SecurityAnonymous',
    1: 'SecurityIdentification',
    2: 'SecurityImpersonation',
    3: 'SecurityDelegation',
}
SecurityAnonymous = 0
SecurityIdentification = 1
SecurityImpersonation = 2
SecurityDelegation = 3
_SECURITY_IMPERSONATION_LEVEL = ctypes.c_uint32 # enum
struct__SECURITY_QUALITY_OF_SERVICE._pack_ = 1 # source:False
struct__SECURITY_QUALITY_OF_SERVICE._fields_ = [
    ('Length', ctypes.c_uint32),
    ('ImpersonationLevel', _SECURITY_IMPERSONATION_LEVEL),
    ('ContextTrackingMode', ctypes.c_ubyte),
    ('EffectiveOnly', ctypes.c_ubyte),
    ('PADDING_0', ctypes.c_ubyte * 2),
]

PSECURITY_QUALITY_OF_SERVICE = ctypes.POINTER(struct__SECURITY_QUALITY_OF_SERVICE)
NtImpersonateThread = _libraries['FIXME_STUB'].NtImpersonateThread
NtImpersonateThread.restype = NTSTATUS
NtImpersonateThread.argtypes = [HANDLE, HANDLE, PSECURITY_QUALITY_OF_SERVICE]
LONG = ctypes.c_int32
NtCreateSemaphore = _libraries['FIXME_STUB'].NtCreateSemaphore
NtCreateSemaphore.restype = NTSTATUS
NtCreateSemaphore.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, LONG, LONG]
NtOpenSemaphore = _libraries['FIXME_STUB'].NtOpenSemaphore
NtOpenSemaphore.restype = NTSTATUS
NtOpenSemaphore.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES]
NtReleaseSemaphore = _libraries['FIXME_STUB'].NtReleaseSemaphore
NtReleaseSemaphore.restype = NTSTATUS
NtReleaseSemaphore.argtypes = [HANDLE, LONG, PLONG]
NtQuerySemaphore = _libraries['FIXME_STUB'].NtQuerySemaphore
NtQuerySemaphore.restype = NTSTATUS
NtQuerySemaphore.argtypes = [HANDLE, SEMAPHORE_INFORMATION_CLASS, PVOID, ULONG, PULONG]
NtCreateTimer = _libraries['FIXME_STUB'].NtCreateTimer
NtCreateTimer.restype = NTSTATUS
NtCreateTimer.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, TIMER_TYPE]
NtOpenTimer = _libraries['FIXME_STUB'].NtOpenTimer
NtOpenTimer.restype = NTSTATUS
NtOpenTimer.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES]
NtSetTimer = _libraries['FIXME_STUB'].NtSetTimer
NtSetTimer.restype = NTSTATUS
NtSetTimer.argtypes = [HANDLE, PLARGE_INTEGER, PTIMER_APC_ROUTINE, PVOID, BOOLEAN, LONG, PBOOLEAN]
NtSetTimerEx = _libraries['FIXME_STUB'].NtSetTimerEx
NtSetTimerEx.restype = NTSTATUS
NtSetTimerEx.argtypes = [HANDLE, TIMER_SET_INFORMATION_CLASS, PVOID, ULONG]
NtCancelTimer = _libraries['FIXME_STUB'].NtCancelTimer
NtCancelTimer.restype = NTSTATUS
NtCancelTimer.argtypes = [HANDLE, PBOOLEAN]
NtQueryTimer = _libraries['FIXME_STUB'].NtQueryTimer
NtQueryTimer.restype = NTSTATUS
NtQueryTimer.argtypes = [HANDLE, TIMER_INFORMATION_CLASS, PVOID, ULONG, PULONG]
NtCreateKeyedEvent = _libraries['FIXME_STUB'].NtCreateKeyedEvent
NtCreateKeyedEvent.restype = NTSTATUS
NtCreateKeyedEvent.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, ULONG]
NtOpenKeyedEvent = _libraries['FIXME_STUB'].NtOpenKeyedEvent
NtOpenKeyedEvent.restype = NTSTATUS
NtOpenKeyedEvent.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES]
NtReleaseKeyedEvent = _libraries['FIXME_STUB'].NtReleaseKeyedEvent
NtReleaseKeyedEvent.restype = NTSTATUS
NtReleaseKeyedEvent.argtypes = [HANDLE, PVOID, BOOLEAN, PLARGE_INTEGER]
NtWaitForKeyedEvent = _libraries['FIXME_STUB'].NtWaitForKeyedEvent
NtWaitForKeyedEvent.restype = NTSTATUS
NtWaitForKeyedEvent.argtypes = [HANDLE, PVOID, BOOLEAN, PLARGE_INTEGER]
NtUmsThreadYield = _libraries['FIXME_STUB'].NtUmsThreadYield
NtUmsThreadYield.restype = NTSTATUS
NtUmsThreadYield.argtypes = [PVOID]
NtCreateTransactionManager = _libraries['FIXME_STUB'].NtCreateTransactionManager
NtCreateTransactionManager.restype = NTSTATUS
NtCreateTransactionManager.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, PUNICODE_STRING, ULONG, ULONG]
LPGUID = ctypes.POINTER(struct__GUID)
NtOpenTransactionManager = _libraries['FIXME_STUB'].NtOpenTransactionManager
NtOpenTransactionManager.restype = NTSTATUS
NtOpenTransactionManager.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, PUNICODE_STRING, LPGUID, ULONG]
NtRenameTransactionManager = _libraries['FIXME_STUB'].NtRenameTransactionManager
NtRenameTransactionManager.restype = NTSTATUS
NtRenameTransactionManager.argtypes = [PUNICODE_STRING, LPGUID]
NtRollforwardTransactionManager = _libraries['FIXME_STUB'].NtRollforwardTransactionManager
NtRollforwardTransactionManager.restype = NTSTATUS
NtRollforwardTransactionManager.argtypes = [HANDLE, PLARGE_INTEGER]
NtRecoverTransactionManager = _libraries['FIXME_STUB'].NtRecoverTransactionManager
NtRecoverTransactionManager.restype = NTSTATUS
NtRecoverTransactionManager.argtypes = [HANDLE]

# values for enumeration '_TRANSACTIONMANAGER_INFORMATION_CLASS'
_TRANSACTIONMANAGER_INFORMATION_CLASS__enumvalues = {
    0: 'TransactionManagerBasicInformation',
    1: 'TransactionManagerLogInformation',
    2: 'TransactionManagerLogPathInformation',
    4: 'TransactionManagerRecoveryInformation',
    3: 'TransactionManagerOnlineProbeInformation',
    5: 'TransactionManagerOldestTransactionInformation',
}
TransactionManagerBasicInformation = 0
TransactionManagerLogInformation = 1
TransactionManagerLogPathInformation = 2
TransactionManagerRecoveryInformation = 4
TransactionManagerOnlineProbeInformation = 3
TransactionManagerOldestTransactionInformation = 5
_TRANSACTIONMANAGER_INFORMATION_CLASS = ctypes.c_uint32 # enum
TRANSACTIONMANAGER_INFORMATION_CLASS = _TRANSACTIONMANAGER_INFORMATION_CLASS
TRANSACTIONMANAGER_INFORMATION_CLASS__enumvalues = _TRANSACTIONMANAGER_INFORMATION_CLASS__enumvalues
NtQueryInformationTransactionManager = _libraries['FIXME_STUB'].NtQueryInformationTransactionManager
NtQueryInformationTransactionManager.restype = NTSTATUS
NtQueryInformationTransactionManager.argtypes = [HANDLE, TRANSACTIONMANAGER_INFORMATION_CLASS, PVOID, ULONG, PULONG]
NtSetInformationTransactionManager = _libraries['FIXME_STUB'].NtSetInformationTransactionManager
NtSetInformationTransactionManager.restype = NTSTATUS
NtSetInformationTransactionManager.argtypes = [HANDLE, TRANSACTIONMANAGER_INFORMATION_CLASS, PVOID, ULONG]

# values for enumeration '_KTMOBJECT_TYPE'
_KTMOBJECT_TYPE__enumvalues = {
    0: 'KTMOBJECT_TRANSACTION',
    1: 'KTMOBJECT_TRANSACTION_MANAGER',
    2: 'KTMOBJECT_RESOURCE_MANAGER',
    3: 'KTMOBJECT_ENLISTMENT',
    4: 'KTMOBJECT_INVALID',
}
KTMOBJECT_TRANSACTION = 0
KTMOBJECT_TRANSACTION_MANAGER = 1
KTMOBJECT_RESOURCE_MANAGER = 2
KTMOBJECT_ENLISTMENT = 3
KTMOBJECT_INVALID = 4
_KTMOBJECT_TYPE = ctypes.c_uint32 # enum
KTMOBJECT_TYPE = _KTMOBJECT_TYPE
KTMOBJECT_TYPE__enumvalues = _KTMOBJECT_TYPE__enumvalues
class struct__KTMOBJECT_CURSOR(Structure):
    pass

struct__KTMOBJECT_CURSOR._pack_ = 1 # source:False
struct__KTMOBJECT_CURSOR._fields_ = [
    ('LastQuery', struct__GUID),
    ('ObjectIdCount', ctypes.c_uint32),
    ('ObjectIds', struct__GUID * 1),
]

PKTMOBJECT_CURSOR = ctypes.POINTER(struct__KTMOBJECT_CURSOR)
NtEnumerateTransactionObject = _libraries['FIXME_STUB'].NtEnumerateTransactionObject
NtEnumerateTransactionObject.restype = NTSTATUS
NtEnumerateTransactionObject.argtypes = [HANDLE, KTMOBJECT_TYPE, PKTMOBJECT_CURSOR, ULONG, PULONG]
NtCreateTransaction = _libraries['FIXME_STUB'].NtCreateTransaction
NtCreateTransaction.restype = NTSTATUS
NtCreateTransaction.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, LPGUID, HANDLE, ULONG, ULONG, ULONG, PLARGE_INTEGER, PUNICODE_STRING]
NtOpenTransaction = _libraries['FIXME_STUB'].NtOpenTransaction
NtOpenTransaction.restype = NTSTATUS
NtOpenTransaction.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, LPGUID, HANDLE]

# values for enumeration '_TRANSACTION_INFORMATION_CLASS'
_TRANSACTION_INFORMATION_CLASS__enumvalues = {
    0: 'TransactionBasicInformation',
    1: 'TransactionPropertiesInformation',
    2: 'TransactionEnlistmentInformation',
    3: 'TransactionSuperiorEnlistmentInformation',
    4: 'TransactionBindInformation',
    5: 'TransactionDTCPrivateInformation',
}
TransactionBasicInformation = 0
TransactionPropertiesInformation = 1
TransactionEnlistmentInformation = 2
TransactionSuperiorEnlistmentInformation = 3
TransactionBindInformation = 4
TransactionDTCPrivateInformation = 5
_TRANSACTION_INFORMATION_CLASS = ctypes.c_uint32 # enum
TRANSACTION_INFORMATION_CLASS = _TRANSACTION_INFORMATION_CLASS
TRANSACTION_INFORMATION_CLASS__enumvalues = _TRANSACTION_INFORMATION_CLASS__enumvalues
NtQueryInformationTransaction = _libraries['FIXME_STUB'].NtQueryInformationTransaction
NtQueryInformationTransaction.restype = NTSTATUS
NtQueryInformationTransaction.argtypes = [HANDLE, TRANSACTION_INFORMATION_CLASS, PVOID, ULONG, PULONG]
NtSetInformationTransaction = _libraries['FIXME_STUB'].NtSetInformationTransaction
NtSetInformationTransaction.restype = NTSTATUS
NtSetInformationTransaction.argtypes = [HANDLE, TRANSACTION_INFORMATION_CLASS, PVOID, ULONG]
NtCommitTransaction = _libraries['FIXME_STUB'].NtCommitTransaction
NtCommitTransaction.restype = NTSTATUS
NtCommitTransaction.argtypes = [HANDLE, BOOLEAN]
NtRollbackTransaction = _libraries['FIXME_STUB'].NtRollbackTransaction
NtRollbackTransaction.restype = NTSTATUS
NtRollbackTransaction.argtypes = [HANDLE, BOOLEAN]
NOTIFICATION_MASK = ctypes.c_uint32
NtCreateEnlistment = _libraries['FIXME_STUB'].NtCreateEnlistment
NtCreateEnlistment.restype = NTSTATUS
NtCreateEnlistment.argtypes = [PHANDLE, ACCESS_MASK, HANDLE, HANDLE, POBJECT_ATTRIBUTES, ULONG, NOTIFICATION_MASK, PVOID]
NtOpenEnlistment = _libraries['FIXME_STUB'].NtOpenEnlistment
NtOpenEnlistment.restype = NTSTATUS
NtOpenEnlistment.argtypes = [PHANDLE, ACCESS_MASK, HANDLE, LPGUID, POBJECT_ATTRIBUTES]

# values for enumeration '_ENLISTMENT_INFORMATION_CLASS'
_ENLISTMENT_INFORMATION_CLASS__enumvalues = {
    0: 'EnlistmentBasicInformation',
    1: 'EnlistmentRecoveryInformation',
    2: 'EnlistmentCrmInformation',
}
EnlistmentBasicInformation = 0
EnlistmentRecoveryInformation = 1
EnlistmentCrmInformation = 2
_ENLISTMENT_INFORMATION_CLASS = ctypes.c_uint32 # enum
ENLISTMENT_INFORMATION_CLASS = _ENLISTMENT_INFORMATION_CLASS
ENLISTMENT_INFORMATION_CLASS__enumvalues = _ENLISTMENT_INFORMATION_CLASS__enumvalues
NtQueryInformationEnlistment = _libraries['FIXME_STUB'].NtQueryInformationEnlistment
NtQueryInformationEnlistment.restype = NTSTATUS
NtQueryInformationEnlistment.argtypes = [HANDLE, ENLISTMENT_INFORMATION_CLASS, PVOID, ULONG, PULONG]
NtSetInformationEnlistment = _libraries['FIXME_STUB'].NtSetInformationEnlistment
NtSetInformationEnlistment.restype = NTSTATUS
NtSetInformationEnlistment.argtypes = [HANDLE, ENLISTMENT_INFORMATION_CLASS, PVOID, ULONG]
NtRecoverEnlistment = _libraries['FIXME_STUB'].NtRecoverEnlistment
NtRecoverEnlistment.restype = NTSTATUS
NtRecoverEnlistment.argtypes = [HANDLE, PVOID]
NtPrePrepareEnlistment = _libraries['FIXME_STUB'].NtPrePrepareEnlistment
NtPrePrepareEnlistment.restype = NTSTATUS
NtPrePrepareEnlistment.argtypes = [HANDLE, PLARGE_INTEGER]
NtPrepareEnlistment = _libraries['FIXME_STUB'].NtPrepareEnlistment
NtPrepareEnlistment.restype = NTSTATUS
NtPrepareEnlistment.argtypes = [HANDLE, PLARGE_INTEGER]
NtCommitEnlistment = _libraries['FIXME_STUB'].NtCommitEnlistment
NtCommitEnlistment.restype = NTSTATUS
NtCommitEnlistment.argtypes = [HANDLE, PLARGE_INTEGER]
NtRollbackEnlistment = _libraries['FIXME_STUB'].NtRollbackEnlistment
NtRollbackEnlistment.restype = NTSTATUS
NtRollbackEnlistment.argtypes = [HANDLE, PLARGE_INTEGER]
NtPrePrepareComplete = _libraries['FIXME_STUB'].NtPrePrepareComplete
NtPrePrepareComplete.restype = NTSTATUS
NtPrePrepareComplete.argtypes = [HANDLE, PLARGE_INTEGER]
NtPrepareComplete = _libraries['FIXME_STUB'].NtPrepareComplete
NtPrepareComplete.restype = NTSTATUS
NtPrepareComplete.argtypes = [HANDLE, PLARGE_INTEGER]
NtCommitComplete = _libraries['FIXME_STUB'].NtCommitComplete
NtCommitComplete.restype = NTSTATUS
NtCommitComplete.argtypes = [HANDLE, PLARGE_INTEGER]
NtReadOnlyEnlistment = _libraries['FIXME_STUB'].NtReadOnlyEnlistment
NtReadOnlyEnlistment.restype = NTSTATUS
NtReadOnlyEnlistment.argtypes = [HANDLE, PLARGE_INTEGER]
NtRollbackComplete = _libraries['FIXME_STUB'].NtRollbackComplete
NtRollbackComplete.restype = NTSTATUS
NtRollbackComplete.argtypes = [HANDLE, PLARGE_INTEGER]
NtSinglePhaseReject = _libraries['FIXME_STUB'].NtSinglePhaseReject
NtSinglePhaseReject.restype = NTSTATUS
NtSinglePhaseReject.argtypes = [HANDLE, PLARGE_INTEGER]
NtCreateResourceManager = _libraries['FIXME_STUB'].NtCreateResourceManager
NtCreateResourceManager.restype = NTSTATUS
NtCreateResourceManager.argtypes = [PHANDLE, ACCESS_MASK, HANDLE, LPGUID, POBJECT_ATTRIBUTES, ULONG, PUNICODE_STRING]
NtOpenResourceManager = _libraries['FIXME_STUB'].NtOpenResourceManager
NtOpenResourceManager.restype = NTSTATUS
NtOpenResourceManager.argtypes = [PHANDLE, ACCESS_MASK, HANDLE, LPGUID, POBJECT_ATTRIBUTES]
NtRecoverResourceManager = _libraries['FIXME_STUB'].NtRecoverResourceManager
NtRecoverResourceManager.restype = NTSTATUS
NtRecoverResourceManager.argtypes = [HANDLE]
class struct__TRANSACTION_NOTIFICATION(Structure):
    pass

struct__TRANSACTION_NOTIFICATION._pack_ = 1 # source:False
struct__TRANSACTION_NOTIFICATION._fields_ = [
    ('TransactionKey', ctypes.POINTER(None)),
    ('TransactionNotification', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('TmVirtualClock', union__LARGE_INTEGER),
    ('ArgumentLength', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
]

PTRANSACTION_NOTIFICATION = ctypes.POINTER(struct__TRANSACTION_NOTIFICATION)
NtGetNotificationResourceManager = _libraries['FIXME_STUB'].NtGetNotificationResourceManager
NtGetNotificationResourceManager.restype = NTSTATUS
NtGetNotificationResourceManager.argtypes = [HANDLE, PTRANSACTION_NOTIFICATION, ULONG, PLARGE_INTEGER, PULONG, ULONG, ULONG_PTR]

# values for enumeration '_RESOURCEMANAGER_INFORMATION_CLASS'
_RESOURCEMANAGER_INFORMATION_CLASS__enumvalues = {
    0: 'ResourceManagerBasicInformation',
    1: 'ResourceManagerCompletionInformation',
}
ResourceManagerBasicInformation = 0
ResourceManagerCompletionInformation = 1
_RESOURCEMANAGER_INFORMATION_CLASS = ctypes.c_uint32 # enum
RESOURCEMANAGER_INFORMATION_CLASS = _RESOURCEMANAGER_INFORMATION_CLASS
RESOURCEMANAGER_INFORMATION_CLASS__enumvalues = _RESOURCEMANAGER_INFORMATION_CLASS__enumvalues
NtQueryInformationResourceManager = _libraries['FIXME_STUB'].NtQueryInformationResourceManager
NtQueryInformationResourceManager.restype = NTSTATUS
NtQueryInformationResourceManager.argtypes = [HANDLE, RESOURCEMANAGER_INFORMATION_CLASS, PVOID, ULONG, PULONG]
NtSetInformationResourceManager = _libraries['FIXME_STUB'].NtSetInformationResourceManager
NtSetInformationResourceManager.restype = NTSTATUS
NtSetInformationResourceManager.argtypes = [HANDLE, RESOURCEMANAGER_INFORMATION_CLASS, PVOID, ULONG]
PCRM_PROTOCOL_ID = ctypes.POINTER(struct__GUID)
NtRegisterProtocolAddressInformation = _libraries['FIXME_STUB'].NtRegisterProtocolAddressInformation
NtRegisterProtocolAddressInformation.restype = NTSTATUS
NtRegisterProtocolAddressInformation.argtypes = [HANDLE, PCRM_PROTOCOL_ID, ULONG, PVOID, ULONG]
NtPropagationComplete = _libraries['FIXME_STUB'].NtPropagationComplete
NtPropagationComplete.restype = NTSTATUS
NtPropagationComplete.argtypes = [HANDLE, ULONG, ULONG, PVOID]
NtPropagationFailed = _libraries['FIXME_STUB'].NtPropagationFailed
NtPropagationFailed.restype = NTSTATUS
NtPropagationFailed.argtypes = [HANDLE, ULONG, NTSTATUS]
NtFreezeTransactions = _libraries['FIXME_STUB'].NtFreezeTransactions
NtFreezeTransactions.restype = NTSTATUS
NtFreezeTransactions.argtypes = [PLARGE_INTEGER, PLARGE_INTEGER]
NtThawTransactions = _libraries['FIXME_STUB'].NtThawTransactions
NtThawTransactions.restype = NTSTATUS
NtThawTransactions.argtypes = []
NtCreateWorkerFactory = _libraries['FIXME_STUB'].NtCreateWorkerFactory
NtCreateWorkerFactory.restype = NTSTATUS
NtCreateWorkerFactory.argtypes = [PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, HANDLE, HANDLE, PUSER_THREAD_START_ROUTINE, PVOID, ULONG, SIZE_T, SIZE_T]
NtQueryInformationWorkerFactory = _libraries['FIXME_STUB'].NtQueryInformationWorkerFactory
NtQueryInformationWorkerFactory.restype = NTSTATUS
NtQueryInformationWorkerFactory.argtypes = [HANDLE, WORKERFACTORYINFOCLASS, PVOID, ULONG, PULONG]
NtSetInformationWorkerFactory = _libraries['FIXME_STUB'].NtSetInformationWorkerFactory
NtSetInformationWorkerFactory.restype = NTSTATUS
NtSetInformationWorkerFactory.argtypes = [HANDLE, WORKERFACTORYINFOCLASS, PVOID, ULONG]
NtShutdownWorkerFactory = _libraries['FIXME_STUB'].NtShutdownWorkerFactory
NtShutdownWorkerFactory.restype = NTSTATUS
NtShutdownWorkerFactory.argtypes = [HANDLE, ctypes.POINTER(ctypes.c_int32)]
NtReleaseWorkerFactoryWorker = _libraries['FIXME_STUB'].NtReleaseWorkerFactoryWorker
NtReleaseWorkerFactoryWorker.restype = NTSTATUS
NtReleaseWorkerFactoryWorker.argtypes = [HANDLE]
NtWorkerFactoryWorkerReady = _libraries['FIXME_STUB'].NtWorkerFactoryWorkerReady
NtWorkerFactoryWorkerReady.restype = NTSTATUS
NtWorkerFactoryWorkerReady.argtypes = [HANDLE]
NtWaitForWorkViaWorkerFactory = _libraries['FIXME_STUB'].NtWaitForWorkViaWorkerFactory
NtWaitForWorkViaWorkerFactory.restype = NTSTATUS
NtWaitForWorkViaWorkerFactory.argtypes = [HANDLE, PFILE_IO_COMPLETION_INFORMATION, ULONG, PULONG, PLARGE_INTEGER]
PWSTR = ctypes.POINTER(ctypes.c_uint16)
PUSHORT = ctypes.POINTER(ctypes.c_uint16)
NtQuerySystemEnvironmentValue = _libraries['FIXME_STUB'].NtQuerySystemEnvironmentValue
NtQuerySystemEnvironmentValue.restype = NTSTATUS
NtQuerySystemEnvironmentValue.argtypes = [PUNICODE_STRING, PWSTR, USHORT, PUSHORT]
NtSetSystemEnvironmentValue = _libraries['FIXME_STUB'].NtSetSystemEnvironmentValue
NtSetSystemEnvironmentValue.restype = NTSTATUS
NtSetSystemEnvironmentValue.argtypes = [PUNICODE_STRING, PUNICODE_STRING]
NtQuerySystemEnvironmentValueEx = _libraries['FIXME_STUB'].NtQuerySystemEnvironmentValueEx
NtQuerySystemEnvironmentValueEx.restype = NTSTATUS
NtQuerySystemEnvironmentValueEx.argtypes = [PUNICODE_STRING, LPGUID, PVOID, PULONG, PULONG]
NtSetSystemEnvironmentValueEx = _libraries['FIXME_STUB'].NtSetSystemEnvironmentValueEx
NtSetSystemEnvironmentValueEx.restype = NTSTATUS
NtSetSystemEnvironmentValueEx.argtypes = [PUNICODE_STRING, LPGUID, PVOID, ULONG, ULONG]
NtEnumerateSystemEnvironmentValuesEx = _libraries['FIXME_STUB'].NtEnumerateSystemEnvironmentValuesEx
NtEnumerateSystemEnvironmentValuesEx.restype = NTSTATUS
NtEnumerateSystemEnvironmentValuesEx.argtypes = [ULONG, PVOID, PULONG]
NtAddBootEntry = _libraries['FIXME_STUB'].NtAddBootEntry
NtAddBootEntry.restype = NTSTATUS
NtAddBootEntry.argtypes = [PBOOT_ENTRY, PULONG]
NtDeleteBootEntry = _libraries['FIXME_STUB'].NtDeleteBootEntry
NtDeleteBootEntry.restype = NTSTATUS
NtDeleteBootEntry.argtypes = [ULONG]
NtModifyBootEntry = _libraries['FIXME_STUB'].NtModifyBootEntry
NtModifyBootEntry.restype = NTSTATUS
NtModifyBootEntry.argtypes = [PBOOT_ENTRY]
NtEnumerateBootEntries = _libraries['FIXME_STUB'].NtEnumerateBootEntries
NtEnumerateBootEntries.restype = NTSTATUS
NtEnumerateBootEntries.argtypes = [PVOID, PULONG]
NtQueryBootEntryOrder = _libraries['FIXME_STUB'].NtQueryBootEntryOrder
NtQueryBootEntryOrder.restype = NTSTATUS
NtQueryBootEntryOrder.argtypes = [PULONG, PULONG]
NtSetBootEntryOrder = _libraries['FIXME_STUB'].NtSetBootEntryOrder
NtSetBootEntryOrder.restype = NTSTATUS
NtSetBootEntryOrder.argtypes = [PULONG, ULONG]
NtQueryBootOptions = _libraries['FIXME_STUB'].NtQueryBootOptions
NtQueryBootOptions.restype = NTSTATUS
NtQueryBootOptions.argtypes = [PBOOT_OPTIONS, PULONG]
NtSetBootOptions = _libraries['FIXME_STUB'].NtSetBootOptions
NtSetBootOptions.restype = NTSTATUS
NtSetBootOptions.argtypes = [PBOOT_OPTIONS, ULONG]
NtTranslateFilePath = _libraries['FIXME_STUB'].NtTranslateFilePath
NtTranslateFilePath.restype = NTSTATUS
NtTranslateFilePath.argtypes = [PFILE_PATH, ULONG, PFILE_PATH, PULONG]
NtAddDriverEntry = _libraries['FIXME_STUB'].NtAddDriverEntry
NtAddDriverEntry.restype = NTSTATUS
NtAddDriverEntry.argtypes = [PEFI_DRIVER_ENTRY, PULONG]
NtDeleteDriverEntry = _libraries['FIXME_STUB'].NtDeleteDriverEntry
NtDeleteDriverEntry.restype = NTSTATUS
NtDeleteDriverEntry.argtypes = [ULONG]
NtModifyDriverEntry = _libraries['FIXME_STUB'].NtModifyDriverEntry
NtModifyDriverEntry.restype = NTSTATUS
NtModifyDriverEntry.argtypes = [PEFI_DRIVER_ENTRY]
NtEnumerateDriverEntries = _libraries['FIXME_STUB'].NtEnumerateDriverEntries
NtEnumerateDriverEntries.restype = NTSTATUS
NtEnumerateDriverEntries.argtypes = [PVOID, PULONG]
NtQueryDriverEntryOrder = _libraries['FIXME_STUB'].NtQueryDriverEntryOrder
NtQueryDriverEntryOrder.restype = NTSTATUS
NtQueryDriverEntryOrder.argtypes = [PULONG, PULONG]
NtSetDriverEntryOrder = _libraries['FIXME_STUB'].NtSetDriverEntryOrder
NtSetDriverEntryOrder.restype = NTSTATUS
NtSetDriverEntryOrder.argtypes = [PULONG, ULONG]
NtSerializeBoot = _libraries['FIXME_STUB'].NtSerializeBoot
NtSerializeBoot.restype = NTSTATUS
NtSerializeBoot.argtypes = []
NtEnableLastKnownGood = _libraries['FIXME_STUB'].NtEnableLastKnownGood
NtEnableLastKnownGood.restype = NTSTATUS
NtEnableLastKnownGood.argtypes = []
NtDisableLastKnownGood = _libraries['FIXME_STUB'].NtDisableLastKnownGood
NtDisableLastKnownGood.restype = NTSTATUS
NtDisableLastKnownGood.argtypes = []
PCH = ctypes.POINTER(ctypes.c_char)
DbgPrint = _libraries['FIXME_STUB'].DbgPrint
DbgPrint.restype = ULONG
DbgPrint.argtypes = [PCH]
PCSTR = ctypes.POINTER(ctypes.c_char)
DbgPrintEx = _libraries['FIXME_STUB'].DbgPrintEx
DbgPrintEx.restype = ULONG
DbgPrintEx.argtypes = [ULONG, ULONG, PCSTR]
DbgBreakPoint = _libraries['FIXME_STUB'].DbgBreakPoint
DbgBreakPoint.restype = None
DbgBreakPoint.argtypes = []
DbgUiConnectToDbg = _libraries['FIXME_STUB'].DbgUiConnectToDbg
DbgUiConnectToDbg.restype = NTSTATUS
DbgUiConnectToDbg.argtypes = []
DbgUiGetThreadDebugObject = _libraries['FIXME_STUB'].DbgUiGetThreadDebugObject
DbgUiGetThreadDebugObject.restype = HANDLE
DbgUiGetThreadDebugObject.argtypes = []
DbgUiSetThreadDebugObject = _libraries['FIXME_STUB'].DbgUiSetThreadDebugObject
DbgUiSetThreadDebugObject.restype = None
DbgUiSetThreadDebugObject.argtypes = [HANDLE]
DbgUiWaitStateChange = _libraries['FIXME_STUB'].DbgUiWaitStateChange
DbgUiWaitStateChange.restype = NTSTATUS
DbgUiWaitStateChange.argtypes = [PDBGUI_WAIT_STATE_CHANGE, PLARGE_INTEGER]
DbgUiContinue = _libraries['FIXME_STUB'].DbgUiContinue
DbgUiContinue.restype = NTSTATUS
DbgUiContinue.argtypes = [PCLIENT_ID, NTSTATUS]
DbgUiStopDebugging = _libraries['FIXME_STUB'].DbgUiStopDebugging
DbgUiStopDebugging.restype = NTSTATUS
DbgUiStopDebugging.argtypes = [HANDLE]
DbgUiDebugActiveProcess = _libraries['FIXME_STUB'].DbgUiDebugActiveProcess
DbgUiDebugActiveProcess.restype = NTSTATUS
DbgUiDebugActiveProcess.argtypes = [HANDLE]
DbgUiRemoteBreakin = _libraries['FIXME_STUB'].DbgUiRemoteBreakin
DbgUiRemoteBreakin.restype = None
DbgUiRemoteBreakin.argtypes = [PVOID]
DbgUiIssueRemoteBreakin = _libraries['FIXME_STUB'].DbgUiIssueRemoteBreakin
DbgUiIssueRemoteBreakin.restype = NTSTATUS
DbgUiIssueRemoteBreakin.argtypes = [HANDLE]
class struct__DEBUG_EVENT(Structure):
    pass

class union_union_77(Union):
    pass

class struct__CREATE_THREAD_DEBUG_INFO(Structure):
    pass

struct__CREATE_THREAD_DEBUG_INFO._pack_ = 1 # source:False
struct__CREATE_THREAD_DEBUG_INFO._fields_ = [
    ('hThread', ctypes.POINTER(None)),
    ('lpThreadLocalBase', ctypes.POINTER(None)),
    ('lpStartAddress', ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(None))),
]

class struct__EXIT_PROCESS_DEBUG_INFO(Structure):
    pass

struct__EXIT_PROCESS_DEBUG_INFO._pack_ = 1 # source:False
struct__EXIT_PROCESS_DEBUG_INFO._fields_ = [
    ('dwExitCode', ctypes.c_uint32),
]

class struct__EXCEPTION_DEBUG_INFO(Structure):
    pass

struct__EXCEPTION_DEBUG_INFO._pack_ = 1 # source:False
struct__EXCEPTION_DEBUG_INFO._fields_ = [
    ('ExceptionRecord', struct__EXCEPTION_RECORD),
    ('dwFirstChance', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

class struct__UNLOAD_DLL_DEBUG_INFO(Structure):
    pass

struct__UNLOAD_DLL_DEBUG_INFO._pack_ = 1 # source:False
struct__UNLOAD_DLL_DEBUG_INFO._fields_ = [
    ('lpBaseOfDll', ctypes.POINTER(None)),
]

class struct__EXIT_THREAD_DEBUG_INFO(Structure):
    pass

struct__EXIT_THREAD_DEBUG_INFO._pack_ = 1 # source:False
struct__EXIT_THREAD_DEBUG_INFO._fields_ = [
    ('dwExitCode', ctypes.c_uint32),
]

class struct__OUTPUT_DEBUG_STRING_INFO(Structure):
    pass

struct__OUTPUT_DEBUG_STRING_INFO._pack_ = 1 # source:False
struct__OUTPUT_DEBUG_STRING_INFO._fields_ = [
    ('lpDebugStringData', ctypes.POINTER(ctypes.c_char)),
    ('fUnicode', ctypes.c_uint16),
    ('nDebugStringLength', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

class struct__RIP_INFO(Structure):
    pass

struct__RIP_INFO._pack_ = 1 # source:False
struct__RIP_INFO._fields_ = [
    ('dwError', ctypes.c_uint32),
    ('dwType', ctypes.c_uint32),
]

class struct__LOAD_DLL_DEBUG_INFO(Structure):
    pass

struct__LOAD_DLL_DEBUG_INFO._pack_ = 1 # source:False
struct__LOAD_DLL_DEBUG_INFO._fields_ = [
    ('hFile', ctypes.POINTER(None)),
    ('lpBaseOfDll', ctypes.POINTER(None)),
    ('dwDebugInfoFileOffset', ctypes.c_uint32),
    ('nDebugInfoSize', ctypes.c_uint32),
    ('lpImageName', ctypes.POINTER(None)),
    ('fUnicode', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 6),
]

class struct__CREATE_PROCESS_DEBUG_INFO(Structure):
    pass

struct__CREATE_PROCESS_DEBUG_INFO._pack_ = 1 # source:False
struct__CREATE_PROCESS_DEBUG_INFO._fields_ = [
    ('hFile', ctypes.POINTER(None)),
    ('hProcess', ctypes.POINTER(None)),
    ('hThread', ctypes.POINTER(None)),
    ('lpBaseOfImage', ctypes.POINTER(None)),
    ('dwDebugInfoFileOffset', ctypes.c_uint32),
    ('nDebugInfoSize', ctypes.c_uint32),
    ('lpThreadLocalBase', ctypes.POINTER(None)),
    ('lpStartAddress', ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(None))),
    ('lpImageName', ctypes.POINTER(None)),
    ('fUnicode', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 6),
]

union_union_77._pack_ = 1 # source:False
union_union_77._fields_ = [
    ('Exception', struct__EXCEPTION_DEBUG_INFO),
    ('CreateThread', struct__CREATE_THREAD_DEBUG_INFO),
    ('CreateProcessInfo', struct__CREATE_PROCESS_DEBUG_INFO),
    ('ExitThread', struct__EXIT_THREAD_DEBUG_INFO),
    ('ExitProcess', struct__EXIT_PROCESS_DEBUG_INFO),
    ('LoadDll', struct__LOAD_DLL_DEBUG_INFO),
    ('UnloadDll', struct__UNLOAD_DLL_DEBUG_INFO),
    ('DebugString', struct__OUTPUT_DEBUG_STRING_INFO),
    ('RipInfo', struct__RIP_INFO),
    ('PADDING_0', ctypes.c_ubyte * 152),
]

struct__DEBUG_EVENT._pack_ = 1 # source:False
struct__DEBUG_EVENT._fields_ = [
    ('dwDebugEventCode', ctypes.c_uint32),
    ('dwProcessId', ctypes.c_uint32),
    ('dwThreadId', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('u', union_union_77),
]

DbgUiConvertStateChangeStructure = _libraries['FIXME_STUB'].DbgUiConvertStateChangeStructure
DbgUiConvertStateChangeStructure.restype = NTSTATUS
DbgUiConvertStateChangeStructure.argtypes = [PDBGUI_WAIT_STATE_CHANGE, ctypes.POINTER(struct__DEBUG_EVENT)]
PCWSTR = ctypes.POINTER(ctypes.c_uint16)
LdrLoadDll = _libraries['FIXME_STUB'].LdrLoadDll
LdrLoadDll.restype = NTSTATUS
LdrLoadDll.argtypes = [PCWSTR, PULONG, PUNICODE_STRING, ctypes.POINTER(ctypes.POINTER(None))]
LdrGetDllHandle = _libraries['FIXME_STUB'].LdrGetDllHandle
LdrGetDllHandle.restype = NTSTATUS
LdrGetDllHandle.argtypes = [PCWSTR, PULONG, PUNICODE_STRING, ctypes.POINTER(ctypes.POINTER(None))]
LdrGetDllHandleEx = _libraries['FIXME_STUB'].LdrGetDllHandleEx
LdrGetDllHandleEx.restype = NTSTATUS
LdrGetDllHandleEx.argtypes = [ULONG, PCWSTR, PULONG, PUNICODE_STRING, ctypes.POINTER(ctypes.POINTER(None))]
LdrGetDllHandleByMapping = _libraries['FIXME_STUB'].LdrGetDllHandleByMapping
LdrGetDllHandleByMapping.restype = NTSTATUS
LdrGetDllHandleByMapping.argtypes = [PVOID, ctypes.POINTER(ctypes.POINTER(None))]
LdrGetDllHandleByName = _libraries['FIXME_STUB'].LdrGetDllHandleByName
LdrGetDllHandleByName.restype = NTSTATUS
LdrGetDllHandleByName.argtypes = [PUNICODE_STRING, PUNICODE_STRING, ctypes.POINTER(ctypes.POINTER(None))]
LdrGetProcedureAddress = _libraries['FIXME_STUB'].LdrGetProcedureAddress
LdrGetProcedureAddress.restype = NTSTATUS
LdrGetProcedureAddress.argtypes = [PVOID, PANSI_STRING, ULONG, ctypes.POINTER(ctypes.POINTER(None))]
LdrGetProcedureAddressEx = _libraries['FIXME_STUB'].LdrGetProcedureAddressEx
LdrGetProcedureAddressEx.restype = NTSTATUS
LdrGetProcedureAddressEx.argtypes = [PVOID, PANSI_STRING, ULONG, ctypes.POINTER(ctypes.POINTER(None)), ULONG]
LdrLockLoaderLock = _libraries['FIXME_STUB'].LdrLockLoaderLock
LdrLockLoaderLock.restype = NTSTATUS
LdrLockLoaderLock.argtypes = [ULONG, ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.POINTER(None))]
LdrUnlockLoaderLock = _libraries['FIXME_STUB'].LdrUnlockLoaderLock
LdrUnlockLoaderLock.restype = NTSTATUS
LdrUnlockLoaderLock.argtypes = [ULONG, PVOID]
class struct__IMAGE_BASE_RELOCATION(Structure):
    pass

struct__IMAGE_BASE_RELOCATION._pack_ = 1 # source:False
struct__IMAGE_BASE_RELOCATION._fields_ = [
    ('VirtualAddress', ctypes.c_uint32),
    ('SizeOfBlock', ctypes.c_uint32),
]

PIMAGE_BASE_RELOCATION = ctypes.POINTER(struct__IMAGE_BASE_RELOCATION)
LONG_PTR = ctypes.c_int64
LdrProcessRelocationBlock = _libraries['FIXME_STUB'].LdrProcessRelocationBlock
LdrProcessRelocationBlock.restype = PIMAGE_BASE_RELOCATION
LdrProcessRelocationBlock.argtypes = [ULONG_PTR, ULONG, PUSHORT, LONG_PTR]
LdrUnloadDll = _libraries['FIXME_STUB'].LdrUnloadDll
LdrUnloadDll.restype = NTSTATUS
LdrUnloadDll.argtypes = [PVOID]
LdrDisableThreadCalloutsForDll = _libraries['FIXME_STUB'].LdrDisableThreadCalloutsForDll
LdrDisableThreadCalloutsForDll.restype = NTSTATUS
LdrDisableThreadCalloutsForDll.argtypes = [PVOID]
LdrOpenImageFileOptionsKey = _libraries['FIXME_STUB'].LdrOpenImageFileOptionsKey
LdrOpenImageFileOptionsKey.restype = NTSTATUS
LdrOpenImageFileOptionsKey.argtypes = [PUNICODE_STRING, BOOLEAN, PHANDLE]
LdrQueryImageFileKeyOption = _libraries['FIXME_STUB'].LdrQueryImageFileKeyOption
LdrQueryImageFileKeyOption.restype = NTSTATUS
LdrQueryImageFileKeyOption.argtypes = [HANDLE, PCWSTR, ULONG, PVOID, ULONG, PULONG]
LdrVerifyImageMatchesChecksum = _libraries['FIXME_STUB'].LdrVerifyImageMatchesChecksum
LdrVerifyImageMatchesChecksum.restype = NTSTATUS
LdrVerifyImageMatchesChecksum.argtypes = [HANDLE, PLDR_IMPORT_MODULE_CALLBACK, PVOID, PUSHORT]
LdrVerifyImageMatchesChecksumEx = _libraries['FIXME_STUB'].LdrVerifyImageMatchesChecksumEx
LdrVerifyImageMatchesChecksumEx.restype = NTSTATUS
LdrVerifyImageMatchesChecksumEx.argtypes = [HANDLE, PLDR_VERIFY_IMAGE_INFO]
class struct__IMAGE_RESOURCE_DIRECTORY(Structure):
    pass

struct__IMAGE_RESOURCE_DIRECTORY._pack_ = 1 # source:False
struct__IMAGE_RESOURCE_DIRECTORY._fields_ = [
    ('Characteristics', ctypes.c_uint32),
    ('TimeDateStamp', ctypes.c_uint32),
    ('MajorVersion', ctypes.c_uint16),
    ('MinorVersion', ctypes.c_uint16),
    ('NumberOfNamedEntries', ctypes.c_uint16),
    ('NumberOfIdEntries', ctypes.c_uint16),
]

LdrFindResourceDirectory_U = _libraries['FIXME_STUB'].LdrFindResourceDirectory_U
LdrFindResourceDirectory_U.restype = NTSTATUS
LdrFindResourceDirectory_U.argtypes = [PVOID, ctypes.POINTER(struct__LDR_RESOURCE_INFO), ULONG, ctypes.POINTER(ctypes.POINTER(struct__IMAGE_RESOURCE_DIRECTORY))]
class struct__IMAGE_RESOURCE_DATA_ENTRY(Structure):
    pass

struct__IMAGE_RESOURCE_DATA_ENTRY._pack_ = 1 # source:False
struct__IMAGE_RESOURCE_DATA_ENTRY._fields_ = [
    ('OffsetToData', ctypes.c_uint32),
    ('Size', ctypes.c_uint32),
    ('CodePage', ctypes.c_uint32),
    ('Reserved', ctypes.c_uint32),
]

LdrFindResource_U = _libraries['FIXME_STUB'].LdrFindResource_U
LdrFindResource_U.restype = NTSTATUS
LdrFindResource_U.argtypes = [PVOID, ctypes.POINTER(struct__LDR_RESOURCE_INFO), ULONG, ctypes.POINTER(ctypes.POINTER(struct__IMAGE_RESOURCE_DATA_ENTRY))]
LdrFindResourceEx_U = _libraries['FIXME_STUB'].LdrFindResourceEx_U
LdrFindResourceEx_U.restype = NTSTATUS
LdrFindResourceEx_U.argtypes = [ULONG, PVOID, ctypes.POINTER(struct__LDR_RESOURCE_INFO), ULONG, ctypes.POINTER(ctypes.POINTER(struct__IMAGE_RESOURCE_DATA_ENTRY))]
PSTR = ctypes.POINTER(ctypes.c_char)
RtlAssert = _libraries['FIXME_STUB'].RtlAssert
RtlAssert.restype = None
RtlAssert.argtypes = [PVOID, PVOID, ULONG, PSTR]
RtlRaiseStatus = _libraries['FIXME_STUB'].RtlRaiseStatus
RtlRaiseStatus.restype = None
RtlRaiseStatus.argtypes = [NTSTATUS]
RtlRaiseException = _libraries['FIXME_STUB'].RtlRaiseException
RtlRaiseException.restype = None
RtlRaiseException.argtypes = [PEXCEPTION_RECORD]
DWORD = ctypes.c_uint32
RtlConnectToSm = _libraries['FIXME_STUB'].RtlConnectToSm
RtlConnectToSm.restype = NTSTATUS
RtlConnectToSm.argtypes = [PUNICODE_STRING, HANDLE, DWORD, PHANDLE]
RtlSendMsgToSm = _libraries['FIXME_STUB'].RtlSendMsgToSm
RtlSendMsgToSm.restype = NTSTATUS
RtlSendMsgToSm.argtypes = [HANDLE, PPORT_MESSAGE]
RtlRegisterThreadWithCsrss = _libraries['FIXME_STUB'].RtlRegisterThreadWithCsrss
RtlRegisterThreadWithCsrss.restype = NTSTATUS
RtlRegisterThreadWithCsrss.argtypes = []
PRTL_CRITICAL_SECTION = ctypes.POINTER(struct__RTL_CRITICAL_SECTION)
RtlEnterCriticalSection = _libraries['FIXME_STUB'].RtlEnterCriticalSection
RtlEnterCriticalSection.restype = NTSTATUS
RtlEnterCriticalSection.argtypes = [PRTL_CRITICAL_SECTION]
RtlLeaveCriticalSection = _libraries['FIXME_STUB'].RtlLeaveCriticalSection
RtlLeaveCriticalSection.restype = NTSTATUS
RtlLeaveCriticalSection.argtypes = [PRTL_CRITICAL_SECTION]
RtlIsCriticalSectionLocked = _libraries['FIXME_STUB'].RtlIsCriticalSectionLocked
RtlIsCriticalSectionLocked.restype = LOGICAL
RtlIsCriticalSectionLocked.argtypes = [PRTL_CRITICAL_SECTION]
RtlIsCriticalSectionLockedByThread = _libraries['FIXME_STUB'].RtlIsCriticalSectionLockedByThread
RtlIsCriticalSectionLockedByThread.restype = LOGICAL
RtlIsCriticalSectionLockedByThread.argtypes = [PRTL_CRITICAL_SECTION]
RtlGetCriticalSectionRecursionCount = _libraries['FIXME_STUB'].RtlGetCriticalSectionRecursionCount
RtlGetCriticalSectionRecursionCount.restype = ULONG
RtlGetCriticalSectionRecursionCount.argtypes = [PRTL_CRITICAL_SECTION]
RtlTryEnterCriticalSection = _libraries['FIXME_STUB'].RtlTryEnterCriticalSection
RtlTryEnterCriticalSection.restype = LOGICAL
RtlTryEnterCriticalSection.argtypes = [PRTL_CRITICAL_SECTION]
RtlInitializeCriticalSection = _libraries['FIXME_STUB'].RtlInitializeCriticalSection
RtlInitializeCriticalSection.restype = NTSTATUS
RtlInitializeCriticalSection.argtypes = [PRTL_CRITICAL_SECTION]
RtlEnableEarlyCriticalSectionEventCreation = _libraries['FIXME_STUB'].RtlEnableEarlyCriticalSectionEventCreation
RtlEnableEarlyCriticalSectionEventCreation.restype = None
RtlEnableEarlyCriticalSectionEventCreation.argtypes = []
RtlInitializeCriticalSectionAndSpinCount = _libraries['FIXME_STUB'].RtlInitializeCriticalSectionAndSpinCount
RtlInitializeCriticalSectionAndSpinCount.restype = NTSTATUS
RtlInitializeCriticalSectionAndSpinCount.argtypes = [PRTL_CRITICAL_SECTION, ULONG]
RtlSetCriticalSectionSpinCount = _libraries['FIXME_STUB'].RtlSetCriticalSectionSpinCount
RtlSetCriticalSectionSpinCount.restype = ULONG
RtlSetCriticalSectionSpinCount.argtypes = [PRTL_CRITICAL_SECTION, ULONG]
RtlDeleteCriticalSection = _libraries['FIXME_STUB'].RtlDeleteCriticalSection
RtlDeleteCriticalSection.restype = NTSTATUS
RtlDeleteCriticalSection.argtypes = [PRTL_CRITICAL_SECTION]
BOOL = ctypes.c_int32
RtlQueryPerformanceFrequency = _libraries['FIXME_STUB'].RtlQueryPerformanceFrequency
RtlQueryPerformanceFrequency.restype = BOOL
RtlQueryPerformanceFrequency.argtypes = [PLARGE_INTEGER]
RtlQueryPerformanceCounter = _libraries['FIXME_STUB'].RtlQueryPerformanceCounter
RtlQueryPerformanceCounter.restype = BOOL
RtlQueryPerformanceCounter.argtypes = [PLARGE_INTEGER]
RtlGetCompressionWorkSpaceSize = _libraries['FIXME_STUB'].RtlGetCompressionWorkSpaceSize
RtlGetCompressionWorkSpaceSize.restype = NTSTATUS
RtlGetCompressionWorkSpaceSize.argtypes = [USHORT, PULONG, PULONG]
PUCHAR = ctypes.POINTER(ctypes.c_ubyte)
RtlCompressBuffer = _libraries['FIXME_STUB'].RtlCompressBuffer
RtlCompressBuffer.restype = NTSTATUS
RtlCompressBuffer.argtypes = [USHORT, PUCHAR, ULONG, PUCHAR, ULONG, ULONG, PULONG, PVOID]
RtlDecompressBuffer = _libraries['FIXME_STUB'].RtlDecompressBuffer
RtlDecompressBuffer.restype = NTSTATUS
RtlDecompressBuffer.argtypes = [USHORT, PUCHAR, ULONG, PUCHAR, ULONG, PULONG]
RtlCreateHeap = _libraries['FIXME_STUB'].RtlCreateHeap
RtlCreateHeap.restype = PVOID
RtlCreateHeap.argtypes = [ULONG, PVOID, SIZE_T, SIZE_T, PVOID, PRTL_HEAP_PARAMETERS]
RtlDestroyHeap = _libraries['FIXME_STUB'].RtlDestroyHeap
RtlDestroyHeap.restype = PVOID
RtlDestroyHeap.argtypes = [PVOID]
RtlAllocateHeap = _libraries['FIXME_STUB'].RtlAllocateHeap
RtlAllocateHeap.restype = PVOID
RtlAllocateHeap.argtypes = [PVOID, ULONG, SIZE_T]
RtlFreeHeap = _libraries['FIXME_STUB'].RtlFreeHeap
RtlFreeHeap.restype = BOOLEAN
RtlFreeHeap.argtypes = [PVOID, ULONG, PVOID]
RtlWalkHeap = _libraries['FIXME_STUB'].RtlWalkHeap
RtlWalkHeap.restype = NTSTATUS
RtlWalkHeap.argtypes = [PVOID, PRTL_HEAP_WALK_ENTRY]

# values for enumeration '_HEAP_INFORMATION_CLASS'
_HEAP_INFORMATION_CLASS__enumvalues = {
    0: 'HeapCompatibilityInformation',
    1: 'HeapEnableTerminationOnCorruption',
    3: 'HeapOptimizeResources',
}
HeapCompatibilityInformation = 0
HeapEnableTerminationOnCorruption = 1
HeapOptimizeResources = 3
_HEAP_INFORMATION_CLASS = ctypes.c_uint32 # enum
HEAP_INFORMATION_CLASS = _HEAP_INFORMATION_CLASS
HEAP_INFORMATION_CLASS__enumvalues = _HEAP_INFORMATION_CLASS__enumvalues
RtlQueryHeapInformation = _libraries['FIXME_STUB'].RtlQueryHeapInformation
RtlQueryHeapInformation.restype = NTSTATUS
RtlQueryHeapInformation.argtypes = [PVOID, HEAP_INFORMATION_CLASS, PVOID, SIZE_T, PSIZE_T]
RtlSetHeapInformation = _libraries['FIXME_STUB'].RtlSetHeapInformation
RtlSetHeapInformation.restype = NTSTATUS
RtlSetHeapInformation.argtypes = [PVOID, HEAP_INFORMATION_CLASS, PVOID, SIZE_T]
RtlSizeHeap = _libraries['FIXME_STUB'].RtlSizeHeap
RtlSizeHeap.restype = SIZE_T
RtlSizeHeap.argtypes = [PVOID, ULONG, PVOID]
RtlZeroHeap = _libraries['FIXME_STUB'].RtlZeroHeap
RtlZeroHeap.restype = NTSTATUS
RtlZeroHeap.argtypes = [PVOID, ULONG]
RtlProtectHeap = _libraries['FIXME_STUB'].RtlProtectHeap
RtlProtectHeap.restype = None
RtlProtectHeap.argtypes = [PVOID, BOOLEAN]
RtlLockHeap = _libraries['FIXME_STUB'].RtlLockHeap
RtlLockHeap.restype = BOOLEAN
RtlLockHeap.argtypes = [PVOID]
RtlUnlockHeap = _libraries['FIXME_STUB'].RtlUnlockHeap
RtlUnlockHeap.restype = BOOLEAN
RtlUnlockHeap.argtypes = [PVOID]
RtlReAllocateHeap = _libraries['FIXME_STUB'].RtlReAllocateHeap
RtlReAllocateHeap.restype = PVOID
RtlReAllocateHeap.argtypes = [PVOID, ULONG, PVOID, SIZE_T]
RtlGetUserInfoHeap = _libraries['FIXME_STUB'].RtlGetUserInfoHeap
RtlGetUserInfoHeap.restype = BOOLEAN
RtlGetUserInfoHeap.argtypes = [PVOID, ULONG, PVOID, ctypes.POINTER(ctypes.POINTER(None)), PULONG]
RtlSetUserValueHeap = _libraries['FIXME_STUB'].RtlSetUserValueHeap
RtlSetUserValueHeap.restype = BOOLEAN
RtlSetUserValueHeap.argtypes = [PVOID, ULONG, PVOID, PVOID]
RtlSetUserFlagsHeap = _libraries['FIXME_STUB'].RtlSetUserFlagsHeap
RtlSetUserFlagsHeap.restype = BOOLEAN
RtlSetUserFlagsHeap.argtypes = [PVOID, ULONG, PVOID, ULONG, ULONG]
RtlCreateTagHeap = _libraries['FIXME_STUB'].RtlCreateTagHeap
RtlCreateTagHeap.restype = ULONG
RtlCreateTagHeap.argtypes = [PVOID, ULONG, PWSTR, PWSTR]
RtlQueryTagHeap = _libraries['FIXME_STUB'].RtlQueryTagHeap
RtlQueryTagHeap.restype = PWSTR
RtlQueryTagHeap.argtypes = [PVOID, ULONG, USHORT, BOOLEAN, PRTL_HEAP_TAG_INFO]
RtlCompactHeap = _libraries['FIXME_STUB'].RtlCompactHeap
RtlCompactHeap.restype = SIZE_T
RtlCompactHeap.argtypes = [PVOID, ULONG]
RtlValidateHeap = _libraries['FIXME_STUB'].RtlValidateHeap
RtlValidateHeap.restype = BOOLEAN
RtlValidateHeap.argtypes = [PVOID, ULONG, PVOID]
RtlValidateProcessHeaps = _libraries['FIXME_STUB'].RtlValidateProcessHeaps
RtlValidateProcessHeaps.restype = BOOLEAN
RtlValidateProcessHeaps.argtypes = []
RtlGetProcessHeaps = _libraries['FIXME_STUB'].RtlGetProcessHeaps
RtlGetProcessHeaps.restype = ULONG
RtlGetProcessHeaps.argtypes = [ULONG, ctypes.POINTER(ctypes.POINTER(None))]
RtlEnumProcessHeaps = _libraries['FIXME_STUB'].RtlEnumProcessHeaps
RtlEnumProcessHeaps.restype = NTSTATUS
RtlEnumProcessHeaps.argtypes = [PRTL_ENUM_HEAPS_ROUTINE, PVOID]
RtlUniform = _libraries['FIXME_STUB'].RtlUniform
RtlUniform.restype = ULONG
RtlUniform.argtypes = [PULONG]
RtlRandom = _libraries['FIXME_STUB'].RtlRandom
RtlRandom.restype = ULONG
RtlRandom.argtypes = [PULONG]
RtlRandomEx = _libraries['FIXME_STUB'].RtlRandomEx
RtlRandomEx.restype = ULONG
RtlRandomEx.argtypes = [PULONG]
class struct__MESSAGE_RESOURCE_ENTRY(Structure):
    pass

struct__MESSAGE_RESOURCE_ENTRY._pack_ = 1 # source:False
struct__MESSAGE_RESOURCE_ENTRY._fields_ = [
    ('Length', ctypes.c_uint16),
    ('Flags', ctypes.c_uint16),
    ('Text', ctypes.c_ubyte * 1),
    ('PADDING_0', ctypes.c_ubyte),
]

RtlFindMessage = _libraries['FIXME_STUB'].RtlFindMessage
RtlFindMessage.restype = NTSTATUS
RtlFindMessage.argtypes = [PVOID, ULONG, ULONG, ULONG, ctypes.POINTER(ctypes.POINTER(struct__MESSAGE_RESOURCE_ENTRY))]
RtlFormatMessage = _libraries['FIXME_STUB'].RtlFormatMessage
RtlFormatMessage.restype = NTSTATUS
RtlFormatMessage.argtypes = [PCWSTR, ULONG, BOOLEAN, BOOLEAN, BOOLEAN, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), PWSTR, ULONG, PULONG]
RtlNtStatusToDosError = _libraries['FIXME_STUB'].RtlNtStatusToDosError
RtlNtStatusToDosError.restype = ULONG
RtlNtStatusToDosError.argtypes = [NTSTATUS]
RtlNtStatusToDosErrorNoTeb = _libraries['FIXME_STUB'].RtlNtStatusToDosErrorNoTeb
RtlNtStatusToDosErrorNoTeb.restype = ULONG
RtlNtStatusToDosErrorNoTeb.argtypes = [NTSTATUS]
RtlGetLastNtStatus = _libraries['FIXME_STUB'].RtlGetLastNtStatus
RtlGetLastNtStatus.restype = NTSTATUS
RtlGetLastNtStatus.argtypes = []
RtlGetLastWin32Error = _libraries['FIXME_STUB'].RtlGetLastWin32Error
RtlGetLastWin32Error.restype = LONG
RtlGetLastWin32Error.argtypes = []
RtlSetLastWin32ErrorAndNtStatusFromNtStatus = _libraries['FIXME_STUB'].RtlSetLastWin32ErrorAndNtStatusFromNtStatus
RtlSetLastWin32ErrorAndNtStatusFromNtStatus.restype = None
RtlSetLastWin32ErrorAndNtStatusFromNtStatus.argtypes = [NTSTATUS]
RtlSetLastWin32Error = _libraries['FIXME_STUB'].RtlSetLastWin32Error
RtlSetLastWin32Error.restype = None
RtlSetLastWin32Error.argtypes = [LONG]
RtlRestoreLastWin32Error = _libraries['FIXME_STUB'].RtlRestoreLastWin32Error
RtlRestoreLastWin32Error.restype = None
RtlRestoreLastWin32Error.argtypes = [LONG]
RtlGetThreadErrorMode = _libraries['FIXME_STUB'].RtlGetThreadErrorMode
RtlGetThreadErrorMode.restype = ULONG
RtlGetThreadErrorMode.argtypes = []
RtlSetThreadErrorMode = _libraries['FIXME_STUB'].RtlSetThreadErrorMode
RtlSetThreadErrorMode.restype = NTSTATUS
RtlSetThreadErrorMode.argtypes = [ULONG, PULONG]
RtlUpcaseUnicodeString = _libraries['FIXME_STUB'].RtlUpcaseUnicodeString
RtlUpcaseUnicodeString.restype = NTSTATUS
RtlUpcaseUnicodeString.argtypes = [PUNICODE_STRING, PCUNICODE_STRING, BOOLEAN]
RtlInitUnicodeString = _libraries['FIXME_STUB'].RtlInitUnicodeString
RtlInitUnicodeString.restype = None
RtlInitUnicodeString.argtypes = [PUNICODE_STRING, PWSTR]
RtlInitAnsiString = _libraries['FIXME_STUB'].RtlInitAnsiString
RtlInitAnsiString.restype = None
RtlInitAnsiString.argtypes = [PANSI_STRING, PSTR]
RtlCopyUnicodeString = _libraries['FIXME_STUB'].RtlCopyUnicodeString
RtlCopyUnicodeString.restype = None
RtlCopyUnicodeString.argtypes = [PUNICODE_STRING, PCUNICODE_STRING]
RtlAppendUnicodeToString = _libraries['FIXME_STUB'].RtlAppendUnicodeToString
RtlAppendUnicodeToString.restype = NTSTATUS
RtlAppendUnicodeToString.argtypes = [PUNICODE_STRING, PCWSTR]
RtlAnsiStringToUnicodeString = _libraries['FIXME_STUB'].RtlAnsiStringToUnicodeString
RtlAnsiStringToUnicodeString.restype = NTSTATUS
RtlAnsiStringToUnicodeString.argtypes = [PUNICODE_STRING, PANSI_STRING, BOOLEAN]
RtlUnicodeStringToAnsiString = _libraries['FIXME_STUB'].RtlUnicodeStringToAnsiString
RtlUnicodeStringToAnsiString.restype = NTSTATUS
RtlUnicodeStringToAnsiString.argtypes = [PANSI_STRING, PUNICODE_STRING, BOOLEAN]
RtlFreeAnsiString = _libraries['FIXME_STUB'].RtlFreeAnsiString
RtlFreeAnsiString.restype = None
RtlFreeAnsiString.argtypes = [PANSI_STRING]
RtlDefaultNpAcl = _libraries['FIXME_STUB'].RtlDefaultNpAcl
RtlDefaultNpAcl.restype = NTSTATUS
RtlDefaultNpAcl.argtypes = [ctypes.POINTER(ctypes.POINTER(struct__ACL))]
RtlCreateEnvironment = _libraries['FIXME_STUB'].RtlCreateEnvironment
RtlCreateEnvironment.restype = NTSTATUS
RtlCreateEnvironment.argtypes = [BOOLEAN, ctypes.POINTER(ctypes.POINTER(None))]
RtlCreateEnvironmentEx = _libraries['FIXME_STUB'].RtlCreateEnvironmentEx
RtlCreateEnvironmentEx.restype = NTSTATUS
RtlCreateEnvironmentEx.argtypes = [PVOID, ctypes.POINTER(ctypes.POINTER(None)), ULONG]
RtlDestroyEnvironment = _libraries['FIXME_STUB'].RtlDestroyEnvironment
RtlDestroyEnvironment.restype = NTSTATUS
RtlDestroyEnvironment.argtypes = [PVOID]
RtlSetCurrentEnvironment = _libraries['FIXME_STUB'].RtlSetCurrentEnvironment
RtlSetCurrentEnvironment.restype = NTSTATUS
RtlSetCurrentEnvironment.argtypes = [PVOID, ctypes.POINTER(ctypes.POINTER(None))]
RtlSetEnvironmentVar = _libraries['FIXME_STUB'].RtlSetEnvironmentVar
RtlSetEnvironmentVar.restype = NTSTATUS
RtlSetEnvironmentVar.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_uint16)), PWSTR, SIZE_T, PWSTR, SIZE_T]
RtlSetEnvironmentVariable = _libraries['FIXME_STUB'].RtlSetEnvironmentVariable
RtlSetEnvironmentVariable.restype = NTSTATUS
RtlSetEnvironmentVariable.argtypes = [ctypes.POINTER(ctypes.POINTER(None)), PUNICODE_STRING, PUNICODE_STRING]
RtlQueryEnvironmentVariable = _libraries['FIXME_STUB'].RtlQueryEnvironmentVariable
RtlQueryEnvironmentVariable.restype = NTSTATUS
RtlQueryEnvironmentVariable.argtypes = [PVOID, PWSTR, SIZE_T, PWSTR, SIZE_T, PSIZE_T]
RtlQueryEnvironmentVariable_U = _libraries['FIXME_STUB'].RtlQueryEnvironmentVariable_U
RtlQueryEnvironmentVariable_U.restype = NTSTATUS
RtlQueryEnvironmentVariable_U.argtypes = [PVOID, PUNICODE_STRING, PUNICODE_STRING]
RtlExpandEnvironmentStrings = _libraries['FIXME_STUB'].RtlExpandEnvironmentStrings
RtlExpandEnvironmentStrings.restype = NTSTATUS
RtlExpandEnvironmentStrings.argtypes = [PVOID, PWSTR, SIZE_T, PWSTR, SIZE_T, PSIZE_T]
RtlExpandEnvironmentStrings_U = _libraries['FIXME_STUB'].RtlExpandEnvironmentStrings_U
RtlExpandEnvironmentStrings_U.restype = NTSTATUS
RtlExpandEnvironmentStrings_U.argtypes = [PVOID, PUNICODE_STRING, PUNICODE_STRING, PULONG]
RtlSetEnvironmentStrings = _libraries['FIXME_STUB'].RtlSetEnvironmentStrings
RtlSetEnvironmentStrings.restype = NTSTATUS
RtlSetEnvironmentStrings.argtypes = [PWCHAR, SIZE_T]
RtlCreateProcessParameters = _libraries['FIXME_STUB'].RtlCreateProcessParameters
RtlCreateProcessParameters.restype = NTSTATUS
RtlCreateProcessParameters.argtypes = [ctypes.POINTER(ctypes.POINTER(struct__RTL_USER_PROCESS_PARAMETERS)), PUNICODE_STRING, PUNICODE_STRING, PUNICODE_STRING, PUNICODE_STRING, PVOID, PUNICODE_STRING, PUNICODE_STRING, PUNICODE_STRING, PUNICODE_STRING]
RtlCreateProcessParametersEx = _libraries['FIXME_STUB'].RtlCreateProcessParametersEx
RtlCreateProcessParametersEx.restype = NTSTATUS
RtlCreateProcessParametersEx.argtypes = [ctypes.POINTER(ctypes.POINTER(struct__RTL_USER_PROCESS_PARAMETERS)), PUNICODE_STRING, PUNICODE_STRING, PUNICODE_STRING, PUNICODE_STRING, PVOID, PUNICODE_STRING, PUNICODE_STRING, PUNICODE_STRING, PUNICODE_STRING, ULONG]
RtlDestroyProcessParameters = _libraries['FIXME_STUB'].RtlDestroyProcessParameters
RtlDestroyProcessParameters.restype = NTSTATUS
RtlDestroyProcessParameters.argtypes = [PRTL_USER_PROCESS_PARAMETERS]
RtlNormalizeProcessParams = _libraries['FIXME_STUB'].RtlNormalizeProcessParams
RtlNormalizeProcessParams.restype = PRTL_USER_PROCESS_PARAMETERS
RtlNormalizeProcessParams.argtypes = [PRTL_USER_PROCESS_PARAMETERS]
RtlDeNormalizeProcessParams = _libraries['FIXME_STUB'].RtlDeNormalizeProcessParams
RtlDeNormalizeProcessParams.restype = PRTL_USER_PROCESS_PARAMETERS
RtlDeNormalizeProcessParams.argtypes = [PRTL_USER_PROCESS_PARAMETERS]
RtlCreateUserProcess = _libraries['FIXME_STUB'].RtlCreateUserProcess
RtlCreateUserProcess.restype = NTSTATUS
RtlCreateUserProcess.argtypes = [PUNICODE_STRING, ULONG, PRTL_USER_PROCESS_PARAMETERS, PSECURITY_DESCRIPTOR, PSECURITY_DESCRIPTOR, HANDLE, BOOLEAN, HANDLE, HANDLE, PRTL_USER_PROCESS_INFORMATION]
RtlCreateUserThread = _libraries['FIXME_STUB'].RtlCreateUserThread
RtlCreateUserThread.restype = NTSTATUS
RtlCreateUserThread.argtypes = [HANDLE, PSECURITY_DESCRIPTOR, BOOLEAN, ULONG, SIZE_T, SIZE_T, PUSER_THREAD_START_ROUTINE, PVOID, PHANDLE, PCLIENT_ID]
RtlDosApplyFileIsolationRedirection_Ustr = _libraries['FIXME_STUB'].RtlDosApplyFileIsolationRedirection_Ustr
RtlDosApplyFileIsolationRedirection_Ustr.restype = NTSTATUS
RtlDosApplyFileIsolationRedirection_Ustr.argtypes = [ULONG, PUNICODE_STRING, PUNICODE_STRING, PUNICODE_STRING, PUNICODE_STRING, ctypes.POINTER(ctypes.POINTER(struct__UNICODE_STRING)), PULONG, PSIZE_T, PSIZE_T]
class struct__IMAGE_NT_HEADERS64(Structure):
    pass

class struct__IMAGE_FILE_HEADER(Structure):
    pass

struct__IMAGE_FILE_HEADER._pack_ = 1 # source:False
struct__IMAGE_FILE_HEADER._fields_ = [
    ('Machine', ctypes.c_uint16),
    ('NumberOfSections', ctypes.c_uint16),
    ('TimeDateStamp', ctypes.c_uint32),
    ('PointerToSymbolTable', ctypes.c_uint32),
    ('NumberOfSymbols', ctypes.c_uint32),
    ('SizeOfOptionalHeader', ctypes.c_uint16),
    ('Characteristics', ctypes.c_uint16),
]

class struct__IMAGE_OPTIONAL_HEADER64(Structure):
    pass

class struct__IMAGE_DATA_DIRECTORY(Structure):
    pass

struct__IMAGE_DATA_DIRECTORY._pack_ = 1 # source:False
struct__IMAGE_DATA_DIRECTORY._fields_ = [
    ('VirtualAddress', ctypes.c_uint32),
    ('Size', ctypes.c_uint32),
]

struct__IMAGE_OPTIONAL_HEADER64._pack_ = 1 # source:False
struct__IMAGE_OPTIONAL_HEADER64._fields_ = [
    ('Magic', ctypes.c_uint16),
    ('MajorLinkerVersion', ctypes.c_ubyte),
    ('MinorLinkerVersion', ctypes.c_ubyte),
    ('SizeOfCode', ctypes.c_uint32),
    ('SizeOfInitializedData', ctypes.c_uint32),
    ('SizeOfUninitializedData', ctypes.c_uint32),
    ('AddressOfEntryPoint', ctypes.c_uint32),
    ('BaseOfCode', ctypes.c_uint32),
    ('ImageBase', ctypes.c_uint64),
    ('SectionAlignment', ctypes.c_uint32),
    ('FileAlignment', ctypes.c_uint32),
    ('MajorOperatingSystemVersion', ctypes.c_uint16),
    ('MinorOperatingSystemVersion', ctypes.c_uint16),
    ('MajorImageVersion', ctypes.c_uint16),
    ('MinorImageVersion', ctypes.c_uint16),
    ('MajorSubsystemVersion', ctypes.c_uint16),
    ('MinorSubsystemVersion', ctypes.c_uint16),
    ('Win32VersionValue', ctypes.c_uint32),
    ('SizeOfImage', ctypes.c_uint32),
    ('SizeOfHeaders', ctypes.c_uint32),
    ('CheckSum', ctypes.c_uint32),
    ('Subsystem', ctypes.c_uint16),
    ('DllCharacteristics', ctypes.c_uint16),
    ('SizeOfStackReserve', ctypes.c_uint64),
    ('SizeOfStackCommit', ctypes.c_uint64),
    ('SizeOfHeapReserve', ctypes.c_uint64),
    ('SizeOfHeapCommit', ctypes.c_uint64),
    ('LoaderFlags', ctypes.c_uint32),
    ('NumberOfRvaAndSizes', ctypes.c_uint32),
    ('DataDirectory', struct__IMAGE_DATA_DIRECTORY * 16),
]

struct__IMAGE_NT_HEADERS64._pack_ = 1 # source:False
struct__IMAGE_NT_HEADERS64._fields_ = [
    ('Signature', ctypes.c_uint32),
    ('FileHeader', struct__IMAGE_FILE_HEADER),
    ('OptionalHeader', struct__IMAGE_OPTIONAL_HEADER64),
]

PIMAGE_NT_HEADERS = ctypes.POINTER(struct__IMAGE_NT_HEADERS64)
RtlImageNtHeader = _libraries['FIXME_STUB'].RtlImageNtHeader
RtlImageNtHeader.restype = PIMAGE_NT_HEADERS
RtlImageNtHeader.argtypes = [PVOID]
ULONG64 = ctypes.c_uint64
RtlImageNtHeaderEx = _libraries['FIXME_STUB'].RtlImageNtHeaderEx
RtlImageNtHeaderEx.restype = NTSTATUS
RtlImageNtHeaderEx.argtypes = [ULONG, PVOID, ULONG64, ctypes.POINTER(ctypes.POINTER(struct__IMAGE_NT_HEADERS64))]
RtlImageDirectoryEntryToData = _libraries['FIXME_STUB'].RtlImageDirectoryEntryToData
RtlImageDirectoryEntryToData.restype = PVOID
RtlImageDirectoryEntryToData.argtypes = [PVOID, BOOLEAN, USHORT, PULONG]
RtlPcToFileHeader = _libraries['FIXME_STUB'].RtlPcToFileHeader
RtlPcToFileHeader.restype = PVOID
RtlPcToFileHeader.argtypes = [PVOID, ctypes.POINTER(ctypes.POINTER(None))]
RtlAddressInSectionTable = _libraries['FIXME_STUB'].RtlAddressInSectionTable
RtlAddressInSectionTable.restype = PVOID
RtlAddressInSectionTable.argtypes = [PIMAGE_NT_HEADERS, PVOID, ULONG]
class struct__IMAGE_SECTION_HEADER(Structure):
    pass

class union_union_78(Union):
    pass

union_union_78._pack_ = 1 # source:False
union_union_78._fields_ = [
    ('PhysicalAddress', ctypes.c_uint32),
    ('VirtualSize', ctypes.c_uint32),
]

struct__IMAGE_SECTION_HEADER._pack_ = 1 # source:False
struct__IMAGE_SECTION_HEADER._fields_ = [
    ('Name', ctypes.c_ubyte * 8),
    ('Misc', union_union_78),
    ('VirtualAddress', ctypes.c_uint32),
    ('SizeOfRawData', ctypes.c_uint32),
    ('PointerToRawData', ctypes.c_uint32),
    ('PointerToRelocations', ctypes.c_uint32),
    ('PointerToLinenumbers', ctypes.c_uint32),
    ('NumberOfRelocations', ctypes.c_uint16),
    ('NumberOfLinenumbers', ctypes.c_uint16),
    ('Characteristics', ctypes.c_uint32),
]

PIMAGE_SECTION_HEADER = ctypes.POINTER(struct__IMAGE_SECTION_HEADER)
RtlImageRvaToSection = _libraries['FIXME_STUB'].RtlImageRvaToSection
RtlImageRvaToSection.restype = PIMAGE_SECTION_HEADER
RtlImageRvaToSection.argtypes = [PIMAGE_NT_HEADERS, PVOID, ULONG]
RtlImageRvaToVa = _libraries['FIXME_STUB'].RtlImageRvaToVa
RtlImageRvaToVa.restype = PVOID
RtlImageRvaToVa.argtypes = [PIMAGE_NT_HEADERS, PVOID, ULONG, ctypes.POINTER(ctypes.POINTER(struct__IMAGE_SECTION_HEADER))]
RtlQueryProcessHeapInformation = _libraries['FIXME_STUB'].RtlQueryProcessHeapInformation
RtlQueryProcessHeapInformation.restype = NTSTATUS
RtlQueryProcessHeapInformation.argtypes = [PRTL_DEBUG_INFORMATION]
RtlCreateQueryDebugBuffer = _libraries['FIXME_STUB'].RtlCreateQueryDebugBuffer
RtlCreateQueryDebugBuffer.restype = PRTL_DEBUG_INFORMATION
RtlCreateQueryDebugBuffer.argtypes = [ULONG, BOOLEAN]
RtlQueryProcessDebugInformation = _libraries['FIXME_STUB'].RtlQueryProcessDebugInformation
RtlQueryProcessDebugInformation.restype = NTSTATUS
RtlQueryProcessDebugInformation.argtypes = [HANDLE, ULONG, PRTL_DEBUG_INFORMATION]
RtlRestoreContext = _libraries['FIXME_STUB'].RtlRestoreContext
RtlRestoreContext.restype = None
RtlRestoreContext.argtypes = [PCONTEXT, PEXCEPTION_RECORD]
RtlAdjustPrivilege = _libraries['FIXME_STUB'].RtlAdjustPrivilege
RtlAdjustPrivilege.restype = NTSTATUS
RtlAdjustPrivilege.argtypes = [ULONG, BOOLEAN, BOOLEAN, PBOOLEAN]
RtlAcquirePrivilege = _libraries['FIXME_STUB'].RtlAcquirePrivilege
RtlAcquirePrivilege.restype = NTSTATUS
RtlAcquirePrivilege.argtypes = [PULONG, ULONG, ULONG, ctypes.POINTER(ctypes.POINTER(None))]
RtlReleasePrivilege = _libraries['FIXME_STUB'].RtlReleasePrivilege
RtlReleasePrivilege.restype = None
RtlReleasePrivilege.argtypes = [PVOID]
RtlGetFullPathName_U = _libraries['FIXME_STUB'].RtlGetFullPathName_U
RtlGetFullPathName_U.restype = ULONG
RtlGetFullPathName_U.argtypes = [PWSTR, ULONG, PWSTR, ctypes.POINTER(ctypes.POINTER(ctypes.c_uint16))]
RtlDosPathNameToNtPathName_U = _libraries['FIXME_STUB'].RtlDosPathNameToNtPathName_U
RtlDosPathNameToNtPathName_U.restype = BOOLEAN
RtlDosPathNameToNtPathName_U.argtypes = [PCWSTR, PUNICODE_STRING, ctypes.POINTER(ctypes.POINTER(ctypes.c_uint16)), PVOID]
RtlDosPathNameToRelativeNtPathName_U = _libraries['FIXME_STUB'].RtlDosPathNameToRelativeNtPathName_U
RtlDosPathNameToRelativeNtPathName_U.restype = BOOLEAN
RtlDosPathNameToRelativeNtPathName_U.argtypes = [PCWSTR, PUNICODE_STRING, ctypes.POINTER(ctypes.POINTER(ctypes.c_uint16)), PRTL_RELATIVE_NAME_U]
RtlDosPathNameToRelativeNtPathName_U_WithStatus = _libraries['FIXME_STUB'].RtlDosPathNameToRelativeNtPathName_U_WithStatus
RtlDosPathNameToRelativeNtPathName_U_WithStatus.restype = NTSTATUS
RtlDosPathNameToRelativeNtPathName_U_WithStatus.argtypes = [PWSTR, PUNICODE_STRING, ctypes.POINTER(ctypes.POINTER(ctypes.c_uint16)), PRTL_RELATIVE_NAME_U]
RtlDetermineDosPathNameType_U = _libraries['FIXME_STUB'].RtlDetermineDosPathNameType_U
RtlDetermineDosPathNameType_U.restype = RTL_PATH_TYPE
RtlDetermineDosPathNameType_U.argtypes = [PCWSTR]
RtlGetFullPathName_UstrEx = _libraries['FIXME_STUB'].RtlGetFullPathName_UstrEx
RtlGetFullPathName_UstrEx.restype = NTSTATUS
RtlGetFullPathName_UstrEx.argtypes = [PUNICODE_STRING, PUNICODE_STRING, PUNICODE_STRING, ctypes.POINTER(ctypes.POINTER(struct__UNICODE_STRING)), PSIZE_T, PBOOLEAN, ctypes.POINTER(_RTL_PATH_TYPE), PSIZE_T]
RtlSetCurrentDirectory_U = _libraries['FIXME_STUB'].RtlSetCurrentDirectory_U
RtlSetCurrentDirectory_U.restype = NTSTATUS
RtlSetCurrentDirectory_U.argtypes = [PUNICODE_STRING]
RtlReleaseRelativeName = _libraries['FIXME_STUB'].RtlReleaseRelativeName
RtlReleaseRelativeName.restype = None
RtlReleaseRelativeName.argtypes = [PRTL_RELATIVE_NAME_U]
RtlNtPathNameToDosPathName = _libraries['FIXME_STUB'].RtlNtPathNameToDosPathName
RtlNtPathNameToDosPathName.restype = NTSTATUS
RtlNtPathNameToDosPathName.argtypes = [ULONG, PRTL_UNICODE_STRING_BUFFER, PULONG, ctypes.POINTER(ctypes.POINTER(ctypes.c_uint16))]
class struct__RTL_SRWLOCK(Structure):
    pass

struct__RTL_SRWLOCK._pack_ = 1 # source:False
struct__RTL_SRWLOCK._fields_ = [
    ('Ptr', ctypes.POINTER(None)),
]

PRTL_SRWLOCK = ctypes.POINTER(struct__RTL_SRWLOCK)
RtlInitializeSRWLock = _libraries['FIXME_STUB'].RtlInitializeSRWLock
RtlInitializeSRWLock.restype = None
RtlInitializeSRWLock.argtypes = [PRTL_SRWLOCK]
RtlAcquireSRWLockExclusive = _libraries['FIXME_STUB'].RtlAcquireSRWLockExclusive
RtlAcquireSRWLockExclusive.restype = None
RtlAcquireSRWLockExclusive.argtypes = [PRTL_SRWLOCK]
RtlAcquireSRWLockShared = _libraries['FIXME_STUB'].RtlAcquireSRWLockShared
RtlAcquireSRWLockShared.restype = None
RtlAcquireSRWLockShared.argtypes = [PRTL_SRWLOCK]
RtlReleaseSRWLockExclusive = _libraries['FIXME_STUB'].RtlReleaseSRWLockExclusive
RtlReleaseSRWLockExclusive.restype = None
RtlReleaseSRWLockExclusive.argtypes = [PRTL_SRWLOCK]
RtlReleaseSRWLockShared = _libraries['FIXME_STUB'].RtlReleaseSRWLockShared
RtlReleaseSRWLockShared.restype = None
RtlReleaseSRWLockShared.argtypes = [PRTL_SRWLOCK]
RtlTryAcquireSRWLockExclusive = _libraries['FIXME_STUB'].RtlTryAcquireSRWLockExclusive
RtlTryAcquireSRWLockExclusive.restype = BOOLEAN
RtlTryAcquireSRWLockExclusive.argtypes = [PRTL_SRWLOCK]
RtlTryAcquireSRWLockShared = _libraries['FIXME_STUB'].RtlTryAcquireSRWLockShared
RtlTryAcquireSRWLockShared.restype = BOOLEAN
RtlTryAcquireSRWLockShared.argtypes = [PRTL_SRWLOCK]
RtlAcquireReleaseSRWLockExclusive = _libraries['FIXME_STUB'].RtlAcquireReleaseSRWLockExclusive
RtlAcquireReleaseSRWLockExclusive.restype = None
RtlAcquireReleaseSRWLockExclusive.argtypes = [PRTL_SRWLOCK]
RtlWalkFrameChain = _libraries['FIXME_STUB'].RtlWalkFrameChain
RtlWalkFrameChain.restype = ULONG
RtlWalkFrameChain.argtypes = [ctypes.POINTER(ctypes.POINTER(None)), ULONG, ULONG]
PfxFindPrefix = _libraries['FIXME_STUB'].PfxFindPrefix
PfxFindPrefix.restype = PPREFIX_TABLE_ENTRY
PfxFindPrefix.argtypes = [PPREFIX_TABLE, PANSI_STRING]
PfxInitialize = _libraries['FIXME_STUB'].PfxInitialize
PfxInitialize.restype = None
PfxInitialize.argtypes = [PPREFIX_TABLE]
PfxInsertPrefix = _libraries['FIXME_STUB'].PfxInsertPrefix
PfxInsertPrefix.restype = BOOLEAN
PfxInsertPrefix.argtypes = [PPREFIX_TABLE, PANSI_STRING, PPREFIX_TABLE_ENTRY]
PfxRemovePrefix = _libraries['FIXME_STUB'].PfxRemovePrefix
PfxRemovePrefix.restype = None
PfxRemovePrefix.argtypes = [PPREFIX_TABLE, PPREFIX_TABLE_ENTRY]
RtlAbsoluteToSelfRelativeSD = _libraries['FIXME_STUB'].RtlAbsoluteToSelfRelativeSD
RtlAbsoluteToSelfRelativeSD.restype = NTSTATUS
RtlAbsoluteToSelfRelativeSD.argtypes = [PSECURITY_DESCRIPTOR, PSECURITY_DESCRIPTOR, PULONG]
PACL = ctypes.POINTER(struct__ACL)
RtlAddAccessAllowedAce = _libraries['FIXME_STUB'].RtlAddAccessAllowedAce
RtlAddAccessAllowedAce.restype = NTSTATUS
RtlAddAccessAllowedAce.argtypes = [PACL, ULONG, ACCESS_MASK, PSID]
RtlAddAccessAllowedAceEx = _libraries['FIXME_STUB'].RtlAddAccessAllowedAceEx
RtlAddAccessAllowedAceEx.restype = NTSTATUS
RtlAddAccessAllowedAceEx.argtypes = [PACL, ULONG, ULONG, ACCESS_MASK, PSID]
RtlAddAce = _libraries['FIXME_STUB'].RtlAddAce
RtlAddAce.restype = NTSTATUS
RtlAddAce.argtypes = [PACL, ULONG, ULONG, PVOID, ULONG]
RtlAddAtomToAtomTable = _libraries['FIXME_STUB'].RtlAddAtomToAtomTable
RtlAddAtomToAtomTable.restype = NTSTATUS
RtlAddAtomToAtomTable.argtypes = [PVOID, PWSTR, PRTL_ATOM]
RtlAppendUnicodeStringToString = _libraries['FIXME_STUB'].RtlAppendUnicodeStringToString
RtlAppendUnicodeStringToString.restype = NTSTATUS
RtlAppendUnicodeStringToString.argtypes = [PUNICODE_STRING, PCUNICODE_STRING]
RtlAreAllAccessesGranted = _libraries['FIXME_STUB'].RtlAreAllAccessesGranted
RtlAreAllAccessesGranted.restype = BOOLEAN
RtlAreAllAccessesGranted.argtypes = [ACCESS_MASK, ACCESS_MASK]
RtlAreAnyAccessesGranted = _libraries['FIXME_STUB'].RtlAreAnyAccessesGranted
RtlAreAnyAccessesGranted.restype = BOOLEAN
RtlAreAnyAccessesGranted.argtypes = [ACCESS_MASK, ACCESS_MASK]
RtlAreBitsClear = _libraries['FIXME_STUB'].RtlAreBitsClear
RtlAreBitsClear.restype = BOOLEAN
RtlAreBitsClear.argtypes = [PRTL_BITMAP, ULONG, ULONG]
RtlAreBitsSet = _libraries['FIXME_STUB'].RtlAreBitsSet
RtlAreBitsSet.restype = BOOLEAN
RtlAreBitsSet.argtypes = [PRTL_BITMAP, ULONG, ULONG]
RtlCaptureContext = _libraries['FIXME_STUB'].RtlCaptureContext
RtlCaptureContext.restype = None
RtlCaptureContext.argtypes = [PCONTEXT]
WORD = ctypes.c_uint16
RtlCaptureStackBackTrace = _libraries['FIXME_STUB'].RtlCaptureStackBackTrace
RtlCaptureStackBackTrace.restype = WORD
RtlCaptureStackBackTrace.argtypes = [ULONG, ULONG, ctypes.POINTER(ctypes.POINTER(None)), PULONG]
RtlClearAllBits = _libraries['FIXME_STUB'].RtlClearAllBits
RtlClearAllBits.restype = None
RtlClearAllBits.argtypes = [PRTL_BITMAP]
RtlClearBits = _libraries['FIXME_STUB'].RtlClearBits
RtlClearBits.restype = None
RtlClearBits.argtypes = [PRTL_BITMAP, ULONG, ULONG]
RtlCreateSystemVolumeInformationFolder = _libraries['FIXME_STUB'].RtlCreateSystemVolumeInformationFolder
RtlCreateSystemVolumeInformationFolder.restype = NTSTATUS
RtlCreateSystemVolumeInformationFolder.argtypes = [PCUNICODE_STRING]
RtlCompareAltitudes = _libraries['FIXME_STUB'].RtlCompareAltitudes
RtlCompareAltitudes.restype = LONG
RtlCompareAltitudes.argtypes = [PCUNICODE_STRING, PCUNICODE_STRING]
RtlCompareUnicodeString = _libraries['FIXME_STUB'].RtlCompareUnicodeString
RtlCompareUnicodeString.restype = LONG
RtlCompareUnicodeString.argtypes = [PCUNICODE_STRING, PCUNICODE_STRING, BOOLEAN]
ULONG32 = ctypes.c_uint32
RtlComputeCrc32 = _libraries['FIXME_STUB'].RtlComputeCrc32
RtlComputeCrc32.restype = ULONG32
RtlComputeCrc32.argtypes = [ULONG32, PVOID, ULONG]
RtlConvertSidToUnicodeString = _libraries['FIXME_STUB'].RtlConvertSidToUnicodeString
RtlConvertSidToUnicodeString.restype = NTSTATUS
RtlConvertSidToUnicodeString.argtypes = [PUNICODE_STRING, PSID, BOOLEAN]
RtlCopyLuid = _libraries['FIXME_STUB'].RtlCopyLuid
RtlCopyLuid.restype = None
RtlCopyLuid.argtypes = [PLUID, PLUID]
RtlCopySid = _libraries['FIXME_STUB'].RtlCopySid
RtlCopySid.restype = NTSTATUS
RtlCopySid.argtypes = [ULONG, PSID, PSID]
RtlCreateAcl = _libraries['FIXME_STUB'].RtlCreateAcl
RtlCreateAcl.restype = NTSTATUS
RtlCreateAcl.argtypes = [PACL, ULONG, ULONG]
RtlCreateAtomTable = _libraries['FIXME_STUB'].RtlCreateAtomTable
RtlCreateAtomTable.restype = NTSTATUS
RtlCreateAtomTable.argtypes = [ULONG, ctypes.POINTER(ctypes.POINTER(None))]
RtlDecompressFragment = _libraries['FIXME_STUB'].RtlDecompressFragment
RtlDecompressFragment.restype = NTSTATUS
RtlDecompressFragment.argtypes = [USHORT, PUCHAR, ULONG, PUCHAR, ULONG, ULONG, PULONG, PVOID]
RtlDelete = _libraries['FIXME_STUB'].RtlDelete
RtlDelete.restype = PRTL_SPLAY_LINKS
RtlDelete.argtypes = [PRTL_SPLAY_LINKS]
RtlDeleteAce = _libraries['FIXME_STUB'].RtlDeleteAce
RtlDeleteAce.restype = NTSTATUS
RtlDeleteAce.argtypes = [PACL, ULONG]
RtlDeleteAtomFromAtomTable = _libraries['FIXME_STUB'].RtlDeleteAtomFromAtomTable
RtlDeleteAtomFromAtomTable.restype = NTSTATUS
RtlDeleteAtomFromAtomTable.argtypes = [PVOID, RTL_ATOM]
RtlDeleteNoSplay = _libraries['FIXME_STUB'].RtlDeleteNoSplay
RtlDeleteNoSplay.restype = None
RtlDeleteNoSplay.argtypes = [PRTL_SPLAY_LINKS, ctypes.POINTER(ctypes.POINTER(struct__RTL_SPLAY_LINKS))]
RtlDowncaseUnicodeString = _libraries['FIXME_STUB'].RtlDowncaseUnicodeString
RtlDowncaseUnicodeString.restype = NTSTATUS
RtlDowncaseUnicodeString.argtypes = [PUNICODE_STRING, PCUNICODE_STRING, BOOLEAN]
RtlDuplicateUnicodeString = _libraries['FIXME_STUB'].RtlDuplicateUnicodeString
RtlDuplicateUnicodeString.restype = NTSTATUS
RtlDuplicateUnicodeString.argtypes = [ULONG, ctypes.POINTER(struct__UNICODE_STRING), ctypes.POINTER(struct__UNICODE_STRING)]
RtlEmptyAtomTable = _libraries['FIXME_STUB'].RtlEmptyAtomTable
RtlEmptyAtomTable.restype = NTSTATUS
RtlEmptyAtomTable.argtypes = [PVOID, BOOLEAN]
RtlEqualSid = _libraries['FIXME_STUB'].RtlEqualSid
RtlEqualSid.restype = BOOLEAN
RtlEqualSid.argtypes = [PSID, PSID]
RtlEqualString = _libraries['FIXME_STUB'].RtlEqualString
RtlEqualString.restype = BOOLEAN
RtlEqualString.argtypes = [PANSI_STRING, PANSI_STRING, BOOLEAN]
RtlEqualUnicodeString = _libraries['FIXME_STUB'].RtlEqualUnicodeString
RtlEqualUnicodeString.restype = BOOLEAN
RtlEqualUnicodeString.argtypes = [PCUNICODE_STRING, PCUNICODE_STRING, BOOLEAN]
RtlFindClearBits = _libraries['FIXME_STUB'].RtlFindClearBits
RtlFindClearBits.restype = ULONG
RtlFindClearBits.argtypes = [PRTL_BITMAP, ULONG, ULONG]
RtlFindClearBitsAndSet = _libraries['FIXME_STUB'].RtlFindClearBitsAndSet
RtlFindClearBitsAndSet.restype = ULONG
RtlFindClearBitsAndSet.argtypes = [PRTL_BITMAP, ULONG, ULONG]
RtlFindClearRuns = _libraries['FIXME_STUB'].RtlFindClearRuns
RtlFindClearRuns.restype = ULONG
RtlFindClearRuns.argtypes = [PRTL_BITMAP, PRTL_BITMAP_RUN, ULONG, BOOLEAN]
RtlFindLastBackwardRunClear = _libraries['FIXME_STUB'].RtlFindLastBackwardRunClear
RtlFindLastBackwardRunClear.restype = ULONG
RtlFindLastBackwardRunClear.argtypes = [PRTL_BITMAP, ULONG, PULONG]
CCHAR = ctypes.c_char
ULONGLONG = ctypes.c_uint64
RtlFindLeastSignificantBit = _libraries['FIXME_STUB'].RtlFindLeastSignificantBit
RtlFindLeastSignificantBit.restype = CCHAR
RtlFindLeastSignificantBit.argtypes = [ULONGLONG]
RtlFindLongestRunClear = _libraries['FIXME_STUB'].RtlFindLongestRunClear
RtlFindLongestRunClear.restype = ULONG
RtlFindLongestRunClear.argtypes = [PRTL_BITMAP, PULONG]
RtlFindMostSignificantBit = _libraries['FIXME_STUB'].RtlFindMostSignificantBit
RtlFindMostSignificantBit.restype = CCHAR
RtlFindMostSignificantBit.argtypes = [ULONGLONG]
RtlFindNextForwardRunClear = _libraries['FIXME_STUB'].RtlFindNextForwardRunClear
RtlFindNextForwardRunClear.restype = ULONG
RtlFindNextForwardRunClear.argtypes = [PRTL_BITMAP, ULONG, PULONG]
RtlFindSetBits = _libraries['FIXME_STUB'].RtlFindSetBits
RtlFindSetBits.restype = ULONG
RtlFindSetBits.argtypes = [PRTL_BITMAP, ULONG, ULONG]
RtlFindSetBitsAndClear = _libraries['FIXME_STUB'].RtlFindSetBitsAndClear
RtlFindSetBitsAndClear.restype = ULONG
RtlFindSetBitsAndClear.argtypes = [PRTL_BITMAP, ULONG, ULONG]
RtlGetCallersAddress = _libraries['FIXME_STUB'].RtlGetCallersAddress
RtlGetCallersAddress.restype = None
RtlGetCallersAddress.argtypes = [ctypes.POINTER(ctypes.POINTER(None)), ctypes.POINTER(ctypes.POINTER(None))]
RtlGetDaclSecurityDescriptor = _libraries['FIXME_STUB'].RtlGetDaclSecurityDescriptor
RtlGetDaclSecurityDescriptor.restype = NTSTATUS
RtlGetDaclSecurityDescriptor.argtypes = [PSECURITY_DESCRIPTOR, PBOOLEAN, ctypes.POINTER(ctypes.POINTER(struct__ACL)), PBOOLEAN]
RtlGetGroupSecurityDescriptor = _libraries['FIXME_STUB'].RtlGetGroupSecurityDescriptor
RtlGetGroupSecurityDescriptor.restype = NTSTATUS
RtlGetGroupSecurityDescriptor.argtypes = [PSECURITY_DESCRIPTOR, ctypes.POINTER(ctypes.POINTER(None)), PBOOLEAN]
RtlGetOwnerSecurityDescriptor = _libraries['FIXME_STUB'].RtlGetOwnerSecurityDescriptor
RtlGetOwnerSecurityDescriptor.restype = NTSTATUS
RtlGetOwnerSecurityDescriptor.argtypes = [PSECURITY_DESCRIPTOR, ctypes.POINTER(ctypes.POINTER(None)), PBOOLEAN]
RtlGetSaclSecurityDescriptor = _libraries['FIXME_STUB'].RtlGetSaclSecurityDescriptor
RtlGetSaclSecurityDescriptor.restype = NTSTATUS
RtlGetSaclSecurityDescriptor.argtypes = [PSECURITY_DESCRIPTOR, PBOOLEAN, ctypes.POINTER(ctypes.POINTER(struct__ACL)), PBOOLEAN]
RtlGetSetBootStatusData = _libraries['FIXME_STUB'].RtlGetSetBootStatusData
RtlGetSetBootStatusData.restype = NTSTATUS
RtlGetSetBootStatusData.argtypes = [HANDLE, BOOLEAN, RTL_BSD_ITEM_TYPE, PVOID, ULONG, PULONG]
RtlCreateBootStatusDataFile = _libraries['FIXME_STUB'].RtlCreateBootStatusDataFile
RtlCreateBootStatusDataFile.restype = NTSTATUS
RtlCreateBootStatusDataFile.argtypes = []
class struct__OSVERSIONINFOW(Structure):
    pass

struct__OSVERSIONINFOW._pack_ = 1 # source:False
struct__OSVERSIONINFOW._fields_ = [
    ('dwOSVersionInfoSize', ctypes.c_uint32),
    ('dwMajorVersion', ctypes.c_uint32),
    ('dwMinorVersion', ctypes.c_uint32),
    ('dwBuildNumber', ctypes.c_uint32),
    ('dwPlatformId', ctypes.c_uint32),
    ('szCSDVersion', ctypes.c_uint16 * 128),
]

PRTL_OSVERSIONINFOW = ctypes.POINTER(struct__OSVERSIONINFOW)
RtlGetVersion = _libraries['FIXME_STUB'].RtlGetVersion
RtlGetVersion.restype = NTSTATUS
RtlGetVersion.argtypes = [PRTL_OSVERSIONINFOW]
RtlGUIDFromString = _libraries['FIXME_STUB'].RtlGUIDFromString
RtlGUIDFromString.restype = NTSTATUS
RtlGUIDFromString.argtypes = [PUNICODE_STRING, ctypes.POINTER(struct__GUID)]
RtlHashUnicodeString = _libraries['FIXME_STUB'].RtlHashUnicodeString
RtlHashUnicodeString.restype = NTSTATUS
RtlHashUnicodeString.argtypes = [ctypes.POINTER(struct__UNICODE_STRING), BOOLEAN, ULONG, PULONG]
class struct__SID_IDENTIFIER_AUTHORITY(Structure):
    pass

struct__SID_IDENTIFIER_AUTHORITY._pack_ = 1 # source:False
struct__SID_IDENTIFIER_AUTHORITY._fields_ = [
    ('Value', ctypes.c_ubyte * 6),
]

PSID_IDENTIFIER_AUTHORITY = ctypes.POINTER(struct__SID_IDENTIFIER_AUTHORITY)
UCHAR = ctypes.c_ubyte
RtlInitializeSid = _libraries['FIXME_STUB'].RtlInitializeSid
RtlInitializeSid.restype = NTSTATUS
RtlInitializeSid.argtypes = [PSID, PSID_IDENTIFIER_AUTHORITY, UCHAR]
RtlLengthRequiredSid = _libraries['FIXME_STUB'].RtlLengthRequiredSid
RtlLengthRequiredSid.restype = ULONG
RtlLengthRequiredSid.argtypes = [ULONG]
RtlLengthSecurityDescriptor = _libraries['FIXME_STUB'].RtlLengthSecurityDescriptor
RtlLengthSecurityDescriptor.restype = ULONG
RtlLengthSecurityDescriptor.argtypes = [PSECURITY_DESCRIPTOR]
RtlLengthSid = _libraries['FIXME_STUB'].RtlLengthSid
RtlLengthSid.restype = ULONG
RtlLengthSid.argtypes = [PSID]
RtlLockBootStatusData = _libraries['FIXME_STUB'].RtlLockBootStatusData
RtlLockBootStatusData.restype = NTSTATUS
RtlLockBootStatusData.argtypes = [PHANDLE]
RtlLookupAtomInAtomTable = _libraries['FIXME_STUB'].RtlLookupAtomInAtomTable
RtlLookupAtomInAtomTable.restype = NTSTATUS
RtlLookupAtomInAtomTable.argtypes = [PVOID, PWSTR, PRTL_ATOM]
RtlMapSecurityErrorToNtStatus = _libraries['FIXME_STUB'].RtlMapSecurityErrorToNtStatus
RtlMapSecurityErrorToNtStatus.restype = NTSTATUS
RtlMapSecurityErrorToNtStatus.argtypes = [SECURITY_STATUS]
PWCH = ctypes.POINTER(ctypes.c_uint16)
RtlMultiByteToUnicodeN = _libraries['FIXME_STUB'].RtlMultiByteToUnicodeN
RtlMultiByteToUnicodeN.restype = NTSTATUS
RtlMultiByteToUnicodeN.argtypes = [PWCH, ULONG, PULONG, PCSTR, ULONG]
RtlMultiByteToUnicodeSize = _libraries['FIXME_STUB'].RtlMultiByteToUnicodeSize
RtlMultiByteToUnicodeSize.restype = NTSTATUS
RtlMultiByteToUnicodeSize.argtypes = [PULONG, PCSTR, ULONG]
RtlNumberOfClearBits = _libraries['FIXME_STUB'].RtlNumberOfClearBits
RtlNumberOfClearBits.restype = ULONG
RtlNumberOfClearBits.argtypes = [PRTL_BITMAP]
RtlNumberOfSetBits = _libraries['FIXME_STUB'].RtlNumberOfSetBits
RtlNumberOfSetBits.restype = ULONG
RtlNumberOfSetBits.argtypes = [PRTL_BITMAP]
RtlQueryAtomInAtomTable = _libraries['FIXME_STUB'].RtlQueryAtomInAtomTable
RtlQueryAtomInAtomTable.restype = NTSTATUS
RtlQueryAtomInAtomTable.argtypes = [PVOID, RTL_ATOM, PULONG, PULONG, PWSTR, PULONG]
RtlRealPredecessor = _libraries['FIXME_STUB'].RtlRealPredecessor
RtlRealPredecessor.restype = PRTL_SPLAY_LINKS
RtlRealPredecessor.argtypes = [PRTL_SPLAY_LINKS]
RtlRealSuccessor = _libraries['FIXME_STUB'].RtlRealSuccessor
RtlRealSuccessor.restype = PRTL_SPLAY_LINKS
RtlRealSuccessor.argtypes = [PRTL_SPLAY_LINKS]
RtlRunDecodeUnicodeString = _libraries['FIXME_STUB'].RtlRunDecodeUnicodeString
RtlRunDecodeUnicodeString.restype = None
RtlRunDecodeUnicodeString.argtypes = [UCHAR, PUNICODE_STRING]
RtlRunEncodeUnicodeString = _libraries['FIXME_STUB'].RtlRunEncodeUnicodeString
RtlRunEncodeUnicodeString.restype = None
RtlRunEncodeUnicodeString.argtypes = [PUCHAR, PUNICODE_STRING]
RtlSelfRelativeToAbsoluteSD = _libraries['FIXME_STUB'].RtlSelfRelativeToAbsoluteSD
RtlSelfRelativeToAbsoluteSD.restype = NTSTATUS
RtlSelfRelativeToAbsoluteSD.argtypes = [PSECURITY_DESCRIPTOR, PSECURITY_DESCRIPTOR, PULONG, PACL, PULONG, PACL, PULONG, PSID, PULONG, PSID, PULONG]
RtlSelfRelativeToAbsoluteSD2 = _libraries['FIXME_STUB'].RtlSelfRelativeToAbsoluteSD2
RtlSelfRelativeToAbsoluteSD2.restype = NTSTATUS
RtlSelfRelativeToAbsoluteSD2.argtypes = [PSECURITY_DESCRIPTOR, PULONG]
RtlSetAllBits = _libraries['FIXME_STUB'].RtlSetAllBits
RtlSetAllBits.restype = None
RtlSetAllBits.argtypes = [PRTL_BITMAP]
RtlSetBits = _libraries['FIXME_STUB'].RtlSetBits
RtlSetBits.restype = None
RtlSetBits.argtypes = [PRTL_BITMAP, ULONG, ULONG]
RtlSetDaclSecurityDescriptor = _libraries['FIXME_STUB'].RtlSetDaclSecurityDescriptor
RtlSetDaclSecurityDescriptor.restype = NTSTATUS
RtlSetDaclSecurityDescriptor.argtypes = [PSECURITY_DESCRIPTOR, BOOLEAN, PACL, BOOLEAN]
RtlSetGroupSecurityDescriptor = _libraries['FIXME_STUB'].RtlSetGroupSecurityDescriptor
RtlSetGroupSecurityDescriptor.restype = NTSTATUS
RtlSetGroupSecurityDescriptor.argtypes = [PSECURITY_DESCRIPTOR, PSID, BOOLEAN]
RtlSetOwnerSecurityDescriptor = _libraries['FIXME_STUB'].RtlSetOwnerSecurityDescriptor
RtlSetOwnerSecurityDescriptor.restype = NTSTATUS
RtlSetOwnerSecurityDescriptor.argtypes = [PSECURITY_DESCRIPTOR, PSID, BOOLEAN]
RtlSetSaclSecurityDescriptor = _libraries['FIXME_STUB'].RtlSetSaclSecurityDescriptor
RtlSetSaclSecurityDescriptor.restype = NTSTATUS
RtlSetSaclSecurityDescriptor.argtypes = [PSECURITY_DESCRIPTOR, BOOLEAN, PACL, BOOLEAN]
RtlSplay = _libraries['FIXME_STUB'].RtlSplay
RtlSplay.restype = PRTL_SPLAY_LINKS
RtlSplay.argtypes = [PRTL_SPLAY_LINKS]
RtlStringFromGUID = _libraries['FIXME_STUB'].RtlStringFromGUID
RtlStringFromGUID.restype = NTSTATUS
RtlStringFromGUID.argtypes = [ctypes.POINTER(struct__GUID), PUNICODE_STRING]
RtlSubAuthorityCountSid = _libraries['FIXME_STUB'].RtlSubAuthorityCountSid
RtlSubAuthorityCountSid.restype = PUCHAR
RtlSubAuthorityCountSid.argtypes = [PSID]
RtlSubAuthoritySid = _libraries['FIXME_STUB'].RtlSubAuthoritySid
RtlSubAuthoritySid.restype = PULONG
RtlSubAuthoritySid.argtypes = [PSID, ULONG]
RtlSubtreePredecessor = _libraries['FIXME_STUB'].RtlSubtreePredecessor
RtlSubtreePredecessor.restype = PRTL_SPLAY_LINKS
RtlSubtreePredecessor.argtypes = [PRTL_SPLAY_LINKS]
RtlSubtreeSuccessor = _libraries['FIXME_STUB'].RtlSubtreeSuccessor
RtlSubtreeSuccessor.restype = PRTL_SPLAY_LINKS
RtlSubtreeSuccessor.argtypes = [PRTL_SPLAY_LINKS]
RtlTestBit = _libraries['FIXME_STUB'].RtlTestBit
RtlTestBit.restype = BOOLEAN
RtlTestBit.argtypes = [PRTL_BITMAP, ULONG]
RtlUnlockBootStatusData = _libraries['FIXME_STUB'].RtlUnlockBootStatusData
RtlUnlockBootStatusData.restype = None
RtlUnlockBootStatusData.argtypes = [HANDLE]
RtlCreateSecurityDescriptor = _libraries['FIXME_STUB'].RtlCreateSecurityDescriptor
RtlCreateSecurityDescriptor.restype = NTSTATUS
RtlCreateSecurityDescriptor.argtypes = [PSECURITY_DESCRIPTOR, ULONG]
RtlValidRelativeSecurityDescriptor = _libraries['FIXME_STUB'].RtlValidRelativeSecurityDescriptor
RtlValidRelativeSecurityDescriptor.restype = BOOLEAN
RtlValidRelativeSecurityDescriptor.argtypes = [PSECURITY_DESCRIPTOR, ULONG, SECURITY_INFORMATION]
RtlValidSecurityDescriptor = _libraries['FIXME_STUB'].RtlValidSecurityDescriptor
RtlValidSecurityDescriptor.restype = BOOLEAN
RtlValidSecurityDescriptor.argtypes = [PSECURITY_DESCRIPTOR]
RtlValidSid = _libraries['FIXME_STUB'].RtlValidSid
RtlValidSid.restype = BOOLEAN
RtlValidSid.argtypes = [PSID]
class struct__OSVERSIONINFOEXW(Structure):
    pass

struct__OSVERSIONINFOEXW._pack_ = 1 # source:False
struct__OSVERSIONINFOEXW._fields_ = [
    ('dwOSVersionInfoSize', ctypes.c_uint32),
    ('dwMajorVersion', ctypes.c_uint32),
    ('dwMinorVersion', ctypes.c_uint32),
    ('dwBuildNumber', ctypes.c_uint32),
    ('dwPlatformId', ctypes.c_uint32),
    ('szCSDVersion', ctypes.c_uint16 * 128),
    ('wServicePackMajor', ctypes.c_uint16),
    ('wServicePackMinor', ctypes.c_uint16),
    ('wSuiteMask', ctypes.c_uint16),
    ('wProductType', ctypes.c_ubyte),
    ('wReserved', ctypes.c_ubyte),
]

RTL_OSVERSIONINFOEXW = struct__OSVERSIONINFOEXW
RtlVerifyVersionInfo = _libraries['FIXME_STUB'].RtlVerifyVersionInfo
RtlVerifyVersionInfo.restype = NTSTATUS
RtlVerifyVersionInfo.argtypes = [RTL_OSVERSIONINFOEXW, ULONG, ULONGLONG]
VerSetConditionMask = _libraries['FIXME_STUB'].VerSetConditionMask
VerSetConditionMask.restype = ULONGLONG
VerSetConditionMask.argtypes = [ULONGLONG, ULONG, UCHAR]
class struct__TP_POOL(Structure):
    pass

TpAllocPool = _libraries['FIXME_STUB'].TpAllocPool
TpAllocPool.restype = NTSTATUS
TpAllocPool.argtypes = [ctypes.POINTER(ctypes.POINTER(struct__TP_POOL)), PVOID]
PTP_POOL = ctypes.POINTER(struct__TP_POOL)
TpDisablePoolCallbackChecks = _libraries['FIXME_STUB'].TpDisablePoolCallbackChecks
TpDisablePoolCallbackChecks.restype = NTSTATUS
TpDisablePoolCallbackChecks.argtypes = [PTP_POOL]
TpReleasePool = _libraries['FIXME_STUB'].TpReleasePool
TpReleasePool.restype = None
TpReleasePool.argtypes = [PTP_POOL]
TpSetPoolMaxThreads = _libraries['FIXME_STUB'].TpSetPoolMaxThreads
TpSetPoolMaxThreads.restype = None
TpSetPoolMaxThreads.argtypes = [PTP_POOL, LONG]
TpSetPoolMinThreads = _libraries['FIXME_STUB'].TpSetPoolMinThreads
TpSetPoolMinThreads.restype = NTSTATUS
TpSetPoolMinThreads.argtypes = [PTP_POOL, LONG]
class struct__TP_POOL_STACK_INFORMATION(Structure):
    pass

struct__TP_POOL_STACK_INFORMATION._pack_ = 1 # source:False
struct__TP_POOL_STACK_INFORMATION._fields_ = [
    ('StackReserve', ctypes.c_uint64),
    ('StackCommit', ctypes.c_uint64),
]

PTP_POOL_STACK_INFORMATION = ctypes.POINTER(struct__TP_POOL_STACK_INFORMATION)
TpQueryPoolStackInformation = _libraries['FIXME_STUB'].TpQueryPoolStackInformation
TpQueryPoolStackInformation.restype = NTSTATUS
TpQueryPoolStackInformation.argtypes = [PTP_POOL, PTP_POOL_STACK_INFORMATION]
TpSetPoolStackInformation = _libraries['FIXME_STUB'].TpSetPoolStackInformation
TpSetPoolStackInformation.restype = NTSTATUS
TpSetPoolStackInformation.argtypes = [PTP_POOL, PTP_POOL_STACK_INFORMATION]
class struct__TP_CLEANUP_GROUP(Structure):
    pass

TpAllocCleanupGroup = _libraries['FIXME_STUB'].TpAllocCleanupGroup
TpAllocCleanupGroup.restype = NTSTATUS
TpAllocCleanupGroup.argtypes = [ctypes.POINTER(ctypes.POINTER(struct__TP_CLEANUP_GROUP))]
PTP_CLEANUP_GROUP = ctypes.POINTER(struct__TP_CLEANUP_GROUP)
TpReleaseCleanupGroup = _libraries['FIXME_STUB'].TpReleaseCleanupGroup
TpReleaseCleanupGroup.restype = None
TpReleaseCleanupGroup.argtypes = [PTP_CLEANUP_GROUP]
TpReleaseCleanupGroupMembers = _libraries['FIXME_STUB'].TpReleaseCleanupGroupMembers
TpReleaseCleanupGroupMembers.restype = None
TpReleaseCleanupGroupMembers.argtypes = [PTP_CLEANUP_GROUP, LOGICAL, PVOID]
PTP_SIMPLE_CALLBACK = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct__TP_CALLBACK_INSTANCE), ctypes.POINTER(None))
class struct__TP_CALLBACK_ENVIRON_V3(Structure):
    pass


# values for enumeration '_TP_CALLBACK_PRIORITY'
_TP_CALLBACK_PRIORITY__enumvalues = {
    0: 'TP_CALLBACK_PRIORITY_HIGH',
    1: 'TP_CALLBACK_PRIORITY_NORMAL',
    2: 'TP_CALLBACK_PRIORITY_LOW',
    3: 'TP_CALLBACK_PRIORITY_INVALID',
    3: 'TP_CALLBACK_PRIORITY_COUNT',
}
TP_CALLBACK_PRIORITY_HIGH = 0
TP_CALLBACK_PRIORITY_NORMAL = 1
TP_CALLBACK_PRIORITY_LOW = 2
TP_CALLBACK_PRIORITY_INVALID = 3
TP_CALLBACK_PRIORITY_COUNT = 3
_TP_CALLBACK_PRIORITY = ctypes.c_uint32 # enum
class union_union_79(Union):
    pass

class struct_struct_80(Structure):
    pass

struct_struct_80._pack_ = 1 # source:False
struct_struct_80._fields_ = [
    ('LongFunction', ctypes.c_uint32, 1),
    ('Persistent', ctypes.c_uint32, 1),
    ('Private', ctypes.c_uint32, 30),
]

union_union_79._pack_ = 1 # source:False
union_union_79._fields_ = [
    ('Flags', ctypes.c_uint32),
    ('s', struct_struct_80),
]

struct__TP_CALLBACK_ENVIRON_V3._pack_ = 1 # source:False
struct__TP_CALLBACK_ENVIRON_V3._fields_ = [
    ('Version', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('Pool', ctypes.POINTER(struct__TP_POOL)),
    ('CleanupGroup', ctypes.POINTER(struct__TP_CLEANUP_GROUP)),
    ('CleanupGroupCancelCallback', ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(None))),
    ('RaceDll', ctypes.POINTER(None)),
    ('ActivationContext', ctypes.POINTER(struct__ACTIVATION_CONTEXT)),
    ('FinalizationCallback', ctypes.CFUNCTYPE(None, ctypes.POINTER(struct__TP_CALLBACK_INSTANCE), ctypes.POINTER(None))),
    ('u', union_union_79),
    ('CallbackPriority', _TP_CALLBACK_PRIORITY),
    ('Size', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
]

PTP_CALLBACK_ENVIRON = ctypes.POINTER(struct__TP_CALLBACK_ENVIRON_V3)
TpSimpleTryPost = _libraries['FIXME_STUB'].TpSimpleTryPost
TpSimpleTryPost.restype = NTSTATUS
TpSimpleTryPost.argtypes = [PTP_SIMPLE_CALLBACK, PVOID, PTP_CALLBACK_ENVIRON]
class struct__TP_WORK(Structure):
    pass

PTP_WORK_CALLBACK = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct__TP_CALLBACK_INSTANCE), ctypes.POINTER(None), ctypes.POINTER(struct__TP_WORK))
TpAllocWork = _libraries['FIXME_STUB'].TpAllocWork
TpAllocWork.restype = NTSTATUS
TpAllocWork.argtypes = [ctypes.POINTER(ctypes.POINTER(struct__TP_WORK)), PTP_WORK_CALLBACK, PVOID, PTP_CALLBACK_ENVIRON]
PTP_WORK = ctypes.POINTER(struct__TP_WORK)
TpReleaseWork = _libraries['FIXME_STUB'].TpReleaseWork
TpReleaseWork.restype = None
TpReleaseWork.argtypes = [PTP_WORK]
TpPostWork = _libraries['FIXME_STUB'].TpPostWork
TpPostWork.restype = None
TpPostWork.argtypes = [PTP_WORK]
TpWaitForWork = _libraries['FIXME_STUB'].TpWaitForWork
TpWaitForWork.restype = None
TpWaitForWork.argtypes = [PTP_WORK, LOGICAL]
class struct__TP_TIMER(Structure):
    pass

PTP_TIMER_CALLBACK = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct__TP_CALLBACK_INSTANCE), ctypes.POINTER(None), ctypes.POINTER(struct__TP_TIMER))
TpAllocTimer = _libraries['FIXME_STUB'].TpAllocTimer
TpAllocTimer.restype = NTSTATUS
TpAllocTimer.argtypes = [ctypes.POINTER(ctypes.POINTER(struct__TP_TIMER)), PTP_TIMER_CALLBACK, PVOID, PTP_CALLBACK_ENVIRON]
PTP_TIMER = ctypes.POINTER(struct__TP_TIMER)
TpReleaseTimer = _libraries['FIXME_STUB'].TpReleaseTimer
TpReleaseTimer.restype = None
TpReleaseTimer.argtypes = [PTP_TIMER]
TpSetTimer = _libraries['FIXME_STUB'].TpSetTimer
TpSetTimer.restype = None
TpSetTimer.argtypes = [PTP_TIMER, PLARGE_INTEGER, LONG, LONG]
TpIsTimerSet = _libraries['FIXME_STUB'].TpIsTimerSet
TpIsTimerSet.restype = LOGICAL
TpIsTimerSet.argtypes = [PTP_TIMER]
TpWaitForTimer = _libraries['FIXME_STUB'].TpWaitForTimer
TpWaitForTimer.restype = None
TpWaitForTimer.argtypes = [PTP_TIMER, LOGICAL]
class struct__TP_WAIT(Structure):
    pass

PTP_WAIT_CALLBACK = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct__TP_CALLBACK_INSTANCE), ctypes.POINTER(None), ctypes.POINTER(struct__TP_WAIT), ctypes.c_uint32)
TpAllocWait = _libraries['FIXME_STUB'].TpAllocWait
TpAllocWait.restype = NTSTATUS
TpAllocWait.argtypes = [ctypes.POINTER(ctypes.POINTER(struct__TP_WAIT)), PTP_WAIT_CALLBACK, PVOID, PTP_CALLBACK_ENVIRON]
PTP_WAIT = ctypes.POINTER(struct__TP_WAIT)
TpReleaseWait = _libraries['FIXME_STUB'].TpReleaseWait
TpReleaseWait.restype = None
TpReleaseWait.argtypes = [PTP_WAIT]
TpSetWait = _libraries['FIXME_STUB'].TpSetWait
TpSetWait.restype = None
TpSetWait.argtypes = [PTP_WAIT, HANDLE, PLARGE_INTEGER]
TpAllocIoCompletion = _libraries['FIXME_STUB'].TpAllocIoCompletion
TpAllocIoCompletion.restype = NTSTATUS
TpAllocIoCompletion.argtypes = [ctypes.POINTER(ctypes.POINTER(struct__TP_IO)), HANDLE, PTP_IO_CALLBACK, PVOID, PTP_CALLBACK_ENVIRON]
PTP_IO = ctypes.POINTER(struct__TP_IO)
TpWaitForIoCompletion = _libraries['FIXME_STUB'].TpWaitForIoCompletion
TpWaitForIoCompletion.restype = None
TpWaitForIoCompletion.argtypes = [PTP_IO, LOGICAL]
TpAllocAlpcCompletion = _libraries['FIXME_STUB'].TpAllocAlpcCompletion
TpAllocAlpcCompletion.restype = NTSTATUS
TpAllocAlpcCompletion.argtypes = [ctypes.POINTER(ctypes.POINTER(struct__TP_ALPC)), HANDLE, PTP_ALPC_CALLBACK, PVOID, PTP_CALLBACK_ENVIRON]
TpAllocAlpcCompletionEx = _libraries['FIXME_STUB'].TpAllocAlpcCompletionEx
TpAllocAlpcCompletionEx.restype = NTSTATUS
TpAllocAlpcCompletionEx.argtypes = [ctypes.POINTER(ctypes.POINTER(struct__TP_ALPC)), HANDLE, PTP_ALPC_CALLBACK_EX, PVOID, PTP_CALLBACK_ENVIRON]
TpReleaseAlpcCompletion = _libraries['FIXME_STUB'].TpReleaseAlpcCompletion
TpReleaseAlpcCompletion.restype = None
TpReleaseAlpcCompletion.argtypes = [PTP_ALPC]
TpWaitForAlpcCompletion = _libraries['FIXME_STUB'].TpWaitForAlpcCompletion
TpWaitForAlpcCompletion.restype = None
TpWaitForAlpcCompletion.argtypes = [PTP_ALPC]
TpAlpcRegisterCompletionList = _libraries['FIXME_STUB'].TpAlpcRegisterCompletionList
TpAlpcRegisterCompletionList.restype = NTSTATUS
TpAlpcRegisterCompletionList.argtypes = [PTP_ALPC]
TpAlpcUnregisterCompletionList = _libraries['FIXME_STUB'].TpAlpcUnregisterCompletionList
TpAlpcUnregisterCompletionList.restype = NTSTATUS
TpAlpcUnregisterCompletionList.argtypes = [PTP_ALPC]
# __all__ = \
#     ['ACCESS_MASK', 'ACTIVATION_CONTEXT_STACK',
#     'ALTERNATIVE_ARCHITECTURE_TYPE',
#     'ALTERNATIVE_ARCHITECTURE_TYPE__enumvalues', 'ANSI_STRING',
#     'AppendTailList', 'BOOL', 'BOOLEAN', 'BOOT_ENTRY',
#     'BOOT_ENTRY_LIST', 'BOOT_OPTIONS', 'CCHAR', 'CLIENT_ID', 'CURDIR',
#     'DBGKM_CREATE_PROCESS', 'DBGKM_CREATE_THREAD', 'DBGKM_EXCEPTION',
#     'DBGKM_EXIT_PROCESS', 'DBGKM_EXIT_THREAD', 'DBGKM_LOAD_DLL',
#     'DBGKM_UNLOAD_DLL', 'DBGSS_THREAD_DATA', 'DBGUI_CREATE_PROCESS',
#     'DBGUI_CREATE_THREAD', 'DBGUI_WAIT_STATE_CHANGE', 'DBG_STATE',
#     'DBG_STATE__enumvalues', 'DEBUGOBJECTINFOCLASS',
#     'DEBUGOBJECTINFOCLASS__enumvalues', 'DWORD', 'DbgBreakPoint',
#     'DbgBreakpointStateChange', 'DbgCreateProcessStateChange',
#     'DbgCreateThreadStateChange', 'DbgExceptionStateChange',
#     'DbgExitProcessStateChange', 'DbgExitThreadStateChange',
#     'DbgIdle', 'DbgLoadDllStateChange', 'DbgPrint', 'DbgPrintEx',
#     'DbgReplyPending', 'DbgSingleStepStateChange',
#     'DbgUiConnectToDbg', 'DbgUiContinue',
#     'DbgUiConvertStateChangeStructure', 'DbgUiDebugActiveProcess',
#     'DbgUiGetThreadDebugObject', 'DbgUiIssueRemoteBreakin',
#     'DbgUiRemoteBreakin', 'DbgUiSetThreadDebugObject',
#     'DbgUiStopDebugging', 'DbgUiWaitStateChange',
#     'DbgUnloadDllStateChange', 'DebugObjectFlags', 'DeferredReady',
#     'DelayExecution', 'EFI_DRIVER_ENTRY', 'EFI_DRIVER_ENTRY_LIST',
#     'ENLISTMENT_INFORMATION_CLASS',
#     'ENLISTMENT_INFORMATION_CLASS__enumvalues', 'EVENT_TYPE',
#     'EVENT_TYPE__enumvalues', 'EndAlternatives',
#     'EnlistmentBasicInformation', 'EnlistmentCrmInformation',
#     'EnlistmentRecoveryInformation', 'ExceptionCollidedUnwind',
#     'ExceptionContinueExecution', 'ExceptionContinueSearch',
#     'ExceptionNestedException', 'Executive', 'FILE_BASIC_INFORMATION',
#     'FILE_COMPLETION_INFORMATION', 'FILE_INFORMATION_CLASS',
#     'FILE_INFORMATION_CLASS__enumvalues',
#     'FILE_IO_COMPLETION_INFORMATION', 'FILE_NETWORK_OPEN_INFORMATION',
#     'FILE_NOTIFY_INFORMATION', 'FILE_PATH', 'FILE_PIPE_PEEK_BUFFER',
#     'FILE_POSITION_INFORMATION', 'FILE_STANDARD_INFORMATION',
#     'FILTER_BOOT_OPTION_OPERATION',
#     'FILTER_BOOT_OPTION_OPERATION__enumvalues',
#     'FS_INFORMATION_CLASS', 'FS_INFORMATION_CLASS__enumvalues',
#     'FileAccessInformation', 'FileAlignmentInformation',
#     'FileAllInformation', 'FileAllocationInformation',
#     'FileAlternateNameInformation', 'FileAttributeTagInformation',
#     'FileBasicInformation', 'FileBothDirectoryInformation',
#     'FileCompletionInformation', 'FileCompressionInformation',
#     'FileDesiredStorageClassInformation', 'FileDirectoryInformation',
#     'FileDispositionInformation', 'FileDispositionInformationEx',
#     'FileEaInformation', 'FileEndOfFileInformation',
#     'FileFsAttributeInformation', 'FileFsControlInformation',
#     'FileFsDataCopyInformation', 'FileFsDeviceInformation',
#     'FileFsDriverPathInformation', 'FileFsFullSizeInformation',
#     'FileFsLabelInformation', 'FileFsMaximumInformation',
#     'FileFsMetadataSizeInformation', 'FileFsObjectIdInformation',
#     'FileFsSectorSizeInformation', 'FileFsSizeInformation',
#     'FileFsVolumeFlagsInformation', 'FileFsVolumeInformation',
#     'FileFullDirectoryInformation', 'FileFullEaInformation',
#     'FileHardLinkFullIdInformation', 'FileHardLinkInformation',
#     'FileIdBothDirectoryInformation',
#     'FileIdExtdBothDirectoryInformation',
#     'FileIdExtdDirectoryInformation',
#     'FileIdFullDirectoryInformation',
#     'FileIdGlobalTxDirectoryInformation', 'FileIdInformation',
#     'FileInternalInformation',
#     'FileIoCompletionNotificationInformation',
#     'FileIoPriorityHintInformation',
#     'FileIoStatusBlockRangeInformation',
#     'FileIsRemoteDeviceInformation', 'FileLinkInformation',
#     'FileLinkInformationBypassAccessCheck',
#     'FileMailslotQueryInformation', 'FileMailslotSetInformation',
#     'FileMaximumInformation', 'FileModeInformation',
#     'FileMoveClusterInformation', 'FileNameInformation',
#     'FileNamesInformation', 'FileNetworkOpenInformation',
#     'FileNetworkPhysicalNameInformation',
#     'FileNormalizedNameInformation', 'FileNumaNodeInformation',
#     'FileObjectIdInformation', 'FilePipeInformation',
#     'FilePipeLocalInformation', 'FilePipeRemoteInformation',
#     'FilePositionInformation', 'FileProcessIdsUsingFileInformation',
#     'FileQuotaInformation', 'FileRemoteProtocolInformation',
#     'FileRenameInformation', 'FileRenameInformationBypassAccessCheck',
#     'FileRenameInformationEx',
#     'FileRenameInformationExBypassAccessCheck',
#     'FileReparsePointInformation', 'FileReplaceCompletionInformation',
#     'FileSfioReserveInformation', 'FileSfioVolumeInformation',
#     'FileShortNameInformation', 'FileStandardInformation',
#     'FileStandardLinkInformation', 'FileStatInformation',
#     'FileStreamInformation', 'FileTrackingInformation',
#     'FileUnusedInformation', 'FileValidDataLengthInformation',
#     'FileVolumeNameInformation',
#     'FilterBootOptionOperationDeleteElement',
#     'FilterBootOptionOperationMax',
#     'FilterBootOptionOperationOpenSystemStore',
#     'FilterBootOptionOperationSetElement', 'FreePage',
#     'GDI_HANDLE_BUFFER', 'GDI_HANDLE_BUFFER32', 'GDI_HANDLE_BUFFER64',
#     'GDI_TEB_BATCH', 'GateWaitObsolete', 'HANDLE',
#     'HARDERROR_RESPONSE', 'HARDERROR_RESPONSE_OPTION',
#     'HARDERROR_RESPONSE_OPTION__enumvalues',
#     'HARDERROR_RESPONSE__enumvalues', 'HEAP_DEBUGGING_INFORMATION',
#     'HEAP_EXTENDED_INFORMATION', 'HEAP_INFORMATION',
#     'HEAP_INFORMATION_CLASS', 'HEAP_INFORMATION_CLASS__enumvalues',
#     'HeapCompatibilityInformation',
#     'HeapEnableTerminationOnCorruption', 'HeapOptimizeResources',
#     'INITIAL_TEB', 'IO_COMPLETION_BASIC_INFORMATION',
#     'IO_COMPLETION_INFORMATION_CLASS',
#     'IO_COMPLETION_INFORMATION_CLASS__enumvalues', 'IO_SESSION_EVENT',
#     'IO_SESSION_EVENT__enumvalues', 'IO_SESSION_STATE',
#     'IO_SESSION_STATE__enumvalues', 'IO_STATUS_BLOCK',
#     'InitializeListHead', 'Initialized', 'InsertHeadList',
#     'InsertTailList', 'IoCompletionBasicInformation',
#     'IoSessionEventConnected', 'IoSessionEventCreated',
#     'IoSessionEventDisconnected', 'IoSessionEventIgnore',
#     'IoSessionEventLogoff', 'IoSessionEventLogon',
#     'IoSessionEventMax', 'IoSessionEventTerminated',
#     'IoSessionStateConnected', 'IoSessionStateCreated',
#     'IoSessionStateDisconnected',
#     'IoSessionStateDisconnectedLoggedOn', 'IoSessionStateInitialized',
#     'IoSessionStateLoggedOff', 'IoSessionStateLoggedOn',
#     'IoSessionStateMax', 'IoSessionStateTerminated', 'IsListEmpty',
#     'KERNEL_USER_TIMES', 'KEY_BASIC_INFORMATION',
#     'KEY_CACHED_INFORMATION', 'KEY_CONTROL_FLAGS_INFORMATION',
#     'KEY_FLAGS_INFORMATION', 'KEY_FULL_INFORMATION',
#     'KEY_HANDLE_TAGS_INFORMATION', 'KEY_INFORMATION_CLASS',
#     'KEY_INFORMATION_CLASS__enumvalues', 'KEY_LAYER_INFORMATION',
#     'KEY_NAME_INFORMATION', 'KEY_NODE_INFORMATION',
#     'KEY_OPEN_SUBKEYS_INFORMATION', 'KEY_PID_ARRAY',
#     'KEY_SET_INFORMATION_CLASS',
#     'KEY_SET_INFORMATION_CLASS__enumvalues',
#     'KEY_SET_VIRTUALIZATION_INFORMATION', 'KEY_TRUST_INFORMATION',
#     'KEY_VALUE_BASIC_INFORMATION', 'KEY_VALUE_ENTRY',
#     'KEY_VALUE_FULL_INFORMATION', 'KEY_VALUE_INFORMATION_CLASS',
#     'KEY_VALUE_INFORMATION_CLASS__enumvalues',
#     'KEY_VALUE_LAYER_INFORMATION', 'KEY_VALUE_PARTIAL_INFORMATION',
#     'KEY_VALUE_PARTIAL_INFORMATION_ALIGN64',
#     'KEY_VIRTUALIZATION_INFORMATION', 'KEY_WOW64_FLAGS_INFORMATION',
#     'KEY_WRITE_TIME_INFORMATION', 'KPRIORITY', 'KPROCESSOR_MODE',
#     'KSYSTEM_TIME', 'KTHREAD_STATE', 'KTHREAD_STATE__enumvalues',
#     'KTMOBJECT_ENLISTMENT', 'KTMOBJECT_INVALID',
#     'KTMOBJECT_RESOURCE_MANAGER', 'KTMOBJECT_TRANSACTION',
#     'KTMOBJECT_TRANSACTION_MANAGER', 'KTMOBJECT_TYPE',
#     'KTMOBJECT_TYPE__enumvalues', 'KUSER_SHARED_DATA', 'KWAIT_REASON',
#     'KWAIT_REASON__enumvalues', 'KernelMode', 'KeyAdded',
#     'KeyBasicInformation', 'KeyCachedInformation',
#     'KeyControlFlagsInformation', 'KeyFlagsInformation',
#     'KeyFullInformation', 'KeyHandleTagsInformation',
#     'KeyLayerInformation', 'KeyModified', 'KeyNameInformation',
#     'KeyNodeInformation', 'KeyRemoved', 'KeySetDebugInformation',
#     'KeySetHandleTagsInformation', 'KeySetVirtualizationInformation',
#     'KeyTrustInformation', 'KeyValueBasicInformation',
#     'KeyValueFullInformation', 'KeyValueFullInformationAlign64',
#     'KeyValueLayerInformation', 'KeyValuePartialInformation',
#     'KeyValuePartialInformationAlign64',
#     'KeyVirtualizationInformation', 'KeyWow64FlagsInformation',
#     'KeyWriteTimeInformation', 'LDRP_CSLIST', 'LDR_DATA_TABLE_ENTRY',
#     'LDR_DDAG_NODE', 'LDR_DDAG_STATE', 'LDR_DDAG_STATE__enumvalues',
#     'LDR_DEPENDENCY_RECORD', 'LDR_DLL_LOAD_REASON',
#     'LDR_DLL_LOAD_REASON__enumvalues', 'LDR_ENUM_RESOURCE_INFO',
#     'LDR_IMPORT_CALLBACK_INFO', 'LDR_RESOURCE_INFO',
#     'LDR_SECTION_INFO', 'LDR_SERVICE_TAG_RECORD',
#     'LDR_VERIFY_IMAGE_INFO', 'LOGICAL', 'LONG', 'LONG_PTR', 'LPGUID',
#     'LdrDisableThreadCalloutsForDll', 'LdrFindResourceDirectory_U',
#     'LdrFindResourceEx_U', 'LdrFindResource_U', 'LdrGetDllHandle',
#     'LdrGetDllHandleByMapping', 'LdrGetDllHandleByName',
#     'LdrGetDllHandleEx', 'LdrGetProcedureAddress',
#     'LdrGetProcedureAddressEx', 'LdrLoadDll', 'LdrLockLoaderLock',
#     'LdrModulesCondensed', 'LdrModulesInitError',
#     'LdrModulesInitializing', 'LdrModulesMapped', 'LdrModulesMapping',
#     'LdrModulesMerged', 'LdrModulesPlaceHolder',
#     'LdrModulesReadyToInit', 'LdrModulesReadyToRun',
#     'LdrModulesSnapError', 'LdrModulesSnapped', 'LdrModulesSnapping',
#     'LdrModulesUnloaded', 'LdrModulesUnloading',
#     'LdrModulesWaitingForDependencies', 'LdrOpenImageFileOptionsKey',
#     'LdrProcessRelocationBlock', 'LdrQueryImageFileKeyOption',
#     'LdrUnloadDll', 'LdrUnlockLoaderLock',
#     'LdrVerifyImageMatchesChecksum',
#     'LdrVerifyImageMatchesChecksumEx', 'LoadReasonAsDataLoad',
#     'LoadReasonAsImageLoad', 'LoadReasonDelayloadDependency',
#     'LoadReasonDynamicForwarderDependency', 'LoadReasonDynamicLoad',
#     'LoadReasonStaticDependency',
#     'LoadReasonStaticForwarderDependency', 'LoadReasonUnknown',
#     'MEMORY_INFORMATION_CLASS',
#     'MEMORY_INFORMATION_CLASS__enumvalues',
#     'MEMORY_REGION_INFORMATION', 'MEMORY_RESERVE_TYPE',
#     'MEMORY_RESERVE_TYPE__enumvalues', 'MaxDebugObjectInfoClass',
#     'MaxKeyInfoClass', 'MaxKeySetInfoClass', 'MaxKeyValueInfoClass',
#     'MaxObjectInfoClass', 'MaxProcessInfoClass',
#     'MaxSectionInfoClass', 'MaxSystemInfoClass', 'MaxThreadInfoClass',
#     'MaxTimerInfoClass', 'MaxTokenInfoClass',
#     'MaxWorkerFactoryInfoClass', 'MaximumThreadState',
#     'MaximumWaitReason', 'MemoryBasicInformation',
#     'MemoryImageInformation', 'MemoryMappedFilenameInformation',
#     'MemoryPrivilegedBasicInformation', 'MemoryRegionInformation',
#     'MemoryRegionInformationEx', 'MemoryReserveIoCompletion',
#     'MemoryReserveTypeMax', 'MemoryReserveUserApc',
#     'MemorySharedCommitInformation', 'MemoryWorkingSetExInformation',
#     'MemoryWorkingSetInformation', 'NAMED_PIPE_CREATE_PARAMETERS',
#     'NEC98x86', 'NOTIFICATION_MASK', 'NTSTATUS', 'NotificationEvent',
#     'NotificationTimer', 'NtAccessCheck', 'NtAccessCheckByType',
#     'NtAccessCheckByTypeResultList', 'NtAddBootEntry',
#     'NtAddDriverEntry', 'NtAdjustGroupsToken',
#     'NtAdjustPrivilegesToken', 'NtAlertResumeThread', 'NtAlertThread',
#     'NtAllocateLocallyUniqueId', 'NtAllocateReserveObject',
#     'NtAllocateUserPhysicalPages', 'NtAllocateUuids',
#     'NtAllocateVirtualMemory', 'NtAreMappedFilesTheSame',
#     'NtCallbackReturn', 'NtCancelIoFile', 'NtCancelIoFileEx',
#     'NtCancelSynchronousIoFile', 'NtCancelTimer', 'NtClearEvent',
#     'NtClose', 'NtCommitComplete', 'NtCommitEnlistment',
#     'NtCommitTransaction', 'NtCompactKeys', 'NtCompareTokens',
#     'NtCompressKey', 'NtContinue', 'NtCreateDebugObject',
#     'NtCreateDirectoryObject', 'NtCreateEnlistment', 'NtCreateEvent',
#     'NtCreateFile', 'NtCreateIoCompletion', 'NtCreateKey',
#     'NtCreateKeyTransacted', 'NtCreateKeyedEvent',
#     'NtCreateMailslotFile', 'NtCreateMutant', 'NtCreateNamedPipeFile',
#     'NtCreatePrivateNamespace', 'NtCreateProcess',
#     'NtCreateProcessEx', 'NtCreateResourceManager', 'NtCreateSection',
#     'NtCreateSemaphore', 'NtCreateSymbolicLinkObject',
#     'NtCreateThread', 'NtCreateThreadEx', 'NtCreateTimer',
#     'NtCreateToken', 'NtCreateTransaction',
#     'NtCreateTransactionManager', 'NtCreateUserProcess',
#     'NtCreateWorkerFactory', 'NtDebugActiveProcess',
#     'NtDebugContinue', 'NtDelayExecution', 'NtDeleteBootEntry',
#     'NtDeleteDriverEntry', 'NtDeleteFile', 'NtDeleteKey',
#     'NtDeletePrivateNamespace', 'NtDeleteValueKey',
#     'NtDeviceIoControlFile', 'NtDisableLastKnownGood',
#     'NtDuplicateObject', 'NtDuplicateToken', 'NtEnableLastKnownGood',
#     'NtEnumerateBootEntries', 'NtEnumerateDriverEntries',
#     'NtEnumerateKey', 'NtEnumerateSystemEnvironmentValuesEx',
#     'NtEnumerateTransactionObject', 'NtEnumerateValueKey',
#     'NtExtendSection', 'NtFilterToken', 'NtFlushBuffersFile',
#     'NtFlushInstructionCache', 'NtFlushKey',
#     'NtFlushProcessWriteBuffers', 'NtFlushVirtualMemory',
#     'NtFlushWriteBuffer', 'NtFreeUserPhysicalPages',
#     'NtFreeVirtualMemory', 'NtFreezeRegistry', 'NtFreezeTransactions',
#     'NtFsControlFile', 'NtGetContextThread',
#     'NtGetCurrentProcessorNumber', 'NtGetNextProcess',
#     'NtGetNextThread', 'NtGetNotificationResourceManager',
#     'NtImpersonateAnonymousToken', 'NtImpersonateThread',
#     'NtInitializeRegistry', 'NtLoadDriver', 'NtLoadKey', 'NtLoadKey2',
#     'NtLoadKeyEx', 'NtLockFile', 'NtLockProductActivationKeys',
#     'NtLockRegistryKey', 'NtLockVirtualMemory',
#     'NtMakePermanentObject', 'NtMakeTemporaryObject',
#     'NtMapUserPhysicalPages', 'NtMapUserPhysicalPagesScatter',
#     'NtMapViewOfSection', 'NtModifyBootEntry', 'NtModifyDriverEntry',
#     'NtNotifyChangeDirectoryFile', 'NtNotifyChangeKey',
#     'NtNotifyChangeMultipleKeys', 'NtNotifyChangeSession',
#     'NtOpenDirectoryObject', 'NtOpenEnlistment', 'NtOpenEvent',
#     'NtOpenFile', 'NtOpenIoCompletion', 'NtOpenKey', 'NtOpenKeyEx',
#     'NtOpenKeyTransacted', 'NtOpenKeyTransactedEx',
#     'NtOpenKeyedEvent', 'NtOpenMutant', 'NtOpenPrivateNamespace',
#     'NtOpenProcess', 'NtOpenProcessToken', 'NtOpenProcessTokenEx',
#     'NtOpenResourceManager', 'NtOpenSection', 'NtOpenSemaphore',
#     'NtOpenSession', 'NtOpenSymbolicLinkObject', 'NtOpenThread',
#     'NtOpenThreadToken', 'NtOpenThreadTokenEx', 'NtOpenTimer',
#     'NtOpenTransaction', 'NtOpenTransactionManager',
#     'NtPrePrepareComplete', 'NtPrePrepareEnlistment',
#     'NtPrepareComplete', 'NtPrepareEnlistment', 'NtPrivilegeCheck',
#     'NtPropagationComplete', 'NtPropagationFailed',
#     'NtProtectVirtualMemory', 'NtQueryAttributesFile',
#     'NtQueryBootEntryOrder', 'NtQueryBootOptions',
#     'NtQueryDebugFilterState', 'NtQueryDirectoryFile',
#     'NtQueryDirectoryObject', 'NtQueryDriverEntryOrder',
#     'NtQueryEaFile', 'NtQueryFullAttributesFile',
#     'NtQueryInformationEnlistment', 'NtQueryInformationFile',
#     'NtQueryInformationProcess', 'NtQueryInformationResourceManager',
#     'NtQueryInformationThread', 'NtQueryInformationTransaction',
#     'NtQueryInformationTransactionManager',
#     'NtQueryInformationWorkerFactory', 'NtQueryIoCompletion',
#     'NtQueryKey', 'NtQueryMultipleValueKey', 'NtQueryObject',
#     'NtQueryOpenSubKeys', 'NtQueryOpenSubKeysEx',
#     'NtQueryPerformanceCounter', 'NtQueryQuotaInformationFile',
#     'NtQuerySection', 'NtQuerySecurityAttributesToken',
#     'NtQuerySecurityObject', 'NtQuerySemaphore',
#     'NtQuerySymbolicLinkObject', 'NtQuerySystemEnvironmentValue',
#     'NtQuerySystemEnvironmentValueEx', 'NtQuerySystemInformation',
#     'NtQuerySystemInformationEx', 'NtQuerySystemTime', 'NtQueryTimer',
#     'NtQueryTimerResolution', 'NtQueryValueKey',
#     'NtQueryVirtualMemory', 'NtQueryVolumeInformationFile',
#     'NtQueueApcThread', 'NtQueueApcThreadEx', 'NtRaiseException',
#     'NtRaiseHardError', 'NtReadFile', 'NtReadFileScatter',
#     'NtReadOnlyEnlistment', 'NtReadVirtualMemory',
#     'NtRecoverEnlistment', 'NtRecoverResourceManager',
#     'NtRecoverTransactionManager',
#     'NtRegisterProtocolAddressInformation',
#     'NtRegisterThreadTerminatePort', 'NtReleaseKeyedEvent',
#     'NtReleaseMutant', 'NtReleaseSemaphore',
#     'NtReleaseWorkerFactoryWorker', 'NtRemoveIoCompletion',
#     'NtRemoveIoCompletionEx', 'NtRemoveProcessDebug', 'NtRenameKey',
#     'NtRenameTransactionManager', 'NtReplaceKey', 'NtResetEvent',
#     'NtRestoreKey', 'NtResumeProcess', 'NtResumeThread',
#     'NtRollbackComplete', 'NtRollbackEnlistment',
#     'NtRollbackTransaction', 'NtRollforwardTransactionManager',
#     'NtSaveKey', 'NtSaveKeyEx', 'NtSaveMergedKeys', 'NtSerializeBoot',
#     'NtSetBootEntryOrder', 'NtSetBootOptions', 'NtSetContextThread',
#     'NtSetDebugFilterState', 'NtSetDriverEntryOrder', 'NtSetEaFile',
#     'NtSetEvent', 'NtSetInformationDebugObject',
#     'NtSetInformationEnlistment', 'NtSetInformationFile',
#     'NtSetInformationKey', 'NtSetInformationObject',
#     'NtSetInformationProcess', 'NtSetInformationResourceManager',
#     'NtSetInformationThread', 'NtSetInformationToken',
#     'NtSetInformationTransaction',
#     'NtSetInformationTransactionManager',
#     'NtSetInformationWorkerFactory', 'NtSetIoCompletion',
#     'NtSetIoCompletionEx', 'NtSetQuotaInformationFile',
#     'NtSetSecurityObject', 'NtSetSystemEnvironmentValue',
#     'NtSetSystemEnvironmentValueEx', 'NtSetSystemInformation',
#     'NtSetSystemTime', 'NtSetTimer', 'NtSetTimerEx',
#     'NtSetTimerResolution', 'NtSetUuidSeed', 'NtSetValueKey',
#     'NtSetVolumeInformationFile', 'NtShutdownWorkerFactory',
#     'NtSignalAndWaitForSingleObject', 'NtSinglePhaseReject',
#     'NtSuspendProcess', 'NtSuspendThread', 'NtSystemDebugControl',
#     'NtTerminateProcess', 'NtTerminateThread', 'NtTestAlert',
#     'NtThawRegistry', 'NtThawTransactions', 'NtTranslateFilePath',
#     'NtUmsThreadYield', 'NtUnloadDriver', 'NtUnloadKey',
#     'NtUnloadKey2', 'NtUnloadKeyEx', 'NtUnlockFile',
#     'NtUnlockVirtualMemory', 'NtUnmapViewOfSection',
#     'NtWaitForDebugEvent', 'NtWaitForKeyedEvent',
#     'NtWaitForMultipleObjects', 'NtWaitForMultipleObjects32',
#     'NtWaitForSingleObject', 'NtWaitForWorkViaWorkerFactory',
#     'NtWorkerFactoryWorkerReady', 'NtWriteFile', 'NtWriteFileGather',
#     'NtWriteVirtualMemory', 'NtYieldExecution', 'OBJECT_ATTRIBUTES',
#     'OBJECT_BASIC_INFORMATION', 'OBJECT_HANDLE_FLAG_INFORMATION',
#     'OBJECT_INFORMATION_CLASS',
#     'OBJECT_INFORMATION_CLASS__enumvalues', 'OBJECT_NAME_INFORMATION',
#     'OBJECT_TYPES_INFORMATION', 'OBJECT_TYPE_INFORMATION',
#     'ObjectBasicInformation', 'ObjectHandleFlagInformation',
#     'ObjectNameInformation', 'ObjectSessionInformation',
#     'ObjectSessionObjectInformation', 'ObjectTypeInformation',
#     'ObjectTypesInformation', 'OptionAbortRetryIgnore',
#     'OptionCancelTryContinue', 'OptionOk', 'OptionOkCancel',
#     'OptionOkNoWait', 'OptionRetryCancel', 'OptionShutdownSystem',
#     'OptionYesNo', 'OptionYesNoCancel', 'PACCESS_MASK', 'PACL',
#     'PACTIVATION_CONTEXT_STACK', 'PANSI_STRING', 'PBOOLEAN',
#     'PBOOT_ENTRY', 'PBOOT_ENTRY_LIST', 'PBOOT_OPTIONS', 'PCH',
#     'PCHAR', 'PCLIENT_ID', 'PCONTEXT', 'PCRM_PROTOCOL_ID', 'PCSTR',
#     'PCUNICODE_STRING', 'PCURDIR', 'PCWSTR', 'PDBGKM_CREATE_PROCESS',
#     'PDBGKM_CREATE_THREAD', 'PDBGKM_EXCEPTION', 'PDBGKM_EXIT_PROCESS',
#     'PDBGKM_EXIT_THREAD', 'PDBGKM_LOAD_DLL', 'PDBGKM_UNLOAD_DLL',
#     'PDBGSS_THREAD_DATA', 'PDBGUI_CREATE_PROCESS',
#     'PDBGUI_CREATE_THREAD', 'PDBGUI_WAIT_STATE_CHANGE', 'PDBG_STATE',
#     'PDEBUGOBJECTINFOCLASS', 'PEB', 'PEB_LDR_DATA',
#     'PEFI_DRIVER_ENTRY', 'PEFI_DRIVER_ENTRY_LIST',
#     'PEXCEPTION_RECORD', 'PFILE_BASIC_INFORMATION',
#     'PFILE_COMPLETION_INFORMATION', 'PFILE_INFORMATION_CLASS',
#     'PFILE_IO_COMPLETION_INFORMATION',
#     'PFILE_NETWORK_OPEN_INFORMATION', 'PFILE_PATH',
#     'PFILE_PIPE_PEEK_BUFFER', 'PFILE_POSITION_INFORMATION',
#     'PFILE_SEGMENT_ELEMENT', 'PFILE_STANDARD_INFORMATION',
#     'PFS_INFORMATION_CLASS', 'PGDI_TEB_BATCH', 'PGENERIC_MAPPING',
#     'PHANDLE', 'PHARDERROR_RESPONSE', 'PHARDERROR_RESPONSE_OPTION',
#     'PHEAP_DEBUGGING_INFORMATION', 'PHEAP_EXTENDED_INFORMATION',
#     'PHEAP_INFORMATION', 'PIMAGE_BASE_RELOCATION',
#     'PIMAGE_NT_HEADERS', 'PIMAGE_SECTION_HEADER', 'PINITIAL_TEB',
#     'PIO_APC_ROUTINE', 'PIO_COMPLETION_BASIC_INFORMATION',
#     'PIO_STATUS_BLOCK', 'PKERNEL_USER_TIMES',
#     'PKEY_BASIC_INFORMATION', 'PKEY_CACHED_INFORMATION',
#     'PKEY_CONTROL_FLAGS_INFORMATION', 'PKEY_FLAGS_INFORMATION',
#     'PKEY_FULL_INFORMATION', 'PKEY_HANDLE_TAGS_INFORMATION',
#     'PKEY_LAYER_INFORMATION', 'PKEY_NAME_INFORMATION',
#     'PKEY_NODE_INFORMATION', 'PKEY_OPEN_SUBKEYS_INFORMATION',
#     'PKEY_PID_ARRAY', 'PKEY_SET_VIRTUALIZATION_INFORMATION',
#     'PKEY_TRUST_INFORMATION', 'PKEY_VALUE_BASIC_INFORMATION',
#     'PKEY_VALUE_ENTRY', 'PKEY_VALUE_FULL_INFORMATION',
#     'PKEY_VALUE_LAYER_INFORMATION', 'PKEY_VALUE_PARTIAL_INFORMATION',
#     'PKEY_VALUE_PARTIAL_INFORMATION_ALIGN64',
#     'PKEY_VIRTUALIZATION_INFORMATION', 'PKEY_WOW64_FLAGS_INFORMATION',
#     'PKEY_WRITE_TIME_INFORMATION', 'PKPRIORITY', 'PKSYSTEM_TIME',
#     'PKTHREAD_STATE', 'PKTMOBJECT_CURSOR', 'PKUSER_SHARED_DATA',
#     'PLARGE_INTEGER', 'PLDRP_CSLIST', 'PLDR_DATA_TABLE_ENTRY',
#     'PLDR_DDAG_NODE', 'PLDR_DEPENDENCY_RECORD',
#     'PLDR_DLL_LOAD_REASON', 'PLDR_ENUM_RESOURCE_INFO',
#     'PLDR_IMPORT_CALLBACK_INFO', 'PLDR_IMPORT_MODULE_CALLBACK',
#     'PLDR_RESOURCE_INFO', 'PLDR_SECTION_INFO',
#     'PLDR_SERVICE_TAG_RECORD', 'PLDR_VERIFY_IMAGE_INFO',
#     'PLIST_ENTRY', 'PLOGICAL', 'PLONG', 'PLUID',
#     'PMEMORY_REGION_INFORMATION', 'PNAMED_PIPE_CREATE_PARAMETERS',
#     'PNTSTATUS', 'POBJECT_ATTRIBUTES', 'POBJECT_BASIC_INFORMATION',
#     'POBJECT_HANDLE_FLAG_INFORMATION', 'POBJECT_NAME_INFORMATION',
#     'POBJECT_TYPES_INFORMATION', 'POBJECT_TYPE_INFORMATION',
#     'POBJECT_TYPE_LIST', 'PORT_MESSAGE', 'PPEB', 'PPEB_LDR_DATA',
#     'PPORT_MESSAGE', 'PPREFIX_TABLE', 'PPREFIX_TABLE_ENTRY',
#     'PPRIVILEGE_SET', 'PPROCESS_ACCESS_TOKEN',
#     'PPROCESS_BASIC_INFORMATION',
#     'PPROCESS_EXTENDED_BASIC_INFORMATION',
#     'PPROCESS_HANDLE_TRACING_ENABLE',
#     'PPROCESS_HANDLE_TRACING_ENABLE_EX', 'PPROCESS_HEAP_INFORMATION',
#     'PPROCESS_LDT_INFORMATION', 'PPROCESS_PRIORITY_CLASS',
#     'PPROCESS_SESSION_INFORMATION', 'PPS_APC_ROUTINE',
#     'PPS_ATTRIBUTE', 'PPS_ATTRIBUTE_LIST',
#     'PPS_BNO_ISOLATION_PARAMETERS', 'PPS_CREATE_INFO',
#     'PPS_MEMORY_RESERVE', 'PPS_PROTECTION', 'PPS_STD_HANDLE_INFO',
#     'PREFIX_TABLE', 'PREFIX_TABLE_ENTRY', 'PREG_NOTIFY_INFORMATION',
#     'PRIORITY_CLASS', 'PROCESSINFOCLASS',
#     'PROCESSINFOCLASS__enumvalues', 'PROCESS_ACCESS_TOKEN',
#     'PROCESS_BASIC_INFORMATION', 'PROCESS_EXTENDED_BASIC_INFORMATION',
#     'PROCESS_HANDLE_TRACING_ENABLE',
#     'PROCESS_HANDLE_TRACING_ENABLE_EX', 'PROCESS_HEAP_INFORMATION',
#     'PROCESS_LDT_INFORMATION', 'PROCESS_PRIORITY_CLASS',
#     'PROCESS_SESSION_INFORMATION', 'PRTLP_CURDIR_REF', 'PRTL_ATOM',
#     'PRTL_BALANCED_NODE', 'PRTL_BITMAP', 'PRTL_BITMAP_RUN',
#     'PRTL_BSD_ITEM_TYPE', 'PRTL_BUFFER', 'PRTL_CRITICAL_SECTION',
#     'PRTL_DEBUG_INFORMATION', 'PRTL_DRIVE_LETTER_CURDIR',
#     'PRTL_ENUM_HEAPS_ROUTINE', 'PRTL_HEAP_COMMIT_ROUTINE',
#     'PRTL_HEAP_ENTRY', 'PRTL_HEAP_INFORMATION',
#     'PRTL_HEAP_LEAK_ENUMERATION_ROUTINE', 'PRTL_HEAP_PARAMETERS',
#     'PRTL_HEAP_TAG', 'PRTL_HEAP_TAG_INFO', 'PRTL_HEAP_WALK_ENTRY',
#     'PRTL_OSVERSIONINFOW', 'PRTL_PROCESS_HEAPS',
#     'PRTL_PROCESS_MODULES', 'PRTL_PROCESS_MODULE_INFORMATION',
#     'PRTL_PROCESS_MODULE_INFORMATION_EX',
#     'PRTL_PROCESS_VERIFIER_OPTIONS', 'PRTL_RELATIVE_NAME_U',
#     'PRTL_SPLAY_LINKS', 'PRTL_SRWLOCK', 'PRTL_UNICODE_STRING_BUFFER',
#     'PRTL_USER_PROCESS_INFORMATION', 'PRTL_USER_PROCESS_PARAMETERS',
#     'PSECTION_BASIC_INFORMATION', 'PSECTION_IMAGE_INFORMATION',
#     'PSECTION_INTERNAL_IMAGE_INFORMATION', 'PSECURITY_DESCRIPTOR',
#     'PSECURITY_QUALITY_OF_SERVICE', 'PSEMAPHORE_BASIC_INFORMATION',
#     'PSID', 'PSID_IDENTIFIER_AUTHORITY', 'PSINGLE_LIST_ENTRY',
#     'PSIZE_T', 'PSTR', 'PSYSDBG_COMMAND', 'PSYSTEM_BASIC_INFORMATION',
#     'PSYSTEM_CONSOLE_INFORMATION',
#     'PSYSTEM_EXTENDED_THREAD_INFORMATION',
#     'PSYSTEM_HANDLE_INFORMATION', 'PSYSTEM_HANDLE_INFORMATION_EX',
#     'PSYSTEM_HANDLE_TABLE_ENTRY_INFO',
#     'PSYSTEM_HANDLE_TABLE_ENTRY_INFO_EX',
#     'PSYSTEM_KERNEL_DEBUGGER_INFORMATION',
#     'PSYSTEM_KERNEL_DEBUGGER_INFORMATION_EX',
#     'PSYSTEM_PROCESS_INFORMATION',
#     'PSYSTEM_SESSION_PROCESS_INFORMATION',
#     'PSYSTEM_THREAD_INFORMATION', 'PSYSTEM_TIMEOFDAY_INFORMATION',
#     'PS_ATTRIBUTE', 'PS_ATTRIBUTE_LIST', 'PS_ATTRIBUTE_NUM',
#     'PS_ATTRIBUTE_NUM__enumvalues', 'PS_BNO_ISOLATION_PARAMETERS',
#     'PS_CREATE_INFO', 'PS_CREATE_STATE',
#     'PS_CREATE_STATE__enumvalues', 'PS_MEMORY_RESERVE',
#     'PS_MITIGATION_OPTION',
#     'PS_MITIGATION_OPTION_BLOCK_NON_MICROSOFT_BINARIES',
#     'PS_MITIGATION_OPTION_BOTTOM_UP_ASLR',
#     'PS_MITIGATION_OPTION_CONTROL_FLOW_GUARD',
#     'PS_MITIGATION_OPTION_EXTENSION_POINT_DISABLE',
#     'PS_MITIGATION_OPTION_FONT_DISABLE',
#     'PS_MITIGATION_OPTION_FORCE_RELOCATE_IMAGES',
#     'PS_MITIGATION_OPTION_HEAP_TERMINATE',
#     'PS_MITIGATION_OPTION_HIGH_ENTROPY_ASLR',
#     'PS_MITIGATION_OPTION_IMAGE_LOAD_NO_LOW_LABEL',
#     'PS_MITIGATION_OPTION_IMAGE_LOAD_NO_REMOTE',
#     'PS_MITIGATION_OPTION_IMAGE_LOAD_PREFER_SYSTEM32',
#     'PS_MITIGATION_OPTION_LOADER_INTEGRITY_CONTINUITY',
#     'PS_MITIGATION_OPTION_NX',
#     'PS_MITIGATION_OPTION_PROHIBIT_DYNAMIC_CODE',
#     'PS_MITIGATION_OPTION_RESTRICT_SET_THREAD_CONTEXT',
#     'PS_MITIGATION_OPTION_RETURN_FLOW_GUARD',
#     'PS_MITIGATION_OPTION_SEHOP',
#     'PS_MITIGATION_OPTION_STRICT_CONTROL_FLOW_GUARD',
#     'PS_MITIGATION_OPTION_STRICT_HANDLE_CHECKS',
#     'PS_MITIGATION_OPTION_WIN32K_SYSTEM_CALL_DISABLE',
#     'PS_MITIGATION_OPTION__enumvalues', 'PS_PROTECTED_SIGNER',
#     'PS_PROTECTED_TYPE', 'PS_PROTECTION', 'PS_STD_HANDLE_INFO',
#     'PS_STD_HANDLE_STATE', 'PS_STD_HANDLE_STATE__enumvalues', 'PTEB',
#     'PTEB_ACTIVE_FRAME', 'PTEB_ACTIVE_FRAME_CONTEXT',
#     'PTHREAD_BASIC_INFORMATION', 'PTIMER_APC_ROUTINE',
#     'PTIMER_BASIC_INFORMATION', 'PTIMER_SET_COALESCABLE_TIMER_INFO',
#     'PTOKEN_DEFAULT_DACL', 'PTOKEN_GROUPS', 'PTOKEN_OWNER',
#     'PTOKEN_PRIMARY_GROUP', 'PTOKEN_PRIVILEGES',
#     'PTOKEN_SECURITY_ATTRIBUTES_INFORMATION',
#     'PTOKEN_SECURITY_ATTRIBUTE_FQBN_VALUE',
#     'PTOKEN_SECURITY_ATTRIBUTE_OCTET_STRING_VALUE',
#     'PTOKEN_SECURITY_ATTRIBUTE_V1', 'PTOKEN_SOURCE', 'PTOKEN_USER',
#     'PTP_ALPC', 'PTP_ALPC_CALLBACK', 'PTP_ALPC_CALLBACK_EX',
#     'PTP_CALLBACK_ENVIRON', 'PTP_CLEANUP_GROUP', 'PTP_IO',
#     'PTP_IO_CALLBACK', 'PTP_POOL', 'PTP_POOL_STACK_INFORMATION',
#     'PTP_SIMPLE_CALLBACK', 'PTP_TIMER', 'PTP_TIMER_CALLBACK',
#     'PTP_WAIT', 'PTP_WAIT_CALLBACK', 'PTP_WORK', 'PTP_WORK_CALLBACK',
#     'PTRANSACTION_NOTIFICATION', 'PUCHAR', 'PULARGE_INTEGER',
#     'PULONG', 'PULONG_PTR', 'PUNICODE_STRING',
#     'PUSER_THREAD_START_ROUTINE', 'PUSHORT', 'PVOID', 'PWCH',
#     'PWCHAR', 'PWORKERFACTORYINFOCLASS',
#     'PWORKER_FACTORY_BASIC_INFORMATION', 'PWSTR', 'PageIn',
#     'PfxFindPrefix', 'PfxInitialize', 'PfxInsertPrefix',
#     'PfxRemovePrefix', 'PoolAllocation', 'PopEntryList',
#     'ProcessAccessToken', 'ProcessActivityThrottlePolicy',
#     'ProcessActivityThrottleState', 'ProcessAffinityMask',
#     'ProcessAffinityUpdateMode', 'ProcessAllowedCpuSetsInformation',
#     'ProcessBasePriority', 'ProcessBasicInformation',
#     'ProcessBreakOnTermination', 'ProcessCheckStackExtentsMode',
#     'ProcessChildProcessInformation', 'ProcessCommandLineInformation',
#     'ProcessCommitReleaseInformation', 'ProcessConsoleHostProcess',
#     'ProcessCookie', 'ProcessCycleTime', 'ProcessDebugFlags',
#     'ProcessDebugObjectHandle', 'ProcessDebugPort',
#     'ProcessDefaultCpuSetsInformation', 'ProcessDefaultHardErrorMode',
#     'ProcessDeviceMap', 'ProcessDisableSystemAllowedCpuSets',
#     'ProcessDynamicFunctionTableInformation',
#     'ProcessEnableAlignmentFaultFixup', 'ProcessEnergyTrackingState',
#     'ProcessEnergyValues', 'ProcessExceptionPort',
#     'ProcessExecuteFlags', 'ProcessFaultInformation',
#     'ProcessForegroundInformation', 'ProcessGroupInformation',
#     'ProcessHandleCheckingMode', 'ProcessHandleCount',
#     'ProcessHandleInformation', 'ProcessHandleTable',
#     'ProcessHandleTracing', 'ProcessHighGraphicsPriorityInformation',
#     'ProcessImageFileMapping', 'ProcessImageFileName',
#     'ProcessImageFileNameWin32', 'ProcessImageInformation',
#     'ProcessInPrivate', 'ProcessInstrumentationCallback',
#     'ProcessIoCounters', 'ProcessIoPortHandlers', 'ProcessIoPriority',
#     'ProcessIumChallengeResponse', 'ProcessJobMemoryInformation',
#     'ProcessKeepAliveCount', 'ProcessLUIDDeviceMapsEnabled',
#     'ProcessLdtInformation', 'ProcessLdtSize',
#     'ProcessMemoryAllocationMode', 'ProcessMemoryExhaustion',
#     'ProcessMitigationPolicy', 'ProcessPagePriority',
#     'ProcessPooledUsageAndLimits', 'ProcessPriorityBoost',
#     'ProcessPriorityClass', 'ProcessProtectionInformation',
#     'ProcessQuotaLimits', 'ProcessRaisePriority',
#     'ProcessRaiseUMExceptionOnInvalidHandleClose',
#     'ProcessResourceManagement', 'ProcessRevokeFileHandles',
#     'ProcessSessionInformation', 'ProcessSubsystemInformation',
#     'ProcessSubsystemProcess', 'ProcessTelemetryIdInformation',
#     'ProcessThreadStackAllocation', 'ProcessTimes',
#     'ProcessTokenVirtualizationEnabled', 'ProcessUserModeIOPL',
#     'ProcessVmCounters', 'ProcessWakeInformation',
#     'ProcessWin32kSyscallFilterInformation',
#     'ProcessWindowInformation', 'ProcessWorkingSetControl',
#     'ProcessWorkingSetWatch', 'ProcessWorkingSetWatchEx',
#     'ProcessWow64Information', 'ProcessWx86Information',
#     'PsAlwaysDuplicate', 'PsAttributeAllApplicationPackagesPolicy',
#     'PsAttributeBnoIsolation', 'PsAttributeChildProcessPolicy',
#     'PsAttributeClientId', 'PsAttributeDebugPort',
#     'PsAttributeDesktopAppPolicy', 'PsAttributeErrorMode',
#     'PsAttributeGroupAffinity', 'PsAttributeHandleList',
#     'PsAttributeIdealProcessor', 'PsAttributeImageInfo',
#     'PsAttributeImageName', 'PsAttributeJobList', 'PsAttributeMax',
#     'PsAttributeMemoryReserve', 'PsAttributeMitigationOptions',
#     'PsAttributeParentProcess', 'PsAttributePreferredNode',
#     'PsAttributePriorityClass', 'PsAttributeProtectionLevel',
#     'PsAttributeSafeOpenPromptOriginClaim',
#     'PsAttributeSecureProcess', 'PsAttributeStdHandleInfo',
#     'PsAttributeTebAddress', 'PsAttributeToken',
#     'PsAttributeUmsThread', 'PsAttributeWin32kFilter',
#     'PsCreateFailExeFormat', 'PsCreateFailExeName',
#     'PsCreateFailMachineMismatch', 'PsCreateFailOnFileOpen',
#     'PsCreateFailOnSectionCreate', 'PsCreateInitialState',
#     'PsCreateMaximumStates', 'PsCreateSuccess',
#     'PsMaxStdHandleStates', 'PsNeverDuplicate', 'PsRequestDuplicate',
#     'PushEntryList', 'REG_ACTION', 'REG_ACTION__enumvalues',
#     'REG_NOTIFY_INFORMATION', 'RESOURCEMANAGER_INFORMATION_CLASS',
#     'RESOURCEMANAGER_INFORMATION_CLASS__enumvalues', 'RTL_ATOM',
#     'RTL_BALANCED_NODE', 'RTL_BITMAP', 'RTL_BITMAP_RUN',
#     'RTL_BSD_ITEM_TYPE', 'RTL_BUFFER', 'RTL_DEBUG_INFORMATION',
#     'RTL_DRIVE_LETTER_CURDIR', 'RTL_HEAP_ENTRY',
#     'RTL_HEAP_INFORMATION', 'RTL_HEAP_PARAMETERS', 'RTL_HEAP_TAG',
#     'RTL_HEAP_TAG_INFO', 'RTL_HEAP_WALK_ENTRY',
#     'RTL_OSVERSIONINFOEXW', 'RTL_PATH_TYPE',
#     'RTL_PATH_TYPE__enumvalues', 'RTL_PROCESS_HEAPS',
#     'RTL_PROCESS_MODULES', 'RTL_PROCESS_MODULE_INFORMATION',
#     'RTL_PROCESS_MODULE_INFORMATION_EX',
#     'RTL_PROCESS_VERIFIER_OPTIONS', 'RTL_RELATIVE_NAME_U',
#     'RTL_SPLAY_LINKS', 'RTL_UNICODE_STRING_BUFFER',
#     'RTL_USER_PROCESS_INFORMATION', 'RTL_USER_PROCESS_PARAMETERS',
#     'Ready', 'RemoveEntryList', 'RemoveHeadList', 'RemoveTailList',
#     'ResourceManagerBasicInformation',
#     'ResourceManagerCompletionInformation', 'ResponseAbort',
#     'ResponseCancel', 'ResponseContinue', 'ResponseIgnore',
#     'ResponseNo', 'ResponseNotHandled', 'ResponseOk', 'ResponseRetry',
#     'ResponseReturnToCaller', 'ResponseTryAgain', 'ResponseYes',
#     'RtlAbsoluteToSelfRelativeSD', 'RtlAcquirePrivilege',
#     'RtlAcquireReleaseSRWLockExclusive', 'RtlAcquireSRWLockExclusive',
#     'RtlAcquireSRWLockShared', 'RtlAddAccessAllowedAce',
#     'RtlAddAccessAllowedAceEx', 'RtlAddAce', 'RtlAddAtomToAtomTable',
#     'RtlAddressInSectionTable', 'RtlAdjustPrivilege',
#     'RtlAllocateHeap', 'RtlAnsiStringToUnicodeString',
#     'RtlAppendUnicodeStringToString', 'RtlAppendUnicodeToString',
#     'RtlAreAllAccessesGranted', 'RtlAreAnyAccessesGranted',
#     'RtlAreBitsClear', 'RtlAreBitsSet', 'RtlAssert',
#     'RtlBsdItemAabEnabled', 'RtlBsdItemAabTimeout',
#     'RtlBsdItemBootGood', 'RtlBsdItemBootShutdown', 'RtlBsdItemMax',
#     'RtlBsdItemProductType', 'RtlBsdItemVersionNumber',
#     'RtlCaptureContext', 'RtlCaptureStackBackTrace',
#     'RtlClearAllBits', 'RtlClearBits', 'RtlCompactHeap',
#     'RtlCompareAltitudes', 'RtlCompareUnicodeString',
#     'RtlCompressBuffer', 'RtlComputeCrc32', 'RtlConnectToSm',
#     'RtlConvertSidToUnicodeString', 'RtlCopyLuid', 'RtlCopySid',
#     'RtlCopyUnicodeString', 'RtlCreateAcl', 'RtlCreateAtomTable',
#     'RtlCreateBootStatusDataFile', 'RtlCreateEnvironment',
#     'RtlCreateEnvironmentEx', 'RtlCreateHeap',
#     'RtlCreateProcessParameters', 'RtlCreateProcessParametersEx',
#     'RtlCreateQueryDebugBuffer', 'RtlCreateSecurityDescriptor',
#     'RtlCreateSystemVolumeInformationFolder', 'RtlCreateTagHeap',
#     'RtlCreateUserProcess', 'RtlCreateUserThread',
#     'RtlDeNormalizeProcessParams', 'RtlDecompressBuffer',
#     'RtlDecompressFragment', 'RtlDefaultNpAcl', 'RtlDelete',
#     'RtlDeleteAce', 'RtlDeleteAtomFromAtomTable',
#     'RtlDeleteCriticalSection', 'RtlDeleteNoSplay',
#     'RtlDestroyEnvironment', 'RtlDestroyHeap',
#     'RtlDestroyProcessParameters', 'RtlDetermineDosPathNameType_U',
#     'RtlDosApplyFileIsolationRedirection_Ustr',
#     'RtlDosPathNameToNtPathName_U',
#     'RtlDosPathNameToRelativeNtPathName_U',
#     'RtlDosPathNameToRelativeNtPathName_U_WithStatus',
#     'RtlDowncaseUnicodeString', 'RtlDuplicateUnicodeString',
#     'RtlEmptyAtomTable', 'RtlEnableEarlyCriticalSectionEventCreation',
#     'RtlEnterCriticalSection', 'RtlEnumProcessHeaps', 'RtlEqualSid',
#     'RtlEqualString', 'RtlEqualUnicodeString',
#     'RtlExpandEnvironmentStrings', 'RtlExpandEnvironmentStrings_U',
#     'RtlFindClearBits', 'RtlFindClearBitsAndSet', 'RtlFindClearRuns',
#     'RtlFindLastBackwardRunClear', 'RtlFindLeastSignificantBit',
#     'RtlFindLongestRunClear', 'RtlFindMessage',
#     'RtlFindMostSignificantBit', 'RtlFindNextForwardRunClear',
#     'RtlFindSetBits', 'RtlFindSetBitsAndClear', 'RtlFormatMessage',
#     'RtlFreeAnsiString', 'RtlFreeHeap', 'RtlGUIDFromString',
#     'RtlGetCallersAddress', 'RtlGetCompressionWorkSpaceSize',
#     'RtlGetCriticalSectionRecursionCount',
#     'RtlGetDaclSecurityDescriptor', 'RtlGetFullPathName_U',
#     'RtlGetFullPathName_UstrEx', 'RtlGetGroupSecurityDescriptor',
#     'RtlGetLastNtStatus', 'RtlGetLastWin32Error',
#     'RtlGetOwnerSecurityDescriptor', 'RtlGetProcessHeaps',
#     'RtlGetSaclSecurityDescriptor', 'RtlGetSetBootStatusData',
#     'RtlGetThreadErrorMode', 'RtlGetUserInfoHeap', 'RtlGetVersion',
#     'RtlHashUnicodeString', 'RtlImageDirectoryEntryToData',
#     'RtlImageNtHeader', 'RtlImageNtHeaderEx', 'RtlImageRvaToSection',
#     'RtlImageRvaToVa', 'RtlInitAnsiString',
#     'RtlInitEmptyUnicodeString', 'RtlInitUnicodeString',
#     'RtlInitializeCriticalSection',
#     'RtlInitializeCriticalSectionAndSpinCount',
#     'RtlInitializeSRWLock', 'RtlInitializeSid',
#     'RtlIsCriticalSectionLocked',
#     'RtlIsCriticalSectionLockedByThread', 'RtlLeaveCriticalSection',
#     'RtlLengthRequiredSid', 'RtlLengthSecurityDescriptor',
#     'RtlLengthSid', 'RtlLockBootStatusData', 'RtlLockHeap',
#     'RtlLookupAtomInAtomTable', 'RtlMapSecurityErrorToNtStatus',
#     'RtlMultiByteToUnicodeN', 'RtlMultiByteToUnicodeSize',
#     'RtlNormalizeProcessParams', 'RtlNtPathNameToDosPathName',
#     'RtlNtStatusToDosError', 'RtlNtStatusToDosErrorNoTeb',
#     'RtlNumberOfClearBits', 'RtlNumberOfSetBits',
#     'RtlPathTypeDriveAbsolute', 'RtlPathTypeDriveRelative',
#     'RtlPathTypeLocalDevice', 'RtlPathTypeRelative',
#     'RtlPathTypeRootLocalDevice', 'RtlPathTypeRooted',
#     'RtlPathTypeUncAbsolute', 'RtlPathTypeUnknown',
#     'RtlPcToFileHeader', 'RtlProtectHeap', 'RtlQueryAtomInAtomTable',
#     'RtlQueryEnvironmentVariable', 'RtlQueryEnvironmentVariable_U',
#     'RtlQueryHeapInformation', 'RtlQueryPerformanceCounter',
#     'RtlQueryPerformanceFrequency', 'RtlQueryProcessDebugInformation',
#     'RtlQueryProcessHeapInformation', 'RtlQueryTagHeap',
#     'RtlRaiseException', 'RtlRaiseStatus', 'RtlRandom', 'RtlRandomEx',
#     'RtlReAllocateHeap', 'RtlRealPredecessor', 'RtlRealSuccessor',
#     'RtlRegisterThreadWithCsrss', 'RtlReleasePrivilege',
#     'RtlReleaseRelativeName', 'RtlReleaseSRWLockExclusive',
#     'RtlReleaseSRWLockShared', 'RtlRestoreContext',
#     'RtlRestoreLastWin32Error', 'RtlRunDecodeUnicodeString',
#     'RtlRunEncodeUnicodeString', 'RtlSelfRelativeToAbsoluteSD',
#     'RtlSelfRelativeToAbsoluteSD2', 'RtlSendMsgToSm', 'RtlSetAllBits',
#     'RtlSetBits', 'RtlSetCriticalSectionSpinCount',
#     'RtlSetCurrentDirectory_U', 'RtlSetCurrentEnvironment',
#     'RtlSetDaclSecurityDescriptor', 'RtlSetEnvironmentStrings',
#     'RtlSetEnvironmentVar', 'RtlSetEnvironmentVariable',
#     'RtlSetGroupSecurityDescriptor', 'RtlSetHeapInformation',
#     'RtlSetLastWin32Error',
#     'RtlSetLastWin32ErrorAndNtStatusFromNtStatus',
#     'RtlSetOwnerSecurityDescriptor', 'RtlSetSaclSecurityDescriptor',
#     'RtlSetThreadErrorMode', 'RtlSetUserFlagsHeap',
#     'RtlSetUserValueHeap', 'RtlSizeHeap', 'RtlSplay',
#     'RtlStringFromGUID', 'RtlSubAuthorityCountSid',
#     'RtlSubAuthoritySid', 'RtlSubtreePredecessor',
#     'RtlSubtreeSuccessor', 'RtlTestBit',
#     'RtlTryAcquireSRWLockExclusive', 'RtlTryAcquireSRWLockShared',
#     'RtlTryEnterCriticalSection', 'RtlUnicodeStringToAnsiString',
#     'RtlUniform', 'RtlUnlockBootStatusData', 'RtlUnlockHeap',
#     'RtlUpcaseUnicodeString', 'RtlValidRelativeSecurityDescriptor',
#     'RtlValidSecurityDescriptor', 'RtlValidSid', 'RtlValidateHeap',
#     'RtlValidateProcessHeaps', 'RtlVerifyVersionInfo',
#     'RtlWalkFrameChain', 'RtlWalkHeap', 'RtlZeroHeap', 'Running',
#     'SECTION_BASIC_INFORMATION', 'SECTION_IMAGE_INFORMATION',
#     'SECTION_INFORMATION_CLASS',
#     'SECTION_INFORMATION_CLASS__enumvalues', 'SECTION_INHERIT',
#     'SECTION_INHERIT__enumvalues',
#     'SECTION_INTERNAL_IMAGE_INFORMATION', 'SECURITY_INFORMATION',
#     'SECURITY_STATUS', 'SEMAPHORE_BASIC_INFORMATION',
#     'SEMAPHORE_INFORMATION_CLASS',
#     'SEMAPHORE_INFORMATION_CLASS__enumvalues', 'SIZE_T',
#     'SYSDBG_COMMAND', 'SYSDBG_COMMAND__enumvalues',
#     'SYSTEM_BASIC_INFORMATION', 'SYSTEM_CONSOLE_INFORMATION',
#     'SYSTEM_EXTENDED_THREAD_INFORMATION', 'SYSTEM_HANDLE_INFORMATION',
#     'SYSTEM_HANDLE_INFORMATION_EX', 'SYSTEM_HANDLE_TABLE_ENTRY_INFO',
#     'SYSTEM_HANDLE_TABLE_ENTRY_INFO_EX', 'SYSTEM_INFORMATION_CLASS',
#     'SYSTEM_INFORMATION_CLASS__enumvalues',
#     'SYSTEM_KERNEL_DEBUGGER_INFORMATION',
#     'SYSTEM_KERNEL_DEBUGGER_INFORMATION_EX',
#     'SYSTEM_PROCESS_INFORMATION',
#     'SYSTEM_SESSION_PROCESS_INFORMATION', 'SYSTEM_THREAD_INFORMATION',
#     'SYSTEM_TIMEOFDAY_INFORMATION', 'SectionBasicInformation',
#     'SectionImageInformation', 'SectionInternalImageInformation',
#     'SectionOriginalBaseInformation', 'SectionRelocationInformation',
#     'SecurityAnonymous', 'SecurityDelegation',
#     'SecurityIdentification', 'SecurityImpersonation',
#     'SemaphoreBasicInformation', 'StandardDesign', 'Standby',
#     'Suspended', 'SynchronizationEvent', 'SynchronizationTimer',
#     'SysDbgBreakPoint', 'SysDbgCheckLowMemory',
#     'SysDbgClearSpecialCalls', 'SysDbgClearUmAttachPid',
#     'SysDbgClearUmBreakPid', 'SysDbgDisableKernelDebugger',
#     'SysDbgEnableKernelDebugger', 'SysDbgGetAutoKdEnable',
#     'SysDbgGetKdBlockEnable', 'SysDbgGetKdUmExceptionEnable',
#     'SysDbgGetLiveKernelDump', 'SysDbgGetPrintBufferSize',
#     'SysDbgGetTriageDump', 'SysDbgGetUmAttachPid',
#     'SysDbgGetUmBreakPid', 'SysDbgQueryModuleInformation',
#     'SysDbgQuerySpecialCalls', 'SysDbgQueryTraceInformation',
#     'SysDbgQueryVersion', 'SysDbgReadBusData',
#     'SysDbgReadControlSpace', 'SysDbgReadIoSpace', 'SysDbgReadMsr',
#     'SysDbgReadPhysical', 'SysDbgReadVirtual',
#     'SysDbgRegisterForUmBreakInfo', 'SysDbgSetAutoKdEnable',
#     'SysDbgSetKdBlockEnable', 'SysDbgSetKdUmExceptionEnable',
#     'SysDbgSetPrintBufferSize', 'SysDbgSetSpecialCall',
#     'SysDbgSetTracepoint', 'SysDbgWriteBusData',
#     'SysDbgWriteControlSpace', 'SysDbgWriteIoSpace', 'SysDbgWriteMsr',
#     'SysDbgWritePhysical', 'SysDbgWriteVirtual',
#     'SystemAcpiAuditInformation', 'SystemActivityModerationExeState',
#     'SystemActivityModerationUserSettings',
#     'SystemAffinitizedInterruptProcessorInformation',
#     'SystemAitSamplingValue', 'SystemAllowedCpuSetsInformation',
#     'SystemBadPageInformation', 'SystemBasicInformation',
#     'SystemBasicPerformanceInformation', 'SystemBigPoolInformation',
#     'SystemBootEnvironmentInformation',
#     'SystemBootGraphicsInformation', 'SystemBootLogoInformation',
#     'SystemBootMetadataInformation', 'SystemCallCountInformation',
#     'SystemCallTimeInformation',
#     'SystemCodeIntegrityCertificateInformation',
#     'SystemCodeIntegrityInformation',
#     'SystemCodeIntegrityPlatformManifestInformation',
#     'SystemCodeIntegrityPoliciesFullInformation',
#     'SystemCodeIntegrityPolicyFullInformation',
#     'SystemCodeIntegrityPolicyInformation',
#     'SystemCodeIntegrityUnlockInformation', 'SystemComPlusPackage',
#     'SystemCombinePhysicalMemoryInformation',
#     'SystemConsoleInformation', 'SystemContextSwitchInformation',
#     'SystemControlFlowTransition', 'SystemCoverageInformation',
#     'SystemCpuQuotaInformation', 'SystemCpuSetInformation',
#     'SystemCpuSetTagInformation', 'SystemCrashDumpStateInformation',
#     'SystemCurrentTimeZoneInformation',
#     'SystemDeviceDataEnumerationInformation',
#     'SystemDeviceDataInformation', 'SystemDeviceInformation',
#     'SystemDmaProtectionInformation', 'SystemDpcBehaviorInformation',
#     'SystemDynamicTimeZoneInformation', 'SystemEdidInformation',
#     'SystemElamCertificateInformation',
#     'SystemEmulationBasicInformation',
#     'SystemEmulationProcessorInformation',
#     'SystemEnergyEstimationConfigInformation',
#     'SystemEntropyInterruptTimingCallback',
#     'SystemEntropyInterruptTimingRawInformation',
#     'SystemErrorPortInformation', 'SystemExceptionInformation',
#     'SystemExtendServiceTableInformation',
#     'SystemExtendedHandleInformation',
#     'SystemExtendedProcessInformation', 'SystemFileCacheInformation',
#     'SystemFileCacheInformationEx', 'SystemFirmwareTableInformation',
#     'SystemFlagsInformation', 'SystemFlushInformation',
#     'SystemFullMemoryInformation', 'SystemFullProcessInformation',
#     'SystemHandleInformation',
#     'SystemHardwareSecurityTestInterfaceResultsInformation',
#     'SystemHotpatchInformation', 'SystemHypervisorDetailInformation',
#     'SystemHypervisorInformation',
#     'SystemHypervisorProcessorCountInformation',
#     'SystemImageFileExecutionOptionsInformation',
#     'SystemIntegrityQuotaInformation',
#     'SystemInterruptCpuSetsInformation', 'SystemInterruptInformation',
#     'SystemInterruptSteeringInformation',
#     'SystemIsolatedUserModeInformation', 'SystemKernelDebuggerFlags',
#     'SystemKernelDebuggerInformation',
#     'SystemKernelDebuggerInformationEx',
#     'SystemKernelDebuggingAllowed', 'SystemLegacyDriverInformation',
#     'SystemLoadGdiDriverInSystemSpace',
#     'SystemLoadGdiDriverInformation', 'SystemLocksInformation',
#     'SystemLogicalProcessorAndGroupInformation',
#     'SystemLogicalProcessorInformation', 'SystemLookasideInformation',
#     'SystemLostDelayedWriteInformation',
#     'SystemLowPriorityIoInformation',
#     'SystemManufacturingInformation',
#     'SystemMemoryChannelInformation', 'SystemMemoryListInformation',
#     'SystemMemoryTopologyInformation', 'SystemMemoryUsageInformation',
#     'SystemMirrorMemoryInformation', 'SystemModuleInformation',
#     'SystemModuleInformationEx', 'SystemNativeBasicInformation',
#     'SystemNodeDistanceInformation', 'SystemNonPagedPoolInformation',
#     'SystemNumaAvailableMemory', 'SystemNumaProcessorMap',
#     'SystemNumaProximityNodeInformation', 'SystemObjectInformation',
#     'SystemObjectSecurityMode', 'SystemObsolete0',
#     'SystemOfflineDumpConfigInformation', 'SystemPageFileInformation',
#     'SystemPageFileInformationEx', 'SystemPagedPoolInformation',
#     'SystemPagedPoolInformationEx', 'SystemPathInformation',
#     'SystemPerformanceInformation',
#     'SystemPerformanceTraceInformation',
#     'SystemPhysicalMemoryInformation',
#     'SystemPlatformBinaryInformation', 'SystemPoolTagInformation',
#     'SystemPortableWorkspaceEfiLauncherInformation',
#     'SystemPrefetchPatchInformation', 'SystemPrefetcherInformation',
#     'SystemPrioritySeperation', 'SystemProcessIdInformation',
#     'SystemProcessInformation', 'SystemProcessorBrandString',
#     'SystemProcessorCycleStatsInformation',
#     'SystemProcessorCycleTimeInformation',
#     'SystemProcessorFeaturesInformation',
#     'SystemProcessorIdleCycleTimeInformation',
#     'SystemProcessorIdleInformation', 'SystemProcessorInformation',
#     'SystemProcessorMicrocodeUpdateInformation',
#     'SystemProcessorPerformanceDistribution',
#     'SystemProcessorPerformanceInformation',
#     'SystemProcessorPerformanceInformationEx',
#     'SystemProcessorPowerInformation',
#     'SystemProcessorPowerInformationEx',
#     'SystemProcessorProfileControlArea',
#     'SystemQueryPerformanceCounterInformation',
#     'SystemRangeStartInformation',
#     'SystemRecommendedSharedDataAlignment',
#     'SystemRefTraceInformation',
#     'SystemRegisterFirmwareTableInformationHandler',
#     'SystemRegistryAppendString', 'SystemRegistryQuotaInformation',
#     'SystemRegistryReconciliationInformation',
#     'SystemRootSiloInformation',
#     'SystemScrubPhysicalMemoryInformation',
#     'SystemSecureBootInformation',
#     'SystemSecureBootPolicyFullInformation',
#     'SystemSecureBootPolicyInformation',
#     'SystemSecureKernelProfileInformation',
#     'SystemSessionBigPoolInformation', 'SystemSessionCreate',
#     'SystemSessionDetach', 'SystemSessionInformation',
#     'SystemSessionMappedViewInformation',
#     'SystemSessionPoolTagInformation',
#     'SystemSessionProcessInformation',
#     'SystemSingleModuleInformation', 'SystemSoftRebootInformation',
#     'SystemSpare0', 'SystemSpare1', 'SystemSpecialPoolInformation',
#     'SystemStackTraceInformation', 'SystemStoreInformation',
#     'SystemSummaryMemoryInformation', 'SystemSuperfetchInformation',
#     'SystemSupportedProcessorArchitectures',
#     'SystemSystemDiskInformation', 'SystemSystemPartitionInformation',
#     'SystemSystemPtesInformationEx',
#     'SystemThreadPriorityClientIdInformation',
#     'SystemThrottleNotificationInformation',
#     'SystemTimeAdjustmentInformation', 'SystemTimeOfDayInformation',
#     'SystemTimeSlipNotification', 'SystemTimeZoneInformation',
#     'SystemTpmBootEntropyInformation',
#     'SystemTrustedPlatformModuleInformation',
#     'SystemUnloadGdiDriverInformation', 'SystemVdmBopInformation',
#     'SystemVdmInstemulInformation',
#     'SystemVerifierAddDriverInformation',
#     'SystemVerifierCancellationInformation',
#     'SystemVerifierCountersInformation',
#     'SystemVerifierFaultsInformation', 'SystemVerifierInformation',
#     'SystemVerifierInformationEx',
#     'SystemVerifierRemoveDriverInformation',
#     'SystemVerifierThunkExtend', 'SystemVerifierTriageInformation',
#     'SystemVhdBootInformation', 'SystemVirtualAddressInformation',
#     'SystemVmGenerationCountInformation',
#     'SystemWatchdogTimerHandler', 'SystemWatchdogTimerInformation',
#     'SystemWin32WerStartCallout',
#     'SystemWow64SharedInformationObsolete', 'TEB', 'TEB_ACTIVE_FRAME',
#     'TEB_ACTIVE_FRAME_CONTEXT', 'THREADINFOCLASS',
#     'THREADINFOCLASS__enumvalues', 'THREAD_BASIC_INFORMATION',
#     'TIMER_BASIC_INFORMATION', 'TIMER_INFORMATION_CLASS',
#     'TIMER_INFORMATION_CLASS__enumvalues',
#     'TIMER_SET_COALESCABLE_TIMER_INFO', 'TIMER_SET_INFORMATION_CLASS',
#     'TIMER_SET_INFORMATION_CLASS__enumvalues', 'TIMER_TYPE',
#     'TIMER_TYPE__enumvalues', 'TOKEN_INFORMATION_CLASS',
#     'TOKEN_INFORMATION_CLASS__enumvalues',
#     'TOKEN_SECURITY_ATTRIBUTES_INFORMATION',
#     'TOKEN_SECURITY_ATTRIBUTE_FQBN_VALUE',
#     'TOKEN_SECURITY_ATTRIBUTE_OCTET_STRING_VALUE',
#     'TOKEN_SECURITY_ATTRIBUTE_V1', 'TOKEN_TYPE',
#     'TOKEN_TYPE__enumvalues', 'TP_ALPC', 'TP_CALLBACK_PRIORITY_COUNT',
#     'TP_CALLBACK_PRIORITY_HIGH', 'TP_CALLBACK_PRIORITY_INVALID',
#     'TP_CALLBACK_PRIORITY_LOW', 'TP_CALLBACK_PRIORITY_NORMAL',
#     'TRANSACTIONMANAGER_INFORMATION_CLASS',
#     'TRANSACTIONMANAGER_INFORMATION_CLASS__enumvalues',
#     'TRANSACTION_INFORMATION_CLASS',
#     'TRANSACTION_INFORMATION_CLASS__enumvalues', 'Terminated',
#     'ThreadActualBasePriority', 'ThreadActualGroupAffinity',
#     'ThreadAffinityMask', 'ThreadAmILastThread',
#     'ThreadAttachContainer', 'ThreadBasePriority',
#     'ThreadBasicInformation', 'ThreadBreakOnTermination',
#     'ThreadCSwitchMon', 'ThreadCSwitchPmu', 'ThreadContainerId',
#     'ThreadCounterProfiling', 'ThreadCpuAccountingInformation',
#     'ThreadCycleTime', 'ThreadDbgkWerReportActive',
#     'ThreadDescriptorTableEntry', 'ThreadDynamicCodePolicyInfo',
#     'ThreadEnableAlignmentFaultFixup', 'ThreadEventPair',
#     'ThreadExplicitCaseSensitivity', 'ThreadGroupInformation',
#     'ThreadHeterogeneousCpuPolicy', 'ThreadHideFromDebugger',
#     'ThreadIdealProcessor', 'ThreadIdealProcessorEx',
#     'ThreadImpersonationToken', 'ThreadIoPriority',
#     'ThreadIsIoPending', 'ThreadIsTerminated', 'ThreadLastSystemCall',
#     'ThreadNameInformation', 'ThreadPagePriority',
#     'ThreadPerformanceCount', 'ThreadPriority', 'ThreadPriorityBoost',
#     'ThreadQuerySetWin32StartAddress', 'ThreadSelectedCpuSets',
#     'ThreadSetTlsArrayAddress', 'ThreadSubsystemInformation',
#     'ThreadSuspendCount', 'ThreadSwitchLegacyState',
#     'ThreadSystemThreadInformation', 'ThreadTebInformation',
#     'ThreadTimes', 'ThreadUmsInformation', 'ThreadWorkOnBehalfTicket',
#     'ThreadWow64Context', 'ThreadZeroTlsCell',
#     'TimerBasicInformation', 'TimerSetCoalescableTimer',
#     'TokenAccessInformation', 'TokenAppContainerNumber',
#     'TokenAppContainerSid', 'TokenAuditPolicy', 'TokenBnoIsolation',
#     'TokenCapabilities', 'TokenChildProcessFlags', 'TokenDefaultDacl',
#     'TokenDeviceClaimAttributes', 'TokenDeviceGroups',
#     'TokenElevation', 'TokenElevationType', 'TokenGroups',
#     'TokenGroupsAndPrivileges', 'TokenHasRestrictions',
#     'TokenImpersonation', 'TokenImpersonationLevel',
#     'TokenIntegrityLevel', 'TokenIsAppContainer',
#     'TokenIsLessPrivilegedAppContainer', 'TokenIsRestricted',
#     'TokenIsSandboxed', 'TokenLinkedToken', 'TokenLogonSid',
#     'TokenMandatoryPolicy', 'TokenOrigin',
#     'TokenOriginatingProcessTrustLevel', 'TokenOwner', 'TokenPrimary',
#     'TokenPrimaryGroup', 'TokenPrivateNameSpace', 'TokenPrivileges',
#     'TokenProcessTrustLevel', 'TokenRestrictedDeviceClaimAttributes',
#     'TokenRestrictedDeviceGroups', 'TokenRestrictedSids',
#     'TokenRestrictedUserClaimAttributes', 'TokenSandBoxInert',
#     'TokenSecurityAttributes', 'TokenSessionId',
#     'TokenSessionReference', 'TokenSingletonAttributes',
#     'TokenSource', 'TokenStatistics', 'TokenType', 'TokenUIAccess',
#     'TokenUser', 'TokenUserClaimAttributes',
#     'TokenVirtualizationAllowed', 'TokenVirtualizationEnabled',
#     'TpAllocAlpcCompletion', 'TpAllocAlpcCompletionEx',
#     'TpAllocCleanupGroup', 'TpAllocIoCompletion', 'TpAllocPool',
#     'TpAllocTimer', 'TpAllocWait', 'TpAllocWork',
#     'TpAlpcRegisterCompletionList', 'TpAlpcUnregisterCompletionList',
#     'TpDisablePoolCallbackChecks', 'TpIsTimerSet', 'TpPostWork',
#     'TpQueryPoolStackInformation', 'TpReleaseAlpcCompletion',
#     'TpReleaseCleanupGroup', 'TpReleaseCleanupGroupMembers',
#     'TpReleasePool', 'TpReleaseTimer', 'TpReleaseWait',
#     'TpReleaseWork', 'TpSetPoolMaxThreads', 'TpSetPoolMinThreads',
#     'TpSetPoolStackInformation', 'TpSetTimer', 'TpSetWait',
#     'TpSimpleTryPost', 'TpWaitForAlpcCompletion',
#     'TpWaitForIoCompletion', 'TpWaitForTimer', 'TpWaitForWork',
#     'TransactionBasicInformation', 'TransactionBindInformation',
#     'TransactionDTCPrivateInformation',
#     'TransactionEnlistmentInformation',
#     'TransactionManagerBasicInformation',
#     'TransactionManagerLogInformation',
#     'TransactionManagerLogPathInformation',
#     'TransactionManagerOldestTransactionInformation',
#     'TransactionManagerOnlineProbeInformation',
#     'TransactionManagerRecoveryInformation',
#     'TransactionPropertiesInformation',
#     'TransactionSuperiorEnlistmentInformation', 'Transition', 'UCHAR',
#     'ULONG', 'ULONG32', 'ULONG64', 'ULONGLONG', 'ULONG_PTR',
#     'UNICODE_STRING', 'USHORT', 'UserMode', 'UserRequest',
#     'VerSetConditionMask', 'ViewShare', 'ViewUnmap', 'WAIT_TYPE',
#     'WAIT_TYPE__enumvalues', 'WORD', 'WORKERFACTORYINFOCLASS',
#     'WORKERFACTORYINFOCLASS__enumvalues',
#     'WORKER_FACTORY_BASIC_INFORMATION', 'WaitAll', 'WaitAny',
#     'WaitDequeue', 'WaitNotification', 'Waiting',
#     'WaitingForProcessInSwap', 'WorkerFactoryAdjustThreadGoal',
#     'WorkerFactoryBasicInformation', 'WorkerFactoryBindingCount',
#     'WorkerFactoryCallbackType', 'WorkerFactoryFlags',
#     'WorkerFactoryIdleTimeout', 'WorkerFactoryPaused',
#     'WorkerFactoryRetryTimeout', 'WorkerFactoryStackInformation',
#     'WorkerFactoryThreadBasePriority', 'WorkerFactoryThreadMaximum',
#     'WorkerFactoryThreadMinimum', 'WorkerFactoryThreadSoftMaximum',
#     'WorkerFactoryTimeout', 'WorkerFactoryTimeoutWaiters',
#     'WrAlertByThreadId', 'WrCalloutStack', 'WrCpuRateControl',
#     'WrDeferredPreempt', 'WrDelayExecution', 'WrDispatchInt',
#     'WrEventPair', 'WrExecutive', 'WrFastMutex', 'WrFreePage',
#     'WrGuardedMutex', 'WrKernel', 'WrKeyedEvent', 'WrLpcReceive',
#     'WrLpcReply', 'WrMutex', 'WrPageIn', 'WrPageOut',
#     'WrPoolAllocation', 'WrPreempted', 'WrProcessInSwap',
#     'WrPushLock', 'WrQuantumEnd', 'WrQueue', 'WrRendezvous',
#     'WrResource', 'WrRundown', 'WrSuspended', 'WrTerminated',
#     'WrUserRequest', 'WrVirtualMemory', 'WrYieldExecution',
#     '_ALTERNATIVE_ARCHITECTURE_TYPE', '_DBG_STATE',
#     '_DEBUGOBJECTINFOCLASS', '_ENLISTMENT_INFORMATION_CLASS',
#     '_EVENT_TYPE', '_EXCEPTION_DISPOSITION',
#     '_FILE_INFORMATION_CLASS', '_FILTER_BOOT_OPTION_OPERATION',
#     '_FSINFOCLASS', '_HARDERROR_RESPONSE',
#     '_HARDERROR_RESPONSE_OPTION', '_HEAP_INFORMATION_CLASS',
#     '_IO_COMPLETION_INFORMATION_CLASS', '_IO_SESSION_EVENT',
#     '_IO_SESSION_STATE', '_KEY_INFORMATION_CLASS',
#     '_KEY_SET_INFORMATION_CLASS', '_KEY_VALUE_INFORMATION_CLASS',
#     '_KTHREAD_STATE', '_KTMOBJECT_TYPE', '_KWAIT_REASON',
#     '_LDR_DDAG_STATE', '_LDR_DLL_LOAD_REASON',
#     '_MEMORY_INFORMATION_CLASS', '_MEMORY_RESERVE_TYPE',
#     '_OBJECT_INFORMATION_CLASS', '_PROCESSINFOCLASS',
#     '_PS_ATTRIBUTE_NUM', '_PS_CREATE_STATE', '_PS_MITIGATION_OPTION',
#     '_PS_STD_HANDLE_STATE', '_REG_ACTION',
#     '_RESOURCEMANAGER_INFORMATION_CLASS', '_RTL_PATH_TYPE',
#     '_SECTION_INFORMATION_CLASS', '_SECTION_INHERIT',
#     '_SECURITY_IMPERSONATION_LEVEL', '_SEMAPHORE_INFORMATION_CLASS',
#     '_SYSDBG_COMMAND', '_SYSTEM_INFORMATION_CLASS',
#     '_THREADINFOCLASS', '_TIMER_INFORMATION_CLASS',
#     '_TIMER_SET_INFORMATION_CLASS', '_TIMER_TYPE',
#     '_TOKEN_INFORMATION_CLASS', '_TOKEN_TYPE',
#     '_TP_CALLBACK_PRIORITY', '_TRANSACTIONMANAGER_INFORMATION_CLASS',
#     '_TRANSACTION_INFORMATION_CLASS', '_WAIT_TYPE',
#     '_WORKERFACTORYINFOCLASS', 'struct__ACL',
#     'struct__ACTIVATION_CONTEXT', 'struct__ACTIVATION_CONTEXT_STACK',
#     'struct__BOOT_ENTRY', 'struct__BOOT_ENTRY_LIST',
#     'struct__BOOT_OPTIONS', 'struct__CLIENT_ID', 'struct__CONTEXT',
#     'struct__COUNTED_REASON_CONTEXT',
#     'struct__CREATE_PROCESS_DEBUG_INFO',
#     'struct__CREATE_THREAD_DEBUG_INFO', 'struct__CURDIR',
#     'struct__DBGKM_CREATE_PROCESS', 'struct__DBGKM_CREATE_THREAD',
#     'struct__DBGKM_EXCEPTION', 'struct__DBGKM_EXIT_PROCESS',
#     'struct__DBGKM_EXIT_THREAD', 'struct__DBGKM_LOAD_DLL',
#     'struct__DBGKM_UNLOAD_DLL', 'struct__DBGSS_THREAD_DATA',
#     'struct__DBGUI_CREATE_PROCESS', 'struct__DBGUI_CREATE_THREAD',
#     'struct__DBGUI_WAIT_STATE_CHANGE', 'struct__DEBUG_EVENT',
#     'struct__EFI_DRIVER_ENTRY', 'struct__EFI_DRIVER_ENTRY_LIST',
#     'struct__EXCEPTION_DEBUG_INFO', 'struct__EXCEPTION_RECORD',
#     'struct__EXCEPTION_REGISTRATION_RECORD',
#     'struct__EXIT_PROCESS_DEBUG_INFO',
#     'struct__EXIT_THREAD_DEBUG_INFO',
#     'struct__FILE_BASIC_INFORMATION',
#     'struct__FILE_COMPLETION_INFORMATION',
#     'struct__FILE_IO_COMPLETION_INFORMATION',
#     'struct__FILE_NETWORK_OPEN_INFORMATION',
#     'struct__FILE_NOTIFY_INFORMATION', 'struct__FILE_PATH',
#     'struct__FILE_PIPE_PEEK_BUFFER',
#     'struct__FILE_POSITION_INFORMATION',
#     'struct__FILE_STANDARD_INFORMATION', 'struct__GDI_TEB_BATCH',
#     'struct__GENERIC_MAPPING', 'struct__GUID',
#     'struct__HEAP_DEBUGGING_INFORMATION',
#     'struct__HEAP_EXTENDED_INFORMATION', 'struct__HEAP_INFORMATION',
#     'struct__IMAGE_BASE_RELOCATION', 'struct__IMAGE_DATA_DIRECTORY',
#     'struct__IMAGE_FILE_HEADER', 'struct__IMAGE_NT_HEADERS64',
#     'struct__IMAGE_OPTIONAL_HEADER64',
#     'struct__IMAGE_RESOURCE_DATA_ENTRY',
#     'struct__IMAGE_RESOURCE_DIRECTORY',
#     'struct__IMAGE_SECTION_HEADER', 'struct__INITIAL_TEB',
#     'struct__IO_COMPLETION_BASIC_INFORMATION',
#     'struct__IO_STATUS_BLOCK', 'struct__KERNEL_USER_TIMES',
#     'struct__KEY_BASIC_INFORMATION', 'struct__KEY_CACHED_INFORMATION',
#     'struct__KEY_CONTROL_FLAGS_INFORMATION',
#     'struct__KEY_FLAGS_INFORMATION', 'struct__KEY_FULL_INFORMATION',
#     'struct__KEY_HANDLE_TAGS_INFORMATION',
#     'struct__KEY_LAYER_INFORMATION', 'struct__KEY_NAME_INFORMATION',
#     'struct__KEY_NODE_INFORMATION',
#     'struct__KEY_OPEN_SUBKEYS_INFORMATION', 'struct__KEY_PID_ARRAY',
#     'struct__KEY_SET_VIRTUALIZATION_INFORMATION',
#     'struct__KEY_TRUST_INFORMATION',
#     'struct__KEY_VALUE_BASIC_INFORMATION', 'struct__KEY_VALUE_ENTRY',
#     'struct__KEY_VALUE_FULL_INFORMATION',
#     'struct__KEY_VALUE_LAYER_INFORMATION',
#     'struct__KEY_VALUE_PARTIAL_INFORMATION',
#     'struct__KEY_VALUE_PARTIAL_INFORMATION_ALIGN64',
#     'struct__KEY_VIRTUALIZATION_INFORMATION',
#     'struct__KEY_WOW64_FLAGS_INFORMATION',
#     'struct__KEY_WRITE_TIME_INFORMATION', 'struct__KSYSTEM_TIME',
#     'struct__KTMOBJECT_CURSOR', 'struct__KUSER_SHARED_DATA',
#     'struct__LDRP_CSLIST', 'struct__LDRP_LOAD_CONTEXT',
#     'struct__LDR_DATA_TABLE_ENTRY', 'struct__LDR_DDAG_NODE',
#     'struct__LDR_DEPENDENCY_RECORD', 'struct__LDR_ENUM_RESOURCE_INFO',
#     'struct__LDR_IMPORT_CALLBACK_INFO', 'struct__LDR_RESOURCE_INFO',
#     'struct__LDR_SECTION_INFO', 'struct__LDR_SERVICE_TAG_RECORD',
#     'struct__LDR_VERIFY_IMAGE_INFO', 'struct__LDT_ENTRY',
#     'struct__LDT_INFORMATION', 'struct__LIST_ENTRY',
#     'struct__LOAD_DLL_DEBUG_INFO', 'struct__LUID',
#     'struct__LUID_AND_ATTRIBUTES', 'struct__M128A',
#     'struct__MEMORY_REGION_INFORMATION',
#     'struct__MESSAGE_RESOURCE_ENTRY',
#     'struct__NAMED_PIPE_CREATE_PARAMETERS', 'struct__NT_TIB',
#     'struct__OBJECT_ATTRIBUTES', 'struct__OBJECT_BASIC_INFORMATION',
#     'struct__OBJECT_HANDLE_FLAG_INFORMATION',
#     'struct__OBJECT_NAME_INFORMATION',
#     'struct__OBJECT_TYPES_INFORMATION',
#     'struct__OBJECT_TYPE_INFORMATION', 'struct__OBJECT_TYPE_LIST',
#     'struct__OSVERSIONINFOEXW', 'struct__OSVERSIONINFOW',
#     'struct__OUTPUT_DEBUG_STRING_INFO', 'struct__PEB',
#     'struct__PEB_LDR_DATA', 'struct__PORT_MESSAGE',
#     'struct__PREFIX_TABLE', 'struct__PREFIX_TABLE_ENTRY',
#     'struct__PRIVILEGE_SET', 'struct__PROCESSOR_NUMBER',
#     'struct__PROCESS_ACCESS_TOKEN',
#     'struct__PROCESS_BASIC_INFORMATION',
#     'struct__PROCESS_EXTENDED_BASIC_INFORMATION',
#     'struct__PROCESS_HANDLE_TRACING_ENABLE',
#     'struct__PROCESS_HANDLE_TRACING_ENABLE_EX',
#     'struct__PROCESS_HEAP_INFORMATION',
#     'struct__PROCESS_PRIORITY_CLASS',
#     'struct__PROCESS_SESSION_INFORMATION', 'struct__PS_ATTRIBUTE',
#     'struct__PS_ATTRIBUTE_LIST',
#     'struct__PS_BNO_ISOLATION_PARAMETERS', 'struct__PS_CREATE_INFO',
#     'struct__PS_MEMORY_RESERVE', 'struct__PS_PROTECTION',
#     'struct__PS_STD_HANDLE_INFO', 'struct__REG_NOTIFY_INFORMATION',
#     'struct__RIP_INFO', 'struct__RTLP_CURDIR_REF',
#     'struct__RTL_ACTIVATION_CONTEXT_STACK_FRAME',
#     'struct__RTL_BALANCED_NODE', 'struct__RTL_BITMAP',
#     'struct__RTL_BITMAP_RUN', 'struct__RTL_BUFFER',
#     'struct__RTL_CRITICAL_SECTION',
#     'struct__RTL_CRITICAL_SECTION_DEBUG',
#     'struct__RTL_DEBUG_INFORMATION',
#     'struct__RTL_DRIVE_LETTER_CURDIR', 'struct__RTL_HEAP_ENTRY',
#     'struct__RTL_HEAP_INFORMATION', 'struct__RTL_HEAP_PARAMETERS',
#     'struct__RTL_HEAP_TAG', 'struct__RTL_HEAP_TAG_INFO',
#     'struct__RTL_HEAP_WALK_ENTRY', 'struct__RTL_PROCESS_BACKTRACES',
#     'struct__RTL_PROCESS_HEAPS', 'struct__RTL_PROCESS_LOCKS',
#     'struct__RTL_PROCESS_MODULES',
#     'struct__RTL_PROCESS_MODULE_INFORMATION',
#     'struct__RTL_PROCESS_MODULE_INFORMATION_EX',
#     'struct__RTL_PROCESS_VERIFIER_OPTIONS',
#     'struct__RTL_RELATIVE_NAME_U', 'struct__RTL_SPLAY_LINKS',
#     'struct__RTL_SRWLOCK', 'struct__RTL_UNICODE_STRING_BUFFER',
#     'struct__RTL_USER_PROCESS_INFORMATION',
#     'struct__RTL_USER_PROCESS_PARAMETERS',
#     'struct__SECTION_BASIC_INFORMATION',
#     'struct__SECTION_IMAGE_INFORMATION',
#     'struct__SECTION_INTERNAL_IMAGE_INFORMATION',
#     'struct__SECURITY_QUALITY_OF_SERVICE',
#     'struct__SEMAPHORE_BASIC_INFORMATION',
#     'struct__SID_AND_ATTRIBUTES', 'struct__SID_IDENTIFIER_AUTHORITY',
#     'struct__SINGLE_LIST_ENTRY', 'struct__STRING',
#     'struct__SYSTEM_BASIC_INFORMATION',
#     'struct__SYSTEM_CONSOLE_INFORMATION',
#     'struct__SYSTEM_EXTENDED_THREAD_INFORMATION',
#     'struct__SYSTEM_HANDLE_INFORMATION',
#     'struct__SYSTEM_HANDLE_INFORMATION_EX',
#     'struct__SYSTEM_HANDLE_TABLE_ENTRY_INFO',
#     'struct__SYSTEM_HANDLE_TABLE_ENTRY_INFO_EX',
#     'struct__SYSTEM_KERNEL_DEBUGGER_INFORMATION',
#     'struct__SYSTEM_KERNEL_DEBUGGER_INFORMATION_EX',
#     'struct__SYSTEM_PROCESS_INFORMATION',
#     'struct__SYSTEM_SESSION_PROCESS_INFORMATION',
#     'struct__SYSTEM_THREAD_INFORMATION',
#     'struct__SYSTEM_TIMEOFDAY_INFORMATION', 'struct__TEB',
#     'struct__TEB_ACTIVE_FRAME', 'struct__TEB_ACTIVE_FRAME_CONTEXT',
#     'struct__THREAD_BASIC_INFORMATION',
#     'struct__TIMER_BASIC_INFORMATION',
#     'struct__TIMER_SET_COALESCABLE_TIMER_INFO',
#     'struct__TOKEN_DEFAULT_DACL', 'struct__TOKEN_GROUPS',
#     'struct__TOKEN_OWNER', 'struct__TOKEN_PRIMARY_GROUP',
#     'struct__TOKEN_PRIVILEGES',
#     'struct__TOKEN_SECURITY_ATTRIBUTES_INFORMATION',
#     'struct__TOKEN_SECURITY_ATTRIBUTE_FQBN_VALUE',
#     'struct__TOKEN_SECURITY_ATTRIBUTE_OCTET_STRING_VALUE',
#     'struct__TOKEN_SECURITY_ATTRIBUTE_V1', 'struct__TOKEN_SOURCE',
#     'struct__TOKEN_USER', 'struct__TP_ALPC',
#     'struct__TP_CALLBACK_ENVIRON_V3', 'struct__TP_CALLBACK_INSTANCE',
#     'struct__TP_CLEANUP_GROUP', 'struct__TP_IO', 'struct__TP_POOL',
#     'struct__TP_POOL_STACK_INFORMATION', 'struct__TP_TIMER',
#     'struct__TP_WAIT', 'struct__TP_WORK',
#     'struct__TRANSACTION_NOTIFICATION', 'struct__UNICODE_STRING',
#     'struct__UNLOAD_DLL_DEBUG_INFO',
#     'struct__WORKER_FACTORY_BASIC_INFORMATION',
#     'struct__XSAVE_FORMAT', 'struct__XSTATE_CONFIGURATION',
#     'struct__XSTATE_FEATURE', 'struct_struct (anonymous at C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.20348.0\\um\\winnt.h:13954:9)',
#     'struct_struct (anonymous at C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.20348.0\\um\\winnt.h:4244:9)',
#     'struct_struct (anonymous at C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.20348.0\\um\\winnt.h:857:5)',
#     'struct_struct (anonymous at C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.20348.0\\um\\winnt.h:877:5)',
#     'struct_struct (unnamed at ./nt_create_user_process/ntdll.h:1139:4)', 'struct_struct (unnamed at ./nt_create_user_process/ntdll.h:1171:4)', 'struct_struct_26',
#     'struct_struct (unnamed at ./nt_create_user_process/ntdll.h:1415:4)', 'struct_struct (unnamed at ./nt_create_user_process/ntdll.h:1475:4)', 'struct_struct_39', 'struct_struct (unnamed at ./nt_create_user_process/ntdll.h:1495:4)', 'struct_struct (unnamed at ./nt_create_user_process/ntdll.h:1501:4)', 'struct_struct_36', 'struct_struct (unnamed at ./nt_create_user_process/ntdll.h:1513:4)', 'struct_struct (unnamed at ./nt_create_user_process/ntdll.h:1518:6)', 'struct_struct_43', 'struct_struct (unnamed at ./nt_create_user_process/ntdll.h:2589:4)', 'struct_struct (unnamed at ./nt_create_user_process/ntdll.h:2615:4)', 'struct_struct_52', 'struct_struct (unnamed at ./nt_create_user_process/ntdll.h:2839:4)', 'struct_struct (unnamed at ./nt_create_user_process/ntdll.h:2883:4)', 'struct_struct_62', 'struct_struct (unnamed at ./nt_create_user_process/ntdll.h:3012:4)', 'struct_struct (unnamed at ./nt_create_user_process/ntdll.h:3072:4)', 'struct_struct_71', 'struct_struct (unnamed at ./nt_create_user_process/ntdll.h:3361:4)', 'struct_struct (unnamed at ./nt_create_user_process/ntdll.h:3366:4)', 'struct_struct_73', 'struct_struct (unnamed at ./nt_create_user_process/ntdll.h:3483:4)', 'struct_struct (unnamed at ./nt_create_user_process/ntdll.h:509:4)', 'struct_struct_11', 'struct_struct (unnamed at ./nt_create_user_process/ntdll.h:549:4)', 'struct_struct (unnamed at ./nt_create_user_process/ntdll.h:563:4)', 'struct_struct_12', 'struct_struct (unnamed at C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.20348.0\\um\\winnt.h:24067:9)',
#     'struct_struct (unnamed at C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.20348.0\\um\\winnt.h:861:5)', 'struct_struct (unnamed at C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.20348.0\\um\\winnt.h:8702:9)', 'struct_struct (unnamed at C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.20348.0\\um\\winnt.h:8708:9)', 'struct_struct (unnamed at C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.20348.0\\um\\winnt.h:881:5)',
#     'union__FILE_SEGMENT_ELEMENT', 'union__LARGE_INTEGER',
#     'union__ULARGE_INTEGER', 'union_union (anonymous at ./nt_create_user_process/ntdll.h:1084:3)', 'union_union (anonymous at ./nt_create_user_process/ntdll.h:1136:3)', 'union_union_25',
#     'union_union (anonymous at ./nt_create_user_process/ntdll.h:1239:3)', 'union_union (anonymous at ./nt_create_user_process/ntdll.h:1294:3)', 'union_union_29',
#     'union_union (anonymous at ./nt_create_user_process/ntdll.h:1472:3)', 'union_union (anonymous at ./nt_create_user_process/ntdll.h:2438:3)', 'union_union_63',
#     'union_union (anonymous at ./nt_create_user_process/ntdll.h:3474:3)', 'union_union (anonymous at ./nt_create_user_process/ntdll.h:978:3)', 'union_union (anonymous at C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.20348.0\\um\\winnt.h:12471:5)',
#     'union_union (anonymous at C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.20348.0\\um\\winnt.h:13952:5)',
#     'union_union (anonymous at C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.20348.0\\um\\winnt.h:4242:5)',
#     'union_union (unnamed at ./nt_create_user_process/ntdll.h:1145:3)', 'union_union (unnamed at ./nt_create_user_process/ntdll.h:1167:3)', 'union_union_38',
#     'union_union (unnamed at ./nt_create_user_process/ntdll.h:1515:5)', 'union_union (unnamed at ./nt_create_user_process/ntdll.h:2586:3)', 'union_union_49',
#     'union_union (unnamed at ./nt_create_user_process/ntdll.h:2627:3)', 'union_union (unnamed at ./nt_create_user_process/ntdll.h:2707:3)', 'union_union_56',
#     'union_union (unnamed at ./nt_create_user_process/ntdll.h:2875:3)', 'union_union (unnamed at ./nt_create_user_process/ntdll.h:2880:3)', 'union_union_61',
#     'union_union (unnamed at ./nt_create_user_process/ntdll.h:3009:3)', 'union_union (unnamed at ./nt_create_user_process/ntdll.h:3069:3)', 'union_union_70',
#     'union_union (unnamed at ./nt_create_user_process/ntdll.h:3359:3)', 'union_union (unnamed at ./nt_create_user_process/ntdll.h:3677:3)', 'union_union_76',
#     'union_union_2',
#     'union_union_10',
#     'union_union_9',
#     'union_union_3',
#     'union_union_13',
#     'union_union_14',
#     'union_union (unnamed at C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.20348.0\\um\\minwinbase.h:365:5)',
#     'union_union (unnamed at C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.20348.0\\um\\winnt.h:18578:5)',
#     'union_union (unnamed at C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.20348.0\\um\\winnt.h:24065:5)',
#     'union_union (unnamed at C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.20348.0\\um\\winnt.h:8701:5)']
