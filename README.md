# Auteurs 

PR311 - Développement système
Année universitaire 2016 - 2017

Projet de transfert de fichier par laser
Herve Perin, Romain Petro, Mathieu Petit

# Prérequis
Il faut lancer le programme de réception avant le programme d'émission.


# Récepteur

Pour lancer le programme de réception :
`sudo python rcpt.py`

Dans un premier temps, le programme récupère la séquence de synchronisation et calcul son horloge en fonction. Puis, les trames sont reçues. A la fin de leur réception, le programme annalyse les trames et détecte les erreurs. Puis, il reconstruit le fichier à partir des trames valides et l'écrit sur le disque en lui donnant le nom "output.txt".

# Emetteur

Pour lancer le programme d'émission :
`sudo python em.py fileASCII.txt [nb_duplication [taille_charge_utile_en_octet [fréquence [temps_de_pause_entre_chaque_trame]]]]`

Dans un premier temps, le programme ouvre le fichier à transmettre, le
charge en mémoire et prépare les trames. Ensuite, il envoit la séquence
de synchronisation au récepteur et l'ensemble des trames.

Remarque : le fichier cassoulet.txt est un exemple de fichier ASCII pouvant être transféré.

# Rapport

Le rapport concernant ce projet est dans le fichier "rapport/rapport.pdf".
