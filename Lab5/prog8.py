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
def mettre_a_jour_position(position,temps_maitenant,G,mu_c):
    g = (0,-G)
    global vitesse,premiere_iteration,temps_precedent_s, position_mobile,norme_v,acceleration_ressentie
    sigma = math.sqrt(1+pente(position[0])**2)
    u = [1/sigma,(pente(position[0])/sigma)]

    if premiere_iteration:
        vitesse = [0*u[0], 0*u[1]]
        premiere_iteration = False
        return

    if vitesse[0]<0:
        u[0] = -u[0]
        u[1] = -u[1]


    delta_ts = temps_maitenant-temps_precedent_s
    norme_v = math.sqrt(vitesse[0]**2 +vitesse[1]**2)
    nouvelle_vitesse= [norme_v*u[0],norme_v*u[1]]

    a_n = [(nouvelle_vitesse[0]-vitesse[0])/delta_ts,(nouvelle_vitesse[1]-vitesse[1])/delta_ts]

    n = [(-pente(position[0]))/sigma,1/sigma]


    n_scalaire_g = n[0]*g[0] + n[1]*g[1]
    a_t = (-n_scalaire_g*n[0],-n_scalaire_g*n[1])


    a_propre = (a_t[0]+a_n[0],a_t[1]+a_n[1])
    acceleration_ressentie = math.sqrt(a_propre[0]**2 + a_propre[1]**2)/9.81
    
    a_p_n = a_propre[0]*n[0] + a_propre[1]*n[1]
    
    a_f = (-mu_c*(a_p_n)*u[0],-mu_c*(a_p_n)*u[1])
    
    a = (a_n[0]+a_t[0]+g[0]+a_f[0],a_n[1]+a_t[1]+g[1]+a_f[1])

    
    vitesse[0] += delta_ts*a[0]
    vitesse[1] += delta_ts*a[1]

    position_mobile[0] += vitesse[0]*delta_ts
    position_mobile[1] += vitesse[1]*delta_ts

    temps_precedent_s = temps_maintenant_s

    return position_mobile

def afficher_tableau_de_bord(x,y):
    texte = "Vitesse : {0:.2f} m/s".format(norme_v)
    image = police.render(texte, True, couleur)
    fenetre.blit(image, (x, y))
    texte2 = "Vitesse max: {0:.2f} m/s".format(vmax)
    image = police.render(texte2, True, couleur)
    fenetre.blit(image, (x, y+20))
    texte3 = "Acceleration ressentie: {0:.2f} g".format(acceleration_ressentie)
    image = police.render(texte3, True, couleur)
    fenetre.blit(image, (x, y+40))
    texte4 = "Acceleration max: {0:.2f} g".format(a_max)
    image = police.render(texte4, True, couleur)
    fenetre.blit(image, (x, y+60))
    texte5 = "Acceleration min: {0:.2f} g".format(a_min)
    image = police.render(texte5, True, couleur)
    fenetre.blit(image, (x, y+80))


vmax = 0
a_max = 0
a_min = 10
def mettre_a_jour_statistiques():
    global vmax,norme_v,a_max,a_min
    if norme_v > vmax:
        vmax = norme_v
    if acceleration_ressentie > a_max:
        a_max = acceleration_ressentie
    if acceleration_ressentie < a_min:
        a_min = acceleration_ressentie


temps_precedent_ms =0
temps_precedent_s = 0
position_mobile = position_initiale_mobile()

while True:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()


    temps_maitenant_ms = pygame.time.get_ticks()

    for t in range(temps_precedent_ms,temps_maitenant_ms-1):
        temps_maintenant_s = t/1000
        mettre_a_jour_position(position_mobile,temps_maintenant_s,9.81,0.03)

    temps_precedent_ms = temps_maitenant_ms

    fenetre.fill(couleur_fond)
    dessiner_piste()
    dessiner_mobile()
    afficher_tableau_de_bord(100,100)
    mettre_a_jour_statistiques()

    pygame.display.flip()
    horloge.tick(images_par_seconde)