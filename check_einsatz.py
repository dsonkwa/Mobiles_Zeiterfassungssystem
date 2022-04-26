
import time
import datetime 
import  RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector
# creer ca dans un autre fichier pour les donnees ci-bas

db = mysql.connector.connect(
	host="localhost",
	user="zeiterfassungadmin",
	passwd= "projectdatabase",
	database = "Zeiterfassung"
)

cursor = db.cursor(buffered=True) #buffered permet dutiliser le cursor chaque fois 
reader = SimpleMFRC522()
current_time = datetime.datetime.now()
print(type(current_time))

eingestempelt=False
try:
	while True:
		#current_time = datetime.datetime.now()
		print("Ihre Karte bitte vor Reader stellen")
		id, text = reader.read()
		cursor.execute("Select id,name FROM Mitarbeiter WHERE rfidnummer="+str(id))
		result = cursor.fetchone()
		print(result[0])
		if cursor.rowcount >= 1:
			print("Willkommen "+result[1])
			cursor.execute("select id from Einsatz where mitarbeiter_ID=%s and datum=date(%s)",(result[0],datetime.datetime.now() ))
			exist= cursor.fetchone()
			if cursor.rowcount >= 1:
				print(result[0])
				print("overwriting Anfangs- bzw. Endzeit\n Welche Zeit wollen Sie ändern?\n Anfangszeit(1)oder Endzeit(2)")
				response = input("1 oder 2\n")
				if response[0]=="1":
					cursor.execute("UPDATE Einsatz SET anfangszeit = %s WHERE mitarbeiter_ID=%s AND datum=date(%s)",
													(datetime.datetime.now(),result[0],datetime.datetime.now()))
					db.commit()
				elif response[0]=="2":
					cursor.execute("UPDATE Einsatz SET endzeit=%s WHERE mitarbeiter_ID=%s AND datum=date(%s)",
													(datetime.datetime.now(),result[0],datetime.datetime.now()))
				db.commit()
			else:
				print ("Wollen sie einstempeln(1)oder ausstempeln(2)?")
				eingabe = input("1 oder 2\n")
				if eingabe[0]=="1":
			#	cursor.execute("select anfangszeit from Einsatz where datum=select "+str(now()))
					cursor.execute("INSERT INTO Einsatz(mitarbeiter_ID,anfangszeit,datum) VALUES (%s,%s,%s)",(result[0],datetime.datetime.now(),
																datetime.datetime.now()))
					eingestempelt = True
					db.commit()
				#elif eingabe[0]=="2":
				#	print("on est dans le elif")
				#	if eingestempelt==True:
				#		print("on sest eingestempelt")
					#cursor.execute("UPDATE Einsatz SET endzeit = %s WHERE mitarbeiter_ID=%s AND isnull(endzeit)=1",(datetime.datetime.now(),
					#												result[0]) ) #(mitarbeiter_ID,endzeit) VALUES (%s,%s)",(result[0],datetime.datetime.now() ))
				#		cursor.execute("UPDATE Einsatz SET endzeit = %s WHERE mitarbeiter_ID=%s AND datum = date(%s)",(datetime.datetime.now(),
				#												result[0],datetime.datetime.now()))
				#		db.commit()
				#else:
				#	print("Wählen Sie 1 oder 2 aus")
			#	cursor.execute("UPDATE Einsatz SET anfangszeit")
				#	eingestempelt=False
		else:
			print("Mitarbeiter doesn't exist. Sie sollen sich erstmals registrieren")
		time.sleep(2)
finally:
	GPIO.cleanup()
