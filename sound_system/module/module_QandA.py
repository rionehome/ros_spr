import os
from pocketsphinx import LiveSpeech, get_model_path
import csv

from . import module_pico
from . import module_beep

import datetime

import math

counter = 0
question_dictionary = {}
noise_words = []
file_path = os.path.abspath(__file__)

# Define path
spr_dic_path = file_path.replace(
    'module/module_QandA.py', 'dictionary/new_spr_question.dict')
spr_gram_path = file_path.replace(
    'module/module_QandA.py', 'dictionary/new_spr_question.gram')
yes_no_dic_path = file_path.replace(
    'module/module_QandA.py', 'dictionary/yes_no.dict')
yes_no_gram_path = file_path.replace(
    'module/module_QandA.py', 'dictionary/yes_no.gram')
model_path = get_model_path()
csv_path = file_path.replace(
    'module/module_QandA.py', 'dictionary/QandA/qanda.csv')
result_path = file_path.replace(
    'module/module_QandA.py', 'log/{}.txt').format(str(datetime.datetime.now()))

# Make a dictionary from a csv file
with open(csv_path, 'r') as f:
    for line in csv.reader(f):
        question_dictionary.setdefault(str(line[0]), str(line[1]))

# Listen question, or speak the number of men and women
def QandA(number):

    ###############
    #
    # use this module at spr section >> | the number of person or Q&A
    #
    # param >> number: | the number of people (wemen|men)
    #                  | how many times do you want to do Q&A
    #
    # return >> 1
    #
    ###############

    global counter
    global question_dictionary
    global noise_words
    global live_speech

    # Speak the number of men and women, person = "the number of men|the number of women"

    if "|" in str(number):
        number = number.split("|")
        person_number = "There are {} people, the number of women is {}, the number of men is {}.".format((int(number[0]) + int(number[1])), number[0], number[1])
        print(person_number)
        module_pico.speak(person_number)
        module_beep.beep("stop")

    # Listen question
    else:
        # Noise list
        noise_words = read_noise_word(spr_gram_path)

        # If I have a question witch I can answer, count 1
        while counter < number:
            print("- "+str(counter+1)+" cycle -")
            print("\n[*] LISTENING ...")
            # Setup live_speech
            setup_live_speech(False, spr_dic_path, spr_gram_path, 1e-10)
            module_beep.beep("start")
            for question in live_speech:
                #print(question)
                if str(question) not in noise_words:
                    max = 0
                    correct_question = ""
                    for question_key in question_dictionary.keys():
                        cos = calc_cos(str(question),question_key)
                        if cos > max:
                            max = cos
                            correct_question = question_key
                            #print(max)
                    question = correct_question
                    if max > 0.8:
                        file = open(result_path, 'a')
                        file.write(str(datetime.datetime.now())+": "+str(question)+", "+str(question_dictionary[str(question)])+"\n")
                        file.close()
                        if str(question) == "i want you to answer with turning":
                            pause()
                            module_beep.beep("stop")
                            print("\n----------------------------\n", str(question), "\n----------------------------\n")
                            module_pico.speak(question_dictionary[str(question)])

                            # Detect yes or no
                            setup_live_speech(False, yes_no_dic_path, yes_no_gram_path, 1e-20)
                            module_beep.beep("start")
                            for yes_no in live_speech:
                                print("\n[*] CONFIRMING ...")
                                # Noise list
                                noise_words = read_noise_word(yes_no_gram_path)

                                if str(yes_no) not in noise_words:
                                    file = open(result_path, 'a')
                                    file.write(str(datetime.datetime.now()) + ": " + str(yes_no) + "\n")
                                    file.close()
                                    if str(yes_no) == "yes":

                                        # Deside order
                                        pause()
                                        module_beep.beep("stop")
                                        answer = "Sure."
                                        print("\n---------------------------------\n", answer,
                                              "\n---------------------------------\n")
                                        module_pico.speak(answer)
                                        counter += 6
                                        break

                                    elif str(yes_no) == "no":

                                        # Fail, Ask yes-no question
                                        pause()
                                        module_beep.beep("stop")
                                        answer = "Sorry, what is your question?"
                                        print("\n---------------------------------\n", answer,
                                              "\n---------------------------------\n")
                                        module_pico.speak(answer)
                                        noise_words = read_noise_word(spr_gram_path)
                                        break
                            break

                        else:
                            pause()
                            module_beep.beep("stop")
                            print("\n-------your question--------\n",str(question),"\n----------------------------\n")
                            print("\n-----------answer-----------\n",question_dictionary[str(question)],"\n----------------------------\n")
                            module_pico.speak(question_dictionary[str(question)])
                            counter += 1
                            break
                    elif 0 < max <= 0.8:
                        pause()
                        module_beep.beep("stop")
                        answer = "Sorry, I don't have answer."
                        file = open(result_path, 'a')
                        file.write(str(datetime.datetime.now()) + ": " + answer + "\n")
                        file.close()
                        print("\n-----------answer-----------\n",answer,"\n----------------------------\n")
                        module_pico.speak(answer)
                        counter += 1
                        break

                # noise
                else:
                    print(".*._noise_.*.")
                    print("\n[*] LISTENING ...")
                    pass
    counter = 0
    return 1

def pause():

    ###############
    #
    # use this module to stop lecognition
    #
    # param >> None
    #
    # return >> None
    #
    ###############

    global live_speech
    live_speech = LiveSpeech(no_search=True)


def read_noise_word(gram):

    ###############
    #
    # use this module to put noise to list
    #
    # param >> None
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
    QandA(5)
