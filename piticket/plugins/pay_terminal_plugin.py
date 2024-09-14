from piticket import hookimpl 

class PayTerminalPlugin():

    name = "piticket-core: payment_terminal"

    def __init__(self, plugin_manager):
        self.pm = plugin_manager

    @hookimpl
    def piticket_cleanup(self, app):
        app.pay.close()
        app.pay.reset()

    @hookimpl 
    def state_pay_enter(self,app):
        # start listening
        app.pay.start_terminal(app.modified_ticket['price'].content)

    @hookimpl
    def state_pay_exit(self,app):
        app.pay.close()
        app.pay.reset()

    