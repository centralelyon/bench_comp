Tests du paramètre `-preset superfast`
===
On vient donc de trouver des valeurs du facteur de qualité `-crf` impactant le bitrate de la vidéo permettant d'avoir un taux de compression compris entre 15% (pour `-crf 24`) et 7.5% (pour `-crf 28`), avec la commande suivante :

`ffmpeg -y -i $in -vcodec libx264 -crf **n** -preset ultrafast -acodec aac -strict experimental $out`

Dans cette commande, le preset `ultrafast` permet de largement réduire le temps d'encodage (on passait de 8:56 à 2:10 en `-crf 24`). Cependant, en lisant la documentation de H.264, on se rend compte que ce preset saute de nombreuses étapes de compression :
- `--no8x8dct` : pas de _direct cosine transform_ (similaire à une TF) permettant de compresser une photo en écrétant les plus hautes fréquences spatiales (qui correspondent aux plus petits détails)
- `--bframes 0` : aucune B-frame, frames recalculées à partir des frames précédentes _et_ suivantes. En utilisant des B-frames, on baisse encore la taille du fichier, en contrepartie, la lecture est plus gourmande en puissance de calcul
- `--b-adapt 0` : puisqu'on produit pas de B-frames, pas besoin de choisir une méthode pour décider quelles frames seront des B-frames
- `--no-cabac` : on désactive l'algorithme de codage adaptable au contexte, qui permet d'optimiser la compression (notamment de compresser **sans perte**!), au prix de plus de temps à l'encodage

Le preset `superfast` rétablit ces réglages et les automatise. On teste alors pour les facteurs de qualités retenus précédemment dans le benchmark les différences en ratio et durée de compression entre les presets `ultrafast` et `superfast`. On regarde aussi les différences visibles sur les vidéos et les frames.

Exécution (dossier _preset_)
---
Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset ultrafast -acodec aac -strict experimental $out`
Output : 0.mp4
Durée de compression : 0:02:08.011083
Ratio de compression : 0.14666485296967077

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset superfast -acodec aac -strict experimental $out`
Output : 1.mp4
Durée de compression : 0:03:11.099387
Ratio de compression : 0.09593845225405452

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 26 -preset ultrafast -acodec aac -strict experimental $out`
Output : 2.mp4
Durée de compression : 0:01:54.289559
Ratio de compression : 0.09210487925625988

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 26 -preset superfast -acodec aac -strict experimental $out`
Output : 3.mp4
Durée de compression : 0:03:06.426529
Ratio de compression : 0.06193442069464627

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 28 -preset ultrafast -acodec aac -strict experimental $out`
Output : 4.mp4
Durée de compression : 0:01:51.493844
Ratio de compression : 0.06761785136847867

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 28 -preset superfast -acodec aac -strict experimental $out`
Output : 5.mp4
Durée de compression : 0:03:03.354804
Ratio de compression : 0.039225688527287035

**Exécution** Ces premiers résultats nous montrent que, à facteur de qualité égal, on obtient un meilleur ratio de compression (entre 55% et 66% du ratio obtenu avec `ultrafast`) car les étapes listées en intro ne sont plus sautées, et ces étapes permettent une meilleure compression. En contrepartie, il faut compter 50% de temps de compression supplémentaire à chaque fois en passant d'`ultrafast` à `superfast`. Ce n'est pas forcément dérangeant puisqu'il ne faut faire la compression qu'une seule fois à l'importation des captations, et parce que le gain de place est significatif.

**1ères frames** Visuellement la différence est vraiment marquante : les frames issues de vidéos compressées en `superfast` sont de bien meilleure qualité que celles des `ultrafast`. C'est ce qu'on remarque également en regardant le poids des frames reconstruites : 33.6 Mo _vs_ 21.7 Mo. Les DCT, les B frames et CABAC permettent d'obtenir des vidéos de plus petite taille, qui une fois décodées sont en réalité plus grandes (plus de détails, meilleure qualité visuelle). Ces résultats visuels nous permettront d'appliquer un ratio `crf` plus grand que 28 en preset `superfast` pour davantage gagner en espace tout en ayant des meilleurs résultats qu'avec `-crf 24 -preset ultrafast`.

**Vidéos** Visuellement, on dirait qu'il y a un grain sur l'image des vidéos encodées en `ultrafast` qu'on ne retrouve pas en `superfast` : il y a comme un lissage (permis par la DCT ?), qui adoucit l'image. Les vidéos encodées en `superfast` et en `ultrafast` mettent autant de temps à s'ouvrir. En revanche, une vidéo `superfast` charge moins longtemps lorsqu'on se déplace arbitrairement loin dans la vidéo (**attention** test qualitatif, dépend peut-être de mon matériel et de ce qui est déjà en mémoire/en swap).

Conclusion
---
Si l'on a le temps (50% de temps d'encodage en plus) et les performances suffisantes (pas de grande différence, mais à quantifier), il est beaucoup plus intéressant de passer en preset `superfast`, car les images sont de bien meilleure qualité et que les fichiers pèsent encore moins lourd.
