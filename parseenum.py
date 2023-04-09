from enum import IntFlag

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

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("type", help="enum type", choices=["accessmask"], nargs="?", default="accessmask")
    parser.add_argument("value", help="enum value", nargs="?", default="0xffffffff")
    args = parser.parse_args()
    if args.type == "accessmask":
        value = parseInteger(args.value)
        flags = parseAccessMask(value)
        print(f"0x{value:08x}")
        for e in flags:
            print(f"0x{value:08x} {e.name}")
