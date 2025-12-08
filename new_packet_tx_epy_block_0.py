from gnuradio import gr
import numpy as np
import pmt

class blk(gr.basic_block):
    def __init__(self, packet_len=188):
        gr.basic_block.__init__(
            self,
            name="pdu_chunker",
            in_sig=[np.uint8],
            out_sig=None,
        )

        self.packet_len = int(packet_len)
        self.buffer = bytearray()

        # add message output port
        self.message_port_register_out(pmt.intern("in"))

    def general_work(self, input_items, output_items):
        data = input_items[0]

        # append incoming data to buffer
        self.buffer.extend(data.tolist())

        # process full packets
        while len(self.buffer) >= self.packet_len:
            chunk = self.buffer[:self.packet_len]
            del self.buffer[:self.packet_len]

            # create PDU
            vec = pmt.init_u8vector(self.packet_len, chunk)
            meta = pmt.make_dict()

            # publish the PDU
            self.message_port_pub(pmt.intern("in"), pmt.cons(meta, vec))

        # consume all input data
        self.consume(0, len(data))
        return 0
