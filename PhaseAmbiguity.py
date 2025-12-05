#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: PhaseAmbiguity
# Author: jason
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import iio
import math
import sip
import threading



class PhaseAmbiguity(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "PhaseAmbiguity", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("PhaseAmbiguity")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "PhaseAmbiguity")

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
        self.sps = sps = 16
        self.samp_rate = samp_rate = 1e6
        self.nfilts = nfilts = 32
        self.alpha = alpha = 0.50
        self.tx_attenuation = tx_attenuation = 10
        self.rx_gain = rx_gain = 10
        self.rcc_taps = rcc_taps = firdes.root_raised_cosine(nfilts, nfilts*samp_rate,samp_rate/sps, alpha, (11*sps*nfilts))
        self.output_sps = output_sps = 1
        self.offset = offset = 0
        self.costas_loop_bandwidth_in_cycles_per_sample = costas_loop_bandwidth_in_cycles_per_sample = .01
        self.constellation = constellation = digital.constellation_calcdist([-1-1j, -1+1j, 1+1j, 1-1j], [0,1,2,3],
        4, 1, digital.constellation.AMPLITUDE_NORMALIZATION).base()
        self.constellation.set_npwr(1.0)
        self.center_freq = center_freq = 915e6

        ##################################################
        # Blocks
        ##################################################

        self._tx_attenuation_range = qtgui.Range(0, 89, 1, 10, 200)
        self._tx_attenuation_win = qtgui.RangeWidget(self._tx_attenuation_range, self.set_tx_attenuation, "'tx_attenuation'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._tx_attenuation_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._offset_range = qtgui.Range(-500e3, 500e3, 1, 0, 200)
        self._offset_win = qtgui.RangeWidget(self._offset_range, self.set_offset, "'offset'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._offset_win, 6, 0, 1, 1)
        for r in range(6, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._costas_loop_bandwidth_in_cycles_per_sample_range = qtgui.Range(0.0001, 0.2, 0.0001, .01, 200)
        self._costas_loop_bandwidth_in_cycles_per_sample_win = qtgui.RangeWidget(self._costas_loop_bandwidth_in_cycles_per_sample_range, self.set_costas_loop_bandwidth_in_cycles_per_sample, "'costas_loop_bandwidth_in_cycles_per_sample'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._costas_loop_bandwidth_in_cycles_per_sample_win, 21, 0, 1, 1)
        for r in range(21, 22):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._rx_gain_range = qtgui.Range(0, 70, 1, 10, 200)
        self._rx_gain_win = qtgui.RangeWidget(self._rx_gain_range, self.set_rx_gain, "'rx_gain'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._rx_gain_win, 4, 0, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.root_raised_cosine_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.root_raised_cosine(
                1,
                samp_rate,
                (samp_rate/sps),
                alpha,
                (11*sps)))
        self.qtgui_time_sink_x_2_1_0 = qtgui.time_sink_f(
            25, #size
            samp_rate/sps*output_sps, #samp_rate
            "", #name
            3, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_2_1_0.set_update_time(0.10)
        self.qtgui_time_sink_x_2_1_0.set_y_axis(-0.5, 3.5)

        self.qtgui_time_sink_x_2_1_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_2_1_0.enable_tags(True)
        self.qtgui_time_sink_x_2_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2_1_0.enable_autoscale(False)
        self.qtgui_time_sink_x_2_1_0.enable_grid(False)
        self.qtgui_time_sink_x_2_1_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_2_1_0.enable_control_panel(False)
        self.qtgui_time_sink_x_2_1_0.enable_stem_plot(False)


        labels = ['input bits', 'differential endoder', 'differential decoded', 'differential with 3/4 cycle (270 deg) phase rotation', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [0, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(3):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_2_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_2_1_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2_1_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2_1_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2_1_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2_1_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_2_1_0_win = sip.wrapinstance(self.qtgui_time_sink_x_2_1_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_2_1_0_win, 26, 0, 1, 1)
        for r in range(26, 27):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_2_1 = qtgui.time_sink_f(
            25, #size
            samp_rate/sps*output_sps, #samp_rate
            "", #name
            4, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_2_1.set_update_time(0.10)
        self.qtgui_time_sink_x_2_1.set_y_axis(-0.5, 3.5)

        self.qtgui_time_sink_x_2_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_2_1.enable_tags(True)
        self.qtgui_time_sink_x_2_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2_1.enable_autoscale(False)
        self.qtgui_time_sink_x_2_1.enable_grid(False)
        self.qtgui_time_sink_x_2_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_2_1.enable_control_panel(False)
        self.qtgui_time_sink_x_2_1.enable_stem_plot(False)


        labels = ['differential with 0 phase rotation', 'differential with 1/4 cycle (90 deg) phase rotation', 'differential with 1/2 cycle (180 deg) phase rotation', 'differential with 3/4 cycle (270 deg) phase rotation', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [0, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(4):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_2_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_2_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_2_1_win = sip.wrapinstance(self.qtgui_time_sink_x_2_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_2_1_win, 27, 0, 1, 1)
        for r in range(27, 28):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_2_0_0_0 = qtgui.time_sink_f(
            50, #size
            samp_rate/sps*output_sps, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_2_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_2_0_0_0.set_y_axis(-0.5, 3.5)

        self.qtgui_time_sink_x_2_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_2_0_0_0.enable_tags(True)
        self.qtgui_time_sink_x_2_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2_0_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_2_0_0_0.enable_grid(False)
        self.qtgui_time_sink_x_2_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_2_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_2_0_0_0.enable_stem_plot(False)


        labels = ['3/4 cycle (270 deg) phase rotation', '1/4 cycle (90 deg) phase rotation', '1/2 cycle (180 deg) phase rotation', '3/4 cycle (270 deg) phase rotation', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['black', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [0, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_2_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_2_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_2_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_2_0_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_2_0_0_0_win, 25, 0, 1, 1)
        for r in range(25, 26):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_2_0_0 = qtgui.time_sink_f(
            50, #size
            samp_rate/sps*output_sps, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_2_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_2_0_0.set_y_axis(-0.5, 3.5)

        self.qtgui_time_sink_x_2_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_2_0_0.enable_tags(True)
        self.qtgui_time_sink_x_2_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_2_0_0.enable_grid(False)
        self.qtgui_time_sink_x_2_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_2_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_2_0_0.enable_stem_plot(False)


        labels = ['1/2 cycle (180 deg) phase rotation', '1/4 cycle (90 deg) phase rotation', '1/2 cycle (180 deg) phase rotation', '3/4 cycle (270 deg) phase rotation', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['green', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [0, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_2_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_2_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_2_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_2_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_2_0_0_win, 24, 0, 1, 1)
        for r in range(24, 25):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_2_0 = qtgui.time_sink_f(
            50, #size
            samp_rate/sps*output_sps, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_2_0.set_update_time(0.10)
        self.qtgui_time_sink_x_2_0.set_y_axis(-0.5, 3.5)

        self.qtgui_time_sink_x_2_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_2_0.enable_tags(True)
        self.qtgui_time_sink_x_2_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2_0.enable_autoscale(False)
        self.qtgui_time_sink_x_2_0.enable_grid(False)
        self.qtgui_time_sink_x_2_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_2_0.enable_control_panel(False)
        self.qtgui_time_sink_x_2_0.enable_stem_plot(False)


        labels = ['1/4 cycle (90 deg) phase rotation', '1/4 cycle (90 deg) phase rotation', '1/2 cycle (180 deg) phase rotation', '3/4 cycle (270 deg) phase rotation', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['red', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [0, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_2_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_2_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_2_0_win = sip.wrapinstance(self.qtgui_time_sink_x_2_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_2_0_win, 23, 0, 1, 1)
        for r in range(23, 24):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_2 = qtgui.time_sink_f(
            50, #size
            samp_rate/sps*output_sps, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_2.set_update_time(0.10)
        self.qtgui_time_sink_x_2.set_y_axis(-0.5, 3.5)

        self.qtgui_time_sink_x_2.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_2.enable_tags(True)
        self.qtgui_time_sink_x_2.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2.enable_autoscale(False)
        self.qtgui_time_sink_x_2.enable_grid(False)
        self.qtgui_time_sink_x_2.enable_axis_labels(True)
        self.qtgui_time_sink_x_2.enable_control_panel(False)
        self.qtgui_time_sink_x_2.enable_stem_plot(False)


        labels = ['0 phase rotation', '1/4 cycle (90 deg) phase rotation', '1/2 cycle (180 deg) phase rotation', '3/4 cycle (270 deg) phase rotation', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [0, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_2.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_2.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_2_win = sip.wrapinstance(self.qtgui_time_sink_x_2.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_2_win, 22, 0, 1, 1)
        for r in range(22, 23):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_1_1_0 = qtgui.time_sink_f(
            10000, #size
            samp_rate/sps*output_sps, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1_1_0.set_update_time(0.10)
        self.qtgui_time_sink_x_1_1_0.set_y_axis(-7, 7)

        self.qtgui_time_sink_x_1_1_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1_1_0.enable_tags(True)
        self.qtgui_time_sink_x_1_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1_1_0.enable_autoscale(False)
        self.qtgui_time_sink_x_1_1_0.enable_grid(False)
        self.qtgui_time_sink_x_1_1_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_1_1_0.enable_control_panel(False)
        self.qtgui_time_sink_x_1_1_0.enable_stem_plot(False)


        labels = ['Costas phase', 'Sync T_inst', 'Sync T_avg', 'Signal 4', 'Signal 5',
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
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_1_1_0_win, 20, 0, 1, 1)
        for r in range(20, 21):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_1_1 = qtgui.time_sink_f(
            10000, #size
            samp_rate/sps*output_sps, #samp_rate
            "", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1_1.set_y_axis(-0.1, 0.1)

        self.qtgui_time_sink_x_1_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1_1.enable_tags(True)
        self.qtgui_time_sink_x_1_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1_1.enable_grid(False)
        self.qtgui_time_sink_x_1_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1_1.enable_control_panel(False)
        self.qtgui_time_sink_x_1_1.enable_stem_plot(False)


        labels = ['Costas error', 'Costas frequency [rad/samp]', 'Sync T_avg', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 2, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [0.5, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
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
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_1_1_win, 19, 0, 1, 1)
        for r in range(19, 20):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_1_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1_0.set_update_time(0.10)
        self.qtgui_time_sink_x_1_0.set_y_axis(sps*0.99, sps*1.01)

        self.qtgui_time_sink_x_1_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1_0.enable_tags(True)
        self.qtgui_time_sink_x_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1_0.enable_autoscale(False)
        self.qtgui_time_sink_x_1_0.enable_grid(False)
        self.qtgui_time_sink_x_1_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_1_0.enable_control_panel(False)
        self.qtgui_time_sink_x_1_0.enable_stem_plot(False)


        labels = ['Sync T_inst', 'Sync T_avg', 'Sync T_avg', 'Signal 4', 'Signal 5',
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
                self.qtgui_time_sink_x_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_0_win = sip.wrapinstance(self.qtgui_time_sink_x_1_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_1_0_win, 15, 0, 1, 1)
        for r in range(15, 16):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(True)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        self.qtgui_time_sink_x_1.enable_stem_plot(False)


        labels = ['Sync error', 'Sync T_inst', 'Sync T_avg', 'Signal 4', 'Signal 5',
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
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_1_win, 14, 0, 1, 1)
        for r in range(14, 15):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0_0_0_0_0 = qtgui.time_sink_c(
            100, #size
            samp_rate/sps*output_sps, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_0_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0_0_0_0.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0_0_0_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0_0_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0_0_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0_0_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0_0_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0_0_0_0.enable_stem_plot(False)


        labels = ['Receive after Costas Re', 'Receive after Costas Im', 'Signal 3', 'Signal 4', 'Signal 5',
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
                    self.qtgui_time_sink_x_0_0_0_0_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0_0_0_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0_0_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_0_0_0_0_win, 18, 0, 1, 1)
        for r in range(18, 19):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0_0_0_0 = qtgui.time_sink_c(
            (10*sps), #size
            samp_rate/sps*output_sps, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0_0_0.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0_0_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0_0_0.enable_stem_plot(False)


        labels = ['Receive Symbol Sync Re', 'Receive Symbol Sync Im', 'Signal 3', 'Signal 4', 'Signal 5',
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
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0_0_0_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0_0_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_0_0_0_win, 11, 0, 1, 1)
        for r in range(11, 12):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0_0_0 = qtgui.time_sink_c(
            (1024*8), #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0_0.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0_0.enable_stem_plot(False)


        labels = ['Receive Tuned AGC and FLL Re', 'Receive Tuned AGC and FLL Im', 'Signal 3', 'Signal 4', 'Signal 5',
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
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0_0_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_0_0_win, 9, 0, 1, 1)
        for r in range(9, 10):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0_0 = qtgui.time_sink_c(
            (1024*8), #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0.enable_stem_plot(False)


        labels = ['Receive Tuned and AGC Re', 'Receive Tuned and AGC Im', 'Signal 3', 'Signal 4', 'Signal 5',
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
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_0_win, 7, 0, 1, 1)
        for r in range(7, 8):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_c(
            (1024*8), #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


        labels = ['Receive Raw Re', 'Receive Raw Im', 'Signal 3', 'Signal 4', 'Signal 5',
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
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_win, 5, 0, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


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
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_raster_sink_x_1_0 = qtgui.time_raster_sink_b(
            samp_rate,
            64,
            (512*constellation.bits_per_symbol()),
            [],
            [],
            "",
            1,
            None
        )

        self.qtgui_time_raster_sink_x_1_0.set_update_time(0.10)
        self.qtgui_time_raster_sink_x_1_0.set_intensity_range(0, 1)
        self.qtgui_time_raster_sink_x_1_0.enable_grid(False)
        self.qtgui_time_raster_sink_x_1_0.enable_axis_labels(True)
        self.qtgui_time_raster_sink_x_1_0.set_x_label("")
        self.qtgui_time_raster_sink_x_1_0.set_x_range(0.0, 0.0)
        self.qtgui_time_raster_sink_x_1_0.set_y_label("")
        self.qtgui_time_raster_sink_x_1_0.set_y_range(0.0, 0.0)

        labels = ['Input Symbols', '', '', '', '',
            '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_raster_sink_x_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_raster_sink_x_1_0.set_line_label(i, labels[i])
            self.qtgui_time_raster_sink_x_1_0.set_color_map(i, colors[i])
            self.qtgui_time_raster_sink_x_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_raster_sink_x_1_0_win = sip.wrapinstance(self.qtgui_time_raster_sink_x_1_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_raster_sink_x_1_0_win, 29, 0, 1, 1)
        for r in range(29, 30):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_raster_sink_x_1 = qtgui.time_raster_sink_b(
            samp_rate,
            64,
            (512*constellation.bits_per_symbol()),
            [],
            [],
            "",
            1,
            None
        )

        self.qtgui_time_raster_sink_x_1.set_update_time(0.10)
        self.qtgui_time_raster_sink_x_1.set_intensity_range(0, 1)
        self.qtgui_time_raster_sink_x_1.enable_grid(False)
        self.qtgui_time_raster_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_raster_sink_x_1.set_x_label("")
        self.qtgui_time_raster_sink_x_1.set_x_range(0.0, 0.0)
        self.qtgui_time_raster_sink_x_1.set_y_label("")
        self.qtgui_time_raster_sink_x_1.set_y_range(0.0, 0.0)

        labels = ['Input Symbols', '', '', '', '',
            '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_raster_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_raster_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_raster_sink_x_1.set_color_map(i, colors[i])
            self.qtgui_time_raster_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_raster_sink_x_1_win = sip.wrapinstance(self.qtgui_time_raster_sink_x_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_raster_sink_x_1_win, 28, 0, 1, 1)
        for r in range(28, 29):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_1 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_1.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1.enable_grid(False)
        self.qtgui_freq_sink_x_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_1.set_fft_window_normalized(False)



        labels = ['Transmit', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_1_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            (1024*8), #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            3,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(0.2)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['Receive Raw', 'Receive Tuned and AGC', 'Receive FLL Band-Edge', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
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
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 8, 0, 1, 1)
        for r in range(8, 9):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_eye_sink_x_0_0_0 = qtgui.eye_sink_c(
            1024, #size
            samp_rate/sps*output_sps, #samp_rate
            1, #number of inputs
            None
        )
        self.qtgui_eye_sink_x_0_0_0.set_update_time(0.10)
        self.qtgui_eye_sink_x_0_0_0.set_samp_per_symbol(sps)
        self.qtgui_eye_sink_x_0_0_0.set_y_axis(-2, 2)

        self.qtgui_eye_sink_x_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_eye_sink_x_0_0_0.enable_tags(True)
        self.qtgui_eye_sink_x_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_eye_sink_x_0_0_0.enable_autoscale(False)
        self.qtgui_eye_sink_x_0_0_0.enable_grid(False)
        self.qtgui_eye_sink_x_0_0_0.enable_axis_labels(True)
        self.qtgui_eye_sink_x_0_0_0.enable_control_panel(False)


        labels = ['Eye Diagram after Costas Re', 'Eye Diagram after Costas  Im', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'blue', 'blue', 'blue', 'blue',
            'blue', 'blue', 'blue', 'blue', 'blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [0, 0, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_eye_sink_x_0_0_0.set_line_label(i, "Eye [Re{{Data {0}}}]".format(round(i/2)))
                else:
                    self.qtgui_eye_sink_x_0_0_0.set_line_label(i, "Eye [Im{{Data {0}}}]".format(round((i-1)/2)))
            else:
                self.qtgui_eye_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_eye_sink_x_0_0_0.set_line_width(i, widths[i])
            self.qtgui_eye_sink_x_0_0_0.set_line_color(i, colors[i])
            self.qtgui_eye_sink_x_0_0_0.set_line_style(i, styles[i])
            self.qtgui_eye_sink_x_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_eye_sink_x_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_eye_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_eye_sink_x_0_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_eye_sink_x_0_0_0_win, 16, 0, 1, 1)
        for r in range(16, 17):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_eye_sink_x_0_0 = qtgui.eye_sink_c(
            1024, #size
            samp_rate/sps*output_sps, #samp_rate
            1, #number of inputs
            None
        )
        self.qtgui_eye_sink_x_0_0.set_update_time(0.10)
        self.qtgui_eye_sink_x_0_0.set_samp_per_symbol(sps)
        self.qtgui_eye_sink_x_0_0.set_y_axis(-2, 2)

        self.qtgui_eye_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_eye_sink_x_0_0.enable_tags(True)
        self.qtgui_eye_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_eye_sink_x_0_0.enable_autoscale(False)
        self.qtgui_eye_sink_x_0_0.enable_grid(False)
        self.qtgui_eye_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_eye_sink_x_0_0.enable_control_panel(False)


        labels = ['Eye Diagram for Receive Symbol Sync Re', 'Eye Diagram for Receive Symbol Sync  Im', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'blue', 'blue', 'blue', 'blue',
            'blue', 'blue', 'blue', 'blue', 'blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [0, 0, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_eye_sink_x_0_0.set_line_label(i, "Eye [Re{{Data {0}}}]".format(round(i/2)))
                else:
                    self.qtgui_eye_sink_x_0_0.set_line_label(i, "Eye [Im{{Data {0}}}]".format(round((i-1)/2)))
            else:
                self.qtgui_eye_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_eye_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_eye_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_eye_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_eye_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_eye_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_eye_sink_x_0_0_win = sip.wrapinstance(self.qtgui_eye_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_eye_sink_x_0_0_win, 12, 0, 1, 1)
        for r in range(12, 13):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_eye_sink_x_0 = qtgui.eye_sink_c(
            1024, #size
            samp_rate, #samp_rate
            1, #number of inputs
            None
        )
        self.qtgui_eye_sink_x_0.set_update_time(0.10)
        self.qtgui_eye_sink_x_0.set_samp_per_symbol(sps)
        self.qtgui_eye_sink_x_0.set_y_axis(-2, 2)

        self.qtgui_eye_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_eye_sink_x_0.enable_tags(True)
        self.qtgui_eye_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_eye_sink_x_0.enable_autoscale(False)
        self.qtgui_eye_sink_x_0.enable_grid(False)
        self.qtgui_eye_sink_x_0.enable_axis_labels(True)
        self.qtgui_eye_sink_x_0.enable_control_panel(False)


        labels = ['Eye Diagram for Receive AGC and FLL Re', 'Eye Diagram for Receive AGC and FLL  Im', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'blue', 'blue', 'blue', 'blue',
            'blue', 'blue', 'blue', 'blue', 'blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [0, 0, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_eye_sink_x_0.set_line_label(i, "Eye [Re{{Data {0}}}]".format(round(i/2)))
                else:
                    self.qtgui_eye_sink_x_0.set_line_label(i, "Eye [Im{{Data {0}}}]".format(round((i-1)/2)))
            else:
                self.qtgui_eye_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_eye_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_eye_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_eye_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_eye_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_eye_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_eye_sink_x_0_win = sip.wrapinstance(self.qtgui_eye_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_eye_sink_x_0_win, 10, 0, 1, 1)
        for r in range(10, 11):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0_0 = qtgui.const_sink_c(
            1024, #size
            "", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0_0.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_0_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0_0.enable_grid(False)
        self.qtgui_const_sink_x_0_0.enable_axis_labels(True)


        labels = ['after Symbol Sync', 'after Costas', '', '', '',
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
                self.qtgui_const_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_0_win, 17, 0, 1, 1)
        for r in range(17, 18):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(False)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['Symbol Sync', '', '', '', '',
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

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_win, 13, 0, 1, 1)
        for r in range(13, 14):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.iio_pluto_source_0 = iio.fmcomms2_source_fc32('192.168.2.1' if '192.168.2.1' else iio.get_pluto_uri(), [True, True], 32768)
        self.iio_pluto_source_0.set_len_tag_key('packet_len')
        self.iio_pluto_source_0.set_frequency(int(center_freq))
        self.iio_pluto_source_0.set_samplerate(int(samp_rate))
        self.iio_pluto_source_0.set_gain_mode(0, 'slow_attack')
        self.iio_pluto_source_0.set_gain(0, 64)
        self.iio_pluto_source_0.set_quadrature(True)
        self.iio_pluto_source_0.set_rfdc(True)
        self.iio_pluto_source_0.set_bbdc(True)
        self.iio_pluto_source_0.set_filter_params('Auto', '', 0, 0)
        self.iio_pluto_sink_0_0 = iio.fmcomms2_sink_fc32('192.168.2.1' if '192.168.2.1' else iio.get_pluto_uri(), [True, True], 32768, False)
        self.iio_pluto_sink_0_0.set_len_tag_key('')
        self.iio_pluto_sink_0_0.set_bandwidth(int(samp_rate))
        self.iio_pluto_sink_0_0.set_frequency(int(center_freq))
        self.iio_pluto_sink_0_0.set_samplerate(int(samp_rate))
        self.iio_pluto_sink_0_0.set_attenuation(0, tx_attenuation)
        self.iio_pluto_sink_0_0.set_filter_params('Auto', '', 0, 0)
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_cc(
            digital.TED_SIGNAL_TIMES_SLOPE_ML,
            sps,
            0.045,
            1.0,
            1.0,
            0.1,
            output_sps,
            digital.constellation_bpsk().base(),
            digital.IR_PFB_MF,
            nfilts,
            rcc_taps)
        self.digital_fll_band_edge_cc_0 = digital.fll_band_edge_cc(sps, alpha, (sps*2+1), (2*math.pi/sps/100))
        self.digital_diff_encoder_bb_0_0_0_0_0 = digital.diff_encoder_bb(constellation.arity(), digital.DIFF_DIFFERENTIAL)
        self.digital_diff_decoder_bb_1 = digital.diff_decoder_bb(constellation.arity(), digital.DIFF_DIFFERENTIAL)
        self.digital_diff_decoder_bb_0_0_0_0 = digital.diff_decoder_bb(constellation.arity(), digital.DIFF_DIFFERENTIAL)
        self.digital_diff_decoder_bb_0_0_0 = digital.diff_decoder_bb(constellation.arity(), digital.DIFF_DIFFERENTIAL)
        self.digital_diff_decoder_bb_0_0 = digital.diff_decoder_bb(constellation.arity(), digital.DIFF_DIFFERENTIAL)
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(constellation.arity(), digital.DIFF_DIFFERENTIAL)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc((2*math.pi*costas_loop_bandwidth_in_cycles_per_sample), constellation.arity(), False)
        self.digital_constellation_modulator_0 = digital.generic_mod(
            constellation=constellation,
            differential=True,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=alpha,
            verbose=False,
            log=False,
            truncate=False)
        self.digital_constellation_decoder_cb_0_0_0_0 = digital.constellation_decoder_cb(constellation)
        self.digital_constellation_decoder_cb_0_0_0 = digital.constellation_decoder_cb(constellation)
        self.digital_constellation_decoder_cb_0_0 = digital.constellation_decoder_cb(constellation)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(constellation)
        self.blocks_vector_source_x_0 = blocks.vector_source_b([0,1,2,3,0,3,0,3], True, 1, [])
        self.blocks_unpacked_to_packed_xx_0_0 = blocks.unpacked_to_packed_bb(constellation.bits_per_symbol(), gr.GR_MSB_FIRST)
        self.blocks_unpack_k_bits_bb_0_0 = blocks.unpack_k_bits_bb(constellation.bits_per_symbol())
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(constellation.bits_per_symbol())
        self.blocks_skiphead_0 = blocks.skiphead(gr.sizeof_gr_complex*1, int(samp_rate))
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_1_1 = blocks.multiply_const_cc(math.e**(2j*math.pi*0))
        self.blocks_multiply_const_vxx_1_0_0 = blocks.multiply_const_cc(-1)
        self.blocks_multiply_const_vxx_1_0 = blocks.multiply_const_cc(-1j)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_cc(1j)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(0.4)
        self.blocks_char_to_float_0_1_0 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0_1 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0_0_1_0_0 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0_0_1_0 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0_0_1 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0_0_0_1 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0_0_0_0_0 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0_0_0_0 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0_0_0 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0_0 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, offset, 1, 0, 0)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, constellation.arity(), 512))), True)
        self.analog_agc_xx_1 = analog.agc_cc((1e-4), 1.0, 1.0, 65536)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc_xx_1, 0), (self.digital_fll_band_edge_cc_0, 0))
        self.connect((self.analog_agc_xx_1, 0), (self.qtgui_freq_sink_x_0, 1))
        self.connect((self.analog_agc_xx_1, 0), (self.qtgui_time_sink_x_0_0_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_unpacked_to_packed_xx_0_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_char_to_float_0, 0), (self.qtgui_time_sink_x_2, 0))
        self.connect((self.blocks_char_to_float_0_0, 0), (self.qtgui_time_sink_x_2_0, 0))
        self.connect((self.blocks_char_to_float_0_0_0, 0), (self.qtgui_time_sink_x_2_0_0, 0))
        self.connect((self.blocks_char_to_float_0_0_0_0, 0), (self.qtgui_time_sink_x_2_0_0_0, 0))
        self.connect((self.blocks_char_to_float_0_0_0_0_0, 0), (self.qtgui_time_sink_x_2_1, 3))
        self.connect((self.blocks_char_to_float_0_0_0_1, 0), (self.qtgui_time_sink_x_2_1, 2))
        self.connect((self.blocks_char_to_float_0_0_1, 0), (self.qtgui_time_sink_x_2_1, 1))
        self.connect((self.blocks_char_to_float_0_0_1_0, 0), (self.qtgui_time_sink_x_2_1_0, 1))
        self.connect((self.blocks_char_to_float_0_0_1_0_0, 0), (self.qtgui_time_sink_x_2_1_0, 2))
        self.connect((self.blocks_char_to_float_0_1, 0), (self.qtgui_time_sink_x_2_1, 0))
        self.connect((self.blocks_char_to_float_0_1_0, 0), (self.qtgui_time_sink_x_2_1_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.iio_pluto_sink_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_freq_sink_x_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.digital_constellation_decoder_cb_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0, 0), (self.digital_constellation_decoder_cb_0_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0_0, 0), (self.digital_constellation_decoder_cb_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1_1, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.analog_agc_xx_1, 0))
        self.connect((self.blocks_skiphead_0, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.qtgui_time_raster_sink_x_1, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0_0, 0), (self.qtgui_time_raster_sink_x_1_0, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_char_to_float_0_1_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.digital_diff_encoder_bb_0_0_0_0_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0, 0), (self.blocks_char_to_float_0_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0, 0), (self.digital_diff_decoder_bb_0_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0_0, 0), (self.blocks_char_to_float_0_0_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0_0, 0), (self.digital_diff_decoder_bb_0_0_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0_0_0, 0), (self.blocks_char_to_float_0_0_0_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0_0_0, 0), (self.digital_diff_decoder_bb_0_0_0_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.blocks_multiply_const_vxx_1_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.blocks_multiply_const_vxx_1_0_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.blocks_multiply_const_vxx_1_1, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.qtgui_const_sink_x_0_0, 1))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.qtgui_eye_sink_x_0_0_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.qtgui_time_sink_x_0_0_0_0_0_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 1), (self.qtgui_time_sink_x_1_1, 1))
        self.connect((self.digital_costas_loop_cc_0, 3), (self.qtgui_time_sink_x_1_1, 0))
        self.connect((self.digital_costas_loop_cc_0, 2), (self.qtgui_time_sink_x_1_1_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.blocks_char_to_float_0_1, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.blocks_unpack_k_bits_bb_0_0, 0))
        self.connect((self.digital_diff_decoder_bb_0_0, 0), (self.blocks_char_to_float_0_0_1, 0))
        self.connect((self.digital_diff_decoder_bb_0_0_0, 0), (self.blocks_char_to_float_0_0_0_1, 0))
        self.connect((self.digital_diff_decoder_bb_0_0_0_0, 0), (self.blocks_char_to_float_0_0_0_0_0, 0))
        self.connect((self.digital_diff_decoder_bb_1, 0), (self.blocks_char_to_float_0_0_1_0_0, 0))
        self.connect((self.digital_diff_encoder_bb_0_0_0_0_0, 0), (self.blocks_char_to_float_0_0_1_0, 0))
        self.connect((self.digital_diff_encoder_bb_0_0_0_0_0, 0), (self.digital_diff_decoder_bb_1, 0))
        self.connect((self.digital_fll_band_edge_cc_0, 0), (self.blocks_skiphead_0, 0))
        self.connect((self.digital_fll_band_edge_cc_0, 0), (self.qtgui_freq_sink_x_0, 2))
        self.connect((self.digital_fll_band_edge_cc_0, 0), (self.root_raised_cosine_filter_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.digital_costas_loop_cc_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.qtgui_const_sink_x_0_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.qtgui_eye_sink_x_0_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.qtgui_time_sink_x_0_0_0_0_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 1), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.digital_symbol_sync_xx_0, 3), (self.qtgui_time_sink_x_1_0, 1))
        self.connect((self.digital_symbol_sync_xx_0, 2), (self.qtgui_time_sink_x_1_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.qtgui_eye_sink_x_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.qtgui_time_sink_x_0_0_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "PhaseAmbiguity")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_rcc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts*self.samp_rate, self.samp_rate/self.sps, self.alpha, (11*self.sps*self.nfilts)))
        self.digital_fll_band_edge_cc_0.set_loop_bandwidth((2*math.pi/self.sps/100))
        self.digital_symbol_sync_xx_0.set_sps(self.sps)
        self.qtgui_eye_sink_x_0.set_samp_per_symbol(self.sps)
        self.qtgui_eye_sink_x_0_0.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_eye_sink_x_0_0.set_samp_per_symbol(self.sps)
        self.qtgui_eye_sink_x_0_0_0.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_eye_sink_x_0_0_0.set_samp_per_symbol(self.sps)
        self.qtgui_time_sink_x_0_0_0_0_0.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_time_sink_x_0_0_0_0_0_0.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_time_sink_x_1_0.set_y_axis(self.sps*0.99, self.sps*1.01)
        self.qtgui_time_sink_x_1_1.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_time_sink_x_1_1_0.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_time_sink_x_2.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_time_sink_x_2_0.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_time_sink_x_2_0_0.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_time_sink_x_2_0_0_0.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_time_sink_x_2_1.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_time_sink_x_2_1_0.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, (self.samp_rate/self.sps), self.alpha, (11*self.sps)))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_rcc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts*self.samp_rate, self.samp_rate/self.sps, self.alpha, (11*self.sps*self.nfilts)))
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.iio_pluto_sink_0_0.set_bandwidth(int(self.samp_rate))
        self.iio_pluto_sink_0_0.set_samplerate(int(self.samp_rate))
        self.qtgui_eye_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_eye_sink_x_0_0.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_eye_sink_x_0_0_0.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_1.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0_0_0_0.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_time_sink_x_0_0_0_0_0_0.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_1_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_1_1.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_time_sink_x_1_1_0.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_time_sink_x_2.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_time_sink_x_2_0.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_time_sink_x_2_0_0.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_time_sink_x_2_0_0_0.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_time_sink_x_2_1.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_time_sink_x_2_1_0.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, (self.samp_rate/self.sps), self.alpha, (11*self.sps)))
        self.iio_pluto_source_0.set_samplerate(int(self.samp_rate))

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rcc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts*self.samp_rate, self.samp_rate/self.sps, self.alpha, (11*self.sps*self.nfilts)))

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.set_rcc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts*self.samp_rate, self.samp_rate/self.sps, self.alpha, (11*self.sps*self.nfilts)))
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, (self.samp_rate/self.sps), self.alpha, (11*self.sps)))

    def get_tx_attenuation(self):
        return self.tx_attenuation

    def set_tx_attenuation(self, tx_attenuation):
        self.tx_attenuation = tx_attenuation
        self.iio_pluto_sink_0_0.set_attenuation(0,self.tx_attenuation)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain

    def get_rcc_taps(self):
        return self.rcc_taps

    def set_rcc_taps(self, rcc_taps):
        self.rcc_taps = rcc_taps

    def get_output_sps(self):
        return self.output_sps

    def set_output_sps(self, output_sps):
        self.output_sps = output_sps
        self.qtgui_eye_sink_x_0_0.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_eye_sink_x_0_0_0.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_time_sink_x_0_0_0_0_0.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_time_sink_x_0_0_0_0_0_0.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_time_sink_x_1_1.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_time_sink_x_1_1_0.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_time_sink_x_2.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_time_sink_x_2_0.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_time_sink_x_2_0_0.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_time_sink_x_2_0_0_0.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_time_sink_x_2_1.set_samp_rate(self.samp_rate/self.sps*self.output_sps)
        self.qtgui_time_sink_x_2_1_0.set_samp_rate(self.samp_rate/self.sps*self.output_sps)

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
        self.analog_sig_source_x_0.set_frequency(self.offset)

    def get_costas_loop_bandwidth_in_cycles_per_sample(self):
        return self.costas_loop_bandwidth_in_cycles_per_sample

    def set_costas_loop_bandwidth_in_cycles_per_sample(self, costas_loop_bandwidth_in_cycles_per_sample):
        self.costas_loop_bandwidth_in_cycles_per_sample = costas_loop_bandwidth_in_cycles_per_sample
        self.digital_costas_loop_cc_0.set_loop_bandwidth((2*math.pi*self.costas_loop_bandwidth_in_cycles_per_sample))

    def get_constellation(self):
        return self.constellation

    def set_constellation(self, constellation):
        self.constellation = constellation
        self.digital_constellation_decoder_cb_0.set_constellation(self.constellation)
        self.digital_constellation_decoder_cb_0_0.set_constellation(self.constellation)
        self.digital_constellation_decoder_cb_0_0_0.set_constellation(self.constellation)
        self.digital_constellation_decoder_cb_0_0_0_0.set_constellation(self.constellation)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.iio_pluto_sink_0_0.set_frequency(int(self.center_freq))
        self.iio_pluto_source_0.set_frequency(int(self.center_freq))




def main(top_block_cls=PhaseAmbiguity, options=None):

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
