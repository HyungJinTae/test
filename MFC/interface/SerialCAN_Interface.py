import shutil
from interface.SerialCAN_Header import *
from common.Setting import *


bitrates = {
    '1M': Bitrate.BITRATE_921K,
    '500K': Bitrate.BITRATE_460K,
    '250K': Bitrate.BITRATE_234K,
    '125K': Bitrate.BITRATE_115K,
    '57K': Bitrate.BITRATE_57K,
    '19K': Bitrate.BITRATE_19K,
}

openflags = {
    'INIT_ACCESS': Openflag.canOPEN_REQUIRE_INIT_ACCESS
}


class Serial_Interface:
    def __init__(self, com_port='', bit_rate=921600, timeout=float(1)):
        self.com_port = com_port
        self.bit_rate = bit_rate
        self.timeout = timeout
        self.is_connected = False
        self.is_opened = False
        self.frame_write_count = 0
        self.frame_read_count = 0
        self.check_read_exception_message = False
        self.write_exception_count = 0
        self.read_exception_count = 0

    def connect(self):
        if self.is_connected:
            return 0
        try:
            self.serial = serial.serial_for_url(self.com_port, baudrate=self.bit_rate, timeout=self.timeout)
            self.is_connected = True
            logger.info("connected")
        except Exception as e:
            logger.error(f"e->{e}")
            return -1
        return 0

    def disconnect(self):
        if not self.is_connected:
            return 0
        try:
            if self.is_opened:
                self.close()
            self.is_connected = False
            logger.info("disconnected")
        except Exception as e:
            logger.error(f"e->{e}")
            return -1
        return 0

    def open(self):
        if not self.is_connected:
            return -1
        self.serial_rw_th = ReaderThread(self.serial, SerialCANProtocol)
        self.serial_rw_th.start()
        self.serial_wr_th = WriterThread(self.serial, SerialCANProtocol)
        self.serial_wr_th.start()
        self.is_opened = True
        logger.info("opened")
        return 0

    def close(self):
        if not self.is_opened:
            return -1
        self.serial_rw_th.stop()
        self.is_opened = False
        logger.info("closed")
        return 0

    def write(self, frame: SerialCANFrame):
        if not self.is_opened:
            return -1
        try:
            #self.serial_rw_th.write(data=frame.serial_data())
            self.serial_wr_th.write(data=frame.serial_data())
            self.frame_write_count += 1
        except Exception as e:
            self.write_exception_count += 1
            logger.error(f"e->{e}")
            return -1
        return 0

    def write_wait(self, frame):
        return self.write(frame)


class SerialCAN_Interface:
    def __init__(self, channel=0, flags="INIT_ACCESS", bit_rate="125K", timeout=float(0.01)):
        """ no use flags, bit_rate, timeout"""
        self.channel = channel    # bcu channel starts from 1
        self.is_connected = False
        self.is_opened = False
        self.serial_inst = None
        self.time_open = time.time()
        self.write_wait_time = float(0.010)

    def setSerialInstance(self, serial_instance: Serial_Interface):
        self.serial_inst = serial_instance

    def connect(self):
        if self.serial_inst is None:
            return -1
        if self.is_connected:
            return 0
        if self.serial_inst.is_connected:
            self.is_connected = self.serial_inst.is_connected
            logger.info(f"{self.channel} is connected")
        return 0

    def disconnect(self):
        if self.serial_inst is None:
            return -1
        if not self.is_connected:
            return -1
        self.is_connected = self.serial_inst.is_connected
        return 0

    def accept_filter(self, mask=0x04000000, code=0):
        if not self.is_connected:
            return
        cmd = SCAN_PROTOCOL_CMD_CAN_FILTER
        data_list = [0] * SCAN_PROTOCOL_CAN_DATA_LENGTH
        data_list[0] = (code >> 24) & 0xFF
        data_list[1] = (code >> 16) & 0xFF
        data_list[2] = (code >> 8) & 0xFF
        data_list[3] = (code >> 0) & 0xFF
        data_list[4] = (mask >> 24) & 0xFF
        data_list[5] = (mask >> 16) & 0xFF
        data_list[6] = (mask >> 8) & 0xFF
        data_list[7] = (mask >> 0) & 0xFF
        frame = SerialCANConfigFrame(ch=self.channel, cmd=cmd, data=data_list)
        self.serial_inst.write(frame)

    def open(self):
        if not self.is_connected:
            return
        if self.is_opened:
            return
        if self.serial_inst.is_opened:
            self.is_opened = self.serial_inst.is_opened
            self.time_open = time.time()

    def close(self):
        if not self.is_opened:
            return
        self.is_opened = self.serial_inst.is_opened

    def write(self, id_, data_list, dlc=8):
        if not self.is_opened:
            return
        frame = SerialCANFrame(ch=self.channel, id_=id_, data=data_list, dlc=dlc)
        self.serial_inst.write(frame)

    def write_wait(self, id_, data, dlc=8):
        if not self.is_opened:
            return
        logger.info(f"{self.write_frame_queue_count()}")
        self.write(id_, data, dlc)

    def write_frame_queue_count(self):
        if not self.is_opened:
            return 0
        if not (self.wr_protocol() is None):
            return len(self.wr_protocol().write_frame_list)
        else:
            return 0

    def read(self):
        if not self.is_opened:
            return None
        qcount = self.read_frame_queue_count()
        if qcount > 0:
            logger.info(qcount)
            frame_read = self.protocol().frame_dict[self.channel].pop(0)
        else:
            frame_read = None
        return frame_read

    def read_frame_queue_count(self):
        if not self.is_opened:
            return 0
        if not (self.protocol() is None):
            return len(self.protocol().frame_dict[self.channel])
        else:
            return 0

    def protocol(self):
        return self.serial_inst.serial_rw_th.protocol

    def wr_protocol(self):
        return self.serial_inst.serial_wr_th.protocol

    def data_list(self, frame):
        if frame is None:
            return []
        return list(frame.data)

    def id(self, frame):
        if frame is None:
            return 0
        return frame.id

    def data_bytearray(self, frame):
        if frame is None:
            return bytearray()
        return frame.data

    def dlc(self, frame):
        if frame is None:
            return 0
        return frame.dlc

    def flags(self, frame):
        if frame is None:
            return 0
        return frame.flags

    def timestamp(self, frame):
        if frame is None:
            return 0
        return frame.timestamp

    def timestamp_system(self, frame):
        if frame is None:
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
