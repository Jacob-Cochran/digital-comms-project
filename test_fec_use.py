#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
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
import numpy
import sip
import threading



class test_fec_use(gr.top_block, Qt.QWidget):

    def __init__(self, puncpat='11'):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "test_fec_use")

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
        self.puncpat = puncpat

        ##################################################
        # Variables
        ##################################################
        self.ts_packet_size = ts_packet_size = 188
        self.packet_groups = packet_groups = 1
        self.packet_length = packet_length = packet_groups*ts_packet_size
        self.constellation = constellation = digital.constellation_calcdist([-1-1j, -1+1j, 1+1j, 1-1j], [0, 1, 2, 3],
        4, 1, digital.constellation.AMPLITUDE_NORMALIZATION).base()
        self.constellation.set_npwr(1.0)
        self.thresh = thresh = 0
        self.rate = rate = 2
        self.polys = polys = [109, 79]
        self.k = k = 7
        self.frame_size = frame_size = packet_length
        self.bps = bps = constellation.bits_per_symbol()
        self.access_key = access_key = '11100001010110101110100010010011'
        self.samp_rate = samp_rate = int(1e6)
        self.hdr_format = hdr_format = digital.header_format_default(access_key, thresh, bps)
        self.enc_cc = enc_cc = fec.cc_encoder_make((frame_size*8),k, rate, polys, 0, fec.CC_STREAMING, False)
        self.dec_cc = dec_cc = fec.cc_decoder.make((frame_size*8),k, rate, polys, 0, (-1), fec.CC_STREAMING, False)

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_time_sink_x_1_1_2 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "TX Final PKT Bytes", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1_1_2.set_update_time(0.10)
        self.qtgui_time_sink_x_1_1_2.set_y_axis(0, 256)

        self.qtgui_time_sink_x_1_1_2.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1_1_2.enable_tags(True)
        self.qtgui_time_sink_x_1_1_2.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1_1_2.enable_autoscale(False)
        self.qtgui_time_sink_x_1_1_2.enable_grid(False)
        self.qtgui_time_sink_x_1_1_2.enable_axis_labels(True)
        self.qtgui_time_sink_x_1_1_2.enable_control_panel(False)
        self.qtgui_time_sink_x_1_1_2.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1_1_2.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1_1_2.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1_1_2.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1_1_2.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1_1_2.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1_1_2.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1_1_2.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_1_2_win = sip.wrapinstance(self.qtgui_time_sink_x_1_1_2.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_1_2_win)
        self.qtgui_time_sink_x_1_1_1 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "TX Payload No FEC", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1_1_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1_1_1.set_y_axis(0, 256)

        self.qtgui_time_sink_x_1_1_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1_1_1.enable_tags(True)
        self.qtgui_time_sink_x_1_1_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1_1_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1_1_1.enable_grid(False)
        self.qtgui_time_sink_x_1_1_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1_1_1.enable_control_panel(False)
        self.qtgui_time_sink_x_1_1_1.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1_1_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1_1_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1_1_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1_1_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1_1_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1_1_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1_1_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_1_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1_1_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_1_1_win)
        self.qtgui_time_sink_x_1_1_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "CRC Tag Stream In (bits)", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1_1_0.set_update_time(0.10)
        self.qtgui_time_sink_x_1_1_0.set_y_axis(-0.1, 1.1)

        self.qtgui_time_sink_x_1_1_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1_1_0.enable_tags(True)
        self.qtgui_time_sink_x_1_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1_1_0.enable_autoscale(False)
        self.qtgui_time_sink_x_1_1_0.enable_grid(False)
        self.qtgui_time_sink_x_1_1_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_1_1_0.enable_control_panel(False)
        self.qtgui_time_sink_x_1_1_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1_1_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1_1_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1_1_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1_1_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1_1_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_1_0_win = sip.wrapinstance(self.qtgui_time_sink_x_1_1_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_1_0_win)
        self.qtgui_time_sink_x_1_1 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "TX Payload with FEC", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1_1.set_y_axis(0, 256)

        self.qtgui_time_sink_x_1_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1_1.enable_tags(True)
        self.qtgui_time_sink_x_1_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1_1.enable_grid(False)
        self.qtgui_time_sink_x_1_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1_1.enable_control_panel(False)
        self.qtgui_time_sink_x_1_1.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_1_win)
        self.qtgui_time_sink_x_1_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "FEC Decoded Payload", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1_0.set_update_time(0.10)
        self.qtgui_time_sink_x_1_0.set_y_axis(0, 256)

        self.qtgui_time_sink_x_1_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1_0.enable_tags(True)
        self.qtgui_time_sink_x_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1_0.enable_autoscale(False)
        self.qtgui_time_sink_x_1_0.enable_grid(False)
        self.qtgui_time_sink_x_1_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_1_0.enable_control_panel(False)
        self.qtgui_time_sink_x_1_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_0_win = sip.wrapinstance(self.qtgui_time_sink_x_1_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_0_win)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "Received Payload after Correlate", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(0, 256)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        self.qtgui_time_sink_x_1.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_win)
        self.fec_extended_tagged_encoder_0_0 = fec.extended_tagged_encoder(encoder_obj_list=enc_cc, puncpat='11', lentagname="packet_len", mtu=1000)
        self.fec_extended_tagged_decoder_0 = self.fec_extended_tagged_decoder_0 = fec_extended_tagged_decoder_0 = fec.extended_tagged_decoder(decoder_obj_list=dec_cc, ann=None, puncpat='11', integration_period=10000, lentagname="packet_len", mtu=1000)
        self.digital_protocol_formatter_bb_0 = digital.protocol_formatter_bb(hdr_format, "packet_len")
        self.digital_map_bb_0 = digital.map_bb([-1, 1])
        self.digital_crc32_bb_0_0 = digital.crc32_bb(False, "packet_len", True)
        self.digital_correlate_access_code_xx_ts_0_0_0 = digital.correlate_access_code_bb_ts(access_key,
          thresh, "packet_len")
        self.blocks_vector_source_x_0_0 = blocks.vector_source_b(numpy.zeros(188, dtype=numpy.uint8).tolist(), True, 1, [])
        self.blocks_vector_source_x_0 = blocks.vector_source_b(numpy.tile(numpy.arange(188, dtype=numpy.uint8), 1000).tolist(), True, 1, [])
        self.blocks_uchar_to_float_1_1_2 = blocks.uchar_to_float()
        self.blocks_uchar_to_float_1_1_1 = blocks.uchar_to_float()
        self.blocks_uchar_to_float_1_1_0 = blocks.uchar_to_float()
        self.blocks_uchar_to_float_1_1 = blocks.uchar_to_float()
        self.blocks_uchar_to_float_1_0 = blocks.uchar_to_float()
        self.blocks_uchar_to_float_1 = blocks.uchar_to_float()
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_char*1, (samp_rate/10), True, 0 if "auto" == "auto" else max( int(float(0.1) * (samp_rate/10)) if "auto" == "time" else int(0.1), 1) )
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, "packet_len", 0)
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_char * 1, False)
        self.blocks_tag_gate_0.set_single_key("")
        self.blocks_stream_to_tagged_stream_0_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, packet_length, "packet_len")
        self.blocks_stream_mux_0 = blocks.stream_mux(gr.sizeof_char*1, (188, 188))
        self.blocks_repack_bits_bb_1_0_1 = blocks.repack_bits_bb(8, 1, "", False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_1_0_0_0_0_0_0 = blocks.repack_bits_bb(1, 8, "packet_len", False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_1_0_0_0_0_0 = blocks.repack_bits_bb(8, 1, "packet_len", False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_1_0_0_0_0 = blocks.repack_bits_bb(1, 8, "packet_len", False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0_2 = blocks.repack_bits_bb(1, 8, "packet_len", False, gr.GR_MSB_FIRST)
        self.blocks_char_to_float_1 = blocks.char_to_float(1, 1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_char_to_float_1, 0), (self.fec_extended_tagged_decoder_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_2, 0), (self.blocks_uchar_to_float_1_0, 0))
        self.connect((self.blocks_repack_bits_bb_1_0_0_0_0, 0), (self.blocks_uchar_to_float_1, 0))
        self.connect((self.blocks_repack_bits_bb_1_0_0_0_0_0, 0), (self.fec_extended_tagged_encoder_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_1_0_0_0_0_0_0, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.blocks_repack_bits_bb_1_0_0_0_0_0_0, 0), (self.blocks_uchar_to_float_1_1, 0))
        self.connect((self.blocks_repack_bits_bb_1_0_0_0_0_0_0, 0), (self.digital_protocol_formatter_bb_0, 0))
        self.connect((self.blocks_repack_bits_bb_1_0_1, 0), (self.blocks_uchar_to_float_1_1_0, 0))
        self.connect((self.blocks_repack_bits_bb_1_0_1, 0), (self.digital_correlate_access_code_xx_ts_0_0_0, 0))
        self.connect((self.blocks_stream_mux_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0_0, 0), (self.digital_crc32_bb_0_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.blocks_repack_bits_bb_1_0_1, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.blocks_tag_gate_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.blocks_uchar_to_float_1_1_2, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_stream_to_tagged_stream_0_0, 0))
        self.connect((self.blocks_uchar_to_float_1, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.blocks_uchar_to_float_1_0, 0), (self.qtgui_time_sink_x_1_0, 0))
        self.connect((self.blocks_uchar_to_float_1_1, 0), (self.qtgui_time_sink_x_1_1, 0))
        self.connect((self.blocks_uchar_to_float_1_1_0, 0), (self.qtgui_time_sink_x_1_1_0, 0))
        self.connect((self.blocks_uchar_to_float_1_1_1, 0), (self.qtgui_time_sink_x_1_1_1, 0))
        self.connect((self.blocks_uchar_to_float_1_1_2, 0), (self.qtgui_time_sink_x_1_1_2, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_stream_mux_0, 0))
        self.connect((self.blocks_vector_source_x_0_0, 0), (self.blocks_stream_mux_0, 1))
        self.connect((self.digital_correlate_access_code_xx_ts_0_0_0, 0), (self.blocks_repack_bits_bb_1_0_0_0_0, 0))
        self.connect((self.digital_correlate_access_code_xx_ts_0_0_0, 0), (self.digital_map_bb_0, 0))
        self.connect((self.digital_crc32_bb_0_0, 0), (self.blocks_repack_bits_bb_1_0_0_0_0_0, 0))
        self.connect((self.digital_crc32_bb_0_0, 0), (self.blocks_uchar_to_float_1_1_1, 0))
        self.connect((self.digital_map_bb_0, 0), (self.blocks_char_to_float_1, 0))
        self.connect((self.digital_protocol_formatter_bb_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.fec_extended_tagged_decoder_0, 0), (self.blocks_repack_bits_bb_0_2, 0))
        self.connect((self.fec_extended_tagged_encoder_0_0, 0), (self.blocks_repack_bits_bb_1_0_0_0_0_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "test_fec_use")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_puncpat(self):
        return self.puncpat

    def set_puncpat(self, puncpat):
        self.puncpat = puncpat

    def get_ts_packet_size(self):
        return self.ts_packet_size

    def set_ts_packet_size(self, ts_packet_size):
        self.ts_packet_size = ts_packet_size
        self.set_packet_length(self.packet_groups*self.ts_packet_size)

    def get_packet_groups(self):
        return self.packet_groups

    def set_packet_groups(self, packet_groups):
        self.packet_groups = packet_groups
        self.set_packet_length(self.packet_groups*self.ts_packet_size)

    def get_packet_length(self):
        return self.packet_length

    def set_packet_length(self, packet_length):
        self.packet_length = packet_length
        self.set_frame_size(self.packet_length)
        self.blocks_stream_to_tagged_stream_0_0.set_packet_len(self.packet_length)
        self.blocks_stream_to_tagged_stream_0_0.set_packet_len_pmt(self.packet_length)

    def get_constellation(self):
        return self.constellation

    def set_constellation(self, constellation):
        self.constellation = constellation

    def get_thresh(self):
        return self.thresh

    def set_thresh(self, thresh):
        self.thresh = thresh
        self.set_hdr_format(digital.header_format_default(self.access_key, self.thresh, self.bps))

    def get_rate(self):
        return self.rate

    def set_rate(self, rate):
        self.rate = rate

    def get_polys(self):
        return self.polys

    def set_polys(self, polys):
        self.polys = polys

    def get_k(self):
        return self.k

    def set_k(self, k):
        self.k = k

    def get_frame_size(self):
        return self.frame_size

    def set_frame_size(self, frame_size):
        self.frame_size = frame_size

    def get_bps(self):
        return self.bps

    def set_bps(self, bps):
        self.bps = bps
        self.set_hdr_format(digital.header_format_default(self.access_key, self.thresh, self.bps))

    def get_access_key(self):
        return self.access_key

    def set_access_key(self, access_key):
        self.access_key = access_key
        self.set_hdr_format(digital.header_format_default(self.access_key, self.thresh, self.bps))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle2_0.set_sample_rate((self.samp_rate/10))
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_1_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_1_1.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_1_1_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_1_1_1.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_1_1_2.set_samp_rate(self.samp_rate)

    def get_hdr_format(self):
        return self.hdr_format

    def set_hdr_format(self, hdr_format):
        self.hdr_format = hdr_format
        self.digital_protocol_formatter_bb_0.set_header_format(self.hdr_format)

    def get_enc_cc(self):
        return self.enc_cc

    def set_enc_cc(self, enc_cc):
        self.enc_cc = enc_cc

    def get_dec_cc(self):
        return self.dec_cc

    def set_dec_cc(self, dec_cc):
        self.dec_cc = dec_cc



def argument_parser():
    parser = ArgumentParser()
    return parser


def main(top_block_cls=test_fec_use, options=None):
    if options is None:
        options = argument_parser().parse_args()

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

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
