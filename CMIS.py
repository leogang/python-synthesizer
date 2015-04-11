'''
Created on Dec 11, 2012

@author: James
'''

'''
Basic plan: 
take a file name, make sure it's valid
create 4 lists, to represent channels.
read in each line. execute the command.
once file is empty, make the wave file. 

instruments will be stored in a list. search through it by name. 
each instrument will have attack, decay, and a list of strengths of harmonics. 

function to create a waveform. 

4 commonds

INI - songtitle, tempo 
DEF - sets up instruments
PLY - plays a note (4 of these) 
RES - plays a rest on (channel, length) 
VOL - changes the volume of a channel(4 of these)


PLY: will have channel, instrument, note, length   OF NOTE: Rests are simply of freqency 0.

VOL: each channel should have an amplitude setting? 

additive synthesis to create sounds with the right blend of harmonics. 
'''

import wave as w
import math
import struct

class CMIS(object):
    coms = []
    input = ""
    instruments = []
    channels = [],[],[],[]
    tempoSec = 0
    name = ""
    
    vols = [1.0,1.0,1.0,1.0]
    
    tones = ["C0", "C0#", "D0b", "D0", "D0#", "E0b", "E0", "E0#", "F0b", "F0", "F0#", "G0b", "G0","G0#", "A0b", "A0", "A0#", "B0b", "B0", "B0#","C1b",
             "C1", "C1#", "D1b", "D1", "D1#", "E1b", "E1", "E1#", "F1b", "F1", "F1#", "G1b", "G1","G1#", "A1b", "A1", "A1#", "B1b", "B1", "B1#","C2b",
             "C2", "C2#", "D2b", "D2", "D2#", "E2b", "E2", "E2#", "F2b", "F2", "F2#", "G2b", "G2","G2#", "A2b", "A2", "A2#", "B2b", "B2", "B2#","C3b",
             "C3", "C3#", "D3b", "D3", "D3#", "E3b", "E3", "E3#", "F3b", "F3", "F3#", "G3b", "G3","G3#", "A3b", "A3", "A3#", "B3b", "B3", "B3","C4b",
             "C4", "C4#", "D4b", "D4", "D4#", "E4b", "E4", "E4#", "F4b", "F4", "F4#", "G4b", "G4","G4#", "A4b", "A4", "A4#", "B4b", "B4", "B4#","C5b",
             "C5", "C5#", "D5b", "D5", "D5#", "E5b", "E5", "E5#", "F5b", "F5", "F5#", "G5b", "G5","G5#", "A5b", "A5", "A5#", "B5b", "B5", "B5#","C6b",
             "C6", "C6#", "D6b", "D6", "D6#", "E6b", "E6", "E6#", "F6b", "F6", "F6#", "G6b", "G6","G6#", "A6b", "A6", "A6#", "B6b", "B6", "B6#","C7b",
             "C7", "C7#", "D7b", "D7", "D7#", "E7b", "E7", "E7#", "F7b", "F7", "F7#", "G7b", "G7","G7#", "A7b", "A7", "A7#", "B7b", "B7", "B7#","C8b",
             "C8", "C8#", "D8b", "D8", "D8#", "E8b"],[16.35, 17.32, 17.32, 18.35, 19.45, 19.45, 20.60, 20.60, 21.83, 21.83, 23.12, 23.12, 24.50, 25.96, 25.96,
             27.50, 29.14, 29.14, 30.87,30.87, 32.70, 32.70, 34.65, 34.65, 36.71, 38.89, 38.89, 41.20, 41.20, 43.65, 43.65, 46.25, 46.25, 49.00, 51.91, 51.91, 55.00,
              58.27, 58.27, 61.74, 61.74, 65.41, 65.41, 69.30, 69.30, 73.42, 77.78, 77.78, 82.41, 82.41, 87.31, 87.31, 92.50, 92.50, 98.00, 103.83, 103.83, 110.00,
               116.54, 116.54, 123.47, 123.47, 130.81, 130.81, 138.59, 138.59, 146.83, 155.56, 155.56, 164.81, 164.81, 174.61, 174.61, 185.00, 185.00, 196.00, 207.65, 
               207.65, 220.00, 233.08, 233.08, 246.94, 246.94, 261.63, 261.63, 277.18, 277.18, 293.66, 311.13, 311.13, 329.63, 329.63, 349.23, 349.23, 369.99, 369.99,
                392.00, 415.30, 415.30, 440.00, 466.16, 466.16, 493.88, 493.88, 523.25, 523.25, 554.37, 554.37, 587.33, 622.25, 622.25, 659.26, 659.26, 698.46, 698.46, 
                739.99, 739.99, 783.99, 830.61, 830.61, 880.00, 932.33, 932.33, 987.77, 987.77, 1046.50, 1046.50, 1108.73, 1108.73, 1174.66, 1244.51, 1244.51, 1318.51, 1318.51,
                 1396.91, 1396.91, 1479.98, 1479.98, 1567.98, 1661.22, 1661.22, 1760.00, 1864.66, 1864.66, 1975.53, 1975.53, 2093.00, 2093.00, 2217.46, 2217.46, 2349.32,
                  2489.02, 2489.02, 2637.02, 2637.02, 2793.83, 2793.83, 2959.96, 2959.96, 3135.96, 3322.44, 3322.44, 3520.00, 3729.31, 3729.31, 3951.07, 3951.07,
                   4186.01, 4186.01, 4434.92, 4424.92, 4698.64, 4978.03, 4978.03]
                  
                  
    def __init__(self):
        var = raw_input("Enter File Name: ")
        self.input = open(var,'r')
        self.name = var
        #fix the above with a possibility of failure.
        for x in range(0,4):
            self.channels[x].append(0)
        self.coms = self.input.readlines()
        self.convertCommands()
        self.executeCommands()
        self.convertToWave()
        return

    def convertCommands(self):
        temp = []
        for x in range(0,len(self.coms)):
            temp.append(self.coms[x].split())
        self.coms = temp
        return

    def executeCommands(self):
        for x in range(0,len(self.coms)):
            if self.coms[x][0] == "INI":
                self.initial(self.coms[x])
            elif self.coms[x][0] == "DEF":
                self.defInstrument(self.coms[x])
            elif self.coms[x][0] == "PLY":
                self.playNote(self.coms[x])
            elif self.coms[x][0]== "RST":
                self.addRest(self.coms[x])
            elif self.coms[x][0] == "VOL":
                self.volAdjust(self.coms[x])
        return

    def initial(self,com):
        self.tempoSec =  44100 / (int(float(com[2]))/ 60)
        #tempo == number of samples per beat. 
        return
    
    def defInstrument(self,com):
        tem = []
        for x in range(1,len(com)):
            tem.append(com[x])
        self.instruments.append(tem)
        return 
    
    def addRest(self,com):
        for x in range(0,int(float(com[2])*self.tempoSec)):
            self.channels[int(float(com[1]))].append(0)
        return
    
    def playNote(self,com):
        note = self.generateNote(self.findInstrument(com[2]),self.lookupNote(com[3]),float(com[4]),int(float(com[1])))
        self.addToChannel(int(float(com[1])), note)
        return
    
    def lookupNote(self,note):
        for x in range(0,168):
            if self.tones[0][x] == note:
                return self.tones[1][x]
        print ''.join(["Note not Found ",note]) 
        return 0.0
    
    def volAdjust(self,com):
        ch = int(float(com[1]))
        self.vols[ch] = float(com[2])
        return
    
    def findInstrument(self,in_id):
        y = -1
        for x in range(0,len(self.instruments)):
            if self.instruments[x][0] == in_id:
                y = x
        if y == -1:
            print ''.join(["Instrument ",in_id," not found"])
            y = 0
        return y

    #add waves depends on equal sized lists
    def addWaves(self,wav1,wav2,per1,per2):
        wav = []
        for x in range(0,len(wav1)):
            temp = ((wav1[x])*per1) + ((wav2[x]) * per2)
            wav.append(temp/2.0)
        return wav

    def generateNote(self,instrument,freq,length,chan):
        instr = self.instruments[instrument]
        note_len = int(length* self.tempoSec)
        note = []
        for y in range(0,note_len):
            temp = 0.0
            for x in range(1,len(instr)):
                angle = (2.0 * math.pi * (freq*x)) / 44100.0
                temp += float(instr[x])*(math.sin(angle*y)+math.cos(angle*y))
            temp *= self.vols[chan]
            note.append(temp)
	return note
        
    
    #takes self, channel number and note to add
    def addToChannel(self,chan,note):
        for x in range(0,len(note)):
            self.channels[chan].append(note[x])
        return

    def combineChannels(self):
        max_len = max_len = len(self.channels[0])
        for x in range(1,4):
            if len(self.channels[x]) > max_len:
                max_len = len(self.channels[x])
        for y in range(0,4):
            if len(self.channels[y]) < max_len:
                for z in range(len(self.channels[y]),max_len):
                    self.channels[y].append(0)
        output = self.addWaves(self.channels[0],self.channels[1],1.0,1.0)
        output = self.addWaves(self.channels[2],output,1.0,1.0)
        output = self.addWaves(self.channels[3],output,1.0,1.0)
        return output

    def convertToWave(self):
        output = self.combineChannels()
        outs = []
        for x in range(0,len(output)):
            outs.append(struct.pack('f',output[x]))
        self.name = ''.join([self.name,".wav"])
        wav = w.openfp(self.name,'w')
        wav.setparams((1, 4, 44100, len(outs), "NONE", ""))
        out_str = ''.join(outs)
        wav.writeframes(out_str)
        wav.close()
        return

CM = CMIS()
