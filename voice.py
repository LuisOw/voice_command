import speech_recognition as sr
import pydub
import os
import glob
import re
import subprocess
from playsound import playsound
from gtts import gTTS

def main():
    #convert_files()
    r = sr.Recognizer()    
    mic = sr.Microphone(0)

    basic_commands = {
        "run": run,
        "exit": _exit_,
        "navigation mode": navigation_mode,
        "hello": hello
    }
    navigation_commands = ["list", "go to", "up", "exit"]
    compiled_bc = []
    compiled_nc = []

    output_mode = input("Output mode:\n1)audio\n2)text\n")
    output(output_mode, "hello")

    for command in basic_commands:
        compiled_bc.append(re.compile(command, flags=re.I))
    
    for command in navigation_commands:
        compiled_nc.append(re.compile(command, flags=re.I))

    while True:
        string_command = get_audio(r, mic)

        for word in compiled_bc:
            match = word.search(string_command)
            if match:
                break
                    
        if not match:
            output(output_mode, "That's not a command")
            continue
        
        basic_commands[match[0]](output_mode, r, mic, compiled_nc)

           
#function to convert different file formats to wav
def convert_files():
    """
    mp3_files = glob.glob('./sounds/*.mp3')
    flv_files = glob.glob('./sounds/*.flv')
    wma_files = glob.glob('./sounds/*.wma')
    aac_files = glob.glob('./sounds/*.aac')
    """
    ogg_files = glob.glob('./sounds/*.ogg')

    for ogg_file in ogg_files:
        wav_file = os.path.splitext(ogg_file)[0] + '.wav'
        sound = pydub.AudioSegment.from_ogg(ogg_file)
        sound.export(wav_file, format="wav")

#uses the recognizer 'r' and the mic 'mic' to get the audio input
def get_audio(r, mic):
    while True:
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            try:
                string_command = r.recognize_google(audio)
                print(string_command)
                return (string_command)
            except sr.UnknownValueError:
                print("Could not undertand, please repeat.")

#text or voice output
def output(flag, text):
    if flag == "1":
        f = open("command.txt", 'w')
        f.write(text)
        f.close()
        with open("command.txt") as file:
            speak = gTTS(file.read(), lang="en")
        speak.save("command.mp3")
        playsound("command.mp3")
    elif flag == "2":
        print(text)
    else:
        pass

def navigation_mode(output_mode, r, mic, navigation_commands, *args):
    output(output_mode, "Navegation mode")
    output(output_mode, "Current directory is:")
    output(output_mode, os.getcwd())

    while True:
        string_command = get_audio(r, mic)

        for word in compiled_nc:
            match = word.search(string_command)
            if match:
                break
        
        if not match:
            output(output_mode, "That's not a navigation command")
            continue

        if match.string.lower() == "exit":
            output(output_mode, "exiting navigation mode")
            return

        if match.string.lower() == "list":
            dir_list = os.listdir()
            dir_list = ', '.join(dir_list)
            output(output_mode, dir_list)
        
        if match.string.lower() == "go to":
            #TODO
            output(output_mode, "go to not implemented")

def run(output_mode, r, mic, *args):
    output(output_mode, "Run mode. What would you like to run?")
    while True:
        string_command = get_audio(r, mic)
        try:
            sts = subprocess.run([string_command.lower()])
            return
        except OSError as e:
            output(1, ("Execution failed: {}".format, e.args[0]))            


def _exit_(output_mode, *args):
    output(output_mode, "Bye bye cutie. Have a nice day")
    exit()

def hello(output_mode, *args):
    output(output_mode, "Hello to you, but thats not a command")
main()