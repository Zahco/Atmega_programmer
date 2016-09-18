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
	print("Data_MSBy : %s "   % data_MSBy)
#	print("Read program memory High Byte Done.")

def read_prg_mem_LB(octet_1 , adr_MSBy , adr_LSBy):
	spi.writebytes([octet_1 , adr_MSBy , adr_LSBy])
	data_LSBy = spi.readbytes(1)
	print("Data_LSBy : %s "  % data_LSBy)
#       print("Read program memory Low Byte Done.")

def recup_infos_fichier(fich_txt):
	fichier = open(fich_txt , "r")
	nb_ligne = 0
	while fichier.readline():
		nb_ligne += 1
	
	reste_page = nb_ligne % 64
	nb_page_complete = nb_ligne / 64
	nb_page_totale = nb_page_complete + 1
	print("Nb de ligne du fichier : %d " % nb_ligne)
	print("Nb de page complete : %s , Reste de la derniere page a completer : %s " % (nb_page_complete , reste_page ))
	print("Nb de pages a remplir : %s " % nb_page_totale)	
	fichier.close()
	print("Recup infos fichier Done.")
	return nb_page_complete , reste_page , nb_page_totale


def progr_flash(fich_txt , nb_page_complete , reste_page , nb_mot_page, nb_page_totale):
	fichier = open(fich_txt , "r")
	cpt_nbl = 0
	for indice in range(0 , nb_page_complete):
		for indice_bis in range(0 , nb_mot_page):
			ligne = fichier.readline()
			adr_data = ligne.split(":") # Recupere @ d'un cote et data de l'au$
                        adr_l = adr_data[0]
                        data_l = adr_data[1]
			adr_l = int(adr_l , 16)
                        data_l = data_l.split('\r\n')
                        data_l[0] = int(data_l[0], 16)
			data_fort = data_l[0] & 0b1111111100000000
                        data_fort = data_fort >> 8
                        data_faible = data_l[0] & 255
                        adr_fort = adr_l & 0b1111111100000000
                        adr_fort = adr_fort >>8
                        adr_faible = adr_l & 255
			spi.writebytes([0x40 , adr_fort , adr_faible , data_faible])
                        spi.writebytes([0x48 , adr_fort , adr_faible , data_fort])
                        cpt_nbl = cpt_nbl + 1
			print(" %s : %s %s " % ( hex(cpt_nbl - 1) , hex(data_fort) , hex(data_faible)))

		num_grp = indice
                num_grp = num_grp << 6
                grp_haut = num_grp & 0b0001111100000000
                grp_haut = grp_haut >> 8
                grp_bas = num_grp & 0b11000000
		spi.writebytes([0x4C , grp_haut ,grp_bas , 0]) # Ecriture du groupe

	for indice_biss in range(0 , reste_page):
		ligne = fichier.readline()
		adr_data = ligne.split(":") # Recupere @ d'un cote et data de l'au$
		adr_l = adr_data[0]
		data_l = adr_data[1]
		adr_l = int(adr_l , 16)
		data_l = data_l.split('\r\n')
		data_l[0] = int(data_l[0], 16)
		data_fort = data_l[0] & 0b1111111100000000
		data_fort = data_fort >> 8
		data_faible = data_l[0] & 255
		adr_fort = adr_l & 0b1111111100000000
		adr_fort = adr_fort >>8
		adr_faible = adr_l & 255
		spi.writebytes([0x40 , adr_fort , adr_faible , data_faible])
		spi.writebytes([0x48 , adr_fort , adr_faible , data_fort])
		cpt_nbl = cpt_nbl + 1
		print("%s : %s %s " % (hex(cpt_nbl - 1 ) , hex(data_fort) , hex(data_faible)))
		
	num_grp = nb_page_totale - 1 # Num de la derniere page
        num_grp = num_grp << 6
        grp_haut = num_grp & 0b0001111100000000
        grp_haut = grp_haut >> 8
        grp_bas = num_grp & 0b11000000
        spi.writebytes([0x4C , grp_haut ,grp_bas , 0]) # Ecriture du groupe
        fichier.close()
        spi.close()
        print("Programme mem flash Done.")
