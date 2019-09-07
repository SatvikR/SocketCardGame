# Python program to implement server side of chat room. 
import socket 
import select 
import sys
import pickle
ver = sys.version_info[0]
import _thread as thr
from DeckOfCards import *
import json
ver = sys.version_info[0]
CardList = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
   
# checks whether sufficient arguments have been provided 
if len(sys.argv) != 3: 
    print("correct usage: script, IP address, port number")
    exit() 
  
# takes the first argument from command prompt as IP address 
IP_address = str(sys.argv[1]) 
  
# takes second argument from command prompt as port number 
Port = int(sys.argv[2]) 


server.bind((IP_address, Port)) 
#doihavefriends = "NO"
print("How many players would you like in the game?")
maxplayersforgame = input()
list_of_names = []
server.listen(int(maxplayersforgame)) 
list_of_clients = [] 
TheDeckOfDecks = Deck()
dict_of_clients = {}
turn = None
TheTurnNumber = 0
waiting = True
def clientthread(conn, addr): 
    global waiting
    global list_of_names
    while True: 
            try: 
                message = conn.recv(2048) 
                if message: 
                    contents = pickle.loads(message)
                    if contents[0] == "name":
                        name = contents[1]
                        dict_of_clients[conn] = name
                        print("name::", dict_of_clients[conn])
                        list_of_names = list(dict_of_clients.values())
                    elif contents[0] == "notice":
                        broadcast(["notice", contents[1]], conn)
                        if len(list_of_names) == int(maxplayersforgame):
                            broadcast(["theotherplayers", list_of_names], None)
                            print("nammeeeese",list_of_names)
                         
                    elif contents[0] == "playcard":
                        print(dict_of_clients[conn] + " played an " + str(contents[1]))
                        broadcast(["notice", dict_of_clients[conn] + " played a(n) " + str(contents[1])], conn)
                    elif contents[0] == "Grab":
                        value = contents[1]
                        playerclientwantstostealfrom = contents[2]
                        qwerty = conn_from_name(playerclientwantstostealfrom)
                        print(qwerty)   
                        qwerty.send(pickle.dumps(["fished", name + "would like a " + value, value]))
                        waiting = False
                        print(waiting)
                    elif contents[0] == "matches":
                        player_index = list_of_clients.index(conn)
                        for f in range(len(matches)):
                            CardList[player_index].append(matches[f])
                        conn.send(pickle.dumps(["yourhand", CardList[player_index]]))
                                       
                              
                else:
                    remove(conn) 
  
            except Exception as e:
                print(e)
                continue
  
"""Using the below function, we broadcast the message to all
clients who's object is not the same as the one sending 
the message """

def broadcast(message, connection): 
    for client in list_of_clients: 
        if client!=connection: 
            try: 
                pickled_msg = pickle.dumps(message)
                print(pickled_msg)
                client.send(pickled_msg)
            except: 
                client.close() 
  
                # if the link is broken, we remove the client 
                remove(client) 
  
"""The following function simply removes the object 
from the list that was created at the beginning of  
the program"""
def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection) 

def distribute_cards():
    global CardList
    shuffle(TheDeckOfDecks.deck)    
    CardList = TheDeckOfDecks.DealHand(len(list_of_clients), 7)
    print(CardList)
    for i in CardList:
        EreaseTheWholeThing(i)
    print("THE REST OF THE DECK:\n" + str(TheDeckOfDecks))
def conn_from_name(player_name):
    connections = [x for x in dict_of_clients.keys() if dict_of_clients[x] == player_name]
    print("!!!!!", player_name, dict_of_clients[connections[0]])
    return connections[0]
#setup loop
for i in range(int(maxplayersforgame)): 
    conn, addr = server.accept()
    list_of_clients.append(conn)
    # prints the address of the user that just connected 
    print(addr[0] + " connected")
    thr.start_new_thread(clientthread,(conn,addr))
    while(len(list_of_clients) == int(maxplayersforgame)):
        if len(dict_of_clients) == int(maxplayersforgame):
            distribute_cards()
            clientnum = 0
            
            for client in list_of_clients:
                client.send(pickle.dumps(["yourhand", CardList[clientnum], list_of_names]))
                clientnum += 1
            turn = list_of_names[TheTurnNumber]
            break
#game
while True:
    current_client = conn_from_name(turn)
    current_client.send(pickle.dumps(["notice", "It is now YOUR turn, insert insult here"]))
    while waiting:
        pass
    waiting = True
    TheTurnNumber += 1
    if TheTurnNumber >= int(maxplayersforgame):
        TheTurnNumber -= int(maxplayersforgame)
    turn = list_of_names[TheTurnNumber]     
        
    
conn.close() 
server.close()