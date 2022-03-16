from labd.libs._serial import SerialProxy

#visa = VisaProxy(('192.168.1.49', 42922))
serial = SerialProxy(('192.168.107.58', 42922))
message = serial._echo('hello!')
