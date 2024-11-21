import math
import pygame
pygame.init()
# Constantes

JAUNEPALE = (255, 255, 192)
MAUVE = (128,64,255)
ROUGE = (255,0,0)
# Paramètres

dimensions_fenetre = (800, 600)  # en pixels
dimensions_piste = (40,30)
images_par_seconde = 25

couleur = (0, 0, 0)

# Initialisation
police  = pygame.font.SysFont("monospace", 16)



fenetre = pygame.display.set_mode(dimensions_fenetre)
pygame.display.set_caption("Programme 8")

horloge = pygame.time.Clock()
couleur_fond = JAUNEPALE
 

def fenetre_vers_piste(point_fenetre):
    x_f, y_f = point_fenetre
    x_p = (x_f-dimensions_fenetre[0]/2)*dimensions_piste[0]/dimensions_fenetre[0]
    y_p = (dimensions_fenetre[1]-y_f)*dimensions_piste[1]/dimensions_fenetre[1]
    return (x_p, y_p)

def piste_vers_fenetre(point_piste):
    x_p, y_p = point_piste
    x_f = round(((x_p*dimensions_fenetre[0])/dimensions_piste[0])+dimensions_fenetre[0]/2)
    y_f = round(-((y_p*dimensions_fenetre[1]/dimensions_piste[1])-dimensions_fenetre[1]))
    return (x_f, y_f)
def hauteur_piste(x):
    return (0.000165)*(x**4)-(0.055)*(x**2) + 5

def dessiner_piste():
    for x in range(dimensions_fenetre[0]):
        x_p,y_p = fenetre_vers_piste((x,dimensions_fenetre[1]))
        y_p = hauteur_piste(x_p)
        x_f,y_f = piste_vers_fenetre((x_p,y_p))
        pygame.draw.rect(fenetre,MAUVE,(x_f,y_f,1,dimensions_fenetre[1]-y_f))
        
        


def position_initiale_mobile():
    global position_mobile
    x0 = -dimensions_piste[0]/2
    x_mobile,y_mobile = [x0,hauteur_piste(x0)]
    position_mobile = [x_mobile,y_mobile]
    return position_mobile


def dessiner_mobile():
    pygame.draw.circle(fenetre,ROUGE,piste_vers_fenetre(position_mobile),10)

def calculer_acceleration(position_mobile):
    pos_en_m = fenetre_vers_piste(position_mobile)
    gamma = 10**-6
    acceleration = (hauteur_piste(pos_en_m[0]+gamma)-hauteur_piste(pos_en_m[0]))/gamma
    return acceleration

def pente(x):
    b = 10**(-6)
    return (hauteur_piste(x+b)-hauteur_piste(x))/b

premiere_iteration = True
def mettre_a_jour_position(position,temps_maitenant):
    global vitesse,premiere_iteration,temps_precedent_s, position_mobile,norme_v
    sigma = math.sqrt(1+pente(position[0])**2)
    u = [1/sigma,(pente(position[0])/sigma)]

    if premiere_iteration:  
        vitesse = [2*u[0], 2*u[1]]
        premiere_iteration = False
        return

    if vitesse[0]<0:
        u[0] = -u[0]
        u[1] = -u[1]


    delta_ts = temps_maitenant-temps_precedent_s
    norme_v = math.sqrt(vitesse[0]**2 +vitesse[1]**2)
    nouvelle_vitesse= [norme_v*u[0],norme_v*u[1]]
    acceleration = [(nouvelle_vitesse[0]-vitesse[0])/delta_ts,(nouvelle_vitesse[1]-vitesse[1])/delta_ts]
    vitesse[0] += delta_ts*acceleration[0]
    vitesse[1] += delta_ts*acceleration[1]
    position_mobile[0] += vitesse[0]*delta_ts
    position_mobile[1] += vitesse[1]*delta_ts
    temps_precedent_s = temps_maitenant_s

    return position_mobile

def afficher_tableau_de_bord(x,y):
    texte = "Vitesse : {0:.2f} m/s".format(norme_v)
    image = police.render(texte, True, couleur)
    fenetre.blit(image, (x, y))
    texte2 = "Vitesse max: {0:.2f} m/s".format(vmax)
    image = police.render(texte2, True, couleur)
    fenetre.blit(image, (x, y+20))

vmax = 0
def mettre_a_jour_statistiques():
    global vmax,norme_v
    if norme_v > vmax:
        vmax = norme_v


temps_precedent_ms =0
temps_precedent_s = 0
position_mobile = position_initiale_mobile()

while True:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    temps_maitenant_ms = pygame.time.get_ticks()

    for t in range(temps_precedent_ms,temps_maitenant_ms-1):
        temps_maitenant_s = t/1000
        mettre_a_jour_position(position_mobile,temps_maitenant_s)

    temps_precedent_ms = temps_maitenant_ms

    fenetre.fill(couleur_fond)
    dessiner_piste()
    dessiner_mobile()
    afficher_tableau_de_bord(100,100)
    mettre_a_jour_statistiques()

    pygame.display.flip()
    horloge.tick(images_par_seconde)
