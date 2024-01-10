/*===============================AT==================================== 
Filename: 2. Sample_Data_Inserts.sql
Programmer: Albertus Cilliers
Description: This file will insert sample data into the database.
=====================================================================*/
USE network_store;

INSERT INTO customers(fname, sname, address, phone)
VALUES('Albertus','Cilliers','The middle of nowhere','0844023335'),
	  ('Sherlock','Holmes','221B Baker St., London','0212218888'),
	  ('Spongebob','Squarepants','124 Conch Street, Bikini Bottom','0219750319'),
	  ('Homer','Simpson','742 Evergreen Terrace, Springfield, USA','0219751329'),
	  ('Peter','Griffin','31 Spooner Street, Quahog, Rhode Island','0810435274');
      
INSERT INTO items(iname, descrip, price, count)
VALUES('Jackhammer','Pneumatic or electro-mechanical tool that combines a hammer directly with a chisel',19999.99, 10),
	  ('Forklift','A powered industrial truck used to lift and move materials over short distances',1750000,3),
	  ('Wet Grinder','A grinder that uses water either to soften the product ground or to keep the grinding elements cool',4200,15),
	  ('Hammer','Weighted head fixed to a long handle, swung to deliver an impact to a small area of an object',250,100),
      ('Crowbar','A lever consisting of a metal bar with a single curved end and flattened points',420.69,69);

INSERT INTO invoices(custId, dateBought, totalPrice)
VALUES(1,'2021-03-03','R420.69'),
	  (2,'2021-05-21','R250'),
	  (3,'2022-03-03','R4200'),
	  (4,'2023-12-25','R1750000'),
      (5,'2023-03-03','R19999.99');