import spidev # Pour l'utilisation du spi import 
import RPi.GPIO as gpio # Pour 
import time



# Constantes
pin_reset = 12
high = 1
low = 0
nb_octets = 1
mem = 8192  #Memoire flash = 8 kWords = 8192
masque = 0b1111111100000000
pause = 0.1
# =======================

# INITIALISATION
spi=spidev.SpiDev() # Creation de l'objet SPi
spi.open(0,0)	# Ouverture des pins
gpio.setmode(gpio.BOARD)
gpio.setup(pin_reset , gpio.OUT) # Pin en sortie
spi.max_speed_hz = 50000
# ========================


try:
	# == Mise en mode prog ==
	gpio.output(pin_reset , low)
	gpio.output(pin_reset , high)
	time.sleep(0.5)
	gpio.output(pin_reset , low) 
	time.sleep(pause)
	# =======================

	# == Instruction Prog Enable ==
	spi.writebytes([0xAC , 0x53 ]) # Instruction Programme Enable
#	time.sleep(pause)
	octet_retour_1 = spi.readbytes(nb_octets)
#	time.sleep(pause)
	octet_retour_2 = spi.readbytes(nb_octets)
	if octet_retour_1 == 83 and octet_retour_2 == 0 : print('OK')
	else : print('NOK')
	# =============================

	print("Appuyer sur le clavier :")
	input()

	# == LECTURE DES DATAS ==
	for i in range(0 , mem):	# lecture en boucle des datas
                PFo_adr = i & masque 	# Recupere @Pfort sur 16 bits 
		PFo_adr = PFo_adr >> 8	# Decalage pour @PFort sur 8 bits
		PFa_adr = i & 255	# Masque pour @PFaible sur 8 bits
		print("L'@ courante est : %s " % hex(i))
		print("Poids fort : %s " % bin(PFo_adr))
		print("Poids faible : %s " % bin(PFa_adr))
 		spi.writebytes([0x20 , PFo_adr , PFa_adr ])	# instruction lecture data Pfaible
		data_PFa = spi.readbytes(nb_octets)
		spi.writebytes([0x28 , PFo_adr , PFa_adr ])	# instruction lecture data PFort
		data_PFo = spi.readbytes(nb_octets)
		print("les datas sont en %s sont : " % hex(i) )
		print(data_PFo , data_PFa)
		time.sleep(pause)
	# =======================

	spi.close()


except KeyboardInterrupt:
	spi.close()


