import os

from pocketsphinx import LiveSpeech, get_model_path

from . import module_pico
from . import module_beep

file_path = os.path.abspath(__file__)
model_path = get_model_path()

# Define path
hotword_dic_path = file_path.replace(
    'module/module_detect.py', '/dictionary/hey_ducker.dict')
hotword_gram_path = file_path.replace(
    'module/module_detect.py', '/dictionary/hey_ducker.gram')

# Detect hotword, "hey ducker"
def detect():

    ###############
    #
    # use this module to detect hotword
    #
    # param >> None
    #
    # return >> 1
    #
    ###############

    print('[*] START HOTWORD RECOGNITION', flush=True)
    setup_live_speech(False, hotword_dic_path, hotword_gram_path, 1e-20)
    global live_speech

    # If detect hotword, delete live_speech
    module_beep.beep("start")
    for phrase in live_speech:
        #print(phrase)
        if 'hey ducker' == str(phrase):
            pause()
            module_beep.beep("stop")
            print(phrase)
            module_pico.speak('yes sir !')
            live_speech.stop = True
            del(live_speech)
            break
    return 1

# setup livespeech
def setup_live_speech(lm, dict_path, jsgf_path, kws_threshold):

    ###############
    #
    # use this module to set live espeech parameter
    #
    # param >> lm: False >> means useing own dict and gram
    # param >> dict_path: ~.dict file's path
    # param >> jsgf_path: ~.gram file's path
    # param >> kws_threshold: mean's confidence (1e-○)
    #
    # return >> None
    #
    ###############

    global live_speech
    live_speech = LiveSpeech(lm=lm,
                             hmm=os.path.join(model_path, 'en-us'),
                             dic=dict_path,
                             jsgf=jsgf_path,
                             kws_threshold=kws_threshold)

# Stop lecognition
def pause():

    ###############
    #
    # use this module to stop live speech
    #
    # param >> None
    #
    # return >> None
    #
    ###############

    global live_speech
    live_speech = LiveSpeech(no_search=True)

if __name__ == '__main__':
    detect()