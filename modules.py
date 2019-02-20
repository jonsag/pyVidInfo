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
    elif errorCode in (4, 6, 7): # prints error message and then exits
        print(extra)
        sys.exit(errorCode)
    elif errorCode in (5, 8, 9): # prints error message and then continues
        print(extra)
        
        
# print usage information        
def usage(exitCode):
    print("\nUsage:")
    print("----------------------------------------")
    print("%s -f <-p [argument]> <-r>" % sys.argv[0])
    print("    Find videos <in path [argument]> <recursively>")
    print("\n%s ... --vbr [argument]" % sys.argv[0])
    print("    Find videos with video bitrate larger or smaller than bitrate in kbps")
    print("    Begin argument with either '+', larger than, or '.', smaller than")
    print("    Example: --vbr +1500 , to find videos with video bitrate larger than 1500 kbps")
    print("\n%s -v" % sys.argv[0])
    print("    Verbose output")
    print("\n%s -h" % sys.argv[0])
    print("    Prints this")
    sys.exit(exitCode)
    
    
############################ find videos ###########################
def findVideos(path, recursive, videoTypes, verbose):
    foundVideos = []
    
    for myFile in glob.iglob("%s/**" % path, recursive=recursive):
        if checkIfVideo(myFile, videoTypes, verbose):
            if verbose:
                print("\n--- Found: %s" % myFile)
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
    
    mi = MediaInfo.parse(file)
    
    for track in mi.tracks:
        if track.track_type == 'General':
            print("General:")
            print("     Duration: %s" % track.other_duration[3])
            print("     File size: %s" % track.other_file_size[4])
            print("     Codec: %s" % track.codec)
            print("     Stream size: %s" % track.other_stream_size[4])
            print("     Bit rate: %s" % track.other_overall_bit_rate[0])
        elif track.track_type == 'Video':
            print("Video:")
            print("     Bit rate: %s" % track.other_bit_rate[0])
            print("     Stream size: %s" % track.other_stream_size[4])
            #print("     Bit rate mode: %s" % track.bit_rate_mode)
            print("     Codec: %s" % track.codec)
            print("     Encoding library: %s" % track.encoded_library_name)
            print("     Width x height: %s x %s" % (track.width, track.height))
            print("     Frame rate: %s fps" % track.frame_rate)
            print("     Aspect ratio: %s" % track.other_display_aspect_ratio[0])
        elif track.track_type == 'Audio':
            print("Audio:")
            print("     Bit rate: %s" % track.other_bit_rate[0])
            print("     Stream size: %s" % track.other_stream_size[4])
            #print("     Bit rate mode: %s" % track.bit_rate_mode)
            print("     Codec: %s" % track.codec)    
     
        
    #for track in mi.tracks:
    #    if track.track_type == 'Video':
    #        for attr, value in track.__dict__.items():
    #            print(attr, value)
            
            
############################# video bit rate ################################
def findVideoBitrate(files, vbrLargerThan, videoBitrate, verbose):
    
    foundFiles = []
    
    for myFile in files:
        try:
            mi = MediaInfo.parse(myFile)
        except:
            onError(9, "Could not read info on video \n%s" % myFile)

        for track in mi.tracks:
            if track.track_type == 'Video':
                try:
                    vbr = int(round(track.bit_rate / 1000))
                except:
                    onError(8, "Could not detect video bitrate from \n%s \nGot '%s'" % (myFile, track.bit_rate))
              
                if vbrLargerThan:
                    if vbr >= videoBitrate:
                        foundFiles.append({'file': myFile, 'videoBitrate': vbr})
                else:
                    if vbr <= videoBitrate:
                        foundFiles.append({'file': myFile, 'videoBitrate': vbr})
                     
    return foundFiles
                        
        
############################ file size ############################
def convert_bytes(num):
    for x in ['bytes', 'KiB', 'MiB', 'GiB', 'TiB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def file_size(file_path):
    file_info = os.stat(file_path)
    return convert_bytes(file_info.st_size)
        
        
        
        
        