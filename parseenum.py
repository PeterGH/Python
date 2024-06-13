from enum import IntEnum, IntFlag

class AccessMask(IntFlag):
    GENERIC_READ =           0x80000000
    GENERIC_WRITE =          0x40000000
    GENERIC_EXECUTE =        0x20000000
    GENERIC_ALL =            0x10000000
    MAXIMUM_ALLOWED =        0x02000000
    ACCESS_SYSTEM_SECURITY = 0x01000000
    SYNCHRONIZE =            0x00100000
    WRITE_OWNER =            0x00080000
    WRITE_DAC =              0x00040000
    READ_CONTROL =           0x00020000
    DELETE =                 0x00010000
    FILE_WRITE_ATTRIBUTES =                     0x0100
    FILE_READ_ATTRIBUTES =                      0x0080
    FILE_DELETE_CHILD =                         0x0040
    FILE_EXECUTE_OR_FILE_TRAVERSE =             0x0020
    FILE_WRITE_EA =                             0x0010
    FILE_READ_EA =                              0x0008
    FILE_APPEND_DATA_OR_FILE_ADD_SUBDIRECTORY = 0x0004
    FILE_WRITE_DATA_OR_FILE_ADD_FILE =          0x0002
    FILE_READ_DATA_OR_FILE_LIST_DIRECTORY =     0x0001

class CreateDisposition(IntEnum):
    FILE_SUPERSEDE =                0x00000000
    FILE_OPEN =                     0x00000001
    FILE_CREATE =                   0x00000002
    FILE_OPEN_IF =                  0x00000003
    FILE_OVERWRITE =                0x00000004
    FILE_OVERWRITE_IF =             0x00000005
    FILE_MAXIMUM_DISPOSITION =      0x00000005

class CreateOption(IntFlag):
    FILE_DIRECTORY_FILE =                   0x00000001
    FILE_WRITE_THROUGH =                    0x00000002
    FILE_SEQUENTIAL_ONLY =                  0x00000004
    FILE_NO_INTERMEDIATE_BUFFERING =        0x00000008
    FILE_SYNCHRONOUS_IO_ALERT =             0x00000010
    FILE_SYNCHRONOUS_IO_NONALERT =          0x00000020
    FILE_NON_DIRECTORY_FILE =               0x00000040
    FILE_CREATE_TREE_CONNECTION =           0x00000080
    FILE_COMPLETE_IF_OPLOCKED =             0x00000100
    FILE_NO_EA_KNOWLEDGE =                  0x00000200
    FILE_OPEN_REMOTE_INSTANCE =             0x00000400
    FILE_RANDOM_ACCESS =                    0x00000800
    FILE_DELETE_ON_CLOSE =                  0x00001000
    FILE_OPEN_BY_FILE_ID =                  0x00002000
    FILE_OPEN_FOR_BACKUP_INTENT =           0x00004000
    FILE_NO_COMPRESSION =                   0x00008000
    FILE_OPEN_REQUIRING_OPLOCK =            0x00010000
    FILE_RESERVE_OPFILTER =                 0x00100000
    FILE_OPEN_REPARSE_POINT =               0x00200000
    FILE_OPEN_NO_RECALL =                   0x00400000
    FILE_OPEN_FOR_FREE_SPACE_QUERY =        0x00800000

def parseInteger(str):
    if len(str) > 2 and str[0] == '0' and (str[1] == 'x' or str[1] == 'X'):
        return int(str, base=16)
    else:
        return int(str)

def parseAccessMask(mask):
    result = []
    for m in AccessMask:
        if mask & m.value:
            result.append(m)
    return result

def parseCreateDisposition(mask):
    result = []
    for m in CreateDisposition:
        if mask == m.value:
            result.append(m)
    return result

def parseCreateOption(mask):
    result = []
    for m in CreateOption:
        if mask & m.value:
            result.append(m)
    return result

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("type", help="enum type", choices=["accessmask", "createdisposition", "createoption"], nargs="?", default="accessmask")
    parser.add_argument("value", help="enum value", nargs="?", default="0xffffffff")
    args = parser.parse_args()
    value = parseInteger(args.value)
    if args.type == "accessmask":
        flags = parseAccessMask(value)
    elif args.type == "createdisposition":
        flags = parseCreateDisposition(value)
    elif args.type == "createoption":
        flags = parseCreateOption(value)
    print(f"0x{value:08x}")
    for e in flags:
        print(f"0x{e.value:08x} {e.name}")
