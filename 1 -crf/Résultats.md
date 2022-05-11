Tests du paramètre `-crf`
===
En accord avec la convention déjà utilisée, on convertit nos vidéos initialement en Apple ProRes (intraframe) en H.264 (interframe). Ce codec nous permet de paramétrer plus en détail l'encodage.

Le paramètre `-crf` qui nous intéresse dans ce test permet d'ajuster dynamiquement le bitrate (on parle de _VBR_, variable bitrate) en fonction du niveau de détail entre chaque frame et de la densité en détail des régions de chaque frame. Ce réglage s'opère par un facteur de qualité compris entre 0 (lossless) et 51 (on ne distingue plus grand chose dans une image 4096x2160). 

On teste donc plusieurs valeurs de ce facteur de qualité en encodant la même vidéo (/pipeline-tracking/2022_CF_Limoges/before_jeudi_droit/A008_11030611_C007.mov) avec des facteurs de qualité différents, puis l'on regarde le taux de compression et on apprécie qualitativement la qualité de la vidéo.

**voir images dans le dossier**

Première exécution (dossier _crf1_)
---

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 0 -preset ultrafast -acodec aac -strict experimental $out`
Output : 0.mp4
Durée de compression : 0:11:33.006050
Ratio de compression : 3.571156382489922

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 12 -preset ultrafast -acodec aac -strict experimental $out`
Output : 1.mp4
Durée de compression : 0:06:02.458777
Ratio de compression : 1.293921345534667

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset ultrafast -acodec aac -strict experimental $out`
Output : 2.mp4
Durée de compression : 0:02:06.897551
Ratio de compression : 0.14666485296967077

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 36 -preset ultrafast -acodec aac -strict experimental $out`
Output : 3.mp4
Durée de compression : 0:01:48.364789
Ratio de compression : 0.018456960152260532

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 48 -preset ultrafast -acodec aac -strict experimental $out`
Output : 4.mp4
Durée de compression : 0:01:47.702688
Ratio de compression : 0.0035231349809726736

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 51 -preset ultrafast -acodec aac -strict experimental $out`
Output : 5.mp4
Durée de compression : 0:01:47.298015
Ratio de compression : 0.0020901079144929296

Avec cette première exécution, on se rend compte qu'une valeur du facteur de qualité située autour de 24 est très satisfaisante (c'est déjà ce qui était utilisé). Cependant, on se rend compte qu'il est encore possible de baisser l'espace occupé en compressant davantage : 14.6% pour `-crf 24`, 1.8% pour `-crf 36`. On lance alors une deuxième exécution pour trouver une valeur optimale, en balayant de 22 à 36 :

Deuxième exécution (dossier _crf2_)
---

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 22 -preset ultrafast -acodec aac -strict experimental $out`
Output : 0.mp4
Durée de compression : 0:02:38.802445
Ratio de compression : 0.24468937922011882

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset ultrafast -acodec aac -strict experimental $out`
Output : 1.mp4
Durée de compression : 0:02:07.296000
Ratio de compression : 0.14666485296967077

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 26 -preset ultrafast -acodec aac -strict experimental $out`
Output : 2.mp4
Durée de compression : 0:01:53.833741
Ratio de compression : 0.09210487925625988

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 28 -preset ultrafast -acodec aac -strict experimental $out`
Output : 3.mp4
Durée de compression : 0:01:50.757603
Ratio de compression : 0.06761785136847867

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 30 -preset ultrafast -acodec aac -strict experimental $out`
Output : 4.mp4
Durée de compression : 0:01:49.303642
Ratio de compression : 0.04617644895425271

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 32 -preset ultrafast -acodec aac -strict experimental $out`
Output : 5.mp4
Durée de compression : 0:01:48.577781
Ratio de compression : 0.03365937476864848

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 34 -preset ultrafast -acodec aac -strict experimental $out`
Output : 6.mp4
Durée de compression : 0:01:48.420272
Ratio de compression : 0.025321984434272832

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 36 -preset ultrafast -acodec aac -strict experimental $out`
Output : 7.mp4
Durée de compression : 0:01:47.895087
Ratio de compression : 0.018456960152260532

En zoomant à 200% sur les premières frames, on trouve que le facteur de qualité `-crf 30` est une limite à partir de laquelle on ne pourra plus distinguer avec précision les membres des nageurs des dernières lignes. On constate la même chose en regardant les vidéos.

On constate qu'on distingue encore bien les bras des nageurs, mais aussi ceux des membres de la fédération qui passent derrière le bassin sur la vidéo avec `-crf 28` (_bench/crf2/3.mp4_). On pourrait choisir ce niveau de compression qui nous permettrait de passer d'un ratio de 14.6% à 6.7%.

Dans les prochains tests qui seront réalisés dans ce benchmark, nous utiliserons les paramètres `-crf 24` (convention actuelle), `-crf 28` (facteur prometteur pour économiser 50% d'espace occupé par vidéo) et `-crf 26` (entre-deux, pour gagner de la place tout en préservant une qualité proche de la qualité actuelle).
