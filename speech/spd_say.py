from subprocess import PIPE, Popen


def spd_say(text, speed=100, pitch=-10, volume=0, voice_type='female1'):
    '''
    Read with spd-say
    '''
    speed = round((speed * 100) / 2)
    pitch = round((speed * -10) / 100)

    return Popen(
        ['spd-say', '--rate', str(speed), '--pitch', str(pitch), '--volume',
         str(volume), '--wait', '--pipe-mode', '--voice-type', voice_type],
        stdin=PIPE).communicate(text.encode())
