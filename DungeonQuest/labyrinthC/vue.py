'''
Created on Sep 1, 2016

@author: antoi_000
'''

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color
from kivy.graphics import Line
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.clock import Clock

from commun.constante import Constante
from labyrinthC.client import Client
from labyrinthC.modele import Modele
#from bokeh.core.enums import Orientation

class Vue(FloatLayout):

    def __init__(self, controleur, **kwargs):
        super(Vue, self).__init__(**kwargs)
        Window.size = (1024, 600)

        with self.canvas.before:
            self.rect = Rectangle(size=self.size, pos=self.pos, source='labyrinthC/Modeles/Background.png')
            self.wimg = Image(size=(1000,1000), pos=(0,200), source='labyrinthC/Modeles/Dungeon_Quest.png')

        self.controleur = controleur
        #self.racine = FloatLayout(size=Constante.TAILLE_FENETRE)
        #bottom
        self.panelPrincipale = BoxLayout(padding=10)
        self.panelAccueil = BoxLayout(orientation='vertical', spacing=10, size_hint=(1,0.3), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        self.panelServeur = BoxLayout(orientation='vertical', spacing=10, size_hint=(1,0.4), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        self.panelAdresseServeur = BoxLayout(orientation='vertical', spacing=10, size_hint=(1,0.4), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        self.panelNom = BoxLayout(orientation='vertical', spacing=10, size_hint=(1,0.4), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        self.panelDefaite = BoxLayout(orientation='vertical', spacing=10, size_hint=(1,0.4), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        self.panelVictoire = BoxLayout(orientation='vertical', spacing=10, size_hint=(1,0.4), pos_hint={'center_x': 0.5, 'center_y': 0.4})


        self.buttonJoueur = Button(text='Joueur', background_normal='labyrinthC/Modeles/Button_normal.png', background_down='labyrinthC/Modeles/Button_down.png', font_size=20, size_hint=(0.3,1), pos_hint={'center_x': 0.5})
        self.buttonHost = Button(text='Host', background_normal='labyrinthC/Modeles/Button_normal.png', background_down='labyrinthC/Modeles/Button_down.png', font_size=20, size_hint=(0.3,1), pos_hint={'center_x': 0.5})
        #self.buttonConfirmeNom = Button(text='Start Partie', background_normal='Button_normal.png', background_down='Button_down.png', font_size=20, size_hint=(0.3,1), pos_hint={'center_x': 0.5})
        self.buttonConfirmeServeur = Button(text='Ok', background_normal='labyrinthC/Modeles/Button_normal.png', background_down='labyrinthC/Modeles/Button_down.png', font_size=20, size_hint=(0.3,1), pos_hint={'center_x': 0.5})
        self.buttonStartServer = Button(text='Start', background_normal='labyrinthC/Modeles/Button_normal.png', background_down='labyrinthC/Modeles/Button_down.png', font_size=20, size_hint=(0.3,1), pos_hint={'center_x': 0.5})
        self.buttonStopServer = Button(text='Stop', background_normal='labyrinthC/Modeles/Button_normal.png', background_down='labyrinthC/Modeles/Button_down.png', font_size=20, size_hint=(0.3,1), pos_hint={'center_x': 0.5})
        self.buttonConfirmeAdresse = Button(text='Ok', background_normal='labyrinthC/Modeles/Button_normal.png', background_down='labyrinthC/Modeles/Button_down.png', font_size=20, size_hint=(0.3,1), pos_hint={'center_x': 0.5})
        self.buttonStartPartie = Button(text='Start Partie', background_normal='labyrinthC/Modeles/Button_normal.png', background_down='labyrinthC/Modeles/Button_down.png', font_size=20, size_hint=(0.3,1), pos_hint={'center_x': 0.5})
        self.buttonRetourAccueil = Button(text='Retour Accueil', background_normal='labyrinthC/Modeles/Button_normal.png', background_down='labyrinthC/Modeles/Button_down.png', font_size=20, size_hint=(0.3,1), pos_hint={'center_x': 0.5})
        self.buttonRetourAccueil1 = Button(text='Retour Accueil', background_normal='labyrinthC/Modeles/Button_normal.png', background_down='labyrinthC/Modeles/Button_down.png', font_size=20, size_hint=(0.3,1), pos_hint={'center_x': 0.5})
        self.buttonRetourAccueil2 = Button(text='Retour Accueil', background_normal='labyrinthC/Modeles/Button_normal.png', background_down='labyrinthC/Modeles/Button_down.png', font_size=20, size_hint=(0.3,1), pos_hint={'center_x': 0.5})

        self.textAdresseServeur = TextInput(text='127.0.0.1', padding=(10,10,0,0), font_size=20, size_hint=(0.3,1), pos_hint={'center_x': 0.5})
        self.textAdresseServeur.multiline = False
        self.textNom = TextInput(text='', padding=(10,10,0,0), font_size=20, size_hint=(0.3,1), pos_hint={'center_x': 0.5})
        self.textNom.multiline = False

        self.labelAccueil = Label(text='Bienvenue à toi Aventurier !', font_size=30, bold=True, pos_hint={'center_x': 0.5})
        self.labelServeur = Label(text='Démarrer / Arrêter le serveur', font_size=30, bold=True, pos_hint={'center_x': 0.5})
        self.labelAdresse = Label(text='Rentrer l\'adresse du serveur :', font_size=30, bold=True, pos_hint={'center_x': 0.5})
        self.labelNom = Label(text='Rentrer votre pseudo :', font_size=30, bold=True, pos_hint={'center_x': 0.5})

        self.panelAccueil.add_widget(self.labelAccueil)
        self.panelAccueil.add_widget(self.buttonJoueur)
        self.panelAccueil.add_widget(self.buttonHost)

        self.anim = Animation(x=0,y=-50) +  Animation(x=0,y=-20)
        self.anim.repeat = True
        self.anim.start(self.wimg)

        self.panelNom.add_widget(self.labelNom)
        self.panelNom.add_widget(self.textNom)
        self.panelNom.add_widget(self.buttonStartPartie)
        self.panelNom.add_widget(self.buttonRetourAccueil)

        self.panelServeur.add_widget(self.labelServeur)
        self.panelServeur.add_widget(self.buttonStartServer)
        self.panelServeur.add_widget(self.buttonStopServer)
        self.panelServeur.add_widget(self.buttonRetourAccueil1)

        self.panelAdresseServeur.add_widget(self.labelAdresse)
        self.panelAdresseServeur.add_widget(self.textAdresseServeur)
        self.panelAdresseServeur.add_widget(self.buttonConfirmeAdresse)
        self.panelAdresseServeur.add_widget(self.buttonRetourAccueil2)

        self.add_widget(self.panelPrincipale)

        self.affichePanelAccueil()

        self.imageSource = 'pac8.png'
        self.joueur = None
        self.but = None
        self.tailleCase = None
        self.orientation = 0
        self.marche = 0

        print('Trying to get keyboard')
        self.keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        print('Trying to get keyboard done')

    def startPartie(self):

        self.canvas.before.clear()

        self.keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        #self.plateau = Rectangle(size=Constante.TAILLE_FENETRE, pos=(0,0))
        #self.canvas.add(self.plateau)

    def affichePanelAccueil(self):

        self.panelPrincipale.clear_widgets()
        self.panelPrincipale.add_widget(self.panelAccueil)

    def affichePanelDemarrerServeur(self):

        self.panelPrincipale.clear_widgets()
        self.buttonStopServer.disabled = True
        self.panelPrincipale.add_widget(self.panelServeur)

    def affichePanelAdresseServeur(self):
        self.panelPrincipale.clear_widgets()
        self.panelPrincipale.add_widget(self.panelAdresseServeur)

    '''def affichePanelStartPartie(self):
        self.panelPrincipale.clear_widgets()
        self.panelPrincipale.add_widget(self.buttonStartPartie)'''

    def affichePanelNom(self):
        self.panelPrincipale.clear_widgets()
        self.panelPrincipale.add_widget(self.panelNom)

    def transpose (self, position) :
        x = position[0]
        y = position[1]
        return (x * self.tailleCase, y * self.tailleCase)

    def afficherMurs(self, murs, classe, sols):

        if classe == 1:
            self.canvas.before.clear()

        with self.canvas.before:
            for mur in murs:
                if ((mur[0],mur[1]-1) in sols):
                    Rectangle(source='labyrinthC/Sprites/Wall/Wall edge (no border).png', pos=self.transpose(mur), size=(self.tailleCase, self.tailleCase))
                else:
                    Rectangle(source='labyrinthC/Sprites/Wall/Wall top (no border).png', pos=self.transpose(mur), size=(self.tailleCase, self.tailleCase))

            for sol in sols:
                Rectangle(source='labyrinthC/Sprites/Wall/Floor.png', pos=self.transpose(sol), size=(self.tailleCase, self.tailleCase))

    def afficheJoueur(self, position, classe):
        self.canvas.clear()
        with self.canvas:
            if classe == 0:
                self.joueur = Rectangle(source='labyrinthC/Sprites/Aventurier/aventurier_'+str(self.orientation)+str(self.marche)+'.png', pos=self.transpose(position), size=(self.tailleCase, self.tailleCase))
            elif classe == 1:
                self.joueur = Rectangle(source='labyrinthC/Sprites/Chasseurs/chasseur1_'+str(self.orientation)+str(self.marche)+'.png', pos=self.transpose(position), size=(self.tailleCase, self.tailleCase))

    def afficheJoueurs(self, info, position, classe, sols):
        self.canvas.after.clear()
        with self.canvas.after:
            if classe == 0:
                for (pos,o,c) in info:
                    if not pos == position:
                        Rectangle(source='labyrinthC/Sprites/Chasseurs/chasseur1_'+o+'0.png', pos=self.transpose(pos), size=(self.tailleCase, self.tailleCase))
            elif classe == 1:
                for (pos,o,c) in info:
                    if not pos == position:
                        if c == 0 and pos in sols :
                            Rectangle(source='labyrinthC/Sprites/Aventurier/aventurier_'+o+'0.png', pos=self.transpose(pos), size=(self.tailleCase, self.tailleCase))
                        elif c == 1:
                            Rectangle(source='labyrinthC/Sprites/Chasseurs/chasseur1_'+o+'0.png', pos=self.transpose(pos), size=(self.tailleCase, self.tailleCase))

    def afficheBut(self, positionBut):
        self.but = InstructionGroup()
        for goal in positionBut:
            self.but.add(Rectangle(source='labyrinthC/Sprites/Artefacts/Treasure.png',pos=self.transpose(goal), size=(self.tailleCase, self.tailleCase)))
        self.canvas.add(self.but)

    def ecranDefaite(self):
        self.canvas.clear()
        self.canvas.after.clear()
        self.loose = InstructionGroup()
        self.loose.add(Rectangle(source='labyrinthC/Sprites/DEFAITE.png',size=self.size, pos=(0,0)))
        self.canvas.after.add(elf.loose)

    def ecranVictoire(self):
        self.canvas.clear()
        self.canvas.after.clear()
        self.win = InstructionGroup()
        self.win.add(Rectangle(source='labyrinthC/Sprites/VICTOIRE.png',size=self.size, pos=(0,0)))
        self.canvas.after.add(self.win)


    def _keyboard_closed(self):
        print('Mon clavier est ferme')
