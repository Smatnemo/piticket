import subprocess
import time 
from datetime import datetime, timedelta
from piticket.utils import LOGGER
from piticket.py532lib.mifare import Mifare, MIFARE_FACTORY_KEY, MIFARE_SAFE_RETRIES, MIFARE_WAIT_FOR_ENTRY 
from piticket.py532lib.frame import Pn532Frame
from piticket.py532lib.constants import *

# Do not use this on sector 0. Keep MIFARE_FACTORY_KEY in block 3 of sector 0
# Use this key on all other sectors
CUSTOM_KEY_A = b'\x10\x28\x30\x89\x56\x32'
CUSTOM_KEY_B = b'\x10\x28\x30\x89\x56\x00'

# make shift database of our uids
UIDS = [b'\xf4\xd20r'] 

# Details of the customer
CUSTOMERS = {b'\xf4\xd20r':{'card_type':"student", # options student, elderly, 
                            'name':'Tertese',
                            'surname':'Moses',
                            'uid':b'\xf4\xd20r',
                            'sub_type':"month", # options week, month, year
                            'start_date':"",
                            'end_date':"",
                            'registered_date':""}}

# # NOTE: Sector 1 is locked out
# # Write start date to sector 2 block 1 - strip all none integer strings
# # Write end date to sector 2 block 2 - strip all none integer strings

def date_to_byte(date):
    """Unpack a date object and return a bytes object of the same date integers
    :param date: datetime object
    :type date: datetime
    
    :return data_byte: concatenated bytes of the individual integers in a datetime
    :rtype data_byte: bytes"""
    date_byte = bytes()
    date=date.strftime('%Y%m%d%H%M%S')
    return bytes(date,'utf-8')

def byte_to_date(date_byte):
    date_str = date_byte.decode('utf-8')
    date = datetime.strptime(date_str, '%Y%m%d%H%M%S')
    return date

def is_date_valid(start_date, end_date, current_date=None):
    """Check if current_date falls between the start date and the end date"""
    if current_date is None:
        current_date = datetime.now()
    return start_date < current_date < end_date

def detect_nfc():
    p = subprocess.run(['nfc-list'], capture_output=True)
    lines=p.stdout.decode().splitlines()
    print('Detecting card reader....')
    for line in lines:
        if 'libnfc' in line:
            print('libnfc is installed')
        if 'NFC reader' in line and 'opened' in line:
            print('NFC reader is connected and ready to use')
        if 'PN532' in line:
            print('Correct ic detected')
    return SmartCard()

class SmartCardException(Exception):
    pass

class SmartCard(Mifare):
    def __init__(self):
        Mifare.__init__(self)
        self._initialize()
    
    def _initialize(self):
        self.SAMconfigure()
        self.set_max_retries(MIFARE_WAIT_FOR_ENTRY)
        self.reset_i2c()

    def get_size(self):
        """Return the size of a mifare card in kb
        """

    def authenticate(self, sector, block, key_a=CUSTOM_KEY_A, key_b=CUSTOM_KEY_B):
        """Use key a or key b to authenticate a sector. 
        """
        self._uid = self.scan_field()
        if self._uid:
            if self.is_card_valid():
                address = self.mifare_address(sector,block)
                try:
                    # Authenticate using factory key a. Without this you can not access memory
                    self.mifare_auth_a(address, key_a) # raises IOError if card is moved swiftly
                    # card.mifare_auth_b(address, CUSTOM_KEY_B)
                    LOGGER.info('Successfully authenticated Key a')
                except IOError as ex:
                    LOGGER.error(f'{ex} - Could not authenticate card with key a')
                else:
                    try:
                        self.mifare_auth_b(address, key_b)
                        LOGGER.info('Successfully authenticated key b')
                        return True
                    except IOError as ex:
                        LOGGER.error(f'{ex} Could not authenticate card with key b')
            else:
                LOGGER.debug('Invalid card')

    def read(self, sector, block):
        """ Read card after authenticating it.
        :param sector: an abstract division of the mifare card for reference. A group of four blocks
        :type sector: int
        :param block: a memory location on the mifare card. value range 0 to 3 but use only 0 to 2
        :type block: int
         """
        if self.authenticate(sector, block):
            address = self.mifare_address(sector, block)
            data = bytearray(b'')
            
            try:
                data = self.mifare_read(address) # raises IOError
                return data
            except IOError as ex:
                return SmartCardException(f'{ex} Could not read address')
                    
    def write(self, data, sector, block):
        """Write card after authenticating it.
        :param sector: an abstract division of the mifare card into four blocks of sixteen bytes.
        :type sector: int
        :param block: division of a sector - four possible values, 0, 1, 2, 3
        :type block: int
        :param data: content to write to a block
        :type data: bytes or bytearray
        """
        if self.authenticate(sector, block):
            address = self.mifare_address(sector, block)
            try:
                # Write only the first 16 characters
                self.mifare_write_standard(address, data[:16])
                LOGGER.info('Successfully wrote data')
                return True
            except IOError as ex:
                return SmartCardException(f'{ex} - Could not write address')

    def is_card_valid(self, uids=UIDS):
        """Check if unique identifier is registered in our database
        :rtype: bool
        """
        # if the serial_number of the card is in our database return True
        # otherwise False
        if self._uid in uids:
            return True
        return False
    
    def close(self):
        self.event.set()