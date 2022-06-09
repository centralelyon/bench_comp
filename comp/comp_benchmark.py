#!/usr/bin/env python
# -*- coding: utf-8 -*-

import timeit
import subprocess
import shlex
from datetime import timedelta
import os
import ffmpeg #pip install ffmpeg-python (and not other packages)
import json

#%% Configuration

file_in = "/data/bench/A008_11030611_C007.mov"
format_out = ""
destination = ""

# -y force overwrite output file
commands = [
    #"ffmpeg -y -i $in $out", # = ne rien faire, juste changer conteneur de file_in en format_out
    #"ffmpeg -y -i $in -vcodec libx264 -crf 24 $out",
    "ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset ultrafast -acodec aac -strict experimental $out",                      #4:2:2 10-bit
    "ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset ultrafast -vf format=yuv422p -acodec aac -strict experimental $out",     #4:2:2 8-bit
    "ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset ultrafast -vf format=yuv420p10le -acodec aac -strict experimental $out", #4:2:0 10-bit
    "ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset ultrafast -vf format=yuv420p -acodec aac -strict experimental $out",     #4:2:0 8-bit
    "ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset ultrafast -vf format=yuv411p -acodec aac -strict experimental $out",     #4:1:1 8-bit
    
    "ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset superfast -acodec aac -strict experimental $out",                      #4:2:2 10-bit
    "ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset superfast -vf format=yuv422p -acodec aac -strict experimental $out",     #4:2:2 8-bit
    "ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset superfast -vf format=yuv420p10le -acodec aac -strict experimental $out", #4:2:0 10-bit
    "ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset superfast -vf format=yuv420p -acodec aac -strict experimental $out",     #4:2:0 8-bit
    "ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset superfast -vf format=yuv411p -acodec aac -strict experimental $out",     #4:1:1 8-bit    
]


#%% Processing
if not format_out: format_out = '.m4v'
if not destination: destination = os.getcwd()+'/out/'

Comp = [0]*len(commands)
Durees = [0]*len(commands)
f_time = timeit.default_timer

# get the metadata of the input video once and for all
file_duration = float(ffmpeg.probe(file_in)["streams"][0]["duration"])
in_size = os.path.getsize(file_in)

if __name__ == '__main__':
    for i, command in enumerate(commands):
        file_out = destination + str(i) + format_out
        print("Commande :", command)
        print("Output :", str(i) + format_out)
        
        c_time0 = f_time()
        open(file_out, 'a').close() # create empty file

        cmd = shlex.split(command.replace("$in", file_in).replace("$out", file_out))
        # returns a list ["ffmpeg", "-y", "$in"...]
        
        #ffmpeg renvoie bcp bcp de texte (essayer dans un terminal), on log que
        #les erreurs qui empêcheraient l'exécution correcte du code
        cmd.append("-loglevel"); cmd.append("error")
        
        #subprocess.call(cmd) # execute une commande sous forme de liste (cf. au dessus)
        
        c_time1 = f_time()
        Durees[i] = c_time1 - c_time0
        print("Durée de compression :", str(timedelta(seconds = Durees[i])))
        print("Par rapport à la durée :", str( Durees[i]/file_duration ))

        out_size = os.path.getsize(file_out)
        Comp[i] = out_size/in_size
        print("Ratio de compression :", str( Comp[i] ))
        print("")
        
        
        #%% Export
        data_out = {}
        data_out["parametres"] = Formats
        data_out["tps_ultrafast"] = Y[:5]
        data_out["comp_ultrafast"] = Comp[:5]
        data_out["tps_superfast"] = Y[5:]
        data_out["comp_ultrafast"] = Comp[:5]
        
        with open(destination + '/results.json', 'a') as json_out: 
            json.dump(data_out, json_out, indent=4)