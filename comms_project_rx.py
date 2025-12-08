#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Packetized MPEG Receiver
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import blocks
from gnuradio import blocks, gr
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import iio
import math
import numpy
import sip
import threading



class comms_project_rx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Packetized MPEG Receiver", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Packetized MPEG Receiver")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "comms_project_rx")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.constellation = constellation = digital.constellation_calcdist([-1-1j, -1+1j, 1+1j, 1-1j], [0, 1, 2, 3],
        4, 1, digital.constellation.AMPLITUDE_NORMALIZATION).base()
        self.constellation.set_npwr(1.0)
        self.ts_packet_size = ts_packet_size = 188
        self.thresh = thresh = 0
        self.sps = sps = 16
        self.samp_rate = samp_rate = int(1e6)
        self.packet_groups = packet_groups = 1
        self.nfilts = nfilts = 32
        self.bps = bps = constellation.bits_per_symbol()
        self.alpha = alpha = 0.45
        self.access_key = access_key = '11100001010110101110100010010011'
        self.timing_error_loop_bandwith = timing_error_loop_bandwith = 0.045
        self.rcc_taps = rcc_taps = firdes.root_raised_cosine(nfilts, nfilts*samp_rate,samp_rate/sps, alpha, (11*sps*nfilts))
        self.packet_length = packet_length = packet_groups*ts_packet_size
        self.out_frame_sync_cols = out_frame_sync_cols = 200
        self.hdr_format = hdr_format = digital.header_format_default(access_key, thresh, bps)
        self.costas_loop_bandwidth_in_cycles_per_sample = costas_loop_bandwidth_in_cycles_per_sample = 0.01
        self.cfo_offset = cfo_offset = 200
        self.center_freq = center_freq = 915e6
        self.agc_rate = agc_rate = 1e-4

        ##################################################
        # Blocks
        ##################################################

        self._timing_error_loop_bandwith_range = qtgui.Range(0, 1, 0.0001, 0.045, 200)
        self._timing_error_loop_bandwith_win = qtgui.RangeWidget(self._timing_error_loop_bandwith_range, self.set_timing_error_loop_bandwith, "'timing_error_loop_bandwith'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._timing_error_loop_bandwith_win, 5, 3, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._out_frame_sync_cols_range = qtgui.Range(0, 1600, 1, 200, 200)
        self._out_frame_sync_cols_win = qtgui.RangeWidget(self._out_frame_sync_cols_range, self.set_out_frame_sync_cols, "'out_frame_sync_cols'", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._out_frame_sync_cols_win)
        self._costas_loop_bandwidth_in_cycles_per_sample_range = qtgui.Range(0.0001, 0.2, 0.0001, 0.01, 200)
        self._costas_loop_bandwidth_in_cycles_per_sample_win = qtgui.RangeWidget(self._costas_loop_bandwidth_in_cycles_per_sample_range, self.set_costas_loop_bandwidth_in_cycles_per_sample, "'costas_loop_bandwidth_in_cycles_per_sample'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._costas_loop_bandwidth_in_cycles_per_sample_win, 6, 2, 1, 2)
        for r in range(6, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._cfo_offset_range = qtgui.Range(-200e3, 200e3, 1, 200, 200)
        self._cfo_offset_win = qtgui.RangeWidget(self._cfo_offset_range, self.set_cfo_offset, "'cfo_offset'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._cfo_offset_win, 0, 0, 1, 4)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._agc_rate_range = qtgui.Range(0, 1, 0.0001, 1e-4, 200)
        self._agc_rate_win = qtgui.RangeWidget(self._agc_rate_range, self.set_agc_rate, "'agc_rate'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._agc_rate_win, 5, 2, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            center_freq, #fc
            samp_rate, #bw
            "Received Frequency Raster", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win, 1, 2, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_2_0_0 = qtgui.time_sink_f(
            256, #size
            samp_rate, #samp_rate
            'Correlate input', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_2_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_2_0_0.set_y_axis(-0.1, 1.1)

        self.qtgui_time_sink_x_0_2_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_2_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_2_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.2, 0.0, 0, "packet_len")
        self.qtgui_time_sink_x_0_2_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_2_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_2_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_2_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_2_0_0.enable_stem_plot(False)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
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
                self.qtgui_time_sink_x_0_2_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_2_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_2_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_2_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_2_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_2_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_2_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_2_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_2_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_2_0_0_win, 8, 0, 1, 2)
        for r in range(8, 9):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0_0_0_1 = qtgui.time_sink_f(
            256, #size
            samp_rate, #samp_rate
            'Correlate Output', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_0_0_1.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0_0_1.set_y_axis(-0.1, 1.1)

        self.qtgui_time_sink_x_0_0_0_0_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0_0_1.enable_tags(True)
        self.qtgui_time_sink_x_0_0_0_0_1.set_trigger_mode(qtgui.TRIG_MODE_TAG, qtgui.TRIG_SLOPE_POS, 0.1, 0.0, 0, "packet_len")
        self.qtgui_time_sink_x_0_0_0_0_1.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0_0_1.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0_0_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0_0_1.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0_0_1.enable_stem_plot(False)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
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
                self.qtgui_time_sink_x_0_0_0_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_0_0_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0_0_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0_0_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0_0_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0_0_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_0_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0_0_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_0_0_1_win, 8, 2, 1, 2)
        for r in range(8, 9):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_1 = qtgui.time_sink_f(
            100, #size
            samp_rate, #samp_rate
            "CRC Out", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_1.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_1.set_y_axis(-500, 500)

        self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_1.enable_tags(False)
        self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_1.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_1.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_1.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_1.enable_stem_plot(False)


        labels = ['Constellation Receiver Decoded', 'Costas Im', 'Signal 3', 'Signal 4', 'Signal 5',
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


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_0_0_0_1_0_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_0_0_0_0_1_0_1_win, 9, 0, 1, 4)
        for r in range(9, 10):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_0 = qtgui.time_sink_f(
            (1024*8), #size
            samp_rate, #samp_rate
            "", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_0.set_y_axis(sps*0.99, sps*1.01)

        self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_0.enable_stem_plot(False)


        labels = ['Sync T_inst', 'Sync T_avg', 'Signal 3', 'Signal 4', 'Signal 5',
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


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_0_0_0_1_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_0_0_0_0_1_0_0_win, 10, 0, 1, 4)
        for r in range(10, 11):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_raster_sink_x_0_1_0_0_0 = qtgui.time_raster_sink_b(
            samp_rate,
            64,
            out_frame_sync_cols,
            [],
            [],
            "Packet Out Frames Bytes",
            1,
            None
        )

        self.qtgui_time_raster_sink_x_0_1_0_0_0.set_update_time(0.10)
        self.qtgui_time_raster_sink_x_0_1_0_0_0.set_intensity_range(0, 255)
        self.qtgui_time_raster_sink_x_0_1_0_0_0.enable_grid(False)
        self.qtgui_time_raster_sink_x_0_1_0_0_0.enable_axis_labels(True)
        self.qtgui_time_raster_sink_x_0_1_0_0_0.set_x_label("")
        self.qtgui_time_raster_sink_x_0_1_0_0_0.set_x_range(0.0, 0.0)
        self.qtgui_time_raster_sink_x_0_1_0_0_0.set_y_label("")
        self.qtgui_time_raster_sink_x_0_1_0_0_0.set_y_range(0.0, 0.0)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_raster_sink_x_0_1_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_raster_sink_x_0_1_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_raster_sink_x_0_1_0_0_0.set_color_map(i, colors[i])
            self.qtgui_time_raster_sink_x_0_1_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_raster_sink_x_0_1_0_0_0_win = sip.wrapinstance(self.qtgui_time_raster_sink_x_0_1_0_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_raster_sink_x_0_1_0_0_0_win, 7, 2, 1, 2)
        for r in range(7, 8):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_raster_sink_x_0_1_0_0 = qtgui.time_raster_sink_b(
            samp_rate,
            64,
            (out_frame_sync_cols*8),
            [],
            [],
            "Packet Out Frames Bits",
            1,
            None
        )

        self.qtgui_time_raster_sink_x_0_1_0_0.set_update_time(0.10)
        self.qtgui_time_raster_sink_x_0_1_0_0.set_intensity_range(0, 1)
        self.qtgui_time_raster_sink_x_0_1_0_0.enable_grid(False)
        self.qtgui_time_raster_sink_x_0_1_0_0.enable_axis_labels(True)
        self.qtgui_time_raster_sink_x_0_1_0_0.set_x_label("")
        self.qtgui_time_raster_sink_x_0_1_0_0.set_x_range(0.0, 0.0)
        self.qtgui_time_raster_sink_x_0_1_0_0.set_y_label("")
        self.qtgui_time_raster_sink_x_0_1_0_0.set_y_range(0.0, 0.0)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_raster_sink_x_0_1_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_raster_sink_x_0_1_0_0.set_line_label(i, labels[i])
            self.qtgui_time_raster_sink_x_0_1_0_0.set_color_map(i, colors[i])
            self.qtgui_time_raster_sink_x_0_1_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_raster_sink_x_0_1_0_0_win = sip.wrapinstance(self.qtgui_time_raster_sink_x_0_1_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_raster_sink_x_0_1_0_0_win, 7, 0, 1, 2)
        for r in range(7, 8):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            (1024*8), #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "RX Spectrum Raw, CFO, and CFO-Corrected", #name
            3,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(0.05)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['Receive Raw', 'Received with Artificial CFO', 'Receive FLL Band-Edge', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["black", "blue", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(3):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 1, 0, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_1_0 = qtgui.const_sink_c(
            4096, #size
            "Symbol Sink and Costas", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_1_0.set_update_time(0.10)
        self.qtgui_const_sink_x_1_0.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_1_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_1_0.enable_autoscale(False)
        self.qtgui_const_sink_x_1_0.enable_grid(False)
        self.qtgui_const_sink_x_1_0.enable_axis_labels(True)


        labels = ['Sync', 'Costas', 'No CFO Correction', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_1_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_1_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_1_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_1_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_1_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_1_0_win = sip.wrapinstance(self.qtgui_const_sink_x_1_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_1_0_win, 5, 0, 2, 2)
        for r in range(5, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.iio_pluto_source_0 = iio.fmcomms2_source_fc32('192.168.2.1' if '192.168.2.1' else iio.get_pluto_uri(), [True, True], 32768)
        self.iio_pluto_source_0.set_len_tag_key('')
        self.iio_pluto_source_0.set_frequency(int(center_freq))
        self.iio_pluto_source_0.set_samplerate(int(samp_rate))
        self.iio_pluto_source_0.set_gain_mode(0, 'slow_attack')
        self.iio_pluto_source_0.set_gain(0, 64)
        self.iio_pluto_source_0.set_quadrature(True)
        self.iio_pluto_source_0.set_rfdc(True)
        self.iio_pluto_source_0.set_bbdc(True)
        self.iio_pluto_source_0.set_filter_params('Auto', '', 0, 0)
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_cc(
            digital.TED_SIGNAL_TIMES_SLOPE_ML,
            sps,
            timing_error_loop_bandwith,
            1.0,
            1.0,
            .1,
            1,
            constellation,
            digital.IR_PFB_MF,
            nfilts,
            rcc_taps)
        self.digital_protocol_parser_b_0 = digital.protocol_parser_b(hdr_format)
        self.digital_fll_band_edge_cc_0 = digital.fll_band_edge_cc(sps, alpha, (sps*2+1), (2*math.pi/sps/100/sps))
        self.digital_diff_decoder_bb_0_0 = digital.diff_decoder_bb(constellation.arity(), digital.DIFF_DIFFERENTIAL)
        self.digital_crc32_bb_0_0_0_0 = digital.crc32_bb(True, "packet_len", True)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc((2*math.pi*costas_loop_bandwidth_in_cycles_per_sample), constellation.arity(), False)
        self.digital_correlate_access_code_xx_ts_0_0_0 = digital.correlate_access_code_bb_ts(access_key,
          thresh, "packet_len")
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(constellation)
        self.blocks_unpacked_to_packed_xx_0_1 = blocks.unpacked_to_packed_bb(constellation.bits_per_symbol(), gr.GR_MSB_FIRST)
        self.blocks_uchar_to_float_0_0_1_0 = blocks.uchar_to_float()
        self.blocks_uchar_to_float_0_0_0_0_0 = blocks.uchar_to_float()
        self.blocks_skiphead_0_0 = blocks.skiphead(gr.sizeof_gr_complex*1, int(samp_rate))
        self.blocks_repack_bits_bb_1_0_1 = blocks.repack_bits_bb(8, 1, "", False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_1_0_0_0_0 = blocks.repack_bits_bb(1, 8, "packet_len", False, gr.GR_MSB_FIRST)
        self.blocks_null_sink_3 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_1 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_0_1 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_1_1 = blocks.multiply_const_cc(math.e**(2j*math.pi*0))
        self.blocks_message_debug_0 = blocks.message_debug(True, gr.log_levels.info)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, cfo_offset, 1, 0, 0)
        self.analog_agc_xx_0 = analog.agc_cc(agc_rate, 1.0, 1.0, 65536)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.digital_protocol_parser_b_0, 'info'), (self.blocks_message_debug_0, 'print'))
        self.connect((self.analog_agc_xx_0, 0), (self.digital_fll_band_edge_cc_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_char_to_float_0, 0), (self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_1, 0))
        self.connect((self.blocks_multiply_const_vxx_1_1, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.qtgui_freq_sink_x_0, 1))
        self.connect((self.blocks_repack_bits_bb_1_0_0_0_0, 0), (self.digital_crc32_bb_0_0_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_1_0_1, 0), (self.blocks_uchar_to_float_0_0_1_0, 0))
        self.connect((self.blocks_repack_bits_bb_1_0_1, 0), (self.digital_correlate_access_code_xx_ts_0_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_1_0_1, 0), (self.qtgui_time_raster_sink_x_0_1_0_0, 0))
        self.connect((self.blocks_skiphead_0_0, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.blocks_uchar_to_float_0_0_0_0_0, 0), (self.qtgui_time_sink_x_0_0_0_0_1, 0))
        self.connect((self.blocks_uchar_to_float_0_0_1_0, 0), (self.qtgui_time_sink_x_0_2_0_0, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0_1, 0), (self.blocks_repack_bits_bb_1_0_1, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0_1, 0), (self.qtgui_time_raster_sink_x_0_1_0_0_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_diff_decoder_bb_0_0, 0))
        self.connect((self.digital_correlate_access_code_xx_ts_0_0_0, 0), (self.blocks_repack_bits_bb_1_0_0_0_0, 0))
        self.connect((self.digital_correlate_access_code_xx_ts_0_0_0, 0), (self.blocks_uchar_to_float_0_0_0_0_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.blocks_multiply_const_vxx_1_1, 0))
        self.connect((self.digital_costas_loop_cc_0, 3), (self.blocks_null_sink_1, 0))
        self.connect((self.digital_costas_loop_cc_0, 1), (self.blocks_null_sink_2, 0))
        self.connect((self.digital_costas_loop_cc_0, 2), (self.blocks_null_sink_3, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.qtgui_const_sink_x_1_0, 1))
        self.connect((self.digital_crc32_bb_0_0_0_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.digital_crc32_bb_0_0_0_0, 0), (self.digital_protocol_parser_b_0, 0))
        self.connect((self.digital_diff_decoder_bb_0_0, 0), (self.blocks_unpacked_to_packed_xx_0_1, 0))
        self.connect((self.digital_fll_band_edge_cc_0, 0), (self.blocks_skiphead_0_0, 0))
        self.connect((self.digital_fll_band_edge_cc_0, 0), (self.qtgui_freq_sink_x_0, 2))
        self.connect((self.digital_symbol_sync_xx_0, 1), (self.blocks_null_sink_0_1, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.digital_costas_loop_cc_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.qtgui_const_sink_x_1_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 2), (self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 3), (self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_0, 1))
        self.connect((self.iio_pluto_source_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "comms_project_rx")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_constellation(self):
        return self.constellation

    def set_constellation(self, constellation):
        self.constellation = constellation
        self.digital_constellation_decoder_cb_0.set_constellation(self.constellation)

    def get_ts_packet_size(self):
        return self.ts_packet_size

    def set_ts_packet_size(self, ts_packet_size):
        self.ts_packet_size = ts_packet_size
        self.set_packet_length(self.packet_groups*self.ts_packet_size)

    def get_thresh(self):
        return self.thresh

    def set_thresh(self, thresh):
        self.thresh = thresh
        self.set_hdr_format(digital.header_format_default(self.access_key, self.thresh, self.bps))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_rcc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts*self.samp_rate, self.samp_rate/self.sps, self.alpha, (11*self.sps*self.nfilts)))
        self.digital_fll_band_edge_cc_0.set_loop_bandwidth((2*math.pi/self.sps/100/self.sps))
        self.digital_symbol_sync_xx_0.set_sps(self.sps)
        self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_0.set_y_axis(self.sps*0.99, self.sps*1.01)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_rcc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts*self.samp_rate, self.samp_rate/self.sps, self.alpha, (11*self.sps*self.nfilts)))
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.iio_pluto_source_0.set_samplerate(int(self.samp_rate))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0_0_0_0_0_1_0_1.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0_0_0_1.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_2_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate)

    def get_packet_groups(self):
        return self.packet_groups

    def set_packet_groups(self, packet_groups):
        self.packet_groups = packet_groups
        self.set_packet_length(self.packet_groups*self.ts_packet_size)

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rcc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts*self.samp_rate, self.samp_rate/self.sps, self.alpha, (11*self.sps*self.nfilts)))

    def get_bps(self):
        return self.bps

    def set_bps(self, bps):
        self.bps = bps
        self.set_hdr_format(digital.header_format_default(self.access_key, self.thresh, self.bps))

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.set_rcc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts*self.samp_rate, self.samp_rate/self.sps, self.alpha, (11*self.sps*self.nfilts)))

    def get_access_key(self):
        return self.access_key

    def set_access_key(self, access_key):
        self.access_key = access_key
        self.set_hdr_format(digital.header_format_default(self.access_key, self.thresh, self.bps))

    def get_timing_error_loop_bandwith(self):
        return self.timing_error_loop_bandwith

    def set_timing_error_loop_bandwith(self, timing_error_loop_bandwith):
        self.timing_error_loop_bandwith = timing_error_loop_bandwith
        self.digital_symbol_sync_xx_0.set_loop_bandwidth(self.timing_error_loop_bandwith)

    def get_rcc_taps(self):
        return self.rcc_taps

    def set_rcc_taps(self, rcc_taps):
        self.rcc_taps = rcc_taps

    def get_packet_length(self):
        return self.packet_length

    def set_packet_length(self, packet_length):
        self.packet_length = packet_length

    def get_out_frame_sync_cols(self):
        return self.out_frame_sync_cols

    def set_out_frame_sync_cols(self, out_frame_sync_cols):
        self.out_frame_sync_cols = out_frame_sync_cols
        self.qtgui_time_raster_sink_x_0_1_0_0.set_num_cols((self.out_frame_sync_cols*8))
        self.qtgui_time_raster_sink_x_0_1_0_0_0.set_num_cols(self.out_frame_sync_cols)

    def get_hdr_format(self):
        return self.hdr_format

    def set_hdr_format(self, hdr_format):
        self.hdr_format = hdr_format

    def get_costas_loop_bandwidth_in_cycles_per_sample(self):
        return self.costas_loop_bandwidth_in_cycles_per_sample

    def set_costas_loop_bandwidth_in_cycles_per_sample(self, costas_loop_bandwidth_in_cycles_per_sample):
        self.costas_loop_bandwidth_in_cycles_per_sample = costas_loop_bandwidth_in_cycles_per_sample
        self.digital_costas_loop_cc_0.set_loop_bandwidth((2*math.pi*self.costas_loop_bandwidth_in_cycles_per_sample))

    def get_cfo_offset(self):
        return self.cfo_offset

    def set_cfo_offset(self, cfo_offset):
        self.cfo_offset = cfo_offset
        self.analog_sig_source_x_0.set_frequency(self.cfo_offset)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.iio_pluto_source_0.set_frequency(int(self.center_freq))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate)

    def get_agc_rate(self):
        return self.agc_rate

    def set_agc_rate(self, agc_rate):
        self.agc_rate = agc_rate
        self.analog_agc_xx_0.set_rate(self.agc_rate)




def main(top_block_cls=comms_project_rx, options=None):

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
