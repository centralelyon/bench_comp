# bench_comp

Benchmark de différentes techniques de compression pour gagner de l'espace sur le pipeline et pas trop perdre de temps lors du traitement.

Intro : pourquoi ce benchmark ?
---
Lors des captations, on filme avec les réglages suivants :
- résolution 4096 × 2160 (DCI 4K)
- 50 images/s pour pouvoir faire des analyses temporelles fines des mouvements des nageurs
- avec le codec (cf. explications sur Trello) Apple ProRes
- en échantillonnage colorimétrique 4:2:2

Ceci donne un très bon rendu visuel, mais une minute de vidéo avec ces paramètres pèse de l'ordre de 2.5 Go. Il faut donc compresser les vidéos si on souhaite (entre autres) :
- avoir des vidéos sur sa propre machine
- uploader rapidement les vidéos sur la pipeline
- traiter plus rapidement les vidéos : les logiciels de tracking tourneront plus lentement avec des trop gros fichiers

On souhaite alors savoir comment compresser nos vidéos (quels réglages, pour quels rendus ?).

Notre outil : `ffmpeg`
---
Nous utiliserons le programme `ffmpeg` disponble en CLI sur les systèmes Unix (natif Linux, dispo avec Conda sur macOS), qui permet de manipuler des fichiers multimédia (ajouter, supprimer des canaux, modifier les codecs, les conteneurs, etc.)

Méthode
---
Ce repo propose un algorithme permettant d'exécuter dans un shell Unix une liste de commandes ffmpeg et de mesurer le temps pris et le ratio de compression. Nous testons différents réglages d'abord un par un, puis ensuite en les combinant jusqu'à trouver une compression qui nous paraisse optimale.

Résultats globaux
===
**Des résultats plus détaillés (avec images) sont disponibles dans les dossiers de chaque test**

H.264
---
On commence par passer du codec ProRes à H.264 : 

`ffmpeg -y -i $in -vcodec libx264 -crf 24 $out`

La commande ne s'exécute pas assez rapidement, on utilise alors un preset du codec H.264 qui enlève des étapes (cf. `x264 --fullhelp` pour plus d'infos) pendant l'encodage :

`ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset ultrafast -acodec aac -strict experimental $out`

Le bitrate
---

Dans cette commande,`-crf n` représente un facteur de qualité, compris entre 0 (lossless) et 51. On teste différentes valeurs. La convention actuelle, 24 nous donne de très bons résultats : qualité largement exploitable pour un rapport de compression de l'ordre de 15%. On se rend compte que jusqu'à 28 (rapport 7%) la qualité est encore très bonne.

Le preset `ultrafast` rend l'encodage beaucoup plus court, mais il inclut des réglages qui limitent la compression. On réalise des tests pour voir si le réglage de rapidité inférieure permet d'améliorer la compression :

`ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset superfast -acodec aac -strict experimental $out`

Le preset
---
On se rend compte que le preset `ultrafast`, pour gagner du temps à l'encodage, saute de nombreuses étapes de compression (listées dans les résultats du benchmark du preset). Passer en preset `superfast` permet à la fois de gagner en espace occupé (le ratio de compression en `superfast` vaut 55% à 66% ce qu'il vaut en `ultrafast`) et en qualité visuelle (cf. photos ici dans le repo et les vidéos sur le pipeline), au prix d'un temps d'encodage plus long (environ 50% de plus).

TODO :
- sous échantillonnage colorimétrique avec crf 24 et crf opti
- h.265
