# coding=utf-8


MUSICAL_ALPHABET = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


# return : [(index, mt)]
def scales_major(mt):
    list_scales = []
    assert len(mt) <= 2

    hit = MUSICAL_ALPHABET.index(mt[0].upper())
    if hit == -1:
        return None
    if len(mt) == 2:
        if mt[1].lower() == 'b':
            hit -= 1
        elif mt[1].lower() == '#':
            hit += 1

    assert (0 <= hit) and (hit < 12)

    list_scales.append((hit % 12, MUSICAL_ALPHABET[hit % 12]))

    hit += 2
    list_scales.append((hit % 12, MUSICAL_ALPHABET[hit % 12]))

    hit += 2
    list_scales.append((hit % 12, MUSICAL_ALPHABET[hit % 12]))

    hit += 1
    list_scales.append((hit % 12, MUSICAL_ALPHABET[hit % 12]))

    hit += 2
    list_scales.append((hit % 12, MUSICAL_ALPHABET[hit % 12]))

    hit += 2
    list_scales.append((hit % 12, MUSICAL_ALPHABET[hit % 12]))

    hit += 2
    list_scales.append((hit % 12, MUSICAL_ALPHABET[hit % 12]))
    return list_scales


# return : [(index, mt)]
def scales_minor(mt):
    list_scales = []
    assert len(mt) <= 2

    hit = MUSICAL_ALPHABET.index(mt[0].upper())
    if hit == -1:
        return None
    if len(mt) == 2:
        if mt[1].lower() == 'b':
            hit -= 1
        elif mt[1].lower() == '#':
            hit += 1

    assert (0 <= hit) and (hit < 12)

    list_scales.append((hit % 12, MUSICAL_ALPHABET[hit % 12]))

    hit += 2
    list_scales.append((hit % 12, MUSICAL_ALPHABET[hit % 12]))

    hit += 1
    list_scales.append((hit % 12, MUSICAL_ALPHABET[hit % 12]))

    hit += 2
    list_scales.append((hit % 12, MUSICAL_ALPHABET[hit % 12]))

    hit += 2
    list_scales.append((hit % 12, MUSICAL_ALPHABET[hit % 12]))

    hit += 1
    list_scales.append((hit % 12, MUSICAL_ALPHABET[hit % 12]))

    hit += 2
    list_scales.append((hit % 12, MUSICAL_ALPHABET[hit % 12]))
    return list_scales
