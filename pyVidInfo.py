#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

# import modules
import sys, getopt, os

# import modules from file modules.py
from modules import (onError, usage, 
                     videoTypes, file_size, 
                     findVideos, printVideoInfo, findVideoBitrate)


# handle options and arguments passed to script
try:
    myopts, args = getopt.getopt(sys.argv[1:],
                                 'fri'
                                 'p:'
                                 'vh',
                                 ['find', 'recursive', 'info', 'vbr=', 'path=', 'verbose', 'help'])

except getopt.GetoptError as e:
    onError(1, str(e))

# if no options passed, then exit
if len(sys.argv) == 1:  # no options passed
    onError(2, "No options given")
    
find = False
recursive = False
info = False
videoBitrate = False
path = False
verbose = False
    

# interpret options and arguments
for option, argument in myopts:
    if option in ('-f', '--find'):  # verbose output
        find = True
    elif option in ('-r', '--recursive'):  # verbose output
        recursive = True
    elif option in ('-i', '--info'):  # verbose output
        info = True    
    elif option in ('-p', '--path'):  # verbose output
        path = argument
    elif option == '--vbr':  # verbose output
        videoBitrate = argument
    elif option in ('-v', '--verbose'):  # verbose output
        verbose = True
    elif option in ('-h', '--help'):  # display help text
        usage(0)
 
if path:  # argument -p --path passed
    if not os.path.isdir(path):  # not a valid path
        onError(4, "%s is not a valid path" % path)
    else:
        path = os.path.abspath(path)
else:
    path = os.path.abspath(os.getcwd())
    onError(5, "\nNo path given.\nUsing current dir")
        
if find:
    if recursive:
        print("\nSearching recursively for video files in \n%s ..." % path)
    else:
        print("\nSearching for video files in \n%s ..." % path)
    
    videos = findVideos(path, recursive, videoTypes, verbose)
    
    if videos:
        print("\nFound %s video files" % len(videos))
    else:
        print("\nDidn't find any videos")
    
if videos and info:
    for video in videos:
        printVideoInfo(video, verbose)
        
if videoBitrate:
    
    if videoBitrate.startswith("+"):
        vbrLargerThan = True
        text = "larger"
    elif videoBitrate.startswith("-"):
        vbrLargerThan = False
        text = "less"
    else:
        onError(6, "Argument must start with either '+' or '-'")
        
    try:
        videoBitrate = int(videoBitrate[1:])
    except:
        onError(7, "Everything after '+' or '-' in %s \nmust be integers" % videoBitrate)
        
    print("\nFinding files with bitrate %s than %s kbps..." % (text, videoBitrate))
    
    videos = findVideoBitrate(videos, vbrLargerThan, videoBitrate, verbose)
    
    videos = sorted(videos, key=lambda k: k['videoBitrate']) 
    
    for video in videos:
        #print(video)
        print("\n%s \n-------------------- }\nFile Size: %s \nVideo Bitrate: %s kbps" % 
              (video['file'], file_size(video['file']), video['videoBitrate']))
    
    
    
    
    
    
    
    