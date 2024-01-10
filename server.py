# Filename: server.py
# Description: Accepts requests from client, performs database operations and returns results to client

import json
import socket
from datetime import date

import mysql.connector

class Server:
    def __init__(self, port, listen = 5, timeout = 10, buf = 4096, queueSize = 10):
        self.port = port
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen = listen
        self.timeout = timeout
        self.bufsize = buf
        self.db_username = 'username'   # Change these to match valid
        self.db_password = 'password'   # MySQL credentials on your system
        self.db_host = 'localhost'
        self.db_name = 'network_store'

    def send(self, conn, string):
        conn.send(bytes(string,encoding="ascii"))

    def recv(self, conn):
        return str(conn.recv(self.bufsize),encoding="ascii")
    
    def connect_to_db(self):
        try:
            db_conn = mysql.connector.connect(user=self.db_username,
                                password=self.db_password,
                                host=self.db_host,
                                database=self.db_name,
                                autocommit=True,
                                buffered=True)
            return db_conn
        except:
            print("ERROR: Unable to connect to database")
            return None

    def run(self):
        print("Server started...\nPort:",self.port,"\nListen number:",self.listen)
        self.soc.bind(('', self.port))
        self.soc.listen(self.listen)
        client_back = ""

        while True:
            client_conn, client_address = self.soc.accept()
            serialized_request = self.recv(client_conn)
            deserialized_request = json.loads(serialized_request)

            request_type = deserialized_request["request_type"]
            print('Request type received from client (@ '+str(client_address[0]) + '):',request_type)

            if request_type == "Register Customer":
                try:
                    db_conn = self.connect_to_db()
                    cur = db_conn.cursor()
                except:
                    pass

                query = "INSERT INTO customers (fname, sname, address, phone) VALUES ({}, {}, {}, {})".format(deserialized_request["fname"], deserialized_request["sname"], deserialized_request["address"], deserialized_request["phone"])

                try:
                    cur.execute(query)
                    client_back = "Customer registered successfully"
                    print ("Customer registered successfully using query: {}".format(query))
                except Exception as error:
                    client_back = "ERROR: Unable to register customer"
                    print ("{}: Unable to register customer using query: {}".format(type(error).__name__, query))

                try:
                    cur.close()
                    db_conn.close()
                except:
                    pass

            elif request_type == "Register Item":
                try:
                    db_conn = self.connect_to_db()
                    cur = db_conn.cursor()
                except:
                    pass

                query = "INSERT INTO items (iname, descrip, price, count) VALUES ({}, {}, {}, {})".format(deserialized_request["iname"], deserialized_request["descrip"], deserialized_request["price"], deserialized_request["count"])

                try:
                    cur.execute(query)
                    client_back = "Item registered successfully"
                    print ("Item registered successfully using query: {}".format(query))
                except Exception as error:
                    client_back = "ERROR: Unable to register item"
                    print ("{}: Unable to register item using query: {}".format(type(error).__name__, query))

                try:
                    cur.close()
                    db_conn.close()
                except:
                    pass

            elif request_type == "List Items":
                try:
                    db_conn = self.connect_to_db()
                    cur = db_conn.cursor()
                except:
                    pass

                where_clause = ""

                if deserialized_request["iname"] != "" and deserialized_request["descrip"] != "":
                    where_clause = "WHERE (iname LIKE '%{}%' OR descrip LIKE '%{}%')".format(deserialized_request["iname"], deserialized_request["descrip"])
                elif deserialized_request["iname"] != "":
                    where_clause = "WHERE iname LIKE '%{}%'".format(deserialized_request["iname"])
                elif deserialized_request["descrip"] != "":
                    where_clause = "WHERE descrip LIKE '%{}%'".format(deserialized_request["descrip"])

                if where_clause != "":
                    where_clause += " AND count >= {}".format(deserialized_request["count"])
                else:
                    where_clause = "WHERE count >= {}".format(deserialized_request["count"])

                query = "SELECT * FROM items " + where_clause

                try:
                    cur.execute(query)

                    result_set = cur.fetchall()

                    result_count = 0
                    for row in result_set:
                        result_count += 1
                        id = row [0]
                        name = row[1]
                        descrip = row[2]
                        price = row[3]
                        count = row[4]

                        if result_count == 1:
                            client_back = "\nFound items:\n"

                        client_back += "=============\n ID: {}\n Name: {}\n Description: {}\n Price: R{}\n Amount in stock: {}\n".format(id, name, descrip, price, count)

                    print("Returned {} items using query: {}".format(result_count, query))
                except Exception as error:
                    client_back = "ERROR: No items found that match provided criteria"
                    print("{}: No items found for query: {}".format(type(error).__name__, query))
                
                try:
                    cur.close()
                    db_conn.close()
                except:
                    pass
        
            elif request_type == "Buy Items":
                try:
                    db_conn = self.connect_to_db()
                except:
                    pass
                
                error_occured = False
                
                # Get customer ID
                query = "SELECT custId FROM customers WHERE fname = '{}' AND sname = '{}'".format(deserialized_request["fname"], deserialized_request["sname"])
                try:
                    cur = db_conn.cursor()
                    cur.execute(query)
                    result_set = cur.fetchone()
                    custId = result_set[0]
                    cur.close()
                except Exception as error:
                    print("{}: No customers found for query: {}".format(type(error).__name__, query))
                    error_occured = True

                # Get item information
                if not error_occured:
                    total_price = 0
                    items = []
                    for item in deserialized_request["items"]:
                        query = "SELECT * FROM items WHERE itemId = {}".format(item[0])
                        try:
                            cur = db_conn.cursor()
                            cur.execute(query)
                            result_set = cur.fetchall()
                            cur.close()
                            for row in result_set:
                                if int(item[1]) > int(row[4]):
                                    client_back = "ERROR: Not enough items in stock"
                                    print("Not enough items in stock for query: '{}', skipping item...".format(query))
                                    continue
                                items.append([row[1], row[2], row[3], item[1], row[0]])
                                total_price += float(row[3]) * int(item[1])
                        except Exception as error:
                            print("{}: No items found for query: {}".format(type(error).__name__, query))
                            error_occured = True
                
                # Insert invoice to database
                if not error_occured:
                    query = "INSERT INTO invoices (custId, dateBought, totalPrice) VALUES ({}, '{}', {})".format(custId, date.today(), total_price)
                    try:
                        cur = db_conn.cursor()
                        cur.execute(query)
                        cur.close()
                    except Exception as error:
                        print ("{}: Unable to register invoice using query: {}".format(type(error).__name__, query))
                        error_occured = True

                # Get invoice ID
                if not error_occured:          
                    query = "SELECT invoiceId FROM invoices WHERE custId = {} AND dateBought = '{}' AND totalPrice = {}".format(custId, date.today(), total_price)
                    try:
                        cur = db_conn.cursor()
                        cur.execute(query)
                        result_set = cur.fetchone()
                        invoiceId = result_set[0]
                        cur.close()
                    except Exception as error:
                        print ("{}: No invoices found for query: {}".format(type(error).__name__, query))
                        error_occured = True
                
                # Output invoice to textfile and update item count
                if not error_occured:
                    invoice = "=================INVOICE=================="
                    invoice += "\nCustomer Name: {}\nCustomer Surname: {}\nInvoice number: {}"
                    invoice += "\n=========================================="
                    invoice += "\nITEMS"
                    invoice += "\n=========================================="
                    invoice = invoice.format(deserialized_request["fname"], deserialized_request["sname"], invoiceId)
                    
                    for item in items:
                        invoice += "\n{}\n{}\n++++++++++++++++++++++++++++++++++++++++++\nR{} X {}".format(item[0], item[1], item[2], item[3])
                        invoice += "\n------------------------------------------\nR{}".format(float(item[2]) * float(item[3]))
                        invoice += "\n=========================================="

                        # Update item count in database
                        query = "UPDATE items SET count = count - {} WHERE itemId = {}".format(item[3], item[4])
                        try:
                            cur = db_conn.cursor()
                            cur.execute(query)
                            cur.close()
                        except Exception as error:
                            print ("{}: Unable to update item count using query: {}".format(type(error).__name__, query))
                            error_occured = True

                    invoice += "\nTotal: R{}".format(total_price)
                    invoice += "\n=========================================="

                    # Write invoice to text file (writes to %UserProfile%)
                    try:
                        text_file = open("%s.txt" % invoiceId, "w")
                        text_file.write(invoice)
                        text_file.close()
                        print("Invoice (ID: {}) written to text file".format(invoiceId))
                    except Exception as error:
                        print ("{}: Unable to write invoice to text file".format(type(error).__name__))
                        error_occured = True
                    
                    # print(invoice)
                
                if error_occured:
                    client_back = "ERROR: Unable to complete transaction"
                else: 
                    client_back = "\n" + invoice + "\n"

                try:
                    db_conn.close()
                except:
                    pass

            elif request_type == "Request Invoice":
                filename = deserialized_request["invoice_number"] + ".txt"
                try:
                    file = open(filename, 'r')
                    client_back = file.read()
                except:
                    client_back = 'Couldn\'t find file for invoice number: {}.'.format(deserialized_request["invoice_number"])

            else:
                client_back = "ERROR: Unknown request type"

            self.send(client_conn, "\n" + client_back + "\n")
            client_conn.close()

if __name__ == "__main__":
    s = Server(8081, listen = 1000)
    s.run()