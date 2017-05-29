# coding=utf-8
import midi
from Common.Common import *
from Common.MIDI import *
from Modules.KeyAnalyzer import *


# return: boolean
def __piano_solo(track):
    has_instr = False
    for event in track:
        if event.statusmsg != 0xC0:
            continue

        # channel 10(id:9) is Percussion
        if event.channel == 9:
            return False

        has_instr = True

        if is_piano(event.value) is False:
            return False

    return has_instr


def __get_number_for_valid_tracks(partten):
    number = 0
    for track in partten:
        for event in track:
            if event.name != 'Program Change' and event.name != 'pitch On':
                continue
            number += 1
            break
    return number


# return: list_paths
def find_midi_by_single_track(midi_dir):
    list_paths = []
    list_sub_path = get_subs(midi_dir, '*.mid')
    file_count_of_single_track = 0
    cache_group = 'single_track'
    index = 0
    for sub_path in list_sub_path:
        index += 1
        midi_path = midi_dir + sub_path[1:]
        if index % 10 == 0:
            print('cur: %d' % index)
            print('total files single track : %d' % file_count_of_single_track)
        try:
            is_single = read_cache(cache_group, sub_path)
            # is_single = None
            if is_single is None:
                pattern = midi.read_midifile(midi_path)
                track_num = __get_number_for_valid_tracks(pattern)
                if track_num == 1:
                    write_cache(cache_group, sub_path, 'true')
                    is_single = 'true'
                else:
                    write_cache(cache_group, sub_path, 'false')
                    is_single = 'false'
            if is_single == 'true':
                file_count_of_single_track += 1
                list_paths.append(midi_path)
        except Exception, e:
            print("exception: " + midi_path)
            if (str(e).find('Bad header in MIDI file.') != -1) or (str(e).find('Bad track header in MIDI') != -1):
                os.remove(midi_path)
            print(e)
            # raise e

    return list_paths


def find_midi_by_piano_solo(midi_dir):
    list_solo_paths = []
    # piano solo only
    list_paths = find_midi_by_single_track(midi_dir)
    # list_paths.sort(reverse=True)
    cache_group = 'piano_solo_only'
    for midi_path in list_paths:
        try:
            is_piano_solo = read_cache(cache_group, midi_path)
            # is_piano_solo = None
            if is_piano_solo is None:
                pattern = midi.read_midifile(midi_path)
                track = None
                for track in pattern:
                    for event in track:
                        if event.name == 'Program Change' or event.name == 'pitch On':
                            break
                if __piano_solo(track):
                    write_cache(cache_group, midi_path, 'true')
                    is_piano_solo = 'true'
                else:
                    write_cache(cache_group, midi_path, 'false')
                    is_piano_solo = 'false'

            if is_piano_solo == 'false':
                continue

            # Here is piano solo
            print('piano solo: ' + midi_path)
            list_solo_paths.append(midi_path)
        except Exception, e:
            print("exception: " + midi_path)
            print(e)
    return list_solo_paths


def __get_min_pitch(track):
    min_pitch = 0xFF
    for event in track:
        if event.statusmsg != 0x90:
            continue
        if min_pitch > event.pitch:
            min_pitch = event.pitch
    if min_pitch == 0xFF:
        return -1
    return min_pitch


def _has_pitch(track):
    for event in track:
        if event.statusmsg == 0x90:
            return True
    return False


"""
# return: {_1_16_index: [pitch,..], }
def gen_feature(track, resolution, pitch_diff):
    # print(123)
    _1_16_tick = resolution / 4  # 十六分音符分到的tick数
    dict_feature = {}
    # TODO：目前还未遇到pattern.resolution（division）为负数情况，可能是py-midi自动做了处理，以后确认
    cur_tick_total = 0
    for event in track:
        if event.tick != 0 and event.tick < _1_16_tick:
            return None  # 表明当前粒度已经小与十六分音符, 暂不支持。
        cur_tick_total += event.tick
        # MIDI中0x90表示按下键盘, 0x80表示松开, 但实际上0x80不一定被使用. 而通常使用0x90加上力度为0来表示某个音符的终结.
        if event.statusmsg != 0x90:
            continue
        if event.velocity == 0:
            continue

        index = cur_tick_total / _1_16_tick
        if dict_feature.has_key(index) is False:
            dict_feature[index] = [event.pitch]
        else:
            dict_feature[index].append(event.pitch + pitch_diff)
    return dict_feature
"""


# return: [(, velocity)]
def gen_feature(track, pitch_diff, tick_multiple):
    list_feature = []
    # TODO：目前还未遇到pattern.resolution（division）为负数情况，可能是py-midi自动做了处理，以后确认
    events_num = len(track)
    for i in range(events_num):
        event = track[i]
        # key down
        if event.statusmsg == 0x90 and event.velocity > 0:
            pitch = event.pitch
            begin_tick = event.tick
            duration_tick = 0
            # find key up
            for _i in range(i, events_num):
                _event = track[_i]
                # MIDI中0x90表示按下键盘, 0x80表示松开, 但实际上0x80不一定被使用. 而通常使用0x90加上力度为0来表示某个音符的终结.
                if (_event.statusmsg == 0x80 and _event.pitch == pitch) or \
                   (_event.statusmsg == 0x90 and _event.velocity == 0 and _event.pitch == pitch):
                    duration_tick = _event.tick
                    break

            list_feature.append((event.pitch + pitch_diff,
                                 event.velocity,
                                 int(begin_tick * tick_multiple),
                                 int(duration_tick * tick_multiple)))
    return list_feature


# return: diff, scale_id
def __calc_pitch_diff(pattern, to_pitch):
    for track in pattern:
        min_pitch = __get_min_pitch(track)
        if min_pitch == -1:
            continue
        is_major, scale_id = get_key_with_track(track)
        if is_major is None:
            return None, None  # failed
        if is_major is False:
            return None, None  # not support minor

        min_pitch_aligned = int(min_pitch / 12)*12 + scale_id
        return to_pitch - min_pitch_aligned, scale_id

        # print 'scale: %d, %d' % (is_major, scale_index)
    return None, None


def __calc_tick_multiple(pattern, to_tick):
    return float(to_tick) / float(pattern.resolution)


def feature_2_str(list_feature):
    str_feature = ''
    for tu_note in list_feature:
        str_feature += '%d %d %d %d ' % (tu_note[0], tu_note[1], tu_note[2], tu_note[3])
    return str_feature


def main():
    out = open('Data/features.txt', 'w')
    pitch_C2 = 0x24  # C2
    tick_480 = 480
    tmp = read_file('Data/piano_solo_midi.txt')
    list_piano_solo_paths = tmp.split('\n')
    # list_piano_solo_paths = find_midi_by_piano_solo('/home/pkiller/tmp/MIDI资源整理合集(共9673个)')
    for midi_path in list_piano_solo_paths:
        try:
            pattern = midi.read_midifile(midi_path)
            print('pattern.resolution:%d' % pattern.resolution)
        except Exception, e:
            print("exception: " + midi_path)
            print(e)
            continue

        # 得到曲子调号, 并算出至C2的距离差(统一features的调号)
        begin = time.time()
        pitch_diff_to_C2, scale_id = __calc_pitch_diff(pattern, pitch_C2)
        print('__calc_pitch_diff time: %f' % (time.time() - begin))
        # 算出至tick480的距离差(统一features的速度)
        begin = time.time()
        tick_multiple_to_480 = __calc_tick_multiple(pattern, tick_480)
        print('__calc_tick_multiple time: %f' % (time.time() - begin))
        # print('%s to middle C: %d, %s' % (key_name_with_id(scale_id), pitch_diff_to_C2, midi_path))
        track = None
        for track in pattern:
            if _has_pitch(track):
                break

        if pitch_diff_to_C2 is None:
            print('get pitch diff err: %s' % midi_path)
            continue

        begin = time.time()
        list_feature = gen_feature(track, pitch_diff_to_C2, tick_multiple_to_480)
        if list_feature is None:
            # print('gen_feature() not support: %s' % midi_path)
            continue
        print('gen_feature time: %f' % (time.time() - begin))
        str_feature = feature_2_str(list_feature)
        out.write(str_feature + '\n')
        print('writed: %s' % midi_path)
    out.close()

    pass

main()
# find_midi_by_piano_solo('/home/pkiller/tmp/MIDI资源整理合集(共9673个)')