# Projet Challenge laser

Ce projet permet de tester l'envoi et la réception de n'importe quel type de fichier entre deux Raspberry Pi à l'aide d'une paire d'émetteur et de récepteur laser.

## Organisation

```
Rapport
 . rapport.pdf : rapport du projet contenant les notices de montage des deux Raspberry
src
 . python
 . . align : permet d'aligner le laser avec le récepteur
 . . . tx.py
 . . . rx.py
 . . data : permet l'échange de fichiers de tout type
 . . . tx.py
 . . . rx.py
 . . detect : permet de détecter sur quelle Raspberry le laser est connecté
 . . . detect.py
 . . module : renvoie les vitesses utilisables
 . . . baudrate.py
 . . text : permet l'échange de fichiers au format texte (ASCII)
 . . . tx.py
 . . . rx.py
 . hybrid : solution utilisant du C et du python, 
            permet l'échange de fichiers de tout type à une vitesse plus élevée
 . . tx.py
 . . rx.py
 . . rx.c
 . . Makefile
test : différents fichiers pour tester la transmission de fichiers
 . 1000x1000.bmp
 . 100x100.bmp
 . 150x150.bmp
 . 200x200.bmp
 . 250x250.bmp
 . 300x300.bmp
 . 350x350.bmp
 . 400x400.bmp
 . 40x40.bmp
 . bigtext.txt
 . default.txt
 . mountain.jpg
old : sources de l'ancien projet
```

## Prérequis

Attention, veuillez toujours lancer un script depuis le répertoire où il se situe.

* Brancher correctement l'émetteur et le récepteur (cf rapport.pdf)
* Savoir quelle raspberry émet (detect.py fait clignoter le laser de celle-ci si tel est le cas)
* Les aligner (avec les programmes situés dans le dossier align)

## Utilisation

* Aller dans le répertoire des scripts que l'on désire tester.
* Lancer le script rx.py avec un certain baud rate sur la carte réceptrice.
* Dans le cas d'hybrid, compiler d'abord rx.c (make rx).
* Lancer le script tx.py avec le baud rate et le fichier à envoyer en argument sur la carte émettrice.
* Suivre alors les instructions des différents scripts.

## Limites

* Il est très difficile d'aligner le laser pour un baud rate de 13 ou plus.
* Les scripts en python pure ne fonctionneront pas pour un baud rate de 12 ou plus.
* Le programme hybride ne fonctionnera pas pour un baud rate de 14 ou plus.

## Baud rates utilisés
```
[1] 110
[2] 1200
[3] 2400
[4] 9600
[5] 14400
[6] 19200
[7] 38400
[8] 57600
[9] 76800
[10] 115200
[11] 230400
[12] 460800
[13] 921600
```
## Auteurs 

PR311 - Développement système
Année universitaire 2017 - 2018

Projet de transfert de fichier par laser
Louis Deguillaume, Nathan Nguyen, Adrien Rodrigues
