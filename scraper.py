# -*- coding: utf-8 -*-
import soundcloud
import json
import sys
from collections import deque
import time


#creo client soundcloud

clientId = sys.argv[1]
firstId = int(sys.argv[2])

# se il clientid e' vuoto, ritorno
if(clientId == None or firstId == None):
	print "ClientId or UserId missing"
	sys.exit(0)

client = soundcloud.Client(client_id=clientId)

#creo coda con utenti da visitare
queue = deque([])
#creo lista con dati degli utenti
userData = []
#creo lista con dati su nodi visitati
visited = []

#contatore di quanti elementi sono stati staricati
cont = 0

print "Working..."


#definisco funzione per ottenere i dati dell'utente
def getData(firstId):

	#coso variabile globale
	global cont

	#apro files
	edge_list = open("edge_list.txt","a")
	user_data = open("user_data.txt","a")

	#Inserisco il primo elemento nella coda
	queue.append(firstId)

	while len(queue) > 0:

		#poppo il primo elemento della coda
		userId = queue.popleft()

		try:
			users = client.get('/users/%d' % userId)
		except Exception as e:
			print "Error "+str(e)+"found! Sleeping..."
			time.sleep(600)
			queue.appendleft(userId)
			continue

		#aggiungo nodo a lista visitati
		visited.append(users.id)


	#se non sono presenti dati sull'utente corrente, li aggiungo
	#for data in userData:
		#if data['id']!=userId:
			#aggiungo user alla lista visitati
			
		if cont == 0:
			temp = {'id':users.id, 'country':users.country, 'tracks': users.track_count,'playlists':users.playlist_count}
			userData.append(temp)
			user_data.write(str(temp)+",")
			cont = cont + 1


	#Se la lunghezza della coda e' maggiore di 5000, ritorno la funzione (per far finire la ricorsione)
	#if len(queue) > 200000:
	#	return

	#ottengo lista followers e lista followed
		try:
			followers = client.get('/users/%d/followers' % userId)
			followings = client.get('/users/%d/followings' % userId)
		except Exception as e:
			print "Error "+str(e)+"found! Sleeping..."
			#errore trovato. reinserisco il valore nella coda (subito a sinistra) e ripeto il ciclo
			time.sleep(600)
			queue.appendleft(userId)
			continue

		#Aggiungo dati followers:
		for user in followers.collection:
			#aggiungo dati follower nella lista
			temp = {'id':user.id, 'country':user.country, 'tracks': user.track_count,'playlists':user.playlist_count}
		
			if temp not in userData:
				userData.append(temp)
				user_data.write(str(temp)+",")
		
			#aggiungo i link nel file
			edge_list.write(str(user.id)+","+str(userId)+"\n")
			#incremento contatore
			cont = cont + 1
		
			#controllo se l'utente è già presente nella lista dei visitati: se no, lo aggiungo nella coda
			if user.id not in visited and user.id not in queue:
				queue.append(user.id)


		#Aggiungo dati followings:
		for user in followings.collection:
			#aggiungo dati follower nella lista
			temp = {'id':user.id, 'country':user.country, 'tracks': user.track_count,'playlists':user.playlist_count}
	 
			if temp not in userData:
				userData.append(temp)
				user_data.write(str(temp)+",")

			#aggiungo i link nel file
			edge_list.write(str(userId)+","+str(user.id)+"\n")
			cont = cont + 1

			#controllo se l'utente è già presente nella lista dei visitati: se no, lo aggiungo nella coda
			if user.id not in visited and user.id not in queue:
				queue.append(user.id)

		#stampo quanti nodi ho recuperato
		print("Fetched %d users\r" % cont)


		#sleeppo la funzione
		time.sleep(1)



getData(firstId)
print("Fetched %d users" % cont)
