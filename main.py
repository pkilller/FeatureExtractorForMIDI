# coding=utf-8
import midi
from Common.Common import *
from Common.MIDI import *


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
            if event.name != 'Program Change' and event.name != 'Note On':
                continue
            number += 1
            break
    return number


# return: list_paths
def find_midi_by_single_track(root):
    list_paths = []
    list_sub_path = get_subs(root, '*.mid')
    file_count_of_single_track = 0
    cache_group = 'single_track'
    index = 0
    for sub_path in list_sub_path:
        index += 1
        midi_path = root + sub_path[1:]
        if index % 10 == 0:
            print('cur: %d' % index)
            print('single track file: %d' % file_count_of_single_track)
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


def find_midi_by_piano_solo():
    list_paths = []
    # piano solo only
    midi_path = '/media/pkiller/Data1/MIDI资源整理合集(共9673个)'
    list_paths = find_midi_by_single_track(midi_path)
    # list_paths.sort(reverse=True)
    cache_group = 'piano_solo_only'
    for midi_path in list_paths:
        try:
            is_piano_solo = read_cache(cache_group, midi_path)
            # is_piano_solo = None
            if is_piano_solo is None:
                pattern = midi.read_midifile(midi_path)
                for track in pattern:
                    for event in track:
                        if event.name == 'Program Change' or event.name == 'Note On':
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
            list_paths.append(midi_path)
        except Exception, e:
            print("exception: " + midi_path)
            print(e)
        return list_paths


def main():
    tmp = read_file('Data/piano_solo_midi.txt')
    list_piano_solo_paths = tmp.split('\n')
    for midi_path in list_piano_solo_paths:
        try:
            pattern = midi.read_midifile(midi_path)
            for track in pattern:
                for event in track:
                    if not (event.statusmsg == 0xFF and event.metacommand == 0x59):
                        continue

                    # 调号不是必须选项, 所以不可靠. 注释掉！
                    # assert event.data[1] == 0  # 目前只有大调样本, 所以先不考虑小调
                    if event.alternatives != 0:
                        print(123)

        except Exception, e:
            print("exception: " + midi_path)
            print(e)
    pass

main()
