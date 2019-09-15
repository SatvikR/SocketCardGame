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
print("How many players would you like in the game?")
maxplayersforgame = input()
list_of_names = []
server.listen(int(maxplayersforgame))
list_of_clients = []
TheDeckOfDecks = Deck()
dict_of_clients = {}
turn = None
cycle = 1
TheTurnNumber = 0
waiting = True
fishing_success = False

def clientthread(conn, addr):
    global waiting
    global list_of_names
    global fishing_success
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
                        print("nammeeeese", list_of_names)
                elif contents[0] == "playcard":
                    print(dict_of_clients[conn] + " played an " + str(contents[1]))
                    broadcast(["notice", dict_of_clients[conn] + " played a(n) " + str(contents[1])], conn)
                elif contents[0] == "Grab":
                    value = contents[1]
                    playerclientwantstostealfrom = contents[2]
                    qwerty = conn_from_name(playerclientwantstostealfrom)
                    print(qwerty)
                    qwerty.send(pickle.dumps(["fished", name + " would like a " + value, value, name]))
                    print(waiting)
                elif contents[0] == "sync":
                    player_index = list_of_clients.index(conn)
                    CardList[player_index] = contents[1]
                elif contents[0] == "matches":
                    fishing_holder = False
                    matches = contents[1]
                    conn_of_fisher = conn_from_name(contents[2])
                    fisher_index = list_of_clients.index(conn_of_fisher)
                    for f in range(len(matches)):
                        CardList[fisher_index].append(matches[f])
                    conn_of_fisher.send(pickle.dumps(["newhand", CardList[fisher_index]]))
                    if len(matches) == 0:
                        print("here 1")
                        conn_of_fisher.send(pickle.dumps(["notice", "Go Fish!"]))
                        fishing_success = False
                    else:
                        print("here 2")
                        fishing_success = True
                    print(fishing_success, " *before")
                    waiting = False

            else:
                remove(conn)

        except Exception as e:
            print(e)
            continue

def broadcast(message, connection):
    for client in list_of_clients:
        if client != connection:
            try:
                pickled_msg = pickle.dumps(message)
                print(pickled_msg)
                client.send(pickled_msg)
            except:
                client.close()

                # if the link is broken, we remove the client 
                remove(client)

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


# setup loop
for i in range(int(maxplayersforgame)):
    conn, addr = server.accept()
    list_of_clients.append(conn)
    # prints the address of the user that just connected 
    print(addr[0] + " connected")
    thr.start_new_thread(clientthread, (conn, addr))
    while (len(list_of_clients) == int(maxplayersforgame)):
        if len(dict_of_clients) == int(maxplayersforgame):
            distribute_cards()
            clientnum = 0
            for client in list_of_clients:
                client.send(pickle.dumps(["yourhand", CardList[clientnum], list_of_names]))
                clientnum += 1
            turn = list_of_names[TheTurnNumber]
            break
# game
while True:
    current_client = conn_from_name(turn)
    current_client.send(pickle.dumps(["notice", "It is now YOUR turn"]))
    if cycle == 1:
        current_client.send(pickle.dumps(["notice", "It is now YOUR turn"]))
        cycle = 21838
    while waiting:
        pass
    waiting = True
    print(fishing_success)
    if fishing_success == False:
        TheTurnNumber += 1
    if TheTurnNumber >= int(maxplayersforgame):
        TheTurnNumber -= int(maxplayersforgame)
    turn = list_of_names[TheTurnNumber]

conn.close()
server.close()
