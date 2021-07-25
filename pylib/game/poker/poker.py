
import random


class Card:
    # 黑桃:S-Spade 橄榄叶(象形),代表和平.
    # 红桃:H-Heart 桃心(象形bai),代表爱情.
    # 方块:D-Diamond 钻石(形同意合),代表财富.
    # 梅花:C-Club 三叶草dao(象形),代表幸运.
    # '♠', '♡', '♢', '♣'
    SUITS = ['S', 'H', 'D', 'C']

    RANKS = ['2', '3', '4', '5', '6', '7', '8',
                '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        pass

    def eq(self, card):
        return self.suit == card.suit and self.rank == card.rank

    def __str__(self):
        return  '%s-%s' % (self.SUITS[self.suit],  self.RANKS[self.rank])

class Poker:
    def __init__(self, number):
        self.number = number
        self.cards = []

        for v in range(52 * number):
            # pack = v // 52
            v = v % 52

            suit = v // 13
            rank = v % 13
            card = Card(suit, rank)
            self.cards.append(card)

    def shuffle(self):
        for index in range(52):
            rnd = random.randint(0, 51)
            self.cards[index], self.cards[rnd] = self.cards[rnd], self.cards[index]

    def pop(self):
        card = self.cards.pop()
        return card


class CardGroup:
    def __init__(self):
        self.cards = []

    def append(self, card):
        self.cards.append(card)

    def extend(self, cardgroup):
        self.cards.extend(cardgroup.get())

    def len(self):
        return len(self.cards)

    def is_req(self, cardgroup):
        for card in self.cards:
            for card2 in cardgroup.get():
                if card.eq(card2):
                    return True
        return False

    @staticmethod
    def _card_key(e):
        return e.rank * 10 + 10 - e.suit

    def sort(self):
        self.cards.sort(key=self._card_key, reverse=True)

    def get(self, index= None):
        if index is None:
            return self.cards

        return self.cards[index]

    def show(self, msg=None):
        self.sort()

        if msg:
            print(msg, end=': ')

        for card in self.cards:
            print(card, end=', ')
        print()



class Player:
    def __init__(self, _id, score=0):
        self._id = _id
        self.score = score
        self.clear()

    def clear(self):
        self.cardgroup = CardGroup()

    def append(self, card):
        self.cardgroup.append(card)

    def get_cardgroup(self):
        self.cardgroup.sort()
        return self.cardgroup

    def show(self):
        print('Player', self._id, end=': ')
        self.cardgroup.show()

    def step(self):
        pass

    def show_status(self):
        print('Player', self._id, end=': \n')
        print('\tScore:', self.score)


if __name__ == '__main__':
    # import sys, io
    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') 
    poker = Poker(1)
    poker.shuffle()

    player = Player(1)
    player2 = Player(2)

    for _ in range(5):
        player.append(poker.pop())

    player.show()

