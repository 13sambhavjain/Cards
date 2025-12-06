from games.poker import *
def test_rank_hands():
        t = Table([
                Player("A", Chips(1000)),
                Player("B", Chips(1000)),
                Player("C", Chips(1000)),
                Player("D", Chips(1000)),
                Player("E", Chips(1000)),
                Player("F", Chips(1000))],
                blind_amount=Chips(10), low_chips_amount=Chips(0))
        r = Round(t)
        r.open_flop()
        r.open_turn()
        r.open_river()
        return r.rank_hands()

