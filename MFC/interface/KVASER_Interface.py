from canlib import canlib
from canlib.frame import Frame
import shutil
import time


bitrates = {
    '1M': canlib.Bitrate.BITRATE_1M,
    '500K': canlib.Bitrate.BITRATE_500K,
    '250K': canlib.Bitrate.BITRATE_250K,
    '125K': canlib.Bitrate.BITRATE_125K,
    '100K': canlib.Bitrate.BITRATE_100K,
    '62K': canlib.Bitrate.BITRATE_62K,
    '50K': canlib.Bitrate.BITRATE_50K,
    '83K': canlib.Bitrate.BITRATE_83K,
    '10K': canlib.Bitrate.BITRATE_10K,
}

openflags = {
    'INIT_ACCESS': canlib.canOPEN_REQUIRE_INIT_ACCESS,
    'NO_INIT_ACCESS': canlib.canOPEN_NO_INIT_ACCESS,
    'EXCLUSIVE': canlib.canOPEN_EXCLUSIVE,
}


class KVASER_Interface:
    def __init__(self, channel=0, flags="INIT_ACCESS", bit_rate="125K", timeout=float(0)):
        self.channel = channel
        self.openflags = openflags[flags.upper()]
        self.bit_rate = bitrates[bit_rate.upper()]
        self.timeout = timeout
        self.is_connected = False
        self.is_opened = False
        self.frame_write = None
        self.frame_read = None
        self.time_open = 0
        self.frame_write_count = 0
        self.frame_read_count = 0
        self.read_frame_available = False

        self.check_read_exception_message = False

        self.write_exception_count = 0
        self.read_exception_count = 0

    def connect(self):
        if self.is_connected:
            return 0
        try:
            self.ch = canlib.openChannel(self.channel, self.openflags, bitrate=self.bit_rate)
            self.is_connected = True
            print("connected")
        except Exception as e:
            print("connect", e)
            return -1
        if self.is_connected:
            self.ch.setBusOutputControl(canlib.canDRIVER_NORMAL)
        return 0

    def disconnect(self):
        if not self.is_connected:
            return -1
        try:
            self.ch.close()
            self.is_connected = False
            print("disconnected")
        except Exception as e:
            print("disconnected", e)
            return -1
        return 0

    def accept_filter(self, mask, code):
        if not self.is_connected:
            return
        self.ch.canAccept(mask, canlib.AcceptFilterFlag.SET_MASK_EXT)
        self.ch.canAccept(code, canlib.AcceptFilterFlag.SET_CODE_EXT)

    def open(self):
        if not self.is_connected:
            return
        self.ch.busOn()
        self.is_opened = True
        self.time_open = time.time()
        print("opened")

    def close(self):
        if not self.is_opened:
            return
        self.ch.busOff()
        self.is_opened = False
        print("closed")

    def write(self, id_, data, dlc=8):
        if not self.is_opened:
            return
        frame = Frame(id_=id_, data=data, dlc=dlc, flags=canlib.MessageFlag.EXT)
        try:
            self.ch.write(frame=frame)
            self.frame_write = frame
            self.frame_write_count += 1
        except Exception as e:
            self.write_exception_count += 1

    def write_wait(self, id_, data, dlc=8):
        if not self.is_opened:
            return
        # print("0x{0:02x}{1:02x}".format((data[0]), (data[1])))
        frame = Frame(id_=id_, data=data, dlc=dlc, flags=canlib.MessageFlag.EXT)
        try:
            self.ch.writeWait(frame=frame, timeout=int(self.timeout * 1000))
            self.frame_write = frame
            self.frame_write_count += 1
        except Exception as e:
            self.write_exception_count += 1

    def read(self):
        if not self.is_opened:
            return
        try:
            frame_read = self.ch.read(timeout=int(self.timeout * 1000))
            self.frame_read = frame_read
            self.frame_read_count += 1
            self.read_frame_available = True
            return frame_read
        except Exception as e:
            self.read_frame_available = False
            self.read_exception_count += 1

    def id(self, frame):
        if not self.read_frame_available:
            return 0
        return frame.id

    def data_bytearray(self, frame):
        if not self.read_frame_available:
            return bytearray()
        return frame.data

    def data_list(self, frame):
        if not self.read_frame_available:
            return []
        return list(frame.data)

    def dlc(self, frame):
        if not self.read_frame_available:
            return 0
        return frame.dlc

    def flags(self, frame):
        if not self.read_frame_available:
            return 0
        return frame.flags

    def timestamp(self, frame):
        if not self.read_frame_available:
            return 0
        return frame.timestamp

    def timestamp_system(self, frame):
        if not self.read_frame_available:
            return 0
        return self.time_open + (float(self.timestamp(frame))/1000.0)

    def printframe(self, frame):
        width, height = shutil.get_terminal_size((80, 20))
        form = '═^' + str(width - 1)
        print(format(" Frame received ", form))
        print("id:", hex(self.id(frame)))
        print("data:", self.data_bytearray(frame))
        print("dlc:", self.dlc(frame))
        print("flags:", self.flags(frame))
        print("timestamp:", self.timestamp(frame))

