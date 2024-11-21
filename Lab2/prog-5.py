# ------------------------------------------------------------------------
# Laboratoires de programmation mathÃ©matique et physique 1                
# ------------------------------------------------------------------------
# 
# Programme 5: Vecteurs vitesse et accÃ©lÃ©ration, dÃ©tection de gestes.
#
# *** CONSIGNES ***: Ne modifier que les fonctions
#                        deplacer_pol(),
#                        dessiner_vecteur(),
#                        initialiser_calculs(),
#                        calculer_vitesse_acceleration_2d() et
#                        detecter_geste()  !!!
#
# ------------------------------------------------------------------------

import math
import pygame
import sys

### Constante(s)

BLEU = (0, 0, 255)
JAUNEMIEL = (255, 192, 0)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)

A = 2
B = 5
C = 20

### Fonctions

# *** A MODIFIER *********************************************************

def deplacer_pol(point, distance, orientation):
    x, y = point
    x2,y2 = x + distance*math.cos(orientation),y + distance*math.sin(orientation)
    return (x2, y2)

# *** A MODIFIER *********************************************************

def dessiner_vecteur(fenetre, couleur, origine, vecteur):
    distance_pp4 = math.sqrt((vecteur[1]**2 + vecteur[0]**2))
    angle = math.atan2(vecteur[1],vecteur[0])
    if distance_pp4 > C :
        
        p4 = (vecteur[0]+origine[0],vecteur[1]+origine[1])
        p1= deplacer_pol(origine,A,angle-math.pi/2)
        p7= deplacer_pol(origine,A,angle+math.pi/2)
        p2 = deplacer_pol(p1,distance_pp4-C,angle)
        p6 = deplacer_pol(p7,distance_pp4-C,angle)
        p3 = deplacer_pol(p2,B,angle-math.pi/2)
        p5 = deplacer_pol(p6,B,angle+math.pi/2)
        polygone = [p1,p2,p3,p4,p5,p6,p7]
        pygame.draw.polygon(fenetre, couleur, polygone)

    else:
        p3 = (vecteur[0]+origine[0],vecteur[1]+origine[1])
        p1 = deplacer_pol(p3,C,angle+math.pi)
        p2 = deplacer_pol(p1,A+B,angle-math.pi/2)
        p4 = deplacer_pol(p1,A+B,angle+math.pi/2)
        polygone= [p1,p2,p3,p4]
        pygame.draw.polygon(fenetre, couleur, polygone)

    return 

# *** A MODIFIER *********************************************************

def initialiser_calculs():#P5-1
    global temps,vitesse_init,position_init
    temps = 0
    position_init = (0,0)
    vitesse_init = (0,0)
    return 

# *** A MODIFIER *********************************************************

def calculer_vitesse_acceleration_2d(position, temps_maintenant): #P5-1
    global position_init,temps,vitesse_init
    vx = (position[0]-position_init[0])/(temps_maintenant-temps)
    vy = (position[1]-position_init[1])/(temps_maintenant-temps)
    ax = (vx-vitesse_init[0])/(temps_maintenant-temps)
    ay =(vy-vitesse_init[1])/(temps_maintenant-temps)
    vitesse_init = (vx,vy)
    position_init = position
    temps = temps_maintenant

    return (vx,vy),(ax,ay)

# *** A MODIFIER *********************************************************

def detecter_geste(vitesse, acceleration): #P5-2
    if math.sqrt(vitesse[0]**2 + vitesse[1]**2)<0.2:
        angle = math.atan2(acceleration[1],acceleration[0])
        if math.sqrt(acceleration[0]**2+acceleration[1]**2)>0.002 and math.radians(90+10) >= angle and angle<= math.radians(90-10) and math.radians(-90-10) <= angle and math.radians(-90+10) >= angle:
            return True
    return False

# ************************************************************************

def afficher_compteur():
    image = police.render(str(compteur), True, NOIR)
    fenetre.blit(image, (50, 50))
    return

def amortir(v, ancien_v, coefficient):
    return (ancien_v[0] * coefficient + v[0] * (1.0 - coefficient),
            ancien_v[1] * coefficient + v[1] * (1.0 - coefficient))

def traiter_mouvement(position):
    global premier_mouvement, ancienne_position, ancienne_acceleration
    global compteur, derniere_detection

    if premier_mouvement:
        premier_mouvement = False
    else:
        x, y = position
        
        # Amortissement pour lisser les mouvements.
        position = amortir(position, ancienne_position,
                           amortissement_position)

        t = pygame.time.get_ticks()
        v, a = calculer_vitesse_acceleration_2d(position, t)

        a = amortir(a, ancienne_acceleration, amortissement_acceleration)
        ancienne_acceleration = a

        if detecter_geste(v, a) and t > derniere_detection + 500:
            compteur += 1
            derniere_detection = t
            
        fenetre.fill(couleur_fond)

        afficher_compteur()
        
        pygame.draw.circle(fenetre, BLEU,
                           (int(position[0]), int(position[1])), 20)

        if doit_afficher_vitesse:
            dessiner_vecteur(fenetre, ROUGE, position,
                             (int(v[0] * facteur_vitesse),
                              int(v[1] * facteur_vitesse)))

        if doit_afficher_acceleration:
            dessiner_vecteur(fenetre, VERT, position,
                             (int(a[0] * facteur_acceleration),
                              int(a[1] * facteur_acceleration)))
            
        pygame.display.flip()

    ancienne_position = position        
    return

### ParamÃ¨tre(s)

dimensions_fenetre = (800, 600)  # en pixels
images_par_seconde = 25

couleur_fond = JAUNEMIEL

amortissement_position = 0.7
amortissement_acceleration = 0.5
facteur_vitesse = 200
facteur_acceleration = 40000

### Programme

# Initialisation

pygame.init()

fenetre = pygame.display.set_mode(dimensions_fenetre)
pygame.display.set_caption("Programme 5");

horloge = pygame.time.Clock()
police  = pygame.font.SysFont("monospace", 36)

premier_mouvement = True

ancienne_acceleration = (0.0, 0.0)

doit_afficher_vitesse = True
doit_afficher_acceleration = True

compteur = 0

derniere_detection = -1000

fenetre.fill(couleur_fond)
pygame.display.flip()

# Boucle principale

initialiser_calculs()

while True:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_a:
                doit_afficher_acceleration = not doit_afficher_acceleration
            elif evenement.key == pygame.K_v:
                doit_afficher_vitesse = not doit_afficher_vitesse

    traiter_mouvement(pygame.mouse.get_pos())        
    horloge.tick(images_par_seconde)