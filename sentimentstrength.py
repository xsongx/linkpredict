# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 11:20:39 2013

@author: xsongx
"""
import shlex, subprocess
#Alec Larsen - University of the Witwatersrand, South Africa, 2012 import shlex, subprocess

def RateSentiment(sentiString):
    #open a subprocess using shlex to get the command line string into the correct args list format
    p = subprocess.Popen(shlex.split("java -jar SentiStrengthCom.jar stdin sentidata /usr/SentStrength_Data/  explain"),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #communicate via stdin the string to be rated. Note that all spaces are replaced with +
    stdout_text, stderr_text = p.communicate(sentiString.replace(" ","+"))
    #remove the tab spacing between the positive and negative ratings. e.g. 1    -5 -> 1-5
    stdout_text = stdout_text.rstrip().replace("\t","")
    return stdout_text

#t=RateSentiment("About to have a coffee, cig and enjoy the time.")
#print t