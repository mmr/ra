#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Reconhece a fala 'RÁ' do microfone e toca rimshot ("tu dum tiss"!).
#
# @author Marcio Ribeiro (mmr (a) b1n org)
# @created May 2012
# 
# Para gerar .lm e .dic : http://www.speech.cs.cmu.edu/tools/lmtool.html
# Use o arquivo ra.corpus
#

import glib, gst, os

DEBUG = False
RIMSHOT_URI = 'file:///%s/rimshot.mp3' % (os.path.abspath('.'))

class Ra(object):
    def __init__(self):
        p = gst.parse_launch('alsasrc ! audioconvert ! audioresample '
                            + '! vader name=vad auto-threshold=true '
                            + '! pocketsphinx name=asr ! fakesink')
        asr = p.get_by_name('asr')
        asr.connect('result', self.result)
        asr.set_property('lm', 'ra.lm')
        asr.set_property('dict', 'ra.dic')
        asr.set_property('configured', True)
        p.set_state(gst.STATE_PLAYING)

        self.player = gst.element_factory_make('playbin2', 'player')
        fakesink = gst.element_factory_make('fakesink', 'fakesink')
        self.player.set_property('video-sink', fakesink)
        self.player.set_state(gst.STATE_NULL)
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self.on_message)

    def on_message(self, bus, message):
        if message.type == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)

    def result(self, asr, word, uttid):
        if DEBUG: print 'final: %s' % word
        if word.find('HAAAA') != -1:
           self.player.set_property('uri', RIMSHOT_URI)
           self.player.set_state(gst.STATE_PLAYING)

app = Ra()
glib.MainLoop().run()
