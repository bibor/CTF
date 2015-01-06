#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Sig By Sig Qam Chal
# Generated: Thu Jan  1 18:44:21 2015
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import blks2 as grc_blks2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import wx

class sig_by_sig_qam_chal(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Sig By Sig Qam Chal")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 100000
        self.noise_level = noise_level = 0.1
        self.constPoints = constPoints = 16

        ##################################################
        # Blocks
        ##################################################
        self.digital_qam_mod_0 = digital.qam.qam_mod(
          constellation_points=constPoints,
          mod_code="gray",
          differential=True,
          samples_per_symbol=2,
          excess_bw=0.35,
          verbose=False,
          log=False,
          )
        self.blocks_xor_xx_0 = blocks.xor_bb()
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, samp_rate)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_char*1, "./payload", True)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, "./key", True)
        self.blocks_file_sink_0_1 = blocks.file_sink(gr.sizeof_gr_complex*1, "./pure_signal_qam", False)
        self.blocks_file_sink_0_1.set_unbuffered(False)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.blks2_packet_encoder_0 = grc_blks2.packet_mod_b(grc_blks2.packet_encoder(
        		samples_per_symbol=2,
        		bits_per_symbol=4,
        		preamble="",
        		access_code="",
        		pad_for_usrp=False,
        	),
        	payload_length=0,
        )
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, noise_level, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blks2_packet_encoder_0, 0), (self.digital_qam_mod_0, 0))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.digital_qam_mod_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_file_sink_0_1, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_xor_xx_0, 1))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_xor_xx_0, 0))
        self.connect((self.blocks_xor_xx_0, 0), (self.blks2_packet_encoder_0, 0))


# QT sink close method reimplementation

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_noise_level(self):
        return self.noise_level

    def set_noise_level(self, noise_level):
        self.noise_level = noise_level
        self.analog_noise_source_x_0.set_amplitude(self.noise_level)

    def get_constPoints(self):
        return self.constPoints

    def set_constPoints(self, constPoints):
        self.constPoints = constPoints

if __name__ == '__main__':
    import ctypes
    import os
    if os.name == 'posix':
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = sig_by_sig_qam_chal()
    tb.Start(True)
    tb.Wait()

