from subprocess import PIPE, DEVNULL, Popen


def argos_translate(input_text: str, sources='en', targets='fr'):
    '''
    Traduire avec argos-translate
    '''

    return Popen(['argos-translate-cli', '--from-lang', f'{sources}',
                  '--to-lang', f'{targets}', f'{input_text}'],
                 stdout=PIPE, stderr=DEVNULL)
