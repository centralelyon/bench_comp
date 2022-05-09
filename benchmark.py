#!/usr/bin/env python
# -*- coding: utf-8 -*-

import timeit
import subprocess
import shlex
import json
# pip install MediaInfo si pas dispo !
from MediaInfo import MediaInfo

f_time = timeit.default_timer

#=============================================================================
#================================CONFIGURATION================================
#=============================================================================

file_in = "/data/pipeline/pipeline-tracking/2022_CF_Limoges/before_jeudi_droit/A008_11030611_C007.mov"
format_out = ".mp4"

# -y force overwrite output file
commands = [
    "ffmpeg -y -i $in $out", # = ne rien faire, juste changer conteneur mov en format_out
    "ffmpeg -y -i $in -vcodec libx264 -crf 24 $out",
    "ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset ultrafast -acodec aac -strict experimental $out",
    "ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset ultrafast -acodec aac -strict experimental -c:v h264_videotoolbox $out"
]



if __name__ == '__main__':
    for i, command in enumerate(commands):
        print(command, i)
        
        c_time0 = f_time()
        
        file_out = str(i) + format_out
        open(file_out, 'a').close() # create empty file

        cmd = shlex.split(command.replace("$in", file_in).replace("$out", file_out)) # -c:v h264_videotoolbox 
        # renvoie liste ["ffmpeg", "-y", "$in"...]
        # .replace("$in", file_in) renvoie ["ffmpeg", "-y", file_in...]
        
        #ffmpeg renvoie bcp bcp de texte (essayer dans un terminal), on log que
        #les erreurs qui empêcheraient l'exécution correcte du code
        cmd.append("-loglevel"); cmd.append("error")
        
        subprocess.call(cmd) # execute une commande sous forme de liste (cf. au dessus)
        
        c_time1 = f_time()

        m = MediaInfo(filename = file_in)
        file_in_infos = m.getInfo()

        m = MediaInfo(filename = file_out)
        file_out_infos = m.getInfo()

        print("Commande : ", command)
        
        print("Ratio de compression : ", str(int(file_out_infos["fileSize"]) / int(file_in_infos["fileSize"])))
        print("Durée de compression : ", str(c_time1 - c_time0))


# TODO
# Generate matrice of compressed files
# mesure time it takes ----> compare with videos
# convertir secondes en heures minutes secondes https://stackoverflow.com/questions/775049/how-do-i-convert-seconds-to-hours-minutes-and-seconds
# ne plus passer par MediaInfo (BEAUCOUP TROP LONG)
# change size of videos https://superuser.com/questions/933264/getting-the-smallest-video-with-same-quality-how-to-with-ffmpeg
