from games.poker import *
def test_rank_hands():
        t = Table([
                (p1 := Player("A", Chips(1000))),
                (p2 := Player("B", Chips(1000))),
                (p3 := Player("C", Chips(1000))),
                (p4 := Player("D", Chips(1000))),
                (p5 := Player("E", Chips(1000))),
                (p6 := Player("F", Chips(1000)))],
                blind_amount=Chips(10), low_chips_amount=Chips(0)
        )
        p_map = dict(A=p1, B=p2, C=p3, D=p4, E=p5, F=p6)
        r = Round(t)
        r.open_flop()
        r.open_turn()
        r.open_river()
        rhs = HandRankfunc.rank_hands(r)
        print(r.community_cards)
        for p, h in rhs.items():
                p_map[p].hand.flip_open()
                print(f"{p}: {h[0].name}, {p_map[p].hand} -> {" ".join(str(card) for card in h[1])}")

