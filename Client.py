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
all_values = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
gofish = False
mybooks = 0
my_turn = False

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
                theotherplayers.remove(name)
                for x in range(len(theotherplayers)): 
                    print(theotherplayers[x]), 
            elif pickleofdamessage[0] == "go_fish":
                print(pickleofdamessage[1])
                server.send(pickle.dumps(["out_of_cards", "Player", name, "needs a new card."]))
            elif pickleofdamessage[0] == "newhand":
                mycards_objects = pickleofdamessage[1]
                for c in pickleofdamessage[1]:
                    print(str(c))
                    mycards.append(str(c))
            elif pickleofdamessage[0] == "notice":
                print(pickleofdamessage[1])
            elif pickleofdamessage[0] == "yourturn":
                my_turn = True
                print(pickleofdamessage[1])
                for v in range(len(all_values)):
                    book_size = [l for l in mycards_objects if l.value == all_values[v]]
                    if len(book_size) == 4:
                        print("You have all four", all_values[v] + "s!")
                        for u in book_size:
                            mycards_objects.remove(u)
                        mycards.clear()
                        for c in mycards_objects:
                            print(str(c))
                            mycards.append(str(c))
                        mybooks += 1
                server.send(pickle.dumps(["sync", mycards_objects]))
                server.send(pickle.dumps(["sync_score", mybooks]))
                if len(mycards) == 0:
                    server.send(pickle.dumps(["out_of_cards", "Player", name, "is out of cards."]))
            elif pickleofdamessage[0] == "fished":
                print(pickleofdamessage[1])
                matches = [x for x in mycards_objects if x.value == pickleofdamessage[2]]
                if len(matches) == 0:
                    gofish = True
                else:
                    gofish = False
                mycards.clear()
                for i in range(len(matches)):
                    mycards_objects.remove(matches[i])
                for c in mycards_objects:
                    print(str(c))
                    mycards.append(str(c))
                if len(mycards) == 0:
                    server.send(pickle.dumps(["out_of_cards", "Player", name, "is out of cards."]))
                server.send(pickle.dumps(["matches", matches, pickleofdamessage[3], gofish]))
                server.send(pickle.dumps(["sync", mycards_objects]))
            elif pickleofdamessage[0] == "extracard":
                mycards_objects.append(pickleofdamessage[1])
                for e in mycards_objects:
                    print(str(e))
                    mycards.append(str(e))
                server.send(pickle.dumps(["sync", mycards_objects]))
            elif pickleofdamessage[0] == "winner":
                print(pickleofdamessage[1])
                break
            elif pickleofdamessage[0] == "loser":
                print(pickleofdamessage[1])
                break
            elif pickleofdamessage[0] == "turn_over":
                my_turn = False
                print()

        else:  # Stuff that we want to tell the server
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
            elif message == "help\n":
                print("Hello,", name)
                print("I am here to help you play \"Go Fish (Python Edition)\" by Alexandre and Satvik")
                print("Let's get started with the basics!")
                print("You can type \"help\" to bring back this menu!")
                print("You can type \"message\", hit enter, and then type your message to talk with ALL the other "
                      "players.")
                print("You can type \"view\" to see your cards")
                print("You can type \"grab\", enter the value of the card you would like to request, hit enter again, "
                      "type in the name of the player you would like to attempt and grab the card from, hit enter for "
                      "the last time, and all the that the player has of the value you selected will be given to you.")
                print("If you would like more information on how to play Go Fish, and not run this program, visit: \n "
                      "https://bicyclecards.com/how-to-play/go-fish/")
            elif message == "players\n":
                for x in range(len(theotherplayers)): 
                    print(theotherplayers[x]), 
            elif message == "grab\n":  # lets you fish from other players
                if my_turn:
                    print("Which value would you like to request?")
                    IWANTIT = input()
                    if IWANTIT not in all_values:
                        print(
                            "You have entered an invalid card value. Here are some examples: Jack, Queen, King, Ace, "
                            "Ten, Three.")
                    else:
                        print("Who would you like to request this value from?")
                        for x in range(len(theotherplayers)):
                            print(theotherplayers[x]),
                        LEMMEGRABIT = input()
                        print(LEMMEGRABIT, name)
                        if LEMMEGRABIT not in theotherplayers or LEMMEGRABIT == name:
                            print(
                                "There are no players with this name. Here are the names of the other players playing "
                                "with you:")
                            for x in range(len(theotherplayers)):
                                print(theotherplayers[x]),
                        else:
                            server.send(pickle.dumps(["Grab", IWANTIT, LEMMEGRABIT]))
                            sys.stdout.write("<You> Requested value " + IWANTIT + " from " + LEMMEGRABIT + "." + "\n")
                            sys.stdout.flush()
server.close()

# Even though we are sending a message indicated by 'msg' we still end up sending the msg as a notice
