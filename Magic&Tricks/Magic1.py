from core import CardPile, Card, Rank
def magic1():
    deck = CardPile(numberOfCards=12)
    cards2insert = [Card(s, SRank.Joker, face_up=True) for s in Suit]
    for card in cards2insert:
        deck.insertCard(card)
    deck.shuffle()
    flip = False
    deck.reverse()
    for card in deck:
        if flip:
            card.flip()
        flip = not flip
    grid = [[CardPile() for _ in range(4)] for __ in range(4)]
    # print(deck)
    # print(grid)
    for row in grid:
        for d in row:
            deck.dealCard(d)
    grid[1].reverse()
    grid[3].reverse()
    def foldarow(grid: list[list[CardPile]], r=None, c=None):
        if r != None:
            if r == 0:
                r1 = 1
            elif r == -1:
                r1 = -2
            else:
                raise ValueError('r can be either 0 or -1.')
            for i in range(len(grid[r])):
                grid[r1][i] += grid[r][i].flip()
            del grid[r]
        elif c != None:
            if c == 0:
                c1 = 1
            elif c == -1:
                c1 = -2
            else:
                raise ValueError('c can be either 0 or -1.')
            for i in range(len(grid)):
                grid[i][c1] += grid[i][c].flip()
                del grid[i][c]
        else:
            raise ValueError('need to give either r or c as 0 or -1.')
    folds = list()
    args = [0, -1]
    for _ in range(3):
        folds.append((None, random.choice(args)))
        folds.append((random.choice(args), None))
    random.shuffle(folds)
    for fold in folds:
        foldarow(grid, *fold)
    print(grid)