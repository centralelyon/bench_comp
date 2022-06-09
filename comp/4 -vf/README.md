Tests du sous-échantillonnage colorimétrique
===
On cherche encore une fois à baisser la taille de nos fichiers. Cette fois-ci, on va exploiter une propriété de nos yeux : on est beaucoup plus sensible à la luminosité qu'aux couleurs.

Concrètement, on va changer de base de représentation de nos couleurs : au lieu d'être en RGB (rouge, vert, bleu), on va travailler en YUV, une autre base de l'espace des couleurs :
- Y ≈ R+G+B est la luminance (contient toutes les informations de luminosité, donne une image en niveaux de gris
- U ≈ B-Y est la chrominance bleue (donne une image bleue-verte)
- V ≈ R-Y est la chrominance rouge (donne une image rouge-verte)

Une fois cette conversion effectuée, on peut, en gardant la même résolution sur Y et en baissant les résolutions de U et de V (sous-échantillonnage), obtenir un rendu indiscernable à l'oeil nu. Pour quantifier l'échantillonnage, on utilise le codage A:B:C, qui décrit ce qu'on fait sur une zone de A pixels de large et 2 pixels de haut. B et C représentent le nombre d'échantillons de chrominance sur la 1ère et la 2è ligne. On retrouve principalement les conventions suivantes :
- 4:4:4 : on a 4 échantillons de Y et 4 échantillons de U et de V sur chaque ligne = 0 sous-échantillonnage. On garde l'information brute (coûteux en espace).
- 4:2:2 : pour 4 échantillons de Y par ligne, on en a que 2 de U et V sur chaque ligne = on a divisé la résolution horizontale de chrominance par 2. Réduit de 33% le débit par rapport au 4:4:4. **On filme actuellement comme ça nos captations**
- 4:2:0 : on n'a aucun échantillon de chrominance sur la 2è ligne, à la place on duplique l'information de chrominance de la 1ère ligne sur la 2è = on a divisé les résolutions horizontales et verticales de la chrominance par 2. Réduit de 50% le débit par rapport au 4:4:4
- 4:1:1 : on prend un échantillon de U et de V par ligne. On garde la même résolution verticale mais on divise la résolution horizontale par 4. Réduit de 50% le débit par rapport au 4:4:4

Il faut aussi penser au nombre de bits sur lesquels on code chaque composante Y, U, V (et donc ensuite à l'affichage chaque composante R, G, B). Actuellement lors des captations, on filme en 10 bits par composante. Ainsi, en 4:2:2 10-bit, on code chaque pixel en moyenne sur 20 bits (en prennant en compte la division par 2 de la résolution horizontale de U et V).

On va donc passer notre vidéo test du 4:2:2 10-bit au au 4:2:2 8-bit (16 bits/pixel), au 4:2:0 10-bit (15 bits/pixel), au 4:2:0 8-bit (12 bits/pixel) et au 4:1:1 8-bit (12 bits/pixel) pour nos commandes usuelles (presets `ultrafast` et `superfast` avec `-crf` 24). On teste quantitativement les gains de ratio et durée de compression, et on regarde aussi les différences visibles sur les vidéos et les frames.

Exécution (dossier _vf_)
===
Pour `ultrafast`
---

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset ultrafast -acodec aac -strict experimental $out` idem que $in : **4:2:2 10-bit**
Output : 0.mp4
Durée de compression : 0:02:09.096690
Par rapport à la durée : 0.7745181790856747
Ratio de compression : 0.14666485296967077

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset ultrafast -vf format=yuv422p -acodec aac -strict experimental $out` **4:2:2 8-bit**
Output : 1.mp4
Durée de compression : 0:02:53.923605
Par rapport à la durée : 1.0434581537797036
Ratio de compression : 0.14066335093076895

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset ultrafast -vf format=yuv420p10le -acodec aac -strict experimental $out` **4:2:0 10-bit**
Output : 2.mp4
Durée de compression : 0:03:04.790689
Par rapport à la durée : 1.1086554417026564
Ratio de compression : 0.11594908332951012

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset ultrafast -vf format=yuv420p -acodec aac -strict experimental $out` **4:2:0 8-bit**
Output : 3.mp4
Durée de compression : 0:02:29.585413
Par rapport à la durée : 0.8974406798236192
Ratio de compression : 0.11849783699175315

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset ultrafast -vf format=yuv411p -acodec aac -strict experimental $out` **4:1:1 8-bit**
Output : 4.mp4
Durée de compression : 0:03:29.294054
Par rapport à la durée : 1.2556638691564719
Ratio de compression : 0.13535018476454416

Pour `superfast`
---

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset superfast -acodec aac -strict experimental $out` idem que $in : **4:2:2 10-bit**
Output : 5.mp4
Durée de compression : 0:03:14.166256
Par rapport à la durée : 1.1649043462982953
Ratio de compression : 0.09593845225405452

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset superfast -vf format=yuv422p -acodec aac -strict experimental $out` **4:2:2 8-bit**
Output : 6.mp4
Durée de compression : 0:03:15.802814
Par rapport à la durée : 1.174722905147597
Ratio de compression : 0.10036851892230592

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset superfast -vf format=yuv420p10le -acodec aac -strict experimental $out` **4:2:0 10-bit**
Output : 7.mp4
Durée de compression : 0:03:43.946542
Par rapport à la durée : 1.3435717665466713
Ratio de compression : 0.07840255478110633

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset superfast -vf format=yuv420p -acodec aac -strict experimental $out` **4:2:0 8-bit**
Output : 8.mp4
Durée de compression : 0:02:49.448795
Par rapport à la durée : 1.0166114412587017
Ratio de compression : 0.08105003499398802

Commande : `ffmpeg -y -i $in -vcodec libx264 -crf 24 -preset superfast -vf format=yuv411p -acodec aac -strict experimental $out` **4:1:1 8-bit**
Output : 9.mp4
Durée de compression : 0:03:56.054259
Par rapport à la durée : 1.4162122576493976
Ratio de compression : 0.09806480196690982

**Exécution** On observe généralement un gain de place pour la plupart de nos réglages, à part quand on passe de 10 bits par couche à 8 en 4:2:2. Certaines conversions ont l'air de rallonger la durée de conversion.

**1ères frames** Visuellement, avec un écran de bureau standard en profil d'écran Adobe RGB 1998, on ne remarque pas de différence notable entre les frames tirées des vidéos issues du même preset, à part le fait que les frames des 8 bits ont l'air plus sombre que celles des 10 bits, mais rien de très marqué. En revanche, on observe que les images PNG reconstruites à partir des frames de vidéos en 8 bits sont bien plus petites que celles des 10 bits. On peut donc espérer un gain de performances à la lecture/à l'analyse par nos modèles.

**Vidéos** On ne voit aucune différence entre les vidéos issues du même preset, à part la très légère différence de luminosité constatée sur les frames.

Conclusion
===
- le sous-échantillonnage permet à chaque fois d'obtenir des fichiers de plus petite taille. C'est plus marqué pour le passage 4:2:2 vers 4:2:0 que pour 4:2:2 vers 4:1:1.
- contrairement à l'intuition, baisser le nombre de bits de codage des couleurs ne baisse pas l'espace occupé par le flux vidéo
  - il semble plus intéressant de rester sur le même nombre de bits (ici, 10) pour avoir le minimum de débit
  - passer en 4:2:2 sur 8 bits (donc pas de sous-échantillonnage) donne sensiblement la même taille de fichier, alors qu'on passe de 20 bits/pixel à 16, et augmente même la taille pour le preset `superfast`
- sinon, le profil 4:2:0 8-bit permet de compresser dans un temps similaire à si l'on ne fait pas de sous-échantillonnage

On retiendra :
- pour gagner de l'espace, passer en 4:2:0 10-bit `-vf format=yuv420p10le`
- pour ne pas prendre plus de temps (en compression et à la lecture), passer en 4:2:0 8-bit `-vf format=yuv420p`

