#!/usr/bin/env python
# coding=utf-8

import sys
import time
import midi
import midi.sequencer as sequencer
from Common.MIDI import *


# Attach to a MIDI device and send the contents of a MIDI file to it.
def test_play():
    """
    if len(sys.argv) != 4:
        print "Usage: {0} <client> <port> <file>".format(sys.argv[0])
        exit(2)
    """

    client = '128'
    port = '0'
    # filename = "/home/pkiller/Downloads/v0/K001.MID"
    filename = '/home/pkiller/tmp/MIDI资源整理合集(共9673个)/【歌曲类】几千首国内外精品老歌/CLASSIC/MOZART.MID'
    pattern = midi.read_midifile(filename)

    hardware = sequencer.SequencerHardware()

    if not client.isdigit:
        client = hardware.get_client(client)

    if not port.isdigit:
        port = hardware.get_port(port)

    seq = sequencer.SequencerWrite(sequencer_resolution=pattern.resolution)
    seq.subscribe_port(client, port)

    pattern.make_ticks_abs()
    events = []
    for track in pattern:
        for event in track:
            if event.statusmsg == 0x90 or event.statusmsg == 0x80:
                event.pitch += 0
            events.append(event)

    events.sort()
    seq.start_sequencer()
    for event in events:
        buf = seq.event_write(event, False, False, True)
        if buf == None:
            continue
        if buf < 1000:
            time.sleep(.5)
    while event.tick > seq.queue_get_tick_time():
        seq.drain()
        time.sleep(.5)

    print 'The end?'

test_play()
