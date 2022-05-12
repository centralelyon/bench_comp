Tests de l'accélération matérielle
===
On vient précédemment de trouver qu'en passant du preset `ultrafast` à `superfast`, on gagnait à la fois en qualité d'image et en taille de fichier, au prix d'un temps d'encodage approximativement 50% plus long. On essaie de voir si on ne peut pas regagner du temps en utilisant l'accélération matérielle.

Pour ce faire, on va compresser plusieurs fois la même vidéo avec les mêmes paramètres en utilisant à chaque fois une accélération différente. On commence par obtenir la liste des accélérations disponibles en entrant `ffmpeg -hwaccels` dans le shell Unix. Nous allons donc tester aujourd'hui :
- `vdpau`
- `cuda`
- `vaapi`
- `drm`
- `opencl`
- `cuvid`

On va tester également le paramètre `-hwaccel auto` pour retrouver à partir du temps de compression le mode d'accélération choisi automatiquement par `ffmpeg`, pour pouvoir ensuite l'inclure dans notre commande optimisée.

Exécution (dossier _hwaccel_)
===
Preset `ultrafast`
---

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset ultrafast -acodec aac -strict experimental $out`
Output : 0.mp4
Durée de compression : 0:02:07.709756

Commande : `ffmpeg -y -hwaccel auto -i $in -vcodec libx264 -crf 24 -preset ultrafast -acodec aac -strict experimental $out`
Output : 1.mp4
Durée de compression : 0:02:07.669944

Commande : `ffmpeg -y -hwaccel vdpau -i $in -vcodec libx264 -crf 24 -preset ultrafast -acodec aac -strict experimental $out`
Output : 2.mp4
Durée de compression : 0:02:07.694151

Commande : `ffmpeg -y -hwaccel cuda -i $in -vcodec libx264 -crf 24 -preset ultrafast -acodec aac -strict experimental $out`
Output : 3.mp4
Durée de compression : 0:02:08.010994

Commande : `ffmpeg -y -hwaccel vaapi -i $in -vcodec libx264 -crf 24 -preset ultrafast -acodec aac -strict experimental $out`
Output : 4.mp4
Durée de compression : 0:02:07.822563

Commande : `ffmpeg -y -hwaccel opencl -i $in -vcodec libx264 -crf 24 -preset ultrafast -acodec aac -strict experimental $out`
Output : 5.mp4
Durée de compression : 0:02:07.862492

Commande : `ffmpeg -y -hwaccel cuvid -i $in -vcodec libx264 -crf 24 -preset ultrafast -acodec aac -strict experimental $out`
Output : 6.mp4
Durée de compression : 0:02:07.627818

Preset `superfast`
---

Commande : ffmpeg -y -i $in -vcodec libx264 -crf 28 -preset superfast -acodec aac -strict experimental $out
Output : 7.mp4
Durée de compression : 0:03:03.484591

Commande : ffmpeg -y -hwaccel auto -i $in -vcodec libx264 -crf 28 -preset superfast -acodec aac -strict experimental $out
Output : 8.mp4
Durée de compression : 0:03:03.322291

Commande : ffmpeg -y -hwaccel vdpau -i $in -vcodec libx264 -crf 28 -preset superfast -acodec aac -strict experimental $out
Output : 9.mp4
Durée de compression : 0:03:02.919410

Commande : ffmpeg -y -hwaccel cuda -i $in -vcodec libx264 -crf 28 -preset superfast -acodec aac -strict experimental $out
Output : 10.mp4
Durée de compression : 0:03:03.055836

Commande : ffmpeg -y -hwaccel vaapi -i $in -vcodec libx264 -crf 28 -preset superfast -acodec aac -strict experimental $out
Output : 11.mp4
Durée de compression : 0:03:03.217776

Commande : ffmpeg -y -hwaccel opencl -i $in -vcodec libx264 -crf 28 -preset superfast -acodec aac -strict experimental $out
Output : 12.mp4
Durée de compression : 0:03:03.223981

Commande : ffmpeg -y -hwaccel cuvid -i $in -vcodec libx264 -crf 28 -preset superfast -acodec aac -strict experimental $out
Output : 13.mp4
Durée de compression : 0:03:04.243322

Conclusion
===
Aucun changement significatif (ni sur les fichiers - encore heureux, ni sur le temps d'exécution) : c'était une fausse piste. D'après la documentation, l'accélération matérielle n'est utilisée que pour le décodage du fichier d'input, ce qui nous donne très peu de différences ici.

