#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from gnuradio import gr
import numpy as np

class ts_file_writer_crc_stream(gr.basic_block):
    """
    Unwrap packets from Stream CRC32 (Check Mode) byte stream
    and write MPEG-TS packets to a file.
    """

    def __init__(self, header_len=12, ts_packet_size=188, crc_len=4, filename="/tmp/video.ts"):
        gr.basic_block.__init__(
            self,
            name="ts_file_writer_crc_stream",
            in_sig=[np.uint8],
            out_sig=[]
        )
        self.header_len = header_len
        self.ts_packet_size = ts_packet_size
        self.crc_len = crc_len
        self.packet_len = header_len + ts_packet_size + crc_len
        self.filename = filename

        self.buffer = bytearray()
        self.f = open(self.filename, "wb")

    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        self.buffer.extend(in0.tobytes())

        while len(self.buffer) >= self.packet_len:
            pkt = self.buffer[:self.packet_len]
            self.buffer = self.buffer[self.packet_len:]

            ts_payload = pkt[self.header_len:self.header_len+self.ts_packet_size]
            self.f.write(ts_payload)

        self.f.flush()
        self.consume(0, len(in0))
        return 0

    def stop(self):
        self.f.close()
        return True
