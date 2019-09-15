# Python program to implement client side of chat room. 
import socket
import select  # Python program to implement client side of chat room.
import sys
import pickle

ver = sys.version_info[0]
theotherplayers = []
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address, Port))
mycards = []
print("What is your name?")
name = input()
server.send(pickle.dumps(["name", name]))
yes_know_maybe = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen",
                  "King"]
gofish = False

while True:
    # maintains a list of possible input streams 
    sockets_list = [sys.stdin, server]
    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
    for socks in read_sockets:
        if socks == server:  # Things that server wants to tell us
            message = socks.recv(2048)
            pickleofdamessage = pickle.loads(message)
            print(pickleofdamessage)
            if pickleofdamessage[0] == "yourhand":
                mycards_objects = pickleofdamessage[1]
                for c in pickleofdamessage[1]:
                    print(str(c))
                    mycards.append(str(c))
                theotherplayers = pickleofdamessage[2]
                print(theotherplayers)
            elif pickleofdamessage[0] == "newhand":
                mycards_objects = pickleofdamessage[1]
                for c in pickleofdamessage[1]:
                    print(str(c))
                    mycards.append(str(c))
            elif pickleofdamessage[0] == "notice":
                print(pickleofdamessage[1])
            elif pickleofdamessage[0] == "fished":
                print(pickleofdamessage[1])
                matches = [x for x in mycards_objects if x.value == pickleofdamessage[2]]
                if len(matches) == 0:
                    gofish == True
                else:
                    gofish == False
                mycards.clear()
                for i in range(len(matches)):
                    mycards_objects.remove(matches[i])
                for c in mycards_objects:
                    print(str(c))
                    mycards.append(str(c))
                server.send(pickle.dumps(["matches", matches, pickleofdamessage[3], gofish]))
                server.send(pickle.dumps(["sync", mycards_objects]))


        else:  # Stuff that we want to tell the server
            mycards.count
            message = sys.stdin.readline()
            message = str(message)
            if message == "msg\n":  # messages all other players
                print("What would you like to send")
                messagez = input()
                server.send(pickle.dumps(["notice", "<" + name + "> " + messagez]))
                sys.stdout.write("<You>" + messagez + "\n")
                sys.stdout.flush()
            elif message == "view\n":  # lets you view cards
                print(mycards)
            elif message == "grab\n":  # lets you fish from other players
                print(theotherplayers)
                print("Which value would you like to request?")
                IWANTIT = input()
                if IWANTIT not in yes_know_maybe:
                    print(
                        "You have entered an invalid card value. Here are some examples: Jack, Queen, King, Ace, Ten, Three.")
                else:
                    print("Who would you like to request this value from?")
                    LEMMEGRABIT = input()
                    print(LEMMEGRABIT, name)
                    if (LEMMEGRABIT not in theotherplayers or LEMMEGRABIT == name):
                        print(
                            "There are no players with this name. Here are the names of the other players playing with you:")
                        for f in range(len(theotherplayers)):
                            print(theotherplayers[f])
                        print("\n")
                    else:
                        server.send(pickle.dumps(["Grab", IWANTIT, LEMMEGRABIT]))
                        sys.stdout.write("<You> Requested value " + IWANTIT + " from " + LEMMEGRABIT + "." + "\n")
                        sys.stdout.flush()
server.close()

# Even though we are sending a message indicated by 'msg' we still end up sending the msg as a notice
