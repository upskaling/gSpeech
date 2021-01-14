from subprocess import PIPE, Popen


def trans(engine='bing', sources='en', targets='fr'):
    '''
    Traduire avec trans
    '''

    return Popen(['trans', '-brief', '-no-browser',
                  '-engine', engine, f'{sources}:{targets}'],
                 stdin=PIPE, stdout=PIPE)
