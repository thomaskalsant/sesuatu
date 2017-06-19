import sqlite3

conn = sqlite3.connect('sepatu.db')
print "Opened database successfully";

conn.execute('CREATE TABLE pesan (pesanId INTEGER PRIMARY KEY AUTOINCREMENT, sepatuId int(12) NOT NULL, userId int(12) NOT NULL)')

conn.execute('CREATE TABLE sepatu (sepatuId INTEGER PRIMARY KEY AUTOINCREMENT, name varchar(128) NOT NULL, description varchar(512) NOT NULL, imageUrl varchar(512) NOT NULL, ukuran int(2) NOT NULL, price decimal(12,0) NOT NULL)')

conn.execute('CREATE TABLE user (userId INTEGER PRIMARY KEY AUTOINCREMENT, email varchar(128) NOT NULL, password varchar(512) NOT NULL)')

print "Table created successfully";
conn.close()

