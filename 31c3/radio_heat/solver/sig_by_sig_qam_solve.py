#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Sig By Sig Qam Solve
# Generated: Thu Jan  1 18:44:34 2015
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import blks2 as grc_blks2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import wx

class sig_by_sig_qam_solve(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Sig By Sig Qam Solve")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 100000
        self.constPoints = constPoints = 16

        ##################################################
        # Blocks
        ##################################################
        self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
        	self.GetWin(),
        	baseband_freq=0,
        	dynamic_range=100,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=512,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="Waterfall Plot",
        )
        self.Add(self.wxgui_waterfallsink2_0.win)
        self.digital_qam_demod_0 = digital.qam.qam_demod(
          constellation_points=constPoints,
          differential=True,
          samples_per_symbol=2,
          excess_bw=0.35,
          freq_bw=6.28/100.0,
          timing_bw=6.28/100.0,
          phase_bw=6.28/100.0,
          mod_code="gray",
          verbose=False,
          log=False,
          )
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, "./complete_signal", True)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, "./demod_part2", False)
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
        self.connect((self.digital_qam_demod_0, 0), (self.blks2_packet_decoder_0_0, 0))
        self.connect((self.blks2_packet_decoder_0_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.digital_qam_demod_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.wxgui_waterfallsink2_0, 0))


# QT sink close method reimplementation

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate)

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
    tb = sig_by_sig_qam_solve()
    tb.Start(True)
    tb.Wait()

