# Filename: client.py
# Description: Menu driven console client for interacting with related server application

import socket
import json

class Client:
  def __init__(self, host, port, bufsize = 100000, timeout = 10):
    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.host = host
    self.port = port
    self.bufsize = bufsize
    self.timeout = timeout
    
  def connect(self):
    self.client.connect((self.host,self.port))
    
  def close(self):
    self.client.close()
    
  def send(self, string):
    self.client.send(bytes(string,"ascii"))
    
  def recv(self):
    return str(self.client.recv(self.bufsize),encoding="ascii")

def print_menu():
    menu_string = "=================================\n"
    menu_string += "|          NETWORK STORE        |\n"
    menu_string += "=================================\n"
    menu_string += "| 1. Register Customer          |\n"
    menu_string += "| 2. Register Item              |\n"   
    menu_string += "=================================\n"
    menu_string += "| 3. Buy Items                  |\n"
    menu_string += "| 4. Request Invoice            |\n"
    menu_string += "=================================\n"
    menu_string += "| x. Exit                       |\n"
    menu_string += "=================================\n"
    print(menu_string)

def make_server_request(request_dictionary):
    serialized_dictionary = json.dumps(request_dictionary)

    try:
        c = Client('localhost',8081)
        c.connect()
        c.send(serialized_dictionary)
        print(c.recv())
    except:
        print("Server is not running. Please start the server and try again.")

def main():
    while True:
        print_menu()
        choice = input("Choice: ")

        if choice == "1" or choice == "Register Customer":
            request_dictionary = {
                "request_type" : "Register Customer",
                "fname" : input("[REQUIRED] Enter first name: "),
                "sname" : input("[REQUIRED] Enter surname: "),
                "address" : input("[REQUIRED] Enter address: "),
                "phone" : input("[REQUIRED] Enter phone number: ")
            }
            make_server_request(request_dictionary)

        elif choice == "2" or choice == "Register Item":
            request_dictionary = {
                "request_type" : "Register Item",
                "iname" : input("[REQUIRED] Enter item name: "),
                "descrip" : input("[REQUIRED] Enter description: "),
                "price" : input("[REQUIRED] Enter price: "),
                "count" : input("[REQUIRED] Enter amount of items: ")
            }
            make_server_request(request_dictionary)

        elif choice == "3" or choice == "Buy Items":
            request_dictionary = {
                "request_type": "Buy Items",
                "fname": input("[REQUIRED] Who's buying? (firstname): "),
                "sname": input("[REQUIRED] Who's buying? (surname): "),
            }

            item_array = []
            still_inputting = True
            while still_inputting:
                print("\nPlease answer at least one of the following two questions (name and/or description)")
                item_info = {
                    "request_type" : "List Items",
                    "iname" : input("What item are you buying? (name): "),
                    "descrip" : input("What item are you buying? (description): "),
                    "count" : input("How many are you buying?: (default = 1): ")
                }
                
                if item_info["count"] == "":
                    item_info["count"] = "1"

                make_server_request(item_info)
                
                item_id = input("Enter appropriate item ID: ")
                if item_id != "":
                    item_array.append([item_id, item_info["count"]])

                print("{} items currently in cart".format(len(item_array)))
                still_inputting = False if input("End input? (end = xxx): ") == "xxx" else True
                
            request_dictionary["items"] = item_array
            make_server_request(request_dictionary)

        elif choice == "4" or choice == "Request Invoice":
            request_dictionary = {
                "request_type": "Request Invoice",
                "invoice_number": input("[REQUIRED] Enter invoice number: ")
            }
            make_server_request(request_dictionary)

        elif choice == "x":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
