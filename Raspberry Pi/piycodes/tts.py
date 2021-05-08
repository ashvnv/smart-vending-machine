# Smart Vending Machine [github.com/ashvnv/smart-vending-machine]
# Raspberry Pi Voice Assistance and Face Recognition [TTS call script]
# Last updated: 8 May 2021
#
# This script calls the Text-To-Speech using Terminal. Currently configured to use espeak
# Current espeak configuration: english female 2

# Functions: TTS_call() <- Accepts string as argument. This string is passed to espeak


from subprocess import call

#---------------------------------------------------------------------
def TTS_call(text):
    call(["espeak", "-s140", "-ven+f2", "-z", "-p65" , text])
