# Table of Contents
- [Installation and Setup](#installation-and-setup)
	- [Requirements](#Requirements)
		- [Python](#Python)
			- [Installation](#Installation-1)
		- [MySQL](#MySQL)
			- [Installation](#Installation-2)
			- [Additional Setup](#Additional-Setup)
- [Usage](#Usage)
- [Error Handling](#Error-Handling)
	- [Invoice files not found](#Invoice-files-not-found)
	- [Ensure MySQL is running](#Ensure-MySQL-is-running)
- [Screenshots](#Screenshots)
# Description
To learn more about the scenario this project is based on check out [the specification](https://github.com/Bergbok/Eduvos-Python-Project/blob/9cd4b5e750a53ce28da0446e6fd902dbba94a95b/Marksheet%20%26%20Specification/ITPYA0%20%E2%80%93%20Project%202%20Specification%202021%20(V3.0)%20(IS).pdf).

Consists of a [server](server.py) and a [client](client.py).   
The server waits for requests from clients and responds by interacting with a MySQL database and text files.    
The client takes user input and makes requests to the server. Features include: adding customers/items to the database, buying items and requesting invoices.
# Installation and Setup
## Requirements
### Python
#### Installation
- **Windows**: Download and use the Python installer from [the official website](https://www.python.org/downloads/). Make sure to check the box that says "**Add Python to PATH**" before you click on Install Now.
- **Linux**: Python is usually pre-installed on most Linux distributions. If you need to install it , use the package manager for your distribution using `sudo <your_package_manager> install python3`
### MySQL 
#### Installation
- **Windows**: Download an use the installer from [the official website](https://dev.mysql.com/downloads/installer/).
- **Linux**: Run `sudo <your_package_manager> install mysql-server`. After the installation, run the security script that comes with the installation `sudo mysql_secure_installation`
#### Additional Setup
##### Run setup scripts  
You'll need to run [1. Create_Database_And_Tables.sql](SQL%20Scripts/1.%20Create_Database_And_Tables.sql) and (optionally) [2. Sample_Data_Inserts.sql](SQL%20Scripts/2.%20Sample_Data_Inserts.sql).  
Two ways to run them are:
1. Open the scripts in MySQL Workbench and run them from there.
2. Open MySQL's command line client, and run `source <path>` (replace \<path> with the full path to the script).
##### Account Setup
Either: 
1. Change `self.db_username` and `self.db_password` in server.py to your MySQL root account credentials.
2. Create a MySQL user account using the credentials: `username = username` and `password = password`, and grant the account permissions by running `GRANT ALL PRIVILEGES ON network_store.* TO username@localhost IDENTIFIED BY 'password';` in MySQL's command line client.
# Usage
1. Open your terminal or command prompt.
2. `cd` to the directory where you saved [client.py](client.py) and [server.py](server.py)
3. Run `python server.py` then `python client.py`.
	- NOTE: Depending on your system setup, you might need to use `python3` instead of `python` to run your script.
# Error Handling
## Invoice files not found
Ensure you run the scripts from a consistent location since invoices get written to the cwd.
## Ensure MySQL is running
If MySQL isn't running, a variety of errors might occur. To ensure it's running:
- **Windows**: Press `Win + R`, type `services.msc`, look for MySQL and ensure it's running.
- **Linux**:  Run `sudo systemctl start mysql`
# Screenshots
## Registration (choice 1 & 2)
![Screenshots/Registration-(choice-1-and-2).jpg](Screenshots/Registration-(choice-1-and-2).jpg)
## Buying (choice 3)
![Screenshots/Buying-(choice-3).jpg](Screenshots/Buying-(choice-3).jpg)
## Invoice requesting (choice 4)
![Screenshots/Invoice-request-(choice-4).jpg](Screenshots/Invoice-request-(choice-4).jpg)
