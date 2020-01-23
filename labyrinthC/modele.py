'''
Created on Sep 6, 2016

@author: antoi_000
'''
class Modele :

    def __init__(self, position, nomJoueur):
        self.positionJoueur = position
        self.nomJoueur = nomJoueur
        self.classeJoueur = 0
        self.positionBut = []
        self.infoJoueurs = []
        self.murs = []
        self.mursA = []
        self.sols = []
        self.solsA = []
        self.partiePerdue = False
        self.partieGagne = False
        self.tailleCase = 0
        self.tailleFenetre = (0,0)
        self.nbCaseX = 0
        self.nbCaseY = 0
        self.serveurLocal = False

    def setNbCase(self):
            self.nbCaseX = self.tailleFenetre[0]/self.tailleCase
            self.nbCaseY = self.tailleFenetre[1]/self.tailleCase
