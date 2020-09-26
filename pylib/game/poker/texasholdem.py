

# Texas Holdem
from poker import Poker
from poker import CardGroup
from poker import Player


class TexasHoldem:
    def __init__(self, players):
        self.players = players

    Royal_flush = 9 * 10000
    Straight_flush = 9 * 10000
    Four_of_a_kind = 8 * 10000 # 四条
    Full_house = 7 * 10000 # 满堂红/葫芦
    Flush = 6 * 10000 # 同花
    Straight = 5 * 10000 # 顺子
    Three_of_a_kind = 4 * 10000
    Two_pairs = 3 * 10000
    One_pair = 2 * 10000
    High_car = 1 * 10000


    @staticmethod
    def to1(n):
        for i in range(n):
            li = [False] * n
            li[i] = True
            yield li
        return


    @staticmethod
    def to2(n):
        for i in range(n):
            for j in range(n):
                if i != j:
                    li = [False] * n
                    li[i] = True
                    li[j] = True
                    yield li
        return

    @staticmethod
    def to3(n):
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if i != j and j != k and k != i:
                        li = [False] * n
                        li[i] = True
                        li[j] = True
                        li[k] = True
                        yield li
        return


    @staticmethod
    def value(cardgroup):
        cardgroup.sort()
        c = cardgroup.get()
        numbers = {}

        for cc in c:
            if cc.rank in numbers:
                numbers[cc.rank] += 1
            else:
                numbers[cc.rank] = 1

        items = numbers.items()
        numbers = [[v[1],v[0]] for v in items] 
        numbers.sort(reverse=True)

        is_flush = c[0].suit == c[1].suit and c[1].suit == c[2].suit and c[2].suit == c[3].suit and c[3].suit == c[4].suit
        is_straight = c[0].rank-1 == c[1].rank and c[1].rank-1 == c[2].rank and c[2].rank-1 == c[3].rank and c[3].rank-1 == c[4].rank 

        value = TexasHoldem.High_car
        if is_flush and is_straight:
            value = TexasHoldem.Straight_flush
        elif numbers[0][0] == 4:
            value = TexasHoldem.Four_of_a_kind + numbers[0][1] * 100
        elif numbers[0][0] == 3 and numbers[1][0] == 2:
            value = TexasHoldem.Full_house + numbers[0][1] * 100 + numbers[1][1]
        elif is_flush:
            value = TexasHoldem.Flush
        elif is_straight:
            value = TexasHoldem.Straight
        elif numbers[0][0] == 3:
            value = TexasHoldem.Three_of_a_kind + numbers[0][1] * 100
        elif numbers[0][0] == 2 and numbers[1][0] == 2:
            value = TexasHoldem.Two_pairs + numbers[0][1] * 100 +  + numbers[1][1]
        elif numbers[0][0] == 2:
            value = TexasHoldem.One_pair + numbers[0][1] * 100 +  + numbers[1][1]

        lvalue = 0
        for cc in c:
            lvalue = lvalue * 100 + cc.rank

        for cc in c:
            lvalue = lvalue * 10 + cc.suit

        return value * 1000000000000000 + lvalue

    @staticmethod
    def max_value(player_cardgroup_2, pool):
        pool.sort()
        max_value = 0
        max_cardgroup = None
        for li in TexasHoldem.to3(pool.len()):
            p_card_group = CardGroup()
            p_card_group.extend(player_cardgroup_2)

            for i, v in enumerate(li):
                if v:
                    p_card_group.append(pool.get(i))
            value = TexasHoldem.value(p_card_group)
            if max_value < value:
                max_value = value
                max_cardgroup = p_card_group
        return max_value, max_cardgroup


    # 计算当前牌力在整个场面的排名
    @staticmethod
    def rate(player_cardgroup_2, pool):
        poker = Poker(1)

        player_value, _ = TexasHoldem.max_value(player_cardgroup_2, pool)

        win_times = 0
        times = 0
        for li in TexasHoldem.to2(52):
            cardgroup = CardGroup()
            for i, v in enumerate(li):
                if v:
                    cardgroup.append(poker.cards[i])
            if not cardgroup.is_req(pool):
                value, _ = TexasHoldem.max_value(cardgroup, pool)
                if value < player_value:
                    win_times += 1
                times += 1
            #print(win_times, times)
        return win_times, times


    # @staticmethod
    # def rates(player_cardgroup_2, pool):
    #     poker = Poker(1)
    #     l = 5 - pool.len()
    #     if l == 0:
    #         return TexasHoldem.rate(player_cardgroup_2, pool)
    #     elif l == 2:
    #         for li in TexasHoldem.to2(52):
    #             cardgroup = CardGroup()
    #             for i, v in enumerate(li):
    #                 if v:
    #                     cardgroup.append(poker.cards[i])
    #             if not cardgroup.is_req(pool) and cardgroup.is_req(player_cardgroup_2):
    #                 cardgroup.extend(pool)
    #                 w, a = TexasHoldem.rate(player_cardgroup_2, cardgroup)
    #                 print(w, a, w/a)
    #         return 1,1


    def game(self, debug=False):
        # print('Game #############')
        poker = Poker(1)
        poker.shuffle()

        pool = CardGroup()
        for player in self.players:
            player.clear()

        for _ in range(2):
            for player in self.players:
                player.append(poker.pop())

        for _ in range(2):
            pool.append(poker.pop())

        scores = {}
        for player in self.players:
            scores[player] = 0

        for _ in range(3):
            pool.append(poker.pop())
            values = {}
            values['min_score'] = 0
            for player in self.players:
                score = player.step(values)

                if score > values['min_score']:
                    scores[player] += score
                    values['min_score'] = score
                elif score == values['min_score']:
                    scores[player] += score

        win_player = None
        win_value = 0
        for player in self.players:
            max_value, _ = self.max_value(player.get_cardgroup(), pool)
            if win_value < max_value:
                win_player = player
                win_value = max_value

        win_player.win(sum(scores.values()))

        # print('Winner:')
        # win_player.show()
        # pool.show('Pool')
        # win_cardgroup.show('Max')
        # print('Win:', sum(scores.values()))

    def show_status(self):
        print('Status:')
        for player in self.players:
            player.show_status()
            pass


class PlayerAI(Player):
    def __init__(self, _id):
        super().__init__(_id, 1000)
 
    def step(self, values):
        value = 10
        if self.score < value:
            value = self.score
        self.score -= value
        return value

    def win(self, score):
        self.score += score


class PlayerAI2(Player):
    def __init__(self, _id):
        super().__init__(_id, 1000)
 
    def step(self, values):
        value = 10
        if self.score < value:
            value = self.score
        self.score -= value
        return value

    def win(self, score):
        self.score += score

if __name__ == '__main__':

    players = []
    players.append(PlayerAI(1))
    players.append(PlayerAI(2))

    texas = TexasHoldem(players)
    for _ in range(1000):
        texas.game()


    texas.show_status()

