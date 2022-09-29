#Checks for errors in code then opens relevant 
#question pages on StackOvervlow using an API
#Gyan Bains 2021

import subprocess
import os
import sys
from subprocess import Popen,PIPE
import requests
import json
import webbrowser
import random

def findError(l1, err):
    '''
    This function parses the output to find the error type
    Parameters: l1:list of input strings, err:input message string
    Returns: error_type: error type as a string from possible_errors dic, 
             error_msg: specific error message as a string
    '''
    #This function will check for the following errors
    possible_errors = {"NameError:":1, "IndexError:":1, "KeyError:":1, "TypeError:":1,
    "ValueError:":1, "ImportError:":1, "ModuleNotFound:":1}
    
    error_identified=False
    for word in l1:
        if word in possible_errors:
            error_type = word
            error_identified=True
    if not error_identified:
        print("error could not be diagnosed")
        exit()
    error_type = error_type[:-1]
    print("Error Type" +": "+ error_type)
    print("\n", 20*"*")

    error_msg = err[err.index(error_type)+len(error_type)+2:]

    print("Error Msg: ", error_msg)
    print("\n", 20*"*")
    return(error_type, error_msg)

def readInput():
    '''
    This function reads the input and puts it into a list
    Parameters: None
    Returns: l1:list of input strings, err:input message string 
    '''
    process = subprocess.Popen(['python3','test.py'], stdout=PIPE, stderr=PIPE) 
    out, err = process.communicate()
    err = err.decode('utf-8')
    if err == "":
        print("Clean Code!")
        exit()
    l1 = err.split()
    print("l1", l1, "\n")
    err = ' '.join(l1)
    print("err", err, "\n")
    return(l1, err)

def main():
    l1, err = readInput() #read the input
    error_type, error_msg = findError(l1, err) #find the error within the input

    URL = "https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=activity&site=stackoverflow"
    PARAMS = {'title':error_type+": "+error_msg,
            'tagged':'python', 'accepted':'true'} 
    
    r = requests.get(url = URL, params = PARAMS)     
    data = r.json()
    print("opening stack overflow question pages... ")
    print("\n", 20*"*")

    #i corresponds to the number of relevant pages that will be opened
    for i in range(3):
        webbrowser.open_new_tab(data['items'][random.randint(5,len(data['items']))]['link'])

if __name__ == '__main__':
    main()