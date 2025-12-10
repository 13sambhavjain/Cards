from enum import IntEnum
from . import Card, CardPile, Rank, Suit, Round
from typing import Optional

class HandRank(IntEnum):
    ROYAL_FLUSH = 1
    STRAIGHT_FLUSH = 2
    FOUR_OF_A_KIND = 3
    FULL_HOUSE = 4
    FLUSH = 5
    STRAIGHT = 6
    THREE_OF_A_KIND = 7
    TWO_PAIR = 8
    ONE_PAIR = 9
    HIGH_CARD = 10

class HandRankfunc():
    @classmethod
    def rank_of_hand(cls, net: CardPile) -> tuple[HandRank, list[Card]]:
        # net :CardPile = self.community_cards + player.hand
        suit_counts = net.suit_counts()
        
        if (f_suit:=cls.flush(suit_counts)):
            f_suit_cards: list[Card] = []
            for card in net:
                if card.suit == f_suit:
                    f_suit_cards.append(card)
            f_suit_cards.sort(reverse=True, key=lambda card: card.rank)
            s_flush = cls.straight_flush(f_suit_cards)
            if s_flush:
                if s_flush[0].rank == Rank.Ace:
                    return HandRank.ROYAL_FLUSH, s_flush # Royal Flush
                else:
                    return HandRank.STRAIGHT_FLUSH, s_flush # Straight Flush
            
        rank_counts = sorted(net.rank_counts().items() ,key=lambda x: (x[1], x[0]), reverse=True)
        net.sort(key=lambda card: card.rank, reverse=True)
        if rank_counts[0][1] == 4:
            return HandRank.FOUR_OF_A_KIND, net.seperate_cards_by_rank(rank_counts[0][0]) + net[0:1]
        elif rank_counts[0][1] == 3 and rank_counts[1][1] >= 2:
            return HandRank.FULL_HOUSE, net.seperate_cards_by_rank(rank_counts[0][0]) + net.seperate_cards_by_rank(rank_counts[1][0])[0:2]
        elif f_suit:
            return HandRank.FLUSH, f_suit_cards[:6]
        elif (st := cls.straight(net, rank_counts)):
            return HandRank.STRAIGHT, st
        elif rank_counts[0][1] == 3:
            return HandRank.THREE_OF_A_KIND, net.seperate_cards_by_rank(rank_counts[0][0]) + net[0:2]
        elif rank_counts[0][1] == 2:
            if rank_counts[1][1] == 2:
                return HandRank.TWO_PAIR, net.seperate_cards_by_rank(rank_counts[0][0]) + net.seperate_cards_by_rank(rank_counts[1][0]) + net[0:1]
            else:
                return HandRank.ONE_PAIR, net.seperate_cards_by_rank(rank_counts[0][0]) + net[0:3]
        else:
            return HandRank.HIGH_CARD, net[0:5]   

    @staticmethod            
    def rank_hands(round: Round):
        ans = []
        for player in round.players:
            if player.active and not player.folded:
                ans.append((player.id, HandRankfunc.rank_of_hand(round.community_cards + player.hand)))
        ans.sort(key= lambda x: (-x[1][0], x[1][1][0].rank, x[1][1][1].rank, x[1][1][2].rank, x[1][1][3].rank, x[1][1][4].rank), reverse=True)
        ans = dict(ans)
        return ans
        
        # not straight flush
        # check four of a kind, three    
    def round_end(self):
        
        pass

    @staticmethod
    def straight_flush(f_suit_cards: list[Card]) -> list[Card]:
        count = 0
        for i in range(1, len(f_suit_cards)):
            if f_suit_cards[i-1].rank - f_suit_cards[i].rank == 1:
                count += 1
                if count == 5: #straight flush is there
                    return f_suit_cards[i-4: i+1]
            else:
                count = 0
                if i > 2:
                    return []
        return []
    
    @staticmethod
    def straight(cards: CardPile, rank_count: list[tuple[Rank, int]]) -> list[Card]:
        count = 0
        ranks = list(x[0] for x in rank_count)
        ranks.sort(reverse=True)
        for i in range(1, len(ranks)):
            if ranks[i-1] - ranks[i] == 1:
                count += 1
                if count == 5: #straight is there
                    ans = []
                    for j in range(ranks[i]+4, ranks[i]-1, -1):
                        for card in cards:
                            if card.rank == Rank(j):
                                ans.append(card)
                                break
                        else:
                            raise Exception(f"Coundn't find {Rank(j)} in {cards}")
                    return ans
            elif ranks[i-1] - ranks[i] == 0:
                continue
            else:
                count = 0
                if i > 2:
                    return [] #False
        return [] #False
    
    @staticmethod
    def flush(suit_counts: dict[Suit, int]) -> Optional[Suit]:
        for suit, count in suit_counts.items():
            if count >= 5:
                # check staright flush to flush
                # check straight fluch here
                return suit
        return None
 