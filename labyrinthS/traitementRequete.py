#!/usr/bin/python
# -*- coding: utf-8 -*-


'''
Created on 3 Jul 2013

@author: pigeau-a
'''

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from labyrinthS.joueur import Joueur, Aventurier, Chasseur
from commun.constante import Constante
import random

# def not_insane_address_string(self):
#         host, port = self.client_address[:2]
#         return '%s (no getfqdn)' % host #used to call: socket.getfqdn(host)
#
# BaseHTTPRequestHandler.address_string = not_insane_address_string


#This class will handles any incoming request from
#the browser
class TraitementRequete(BaseHTTPRequestHandler):

#     def address_string(self):
#         '''
#         fonction à ajouter pour gérer le bug (temps de latence pour obtenir une réponse du serveur)
#         '''
#         host, port = self.client_address[:2]
#         #return socket.getfqdn(host)
#         return host

    def setDelay(self):
        return 0.0

    #Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Send the html message

        #print ("serveur version "+str(self.server_version))

        reponse = (Constante.SORTIE_OK, "le serveur fonctionne")
        error = False

        #parser la requete pour la diviser
        decoupageRequete = urlparse(self.path)

        #recuperer la requete
        nomFonction = decoupageRequete.path.rpartition('/')[2]

        #recuperer les parametres
        parametres = parse_qs(decoupageRequete.query)


        print (self.path)
        print ("nom de la fonction:",str(nomFonction))
        print ("parametres:",str(parametres))
        if 'direction' in parametres:
            arg_direction = parametres.get('direction')
            print("arg_direction "+str(arg_direction))
            direction = arg_direction[0]
            print ("direction "+str(direction))


        """
        ####################################
        QUERY_DEPLACEMENT
        ####################################
        """
        if nomFonction == Constante.QUERY_DEPLACEMENT:

            if Constante.ARG_DEPLACEMENT_DIRECTION in parametres:
                arg_direction = parametres[Constante.ARG_DEPLACEMENT_DIRECTION]
                direction = arg_direction[0]
            else:
                print(Constante.QUERY_DEPLACEMENT + " aucune direction")
                error = True

            if Constante.ARG_JOUEUR_NOM in parametres:
                arg_nom = parametres[Constante.ARG_JOUEUR_NOM]
                nomJoueur = arg_nom[0]
            else:
                print(Constante.QUERY_DEPLACEMENT + " aucun nom de joueur")
                error = True

            reponse = (Constante.SORTIE_ERROR, 0)

            if not error:
                print("requete deplacement - argument direction:", arg_direction[0])

                partie = self.server.partie

                if partie.etat == Constante.ETAT_PARTIE_FINIE:
                    print(Constante.QUERY_DEPLACEMENT + " la partie est finie")
                    reponse = (Constante.SORTIE_PARTIE_PERDUE, 0)
                    self.server.mustStop = True

                if partie.etat == Constante.ETAT_PARTIE_COMMENCEE:
                    if nomJoueur in partie.joueurs:
                        joueur = partie.recupererJoueur(nomJoueur)
                        reponse = partie.deplacement(direction, joueur)
                        print(reponse)
                    else:
                        print(Constante.QUERY_DEPLACEMENT + " le joueur " + nomJoueur + " n'existe pas dans la partie ")


        """
        ####################################
        QUERY_INSCRIPTION_PARTIE
        ####################################
        """
        if nomFonction == Constante.QUERY_INSCRIPTION_PARTIE:

            if Constante.ARG_JOUEUR_NOM in parametres:
                arg_nom = parametres[Constante.ARG_JOUEUR_NOM]
                nomJoueur = arg_nom[0]
            else:
                error = True
                print(Constante.QUERY_INSCRIPTION_PARTIE + " aucun nom de joueur")

            reponse = (Constante.SORTIE_ERROR, 0)

            if not error:
                partie = self.server.partie
                #Test si aucun joueur n'est encore inscrit (dictionnaire joueurs vide)
                items = [(3,1),(3,18),(30,1),(30,18)]
                rand_item = random.choice(items)
                if len(partie.joueurs) == 0:
                    joueur = Aventurier(nomJoueur, rand_item, "bas")
                    print(joueur.classeJoueur)
                elif len(partie.joueurs) > 0:
                    joueur = Chasseur(nomJoueur, (15, 10), "bas")
                    print(joueur.classeJoueur)
                #Test si le joueur est déjà présent
                if not partie.estDejaAjouter(joueur):
                    partie.ajouterJoueur(joueur)
                    reponse = (Constante.SORTIE_OK, 0)
                else:
                    print(Constante.QUERY_INSCRIPTION_PARTIE + " le joueur " + nomJoueur + " est deja present")
                    reponse = (Constante.SORTIE_NOT_OK, 0)

        """
        ####################################
        QUERY_RECUPERER_TAILLE_PLATEAU
        ####################################
        """
        if nomFonction == Constante.QUERY_RECUPERER_TAILLE_PLATEAU:
            partie = self.server.partie
            reponse = ( Constante.SORTIE_OK, (partie.taillePlateauX, partie.taillePlateauY))
            #reponse = str(reponse)
            print(reponse)


        """
        ####################################
        QUERY_x
        ####################################
        """
        if nomFonction == Constante.QUERY_ARRET_SERVEUR:
            self.server.mustStop = True
            reponse = (Constante.SORTIE_OK, 0)

        """
        ####################################
        QUERY_RECUPERER_TAILLE_CASE
        ####################################
        """
        if nomFonction == Constante.QUERY_RECUPERER_TAILLE_CASE:
            partie = self.server.partie
            reponse = (Constante.SORTIE_OK, partie.tailleCase)

        """
        ####################################
        QUERY_RECUPERER_POSITION_BUT
        ####################################
        """
        if nomFonction == Constante.QUERY_RECUPERER_POSITION_BUT:
            partie = self.server.partie
            reponse = (Constante.SORTIE_OK, partie.positionBut)

        """
        ####################################
        QUERY_RECUPERER_NOMBRE_CASE_MAX
        ####################################
        """
        if nomFonction == Constante.QUERY_RECUPERER_NOMBRE_CASE_MAX:
            partie = self.server.partie
            reponse = (Constante.SORTIE_OK, (partie.positionBut[0], partie.positionBut[1]))

        """
        ####################################
        QUERY_RECUPERER_LISTE_MURS
        ####################################
        """
        if nomFonction == Constante.QUERY_RECUPERER_LISTE_MURS:
            partie = self.server.partie
            reponse = (Constante.SORTIE_OK, partie.murs)

        """
        ####################################
        QUERY_RECUPERER_LISTE_SOLS
        ####################################
        """
        if nomFonction == Constante.QUERY_RECUPERER_LISTE_SOLS:
            partie = self.server.partie
            reponse = (Constante.SORTIE_OK, partie.sols)

        """
        ####################################
        QUERY_RECUPERER_INFO_JOUEURS
        ####################################
        """
        if nomFonction == Constante.QUERY_RECUPERER_INFO_JOUEURS:
            partie = self.server.partie
            reponse = (Constante.SORTIE_OK, partie.recupererInfoJoueurs())
            print(str(reponse))

        """
        ####################################
        QUERY_RECUPERER_CLASSE_JOUEUR
        ####################################
        """
        if nomFonction == Constante.QUERY_RECUPERER_CLASSE_JOUEUR:

            if Constante.ARG_JOUEUR_NOM in parametres:
                arg_nom = parametres[Constante.ARG_JOUEUR_NOM]
                nomJoueur = arg_nom[0]
            else:
                error = True
                print(Constante.QUERY_RECUPERER_CLASSE_JOUEUR + " aucun nom de joueur")

            reponse = (Constante.SORTIE_ERROR, 0)

            if not error:

                partie = self.server.partie

                if nomJoueur in partie.joueurs:
                    joueur = partie.recupererJoueur(nomJoueur)
                    reponse = joueur.classeJoueur
                    print(reponse)
                else:
                    print(Constante.QUERY_DEPLACEMENT + " le joueur " + nomJoueur + " n'existe pas dans la partie ")

        """
        ####################################
        ####################################
        retour de la reponse - ne pas supprimer
        ####################################
        ###################################
        """

        self.wfile.write(bytes(str(reponse),'utf-8'))

        return
