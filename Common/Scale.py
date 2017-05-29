# coding=utf-8


MUSICAL_ALPHABET = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def key_name_with_id(id):
    return MUSICAL_ALPHABET[id]


# return : {index: mt, }
# mt: "1 or C#" , "0 or C"
def scale_major(mt):
    dict_scales = {}
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

    dict_scales[hit % 12] = MUSICAL_ALPHABET[hit % 12]

    hit += 2
    dict_scales[hit % 12] = MUSICAL_ALPHABET[hit % 12]

    hit += 2
    dict_scales[hit % 12] = MUSICAL_ALPHABET[hit % 12]

    hit += 1
    dict_scales[hit % 12] = MUSICAL_ALPHABET[hit % 12]

    hit += 2
    dict_scales[hit % 12] = MUSICAL_ALPHABET[hit % 12]

    hit += 2
    dict_scales[hit % 12] = MUSICAL_ALPHABET[hit % 12]

    hit += 2
    dict_scales[hit % 12] = MUSICAL_ALPHABET[hit % 12]
    return dict_scales


def scale_major_with_id(id):
    return scale_major(MUSICAL_ALPHABET[id])


# return : [(index, mt)]
def scale_minor(mt):
    dict_scales = {}
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

    dict_scales[hit % 12] = MUSICAL_ALPHABET[hit % 12]

    hit += 2
    dict_scales[hit % 12] = MUSICAL_ALPHABET[hit % 12]

    hit += 1
    dict_scales[hit % 12] = MUSICAL_ALPHABET[hit % 12]

    hit += 2
    dict_scales[hit % 12] = MUSICAL_ALPHABET[hit % 12]

    hit += 2
    dict_scales[hit % 12] = MUSICAL_ALPHABET[hit % 12]

    hit += 1
    dict_scales[hit % 12] = MUSICAL_ALPHABET[hit % 12]

    hit += 2
    dict_scales[hit % 12] = MUSICAL_ALPHABET[hit % 12]
    return dict_scales


def scale_minor_with_id(id):
    return scale_minor(MUSICAL_ALPHABET[id])
