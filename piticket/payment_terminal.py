import serial
import time
import pygame
import multiprocessing
from threading import Thread, Event 
from datetime import datetime
from piticket.utils import LOGGER

PAYMENT_STATUS_EVENT = pygame.USEREVENT + 1

class PaymentTerminal:
    def __init__(self, port='/dev/ttyACM0'):
        """A serial port listener to recieve status of 
        payment from the arduino board
        """
        self.ser = None
        self.port = port
        self.status = None 
        self.event = Event()
        self.terminal_loop = None
        self.is_open = False
        self._initialize()
        # self.pool = TerminalPool()

    def _initialize(self):
        try:
            self.ser = serial.Serial(self.port, 115200) 
            self.is_open = self.ser.is_open
            # LOGGER.info(f'{self.port} is available for reading')
        except serial.serialutil.SerialException:
            self.ser = None 

    def _on_event(self):
        pygame.event.post(pygame.event.Event(PAYMENT_STATUS_EVENT, status=self.status.lower()))

    def start_terminal(self, data):
        """
        Send data and start terminal
        :param data: the data to be sent over the terminal
        :type data: string 
        """
        # Send message
        self.write(data)
        self.terminal_loop = Thread(target=self.start, args=())
        self.terminal_loop.start()

    def start(self):
        # if not self.ser:
        #     self._initialize()
        while self.is_open:
            if self.event.is_set():
                self.event = Event()
                break
            self.listen()
        LOGGER.info('Stopped listening')

    def listen(self):
        self.read()
        if self.status:
            self._on_event()
            self.status=None

    def read(self):
        if self.ser.in_waiting > 0:
            line = self.ser.readline().decode('utf-8').rstrip()
            if line.startswith('status:'):
                self.status = line.split(':')[1]

    def write(self, data):
        if not self.ser.is_open:
            raise SerialException()
        written = 0
        if not isinstance(data, (bytes, bytearray, memoryview)):
            if isinstance(data, str):
                # End of line is used because it is required in the arduino
                data = data+'\n'
                data = data.encode('utf-8')
            else:
                raise ValueError(f'{data} must be bytes, bytearray, memoryview or str')
        written = self.ser.write(data)
        if len(data) != written:
            raise Exception('Not all data was written')
        else:
            LOGGER.info('Sent data successfully')
            self.ser.reset_output_buffer()
            
    def is_available(self):
        """Detect if arduino is connected and ready on the specified port
        """
        if self.ser is None:
            return False 
        return True

    def reset(self):
        # Arduino resets when serial connection is made
        self._initialize()
        LOGGER.info('Successfully opened port')

    def stop(self):
        self.event.set()
        LOGGER.info('Closing terminal thread ....')
        if self.terminal_loop is None:
            return
        # Hold main thread until child thread is completely closed
        while self.terminal_loop.is_alive():
            LOGGER.info('Thread is still alive')

    def close(self):
        self.stop()
        self.ser.close()
        LOGGER.info('Terminal closed sucessfuly')
