import os
import wave
import pyttsx3


# Speak content
def speak(content):

    ###############
    #
    # use this module to speak param
    #
    # param >> content: speak this content
    #
    # return >> None
    #
    ###############

    print("[*] SPEAK : {0}".format(content),flush=True)
    engine=pyttsx3.init()
    rate=engine.getProperty('rate')
    engine.setProperty('rate', 120)
    engine.say(content)
    engine.runAndWait()
    engine.stop()
    
if __name__ == '__main__':
    speak("hello world")
