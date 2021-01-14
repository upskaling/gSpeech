from os import system


def paplay(outfile, ampersand=False, name='gspeech'):
    if ampersand:
        ampersand_srt = '&'
    else:
        ampersand_srt = ''

    system(f"paplay --client-name={name} '{outfile}' {ampersand_srt}")
