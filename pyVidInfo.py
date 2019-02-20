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

# handle module errors
except getopt.GetoptError as e:
    onError(1, str(e))

# if no options passed, then exit
if len(sys.argv) == 1:  # no options passed
    onError(2, "No options given")
    
# initialize variables
find = False
recursive = False
info = False
videoBitrate = False
path = False
verbose = False    

# interpret options and arguments
for option, argument in myopts:
    if option in ('-f', '--find'):  # search for video files
        find = True
    elif option in ('-r', '--recursive'):  # search reccursively
        recursive = True
    elif option in ('-i', '--info'):  # present info on videos
        info = True    
    elif option in ('-p', '--path'):  # search in specified path
        path = argument
    elif option == '--vbr':  # search after specified video bitrate
        videoBitrate = argument
    elif option in ('-v', '--verbose'):  # verbose output
        verbose = True
    elif option in ('-h', '--help'):  # display help text
        usage(0)
 
if path:  # argument -p --path passed
    if not os.path.isdir(path):  # not a valid path
        onError(4, "%s is not a valid path" % path)
    else:
        path = os.path.abspath(path)  # construct absolute path
else:
    path = os.path.abspath(os.getcwd())  # set path to current path
    onError(5, "\nNo path given.\nUsing current dir")
        
if find:  # search for videos
    if recursive:  # search recursively
        print("\nSearching recursively for video files in \n%s ..." % path)
    else:
        print("\nSearching for video files in \n%s ..." % path)
    
    videos = findVideos(path, recursive, videoTypes, verbose)  # search videos
    
    if videos:  # videos found
        print("\nFound %s video files" % len(videos))
    else:
        print("\nDidn't find any videos")
    
if videos and info:  # found videos and presenting info
    for video in videos:
        printVideoInfo(video, verbose)
        
if videoBitrate:  # if searching by video bitrate
    
    if videoBitrate.startswith("+"):  # video bitrate larger than
        vbrLargerThan = True
        text = "larger"
    elif videoBitrate.startswith("-"):  # video bitrate smaller than
        vbrLargerThan = False
        text = "less"
    else:
        onError(6, "Argument must start with either '+' or '-'")
        
    try:
        videoBitrate = int(videoBitrate[1:])  # checking if characters after first is integer
    except:
        onError(7, "Everything after '+' or '-' in %s \nmust be integers" % videoBitrate)
        
    print("\nFinding files with bitrate %s than %s kbps..." % (text, videoBitrate))
    
    videos = findVideoBitrate(videos, vbrLargerThan, videoBitrate, verbose)  # checking if found videos meets criteria
    
    videos = sorted(videos, key=lambda k: k['videoBitrate'])  # sort by videoBitrate, smallest first 
    
    for video in videos:
        print("\n%s "  # print result
              "\n-------------------- }\n"
              "File Size: %s \n"
              "Video Bitrate: %s kbps" % 
              (video['file'],
               file_size(video['file']),
               video['videoBitrate']))
    
    
