import random

# Constants for possible cards and values

card_value_list = ('A',2,3,4,5,6,7,8,9,10,'J','Q','K')
suit_list = ('Clubs','Diamonds','Hearts','Spades')
#Mapping for value of non-int cards
card_value_dict = {'A':11, 'J':10, 'Q':10, 'K':10}

class card():
    # creates a card with a value and suit
    def __init__(self, value,suit):
        # Checks to see if the card value and suit are valid
        if value not in card_value_list:
            raise ValueError('Unidentified value ({}), must be one of the following: {}'.format(
                value, card_value_list))
        if suit not in suit_list:
            raise ValueError('Unidentified suit ({}), must be one of the following: {}'.format(
                suit, suit_list))
        self.value = value
        self.suit = suit

    def __str__(self):
        return '{} of {}'.format(self.value,self.suit)

    def __repr__(self):
        return '{} of {}'.format(self.value, self.suit)

class deck():
    # creates a new deck with all possible values and suits, shuffled by default
    def __init__(self, shuffle=True):
        self.cards = []
        for suit in suit_list:
            for value in card_value_list:
                self.cards.append(card(value, suit))
        if shuffle == True:
            random.shuffle(self.cards)

    def __str__(self):
        # printing the object returns the amount of cards still in it
        return 'Deck with {} cards'.format(len(self.cards))

    def draw_card(self):
        # Removes one card from deck and returns the card object
        return self.cards.pop()

    def shuffle(self):
        # shuffle deck with cards still on it
        random.shuffle(self.cards)
        print('Deck shuffled')

class hand():
    # Hand object for holding player cards, initiated empty.
    def __init__(self):
        self.cards = []

    # Adds a card to hand, drawing from target deck object. Default is one card draw.
    def add_card(self, deck, draws = 1):
        for draw in range(draws):
            self.cards.append(deck.draw_card())
    
    # returns the value of the player hand for blackjack
    def sum_values(self):
        hand_value = 0
        for card in self.cards:
            #checks if card value is already int or not (ex: 2,3,4 or J,Q,K) to add value itself or mapped value.
            if isinstance(card.value, int):
                hand_value += card.value
            else:
                hand_value += card_value_dict[card.value]
        # Specifically for blackjack, if hand exceeds 21 and contains an Ace, count it as 1 instead of 11
		# by reducing 10 from total hand value
        for card in self.cards:
            if card.value == 'A' and hand_value > 21:
                hand_value -= 10
        return hand_value
	
	# prints returns the number of cards in hand
    def __str__(self):
        return 'Hand with {} cards'.format(len(self.cards))

    def __repr__(self):
        return 'Hand with {} cards'.format(len(self.cards))

class player():
    # Creates a named player with an empty hand object. Default name is "Player".
    # 'playing' state is used for the game flow. Starts as True for default.
    def __init__(self, name = 'Player', playing=True):
        self.hand = hand()
        self.name = name
        self.playing = playing
	
	# evaluating the player object returns the player name and amount of cards in hand
    def __repr__(self):
        return 'Player named {}, {};'.format(self.name,self.hand)

	# returns all cards in player hand to target deck
    def return_cards(self, target_deck):
        n_cards = len(self.hand.cards)
        while len(self.hand.cards) > 0:
            target_deck.cards.append(self.hand.cards.pop())
        print('Returned {} cards from player {} to deck {}'.format(n_cards,self.name, target_deck))
	
	# prints a list with all cards in player hand.
    def show_hand(self):
        print(self.hand.cards)

class game_table():
    # creates a new game table with a full shuffled deck, a player object named Dealer and an empty player list
    def __init__(self):
        self.deck_in_play = deck()
        self.dealer = player('Dealer')
        self.players = []
	
	# adds a player object to the table players list and asks the user for the player's name
    def add_player(self):
        new_player_name = input('Who is playing? (insert player name)\n')
        self.players.append(player(name=new_player_name))
        print('Added player {}'.format(new_player_name))
	
	# printing object returns all players on table
	def __str__(self):
        return_str = 'Table with player(s):\n'
        for player in self.players:
            return_str += player.name + '\n'
        return return_str
	
	# starts the main blackjack gameplay flow. Restart is used for new rounds, default is False for when starting the game.
    def start_blackjack(self, restart = False):
        if not restart:
			# more_players is used to ask the user for more players for the table. Always asks for at least one.
            more_players = True
			# starts loop for adding more players until player chooses 'n' on input.
            while more_players:
                self.add_player()
				# asks the player if more players are to be added. Anything other than 'n' (case-sensitive) restarts the loop.
                more_players_switch = input('Is anyone else playing? (y/n)')
                # ends the add_player loop and starts game
				if more_players_switch == 'n':
                    more_players = False
            print('Game Starting!')
        print(self)
		# dealer draws 2 cards
        self.dealer.hand.add_card(self.deck_in_play, draws=2)
        print('Dealt 2 cards to {}'.format(self.dealer.name))
        # each player draws 2 cards
		for player in self.players:
            player.hand.add_card(self.deck_in_play, draws=2)
            print('Dealt 2 cards to {}'.format(player.name))
        # TODO simplify card showing of dealer and players as loop or func
		# Shows the dealer cards and hand value
		print('{} has:'.format(self.dealer.name))
        self.dealer.show_hand()
        print('Total = {}'.format(self.dealer.hand.sum_values()))
		# Shows each player's cards and hand value
        for player in self.players:
            print('{} has:'.format(player.name))
            player.show_hand()
            print('Total = {}'.format(player.hand.sum_values()))
        # starts asking players for next move, while any player is still playing
		while any(player.playing==True for player in self.players):
            # loops over players
			for player in self.players:
                if player.playing:
					# asks the player if he wants to hit or stand
                    action = input('Player {} choose hit or stand\n'.format(player.name))
                    # if hit, add another card, sum hand_value again and check result
					if action == 'hit':
                        player.hand.add_card(deck=self.deck_in_play)
                        print('{} has:'.format(player.name))
                        player.show_hand()
                        print('Total = {}'.format(player.hand.sum_values()))
                        # checks if player busted 21 limit and sets playing to false if it did
						if player.hand.sum_values() > 21:
                            player.playing = False
                            print('Busted!')
                    # if stand, set playing state to false and print final hand value
					elif action == 'stand':
                        player.playing=False
                        print('Player {} stopped at {}'.format(player.name, player.hand.sum_values()))
        # routines for dealer "AI"
		while self.dealer.hand.sum_values() < 17 and any(
                player.hand.sum_values() < 21 for player in self.players) and any(
                player.hand.sum_values() > self.dealer.hand.sum_values() for player in
            self.players):
            print('Dealer drew another card')
            self.dealer.hand.add_card(deck=self.deck_in_play)
            print('{} has:'.format(self.dealer.name))
            self.dealer.show_hand()
            print('Total = {}'.format(self.dealer.hand.sum_values()))
        while self.dealer.hand.sum_values() <= 17 and any(
                player.hand.sum_values() < 21 for player in self.players) and any(
                player.hand.sum_values() > self.dealer.hand.sum_values() for player in
                self.players) and any(card.value == 'A' for card in self.dealer.hand.cards):
            print('Dealer drew another card')
            self.dealer.hand.add_card(deck=self.deck_in_play)
            print('{} has:'.format(self.dealer.name))
            self.dealer.show_hand()
            print('Total = {}'.format(self.dealer.hand.sum_values()))
        # routines for checking who won and lost
		for player in self.players:
            if player.hand.sum_values() > 21:
                print('Player {} lost'.format(player.name))
            elif player.hand.sum_values() < self.dealer.hand.sum_values() and self.dealer.hand.sum_values() <= 21:
                print('Player {} lost'.format(player.name))
            elif player.hand.sum_values() > self.dealer.hand.sum_values():
                print('Player {} won'.format(player.name))
            elif player.hand.sum_values() < self.dealer.hand.sum_values() and self.dealer.hand.sum_values() > 21:
                print('Player {} won'.format(player.name))
            elif player.hand.sum_values() == self.dealer.hand.sum_values():
                print('Player {} draw'.format(player.name))
        # ask the player if he wants to go another round
		restart = input('Play again? (y/n)')
        if restart == 'y':
			#returns dealer and player cards to deck and shuffle it
            self.dealer.return_cards(self.deck_in_play)
            for player in self.players:
                player.return_cards(self.deck_in_play)
                player.playing=True
            self.deck_in_play.shuffle()
            print('Game Restarting!')
			# starts the gameplay flow again with restart = True to skip asking for who is playing
            self.start_blackjack(restart = True)
        # ends the game
		else:
            print('Game ending')
    
# creates a game table and starts blackjack gameplay loop
table1 = game_table()
table1.start_blackjack()
