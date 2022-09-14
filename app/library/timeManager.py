import serial
import time
from timeit import default_timer as clk

class timeManager(object):
	def __init__(self, port, baudrate=19200):
		self.ser = serial.Serial(port, baudrate=baudrate, bytesize=8, stopbits=1, parity='N')
		time.sleep(3)
		self.ser.reset_input_buffer()
		self.ser.reset_output_buffer()

	def send(self, tx):
		tx = bytearray(tx)
		#print(tx)
		try:
			self.ser.write(tx)
			time.sleep(2)
			self.ser.flush()
			time.sleep(2)
		except serial.SerialException as e:
			if e.args == (5, "WriteFile", "Access is denied."):
				raise IOError(serial.SerialException.errno.ENOENT, "Serial port disappeared.", self.ser.portstr)
			else:
				raise

	def receive(self):
		rx = bytearray()
		delay = 10e-3 # s
		timeout = 5 # s
		end_time = clk() + timeout
		while True:
			time_remaining = end_time - clk()
			if time_remaining < 0:
				break
			rx += self.ser.read(self.ser.inWaiting())
			if 0 in rx:
				break
			time.sleep(delay)
		if time_remaining <= 0:
			raise IOError(serial.SerialTimeoutException, "Communication timed out.")
		return rx