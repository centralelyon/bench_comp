#Premiers résultats.
Résultats des premiers tests de l'algo de benchmark des réglages de compression. Rien de très nouveau.

Commande :  ffmpeg -y -i $in $out
On change juste le conteneur d'origine (.mov) en .mp4
Ratio de compression :  0.09768730057946123
Durée de compression :  535.7346895570008

Commande :  ffmpeg -y -i $in -vcodec libx264 -crf 24 $out
On change en plus le codec d'origine (Apple ProRes 4:2:2) en H.264 également en 4:2:2. -crf permet de fixer le bitrate en fonction de la qualité souhaitée.
Ratio de compression :  0.07630265646395028
Durée de compression :  536.4093951519972

Commande :  ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset ultrafast -acodec aac -strict experimental $out
Idem, sauf qu'en plus on applique un preset. Voir x264 --fullhelp pour voir l'ensemble des options de ce preset. Permet de beaucoup baisser le temps de compression !
Ratio de compression :  0.14666485296967077
Durée de compression :  129.9278661850003
