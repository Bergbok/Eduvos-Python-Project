 /*=============================================================
Filename: 1. Create_Database_And_Tables.sql
Programmer: Albertus Cilliers
Description: This file will create the database and tables with the necessary constraints.
=============================================================*/

DROP DATABASE IF EXISTS network_store;
CREATE DATABASE network_store;

USE network_store;

CREATE TABLE customers
(
	custId INT NOT NULL AUTO_INCREMENT,
	fname VARCHAR(40) NOT NULL,
	sname VARCHAR(40) NOT NULL,
	address VARCHAR(40) NOT NULL,
    phone VARCHAR(10) NOT NULL UNIQUE,
	PRIMARY KEY (custID)
);

CREATE TABLE items
(
	itemId INT NOT NULL AUTO_INCREMENT,
	iname VARCHAR(50) NOT NULL,
	descrip VARCHAR(100) NOT NULL,
	price FLOAT NOT NULL,
    count INT NOT NULL, 
	PRIMARY KEY (itemId)
);

CREATE TABLE invoices
(
	invoiceId INT NOT NULL AUTO_INCREMENT,
	custId INT NOT NULL,
	dateBought DATE NOT NULL,
	totalPrice VARCHAR(10) NOT NULL,
	PRIMARY KEY (invoiceId),
	FOREIGN KEY (custId) REFERENCES customers(custId) ON DELETE CASCADE
);