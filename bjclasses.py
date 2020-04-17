import random

card_value_list = ('A',2,3,4,5,6,7,8,9,10,'J','Q','K')
suit_list = ('Clubs','Diamonds','Hearts','Spades')
card_value_dict = {'A':11, 'J':10, 'Q':10, 'K':10}

class deck():
    # creates a new full deck, shuffled by default
    def __init__(self, shuffle=True):
        self.cards = []
        for suit in suit_list:
            for value in card_value_list:
                self.cards.append(card(value, suit))
        if shuffle == True:
            random.shuffle(self.cards)

    def __str__(self):
        return 'Deck with {} cards'.format(len(self.cards))

    def draw_card(self):
        # remove last card in deck
        return self.cards.pop()

    def shuffle(self):
        # shuffle deck with cards still on it
        random.shuffle(self.cards)
        print('Deck shuffled')

class card():
    def __init__(self, value,suit):
        # creates a card with a value and suit
        if value not in card_value_list:
            raise ValueError('Valor não identificado ({}), deve ser um dos seguintes: {}'.format(
                value, card_value_list))
        if suit not in suit_list:
            raise ValueError('Naipe não identificado ({}), deve ser um dos seguintes: {}'.format(
                suit, suit_list))
        self.value = value
        self.suit = suit

    def __str__(self):
        return '{} of {}'.format(self.value,self.suit)

    def __repr__(self):
        return '{} of {}'.format(self.value, self.suit)

class hand():
    # Hand object. Contains player cards
    def __init__(self):
        self.cards = []

    def add_card(self, deck, draws = 1):
        # Draws a card from target deck
        for draw in range(draws):
            self.cards.append(deck.draw_card())

    def sum_values(self):
        # calculates the value of the player hand for blackjack
        hand_value = 0
        for card in self.cards:
            if isinstance(card.value, int):
                hand_value += card.value
            else:
                hand_value += card_value_dict[card.value]
        for card in self.cards:
            if card.value == 'A' and hand_value > 21:
                hand_value -= 10
        return hand_value

    def __str__(self):
        return 'Hand with {} cards'.format(len(self.cards))

    def __repr__(self):
        return 'Hand with {} cards'.format(len(self.cards))

class player():
    # Creates a named player with an empty hand  object.
    # 'playing' is used for the game logic
    def __init__(self, name = 'Player', playing=True):
        self.hand = hand()
        self.name = name
        self.playing = playing

    def __repr__(self):
        return 'Player named {}, {};'.format(self.name,self.hand)

    def return_cards(self, target_deck):
        # returns all cards in player hand to target deck
        n_cards = len(self.hand.cards)
        while len(self.hand.cards) > 0:
            target_deck.cards.append(self.hand.cards.pop())
        print('Returned {} cards from player {} to deck {}'.format(n_cards,self.name, target_deck))

    def show_hand(self):
        # prints a list with all cards in player hand.
        print(self.hand.cards)

class game_table():
    # creates a new table with a full shuffled deck and a Dealer player object
    def __init__(self):
        self.deck_in_play = deck()
        self.dealer = player('Dealer')
        self.players = []

    def add_player(self):
        new_player_name = input('Who is playing? (insert player name)\n')
        self.players.append(player(name=new_player_name))
        print('Added player {}'.format(new_player_name))

    def start_blackjack(self, restart = False):
        if not restart:
            more_players = True
            while more_players:
                self.add_player()
                more_players_switch = input('Is anyone else playing? (y/n)')
                if more_players_switch == 'n':
                    more_players = False
            print('Game Starting!')
        print(self)
        self.dealer.hand.add_card(self.deck_in_play, draws=2)
        print('Dealt 2 cards to {}'.format(self.dealer.name))
        for player in self.players:
            player.hand.add_card(self.deck_in_play, draws=2)
            print('Dealt 2 cards to {}'.format(player.name))
        print('{} has:'.format(self.dealer.name))
        self.dealer.show_hand()
        print('Total = {}'.format(self.dealer.hand.sum_values()))
        for player in self.players:
            print('{} has:'.format(player.name))
            player.show_hand()
            print('Total = {}'.format(player.hand.sum_values()))
        while any(player.playing==True for player in self.players):
            for player in self.players:
                if player.playing:
                    action = input('Player {} choose hit or stand\n'.format(player.name))
                    if action == 'hit':
                        player.hand.add_card(deck=self.deck_in_play)
                        print('{} has:'.format(player.name))
                        player.show_hand()
                        print('Total = {}'.format(player.hand.sum_values()))
                        if player.hand.sum_values() > 21:
                            player.playing = False
                            print('Busted!')
                    elif action == 'stand':
                        player.playing=False
                        print('Player {} stopped at {}'.format(player.name, player.hand.sum_values()))
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
        restart = input('Play again? (y/n)')
        if restart == 'y':
            self.dealer.return_cards(self.deck_in_play)
            for player in self.players:
                player.return_cards(self.deck_in_play)
                player.playing=True
            self.deck_in_play.shuffle()
            print('Game Restarting!')
            self.start_blackjack(restart = True)
        else:
            print('Game ending')

    def __str__(self):
        return_str = 'Table with player(s):\n'
        for player in self.players:
            return_str += player.name + '\n'
        return return_str

table1 = game_table()
table1.start_blackjack()