""" Morse Table """


""" Eng """
TABLE = {
    "A" : ". -",
    "B" : "- . . .",
    "C" : "- . - .",
    "D" : "- . .",
    "E" : ".",
    "F" : ". . - .",
    "G" : "- - .",
    "H" : ". . . .",
    "I" : ". .",
    "J" : ". - - -",
    "K" : "- . -",
    "L" : ". - . .",
    "M" : "- -",
    "N" : "- .",
    "O" : "- - -",
    "P" : ". - - .",
    "Q" : "- - . -",
    "R" : ". - .",
    "S" : ". . .",
    "T" : "-",
    "U" : ". . -",
    "V" : ". . . -",
    "W" : ". - -",
    "X" : "- . . -",
    "Y" : "- . - -",
    "Z" : "- - . .",



    # 特殊文字
    "_" : "_",
    "/" : "/",
    " " : " "
}


def encode_morse(char):
    sign = TABLE.get(char)
    if not sign:
        raise KeyError("{} does not exist in Morse Table".format(char))
    return sign

def decode_morse(sig):
    if not sig:
        return " "
    keys = [k for k, v in TABLE.items() if v == sig]
    if not keys:
        return " "
    return keys[0]