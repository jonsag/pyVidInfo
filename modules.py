#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import configparser, os, sys, glob

from pymediainfo import MediaInfo


config = configparser.ConfigParser()  # define config file
config.read("%s/config.ini" % os.path.dirname(os.path.realpath(__file__)))  # read config file

# read variables from config file
var = config.get('header', 'var').strip()

videoTypes = (config.get('video', 'videoTypes')).split(',')  # allowed file types

# handle errors
def onError(errorCode, extra):
    print("\nError:")
    if errorCode in(1, 2): # prints error message and then prints usage
        print(extra)
        usage(errorCode)
    elif errorCode == 4: # prints error message and then exits
        print(extra)
        sys.exit(errorCode)
    elif errorCode == 5: # prints error message and then continues
        print(extra)
        
        
# print usage information        
def usage(exitCode):
    print("\nUsage:")
    print("----------------------------------------")
    print("%s -v" % sys.argv[0])
    print("    Verbose output")
    print("\n%s -h" % sys.argv[0])
    print("    Prints this")
    sys.exit(exitCode)
    
    
############################ find videos ###########################
def findVideos(path, recursive, videoTypes, verbose):
    foundVideos = []
    
    #for myFile in os.listdir(path):
    for myFile in glob.iglob("%s/**" % path, recursive=recursive):
        if checkIfVideo(myFile, videoTypes, verbose):
            if verbose:
                print("\n--- Found: %s" % os.path.join(path, myFile))
            #myFile = checkFileName(os.path.join(path, myFile), 
            #                       keepGoing, noRename, 
            #                       outDir, verbose) # check if file name complies to rules
            #if contactSheetExist(path, myFile, outDir, verbose):
            #    print "*** Contactsheet already exist\n    Skipping..."
            #else:
            #    foundVideos.append(myFile)
            foundVideos.append(myFile)
            
    return foundVideos

def checkIfVideo(myFile, videoTypes, verbose):
    isVideo = False
    correctExtension = False
    
    if verbose:
        print("--- Checking %s" % myFile)
    
    extension = os.path.splitext(myFile)[1].lstrip('.')
    for myExtension in videoTypes:
        if extension.lower() == myExtension.strip(" ").lower():
            correctExtension = True
            break

    if correctExtension:
        if os.path.isfile and not os.path.islink(myFile) and not os.path.isdir(myFile):
            if verbose:
                print("--- This is not a link and is a valid video file")
            # print "\n%s\n------------------------------------------------------------------" % myFile
        isVideo = True

    return isVideo


############################ video info ###########################
def printVideoInfo(file, verbose):
    
    print("\n%s\n--------------------" % file)
                   