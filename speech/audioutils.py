from speech.conf import Conf

#load configuration
conf = Conf()

def getAudioCommands(text,outfile):
    cmds = []
    names = []
    if len(text) <= 32768:
        cmds.append('pico2wave -l %s -w %s \"%s\" ' % ( conf.lang, outfile, text ))
        names.append(outfile)
    else:
        discours = text.split('.')
        text = ''
        for idx,paragraph in enumerate(discours):
            text += paragraph
            if idx == len(discours)-1 or len(text) + len(discours[idx+1]) >= 32767:
                filename = conf.cache_path + 'speech' + str(idx) + '.wav'
                cmds.append('pico2wave -l %s -w %s \"%s\" ' % ( conf.lang, filename, text ))
                names.append(filename)
                text = ''

    return names, cmds
