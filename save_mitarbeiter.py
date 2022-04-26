#!/usr/bin/env python
import time
import RPi.GPIO as GPIO 
from mfrc522 import SimpleMFRC522
import mysql.connector

db = mysql.connector.connect(
	host="localhost",
	user="zeiterfassungadmin",
	passwd="projectdatabase",
	database="Zeiterfassung"
)
cursor = db.cursor()
reader = SimpleMFRC522()

try:
	while True:
		print(" RFID-Karte vor Reader stellen")
		id, text = reader.read()
		cursor.execute("SELECT id FROM Mitarbeiter WHERE rfidnummer="+str(id))
		cursor.fetchone()
		if cursor.rowcount >= 1:
			print("Overwrite\nexiting mitarbeiter?")
			overwrite = input("overwrite (y/n)? ")

			if overwrite[0] == 'Y' or overwrite[0] == 'y':
				print("overwriting Mitarbeiter.")
				time.sleep(1)
				sql_insert = "UPDATE Mitarbeiter SET name = %s WHERE rfidnummer=%s"
			else:
				continue;
		else:
			sql_insert = "INSERT INTO Mitarbeiter (name,rfidnummer) VALUES (%s,%s)"
		print("enter new name")
		new_name = input("Name: ")

		cursor.execute(sql_insert,(new_name,id))

		db.commit()
		print("Mitarbeiter"+ new_name + "\nsaved")
		time.sleep(2)
finally:
	GPIO:cleanup()
