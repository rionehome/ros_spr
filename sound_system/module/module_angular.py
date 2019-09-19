import usb
import usb.core
import usb.util
import os
import struct
import csv
import math
import datetime
from pocketsphinx import LiveSpeech, get_model_path

counter = 0
question_dictionary = {}
noise_words = []
return_list = []
live_speech=None
dev = usb.core.find(idVendor=0x2886,idProduct=0x0018)
file_path = os.path.abspath(__file__)
model_path = get_model_path()

# Define path
csv_path = file_path.replace(
    'module/module_angular.py', 'dictionary/QandA/qanda.csv')
dict_path = file_path.replace('module/module_angular.py',
                              '/dictionary/spr_question.dict')
gram_path = file_path.replace('module/module_angular.py',
                              '/dictionary/spr_question.gram')
result_path = file_path.replace(
    'module/module_angular.py', 'log/angurarQandA-{}.txt').format(str(datetime.datetime.now()))
# PARAMETERS for sound localization
PARAMETERS = {
    'DOAANGLE': (21, 0, 'int', 359, 0, 'ro', 'DOA angle. Current value. Orientation depends on build configuration.'),
    'SPEECHDETECTED': (19, 22, 'int', 1, 0, 'ro', 'Speech detection status.', '0 = false (no speech detected)',
                       '1 = true (speech detected)')
}

TIMEOUT = 100000

# Make a dictionary from a csv file
with open(csv_path, 'r') as f:
    for line in csv.reader(f):
        question_dictionary.setdefault(str(line[0]), str(line[1]))

# Find angular
def angular():

    ###############
    #
    # use this module to find angular and detect hotword
    #
    # param >> dictionary: dict and gram file's name
    #
    # return >> return_list: [angular, saying sentence]
    #
    ###############

    global live_speech
    global counter
    global question_dictionary
    global noise_words
    global return_list

    # Noise list
    noise_words = read_noise_word(gram_path)
    setup_live_speech(False,dict_path,gram_path,1e-10)

    while True:
        if read('SPEECHDETECTED') == 1:
            for phrase in live_speech:
                #print(phrase)
                angular = direction()
                if str(phrase) not in noise_words:
                    cos = 0
                    max = 0
                    for question_key in question_dictionary.keys():
                        cos = calc_cos(str(phrase),question_key)
                        if cos > max:
                            max = cos
                            #print(max)
                    if max > 0.8:
                        file = open(result_path, 'a')
                        file.write(str(datetime.datetime.now())+": "+str(phrase)+", "+str(question_dictionary[str(phrase)])+"\n")
                        file.close()
                        print("\n-------your question--------\n",str(phrase),"\n----------------------------\n")
                        print("\n-----------answer-----------\n",question_dictionary[str(phrase)],"\n----------------------------\n")
                        counter += 1
                        print(str(counter) + ':' + str(angular) + "," + question_dictionary[str(phrase)], flush=True)
                        return_list = [angular, question_dictionary[str(phrase)]]
                        return return_list
                    else:
                        answer = "Sorry, I don't have answer."
                        file = open(result_path, 'a')
                        file.write(str(datetime.datetime.now()) + ": " + answer + "\n")
                        file.close()
                        print("\n-----------answer-----------\n",answer,"\n----------------------------\n")
                        counter += 1
                        print(str(counter) + ':' + str(angular) + "," + str(answer), flush=True)
                        return_list = [angular, answer]
                        return return_list

                # noise
                else:
                    print(".*._noise_.*.")
                    print("\n[*] LISTENING ...")
                    pass

def read_noise_word(gram):

    ###############
    #
    # use this module to put noise to list
    #
    # param >> gram: ~.gram path
    #
    # return >> words: list in noises
    #
    ###############

    words = []
    with open(gram) as f:
        for line in f.readlines():
            if "<noise>" not in line:
                continue
            if "<rule>" in line:
                continue
            line = line.replace("<noise>", "").replace(
                    " = ", "").replace("\n", "").replace(";", "")
            words = line.split(" | ")
    return words

def read(param_name):

    try:
        data = PARAMETERS[param_name]
    except KeyError:
        return

    cmd = 0x80 | data[1]

    if data[2] == 'int':
        cmd |= 0x40

    id = data[0]
    length = 8

    response = dev.ctrl_transfer(
        usb.util.CTRL_IN | usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_RECIPIENT_DEVICE,
        0, cmd, id, length, TIMEOUT)

    response = struct.unpack(b'ii', response.tostring())

    if data[2] == 'int':
        result = response[0]
    else:
        result = response[0] * (2. ** response[1])

    return result


def direction():

    ###############
    #
    # use this module to detect angular
    #
    # param >> None
    #
    # return >> None
    #
    ###############

    return read('DOAANGLE')

# Setup livespeech
def setup_live_speech(lm, dict_path, jsgf_path, kws_threshold):

    ###############
    #
    # use this module to set live speech parameter
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

def calc_cos(A,B):

    ###############
    #
    # use this module to define degree of similarity
    #
    # param >> A: first sentence
    # param >> B: second sentence
    #
    # return >> cos: degree of similarity
    #
    ###############

    list_A = []
    list_B = []
    list_A = A.split(" ")
    list_B = B.split(" ")

    lengthA = math.sqrt(len(list_A))
    lengthB = math.sqrt(len(list_B))
    match = 0
    for a in list_A:
        if a in list_B:
            match += 1

    if (lengthA != 0 and lengthB != 0):
        cos = match/(lengthB*lengthA)
    else:cos = match/100

    return cos

if __name__ == '__main__':
    list = angular()
    print(list)
