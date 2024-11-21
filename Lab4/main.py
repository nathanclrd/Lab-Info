import math
import pygame
import sys

# Constantes

NOIR = (0, 0, 0)
ROUGE = (255,0,0)
ORANGE = (255,120,0)
JAUNE = (255,255,0)
GRIS = (188,196,198)

MASSE_VAISSEAU = 1
F_POUSSEE = 0.0003 #tonne*px/ms
G = 0.001

# Paramètres
LARGEUR_FENETRE = 800
HAUTEUR_FENETRE = 600
dimensions_fenetre = (LARGEUR_FENETRE, HAUTEUR_FENETRE)  # en pixels
images_par_seconde = 25

# Initialisation

pygame.init()

fenetre = pygame.display.set_mode(dimensions_fenetre,pygame.RESIZABLE)
pygame.display.set_caption("Programme 7")

horloge = pygame.time.Clock()
couleur_fond = NOIR
position_vaisseau = [dimensions_fenetre[0]//2,dimensions_fenetre[1]//2]
position_planete = []

orientation_vaisseau = 0

compteur_propulseur = 0

collision = False
planete_est_presente = False

def afficher_vaisseau():
   pygame.draw.circle(fenetre,ROUGE,position_vaisseau,15)

def dessiner_triangle(couleur,p,r,a,b):
   p1 = (position_vaisseau[0]+r*math.cos(b+a),position_vaisseau[1]+r*math.sin(b+a))
   p2 = (position_vaisseau[0]+r*math.cos(a-b),position_vaisseau[1]+r*math.sin(a-b))
   pygame.draw.polygon(fenetre,couleur,[p,p1,p2])

def afficher_planete(position_planete,planete_est_presente):
   global MASSE_PLANETE


   if planete_est_presente:
      MASSE_PLANETE = 1600
      planete = pygame.draw.circle(fenetre,GRIS,position_planete,40)

   else:
      MASSE_PLANETE = 0
      return

def gerer_touche(key):
   global orientation_vaisseau,compteur_propulseur,temps_maitenant,moteur_allume

   if key.key == pygame.K_LEFT:
      orientation_vaisseau -= math.pi/20
   if key.key == pygame.K_RIGHT:
      orientation_vaisseau += math.pi/20
   if key.key == pygame.K_UP:
      moteur_allume = True
      compteur_propulseur +=3

def gerer_bouton(button):
   global planete_est_presente,position_planete
   if button.button ==1:
      planete_est_presente = True
      position_planete = pygame.mouse.get_pos()
   else:
      planete_est_presente = False
   return


def init_variable():
   global vx,vy,temps,ax,ay
   ax = 0
   ay = 0
   vx =0
   vy = 0
   temps =0

def afficher_vaisseau():
   pygame.draw.circle(fenetre,ROUGE,position_vaisseau,15)
   coord_x = position_vaisseau[0] + 15 * math.cos(orientation_vaisseau)

afficher_vaisseau()
def mettre_a_jour_position(position_vaisseau, temps_maintenant, MASSE_VAISSEAU, F_POUSSEE, orientation_vaisseau, MASSE_PLANETE, position_planete):
    global vx, vy, temps, G, planete_est_presente
    delta_t = (temps_maitenant-temps)
    ax, ay = 0, 0

    if compteur_propulseur > 0:

        acceleration = F_POUSSEE / MASSE_VAISSEAU
        ax = acceleration * math.cos(orientation_vaisseau)
        ay = acceleration * math.sin(orientation_vaisseau)

    if position_vaisseau[0] <= 0:
        position_vaisseau[0] = LARGEUR_FENETRE
    elif position_vaisseau[0] >= LARGEUR_FENETRE:
        position_vaisseau[0] = 0
    if position_vaisseau[1] <= 0:
        position_vaisseau[1] = HAUTEUR_FENETRE
    elif position_vaisseau[1] >= HAUTEUR_FENETRE:
        position_vaisseau[1] = 0

    if planete_est_presente:
        dx = position_planete[0] - position_vaisseau[0]
        dy = position_planete[1] - position_vaisseau[1]
        distance = math.sqrt(dx**2 + dy**2)

        force_g = (G * MASSE_VAISSEAU * MASSE_PLANETE) / (distance ** 2)
        acceleration_gravite = force_g / MASSE_VAISSEAU


        angle = math.atan2(dy, dx)
        ax += acceleration_gravite*math.cos(angle)
        ay += acceleration_gravite*math.sin(angle)

    vx += ax * delta_t
    vy += ay * delta_t

    position_vaisseau[0] += vx * delta_t + (ax * delta_t**2) / 2
    position_vaisseau[1] += vy * delta_t + (ay * delta_t**2) / 2

    temps = temps_maitenant
    
def test_colision(p1,r1,p2,r2):
   global collision

   if math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)<= r1+r2:
      collision= True
   return collision




pygame.key.set_repeat(10, 10)

init_variable()
while True:
   LARGEUR_FENETRE,HAUTEUR_FENETRE = fenetre.get_size()
   temps_maitenant = pygame.time.get_ticks()   
   for evenement in pygame.event.get():
      if evenement.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
      elif evenement.type == pygame.KEYDOWN:
         gerer_touche(evenement)
      elif evenement.type == pygame.MOUSEBUTTONDOWN:
         gerer_bouton(evenement)
   

   fenetre.fill(couleur_fond)
   
   
   if compteur_propulseur != 0:
        dessiner_triangle(JAUNE, position_vaisseau, 38, orientation_vaisseau + (21 * math.pi) / 20, math.pi / 30)
        dessiner_triangle(JAUNE, position_vaisseau, 38, orientation_vaisseau + (19 * math.pi) / 20, math.pi / 30)



   dessiner_triangle(ORANGE,position_vaisseau,23,orientation_vaisseau+math.pi,(math.pi)/7)
   afficher_vaisseau()
   
   afficher_planete(position_planete,planete_est_presente)
   if planete_est_presente:
      test_colision(position_planete,40,position_vaisseau,15)
      if collision:
         pygame.quit()
         sys.exit()
   mettre_a_jour_position(position_vaisseau,temps_maitenant,MASSE_VAISSEAU,F_POUSSEE,orientation_vaisseau,MASSE_PLANETE,position_planete)

   pygame.display.flip()
   compteur_propulseur =0

   horloge.tick(images_par_seconde)


