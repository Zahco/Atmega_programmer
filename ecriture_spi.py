import spidev # Pour l'utilisation du spi import 
import RPi.GPIO as gpio # Pour 
import time
import string


# Constantes
pin_reset = 12
high = 1
low = 0
nb_octets = 1
mem = 8192  #Memoire flash = 8 kWords = 8192
masque = 0b1111111100000000
pause = 0.1
nb_mot_page = 64
cpt_nbl = 0
# =======================

# INITIALISATION

fich_txt = "prog.rom"


spi=spidev.SpiDev() # Creation de l'objet SPi
spi.open(0,0)	# Ouverture des pins
gpio.setmode(gpio.BOARD)
gpio.setup(pin_reset , gpio. OUT) # Pin en sortie
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
		
	print("Attente prog Enable : ")
	input()
	
	spi.writebytes([0xAC , 0x53 ])		# Instruc mode progEnable
	octet_retour_1 = spi.readbytes(2)
	print(octet_retour_1)

	print("Attente RAZ flash : ")
	input()	

	spi.writebytes([0xAC , 0x80 ,0 , 0 ]) # instruction Effac memoire flash

	# == RECUPERATION DATA DU FICHIER ==
	fichier = open(fich_txt , "r")
	nb_ligne = 0
	while fichier.readline():
		nb_ligne += 1			# Recuperation du nombre de ligne


	reste_page = nb_ligne % 64
	nb_pages = nb_ligne / 64
	nb_pages_total = nb_pages + 1
	print("Nb ligne du fichier : %d " % nb_ligne)	
	print("Nb page complete : %d " % nb_pages, "reste page a completer : %d " % reste_page)
	print("Nb page a remplir : %d " %  nb_pages_total)
	fichier.close()
	
	print("attente lancement programmation : ")
	input()

	fichier = open(fich_txt , "r")
	
	# == REMPLISSAGE PAGES COMPLETES ==
	for indice in range(0 , nb_pages):
		for indice_bis in range(0 , nb_mot_page):
			# == LECTURE DATA + ENVOI
			ligne = fichier.readline()
#			print(ligne)
			adr_data = ligne.split(":") # Recupere @ d'un cote et data de l'autre
			adr_l = adr_data[0]
			data_l = adr_data[1]
#			print(adr_data[1])
			adr_l = int(adr_l , 16)
			data_l = data_l.split('\r\n')	
			data_l[0] = int(data_l[0], 16)
	#		print(bin(adr_l) ,bin( data_l[0])) # Data extraites des lignes
			data_fort = data_l[0] & 0b1111111100000000	
			data_fort = data_fort >> 8
			data_faible = data_l[0] & 255
			adr_fort = adr_l & 0b1111111100000000
			adr_fort = adr_fort >>8
			adr_faible = adr_l & 255
#			print("Adr : ")
#			print(bin(adr_fort) , bin(adr_faible))
#			print("Data : ")
#		        print(bin(data_fort) ,bin( data_faible))
			spi.writebytes([0x40 , adr_fort , adr_faible , data_faible])
			spi.writebytes([0x48 , adr_fort , adr_faible , data_fort])
			cpt_nbl = cpt_nbl + 1
			print(hex(cpt_nbl - 1 ) , hex( data_fort) , hex( data_faible))

		num_grp = indice
		num_grp = num_grp << 6
		grp_haut = num_grp & 0b0001111100000000
		grp_haut = grp_haut >> 8
		grp_bas = num_grp & 0b11000000
#		print("page n : %d " % indice )
#		print("grp_haut : %s "  % bin( grp_haut), "  grp_bas : %s " %bin( grp_bas))
		spi.writebytes([0x4C , grp_haut ,grp_bas , 0]) # Ecriture du groupe
		

	 # ===================================================
	
	# == REMPLISSAGE DERNIERE PAGE NON COMPLETE ==
	for indice_bis in range(0 , reste_page):
                # == LECTURE DATA + ENVOI
        	ligne = fichier.readline()
#               print(ligne)
                adr_data = ligne.split(":") # Recupere @ d'un cote et data de l'au$
                adr_l = adr_data[0]
                data_l = adr_data[1]
#                print(adr_data[1])
                adr_l = int(adr_l , 16)
                data_l = data_l.split('\r\n')
                data_l[0] = int(data_l[0], 16)
     #          print(bin(adr_l) ,bin( data_l[0])) # Data extraites des lignes
                data_fort = data_l[0] & 0b1111111100000000
                data_fort = data_fort >> 8
                data_faible = data_l[0] & 255
                adr_fort = adr_l & 0b1111111100000000
                adr_fort = adr_fort >>8
                adr_faible = adr_l & 255
#               print("Adr : ")
#               print(bin(adr_fort) , bin(adr_faible))
#               print("Data : ")
#               print(bin(data_fort) ,bin( data_faible))
		spi.writebytes([0x40 , adr_fort , adr_faible , data_faible])
                spi.writebytes([0x48 , adr_fort , adr_faible , data_fort])
 #               adr_data[0] = 0
#                adr_data[1] = 0
		cpt_nbl = cpt_nbl + 1
                print(hex(cpt_nbl - 1 ) , hex( data_fort) , hex( data_faible))


	num_grp = nb_pages_total - 1 # Num de la derniere page
#	print("page n : %d " % num_grp)
        num_grp = num_grp << 6
        grp_haut = num_grp & 0b0001111100000000
        grp_haut = grp_haut >> 8
        grp_bas = num_grp & 0b11000000
#	print("grp_haut : %s "  % bin( grp_haut), "  grp_bas : %s " % bin( grp_bas))
	spi.writebytes([0x4C , grp_haut ,grp_bas , 0]) # Ecriture du groupe

	gpio.output(pin_reset , high)
	fichier.close()
	spi.close()
	print("Programme Done.")


except KeyboardInterrupt:
	spi.close()


