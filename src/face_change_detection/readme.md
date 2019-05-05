# suivi de visage et détection de saillance
ce projet présente un système qui permet de détecter des visages sur un flux video
et d'extraire par la suite des caracteristiques pour les classifier en 9 comportements

## dépendances 
vous devez installer les packages python 3 suivants
- numpy (1.16.2)
- matplotlib (3.0.3)
- sklearn (0.20.3)
- dlib (19.17.0)
- opencv-python (4.0.0)
- imutils (0.5.2)

vous pouvez les installer en utilisant pip \
`pip install <package-name>`

pour connaitre la version du package (par exmple dlib) \
```
import dlib
dlib.__version__
```

## Usage
```
usage: video_main.py [-h] [-v VIDEO] [-c CAMERA] [-f FILE] [-e ELASTICITY]
                     [-im INITIAL_METHOD] [-lr LEARNING_RATE] [-sig SIGMA]
                     [-dt DELTA] [-t TIME] [-r RANGE] [-d DISPLAY]

optional arguments:
  -h, --help            show this help message and exit
  
  -v VIDEO, --video VIDEO
                        chemin de la video
  
  -c CAMERA, --camera CAMERA
                        numero de la webcam
  
  -f FILE, --file FILE  
                        chemin dans lequel on sauvgarde le fichier de plotting
  
  -e ELASTICITY, --elasticity ELASTICITY
                        elasticity de la DSOM
  
  -im INITIAL_METHOD, --initial-method INITIAL_METHOD
                        methode d'initialisation de la DSOM (regular, fixed or
                        random)
  
  -lr LEARNING_RATE, --learning-rate LEARNING_RATE
                        le taux d'apprentissage de la DSOM
  
  -sig SIGMA, --sigma SIGMA
                        le parametre sigma de la DSOM
  
  -dt DELTA, --delta DELTA
                        intervale du temps entres les images prises pour les
                        traitements
  
  -t TIME, --time TIME  
                        vitesse du plotting (1 = la vitesse maximale)
  
  -r RANGE, --range RANGE
                        taille de la plage de plotting
  
  -d DISPLAY, --display DISPLAY
                        les figres de plotting a afficher - (000) n'affiche
                        aucune figure - (010) affiche la 2eme figure - (111)
                        affiche toutes les figures ...
```
