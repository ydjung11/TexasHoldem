import random

card_suit_name = [ 'c', 'd', 'h', 's', ]
card_rank_name = [ '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', ]
hand_rank_name = [ '-', 'One pair', 'Two pair', 'Three of a kind', 'Straight', 'Flush', 'Full house', 'Four of a kind', 'Straight of Flush', ]

rank_card_ace  = 12

rank_hand_no_pair = 0
rank_hand_one_pair = 1
rank_hand_two_pair = 2
rank_hand_three_of_a_kind = 3
rank_hand_straight = 4
rank_hand_flush = 5
rank_hand_full_house = 6
rank_hand_four_of_a_kind = 7
rank_hand_straight_flush = 8

def get_suit(card):
    return card%4

def get_rank(card):
    return card//4

def get_card(suit, rank):
    return suit+rank*4

def shuffle(cards, sindex=0, eindex=51, count=52):

    for i in range(1, count):
        #t1 = random.randint(sindex, eindex)
        #t2 = random.randint(sindex, eindex)
        t1 = random.getrandbits(16)%(eindex-sindex+1) + sindex
        t2 = random.getrandbits(16)%(eindex-sindex+1) + sindex

        cards[t1], cards[t2] = cards[t2], cards[t1]

    return cards

# cards must be sorted list by rank
def is_flush(cards):

    suit = get_suit(cards[0])

    for card in cards[1:5]:
        if (suit != get_suit(card)):
            return False

    return True

# cards must be sorted list by rank
def is_straight(cards):

    ranks = list(map(get_rank, cards))

    if (ranks[0]+1 == ranks[1] and ranks[1]+1 == ranks[2] and ranks[2]+1 == ranks[3] and ranks[3]+1 == ranks[4]):
        return True

    if (ranks[0] == 0 and ranks[1] == 1 and ranks[2] == 2 and ranks[3] == 3 and ranks[4] == rank_card_ace):
        return True

    return False

# cards must be sorted list by rank
def get_pair_rank(cards):

    ranks = list(map(get_rank, cards))

    if (ranks[0] == ranks[1] and ranks[1] == ranks[2] and ranks[2] == ranks[3]):
        return (rank_hand_four_of_a_kind, [cards[3], cards[2], cards[1], cards[0], cards[4]])

    if (ranks[4] == ranks[1] and ranks[1] == ranks[2] and ranks[2] == ranks[3]):
        return (rank_hand_four_of_a_kind, [cards[4], cards[3], cards[2], cards[1], cards[0]])

    if (ranks[0] == ranks[1] and ranks[1] == ranks[2] and ranks[3] == ranks[4]):
        return (rank_hand_full_house, [cards[2], cards[1], cards[0], cards[4], cards[3]])

    if (ranks[0] == ranks[1] and ranks[2] == ranks[3] and ranks[3] == ranks[4]):
        return (rank_hand_full_house, [cards[4], cards[3], cards[2], cards[1], cards[0]])

    if (ranks[0] == ranks[1] and ranks[1] == ranks[2]):
        return (rank_hand_three_of_a_kind, [cards[2], cards[1], cards[0], cards[4], cards[3]])

    if (ranks[1] == ranks[2] and ranks[2] == ranks[3]):
        return (rank_hand_three_of_a_kind, [cards[3], cards[2], cards[1], cards[4], cards[0]])

    if (ranks[2] == ranks[3] and ranks[3] == ranks[4]):
        return (rank_hand_three_of_a_kind, [cards[4], cards[3], cards[2], cards[1], cards[0]])

    if (ranks[0] == ranks[1] and ranks[2] == ranks[3]):
        return (rank_hand_two_pair, [cards[3], cards[2], cards[1], cards[0], cards[4]])

    if (ranks[0] == ranks[1] and ranks[3] == ranks[4]):
        return (rank_hand_two_pair, [cards[4], cards[3], cards[1], cards[0], cards[2]])

    if (ranks[1] == ranks[2] and ranks[3] == ranks[4]):
        return (rank_hand_two_pair, [cards[4], cards[3], cards[2], cards[1], cards[0]])

    if (ranks[0] == ranks[1]):
        return (rank_hand_one_pair, [cards[1], cards[0], cards[4], cards[3], cards[2]])

    if (ranks[1] == ranks[2]):
        return (rank_hand_one_pair, [cards[2], cards[1], cards[4], cards[3], cards[0]])

    if (ranks[2] == ranks[3]):
        return (rank_hand_one_pair, [cards[3], cards[2], cards[4], cards[1], cards[0]])

    if (ranks[3] == ranks[4]):
        return (rank_hand_one_pair, [cards[4], cards[3], cards[2], cards[1], cards[0]])

    return (rank_hand_no_pair, [cards[4], cards[3], cards[2], cards[1], cards[0]])

def get_5hand_rank(cards):

    tmp = sorted(cards)

    flush = is_flush(tmp)
    straight = is_straight(tmp)

    if (flush and straight):
        return (rank_hand_straight_flush, [tmp[3], tmp[2], tmp[1], tmp[0], tmp[4]])

    if (flush):
        return (rank_hand_flush, [tmp[4], tmp[3], tmp[2], tmp[1], tmp[0]])

    if (straight):
        return (rank_hand_straight, [tmp[3], tmp[2], tmp[1], tmp[0], tmp[4]])

    return get_pair_rank(tmp)


def pick_5_cards(rank1, rank2, cards):
    return 0 

def get_7hand_rank(cards):

    tmp = list(sorted(cards))
    ranks = list(map(get_rank, tmp))

    suit_hist = [[0,i] for i in range(0,4)]
    rank_hist = [[0,i] for i in range(0,13)]
    
    for card in tmp:
        rank = get_rank(card)
        suit = get_suit(card)
        rank_hist[rank][0] = rank_hist[rank][0]+1
        suit_hist[suit][0] = suit_hist[suit][0]+1

    suit_hist = list(sorted(suit_hist, reverse=True))        
    rank_hist = list(sorted(rank_hist, reverse=True))        

    # check flush
    for i in range(0,4):
        if (suit_hist[i][0]>=5):
            return (rank_hand_flush, [tmp[4], tmp[3], tmp[2], tmp[1], tmp[0]])

    sr = set(ranks)

    # check straight
    for i in range(rank_card_ace,2,-1):
        st_hand = set()
        for j in range(0,5):
            if (i-j>=0):
                st_hand.add(i-j)
            else:
                st_hand.add(rank_card_ace)

        if (st_hand.issubset(sr)):
            return (rank_hand_straight, [tmp[4], tmp[3], tmp[2], tmp[1], tmp[0]])

    # check four of a kind
    if(rank_hist[0][0]==4):
        return(rank_hand_four_of_a_kind, [tmp[4], tmp[3], tmp[2], tmp[1], tmp[0]])             

    # check full house
    if(rank_hist[0][0]==3 and rank_hist[1][0]>=2):
        return(rank_hand_full_house, [tmp[4], tmp[3], tmp[2], tmp[1], tmp[0]])                   

    # check three of a kind
    if(rank_hist[0][0]==3):
        return(rank_hand_three_of_a_kind, [tmp[4], tmp[3], tmp[2], tmp[1], tmp[0]])                   

    # check two pair
    if(rank_hist[0][0]==2 and rank_hist[1][0]==2):
        return(rank_hand_two_pair, [tmp[4], tmp[3], tmp[2], tmp[1], tmp[0]])                   

    # check one pair
    if(rank_hist[0][0]==2):
        return(rank_hand_one_pair, [tmp[4], tmp[3], tmp[2], tmp[1], tmp[0]])                   

    return (rank_hand_no_pair, [tmp[6], tmp[5], tmp[4], tmp[3], tmp[2]])

def winner(mine, yours):

    rank_mine = get_5hand_rank(mine)
    rank_yours = get_5hand_rank(yours)

    if (rank_mine>rank_yours):
        return 2

    if (rank_mine<rank_yours):
        return 0

    return 1


def print_card(card):
    suit = get_suit(card)
    rank = get_rank(card)
    print ("%s%s" %(card_rank_name[rank], card_suit_name[suit])),

deck = list(range(0,52))

hist5 = [0]*9
hist7 = [0]*9
winh5 = [0]*3

for i in range(0, 1000):
    deck = shuffle(deck)

    #deck = [ 0, 5, 8, 13, 17, 20, 24, 28, 32, 36, 40 ]

    w = winner(deck[0:5], deck[5:10])
    
    my_rank5 = get_5hand_rank(deck[0:5])    
    my_rank7 = get_7hand_rank(deck[0:7])
    #your_rank = get_5hand_rank(deck[5:10]) 
    
    hist5[my_rank5[0]] = hist5[my_rank5[0]]+1
    hist7[my_rank7[0]] = hist7[my_rank7[0]]+1
    #hist[your_rank[0]] = hist[your_rank[0]]+1
    winh5[w] = winh5[w]+1
    
    #map(print_card, deck[0:7])
    #print(" - %20s, %-20s %u  " %(hand_rank_name[my_rank5[0]], hand_rank_name[my_rank7[0]], w)),
    #print(my_rank5)


print(hist5)
print(hist7)
print(winh5)


