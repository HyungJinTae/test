#-*- coding:utf-8 -*-
import sys
import time
import serial
import threading
import queue

from common.Setting import *

SCAN_SAFE_WRITE_WAIT_TIME = float(0.009)
SCAN_AVAILABLE_PERIODIC_TIME = float(0.010)

SCAN_PROTOCOL_CMD_CAN_DATA = 0
SCAN_PROTOCOL_CMD_CAN_START = (SCAN_PROTOCOL_CMD_CAN_DATA + 1)
SCAN_PROTOCOL_CMD_CAN_FILTER = (SCAN_PROTOCOL_CMD_CAN_START + 1)

SCAN_PROTOCOL_CAN_CH1 = 1
SCAN_PROTOCOL_CAN_CH2 = 2
SCAN_PROTOCOL_CAN_CH3 = 3
SCAN_PROTOCOL_CAN_DATA_LENGTH = 8

SCAN_PROTOCOL_SOF = 0x69
SCAN_PROTOCOL_EOF = 0x67
SCAN_PROTOCOL_LENGTH = 18
SCAN_PROTOCOL_MAX_FRAME_LENGTH = 32
SCAN_PROTOCOL_SOF_POS = 0
SCAN_PROTOCOL_EOF_POS = (SCAN_PROTOCOL_LENGTH - 1)
SCAN_PROTOCOL_CAN_NO_POS = 1
SCAN_PROTOCOL_CAN_IDE_POS = 2
SCAN_PROTOCOL_CAN_ID_POS = 2
SCAN_PROTOCOL_CAN_DATA_POS = 6
SCAN_PROTOCOL_CS_POS = (SCAN_PROTOCOL_EOF_POS - 1)
SCAN_PROTOCOL_ST_POS = (SCAN_PROTOCOL_CS_POS - 2)


class Bitrate:
    BITRATE_921K = 921600
    BITRATE_460K = 460800
    BITRATE_234K = 230400
    BITRATE_115K = 115200
    BITRATE_57K = 57600
    BITRATE_28K = 38400
    BITRATE_19K = 19200


class Openflag:
    canOPEN_REQUIRE_INIT_ACCESS = 1
    canOPEN_NO_INIT_ACCESS = 2


class SerialCANFrame:
    def __init__(self, ch, id_, data, dlc=None, flags=0, timestamp=None):
        data = bytearray(data)
        byte_ide = int(4).to_bytes(1, byteorder='big')
        byte_id = id_.to_bytes(4, byteorder='big')
        byte_sof = SCAN_PROTOCOL_SOF.to_bytes(1, byteorder="big")
        byte_eof = SCAN_PROTOCOL_EOF.to_bytes(1, byteorder="big")
        byte_ch = ch.to_bytes(1, byteorder="big")
        byte_st = int(0).to_bytes(2, byteorder="big")
        byte_cs = int(0).to_bytes(1, byteorder="big")

        if dlc is None:
            if len(data) <= 8:
                dlc = len(data)
            elif len(data) <= 12:
                dlc = 12
            elif len(data) <= 16:
                dlc = 16
            elif len(data) <= 20:
                dlc = 20
            elif len(data) <= 24:
                dlc = 24
            elif len(data) <= 32:
                dlc = 32
            elif len(data) <= 48:
                dlc = 48
            else:
                dlc = 64
            if dlc > len(data):
                data.extend([0] * (dlc - len(data)))
        elif dlc <= 8:
            data.extend([0] * (dlc - len(data)))

        self.ch = ch
        self.st = int(0)
        self.id = id_
        self.data = data
        self.dlc = dlc
        self.flags = flags
        self.timestamp = timestamp

        byte_cs = self._make_cs(byte_sof + byte_ch + byte_id + data + byte_st)

        self.ser_data = byte_sof + byte_ch + byte_id + data + byte_st + byte_cs + byte_eof

    def _make_cs(self, byte_array):
        cs = int(0)
        for b in list(byte_array):
            cs += b
        return (cs & 0xFF).to_bytes(1, byteorder="big")

    def serial_data(self):
        return self.ser_data


class SerialCANConfigFrame:
    def __init__(self, ch, cmd, data):
        data = bytearray(data)
        byte_id = int(0).to_bytes(4, byteorder='big')
        byte_sof = SCAN_PROTOCOL_SOF.to_bytes(1, byteorder="big")
        byte_eof = SCAN_PROTOCOL_EOF.to_bytes(1, byteorder="big")
        cmd_ch = int((ch & 0x0F) + ((cmd << 4) & 0xF0))
        byte_ch = cmd_ch.to_bytes(1, byteorder="big")
        byte_st = int(0).to_bytes(2, byteorder="big")
        byte_cs = int(0).to_bytes(1, byteorder="big")

        self.ch = ch
        self.cmd = cmd
        self.data = data

        byte_cs = self._make_cs(byte_sof + byte_ch + byte_id + data + byte_st)

        self.ser_data = byte_sof + byte_ch + byte_id + data + byte_st + byte_cs + byte_eof

    def _make_cs(self, byte_array):
        cs = int(0)
        for b in list(byte_array):
            cs += b
        return (cs & 0xFF).to_bytes(1, byteorder="big")

    def serial_data(self):
        return self.ser_data


class Protocol(object):
    """\
    Protocol as used by the ReaderThread. This base class provides empty
    implementations of all methods.
    """
    def __init__(self, frame_length):
        self.frame_length = frame_length
        self.frame_list = []
        self.frame_dict = {SCAN_PROTOCOL_CAN_CH1: [], SCAN_PROTOCOL_CAN_CH2: [], SCAN_PROTOCOL_CAN_CH3: []}
        self.write_frame_list = []

    def connection_made(self, transport):
        """Called when reader thread is started"""

    def data_received(self, data):
        """Called with snippets received from the serial port"""

    def connection_lost(self, exc):
        """\
        Called when the serial port is closed or the reader loop terminated
        otherwise.
        """
        if isinstance(exc, Exception):
            raise exc


class SerialCANProtocol(Protocol):
    def __init__(self):
        super().__init__(SCAN_PROTOCOL_LENGTH)

    # 연결 시작시 발생
    def connection_made(self, transport):
        self.transport = transport
        self.running = True

    # 연결 종료시 발생
    def connection_lost(self, exc):
        self.transport = None

    # 데이터가 들어오면 이곳에서 처리함.
    def data_received(self, data):
        # 입력된 데이터 queuing
        if data:
            data_list = list(data)
            cs = self.getCS(data_list[:SCAN_PROTOCOL_CS_POS])
            if (data_list[SCAN_PROTOCOL_SOF_POS] == SCAN_PROTOCOL_SOF and
                    data_list[SCAN_PROTOCOL_EOF_POS] == SCAN_PROTOCOL_EOF):
                if data_list[SCAN_PROTOCOL_CS_POS] == cs:
                    offset = SCAN_PROTOCOL_CAN_NO_POS
                    ch = int.from_bytes(data[offset:offset+1], 'big')
                    offset = SCAN_PROTOCOL_CAN_ID_POS
                    id_ = int.from_bytes(data[offset:offset+4], 'big')
                    offset = SCAN_PROTOCOL_CAN_DATA_POS
                    frame = SerialCANFrame(ch, id_, data[offset:offset+8], dlc=8)
                    offset = SCAN_PROTOCOL_ST_POS
                    frame.st = int.from_bytes(data[offset:offset+1], 'big')
                    self.frame_dict[ch].append(frame)
                    # if len(self.frame_dict[ch]) >= 256:
                    #    self.frame_dict[ch].pop(0)

    # 데이터 보낼 때 함수
    def write(self, data):
        logger.debug(data)
        self.transport.write(data)

    # 종료 체크
    def isDone(self):
        return self.running

    def getCS(self, data_list):
        cs = int(0)
        for b in data_list:
            cs += b
        return cs & 0xFF


class ReaderThread(threading.Thread):
    """\
    Implement a serial port read loop and dispatch to a Protocol instance (like
    the asyncio.Protocol) but do it with threads.
    Calls to close() will close the serial port but it is also possible to just
    stop() this thread and continue the serial port instance otherwise.
    """

    def __init__(self, serial_instance, protocol_factory):
        """\
        Initialize thread.
        Note that the serial_instance' timeout is set to one second!
        Other settings are not changed.
        """
        super(ReaderThread, self).__init__()
        self.daemon = True
        self.serial = serial_instance
        self.protocol_factory = protocol_factory
        self.alive = True
        self._lock = threading.Lock()
        self._connection_made = threading.Event()
        self.protocol = None

    def stop(self):
        """Stop the reader thread"""
        self.alive = False
        if hasattr(self.serial, 'cancel_read'):
            self.serial.cancel_read()
        self.join(2)

    def run(self):
        """Reader loop"""
        if not hasattr(self.serial, 'cancel_read'):
            self.serial.write_wait_time = 1
        self.protocol = self.protocol_factory()
        try:
            self.protocol.connection_made(self)
        except Exception as e:
            self.alive = False
            self.protocol.connection_lost(e)
            self._connection_made.set()
            return
        error = None
        self._connection_made.set()
        while self.alive and self.serial.is_open:
            try:
                # read all that is there or wait for one byte (blocking)
                data = self.serial.read(self.protocol.frame_length)
            except serial.SerialException as e:
                # probably some I/O problem such as disconnected USB serial
                # adapters -> exit
                error = e
                break
            else:
                if len(data) == SCAN_PROTOCOL_LENGTH:
                    # make a separated try-except for called used code
                    try:
                        self.protocol.data_received(data)
                    except Exception as e:
                        error = e
                        break
        self.alive = False
        self.protocol.connection_lost(error)
        self.protocol = None

    def write(self, data):
        """Thread safe writing (uses lock)"""
        with self._lock:
            self.serial.write(data)

    def close(self):
        """Close the serial port and exit reader thread (uses lock)"""
        # use the lock to let other threads finish writing
        with self._lock:
            # first stop reading, so that closing can be done on idle port
            self.stop()
            self.serial.close()

    def connect(self):
        """
        Wait until connection is set up and return the transport and protocol
        instances.
        """
        if self.alive:
            self._connection_made.wait()
            if not self.alive:
                raise RuntimeError('connection_lost already called')
            return (self, self.protocol)
        else:
            raise RuntimeError('already stopped')

    # - -  context manager, returns protocol

    def __enter__(self):
        """\
        Enter context handler. May raise RuntimeError in case the connection
        could not be created.
        """
        self.start()
        self._connection_made.wait()
        if not self.alive:
            raise RuntimeError('connection_lost already called')
        return self.protocol

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Leave context: close port"""
        self.close()


class WriterThread(threading.Thread):
    """\
    Implement a serial port read loop and dispatch to a Protocol instance (like
    the asyncio.Protocol) but do it with threads.
    Calls to close() will close the serial port but it is also possible to just
    stop() this thread and continue the serial port instance otherwise.
    """

    def __init__(self, serial_instance, protocol_factory):
        """\
        Initialize thread.
        Note that the serial_instance' timeout is set to one second!
        Other settings are not changed.
        """
        super(WriterThread, self).__init__()
        self.daemon = True
        self.serial = serial_instance
        self.protocol_factory = protocol_factory
        self.alive = True
        self._lock = threading.Lock()
        self._connection_made = threading.Event()
        self.protocol = None
        self.time_probe = time.time()

    def stop(self):
        """Stop the writer thread"""
        self.alive = False
        if hasattr(self.serial, 'cancel_write'):
            self.serial.cancel_read()
        self.join(2)

    def run(self):
        """Writer loop"""
        if not hasattr(self.serial, 'cancel_write'):
            self.serial.write_wait_time = 1
        self.protocol = self.protocol_factory()
        try:
            self.protocol.connection_made(self)
        except Exception as e:
            self.alive = False
            self.protocol.connection_lost(e)
            self._connection_made.set()
            return
        error = None
        self._connection_made.set()
        while self.alive and self.serial.is_open:
            probe = time.time()
            if (probe - self.time_probe) > (SCAN_SAFE_WRITE_WAIT_TIME + 0.003):
                logger.info(f"{probe - self.time_probe}, {len(self.protocol.write_frame_list)}")
            self.time_probe = probe

            try:
                len_ = len(self.protocol.write_frame_list)
                if len_:
                    write_data = self.protocol.write_frame_list.pop(0)
                    self.serial.write(write_data)
                time.sleep(SCAN_SAFE_WRITE_WAIT_TIME)
            except serial.SerialException as e:
                # probably some I/O problem such as disconnected USB serial
                # adapters -> exit
                error = e
                break
        self.alive = False
        self.protocol.connection_lost(error)
        self.protocol = None

    def write(self, data):
        self.protocol.write_frame_list.append(data)

    def close(self):
        """Close the serial port and exit reader thread (uses lock)"""
        # use the lock to let other threads finish writing
        with self._lock:
            # first stop reading, so that closing can be done on idle port
            self.stop()
            self.serial.close()

    def connect(self):
        """
        Wait until connection is set up and return the transport and protocol
        instances.
        """
        if self.alive:
            self._connection_made.wait()
            if not self.alive:
                raise RuntimeError('connection_lost already called')
            return (self, self.protocol)
        else:
            raise RuntimeError('already stopped')

    # - -  context manager, returns protocol

    def __enter__(self):
        """\
        Enter context handler. May raise RuntimeError in case the connection
        could not be created.
        """
        self.start()
        self._connection_made.wait()
        if not self.alive:
            raise RuntimeError('connection_lost already called')
        return self.protocol

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Leave context: close port"""
        self.close()
