import os
import binascii
import struct
from config import *

def select_data(file):
    if not file.startswith('.') and file.endswith('.WAV'):
        return True
    else:
        return False

def Little(data):
    if len(data) == 4:
        data = struct.pack('<I', int(binascii.b2a_hex(data), 16))
        return binascii.b2a_hex(data)
    elif len(data) == 2:
        data = struct.pack('h', int(binascii.b2a_hex(data), 16))
        return binascii.b2a_hex(data)
    else:
        print()
        # data = struct.pack('', int(binascii.b2a_hex(data), 16))
        # return binascii.b2a_hex(data)

def Big(data):
    return binascii.b2a_hex(data)

files = [f for f in os.listdir(data_path) if select_data(f)]

file = open(data_path+files[2], 'rb')
l1 = file.readline()
l2 = file.readline()

blocks = [['ChunkID', 'B', 4], ['ChunkSize', 'L', 4], ['Format', 'B', 4]]

i = 0

for blc in blocks:
    if blc[1] == 'B':
        print(blc[0], '=', Big(l1[i:i+blc[2]]), "(", l1[i:i+blc[2]], ")")
    else:
        print(blc[0], '=', Little(l1[i:i+blc[2]]), "(", l1[i:i+blc[2]], ")")
    i += blc[2]

ChunkSize = b'3a980ff8'
print(int(ChunkSize, 16) + 8, end='\n')

blocks = [['Subchunk1ID', 'B', 4], ['Subchunk1', 'L', 4], ['AudioFormat', 'L', 2], ['NumChannels', 'L', 2],
          ['SampleRate', 'L', 4], ['ByteRate', 'L', 4], ['BlockAlign', 'L', 2], ['BitsPerSample', 'L', 2]]

i = str(binascii.b2a_hex(l1))[2:].index(str(binascii.hexlify(b'fmt'))[2:-1])//2
for blc in blocks:
    if blc[1] == 'B':
        print(blc[0], '=', Big(l1[i:i+blc[2]]), "(", l1[i:i+blc[2]], ")")
    else:
        print(blc[0], '=', Little(l1[i:i+blc[2]]), "(", l1[i:i+blc[2]], ")")
    i += blc[2]


extra = str(binascii.b2a_hex(l1))[2:].index(str(binascii.hexlify(b'data'))[2:-1])//2 - i
ExtraBlocks = [['ExtraParamSize', 'L', 2], ['ExtraParams', 'L', extra-2]]
if extra > 2:
    for blc in ExtraBlocks:
        if blc[0] == 'ExtraParams':
            print(l1[i:i+blc[2]])
            test = b'E2\xc8\x01\x00\x00D1417B600000\x17\x08!\x02\x13\x00\x00\x00\x17\x08"\x03\x13\x10\x00\x00\x00\x00,\x01\x00\x000C\x8f\xc4\xf6\xff\xcaBZ\xc6\xf3\xff\xcaBk\xc6\xf3\xff\xc8Bh\xc6\xf4\xff\xcaBh\xc6\xf3\xff\xcbBl\xc6\xf4\xff\xcbBl\xc6\xf4\xff\xc9BJ\xc6\xf4\xff\xc4B?\xc6\xf3\xff\xcaBR\xc6\xf3\xff\xc8BP\xc6\xf3\xff\xc6BH\xc6\xf3\xff\xc8BI\xc6\xf3\xff\xc7BA\xc6\xf3\xff\xc7B9\xc6\xf3\xff\xcbB6\xc6\xf3\xff\xcbB2\xc6\xf3\xff\xd2B)\xc6\xf4\xff\xceB\x0b\xc6\xf3\xff\xceB\x15\xc6\xf3\xff\xcdB\x17\xc6\xf3\xff\xcbB\x14\xc6\xf3\xff\xcfB\x10\xc6\xf3\xff\xccB\x13\xc6\xf3\xff\xccB\xf8\xc5\xf3\xff\xcaB\xfe\xc5999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999V.N.: 04.1.3MTE AURAL M2 Note...............Aural-M2'
            print(len(test))
            print(Little(test))
            
            # if blc[1] == 'B':
            #     print(blc[0], '=', Big(l1[i:i+blc[2]]), "(", l1[i:i+blc[2]], ")")
            # else:
            #     print(blc[0], '=', Little(l1[i:i+blc[2]]), "(", l1[i:i+blc[2]], ")")
        else:
            if blc[1] == 'B':
                print(blc[0], '=', Big(l1[i:i+blc[2]]), "(", l1[i:i+blc[2]], ")")
            else:
                print(blc[0], '=', Little(l1[i:i+blc[2]]), "(", l1[i:i+blc[2]], ")")
        i += blc[2]

print(f"extra param size : {int(b'544d', 16) + 8}")