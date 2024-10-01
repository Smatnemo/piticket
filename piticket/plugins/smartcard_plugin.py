from datetime import datetime, timedelta
from threading import Thread, Event
from piticket import hookimpl 
from piticket.smartcard import detect_nfc, date_to_byte, SmartCardException
from piticket.utils import LOGGER 

class SmartCardPlugin:
    def __init__(self, plugin_manager):
        self.pm = plugin_manager
        self.smartcard = detect_nfc()

        self.start_date = None 
        self.end_date = None

        self.key_uid = None
        self.card_loop = None

    def reset_vars(self):
        self.start_date = None 
        self.end_date = None 
        self.card_loop = None 

    def read_card(self):
        """"""
        customer_details = {}
        for i in range(2, 4):
            j = 0
            while j < 3:
                data = self.smartcard.read(i, j)
                if isinstance(data, SmartCardException):
                    LOGGER.error(data)
                    continue
                elif data:
                    LOGGER.info(data)
                    customer_details[(i,j)] = data
                    j += 1
        if len(customer_details)==6:
            LOGGER.info("Done reading card details")
        else:
            LOGGER.error("Could not read all details")

    def write_card(self):
        """Write date details into card after payment
        """
        written = self.smartcard.write(self.start_date, 2, 1)
        if isinstance(written, SmartCardException):
            LOGGER.error(written)
        elif written:
            LOGGER.info("Successufully wrote start date")
            written = self.smartcard.write(self.end_date, 2, 2)
            if isinstance(written, SmartCardException):
                LOGGER.error(written)
            elif written:
                LOGGER.info('Successfully wrote end date')

    @hookimpl
    def piticket_cleanup(self, app):
        if self.smartcard.PN532:
            self.smartcard.close()

    @hookimpl
    def state_recharge_enter(self):
        # Read card to check if it is valid
        # If card is valid, start the next steps
        # To determine if card is valid, check if the card is in list
        # read the details of the card in sector 2 and 3
        # if the card is valid, Print Details of card and ask if 
        # customer will like to buy for a 30 day extra period
        # The 30 days will be added to the end date
        # End date will be rewritten to current end date + 30 days
        # 
        # If the card is invalid
        #   - if the card is not in our database return invalid card message
        #   - if the details in sector 2 don't exist return error
        #   - If the details in sector 3 don't exist return error
        # 
        # If the current date is after  end date
        # Write today as current date and today + 30 days as end date
        # 
        # Step 1 - pay
        # Step 2 - Recharge card
        # The following are steps for Step 2
        # Calculate start date and end date for programming card
        self.start_date = datetime.now()
        # Create a difference of 30 days and hours to midnight
        td = timedelta(days=30, seconds=59-self.start_date.second, microseconds=0.888889-self.start_date.microsecond, 
                        minutes=59-self.start_date.minute, hours=23-self.start_date.hour)
        self.end_date = self.start_date + td

        self.start_date = date_to_byte(self.start_date)
        self.end_date = date_to_byte(self.end_date)
        self.card_loop = Thread(target=self.read_card, args=())
        self.card_loop.start()
    
    @hookimpl 
    def state_recharge_do(self):
        """"""

    @hookimpl 
    def state_recharge_validate(self, cfg):
        """"""
        # Confirm that the customer details are complete
        # Display details on the screen and show options
        # Name
        # Options for week, month or year
        # Read the contents of the address
        # If the contents match the start and end dates above then it is successful
    
    @hookimpl 
    def state_recharge_exit(self):
        """"""
        self.smartcard.close()
        self.smartcard.reset_i2c()
        self.reset_vars()
