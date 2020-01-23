'''
Created on Sep 6, 2016

@author: antoi_000
'''

from kivy.clock import Clock
from kivy.core.window import Window

from labyrinthC.vue import Vue
from labyrinthS.serveur import Serveur
from labyrinthC.modele import Modele
from commun.constante import Constante
from labyrinthC.client import Client

import threading
import labyrinthS.start

class Controleur:


    def __init__(self):
        self.vue = Vue(self, size=Constante.TAILLE_FENETRE)

        self.processServeur = None
        self.client = None
        self.modele = Modele((0,0), "Peip")

        self.vue.buttonRetourAccueil.bind(on_release=self.actionRetourAccueil)
        self.vue.buttonRetourAccueil1.bind(on_release=self.actionRetourAccueil)
        self.vue.buttonRetourAccueil2.bind(on_release=self.actionRetourAccueil)

        self.vue.buttonJoueur.bind(on_release=self.actionButtonJoueur)
        self.vue.buttonHost.bind(on_release=self.actionButtonHost)

        self.vue.buttonStartServer.bind(on_release=self.actionStartServeur)
        self.vue.buttonStopServer.bind(on_release=self.actionStopServeur)
        #self.vue.buttonConfirmeServeur.bind(on_press=self.actionConfirmeServeur)

        self.vue.buttonStartPartie.bind(on_release=self.actionStartPartie)
        self.vue.buttonConfirmeAdresse.bind(on_release=self.actionConfirmeAdresseServeur)
        #self.vue.buttonConfirmeNom.bind(on_release=self.actionConfirmeNom)

    def update(self, dt):

        if(self.modele.partieGagne or self.client == None or self.modele.partiePerdue):
            pass
        else:
            if self.modele.classeJoueur == 1:
                self.vue.afficherMurs(self.modele.murs, self.modele.classeJoueur, self.modele.sols)
                self.vue.afficheJoueur(self.modele.positionJoueur, self.modele.classeJoueur)
            else:
                self.vue.afficheJoueur(self.modele.positionJoueur, self.modele.classeJoueur)
                self.vue.afficheBut(self.modele.positionBut)

    def updatePos(self, dt):
        self.modele.infoJoueurs = self.client.getInfoJoueurs()
        if(self.modele.partieGagne or self.client == None or self.modele.partiePerdue):
            pass
        else:
            self.vue.afficheJoueurs(self.modele.infoJoueurs, self.modele.positionJoueur, self.modele.classeJoueur, self.modele.sols)
            if self.modele.classeJoueur == 1:
                self.torchGroup(self.modele.infoJoueurs)

    def chargeParametreVue(self):

        self.client.inscriptionPartie(self.modele.nomJoueur)

        self.modele.tailleCase = self.client.getTailleCase()
        self.modele.tailleFenetre = self.client.getTaillePlateau()
        self.modele.positionBut = self.client.getPositionBut()
        self.modele.classeJoueur = self.client.getClasseJoueur(self.modele.nomJoueur)
        if self.modele.classeJoueur == 1:
            self.modele.positionBut = []
        self.modele.positionJoueur = (0,0)
        self.modele.setNbCase()

    def executerServeur(self):
        self.processServeur = threading.Thread(target=labyrinthS.start.lancerServeur)
        self.processServeur.start()


    def deplacement(self, keycode):

        (dx, dy) = self.clavier(keycode)

        (statut, new_pos) = self.requeteDeplacement((dx,dy))

        if statut == Constante.SORTIE_OK:
            self.modele.positionJoueur = new_pos
            if self.modele.classeJoueur == 0:
                self.modele.positionBut = self.client.getPositionBut()

            print("position joueur sur client: ", str(self.modele.positionJoueur), " ", dx, " ", dy)

        if statut == Constante.SORTIE_NOT_OK:
            if (dx,dy) == (0,0):
                self.modele.positionJoueur = new_pos
            else:
                (x,y) = self.modele.positionJoueur
                new_mur = (x+dx, y+dy)
                self.modele.murs.append(new_mur)
                print("append mur: ", new_mur)

        if statut == Constante.SORTIE_PARTIE_PERDUE:
            self.modele.partiePerdue = True
            self.vue.ecranDefaite()
            print("la partie est perdue")

        if statut == Constante.SORTIE_PARTIE_GAGNE:
            self.modele.partieGagne = True
            self.vue.ecranVictoire()
            print("la partie est gagnee")


        self.modele.sols = []
        self.modele.murs = []
        self.etatMarche()
        self.torch()

    def etatMarche(self):

        if self.vue.marche == 1:
            self.vue.marche = 0
        else:
            self.vue.marche = 1

    def torch(self):

        if self.vue.orientation == "haut":
            for i in range(3):
                for j in range(4):
                    if ((self.modele.positionJoueur[0]+i-1, self.modele.positionJoueur[1]+j,) in self.modele.mursA):
                        self.modele.murs.append((self.modele.positionJoueur[0]+i-1, self.modele.positionJoueur[1]+j,))
                    else:
                        self.modele.sols.append((self.modele.positionJoueur[0]+i-1, self.modele.positionJoueur[1]+j,))

        if self.vue.orientation == "bas":
            for i in range(3):
                for j in range(0,-4,-1):
                    if ((self.modele.positionJoueur[0]+i-1, self.modele.positionJoueur[1]+j,) in self.modele.mursA):
                        self.modele.murs.append((self.modele.positionJoueur[0]+i-1, self.modele.positionJoueur[1]+j,))
                    else:
                        self.modele.sols.append((self.modele.positionJoueur[0]+i-1, self.modele.positionJoueur[1]+j,))

        if self.vue.orientation == "droite":
            for i in range(4):
                for j in range(3):
                    if ((self.modele.positionJoueur[0]+i, self.modele.positionJoueur[1]+j-1,) in self.modele.mursA):
                        self.modele.murs.append((self.modele.positionJoueur[0]+i, self.modele.positionJoueur[1]+j-1,))
                    else:
                        self.modele.sols.append((self.modele.positionJoueur[0]+i, self.modele.positionJoueur[1]+j-1,))

        if self.vue.orientation == "gauche":
            for i in range(0,-4,-1):
                for j in range(3):
                    if ((self.modele.positionJoueur[0]+i, self.modele.positionJoueur[1]+j-1,) in self.modele.mursA):
                        self.modele.murs.append((self.modele.positionJoueur[0]+i, self.modele.positionJoueur[1]+j-1,))
                    else:
                        self.modele.sols.append((self.modele.positionJoueur[0]+i, self.modele.positionJoueur[1]+j-1,))

    def torchGroup(self, info):

        for (position, orientation, classe) in info:
            if classe == 1:
                if orientation == "haut":
                    for i in range(3):
                        for j in range(4):
                            if ((position[0]+i-1, position[1]+j,) in self.modele.mursA):
                                self.modele.murs.append((position[0]+i-1, position[1]+j,))
                            else:
                                self.modele.sols.append((position[0]+i-1, position[1]+j,))

                if orientation == "bas":
                    for i in range(3):
                        for j in range(0,-4,-1):
                            if ((position[0]+i-1, position[1]+j,) in self.modele.mursA):
                                self.modele.murs.append((position[0]+i-1, position[1]+j,))
                            else:
                                self.modele.sols.append((position[0]+i-1, position[1]+j,))

                if orientation == "droite":
                    for i in range(4):
                        for j in range(3):
                            if ((position[0]+i, position[1]+j-1,) in self.modele.mursA):
                                self.modele.murs.append((position[0]+i, position[1]+j-1,))
                            else:
                                self.modele.sols.append((position[0]+i, position[1]+j-1,))

                if orientation == "gauche":
                    for i in range(0,-4,-1):
                        for j in range(3):
                            if ((position[0]+i, position[1]+j-1,) in self.modele.mursA):
                                self.modele.murs.append((position[0]+i, position[1]+j-1,))
                            else:
                                self.modele.sols.append((position[0]+i, position[1]+j-1,))

    def requeteDeplacement(self, position):
        message = self.conversion(position)
        reponse = self.client.deplacement(self.modele.nomJoueur, message)

        return reponse

    def conversion(self, param):
        x = param[0]
        y = param[1]
        if ((x,y) == (1,0)):
            self.vue.orientation = "droite"
            return "E"
        if ((x,y) == (-1,0)):
            self.vue.orientation = "gauche"
            return "W"
        if ((x,y) == (0,1)):
            self.vue.orientation = "haut"
            return "N"
        if ((x,y) == (0,-1)):
            self.vue.orientation = "bas"
            return "S"
        if ((x,y) == (0,0)):
            self.vue.orientation = "bas"
            return "K"
        else:
            return "S"

    def clavier(self, keycode):
        if keycode[1] == 'up':
            return (0,1)
        if keycode[1] == 'down':
            return (0,-1)
        if keycode[1] == 'left':
            return (-1,0)
        if keycode[1] == 'right':
            return (1,0)
        return (0,0)

    def actionToucheClavier(self, keyboard, keycode, text, modifiers):

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        print('ActionTouchClavier ' + str(keycode) )
        if keycode[1] == 'escape':
            keyboard.release()

        if self.client != None:
            self.deplacement(keycode)


        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

    def actionRetourAccueil(self, instance):
        self.vue.affichePanelAccueil()

    def actionButtonJoueur(self, instance):
        self.vue.affichePanelAdresseServeur()

    def actionButtonHost(self, instance):
        self.vue.affichePanelDemarrerServeur()

        if (self.modele.serveurLocal):
            self.vue.buttonStopServer.disabled = False
            self.vue.buttonStartServer.disabled = True
        else:
            self.vue.buttonStopServer.disabled = True
            self.vue.buttonStartServer.disabled = False


    def actionStartServeur(self, instance):
        print("actionBoutonStartServer")

        self.executerServeur()
        self.vue.buttonStartServer.disabled = True
        self.vue.buttonStopServer.disabled = False

        self.client = Client(Constante.CLIENT_BASE, Constante.SERVER_PORT)

        self.modele.serveurLocal = True

        self.vue.affichePanelNom()

    def actionStopServeur(self, instance):
        print("actionBoutonStopServer")
        self.vue.buttonStopServer.disabled = True
        self.vue.buttonStartServer.disabled = False

        self.client.arretServeur()

        self.modele.serveurLocal = False

    """def actionConfirmeServeur(self, instance):

        if(self.modele.serveurLocal):
            #self.client = Client(Constante.CLIENT_BASE, Constante.SERVER_PORT)

            self.vue.affichePanelNom()

        else:
            self.vue.affichePanelAdresseServeur()"""

    def actionConfirmeAdresseServeur(self, instance):
        print("actionConfirmeAdresseServeur")
        text = self.vue.textAdresseServeur.text

        self.client = Client(self.vue.textAdresseServeur.text, Constante.SERVER_PORT)

        self.vue.affichePanelNom()

    '''def actionConfirmeNom(self, instance):
        print("actionConfirmeNom")
        self.modele.nomJoueur = self.vue.textNom.text'''

    def actionStartPartie(self, instance):
        print("actionConfirmeNom")
        self.modele.nomJoueur = self.vue.textNom.text
        print("actionBoutonStartPartie")
        self.vue.remove_widget(self.vue.panelPrincipale)
        self.chargeParametreVue()
        print("actionBoutonStartPartie : startpartie")
        self.vue.tailleCase = self.modele.tailleCase
        self.deplacement('home')
        self.modele.mursA = self.client.getListeMurs()
        self.modele.solsA = self.client.getListeSols()
        self.vue.startPartie()
        self.vue.afficheJoueur(self.modele.positionJoueur, self.modele.classeJoueur)
        if self.modele.classeJoueur == 0:
            self.vue.afficherMurs(self.modele.mursA, self.modele.classeJoueur, self.modele.solsA)
        print("actionBoutonStartPartie : keyboardbind")
        self.vue.keyboard.bind(on_key_down=self.actionToucheClavier)
        print("actionBoutonStartPartie : apres keyboardbind")

        Clock.schedule_interval(self.update, 1.0/600.0)
        Clock.schedule_interval(self.updatePos, 1.0/4.0)
