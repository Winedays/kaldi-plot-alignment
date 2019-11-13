import sys
import csv
import os
import argparse
from argparse import ArgumentParser
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import wave
import random

'''
How to plot a wav file : https://stackoverflow.com/questions/18625085/how-to-plot-a-wav-file/18625294
matplotlib: how to draw a rectangle on image : https://stackoverflow.com/questions/37435369/matplotlib-how-to-draw-a-rectangle-on-image
wave packege document : https://docs.python.org/3/library/wave.html
matplotlib.pyplot.ax document : https://matplotlib.org/3.1.1/api/axes_api.html
Common xlabel/ylabel for matplotlib subplots : https://stackoverflow.com/questions/16150819/common-xlabel-ylabel-for-matplotlib-subplots

'''

def setArgument() :
    parser = ArgumentParser()
    parser.add_argument("-c", "--ctm", dest="ctm_file", type=str, help='File of ctm.')
    parser.add_argument("-d", "--data", dest="data_path", type=str, help='Data directory.')
    parser.add_argument("-s", "--save", dest="save_path", type=str, help='A path to save the waveform.')
    args = parser.parse_args()
    return args

# read wav.scp file
def readWavscp( wavscp ) :
    wavDict = {}
    # wav.scp format : utt_id wav_path_with_sox_commend
    f = open( wavscp , 'r' , encoding='utf-8' )
    rows = csv.reader( f , delimiter=' ' )
    for row in rows :
        utt_id = row[0]
        wav_path = row[3]
        wavDict[ utt_id ] = wav_path
    f.close()
    # print( wavDict )
    return wavDict
    
# read ctm file
def readCtm( ctm ) :
    ctmDict = {}
    # ctm format : utt_id channel_num start_time phone_dur text
    f = open( ctm , 'r' , encoding='utf-8' )
    rows = csv.reader( f , delimiter=' ' )
    for row in rows :
        utt_id = row[0]
        start_time = float(row[2])
        phone_dur = float(row[3])
        text = int(row[4])
        end_time = round( start_time+phone_dur , 3 )
        if utt_id not in ctmDict :
            ctmDict[ utt_id ] = []
        ctmDict[ utt_id ].append( { 'text': text, 'start_time': start_time, 'end_time': end_time, 'phone_dur': phone_dur } )
    f.close()
    # print( ctmDict )
    return ctmDict
  
# draw wave form & render phone boundary  
def plotWav( utt_id , cmtList , wavFile , saveFile ) :
    print( "Plot wave of " + wavFile )
    spf = wave.open( wavFile , 'r' )
    
    # If Stereo
    if spf.getnchannels() == 2:
        print('Just mono files')
        sys.exit(0)

    #Extract Raw Audio from Wav File
    signal = spf.readframes(-1)  # all frames of audio, as a bytes object.
    signal = np.fromstring(signal, 'Int16')  # convert frames data to integer
    # To Plot the x-axis in seconds you need get the frame rate and divide by size of your signa
    fs = spf.getframerate()  # sampling frequency.
    Time=np.linspace(0, len(signal)/fs, num=len(signal))  # Time Vector spaced linearly with the size


    # draw wave form
    fig,ax = plt.subplots(1)
    ax.set_title( utt_id + ' Signal Wave' , pad=30 )
    ax.set_ylim(-fs, fs)
    ax.set_xlabel( "Time(s)" )
    ax.set_ylabel( "frequency" , labelpad=-5 )
    ax.text( Time[-1]/2 , fs+1250 , "Text" , ha='center' , va='bottom' , color='k' )  # add label on the top for text 
    ax.plot(Time,signal)
    # render phone boundary
    ax = wavPltAddRectangle( ax , cmtList )
    
    # save image
    # fig = plt.gcf()
    # fig.set_size_inches(16.5, 12.2)
    # fig.savefig( saveFile, dpi=100 )
    plt.savefig( saveFile, dpi=100 )
    plt.close()
    return
    
# render phone boundary : add rectangle to the graph
def wavPltAddRectangle( ax , cmtList , fs=16000 ) :
    for cmt in cmtList :
        text = cmt['text']
        startTime = cmt['start_time']
        phoneDur = cmt['phone_dur']    
        colour = gemRandomColour()
        # Create a Rectangle patch
        rect = patches.Rectangle( (startTime,-fs) , phoneDur , fs*2 , linewidth=1 , edgecolor=colour , facecolor='none' , zorder=99) # (x,y), width, height
        # Add the patch to the Axes
        ax.add_patch(rect)
        # Add text to Axes
        ax.text( startTime+phoneDur/2 , fs , text , ha='center' , va='bottom' , color='k' )  # add text
        ax.text( startTime , -fs-100 , startTime , ha='center' , va='top' , color='k' )  # add start time
    # add end time of final word
    end_time = cmtList[-1]['end_time']
    ax.text( end_time , -fs-100 , end_time , ha='center' , va='top' , color='k' )  
    return ax 
    
# generate random colors for matplotlib
def gemRandomColour() :
    colour = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
    return colour 
    
# main function
if __name__ == "__main__" :  
    print( sys.argv[0] , ':' , ' ' .join(sys.argv) )
    # set Argument
    args = setArgument()
    self = sys.argv[0]
    runDir , self = os.path.split(os.path.realpath(self))
    # read argument
    ctmFile = args.ctm_file
    dataPath = args.data_path
    savePath = args.save_path
    # check argument
    if not os.path.isdir(dataPath) :
        raise argparse.ArgumentTypeError('dataPath exception, --data should be a directory : '+dataPath)
    if not os.path.exists(savePath) :
        print( "Warning : savePath is not exists, create it" )
        os.makedirs(savePath)
        
    # read wav.scp & ctm
    wavscpFile = os.path.join( dataPath , 'wav.scp' )
    wavDict = readWavscp( wavscpFile )
    ctmDict = readCtm( ctmFile )
    
    # drow graph
    for wav in wavDict :
        wavPath = wavDict[ wav ]
        ctmList = ctmDict[ wav ]
        saveFile = os.path.join( savePath, wav+'.png' )
        plotWav( wav , ctmList , wavPath , saveFile )
