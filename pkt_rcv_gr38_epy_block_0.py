"""
Simple Python Block that Writes PDUs that 
pass their CRC to filename skips others
"""

import numpy as np
from gnuradio import gr
import pmt

class blk(gr.sync_block):

    def __init__(self, filename=None):
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Passed CRC To File',   # will show up in GRC
            in_sig=[],
            out_sig=[],
        )
        self.filename = filename

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_pdu)

    def handle_pdu(self, msg):
        meta_pmt = pmt.car(msg)
        payload_pmt = pmt.cdr(msg)

        print("Handle PDU received", str(msg))

        # Guard against None/NIL
        if meta_pmt == pmt.PMT_NIL or payload_pmt == pmt.PMT_NIL:
            print("Warning: received empty PDU")
            return

        meta = pmt.to_python(meta_pmt)
        payload = pmt.to_python(payload_pmt)

        if meta.get("crc_ok", False):
            data = pmt.u8vector_elements(payload)
            with open(self.filename, "ab") as f:
                f.write(bytearray(data))