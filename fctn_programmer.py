# ============================================================ #
#       Filename : fctn_programmer.py
#       Date : 17/09/2016
#       File Version : 1.0
#       Written by : JorisP30
#       Function : fichier contenant les functions du programmer
# ============================================================ #

# == Importation des modules ==
import spidev # Pour l'utilisation du spi import
import RPi.GPIO as gpio # Pour l'utilisation des E/S
import time
# ============================

# == Initialisation du SPI , Obligatoire ==
spi=spidev.SpiDev() # Creation de l'objet SPi
spi.open(0,0)   # Ouverture des pins
spi.max_speed_hz = 50000
gpio.setmode(gpio.BOARD)
# =========================================


def off_on_rst(pin_reset):
	gpio.setup(pin_reset , gpio.OUT)
	gpio.output(pin_reset , 0)
	gpio.output(pin_reset , 1)
	time.sleep(0.5)
	gpio.output(pin_reset , 0)
	time.sleep(0.1)
	print("Onn Off Pin Reset Done.")

def prgm_enable(octet_1 , octet_2):
	spi.writebytes([octet_1 , octet_2])
	octets_retour = spi.readbytes(2) # Lecture des 2 derniers octets de retour
	print(octets_retour)
	print("Programming Enable Done.")

def chip_erase(octet_1 , octet_2 , octet_3 , octet_4):
	spi.writebytes([octet_1 , octet_2 , octet_3 , octet_4])
	print("Chip Erase Done.")

def read_prg_mem_HB(octet_1 , adr_MSBy , adr_LSBy):
	spi.writebytes([octet_1 , adr_MSBy , adr_LSBy ])
	data_MSBy = spi.readbytes(1)
	print("@ : %s %s : %s " ,  % (adr_MSBy ,  adr_LSBy , data_MSBy))
#	print(adr_MSBy ,adr_LSBy , data_MSBy)
	print("Read program memory High Byte Done.")

def read_prg_mem_LB(octet_1 , adr_MSBy , adr_LSBy):
	spi.writebytes([octet_1 , adr_MSBy , adr_LSBy])
	data_LSBy = spi.readbytes(1)
	print(adr_MSBy , adr_LSBy , data_LSBy)
        print("Read program memory Low Byte Done.")
