# -*- coding: utf-8 -*-

'''
Created on 3 Jul 2013

@author: pigeau-a
'''


import urllib.request
import ast
from commun.constante import Constante
import os

class Client:

    """
    constructeur du client pour appeler le serveur
    @param url: url du serveur (par exemple 'www.google.com')
    @param port: port du serveur (par exemple '8080')
    """
    def __init__(self, url, port):

        os.environ['http_proxy'] = ""
        os.environ['HTTP_PROXY'] = ""

        self.url = url
        self.port = port
        self.base_address = 'http://'+url+':'+str(port)+'/'

    """
    methode pour une demande de placement du joueur
    @param direction: la direction demande par le joueur. Valeurs possibles 'N', 'E', 'S' ou 'W' pour
    respectivement Nord, Est, Sud, West. Exemple d'appel : deplacement('N')
    @return: Constante.SORTIE_OK si le deplacement est accepte, Constante.SORTIE_NOT_OK si le deplacement n'est pas accepte,
    Constante.SORTIE_ERROR sinon
    """
    def deplacement(self, nomJoueur, direction):
        function = Constante.QUERY_DEPLACEMENT
        paramEtArg = [(Constante.ARG_DEPLACEMENT_DIRECTION, direction), (Constante.ARG_JOUEUR_NOM, nomJoueur)]
        response = self._query_generic(function, paramEtArg)
        return response

    """
    methode retournant la position de chaque joueurs
    @return: (position_x, position_y) de type (int, int)
    """
    def getInfoJoueurs(self):
        function = Constante.QUERY_RECUPERER_INFO_JOUEURS
        paramEtArg = []
        # recupere un flot d'octets
        (statut, liste) = self._query_generic(function, paramEtArg)

        if (statut == Constante.SORTIE_OK):
            return liste
        else:
            print("getPosJoueurs: statut["+ statut + "]")
            return []

    """
    methode retournant la liste des murs
    @return:  [(x1,y1), (x2, y2), ... (xn,yn)] de type [(int, int), ...(int, int)]
    """
    def getListeMurs(self):
        function = Constante.QUERY_RECUPERER_LISTE_MURS
        paramEtArg = []
        # recupere un flot d'octets
        (statut, liste) = self._query_generic(function, paramEtArg)

        if(statut == Constante.SORTIE_OK):
            return liste
        else:
            print("getListeMurs: statut["+ statut + "]")
            return []

    """
    methode retournant la liste des sols
    @return:  [(x1,y1), (x2, y2), ... (xn,yn)] de type [(int, int), ...(int, int)]
    """
    def getListeSols(self):
        function = Constante.QUERY_RECUPERER_LISTE_SOLS
        paramEtArg = []
        # recupere un flot d'octets
        (statut, liste) = self._query_generic(function, paramEtArg)

        if(statut == Constante.SORTIE_OK):
            return liste
        else:
            print("getListeSols: statut["+ statut + "]")
            return []

    """
    methode retournant la taille du plateau
    @return:  (taille_x, taille_y)
    """
    def getTaillePlateau(self):
        function = Constante.QUERY_RECUPERER_TAILLE_PLATEAU
        paramEtArg = []
        # recupere un flot d'octets
        (statut, taille) = self._query_generic(function, paramEtArg)

        if(statut == Constante.SORTIE_OK):
            return taille
        else:
            print("getTailleFenetre: statut["+ statut + "]")
            return (0,0)

    """
    methode retournant la position du but
    @return: (position_x, position_y) de type (int, int)
    """
    def getPositionBut(self):
        function = Constante.QUERY_RECUPERER_POSITION_BUT
        paramEtArg = []
        # recupere un flot d'octets
        (statut, liste) = self._query_generic(function, paramEtArg)

        if (statut == Constante.SORTIE_OK):
            return liste
        else:
            print("getPositionBut: statut["+ statut + "]")
            return []

    """
    methode retournant le nombre de case max
    @return: (nbre_case_max_x, nbre_case_max_y) de type (float, float)
    """
    def getNombreCaseMax(self):
        function = Constante.QUERY_RECUPERER_NOMBRE_CASE_MAX
        paramEtArg = []
        # recupere un flot d'octets
        (statut, case_max) = self._query_generic(function, paramEtArg)

        if (statut == Constante.SORTIE_OK):
            return (case_max)
        else:
            print("getNombreCaseMax: statut["+ statut + "]")
            return (0,0)

    """
    methode retournant la taille d'une case
    @return: (taille_x, taille_y)
    """
    def getTailleCase(self):
        function = Constante.QUERY_RECUPERER_TAILLE_CASE
        paramEtArg = []
        # recupere un flot d'octets
        (statut, taille) = self._query_generic(function, paramEtArg)

        if (statut == Constante.SORTIE_OK):
            return taille
        else:
            print("getTailleCase: statut["+ statut + "]")
            return (0,0)

    """
    methode pour s'inscrire
    @return: Constante.SORTIE_OK pour dire que l'ajout est fait, Constante.SORTIE_NOT_OK sinon
    """
    def inscriptionPartie(self, nomJoueur):
        function = Constante.QUERY_INSCRIPTION_PARTIE
        paramEtArg = [(Constante.ARG_JOUEUR_NOM, nomJoueur)]
        # recupere un flot d'octets
        (statut, reponse) = self._query_generic(function, paramEtArg)
        return (statut, reponse)

    """
    methode demandant au serveur de s'arreter
    @return: rien
    """
    def arretServeur(self):
        function = Constante.QUERY_ARRET_SERVEUR
        paramEtArg = []
        # recupere un flot d'octets
        (statut, reponse) = self._query_generic(function, paramEtArg)
        return statut

    """
    Methode generique pour faire une requete http. Le client ne l'appelle pas directement.
    Par exemple function="deplacement" et paramEtArg=('direction', 'N') entraine la requete suivante:
    "http://www.google.com/deplacement?direction=N"
    @param function: la fonction appelee en http
    @param paramEtArg: liste de (parametre, argument)
    @return le resultat de la requete realisee
    """
    def _query_generic(self, function, paramEtArg):
        nbrParam = 0;
        q = ""
        for (param, arg) in paramEtArg:
            q = q + param+'='+arg
            if nbrParam != len(paramEtArg)-1:
                nbrParam = nbrParam+1
                q = q + "&"

        print(self.base_address+function+'?'+q)
        f = urllib.request.urlopen(self.base_address+function+'?'+q)

        #print("result of the query:"+f.read())
        return ast.literal_eval(f.read().decode("utf-8"))

    def getClasseJoueur(self, nomJoueur):
        function = Constante.QUERY_RECUPERER_CLASSE_JOUEUR
        paramEtArg = [(Constante.ARG_JOUEUR_NOM, nomJoueur)]
        # recupere un flot d'octets
        reponse = self._query_generic(function, paramEtArg)

        return reponse
