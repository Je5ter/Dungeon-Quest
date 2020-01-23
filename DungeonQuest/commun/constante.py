# -*- coding: utf-8 -*-

class Constante:

    SERVER_BASE = ''
    SERVER_PORT = 8080

    CLIENT_BASE = '127.0.0.1'

    TAILLE_FENETRE = (1024,600)

    QUERY_RECUPERER_INFO_JOUEURS = "recupererInfoJoueurs"
    QUERY_RECUPERER_CLASSE_JOUEUR = "recupererClasseJoueur"
    QUERY_RECUPERER_TAILLE_PLATEAU = "recupererTaillePlateau"
    QUERY_RECUPERER_TAILLE_CASE = "recupererTailleCase"
    QUERY_RECUPERER_POSITION_BUT = "recupererPositionBut"
    QUERY_RECUPERER_NOMBRE_CASE_MAX = "recupererNombreCaseMax"
    QUERY_RECUPERER_LISTE_MURS = "recupererMurs"
    QUERY_RECUPERER_LISTE_SOLS = "recupererSols"
    QUERY_ARRET_SERVEUR = "arretServeur"

    QUERY_PARTIE_CREER = "partieCreer"
    QUERY_PARTIE_CHANGER_ETAT = "partieChangerEtat"
    ARG_PARTIE_NOM = "nomPartie"
    ARG_PARTIE_ETAT = "etat"

    QUERY_INSCRIPTION_PARTIE = "inscriptionPartie"
    ARG_JOUEUR_NOM = "nomJoueur"

    QUERY_DEPLACEMENT = "deplacement"
    ARG_DEPLACEMENT_DIRECTION = "direction"
    SORTIE_OK = "O"
    SORTIE_NOT_OK = "N"
    SORTIE_ERROR = "E"
    SORTIE_PARTIE_PERDUE = "L"
    SORTIE_PARTIE_GAGNE = "Y"

    ETAT_INSCRIPTION_OUVERTE = 0
    ETAT_INSCRIPTION_FERMEE = 1
    ETAT_PARTIE_COMMENCEE = 2
    ETAT_PARTIE_FINIE = 3
