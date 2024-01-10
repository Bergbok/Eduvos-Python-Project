# Table of Contents
- [Installation and Setup](#installation-and-setup)
	- [Requirements](#Requirements)
		- [Python](#Python)
		- [MySQL](#MySQL)
# Description
# Installation and Setup
## Requirements
### Python
#### Installation
- **Windows**: Download the Python installer from [the official website](https://www.python.org/downloads/). Make sure to check the box that says "**Add Python to PATH**" before you click on Install Now.
- **Linux**: Python is usually pre-installed on most Linux distributions. If you need to install it , use the package manager for your distribution using `sudo <your_package_manager> install python3`
### MySQL 
#### Installation
- **Windows**: Download an use the installer from [the official website](https://dev.mysql.com/downloads/installer/).
- **Linux**: Run `sudo <your_package_manager> install mysql-server`. After the installation, run the security script that comes with the installation `sudo mysql_secure_installation`
#### Additional Setup
##### Run setup scripts
You'll need to run `1. Create_Database_And_Tables.sql` and `2. Sample_Data_Inserts.sql`.
Two ways to run them are:
1. Open the scripts in MySQL Workbench and run them from there.
2. Open MySQL's command line client, and run `source <path>` (replace \<path> with the full path to the script).
##### Account Setup
Either: 
1. Change `self.db_username` and `self.db_password` in server.py to your MySQL root account credentials.
2. Create a MySQL user account using the credentials: `username = username` and `password = password`, and grant the account permissions by running `GRANT ALL PRIVILEGES ON network_store.* TO username@localhost IDENTIFIED BY 'password';` in MySQL's command line client.
# Usage
1. Open your terminal or command prompt.
2. `cd` to the directory where you saved client.py and server.py
3. Run `python server.py` then `python client.py`.
	- NOTE: Depending on your system setup, you might need to use `python3` instead of `python` to run your script.
# Error Handling
## Ensure MySQL is running
- **Windows**: Press `Win + R`, type `services.msc`, look for MySQL and ensure it's running.
- **Linux**:  Run `sudo systemctl start mysql`
# Screenshots
