#!/usr/bin/env python
import sys
import os
import wave
import math
import struct
import random
import argparse
from itertools import *
from math import *

def aleatorio(a,b):
    return int(a+random.random()*(b-a))

class note:
    
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
            if(self.length==4.0):
                self.name = "\\pausep"
            elif(self.length==2.0):
                self.name = "\\hp"
            elif(self.length==1.0):
                self.name = "\\qp"
            elif(self.length==0.5):
                self.name = "\\ds"
            elif(self.length==0.25):
                self.name = "\\qs"
            elif(self.length==0.125):
                self.name = "\\hs"
            else:
                print('Error: Bad timing one or more pauses could not be rationalized')
        else:
            notename = notelist[int(round(12*math.log(frequency/55.)/math.log(2.),0))]
            if(self.frequency<=523.25):
                if (self.length==4.0):
                    self.name = '\\wh{'+notename+'}'
                elif (self.length==2.0):
                    self.name = '\\hu{'+notename+'}'
                elif (self.length==1.0):
                    self.name = '\\qu{'+notename+'}'
                elif (self.length==0.5):
                    self.name = '\\cu{'+notename+'}'
                elif (self.length==0.25):
                    self.name = '\\ccu{'+notename+'}'
                elif (self.length==0.125):
                    self.name = '\\cccu{'+notename+'}'
            else:
                if (self.length==4.0):
                    self.name = '\\wh{'+notename+'}'
                elif (self.length==2.0):
                    self.name = '\\hl{'+notename+'}'
                elif (self.length==1.0):
                    self.name = '\\ql{'+notename+'}'
                elif (self.length==0.5):
                    self.name = '\\cl{'+notename+'}'
                elif (self.length==0.25):
                    self.name = '\\ccl{'+notename+'}'
                elif (self.length==0.125):
                    self.name = '\\cccl{'+notename+'}'
    
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
        notelist = ["A","^A","B","C","^C","D","^D","E","F","^F","G","^G",
                    "H","^H","I","J","^J","K","^K","L","M","^M","N","^N",
                    "a","^a","b","c","^c","d","^d","e","f","^f","g","^g",
                    "h","^h","i","j","^j","k","^k","l","m","^m","n","^n",
                    "o","^o","p","q","^q","r","^r","s","t","^t","u","^u"]
        
        self.length = notes[0].length
        self.frequency = 0
        
        for note in notes:
            self.frequency += note.frequency
            if(note.length!=self.length):
                print("Error: An atempt has been made to create a chord with different-legth notes")
                exit()
        self.frequency /= len(notes)
    
        n = ''
        if (self.length==4.0 or self.length==2.0):
            n += '\\zh{'
        else:
            n += '\\zq{'
        
        for i in range(len(notes)-1):
            n += notelist[int(round(12*math.log(notes[i].frequency/55.)/math.log(2.),0))] + ' '
        
        n += '}'
        
        lastnote = int(round(12*math.log(notes[len(notes)-1].frequency/55.)/math.log(2.),0))
        
        if(notes[len(notes)-1].frequency<=523.25):
            if (self.length==4.0):
                n += '\\wh{'+notelist[lastnote]+'}'
            elif (self.length==2.0):
                n += '\\hu{'+notelist[lastnote]+'}'
            elif (self.length==1.0):
                n += '\\qu{'+notelist[lastnote]+'}'
            elif (self.length==0.5):
                n += '\\cu{'+notelist[lastnote]+'}'
            elif (self.length==0.25):
                n += '\\ccu{'+notelist[lastnote]+'}'
            elif (self.length==0.125):
                n += '\\cccu{'+notelist[lastnote]+'}'
        
        else:
            if (self.length==4.0):
                n += '\\wh{'+notelist[lastnote]+'}'
            elif (self.length==2.0):
                n += '\\hl{'+notelist[lastnote]+'}'
            elif (self.length==1.0):
                n += '\\ql{'+notelist[lastnote]+'}'
            elif (self.length==0.5):
                n += '\\cl{'+notelist[lastnote]+'}'
            elif (self.length==0.25):
                n += '\\ccl{'+notelist[lastnote]+'}'
            elif (self.length==0.125):
                n += '\\cccl{'+notelist[lastnote]+'}'
            
        self.name = n 
        
    
    def waveform(self,frame):
        numnotes = len(self.notes)
        aux = 0
        for note in self.notes:
            aux += note.waveform(frame)/numnotes
        return aux
    
    
class piece:
    
    def __init__(self,framerate=44100, blacknote=1.0,piecedata=[]):
        
        self.blacknote = blacknote
        self.framerate = framerate
        self.piecedata = piecedata
        self.piecename = "Auto-Generated-Piece"
        self.composer = "Author"
        self.blacknote = blacknote    # In units of 60 BPM
        self.tempo     = [4,4]        # Tempo [# of notes,# type of note] to be included per measure
        self.cmpinline = 4            # Number of Mesures per line
        
        self.fgseparation = 330.
        self.piecedata = piecedata
        
        self.length = 0
        for n in self.piecedata:
            self.length += n.length
        
        MissingBlacks  = -float(self.length)/(self.cmpinline*self.tempo[0]*self.tempo[1]/4)
        MissingBlacks += math.ceil(float(self.length)/(self.cmpinline*self.tempo[0]*self.tempo[1]/4))
        
        for i in range(int(MissingBlacks*self.cmpinline*self.tempo[0])):
            self.piecedata.append(note(0.,"gaussian",self.framerate,1.0,0.125/2))
            
        self.length = 0
        for n in self.piecedata:
            self.length += n.length
        
        self.numframes = self.length*self.framerate
    
    def write_piece(self):
        
        w = wave.open(self.piecename+'.wav', 'w')
        w.setparams((1,2,self.framerate,self.numframes, 'NONE', 'not compressed'))
        sampwidth = 2
        max_amplitude = float(int((2 ** (sampwidth * 8)) / 2) - 1)
        
        for i in range(len(self.piecedata)):
            for frame in range(int(self.framerate*self.piecedata[i].length/self.blacknote)):
                t = int(max_amplitude*self.piecedata[i].waveform(frame))
                binframe =''.join(''.join(struct.pack('h',t)))
                w.writeframesraw(binframe)
        w.close()
    
    def create_latex(self):
        l = open(self.piecename+'.tex','w')
        w  = ''
        w += '\\documentclass[a4paper]{article}         \n'
        w += '\\usepackage[english]{babel}              \n'
        w += '\\usepackage{graphicx}                    \n'
        w += '\\usepackage{musixtex}                    \n'
        w += '\\usepackage{calligra}                    \n' 
        w += '\\addtolength{\\oddsidemargin}{-.875in}   \n'
        w += '\\addtolength{\\evensidemargin}{-.875in}  \n'
        w += '\\addtolength{\\textwidth}{1.70in}        \n'
        w += '\\addtolength{\\topmargin}{-.875in}       \n'
        w += '\\addtolength{\\textheight}{1.50in}       \n'
        w += '\\pagenumbering{gobble}                   \n'
        w += '\\title{'+self.piecename+' }              \n'
        w += '\\author{'+self.composer+'}               \n'
        w += '\\begin{document}                         \n'
        w += '\\maketitle                               \n'
        w += '\\centering                               \n'
        w += '\\metron{\\qu}{'+str(60*self.blacknote)+'}\n'
        w += '\\input{music.tex}                        \n'
        w += '\\end{document}                           \n'
        l.write(w)
    
    def fill_latex(self):
        tittle = 'music.tex'
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
        w += '\\generalmeter{\\meterfrac'+metric+'}                \n'
        w += '\\nostartrule\n'
        w += '\\setstaffs1{2}\n'
        w += '\\setclef1{\\bass}\n'
        w += '\\startbarno='+str(cc)+'\n'
        w += '\\startextract\n'
        for note in self.piecedata:
            notecounter += 1
            if(compasscounter==0):
                w += '\\bar\n\\Notes'
            if(beamcounter==0 and compasscounter!=0):
                    w += '\\Notes '
            compasscounter += note.length
            beamcounter += note.length
            globalcounter += note.length
            freq = note.frequency
            if(compasscounter==compasslength):
                if(freq>self.fgseparation):
                    gkey += note.name+' '
                    fkey += '\\hsk'
                else:
                    fkey += note.name+' '
                    gkey += '\\hsk'
                w += fkey + '|' + gkey + '\\en'
                fkey = ''
                gkey = ''
                beamcounter = 0
                linecounter += 1
                compasscounter = 0
                cc += 1
            else:
                if(freq>self.fgseparation):
                    gkey += note.name+' '
                    fkey += '\\hsk'
                else:
                    fkey += note.name+' '
                    gkey += '\\hsk'
            if(linecounter==self.cmpinline):
                w += '\\zendextract\n'
                w += '\\end{music}\n\n'
                if(notecounter<len(self.piecedata)):
                    w += '\\begin{music}\n'
                    w += '\\generalmeter{\\meterfrac'+metric+'}\n'
                    w += '\\startbarno='+str(cc)+'\n'
                    w += '\\setstaffs1{2}\n'
                    w += '\\setclef1{\\bass}\n'
                    w += '\\startextract\n'
                linecounter = 0
        l.write(w)
        
    def create_score(self,compile=1):
        self.create_latex()
        self.fill_latex()
        if(compile==1):
            cmdname = (self.piecename).replace(" ","\\ ")+'.tex'
            logfile = (self.piecename).replace(" ","\\ ")+'.latex.log'
            os.system('pdflatex %s > %s' % (cmdname,logfile))
        
def main():
    
    rawnotes = []
    stepsize = 12         #  Tempered (12/x)th -->  AKA if x=4 the scale is built by temepered 3rds 
    basefrequency = 440.  #  Due to a LaTeX the supported range is [55=A1,1661.2188=G6#] 

    for j in range(1):
        rawnotes.append([math.pow(2.,float(12)/stepsize),1.])
        rawnotes.append([math.pow(2.,float(5)/stepsize),2.])
        rawnotes.append([math.pow(2.,float(8)/stepsize),1.])
        
        rawnotes.append([math.pow(2.,float(12)/stepsize),1.])
        rawnotes.append([math.pow(2.,float(5)/stepsize),2.])
        rawnotes.append([math.pow(2.,float(8)/stepsize),1.])
        
        rawnotes.append([math.pow(2.,float(12)/stepsize),.5])
        rawnotes.append([math.pow(2.,float(15)/stepsize),.5])
        rawnotes.append([math.pow(2.,float(14)/stepsize),1.])
        rawnotes.append([math.pow(2.,float(10)/stepsize),1.])
        rawnotes.append([math.pow(2.,float(8)/stepsize),.5])
        rawnotes.append([math.pow(2.,float(10)/stepsize),.5])
        
        rawnotes.append([math.pow(2.,float(12)/stepsize),1.])
        rawnotes.append([math.pow(2.,float(5)/stepsize),1.])
        rawnotes.append([math.pow(2.,float(3)/stepsize),.5])
        rawnotes.append([math.pow(2.,float(7)/stepsize),.5])
        rawnotes.append([math.pow(2.,float(5)/stepsize),1.])
        
        rawnotes.append([math.pow(2.,float(5)/stepsize),4.])
    
    processednotes = []
    typeofnotes = "gaussian"
    dampfactor = 2
    framerate = 44100
    speed = 2
    for i in rawnotes:
        nn = note(i[0]*basefrequency,typeofnotes,framerate,i[1],i[1]/dampfactor)
        processednotes.append(nn)
    
    lenght = 1.
    c = [note(math.pow(2.,float(12)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float( 0)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = 2.
    c = [note(math.pow(2.,float( 5)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-7)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = 1.
    c = [note(math.pow(2.,float( 8)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-4)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    
    lenght = 1.
    c = [note(math.pow(2.,float(12)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float( 0)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = 2.
    c = [note(math.pow(2.,float( 5)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-7)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = 1.
    c = [note(math.pow(2.,float( 8)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-4)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    
    lenght = .5
    c = [note(math.pow(2.,float(12)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float( 0)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = .5
    c = [note(math.pow(2.,float(15)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float( 3)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = 1.
    c = [note(math.pow(2.,float( 14)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float( 2)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = 1.
    c = [note(math.pow(2.,float(10)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-2)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = .5
    c = [note(math.pow(2.,float( 8)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-4)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = .5
    c = [note(math.pow(2.,float(10)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-2)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    
    lenght = 1.
    c = [note(math.pow(2.,float(12)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float( 0)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = 1.
    c = [note(math.pow(2.,float( 5)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-7)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = .5
    c = [note(math.pow(2.,float( 3)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-9)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = .5
    c = [note(math.pow(2.,float( 7)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-5)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = 1.
    c = [note(math.pow(2.,float( 5)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-7)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    
    lenght = 4.
    c = [note(math.pow(2.,float( 5)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-7)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    
    lenght = .5
    c = [note(math.pow(2.,float( 5)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-7)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = .5
    c = [note(math.pow(2.,float( 3)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-9)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = 1.
    c = [note(math.pow(2.,float( 7)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-5)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = 1.
    c = [note(math.pow(2.,float( 3)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-9)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = .5
    c = [note(math.pow(2.,float( 7)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-5)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = .5
    c = [note(math.pow(2.,float( 8)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-4)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    
    lenght = 4.
    c = [note(math.pow(2.,float( 5)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-7)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    
    lenght = .5
    c = [note(math.pow(2.,float( 5)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-7)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = .5
    c = [note(math.pow(2.,float( 3)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-9)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = 1.
    c = [note(math.pow(2.,float( 7)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-5)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = 1.
    c = [note(math.pow(2.,float( 3)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-9)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = .5
    c = [note(math.pow(2.,float( 8)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-5)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = .5
    c = [note(math.pow(2.,float(10)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-2)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    
    lenght = 4.
    c = [note(math.pow(2.,float( 5)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-7)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    
    lenght = .5
    c = [note(math.pow(2.,float(12)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float( 0)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = .5
    c = [note(math.pow(2.,float(15)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float( 3)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = 1.
    c = [note(math.pow(2.,float( 14)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float( 2)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = 1.
    c = [note(math.pow(2.,float(15)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float( 3)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = 1.
    c = [note(math.pow(2.,float(12)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float( 0)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    
    lenght = 1.
    c = [note(math.pow(2.,float(15)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float( 3)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = 1.
    c = [note(math.pow(2.,float(10)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-2)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = 1.
    c = [note(math.pow(2.,float(12)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float( 0)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = .5
    c = [note(math.pow(2.,float( 5)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-7)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = .5
    c = [note(math.pow(2.,float( 3)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-9)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    
    lenght = 1.
    c = [note(math.pow(2.,float( 7)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-5)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = 2.
    c = [note(math.pow(2.,float( 5)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-7)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = 1.
    c = [note(math.pow(2.,float( 5)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-7)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    
    lenght = .5
    c = [note(math.pow(2.,float( 8)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-4)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = .5
    c = [note(math.pow(2.,float(10)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-2)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = 1.
    c = [note(math.pow(2.,float( 8)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-4)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = 1.
    c = [note(math.pow(2.,float(10)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-2)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = .5
    c = [note(math.pow(2.,float( 7)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-5)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = .5
    c = [note(math.pow(2.,float( 3)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-9)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    
    lenght = 1.
    c = [note(math.pow(2.,float( 8)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-4)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = 1.
    c = [note(math.pow(2.,float( 7)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-5)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    lenght = 2.
    c = [note(math.pow(2.,float( 5)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor),
         note(math.pow(2.,float(-7)/stepsize)*basefrequency,typeofnotes,framerate,lenght,lenght/dampfactor)]
    processednotes.append(chord(c))
    
    
    postproc = []
    for i in range(1):
        for n in processednotes:
            postproc.append(n)
    
    MyPiece = piece(framerate,speed,postproc)
    MyPiece.piecename = "Zelda Ocarina of Time: Song of Time"
    MyPiece.write_piece()
    MyPiece.create_score(1)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == "__main__":
    main()
