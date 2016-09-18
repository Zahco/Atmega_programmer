# ============================================================ #
#       Filename : ecriture_spi_V2.py
#       Date : 17/09/2016
#       File Version : 1.0
#       Written by : JorisP30
#       Function : Ecriture des donnees de la memoire flash dans l'Atmega
# ============================================================ #


# == Importation des modules ==
import spidev # Pour l'utilisation du spi import
import RPi.GPIO as gpio # Pour utiliser les E/S
import time     # pour les tempos
import sys
import fctn_programmer # Fonctions
# ============================

# == INITIALISATION SPI GPIO ==
spi=spidev.SpiDev() # Creation de l'objet SPi
spi.open(0,0)   # Ouverture des pins
spi.max_speed_hz = 50000
# ============================

# == Constantes ==
pin_reset = 12  # Pin RAZ atmega
mem = 8192  #Memoire flash = 8 kWords = 8192
masque = 0b1111111100000000
pause = 0.1
fich_txt = "prog.rom"
nb_mot_page = 64
high = 1
low = 0
# ================

fctn_programmer.off_on_rst(pin_reset) # 
print("Attente suite")
input()

fctn_programmer.prgm_enable(0xAC , 0x53)
print("Attente suite")
input()

nb_page_complete , reste_page , nb_page_totale = fctn_programmer.recup_infos_fichier(fich_txt)
print(nb_page_complete , reste_page , nb_page_totale)
print("Attente suite")
input()

fctn_programmer.progr_flash(fich_txt , nb_page_complete , reste_page , nb_mot_page , nb_page_totale)

gpio.output(pin_reset , high)
spi.close()
print("Programmation memoire flash Done.")
