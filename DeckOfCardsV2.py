from random import shuffle

class Card(object):
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    def __str__(self):
        return self.value +" of "+ self.suit+ "."

class Deck(object):
    def __init__(self):
        self.deck = []
        self.values = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
        self.suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
        for suit in self.suits:
            for value in self.values:
                self.deck.append(Card(value, suit))
    def __str__(self):
        return "\n".join([str(str(x)) for x in self.deck])

    def DealHand(self, NoPlayers, NoCards):
        CountCards = 0
        CountPlayers = 0
        CardList = []
        for i in range(NoPlayers):
            CardList.append([])
        for i in range(NoPlayers):
            for y in range(NoCards):
                CardList[i].append(self.deck.pop(0))
        return CardList

class Player(object):
    def __init__(self):
        self.hand = []
    def LookingAtYourHand(self):
        for i, j in enumerate(self.hand):
            print(i, "for the card", j)
            pass

class Host(object):
    def __init__(self):
        self.SomeDeck = Deck()
        shuffle(self.SomeDeck.deck)
    pass

def printDeck(deck):
    print('\n'.join([str(x) for x in deck]))
    print('\nNext Player\n')

if __name__ == "__main__":
    print('How many players will be playing this game?')
    NumPlayers = input()
    print('How many cards do you want to give each player?')
    NumCards = input()
    IntPlayers = int(NumPlayers)
    IntCards = int(NumCards)
    ToBeDistributed = IntPlayers * IntCards
    CardsThatPlayerWantsToBeDistributed = ToBeDistributed
    if CardsThatPlayerWantsToBeDistributed > 52:
        print("Really? Just why? Aren't you smart enough to know that there are 52 cards in a deck. Please kick out some of you're players or make everyone get less cards. :'~(")
        exit()
    gameDeck = Deck()
    shuffle(gameDeck.deck)
    HAND = gameDeck.DealHand(IntPlayers, IntCards)
    for i in HAND:
        printDeck(i)
    print(str(gameDeck))
    print("\n\n Is this game a random card game? (y/n)")
    randomCardGame = input()
    APlayer = Player()
    APlayer.hand = HAND.pop(0)
    APlayer.LookingAtYourHand()
