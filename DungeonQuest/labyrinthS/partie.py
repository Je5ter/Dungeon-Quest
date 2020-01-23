# -*- coding: utf-8 -*-

'''
Created on 3 Jul 2013

@author: pigeau-a
'''
from commun.constante import Constante
import os
import random

# STRUCTURE DE DONNEES POUR REPRESENTER L'ETAT DU JEU A UN INSTANT DONNE.

class Partie:

    # FONCTION D'INITIALISATION
    def __init__(self):
        self.murs = []
        self.sols = []
        self.joueurs = {}
        self.positionBut = []
        self.tailleCase = 30
        self.taillePlateauX = 1024
        self.taillePlateauY = 600
        self.nbCasesX = self.taillePlateauX/self.tailleCase
        self.nbCasesY = self.taillePlateauY/self.tailleCase
        self.etat = Constante.ETAT_INSCRIPTION_OUVERTE

        self.chargerParametre()
        self.genererBut(self.sols)

    def chargerParametre(self,filename='labyrinthS/Labyrinth/laby3.lab'):
        print(os.getcwd())
        fic = open(filename,"r")

        numLigne=1
        for ligne in fic:
            numColonne=0
            for c in ligne:
                if c=='X':
                    self.murs.append((numColonne,self.nbCasesY-numLigne))

                elif c== ' ' or c==None:
                    self.sols.append((numColonne,self.nbCasesY-numLigne))

                '''elif c=='J':
                    self.positionJoueur = (numColonne,self.nbCasesY-numLigne)

                elif c=='T':
                    self.positionBut = (numColonne,self.nbCaseY-numLigne)'''

                numColonne = numColonne +1
            numLigne = numLigne + 1
        fic.close()


    def genererBut(self, sols):
        for i in range(5):
            rand_but = random.choice(sols)
            while rand_but in self.positionBut:
                rand_but = random.choice(sols)
            self.positionBut.append(rand_but)

    def ajouterJoueur(self, joueur):
        print("user ", joueur.nom)
        self.joueurs[joueur.nom] = joueur
        if len(self.joueurs) >= 1:
            self.etat = Constante.ETAT_PARTIE_COMMENCEE

    def recupererJoueur(self, nom):
        return self.joueurs[nom]

    def estDejaAjouter(self, joueur):
        return joueur.nom in self.joueurs

    def recupererInfoJoueurs(self):
        liste = []
        for joueur in self.joueurs:
            liste.append((self.joueurs[joueur].recupererPosition(), self.joueurs[joueur].recupererOrientation(), self.joueurs[joueur].classeJoueur))
        print(str(liste))
        return liste

    # FONCTIONS DE GESTION DES DEPLACEMENTS

    """
    conversion d'une demande de deplacement en deplacement reelle sur le plateau.
    Par exemple, un deplacement au nord entraine de rester sur la meme colonne et de descendre de 1 pour la ligne: (0,-1)
    (pour rappel, (0,0) est situe en haut a gauche du plateau, l'axe y est croissant vers le bas et l'axe x est croissant vers la droite
    """
    def analyse(self, s):
        if s == "S":
            return (0,-1,"bas")
        if s == "N":
            return (0,1,"haut")
        if s == "W":
            return (-1,0,"gauche")
        if s == "E":
            return (1,0,"droite")
        else:
            return (0,0,"bas")

    """
    fonction testant si le deplacement est possible ou non
    @param direction: la direction demande par le joueur Q:quitter, N:Nord, S:South, W:West, E:Est, G:Gagne
    @param joueur: le joueur qui demande le deplacement
    @return: (le code de sortie, la position du joueur). SORTIE_OK si un mouvement a été réalisé, SORTIE_NOT_OK si l'utilisateur n'a pas pu bouger, SORTIE_PARTIE_FINIE si la partie est deja finie et perdue,
    SORTIE_PARTIE_GAGNE, si la partie est gagnée
    """
    def deplacement(self, direction, joueur):
        print("traite_actions_joueur: ", direction, " ", joueur.nom)
        reponse = (Constante.SORTIE_NOT_OK, 0)

        (dx,dy,orientation) = self.analyse(direction) # recupere le deplacement
        joueur.orientation = orientation
        (x, y)  = joueur.positionJoueur
        new_pos = (x+dx, y+dy)

        if not self.collision (new_pos):
            joueur.positionJoueur = new_pos
            reponse = (Constante.SORTIE_OK, new_pos)
        else:
            reponse = (Constante.SORTIE_NOT_OK, joueur.positionJoueur)

        #Condition de victoire pour l'aventurier
        if joueur.positionJoueur in self.positionBut and joueur.classeJoueur == 0:
            pos = joueur.positionJoueur
            self.positionBut.remove(pos)

        if self.positionBut == []:
            reponse = (Constante.SORTIE_PARTIE_GAGNE, 0)
            self.etat = Constante.ETAT_PARTIE_FINIE

        #Condition de victoire pour le chasseur
        if joueur.classeJoueur == 1 and self.catchYa(joueur.positionJoueur, self.posAventurier()):
            reponse = (Constante.SORTIE_PARTIE_GAGNE, 0)
            self.etat = Constante.ETAT_PARTIE_FINIE

        return reponse

    """
    Fonction testant si un deplacement est empeche par un mur ou par une sortie du plateau
    @return: True si pas de collision, False sinon
    """
    def collision (self, param):
        x = param[0]
        y = param[1]
        return ( x >= self.nbCasesX or
               x < 0      or
               y >= self.nbCasesY or
               y < 0      or
               ((x,y) in self.murs)
               )

    def catchYa(self, pos, posA):
        if posA == (pos[0], pos[1]+1) or posA == (pos[0], pos[1]-1) or posA == (pos[0]+1, pos[1]) or posA == (pos[0]-1, pos[1]):
            return True
        else:
            return False

    def posAventurier(self):
        for joueur in self.joueurs:
            if self.joueurs[joueur].classeJoueur == 0:
                posA = self.joueurs[joueur].recupererPosition()
                return posA
