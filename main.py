'''
Created on Sep 1, 2016

@author: antoi_000
'''
import kivy
import os

kivy.require('1.9.1') # replace with your current kivy version !

from kivy.app import App

from labyrinthC.controleur import Controleur
from commun.constante import Constante

class LabyApp(App):

    def build(self):

        controleur = Controleur()

        return controleur.vue



if __name__ == '__main__':
    os.environ["http_proxy"]=""
    os.environ["https_proxy"]=""
    os.environ["HTTP_PROXY"]=""
    os.environ["HTTPS_PROXY"]=""
    labyApp = LabyApp()
    labyApp.run()
