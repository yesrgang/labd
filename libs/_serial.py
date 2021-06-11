""" proxy for controlling serial devices on remote computer through labrad

--- example usage
import labrad
from serial_server.proxy import SerialProxy

cxn = labrad.connect()
serial = SerialProxy(cxn.yesr5_serial)

# ``serial'' now acts like pyserial 3.x library
ser = serial.Serial('COM10')
ser.timeout = 0.1
ser.write('hello!\r\n')
"""
import socket

def _comm(data, host=('localhost', 4292), timeout=10):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(host)
    s.settimeout(timeout)
    s.send(data)
    r = s.recv(1024)
    return r 

class SerialProxy(object):
    def __init__(self, inithost=('localhost', 4292)):
        self._inithost = inithost
        r = _comm('START libs _serial.py'.encode(), inithost)
        self._libhost = inithost[0], int(r.decode())

    def __del__(self):
        r = _comm(f'STOP {self._libhost[1]}'.encode(), self._inithost)

    def Serial(self, port):
        return SerialSerialProxy(self._libhost)

class SerialSerialProxy(object):
    def __init__(self, serial_server, port):
        self.port = port
        self.serial_server.reopen_interface(self.port)

    @property
    def baudrate(self):
        return self.serial_server.baudrate(self.port)
    
    @baudrate.setter
    def baudrate(self, baudrate):
        self.serial_server.baudrate(self.port, baudrate)

    @property
    def bytesize(self):
        return self.serial_server.bytesize(self.port)
    
    @bytesize.setter
    def bytesize(self, bytesize):
        self.serial_server.bytesize(self.port, bytesize)
    
    @property
    def dsrdtr(self):
        return self.serial_server.dsrdtr(self.port)
    
    @dsrdtr.setter
    def dsrdtr(self, dsrdtr):
        self.serial_server.dsrdtr(self.port, dsrdtr)
    
    @property
    def parity(self):
        return self.serial_server.parity(self.port)
    
    @parity.setter
    def parity(self, parity):
        self.serial_server.parity(self.port, parity)
    
    def read(self, size=1):
        return self.serial_server.read(self.port, size)
    
    def read_until(self, expected='\n', size=None):
        return self.serial_server.read_until(self.port, expected, size)
    
    def readline(self, size=-1):
        return self.serial_server.readline(self.port, size)
    
    def readlines(self, size=-1):
        return self.serial_server.readlines(self.port, size)
    
    @property
    def rtscts(self):
        return self.serial_server.rtscts(self.port)
    
    @rtscts.setter
    def rtscts(self, rtscts):
        self.serial_server.rtscts(self.port, rtscts)
    
    @property
    def stopbits(self):
        return self.serial_server.stopbits(self.port)
    
    @stopbits.setter
    def stopbits(self, stopbits):
        self.serial_server.stopbits(self.port, stopbits)
    
    @property
    def timeout(self):
        return self.serial_server.timeout(self.port)
    
    @timeout.setter
    def timeout(self, timeout):
        self.serial_server.timeout(self.port, timeout)
    
    def write(self, data):
        return self.serial_server.write(self.port, data)
    
    def writelines(self, data):
        return self.serial_server.writelines(self.port, data)

from serial import Serial
import serial.tools.list_ports
from labrad.server import setting

from hardware_interface_server.server import HardwareInterfaceServer
from hardware_interface_server.exceptions import InterfaceAlreadyOpen
from hardware_interface_server.exceptions import InterfaceNotAvailable

class SerialServer(HardwareInterfaceServer):
    """Provides access to conputer's serial interface """
    name = '%LABRADNODE%_serial'
    
    def _get_available_interfaces(self):
        available_interfaces = [cp[0] for cp in serial.tools.list_ports.comports()]
        return available_interfaces

    def _get_open_interfaces(self):
        for interface_id, interface in self.interfaces.items():
            try:
                is_open = interface.isOpen()
                if not is_open:
                    del self.interfaces[interface_id]
            except:
                del self.interfaces[interface_id]

        return self.interfaces.keys()

    def _open_interface(self, interface_id):
        open_interfaces = self._get_open_interfaces()
        if interface_id in open_interfaces:
            return
#            raise InterfaceAlreadyOpen(interface_id)
        try:
            ser = Serial(interface_id)
        except:
            raise InterfaceNotAvailable(interface_id)
        self.interfaces[interface_id] = ser
    
    def _close_interface(self, interface_id):
        interface = self._get_interface(interface_id)
        interface.close()
        del self.interfaces[interface_id]
        
    @setting(10, interface_id='s')
    def baudrate(self, c, interface_id, baudrate=None):
        interface = self._get_interface(interface_id)
        if baudrate is not None:
            interface.baudrate = baudrate
        return interface.baudrate
    
    @setting(11, interface_id='s')
    def bytesize(self, c, interface_id, bytesize=None):
        interface = self._get_interface(interface_id)
        if bytesize is not None:
            interface.bytesize = bytesize
        return interface.bytesize
    
    @setting(12, interface_id='s')
    def dsrdtr(self, c, interface_id, dsrdtr=None):
        interface = self._get_interface(interface_id)
        if dsrdtr is not None:
            interface.dsrdtr = dsrdtr
        return interface.dsrdtr
    
    @setting(13, interface_id='s')
    def parity(self, c, interface_id, parity=None):
        interface = self._get_interface(interface_id)
        if parity is not None:
            interface.parity = parity
        return interface.parity
    
    @setting(14, interface_id='s', size='i')
    def read(self, c, interface_id, size=1):
        interface = self._get_interface(interface_id)
        result = interface.read(size)
        return result
    
    @setting(15, interface_id='s', expected='s', size='i')
    def read_until(self, c, interface_id, expected='\n', size=None):
        interface = self._get_interface(interface_id)
        result = interface.read_until(expected, size)
        return result
    
    @setting(16, interface_id='s', size='i')
    def readline(self, c, interface_id, size=-1):
        interface = self._get_interface(interface_id)
        result = interface.readline()
        return result
    
    @setting(17, interface_id='s', size='i')
    def readlines(self, c, interface_id, size=-1):
        interface = self._get_interface(interface_id)
        result = interface.readlines(size)
        return result

    
    @setting(18, interface_id='s')
    def rtscts(self, c, interface_id, rtscts=None):
        interface = self._get_interface(interface_id)
        if rtscts is not None:
            interface.rtscts = rtscts
        return interface.rtscts
    
    @setting(19, interface_id='s')
    def stopbits(self, c, interface_id, stopbits=None):
        interface = self._get_interface(interface_id)
        if stopbits is not None:
            interface.stopbits = stopbits
        return interface.stopbits
    
    @setting(20, interface_id='s')
    def timeout(self, c, interface_id, timeout=None):
        interface = self._get_interface(interface_id)
        if timeout is not None:
            interface.timeout = timeout
        return interface.timeout
    
    @setting(21, interface_id='s')
    def write(self, c, interface_id, data):
        interface = self._get_interface(interface_id)
        num_bytes = interface.write(data)
        return num_bytes

    @setting(22, interface_id='s')
    def writelines(self, c, interface_id, data):
        interface = self._get_interface(interface_id)
        interface.writelines(data)
