#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Packetized Transmit with FEC
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import blocks
import pmt
from gnuradio import digital
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
from gnuradio import iio
import sip
import threading



class new_packet_tx(gr.top_block, Qt.QWidget):

    def __init__(self, sps=2):
        gr.top_block.__init__(self, "Packetized Transmit with FEC", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Packetized Transmit with FEC")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "new_packet_tx")

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
        self.sps = sps

        ##################################################
        # Variables
        ##################################################
        self.ts_packet_size = ts_packet_size = 188
        self.rate = rate = 2
        self.polys = polys = [109, 79]
        self.packet_groups = packet_groups = 1
        self.k = k = 7
        self.constellation = constellation = digital.constellation_calcdist(digital.psk_4()[0], digital.psk_4()[1],
        4, 1, digital.constellation.AMPLITUDE_NORMALIZATION).base()
        self.constellation.set_npwr(1.0)
        self.constellation.gen_soft_dec_lut(8)
        self.tx_attenuation = tx_attenuation = 10
        self.samp_rate = samp_rate = int(1e6)
        self.rep = rep = 3
        self.pld_enc = pld_enc = fec.cc_encoder_make((1500*8),k, rate, polys, 0, fec.CC_TERMINATED, False)
        self.packet_length = packet_length = packet_groups*ts_packet_size
        self.hdr_format = hdr_format = digital.header_format_counter(digital.packet_utils.default_access_code, 3, constellation.bits_per_symbol())
        self.hdr_enc = hdr_enc = fec.dummy_encoder_make(8000)
        self.frame_sync_cols = frame_sync_cols = 200
        self.center_freq = center_freq = 915e6
        self.amp = amp = 0.5
        self.alpha = alpha = 0.45

        ##################################################
        # Blocks
        ##################################################

        self._tx_attenuation_range = qtgui.Range(0, 89, 1, 10, 200)
        self._tx_attenuation_win = qtgui.RangeWidget(self._tx_attenuation_range, self.set_tx_attenuation, "'tx_attenuation'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._tx_attenuation_win)
        self._frame_sync_cols_range = qtgui.Range(0, 40000, 1, 200, 200)
        self._frame_sync_cols_win = qtgui.RangeWidget(self._frame_sync_cols_range, self.set_frame_sync_cols, "'frame_sync_cols'", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._frame_sync_cols_win)
        self.qtgui_time_sink_x_0_1 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "Transmit Time Domain", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_1.set_update_time(0.10)
        self.qtgui_time_sink_x_0_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_1.enable_tags(True)
        self.qtgui_time_sink_x_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_1.enable_autoscale(False)
        self.qtgui_time_sink_x_0_1.enable_grid(False)
        self.qtgui_time_sink_x_0_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_1.enable_control_panel(False)
        self.qtgui_time_sink_x_0_1.enable_stem_plot(False)


        labels = ['Transmit re', 'Transmit im', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [0, 0, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0_1.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_1.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_1_win, 31, 0, 1, 1)
        for r in range(31, 32):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_raster_sink_x_0_1_0_0_0_0 = qtgui.time_raster_sink_b(
            samp_rate,
            64,
            frame_sync_cols,
            [],
            [],
            " Transmit Frames Bytes",
            1,
            None
        )

        self.qtgui_time_raster_sink_x_0_1_0_0_0_0.set_update_time(0.10)
        self.qtgui_time_raster_sink_x_0_1_0_0_0_0.set_intensity_range(0, 255)
        self.qtgui_time_raster_sink_x_0_1_0_0_0_0.enable_grid(False)
        self.qtgui_time_raster_sink_x_0_1_0_0_0_0.enable_axis_labels(True)
        self.qtgui_time_raster_sink_x_0_1_0_0_0_0.set_x_label("")
        self.qtgui_time_raster_sink_x_0_1_0_0_0_0.set_x_range(0.0, 0.0)
        self.qtgui_time_raster_sink_x_0_1_0_0_0_0.set_y_label("")
        self.qtgui_time_raster_sink_x_0_1_0_0_0_0.set_y_range(0.0, 0.0)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_raster_sink_x_0_1_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_raster_sink_x_0_1_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_raster_sink_x_0_1_0_0_0_0.set_color_map(i, colors[i])
            self.qtgui_time_raster_sink_x_0_1_0_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_raster_sink_x_0_1_0_0_0_0_win = sip.wrapinstance(self.qtgui_time_raster_sink_x_0_1_0_0_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_raster_sink_x_0_1_0_0_0_0_win, 29, 0, 1, 1)
        for r in range(29, 30):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_raster_sink_x_0_0 = qtgui.time_raster_sink_b(
            samp_rate,
            64,
            (frame_sync_cols*8),
            [],
            [],
            "Transmit Frames Bits",
            1,
            None
        )

        self.qtgui_time_raster_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_raster_sink_x_0_0.set_intensity_range(0, 1)
        self.qtgui_time_raster_sink_x_0_0.enable_grid(False)
        self.qtgui_time_raster_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_raster_sink_x_0_0.set_x_label("")
        self.qtgui_time_raster_sink_x_0_0.set_x_range(0.0, 0.0)
        self.qtgui_time_raster_sink_x_0_0.set_y_label("")
        self.qtgui_time_raster_sink_x_0_0.set_y_range(0.0, 0.0)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_raster_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_raster_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_raster_sink_x_0_0.set_color_map(i, colors[i])
            self.qtgui_time_raster_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_raster_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_raster_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_raster_sink_x_0_0_win, 28, 0, 1, 1)
        for r in range(28, 29):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.pdu_tagged_stream_to_pdu_0 = pdu.tagged_stream_to_pdu(gr.types.byte_t, 'packet_len')
        self.pdu_pdu_to_tagged_stream_0_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, 'packet_len')
        self.pdu_pdu_to_tagged_stream_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, 'packet_len')
        self.iio_pluto_sink_0_0_0 = iio.fmcomms2_sink_fc32('192.168.2.1' if '192.168.2.1' else iio.get_pluto_uri(), [True, True], 32768, False)
        self.iio_pluto_sink_0_0_0.set_len_tag_key('')
        self.iio_pluto_sink_0_0_0.set_bandwidth(int(samp_rate))
        self.iio_pluto_sink_0_0_0.set_frequency(int(center_freq))
        self.iio_pluto_sink_0_0_0.set_samplerate(int(samp_rate))
        self.iio_pluto_sink_0_0_0.set_attenuation(0, tx_attenuation)
        self.iio_pluto_sink_0_0_0.set_filter_params('Auto', '', 0, 0)
        self.fec_async_encoder_0_0 = fec.async_encoder(hdr_enc, True, False, False, 1500)
        self.fec_async_encoder_0 = fec.async_encoder(pld_enc, True, False, False, 1500)
        self.digital_protocol_formatter_async_0 = digital.protocol_formatter_async(hdr_format)
        self.digital_crc32_async_bb_1 = digital.crc32_async_bb(False)
        self.digital_constellation_modulator_0_0 = digital.generic_mod(
            constellation=constellation,
            differential=False,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=alpha,
            verbose=False,
            log=False,
            truncate=False)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_char*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, "packet_len", 0)
        self.blocks_stream_to_tagged_stream_0_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, packet_length, "packet_len")
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(1, gr.GR_MSB_FIRST)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(0.3)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_char*1, './test_video/mp4sample.ts', True, 0, 0)
        self.blocks_file_source_0_0.set_begin_tag(pmt.PMT_NIL)
        self._amp_range = qtgui.Range(0, 0.9, 0.005, 0.5, 200)
        self._amp_win = qtgui.RangeWidget(self._amp_range, self.set_amp, "Amplitude", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._amp_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.digital_crc32_async_bb_1, 'out'), (self.fec_async_encoder_0, 'in'))
        self.msg_connect((self.digital_protocol_formatter_async_0, 'header'), (self.fec_async_encoder_0_0, 'in'))
        self.msg_connect((self.digital_protocol_formatter_async_0, 'payload'), (self.pdu_pdu_to_tagged_stream_0, 'pdus'))
        self.msg_connect((self.fec_async_encoder_0, 'out'), (self.digital_protocol_formatter_async_0, 'in'))
        self.msg_connect((self.fec_async_encoder_0_0, 'out'), (self.pdu_pdu_to_tagged_stream_0_0, 'pdus'))
        self.msg_connect((self.pdu_tagged_stream_to_pdu_0, 'pdus'), (self.digital_crc32_async_bb_1, 'in'))
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.iio_pluto_sink_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_time_sink_x_0_1, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.qtgui_time_raster_sink_x_0_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0_0, 0), (self.pdu_tagged_stream_to_pdu_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.digital_constellation_modulator_0_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.qtgui_time_raster_sink_x_0_1_0_0_0_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_stream_to_tagged_stream_0_0, 0))
        self.connect((self.digital_constellation_modulator_0_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.pdu_pdu_to_tagged_stream_0_0, 0), (self.blocks_tagged_stream_mux_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "new_packet_tx")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps

    def get_ts_packet_size(self):
        return self.ts_packet_size

    def set_ts_packet_size(self, ts_packet_size):
        self.ts_packet_size = ts_packet_size
        self.set_packet_length(self.packet_groups*self.ts_packet_size)

    def get_rate(self):
        return self.rate

    def set_rate(self, rate):
        self.rate = rate

    def get_polys(self):
        return self.polys

    def set_polys(self, polys):
        self.polys = polys

    def get_packet_groups(self):
        return self.packet_groups

    def set_packet_groups(self, packet_groups):
        self.packet_groups = packet_groups
        self.set_packet_length(self.packet_groups*self.ts_packet_size)

    def get_k(self):
        return self.k

    def set_k(self, k):
        self.k = k

    def get_constellation(self):
        return self.constellation

    def set_constellation(self, constellation):
        self.constellation = constellation

    def get_tx_attenuation(self):
        return self.tx_attenuation

    def set_tx_attenuation(self, tx_attenuation):
        self.tx_attenuation = tx_attenuation
        self.iio_pluto_sink_0_0_0.set_attenuation(0,self.tx_attenuation)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.iio_pluto_sink_0_0_0.set_bandwidth(int(self.samp_rate))
        self.iio_pluto_sink_0_0_0.set_samplerate(int(self.samp_rate))
        self.qtgui_time_sink_x_0_1.set_samp_rate(self.samp_rate)

    def get_rep(self):
        return self.rep

    def set_rep(self, rep):
        self.rep = rep

    def get_pld_enc(self):
        return self.pld_enc

    def set_pld_enc(self, pld_enc):
        self.pld_enc = pld_enc

    def get_packet_length(self):
        return self.packet_length

    def set_packet_length(self, packet_length):
        self.packet_length = packet_length
        self.blocks_stream_to_tagged_stream_0_0.set_packet_len(self.packet_length)
        self.blocks_stream_to_tagged_stream_0_0.set_packet_len_pmt(self.packet_length)

    def get_hdr_format(self):
        return self.hdr_format

    def set_hdr_format(self, hdr_format):
        self.hdr_format = hdr_format

    def get_hdr_enc(self):
        return self.hdr_enc

    def set_hdr_enc(self, hdr_enc):
        self.hdr_enc = hdr_enc

    def get_frame_sync_cols(self):
        return self.frame_sync_cols

    def set_frame_sync_cols(self, frame_sync_cols):
        self.frame_sync_cols = frame_sync_cols
        self.qtgui_time_raster_sink_x_0_0.set_num_cols((self.frame_sync_cols*8))
        self.qtgui_time_raster_sink_x_0_1_0_0_0_0.set_num_cols(self.frame_sync_cols)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.iio_pluto_sink_0_0_0.set_frequency(int(self.center_freq))

    def get_amp(self):
        return self.amp

    def set_amp(self, amp):
        self.amp = amp

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--sps", dest="sps", type=eng_float, default=eng_notation.num_to_str(float(2)),
        help="Set Samples per Symbol [default=%(default)r]")
    return parser


def main(top_block_cls=new_packet_tx, options=None):
    if options is None:
        options = argument_parser().parse_args()

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(sps=options.sps)

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
