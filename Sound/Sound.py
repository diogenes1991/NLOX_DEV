#!/usr/bin/env python
import sys
import os
import wave
import math
import struct
import random
import argparse
from itertools import *

def aleatorio(a,b):
    return int(a+random.random()*(b-a))

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

def sine_wave(frequency=440.0, framerate=44100, amplitude=0.5):
    '''
    Generate a sine wave at a given frequency of infinite length.
    '''
    period = int(framerate / frequency)
    if amplitude > 1.0: amplitude = 1.0
    if amplitude < 0.0: amplitude = 0.0
    lookup_table = [float(amplitude) * math.sin(2.0*math.pi*float(frequency)*(float(i%period)/float(framerate))) for i in xrange(period)]
    return (lookup_table[i%period] for i in count(0))

def square_wave(frequency=440.0, framerate=44100, amplitude=0.5):
    for s in sine_wave(frequency, framerate, amplitude):
        if s > 0:
            yield amplitude
        elif s < 0:
            yield -amplitude
        else:
            yield 0.0

def damped_wave(frequency=440.0, framerate=44100, amplitude=0.5, length=44100):
    if amplitude > 1.0: amplitude = 1.0
    if amplitude < 0.0: amplitude = 0.0
    return (math.exp(-(float(i%length)/float(framerate))) * s for i, s in enumerate(sine_wave(frequency, framerate, amplitude)))

def white_noise(amplitude=0.5):
    '''
    Generate random samples.
    '''
    return (float(amplitude) * random.uniform(-1, 1) for i in count(0))

def compute_samples(channels, nsamples=None):
    '''
    create a generator which computes the samples.

    essentially it creates a sequence of the sum of each function in the channel
    at each sample in the file for each channel.
    '''
    return islice(izip(*(imap(sum, izip(*channel)) for channel in channels)), nsamples)

def write_wavefile(filename, samples, nframes=None, nchannels=2, sampwidth=2, framerate=44100, bufsize=2048):
    "Write samples to a wavefile."
    if nframes is None:
        nframes = -1

    w = wave.open(filename, 'w')
    w.setparams((nchannels, sampwidth, framerate, nframes, 'NONE', 'not compressed'))

    max_amplitude = float(int((2 ** (sampwidth * 8)) / 2) - 1)

    # split the samples into chunks (to reduce memory consumption and improve performance)
    for chunk in grouper(bufsize, samples):
        frames = ''.join(''.join(struct.pack('h', int(max_amplitude * sample)) for sample in channels) for channels in chunk if channels is not None)
        w.writeframesraw(frames)

    w.close()

    return filename

def write_pcm(f, samples, sampwidth=2, framerate=44100, bufsize=2048):
    "Write samples as raw PCM data."
    max_amplitude = float(int((2 ** (sampwidth * 8)) / 2) - 1)

    # split the samples into chunks (to reduce memory consumption and improve performance)
    for chunk in grouper(bufsize, samples):
        frames = ''.join(''.join(struct.pack('h', int(max_amplitude * sample)) for sample in channels) for channels in chunk if channels is not None)
        f.write(frames)

    f.close()

    return filename

class note:
    
    # We will have three styles of notes:
    #        - Square: Sharp rise to maximum amplitude  
    #        - Triangular: Llinear increase to maximum amplitude (2 Parameters)
    #        - Gaussian: Exponential rise to maximum
    
    def __init__(self,frequency=440.0, style="gaussian",
                 framerate=44100,length=1.0, sigma=0.1):
        self.frequency = frequency
        self.framerate = framerate
        self.sigma = sigma
        self.style = style
        self.length = length
        notelist = ["A","^A","B","C","^C","D","^D","E","F","^F","G","^G",
                    "H","^H","I","J","^J","K","^K","L","M","^M","N","^N",
                    "a","^a","b","c","^c","d","^d","e","f","^f","g","^g",
                    "h","^h","i","j","^j","k","^k","l","m","^m","n","^n",
                    "o","^o","p","q","^q","r","^r","s","t","^t","u","^u"]
        
        if(self.frequency==0):
            if(self.length==2.0):
                self.name = "\hp"
            elif(self.length==1.0):
                self.name = "\qp"
            elif(self.length==0.5):
                self.name = "\ds"
            elif(self.length==0.25):
                self.name = "\qs"
            elif(self.length==0.125):
                self.name = "\hs"
            else:
                print 'Error: Bad timing one or more pauses could not be rationalized'
        else:
            if (self.length==2.0):
                self.name = '\hu{'+notelist[int(round(12*math.log(frequency/55.)/math.log(2.),0))]+'}'
            elif (self.length==1.0):
                self.name = '\qu{'+notelist[int(round(12*math.log(frequency/55.)/math.log(2.),0))]+'}'
            elif (self.length==0.5):
                self.name = '\cu{'+notelist[int(round(12*math.log(frequency/55.)/math.log(2.),0))]+'}'
            elif (self.length==0.25):
                self.name = '\ccu{'+notelist[int(round(12*math.log(frequency/55.)/math.log(2.),0))]+'}'
            elif (self.length==0.125):
                self.name = '\cccu{'+notelist[int(round(12*math.log(frequency/55.)/math.log(2.),0))]+'}'
                
    def waveform(self,frame):
        if(self.frequency==0):
            return 0
        if(self.style=="square"):
            return math.sin(2*math.pi*self.frequency*frame/self.framerate)
        if(self.style=="gaussian"):
            r = math.sin(2*math.pi*self.frequency*frame/self.framerate)
            exp = (float(frame)/self.framerate)/self.sigma
            exp *= exp/2
            exp = math.exp(-exp)
            r *= exp
            return r
        
        
class chord:
    
    def __init__(self,notes=[]):
        self.notes = notes
    
    def waveform(self,frame):
        numnotes = len(self.notes)
        for note in self.notes:
            aux = note.waveform(frame)/numnotes
            
    
    
    
class piece:
    
    #  The black note length will set the fixed separation between the start of consecutive notes
    #  2 black notes are added as buffers 1 at the start and 1 at the begining
    #  Piece data stores the notes of the piece in consecutive order 
    # 
    
    def __init__(self,framerate=44100, blacknote=1.0,piecedata=[]):
        
        self.blacknote = blacknote
        self.framerate = framerate
        self.piecedata = piecedata
        self.piecename = "Zelda-Ocarina of Time"
        self.blacknote = "60"
        self.tempo     = [4,4]
        self.cmpinline = 1
        self.composer = "Author"
        
        self.generated = []
        
        numoctaves = 4
        stepsize = 12         #  Tempered (12/x)th -->  AKA if x=4 the scale is built by temepered 3rds 
        basefrequency = 440.  # Lowest coded frequency --> LaTeX limitation
        
        
        ## Fill-in the piece channels 
        
        ## Base Rythm: HARD-CODED
        
        for j in range(10):
            self.generated.append([math.pow(2.,float(14)/stepsize),1.])
            self.generated.append([math.pow(2.,float(7)/stepsize),2.])
            self.generated.append([math.pow(2.,float(10)/stepsize),1.])
            
            self.generated.append([math.pow(2.,float(14)/stepsize),1.])
            self.generated.append([math.pow(2.,float(7)/stepsize),2.])
            self.generated.append([math.pow(2.,float(10)/stepsize),1.])
            
            self.generated.append([math.pow(2.,float(14)/stepsize),.5])
            self.generated.append([math.pow(2.,float(17)/stepsize),.5])
            self.generated.append([math.pow(2.,float(16)/stepsize),1.])
            self.generated.append([math.pow(2.,float(14)/stepsize),1.])
            self.generated.append([math.pow(2.,float(12)/stepsize),.5])
            self.generated.append([math.pow(2.,float(14)/stepsize),.5])
            
            self.generated.append([math.pow(2.,float(14)/stepsize),1.])
            self.generated.append([math.pow(2.,float(7)/stepsize),1.])
            self.generated.append([math.pow(2.,float(5)/stepsize),.5])
            self.generated.append([math.pow(2.,float(9)/stepsize),.5])
            self.generated.append([math.pow(2.,float(7)/stepsize),1.])
            
            self.generated.append([math.pow(2.,float(7)/stepsize),4.])
            
        #print self.generated
        self.piecedata = []
        
        ## Random Trebble
        
        for i in self.generated:
            self.piecedata.append(note(basefrequency*i[0],"gaussian",self.framerate,i[1]/2,i[1]/4))
            
            
        Piecelength = 0
        for n in self.piecedata:
            Piecelength += n.length
        
        MissingBlacks  = -float(Piecelength)/(self.cmpinline*self.tempo[0]*self.tempo[1]/4)
        MissingBlacks += math.ceil(float(Piecelength)/(self.cmpinline*self.tempo[0]*self.tempo[1]/4))
        
        for i in range(int(4*MissingBlacks*self.cmpinline*self.tempo[0])):
            self.piecedata.append(note(0.,"gaussian",self.framerate,0.25,0.125/2))
            
        
        Piecelength = 0
        for n in self.piecedata:
            Piecelength += n.length
        
        self.numframes = Piecelength*self.framerate
    
    def write_piece(self):
        
        w = wave.open(self.piecename+'.wav', 'w')
        w.setparams((1,2,self.framerate,self.numframes, 'NONE', 'not compressed'))
        sampwidth = 2
        max_amplitude = float(int((2 ** (sampwidth * 8)) / 2) - 1)
        
        for i in range(len(self.piecedata)):
            for frame in range(int(self.framerate*self.piecedata[i].length)):
                t = int(max_amplitude*self.piecedata[i].waveform(frame))
                binframe =''.join(''.join(struct.pack('h',t)))
                w.writeframesraw(binframe)
        w.close()
    
    def create_latex(self):
        l = open(self.piecename+'.tex','w')
        w  = ''
        w += '\\documentclass[a4paper]{article}        \n'
        w += '\\usepackage[english]{babel}             \n'
        w += '\\usepackage{graphicx}                   \n'
        w += '\\usepackage{musixtex}                   \n'
        w += '\\usepackage{calligra}                   \n' 
        w += '\\addtolength{\oddsidemargin}{-.875in}   \n'
        w += '\\addtolength{\evensidemargin}{-.875in}  \n'
        w += '\\addtolength{\\textwidth}{1.70in}       \n'
        w += '\\addtolength{\\topmargin}{-.875in}      \n'
        w += '\\addtolength{\\textheight}{1.50in}      \n'
        w += '\\pagenumbering{gobble}                  \n'
        w += '\\title{\\calligra{'+self.piecename+'}}  \n'
        w += '\\author{'+self.composer+'}              \n'
        w += '\\begin{document}                        \n'
        w += '\maketitle                               \n'
        w += '\\input{'+self.piecename+'_music.tex}    \n'
        w += '\\end{document}                          \n'
        l.write(w)
    
    def fill_latex(self):
        tittle = self.piecename+'_music.tex'
        l = open(tittle,'w')
        metric = str(self.tempo[0])+str(self.tempo[1])
        beamlength = 4/self.tempo[1]
        compasslength = 4*self.tempo[0]/self.tempo[1]
        
        notecounter = 0
        linecounter = 0
        globalcounter = 0
        compasscounter = 0
        beamcounter = 0
        cc = 0
        w  = ''
        gkey = ''
        fkey = ''
        w += '\\begin{music}                                     \n'
        w += '\generalmeter{\meterfrac'+metric+'}                \n'
        w += '\\nostartrule\n'
        w += '\setstaffs1{2}\n'
        w += '\setclef1{\\bass}\n'
        w += '\startbarno='+str(cc)+'\n'
        w += '\startextract\n'
        for note in self.piecedata:
            #print note.frequency,note.name
            notecounter += 1
            if(compasscounter==0):
                w += '\\bar\n\Notes'
            if(beamcounter==0 and compasscounter!=0):
                    w += '\Notes '
            compasscounter += note.length
            beamcounter += note.length
            globalcounter += note.length
            freq = note.frequency
            if(beamcounter==beamlength):
                #w += '}\\tbu0\\qb0{'+note.name+'}'
                if(freq>30.63):
                    gkey += note.name+' '
                    fkey += '\hsk'
                else:
                    fkey += note.name+' '
                    gkey += '\hsk'
                w += fkey + '|' + gkey + '\en'
                fkey = ''
                gkey = ''
                beamcounter = 0
            else:
                if(freq>30.63):
                    gkey += note.name+' '
                    fkey += '\hsk'
                else:
                    fkey += note.name+' '
                    gkey += '\hsk'
            if(compasscounter==compasslength):
                #w += '\n'
                linecounter += 1
                compasscounter = 0
                cc += 1
            if(linecounter==self.cmpinline):
                w += '\zendextract\n'
                w += '\end{music}\n\n'
                if(notecounter<len(self.piecedata)):
                    w += '\\begin{music}\n'
                    w += '\generalmeter{\meterfrac'+metric+'}\n'
                    w += '\startbarno='+str(cc)+'\n'
                    w += '\setstaffs1{2}\n'
                    w += '\setclef1{\\bass}\n'
                    w += '\startextract\n'
                linecounter = 0
        l.write(w)
        print w
        
def main():
    #parser = argparse.ArgumentParser()
    #parser.add_argument('-c', '--channels', help="Number of channels to produce", default=2, type=int)
    #parser.add_argument('-b', '--bits', help="Number of bits in each sample", choices=(16,), default=16, type=int)
    #parser.add_argument('-r', '--rate', help="Sample rate in Hz", default=44100, type=int)
    #parser.add_argument('-t', '--time', help="Duration of the wave in seconds.", default=60, type=int)
    #parser.add_argument('-a', '--amplitude', help="Amplitude of the wave on a scale of 0.0-1.0.", default=0.5, type=float)
    #parser.add_argument('-f', '--frequency', help="Frequency of the wave in Hz", default=440.0, type=float)
    #parser.add_argument('filename', help="The file to generate.")
    #args = parser.parse_args()
    
    # The time of the piece will be determined by the number of notes 
    # plus 10 black notes buffer before and after  

    MyPiece = piece()
    MyPiece.write_piece()
    MyPiece.create_latex()
    MyPiece.fill_latex()
    # each channel is defined by infinite functions which are added to produce a sample.
    #channels = ((sine_wave(args.frequency, args.rate, args.amplitude),) for i in range(args.channels))

    # convert the channel functions into waveforms
    #samples = compute_samples(channels, args.rate * args.time)

    # write the samples to a file
    #if args.filename == '-':
        #filename = sys.stdout
    #else:
        #filename = args.filename
    #write_wavefile(filename, samples, args.rate * args.time, args.channels, args.bits / 8, args.rate)

if __name__ == "__main__":
    main()
