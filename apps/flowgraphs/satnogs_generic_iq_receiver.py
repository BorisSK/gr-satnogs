#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Generic IQ samples receiver
# Author: Manolis Surligas (surligas@gmail.com)
# Description: A generic FM demodulation block
# Generated: Sun Nov 19 11:38:07 2017
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr
import satnogs
import time


class satnogs_generic_iq_receiver(gr.top_block):

    def __init__(self, antenna=satnogs.not_set_antenna, bb_gain=satnogs.not_set_rx_bb_gain, dev_args=satnogs.not_set_dev_args, doppler_correction_per_sec=20, file_path='test.wav', if_gain=satnogs.not_set_rx_if_gain, lo_offset=100e3, ppm=0, rf_gain=satnogs.not_set_rx_rf_gain, rigctl_port=4532, rx_freq=100e6, rx_sdr_device='usrpb200'):
        gr.top_block.__init__(self, "Generic IQ samples receiver")

        ##################################################
        # Parameters
        ##################################################
        self.antenna = antenna
        self.bb_gain = bb_gain
        self.dev_args = dev_args
        self.doppler_correction_per_sec = doppler_correction_per_sec
        self.file_path = file_path
        self.if_gain = if_gain
        self.lo_offset = lo_offset
        self.ppm = ppm
        self.rf_gain = rf_gain
        self.rigctl_port = rigctl_port
        self.rx_freq = rx_freq
        self.rx_sdr_device = rx_sdr_device

        ##################################################
        # Variables
        ##################################################
        self.samp_rate_rx = samp_rate_rx = satnogs.hw_rx_settings[rx_sdr_device]['samp_rate']
        self.decimation_rx = decimation_rx = satnogs.fm_demod_settings[rx_sdr_device]['decimation_rx']

        self.taps = taps = firdes.low_pass(12.0, samp_rate_rx, 100e3, 60000, firdes.WIN_HAMMING, 6.76)

        self.quadrature_rate = quadrature_rate = samp_rate_rx / decimation_rx
        self.audio_samp_rate = audio_samp_rate = 44100
        self.audio_decimation = audio_decimation = 2

        ##################################################
        # Blocks
        ##################################################
        self.satnogs_tcp_rigctl_msg_source_0 = satnogs.tcp_rigctl_msg_source("127.0.0.1", rigctl_port, False, 1000/doppler_correction_per_sec, 1500)
        self.satnogs_coarse_doppler_correction_cc_0 = satnogs.coarse_doppler_correction_cc(rx_freq, samp_rate_rx)
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + satnogs.handle_rx_dev_args(rx_sdr_device, dev_args) )
        self.osmosdr_source_0.set_sample_rate(samp_rate_rx)
        self.osmosdr_source_0.set_center_freq(rx_freq - lo_offset, 0)
        self.osmosdr_source_0.set_freq_corr(ppm, 0)
        self.osmosdr_source_0.set_dc_offset_mode(2, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(satnogs.handle_rx_rf_gain(rx_sdr_device, rf_gain), 0)
        self.osmosdr_source_0.set_if_gain(satnogs.handle_rx_if_gain(rx_sdr_device, if_gain), 0)
        self.osmosdr_source_0.set_bb_gain(satnogs.handle_rx_bb_gain(rx_sdr_device, bb_gain), 0)
        self.osmosdr_source_0.set_antenna(satnogs.handle_rx_antenna(rx_sdr_device, antenna), 0)
        self.osmosdr_source_0.set_bandwidth(samp_rate_rx, 0)

        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(decimation_rx, (taps), lo_offset, samp_rate_rx)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, file_path, False)
        self.blocks_file_sink_0.set_unbuffered(True)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.satnogs_tcp_rigctl_msg_source_0, 'freq'), (self.satnogs_coarse_doppler_correction_cc_0, 'freq'))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.satnogs_coarse_doppler_correction_cc_0, 0))
        self.connect((self.satnogs_coarse_doppler_correction_cc_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))

    def get_antenna(self):
        return self.antenna

    def set_antenna(self, antenna):
        self.antenna = antenna
        self.osmosdr_source_0.set_antenna(satnogs.handle_rx_antenna(self.rx_sdr_device, self.antenna), 0)

    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain
        self.osmosdr_source_0.set_bb_gain(satnogs.handle_rx_bb_gain(self.rx_sdr_device, self.bb_gain), 0)

    def get_dev_args(self):
        return self.dev_args

    def set_dev_args(self, dev_args):
        self.dev_args = dev_args

    def get_doppler_correction_per_sec(self):
        return self.doppler_correction_per_sec

    def set_doppler_correction_per_sec(self, doppler_correction_per_sec):
        self.doppler_correction_per_sec = doppler_correction_per_sec

    def get_file_path(self):
        return self.file_path

    def set_file_path(self, file_path):
        self.file_path = file_path
        self.blocks_file_sink_0.open(self.file_path)

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain
        self.osmosdr_source_0.set_if_gain(satnogs.handle_rx_if_gain(self.rx_sdr_device, self.if_gain), 0)

    def get_lo_offset(self):
        return self.lo_offset

    def set_lo_offset(self, lo_offset):
        self.lo_offset = lo_offset
        self.osmosdr_source_0.set_center_freq(self.rx_freq - self.lo_offset, 0)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.lo_offset)

    def get_ppm(self):
        return self.ppm

    def set_ppm(self, ppm):
        self.ppm = ppm
        self.osmosdr_source_0.set_freq_corr(self.ppm, 0)

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.osmosdr_source_0.set_gain(satnogs.handle_rx_rf_gain(self.rx_sdr_device, self.rf_gain), 0)

    def get_rigctl_port(self):
        return self.rigctl_port

    def set_rigctl_port(self, rigctl_port):
        self.rigctl_port = rigctl_port

    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        self.rx_freq = rx_freq
        self.satnogs_coarse_doppler_correction_cc_0.set_new_freq_locked(self.rx_freq)
        self.osmosdr_source_0.set_center_freq(self.rx_freq - self.lo_offset, 0)

    def get_rx_sdr_device(self):
        return self.rx_sdr_device

    def set_rx_sdr_device(self, rx_sdr_device):
        self.rx_sdr_device = rx_sdr_device
        self.set_samp_rate_rx(satnogs.hw_rx_settings[self.rx_sdr_device]['samp_rate'])
        self.set_decimation_rx(satnogs.fm_demod_settings[self.rx_sdr_device]['decimation_rx'])
        self.osmosdr_source_0.set_gain(satnogs.handle_rx_rf_gain(self.rx_sdr_device, self.rf_gain), 0)
        self.osmosdr_source_0.set_if_gain(satnogs.handle_rx_if_gain(self.rx_sdr_device, self.if_gain), 0)
        self.osmosdr_source_0.set_bb_gain(satnogs.handle_rx_bb_gain(self.rx_sdr_device, self.bb_gain), 0)
        self.osmosdr_source_0.set_antenna(satnogs.handle_rx_antenna(self.rx_sdr_device, self.antenna), 0)

    def get_samp_rate_rx(self):
        return self.samp_rate_rx

    def set_samp_rate_rx(self, samp_rate_rx):
        self.samp_rate_rx = samp_rate_rx
        self.set_quadrature_rate(self.samp_rate_rx / self.decimation_rx)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate_rx)
        self.osmosdr_source_0.set_bandwidth(self.samp_rate_rx, 0)

    def get_decimation_rx(self):
        return self.decimation_rx

    def set_decimation_rx(self, decimation_rx):
        self.decimation_rx = decimation_rx
        self.set_quadrature_rate(self.samp_rate_rx / self.decimation_rx)

    def get_taps(self):
        return self.taps

    def set_taps(self, taps):
        self.taps = taps
        self.freq_xlating_fir_filter_xxx_0.set_taps((self.taps))

    def get_quadrature_rate(self):
        return self.quadrature_rate

    def set_quadrature_rate(self, quadrature_rate):
        self.quadrature_rate = quadrature_rate

    def get_audio_samp_rate(self):
        return self.audio_samp_rate

    def set_audio_samp_rate(self, audio_samp_rate):
        self.audio_samp_rate = audio_samp_rate

    def get_audio_decimation(self):
        return self.audio_decimation

    def set_audio_decimation(self, audio_decimation):
        self.audio_decimation = audio_decimation


def argument_parser():
    description = 'A generic FM demodulation block'
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option, description=description)
    parser.add_option(
        "", "--antenna", dest="antenna", type="string", default=satnogs.not_set_antenna,
        help="Set antenna [default=%default]")
    parser.add_option(
        "", "--bb-gain", dest="bb_gain", type="eng_float", default=eng_notation.num_to_str(satnogs.not_set_rx_bb_gain),
        help="Set bb_gain [default=%default]")
    parser.add_option(
        "", "--dev-args", dest="dev_args", type="string", default=satnogs.not_set_dev_args,
        help="Set dev_args [default=%default]")
    parser.add_option(
        "", "--doppler-correction-per-sec", dest="doppler_correction_per_sec", type="intx", default=20,
        help="Set doppler_correction_per_sec [default=%default]")
    parser.add_option(
        "", "--file-path", dest="file_path", type="string", default='test.wav',
        help="Set file_path [default=%default]")
    parser.add_option(
        "", "--if-gain", dest="if_gain", type="eng_float", default=eng_notation.num_to_str(satnogs.not_set_rx_if_gain),
        help="Set if_gain [default=%default]")
    parser.add_option(
        "", "--lo-offset", dest="lo_offset", type="eng_float", default=eng_notation.num_to_str(100e3),
        help="Set lo_offset [default=%default]")
    parser.add_option(
        "", "--ppm", dest="ppm", type="intx", default=0,
        help="Set ppm [default=%default]")
    parser.add_option(
        "", "--rf-gain", dest="rf_gain", type="eng_float", default=eng_notation.num_to_str(satnogs.not_set_rx_rf_gain),
        help="Set rf_gain [default=%default]")
    parser.add_option(
        "", "--rigctl-port", dest="rigctl_port", type="intx", default=4532,
        help="Set rigctl_port [default=%default]")
    parser.add_option(
        "", "--rx-freq", dest="rx_freq", type="eng_float", default=eng_notation.num_to_str(100e6),
        help="Set rx_freq [default=%default]")
    parser.add_option(
        "", "--rx-sdr-device", dest="rx_sdr_device", type="string", default='usrpb200',
        help="Set rx_sdr_device [default=%default]")
    return parser


def main(top_block_cls=satnogs_generic_iq_receiver, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(antenna=options.antenna, bb_gain=options.bb_gain, dev_args=options.dev_args, doppler_correction_per_sec=options.doppler_correction_per_sec, file_path=options.file_path, if_gain=options.if_gain, lo_offset=options.lo_offset, ppm=options.ppm, rf_gain=options.rf_gain, rigctl_port=options.rigctl_port, rx_freq=options.rx_freq, rx_sdr_device=options.rx_sdr_device)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
