import pmt
from gnuradio import gr

class blk(gr.basic_block):
    """
    Generic PDU forwarder:
    Forwards messages from input_port_name → output_port_name
    """
    def __init__(self, input_port_name="in", output_port_name="pdus"):
        gr.basic_block.__init__(self,
            name="pdu_forwarder",
            in_sig=None,
            out_sig=None
        )

        self.input_port_name = input_port_name
        self.output_port_name = output_port_name

        # register dynamic ports
        self.message_port_register_in(pmt.intern(self.input_port_name))
        self.message_port_register_out(pmt.intern(self.output_port_name))

        # set handler
        self.set_msg_handler(pmt.intern(self.input_port_name), self.handle_msg)

    def handle_msg(self, msg):
        # forward the message unchanged
        self.message_port_pub(pmt.intern(self.output_port_name), msg)
