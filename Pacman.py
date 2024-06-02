import random
import tkinter as tk
from tkinter import font  as tkfont
import numpy as np
 

##########################################################################
#
#   Partie I : variables du jeu  -  placez votre code dans cette section
#
#########################################################################
 
# Plan du labyrinthe

# 0 vide
# 1 mur
# 2 maison des fantomes (ils peuvent circuler mais pas pacman)

# transforme une liste de liste Python en TBL numpy équivalent à un tableau 2D en C
def CreateArray(L):
   T = np.array(L,dtype=np.int32)
   T = T.transpose()  ## ainsi, on peut écrire TBL[x][y]
   return T

TBL = CreateArray([
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,0,1,1,2,2,1,1,0,1,1,0,1,0,1],
        [1,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,1],
        [1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ])
# attention, on utilise TBL[x][y] 
        
HAUTEUR = TBL.shape [1]      
LARGEUR = TBL.shape [0]  

tableauBalayage = CreateArray([
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ])

#pour la chasse
modeChasse = False
chasseCounter = 0

# placements des pacgums et des fantomes

def PlacementsGUM():  # placements des pacgums
   GUM = np.zeros(TBL.shape,dtype=np.int32)
   
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 0):
            GUM[x][y] = 1
   return GUM
            
GUM = PlacementsGUM()   

def min(a, b):
    if a <= b:
        return a 
    return b

def balayge():
    fin = True
    # Initialisation du tableau
    for i in range(len(TBL)):
        for j in range(len(TBL[i])):
            if TBL[i][j] >= 1: # murs
                tableauBalayage[i][j] = 1000
            elif GUM[i][j] == 1: # gums
                tableauBalayage[i][j] = 0
            else: # couloirs
                tableauBalayage[i][j] = 100

    while fin:
        fin = False
        # Parcours du balayage
        for i in range(len(tableauBalayage)):
            for j in range(len(tableauBalayage[i])):
                if tableauBalayage[i][j] > 0 and tableauBalayage[i][j] < 1000:
                    gauche = tableauBalayage[i][j-1]
                    droite = tableauBalayage[i][j+1]
                    haut = tableauBalayage[i-1][j]
                    bas = tableauBalayage[i+1][j]
                    
                    # prendre le minimum des 4
                    minimum = min(gauche, droite)
                    minimum = min(minimum, haut)
                    minimum = min(minimum, bas)
                    
                    if minimum == 100:
                        continue

                    # skip si la valeur est déjà à jour
                    if tableauBalayage[i][j] == minimum + 1:
                        continue

                    # affecter le minimum des 4 s'il est inférieur
                    tableauBalayage[i][j] = minimum + 1
                    SetInfo1(i,j,tableauBalayage[i][j])
                    fin = True
    return tableauBalayage
    

tableaupac = balayge()



# Score de la partie   
score = 0

# Fonction qui permet d'effacer les gum lorsqu'elles sont touchées par le pacman et d'augmenter le score
def effacerGum():
    global PacManPos, GUM, score, tableauBalayage, modeChasse, chasseCounter
    if GUM[PacManPos[0]][PacManPos[1]] == 1 :
        GUM[PacManPos[0]][PacManPos[1]] = 0
        tableauBalayage[PacManPos[0]][PacManPos[1]] = 100
        score += 100
        #Dans le cas où c'est une super gum
        if (PacManPos == [1, 1] or PacManPos == [18, 1] or PacManPos == [1, 9] or PacManPos == [18, 9]) and not modeChasse:
         modeChasse = True
         chasseCounter = 16


PacManPos = [5,5]
direction = [ "haut", "bas", "gauche" , "droite"]
Ghosts  = []
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "pink"  , None ]   )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "orange", None ] )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "cyan"  , None ]   )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "red"   , None ]     )         



##############################################################################
#
#  Debug : ne pas toucher (affichage des valeurs autours dans les cases

LTBL = 100
TBL1 = [["" for i in range(LTBL)] for j in range(LTBL)]
TBL2 = [["" for i in range(LTBL)] for j in range(LTBL)]


# info peut etre une valeur / un string vide / un string...
def SetInfo1(x,y,info):
   info = str(info)
   if x < 0 : return
   if y < 0 : return
   if x >= LTBL : return
   if y >= LTBL : return
   TBL1[x][y] = info
   
def SetInfo2(x,y,info):
   info = str(info)
   if x < 0 : return
   if y < 0 : return
   if x >= LTBL : return
   if y >= LTBL : return
   TBL2[x][y] = info
   


##############################################################################
#
#   Partie II :  AFFICHAGE -- NE PAS MODIFIER  jusqu'à la prochaine section
#
##############################################################################

 

ZOOM = 40   # taille d'une case en pixels
EPAISS = 8  # epaisseur des murs bleus en pixels

screeenWidth = (LARGEUR+1) * ZOOM  
screenHeight = (HAUTEUR+2) * ZOOM

Window = tk.Tk()
Window.geometry(str(screeenWidth)+"x"+str(screenHeight))   # taille de la fenetre
Window.title("ESIEE - PACMAN")

# gestion de la pause

PAUSE_FLAG = False 

def keydown(e):
   global PAUSE_FLAG
   if e.char == ' ' : 
      PAUSE_FLAG = not PAUSE_FLAG 
 
Window.bind("<KeyPress>", keydown)
 

# création de la frame principale stockant plusieurs pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)


# gestion des différentes pages

ListePages  = {}
PageActive = 0

def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame

def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()
    
    
def WindowAnim():
    PlayOneTurn()
    Window.after(333,WindowAnim)

Window.after(100,WindowAnim)

# Ressources

PoliceTexte = tkfont.Font(family='Arial', size=22, weight="bold", slant="italic")

# création de la zone de dessin

Frame1 = CreerUnePage(0)

canvas = tk.Canvas( Frame1, width = screeenWidth, height = screenHeight )
canvas.place(x=0,y=0)
canvas.configure(background='black')
 
 
#  FNT AFFICHAGE


def To(coord):
   return coord * ZOOM + ZOOM 
   
# dessine l'ensemble des éléments du jeu par dessus le décor

anim_bouche = 0
animPacman = [ 5,10,15,10,5]


def Affiche(PacmanColor,message):
   global anim_bouche
   
   def CreateCircle(x,y,r,coul):
      canvas.create_oval(x-r,y-r,x+r,y+r, fill=coul, width  = 0)
   
   canvas.delete("all")
      
      
   # murs
   
   for x in range(LARGEUR-1):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 1 and TBL[x+1][y] == 1 ):
            xx = To(x)
            xxx = To(x+1)
            yy = To(y)
            canvas.create_line(xx,yy,xxx,yy,width = EPAISS,fill="blue")

   for x in range(LARGEUR):
      for y in range(HAUTEUR-1):
         if ( TBL[x][y] == 1 and TBL[x][y+1] == 1 ):
            xx = To(x) 
            yy = To(y)
            yyy = To(y+1)
            canvas.create_line(xx,yy,xx,yyy,width = EPAISS,fill="blue")
            
   # pacgum
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( GUM[x][y] == 1):
            xx = To(x) 
            yy = To(y)
            e = 5
            canvas.create_oval(xx-e,yy-e,xx+e,yy+e,fill="orange")
            
   #extra info
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         xx = To(x) 
         yy = To(y) - 11
         txt = TBL1[x][y]
         canvas.create_text(xx,yy, text = txt, fill ="white", font=("Purisa", 8)) 
         
   #extra info 2
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         xx = To(x) + 10
         yy = To(y) 
         txt = TBL2[x][y]
         canvas.create_text(xx,yy, text = txt, fill ="yellow", font=("Purisa", 8)) 
         
  
   # dessine pacman
   xx = To(PacManPos[0]) 
   yy = To(PacManPos[1])
   e = 20
   anim_bouche = (anim_bouche+1)%len(animPacman)
   ouv_bouche = animPacman[anim_bouche] 
   tour = 360 - 2 * ouv_bouche
   canvas.create_oval(xx-e,yy-e, xx+e,yy+e, fill = PacmanColor)
   canvas.create_polygon(xx,yy,xx+e,yy+ouv_bouche,xx+e,yy-ouv_bouche, fill="black")  # bouche
   
  
   #dessine les fantomes
   dec = -3
   for P in Ghosts:
      xx = To(P[0]) 
      yy = To(P[1])
      e = 16
      
      coul = P[2]
      # corps du fantome
      CreateCircle(dec+xx,dec+yy-e+6,e,coul)
      canvas.create_rectangle(dec+xx-e,dec+yy-e,dec+xx+e+1,dec+yy+e, fill=coul, width  = 0)
      
      # oeil gauche
      CreateCircle(dec+xx-7,dec+yy-8,5,"white")
      CreateCircle(dec+xx-7,dec+yy-8,3,"black")
       
      # oeil droit
      CreateCircle(dec+xx+7,dec+yy-8,5,"white")
      CreateCircle(dec+xx+7,dec+yy-8,3,"black")
      
      dec += 3
      
   # texte  
   
   canvas.create_text(screeenWidth // 2, screenHeight- 50 , text = "PAUSE : PRESS SPACE", fill ="yellow", font = PoliceTexte)
   canvas.create_text(screeenWidth // 2, screenHeight- 20 , text = message, fill ="yellow", font = PoliceTexte)
   
 
AfficherPage(0)
            
#########################################################################
#
#  Partie III :   Gestion de partie   -   placez votre code dans cette section
#
#########################################################################

      
def PacManPossibleMove():
   L = []
   x,y = PacManPos
   if ( TBL[x  ][y-1] == 0 ): L.append((0,-1))
   if ( TBL[x  ][y+1] == 0 ): L.append((0, 1))
   if ( TBL[x+1][y  ] == 0 ): L.append(( 1,0))
   if ( TBL[x-1][y  ] == 0 ): L.append((-1,0))
   return L
   
def GhostsPossibleMove(x,y):
   L = []
   if ( TBL[x  ][y-1] == 2 or TBL[x  ][y-1] == 0): L.append((0,-1,"bas"))
   if ( TBL[x  ][y+1] == 2 or TBL[x  ][y+1] == 0): L.append((0, 1,"haut"))
   if ( TBL[x+1][y  ] == 2 or TBL[x+1 ][y ] == 0): L.append(( 1,0,"droite"))
   if ( TBL[x-1][y  ] == 2 or TBL[x-1 ][y ] == 0): L.append((-1,0,"gauche"))
   return L
   
def IAPacman():
   global PacManPos, Ghosts, modeChasse, chasseCounter, PacmanColor
   
   #deplacement Pacman
   L = PacManPossibleMove()
   G = ghostDistance()
   move = 0
   # mode chasse
   if modeChasse:
       # Cherche à se rapprocher des fantômes
       valeur = G[PacManPos[0] + L[0][0]][PacManPos[1] + L[0][1]]
       for i in range(len(L)):
           if G[PacManPos[0] + L[i][0]][PacManPos[1] + L[i][1]] < valeur:
               valeur = G[PacManPos[0] + L[i][0]][PacManPos[1] + L[i][1]]
               move = i

   # mode fuite
   elif G[PacManPos[0]][PacManPos[1]] <= 3:
      valeur = G[PacManPos[0] + L[0][0]] [PacManPos[1] + L[0][1]]
      for i in range(len(L)) :
         if G[PacManPos[0] + L[i][0]] [PacManPos[1] + L[i][1]] > valeur :
            valeur = G[PacManPos[0] + L[i][0]] [PacManPos[1] + L[i][1]] 
            move = i

   # mode normal
   else : 
      valeur = tableaupac[PacManPos[0] + L[0][0]] [PacManPos[1] + L[0][1]]
      for i in range(len(L)) :
         if tableaupac[PacManPos[0] + L[i][0]] [PacManPos[1] + L[i][1]] < valeur :
            valeur = tableaupac[PacManPos[0] + L[i][0]] [PacManPos[1] + L[i][1]] 
            move = i

   PacManPos[0] += L[move][0]
   PacManPos[1] += L[move][1]
   collision()

   # Gestion de la durée du mode chasse
   if modeChasse:
      chasseCounter -= 1
      if chasseCounter == 0:
         modeChasse = False
   
def IAGhosts():
   #deplacement Fantome
   for F in Ghosts:
      L = GhostsPossibleMove(F[0],F[1])
      choix = random.randrange(len(L))
      move = 0
      if F[3] == None :
         F[3] = L[choix][2]
         move = choix  
      else :
            move = random.randrange(len(L))
            if len(L) > 2 :
               move = random.randrange(len(L))
               F[3] = L[move][2]
            else :
               for i in range(len(L)) :
                  if F[3] == L[i][2]:
                     move = i
                     break
               F[3] = L[move][2]

      F[0] += L[move][0]
      F[1] += L[move][1]
      collision()
  
# Collision PacMan | Ghost
def collision() :
   global PAUSE_FLAG, modeChasse, score
   for ghost in Ghosts:
      if PacManPos[0] == ghost[0] and PacManPos[1] == ghost[1]:
         if modeChasse:
            score += 2000
            ghost[0] = LARGEUR // 2
            ghost[1] = HAUTEUR // 2
         else:
            PAUSE_FLAG = True



ghostBalayage = CreateArray([
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ])

# Distance ghost
def ghostDistance():
    fin = True
    # Initialisation du tableau

    for i in range(len(TBL)):
        for j in range(len(TBL[i])):
            if TBL[i][j] >= 1: # murs
                ghostBalayage[i][j] = 1000
            else: # couloirs
                ghostBalayage[i][j] = 100
            for ghost in Ghosts:
               # Exclure la base de départ des fantômes du calcul de la distance
                if [i, j] == [LARGEUR // 2, HAUTEUR // 2]:
                    ghostBalayage[i][j] = 1000
                else:
                  ghostBalayage[ghost[0]][ghost[1]] = 0
    while fin:
        fin = False
        # Parcours du balayage
        for i in range(len(ghostBalayage)):
            for j in range(len(ghostBalayage[i])):
                if ghostBalayage[i][j] > 0 and ghostBalayage[i][j] < 1000:
                    gauche = ghostBalayage[i][j-1]
                    droite = ghostBalayage[i][j+1]
                    haut = ghostBalayage[i-1][j]
                    bas = ghostBalayage[i+1][j]
                    
                    # prendre le minimum des 4
                    minimum = min(gauche, droite)
                    minimum = min(minimum, haut)
                    minimum = min(minimum, bas)
                    
                    if minimum == 100:
                        continue

                    # skip si la valeur est déjà à jour
                    if ghostBalayage[i][j] == minimum + 1:
                        continue
                    # affecter le minimum des 4 s'il est inférieur
                    ghostBalayage[i][j] = minimum + 1
                    SetInfo2(i,j,ghostBalayage[i][j])
                    fin = True
    return ghostBalayage


#  Boucle principale de votre jeu appelée toutes les 500ms

iteration = 0
def PlayOneTurn():
   global iteration, modeChasse

   if not PAUSE_FLAG : 
      iteration += 1
      # Effacer les GUM touchés
      effacerGum()
      balayge()
      ghostDistance()
      if iteration % 2 == 0 :   IAPacman()
      else:                     IAGhosts()
    
    
   # Affiche le score du jeu
   Affiche(PacmanColor = "yellow", message = "Score : " + str(score))  

   if modeChasse:
      Affiche(PacmanColor = "red", message = "Score : " + str(score))  

 
 
###########################################:
#  demarrage de la fenetre - ne pas toucher

Window.mainloop()
