#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: EE4002D
# GNU Radio version: 3.8.4.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
import rfid

from gnuradio import qtgui

class reader(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "EE4002D")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("EE4002D")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
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

        self.settings = Qt.QSettings("GNU Radio", "reader")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.tx_gain = tx_gain = 50
        self.rx_gain = rx_gain = 20
        self.num_taps = num_taps = [1] * 83
        self.freq = freq = 910e6
        self.decim = decim = 5
        self.dac_rate = dac_rate = 3.35*1e6
        self.ampl = ampl = 0.8
        self.adc_rate = adc_rate = 3.35*100e6/50

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_1 = uhd.usrp_source(
            ",".join(("", "driver=lime,soapy=0")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_1.set_center_freq(freq, 0)
        self.uhd_usrp_source_1.set_gain(rx_gain, 0)
        self.uhd_usrp_source_1.set_antenna('LNAL', 0)
        self.uhd_usrp_source_1.set_samp_rate(adc_rate)
        self.uhd_usrp_source_1.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)
        self.uhd_usrp_sink_2 = uhd.usrp_sink(
            ",".join(("", "driver=lime,soapy=0")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            '',
        )
        self.uhd_usrp_sink_2.set_center_freq(freq, 0)
        self.uhd_usrp_sink_2.set_gain(tx_gain, 0)
        self.uhd_usrp_sink_2.set_antenna('BAND1', 0)
        self.uhd_usrp_sink_2.set_samp_rate(dac_rate)
        self.uhd_usrp_sink_2.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)
        self.rfid_tag_decoder_0 = rfid.tag_decoder(int(adc_rate/decim))
        self.rfid_reader_0 = rfid.reader(int(adc_rate/decim), int(dac_rate))
        self.rfid_gate_0 = rfid.gate(int(adc_rate/decim))
        self.fir_filter_xxx_0 = filter.fir_filter_ccc(decim, num_taps)
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(ampl)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_sink_6 = blocks.file_sink(gr.sizeof_gr_complex*1, '/home/yeoenghoejason/Gen2-UHF-RFID-Reader/gr-rfid/misc/data/to_complex', False)
        self.blocks_file_sink_6.set_unbuffered(False)
        self.blocks_file_sink_4 = blocks.file_sink(gr.sizeof_float*1, '/home/yeoenghoejason/Gen2-UHF-RFID-Reader/gr-rfid/misc/data/reader', False)
        self.blocks_file_sink_4.set_unbuffered(False)
        self.blocks_file_sink_3 = blocks.file_sink(gr.sizeof_gr_complex*1, '/home/yeoenghoejason/Gen2-UHF-RFID-Reader/gr-rfid/misc/data/gate', False)
        self.blocks_file_sink_3.set_unbuffered(False)
        self.blocks_file_sink_2_0 = blocks.file_sink(gr.sizeof_gr_complex*1, '/home/yeoenghoejason/Gen2-UHF-RFID-Reader/gr-rfid/misc/data/decoder', False)
        self.blocks_file_sink_2_0.set_unbuffered(False)
        self.blocks_file_sink_2 = blocks.file_sink(gr.sizeof_gr_complex*1, '/home/yeoenghoejason/Gen2-UHF-RFID-Reader/gr-rfid/misc/data/matched_filter', False)
        self.blocks_file_sink_2.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, '/home/yeoenghoejason/Gen2-UHF-RFID-Reader/gr-rfid/misc/data/source', False)
        self.blocks_file_sink_0.set_unbuffered(False)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_file_sink_6, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.uhd_usrp_sink_2, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.blocks_file_sink_2, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.rfid_gate_0, 0))
        self.connect((self.rfid_gate_0, 0), (self.blocks_file_sink_3, 0))
        self.connect((self.rfid_gate_0, 0), (self.rfid_tag_decoder_0, 0))
        self.connect((self.rfid_reader_0, 0), (self.blocks_file_sink_4, 0))
        self.connect((self.rfid_reader_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.rfid_tag_decoder_0, 1), (self.blocks_file_sink_2_0, 0))
        self.connect((self.rfid_tag_decoder_0, 0), (self.rfid_reader_0, 0))
        self.connect((self.uhd_usrp_source_1, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.uhd_usrp_source_1, 0), (self.fir_filter_xxx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "reader")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.uhd_usrp_sink_2.set_gain(self.tx_gain, 0)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.uhd_usrp_source_1.set_gain(self.rx_gain, 0)

    def get_num_taps(self):
        return self.num_taps

    def set_num_taps(self, num_taps):
        self.num_taps = num_taps
        self.fir_filter_xxx_0.set_taps(self.num_taps)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_sink_2.set_center_freq(self.freq, 0)
        self.uhd_usrp_source_1.set_center_freq(self.freq, 0)

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim

    def get_dac_rate(self):
        return self.dac_rate

    def set_dac_rate(self, dac_rate):
        self.dac_rate = dac_rate
        self.uhd_usrp_sink_2.set_samp_rate(self.dac_rate)

    def get_ampl(self):
        return self.ampl

    def set_ampl(self, ampl):
        self.ampl = ampl
        self.blocks_multiply_const_vxx_0.set_k(self.ampl)

    def get_adc_rate(self):
        return self.adc_rate

    def set_adc_rate(self, adc_rate):
        self.adc_rate = adc_rate
        self.uhd_usrp_source_1.set_samp_rate(self.adc_rate)





def main(top_block_cls=reader, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
