#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Polar encoder examples
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
from gnuradio import fec
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, pdu
from gnuradio.fec import polar
import sip
import threading



class fecapi_polar_encoders(gr.top_block, Qt.QWidget):

    def __init__(self, block_size=512, frame_size=30, puncpat='11'):
        gr.top_block.__init__(self, "Polar encoder examples", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Polar encoder examples")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "fecapi_polar_encoders")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Parameters
        ##################################################
        self.block_size = block_size
        self.frame_size = frame_size
        self.puncpat = puncpat

        ##################################################
        # Variables
        ##################################################
        self.n_info_bits = n_info_bits = frame_size * 8
        self.polar_config = polar_config = polar.load_frozen_bits_info(False, polar.CHANNEL_TYPE_BEC, block_size, n_info_bits, 0.0, 32)
        self.samp_rate = samp_rate = int(50e3)
        self.polar_encoder_tagged = polar_encoder_tagged = fec.polar_encoder.make(block_size,n_info_bits, polar_config['positions'], polar_config['values'], False)
        self.polar_encoder_stream = polar_encoder_stream = fec.polar_encoder.make(block_size,(frame_size * 8), polar_config['positions'], polar_config['values'], False)
        self.polar_encoder_async = polar_encoder_async = fec.polar_encoder.make(block_size,n_info_bits, polar_config['positions'], polar_config['values'], False)

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_time_sink_x_0_0_1 = qtgui.time_sink_f(
            2050, #size
            samp_rate, #samp_rate
            "", #name
            3, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_1.set_update_time(0.05)
        self.qtgui_time_sink_x_0_0_1.set_y_axis(-0.5, 1.5)

        self.qtgui_time_sink_x_0_0_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_1.enable_tags(True)
        self.qtgui_time_sink_x_0_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, 'packet_len')
        self.qtgui_time_sink_x_0_0_1.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_1.enable_grid(False)
        self.qtgui_time_sink_x_0_0_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_1.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_1.enable_stem_plot(False)


        labels = ['Polar extended encoder', 'Polar extended tagged encoder', 'Polar async encoder', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 0.6, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(3):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_1_win)
        self.pdu_tagged_stream_to_pdu_0 = pdu.tagged_stream_to_pdu(gr.types.byte_t, 'pkt_len')
        self.pdu_pdu_to_tagged_stream_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, 'pkt_len')
        self.fec_extended_tagged_encoder_0_0 = fec.extended_tagged_encoder(encoder_obj_list=polar_encoder_tagged, puncpat=puncpat, lentagname='length_tag', mtu=1500)
        self.fec_extended_encoder_0_0_0 = fec.extended_encoder(encoder_obj_list=polar_encoder_stream, threading= None, puncpat=puncpat)
        self.fec_async_encoder_0 = fec.async_encoder(polar_encoder_async, True, False, False, 1500)
        self.blocks_vector_source_x_0_1_0 = blocks.vector_source_b((frame_size//15)*[0, 0, 1, 0, 3, 0, 7, 0, 15, 0, 31, 0, 63, 0, 127], True, 1, [])
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, samp_rate,True)
        self.blocks_stream_to_tagged_stream_0_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, frame_size, 'pkt_len')
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, frame_size, 'length_tag')
        self.blocks_repack_bits_bb_0_0 = blocks.repack_bits_bb(8, 1, 'length_tag', False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(8, 1, 'pkt_len', False, gr.GR_MSB_FIRST)
        self.blocks_char_to_float_1_0_0_1 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_1_0_0 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0_1 = blocks.char_to_float(1, 1)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.fec_async_encoder_0, 'out'), (self.pdu_pdu_to_tagged_stream_0, 'pdus'))
        self.msg_connect((self.pdu_tagged_stream_to_pdu_0, 'pdus'), (self.fec_async_encoder_0, 'in'))
        self.connect((self.blocks_char_to_float_0_1, 0), (self.qtgui_time_sink_x_0_0_1, 2))
        self.connect((self.blocks_char_to_float_1_0_0, 0), (self.qtgui_time_sink_x_0_0_1, 0))
        self.connect((self.blocks_char_to_float_1_0_0_1, 0), (self.qtgui_time_sink_x_0_0_1, 1))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.blocks_char_to_float_0_1, 0))
        self.connect((self.blocks_repack_bits_bb_0_0, 0), (self.fec_extended_tagged_encoder_0_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_repack_bits_bb_0_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0_0, 0), (self.pdu_tagged_stream_to_pdu_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_stream_to_tagged_stream_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.fec_extended_encoder_0_0_0, 0))
        self.connect((self.blocks_vector_source_x_0_1_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.fec_extended_encoder_0_0_0, 0), (self.blocks_char_to_float_1_0_0, 0))
        self.connect((self.fec_extended_tagged_encoder_0_0, 0), (self.blocks_char_to_float_1_0_0_1, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0, 0), (self.blocks_repack_bits_bb_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "fecapi_polar_encoders")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_block_size(self):
        return self.block_size

    def set_block_size(self, block_size):
        self.block_size = block_size

    def get_frame_size(self):
        return self.frame_size

    def set_frame_size(self, frame_size):
        self.frame_size = frame_size
        self.set_n_info_bits(self.frame_size * 8)
        self.blocks_stream_to_tagged_stream_0.set_packet_len(self.frame_size)
        self.blocks_stream_to_tagged_stream_0.set_packet_len_pmt(self.frame_size)
        self.blocks_stream_to_tagged_stream_0_0.set_packet_len(self.frame_size)
        self.blocks_stream_to_tagged_stream_0_0.set_packet_len_pmt(self.frame_size)
        self.blocks_vector_source_x_0_1_0.set_data((self.frame_size//15)*[0, 0, 1, 0, 3, 0, 7, 0, 15, 0, 31, 0, 63, 0, 127], [])

    def get_puncpat(self):
        return self.puncpat

    def set_puncpat(self, puncpat):
        self.puncpat = puncpat

    def get_n_info_bits(self):
        return self.n_info_bits

    def set_n_info_bits(self, n_info_bits):
        self.n_info_bits = n_info_bits

    def get_polar_config(self):
        return self.polar_config

    def set_polar_config(self, polar_config):
        self.polar_config = polar_config

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0_1.set_samp_rate(self.samp_rate)

    def get_polar_encoder_tagged(self):
        return self.polar_encoder_tagged

    def set_polar_encoder_tagged(self, polar_encoder_tagged):
        self.polar_encoder_tagged = polar_encoder_tagged

    def get_polar_encoder_stream(self):
        return self.polar_encoder_stream

    def set_polar_encoder_stream(self, polar_encoder_stream):
        self.polar_encoder_stream = polar_encoder_stream

    def get_polar_encoder_async(self):
        return self.polar_encoder_async

    def set_polar_encoder_async(self, polar_encoder_async):
        self.polar_encoder_async = polar_encoder_async



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--block-size", dest="block_size", type=intx, default=512,
        help="Set Block size [default=%(default)r]")
    parser.add_argument(
        "--frame-size", dest="frame_size", type=intx, default=30,
        help="Set Frame Size [default=%(default)r]")
    return parser


def main(top_block_cls=fecapi_polar_encoders, options=None):
    if options is None:
        options = argument_parser().parse_args()

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(block_size=options.block_size, frame_size=options.frame_size)

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
