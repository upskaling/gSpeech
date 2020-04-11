def getAudioCommands(text,outfile,lang,cache_path):
    cmds = []
    names = []
    if len(text) <= 32768:
        stream = 'pico2wave -l %s -w %s \"%s\" ' % ( lang, outfile, text )
        cmds.append(stream)
        names.append(outfile)
    else:
        discours = text.split('.')
        text = ''
        for idx,paragraph in enumerate(discours):
            text += paragraph
            if idx == len(discours)-1 or len(text) + len(discours[idx+1]) >= 32767:
                filename = cache_path + 'speech' + str(idx) + '.wav'
                cmds.append('pico2wave -l %s -w %s \"%s\" ' % ( lang, filename, text ))
                names.append(filename)
                text = ''

    return names, cmds
