# -*- coding: utf-8 -*-

from labyrinthS.traitementRequete import TraitementRequete
from labyrinthS.serveur import Serveur
from commun.constante import Constante

#try:
#    
#    #creation du serveur
#    # lien avec la classe instanciee pour chaque requete du client
#    # - le client fait une requete http
#    # - le serveur cree un objet de type TraitementRequete
#    # - l'objet TraitementRequete execute sa fonction do_GET(self)
#    # - l'objet TraitementRequete est detruit
#  
#    #creation du serveur
#    print ('', str(Constante.SERVER_PORT))
#    serverMine = Serveur((Constante.SERVER_BASE, Constante.SERVER_PORT), TraitementRequete)
#    
#    print ('Serveur demarre sur le port ' , Constante.SERVER_PORT)
#  
#    #en attente des requetes du client
#    serverMine.serve_forever()
#
#except KeyboardInterrupt:
#    serverMine.server_close()
#    print ('^C recu, arret du serveur')
#    
def lancerServeur():
    try:
        
        #creation du serveur
        # lien avec la classe instanciee pour chaque requete du client
        # - le client fait une requete http
        # - le serveur cree un objet de type TraitementRequete
        # - l'objet TraitementRequete execute sa fonction do_GET(self)
        # - l'objet TraitementRequete est detruit
      
        #creation du serveur
        print ('', str(Constante.SERVER_PORT))
        serverMine = Serveur((Constante.SERVER_BASE, Constante.SERVER_PORT), TraitementRequete)
        
        print ('Serveur demarre sur le port ' , Constante.SERVER_PORT)
      
        #en attente des requetes du client
        #serverMine.serve_forever()
        
        
        while serverMine.mustStop != True:
            serverMine.handle_request()
        
        print ("arret du serveur")
        
    except KeyboardInterrupt:
        serverMine.server_close()
        print ('^C recu, arret du serveur')

