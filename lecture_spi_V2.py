# ============================================================ #
#       Filename : lecture_spi_V2.py
#       Date : 17/09/2016
#       File Version : 1.0
#       Written by : JorisP30
#       Function : Lecture des donnees de la memoire flash dans l'Atmega
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
# ================

fctn_programmer.off_on_rst(pin_reset) # 
print("Attente suite")
input()
fctn_programmer.prgm_enable(0xAC , 0x53)
print("Attente suite")
input()

for i in range(0 , mem):
	adr_MSBy = i & masque    	# Recupere @Pfort sur 16 bits
        adr_MSBy  = adr_MSBy >> 8  	# Decalage pour @PFort sur 8 bits
        adr_LSBy = i & 255       	# Masque pour @PFaible sur 8 bits
	print("@ : %s %s " % (hex( adr_MSBy) ,hex( adr_LSBy) ))
	fctn_programmer.read_prg_mem_LB(0x20 , adr_MSBy , adr_LSBy)
	fctn_programmer.read_prg_mem_HB(0x28 , adr_MSBy , adr_LSBy)

spi.close()
print("Lecture mem flash Done.")
