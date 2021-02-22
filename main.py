from random import randint

class Card:
    def __init__(self, value: int, color: int):
        """
        Class used to represent any single card of a basic 52 cards game.

        :value: A number between 1 and 13, the value of the card.
        :color: The color of the card, also a number - between 1 and 4.
        """

        if value == 1:
            self.value = 'Ace'
        elif 2 <= value <= 10:
            self.value = value
        elif 11 <= value <= 13:
            self.value = ['Jack', 'Queen', 'King'][value - 11]
        else:
            raise ValueError('This card does not exist, please choose one with a value between 1 and 13.')

        self.color = ['Heart', 'Club', 'Spade', 'Diamond'][(color % 4) - 1]
        self.score = value if value < 10 else 10

    def __str__(self) -> str:
        """
        :return: A string representing the cards informations.
        """
        return str(f'{self.value} of {self.color}')


class Deck:
    def __init__(self, *cards: Card):
        """
        Class used to store cards.

        :cards: A card or a list of cards to put in the deck.
        """
        self.content = [card for card in cards]

    def __len__(self) -> int:
        """
        :return: The length of the deck.
        """
        return len(self.content)

    def __str__(self) -> str:
        """
        :return: A list-looking string of all the cards in the deck.
        """
        r = '['
        for i in range(len(self)):
            r += str(self.content[i]) if i + 1 == len(self) else str(self.content[i]) + ', '
        return r + ']'
    
    def add_card(self, card: (Card, list)) -> None:
        """
        :card: A card or a list of strings to add to the deck.
        """
        if isinstance(card, Card):
            self.content.append(card)
        else:
            for e in card:
                self.content.append(e)

    def remove_card(self, index_of_card: int) -> Card:
        return self.content.pop(index_of_card)
        
class Player:
    def __init__(self, role: (int, str)):
        """
        Class representing one of the two players in a game; the player or the dealer.

        :role: A value (between 1 and 2) or a string leading to the creation of the player or the dealer.
        """
        self.role = ['Player', 'Dealer'][role % 2 - 1] if isinstance(role, int) else role
        self.hand = Deck()

    def __str__(self) -> str:
        return f'{self.role} : {str(self.hand)} - {self.score()} points.'

    def add_card(self, card: Card) -> None:
        self.hand.add_card(card)

    def give_card(self, index_of_card: int) -> Card:
        return self.hand.remove_card(index_of_card)

    def score(self) -> int:
        score = 0
        stamp = []
        while len(self.hand) > 0:
            stamp.append(self.hand.remove_card(0))
            if stamp[-1].score == 1:
                if self.role == 'Player':
                    ace_value = int(input('Is your Ace worth 1 point or 11 points? '))
                    while ace_value not in [1, 11]:
                        ace_value = int(input('Invalid value, please enter a value between 1 point and 11 points: '))
                else:
                    if self.score() + 11 > 21:
                        ace_value = 1
                    else:
                        ace_value = 11

                score += ace_value
            else:
                score += stamp[-1].score
        for card in stamp:
            self.hand.add_card(card)
        return score


assert str(Card(1, 1)) == 'Ace of Heart'
assert len(Deck()) == 0
assert str(Player(11)) == str(Player('Player'))
assert str(Player(4)) == str(Player('Dealer'))

def game(credit=100):
    ############################################
    # CREATION OF THE CARDS IN A DECK
    ############################################
    deck = Deck()
    for i in range(52):
        deck.add_card(Card(i % 13 + 1, i // 13 + 1))

    ############################################
    # CREATION OF THE PLAYERS
    ############################################
    player = Player(1)
    dealer = Player(2)

    ############################################
    # BET
    ############################################
    bet = int(input('How much do you bet this game? '))
    while 0 > bet > credit:
        bet = int(input('You can not bet that amount, how much do you bet? '))

    ############################################
    # SIMULATION OF CARDS DEAL
    # This part is useless and can be modified.
    ############################################
    # Removing 2 cards from the deck and giving them to the dealer
    dealer.add_card(deck.remove_card(randint(0, len(deck) - 1)))
    dealer.add_card(deck.remove_card(randint(0, len(deck) - 1)))


    # Giving the 2 cards to the player
    player.add_card([dealer.give_card(0), dealer.give_card(0)])
    print(player)

    ############################################
    # GAME: PICKING CARDS
    ############################################
    # Giving the player an other card if they wants to
    if input('Would you like to pick another card? [yes/no]: ')[0].lower() == 'y':
        player.add_card(deck.remove_card(randint(0, len(deck) - 1)))
        print(player)

    player_score = player.score()
    if player_score <= 21:
        while dealer.score() <= 15:
            dealer.add_card(deck.remove_card(randint(0, len(deck) - 1)))
            print(dealer)
        
        if dealer.score() >= player_score and dealer.score() <= 21:
            print(f'You lost {bet} credit, {player.role}: {player_score} - {dealer.role}: {dealer.score()}.')
            return -bet
        else:
            print(f'You won {bet} credit, {player.role}: {player_score} - {dealer.role}: {dealer.score()}.')
            return bet
    else:
        print(f'You lost {bet} credit with a score of {player_score}.')
        return -bet


credit = 100 + game()
while input(f'Would you like to play again ({credit} credits)? [yes/no]: ')[0].lower() == 'y' and credit > 0:
    credit += game(credit)
