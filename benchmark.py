#!/usr/bin/env python
# -*- coding: utf-8 -*-

import timeit
import subprocess
import shlex
from datetime import timedelta
from MediaInfo import MediaInfo # pip install MediaInfo si pas dispo !
import os

#=============================================================================
#================================CONFIGURATION================================
#=============================================================================

file_in = "/data/pipeline/pipeline-tracking/2022_CF_Limoges/before_jeudi_droit/A008_11030611_C007.mov"
format_out = ".mp4"

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



f_time = timeit.default_timer

# get the metadata of the input video once and for all (approximately 5 min)
m = MediaInfo(filename = file_in)
file_in_infos = m.getInfo()

if __name__ == '__main__':
    for i, command in enumerate(commands):
        file_out = str(i) + format_out
        print("Commande :", command)
        print("Output :", file_out)
        
        c_time0 = f_time()
        open(file_out, 'a').close() # create empty file

        cmd = shlex.split(command.replace("$in", file_in).replace("$out", file_out))
        # renvoie liste ["ffmpeg", "-y", "$in"...]
        # .replace("$in", file_in) renvoie ["ffmpeg", "-y", file_in...]
        
        #ffmpeg renvoie bcp bcp de texte (essayer dans un terminal), on log que
        #les erreurs qui empêcheraient l'exécution correcte du code
        cmd.append("-loglevel"); cmd.append("error")
        
        subprocess.call(cmd) # execute une commande sous forme de liste (cf. au dessus)
        
        c_time1 = f_time()
        print("Durée de compression :", str(timedelta(seconds = (c_time1 - c_time0))))
        print("Par rapport à la durée :", str( (c_time1 - c_time0)/float(file_in_infos["duration"]) ))

        out_size = os.path.getsize(file_out)
        print("Ratio de compression :", str( out_size/float(file_in_infos["fileSize"]) ))
        print("")

# TODO
# Generate matrice of compressed files