'''
classe representant un utilisateur
Un utilisateur est defini par:
  un nom, utile pour dire au serveur qui joue
  une position sur le plateau de jeu

'''
class Joueur:

    # Constructeur
    def __init__(self, nom, pos_joueur, orientation):
        self.nom = nom
        self.positionJoueur = pos_joueur
        self.orientation = orientation

    def modifierPosition(self, x, y):
        self.positionJoueur = (x, y)

    def recupererPosition(self):
        return self.positionJoueur

    def recupererOrientation(self):
        return self.orientation

    def retournerNom(self):
        return self.nom

    def modifierNom(self, nom):
        self.nom = nom


class Aventurier(Joueur):

    def __init__(self, nom, pos_joueur, orientation):
        super().__init__(nom,pos_joueur, orientation)
        self.classeJoueur = 0

class Chasseur(Joueur):

    def __init__(self, nom, pos_joueur, orientation):
        super().__init__(nom,pos_joueur, orientation)
        self.classeJoueur = 1
