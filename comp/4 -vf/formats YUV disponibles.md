Issu de `ffmpeg -pix_fmts`. J'ai elevé tous les formats qui n'étaient pas YUV (y compris les formats UYVY, YVYU, YUY2, etc.) et les YUVA (avec un canal alpha pour gérer la transparence). Les YUVJ sont presque comme les YUV, la seule différences est dans leur plage de valeur : sur 8 bits, YUVJ fait 0-255 et YUV 16-240 pour mieux coller à l'analogique (NB : c'est pas gênant que les composantes U et V soient comprises entre 16 et 240 car dans tous les cas le gamut (le domaine de l'espace des couleurs) affichable de la plupart des écrans ne recouvre pas toute le domaine \[0,255\]x\[0,255\]).

FLAGS NAME            NB\_COMPONENTS BITS\_PER\_PIXEL
-----
*IO... yuv420p                3            12*
*IO... yuv422p                3            16*
IO... yuv444p                3            24
IO... yuv410p                3             9
IO... yuv411p                3            12

IO... yuvj420p               3            12
IO... yuvj422p               3            16
IO... yuvj444p               3            24
IO... yuv440p                3            16
IO... yuvj440p               3            16

IO... yuv420p16le            3            24
IO... yuv420p16be            3            24
IO... yuv422p16le            3            32
IO... yuv422p16be            3            32
IO... yuv444p16le            3            48
IO... yuv444p16be            3            48

IO... yuv420p9be             3            13
IO... yuv420p9le             3            13
IO... yuv420p10be            3            15
*IO... yuv420p10le            3            15*
IO... yuv422p10be            3            20
**IO... yuv422p10le            3            20**    format de captation
IO... yuv444p9be             3            27
IO... yuv444p9le             3            27
IO... yuv444p10be            3            30
IO... yuv444p10le            3            30
IO... yuv422p9be             3            18
IO... yuv422p9le             3            18

IO... yuv420p12be            3            18
IO... yuv420p12le            3            18
IO... yuv420p14be            3            21
IO... yuv420p14le            3            21
IO... yuv422p12be            3            24
IO... yuv422p12le            3            24
IO... yuv422p14be            3            28
IO... yuv422p14le            3            28
IO... yuv444p12be            3            36
IO... yuv444p12le            3            36
IO... yuv444p14be            3            42
IO... yuv444p14le            3            42
IO... yuv440p10le            3            20
IO... yuv440p10be            3            20
IO... yuv440p12le            3            24
IO... yuv440p12be            3            24
