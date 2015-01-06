#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Sig By Sig Psk Solve
# Generated: Thu Jan  1 18:44:32 2015
##################################################

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

class sig_by_sig_psk_solve(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Sig By Sig Psk Solve")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 100000
        self.noise_level = noise_level = 0.1

        ##################################################
        # Blocks
        ##################################################
        self.digital_psk_demod_0 = digital.psk.psk_demod(
          constellation_points=4,
          differential=True,
          samples_per_symbol=2,
          excess_bw=0.35,
          phase_bw=6.28/100.0,
          timing_bw=6.28/100.0,
          mod_code="none",
          verbose=False,
          log=False,
          )
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, "./complete_signal", True)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, "./demod_part1", False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blks2_packet_decoder_0_0 = grc_blks2.packet_demod_b(grc_blks2.packet_decoder(
        		access_code="",
        		threshold=-1,
        		callback=lambda ok, payload: self.blks2_packet_decoder_0_0.recv_pkt(ok, payload),
        	),
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.digital_psk_demod_0, 0), (self.blks2_packet_decoder_0_0, 0))
        self.connect((self.blks2_packet_decoder_0_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.digital_psk_demod_0, 0))


# QT sink close method reimplementation

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_noise_level(self):
        return self.noise_level

    def set_noise_level(self, noise_level):
        self.noise_level = noise_level

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
    tb = sig_by_sig_psk_solve()
    tb.Start(True)
    tb.Wait()

