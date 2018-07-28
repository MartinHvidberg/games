if len(strategy) < 99:
    for option in lst_myhouses:
ika = Kalaha()
lst_myhouses = ika.get_my_houses(player)
if board:
    ika.b = board
if ika.b[option] > 0:
    mv = ika.move(option, player)
if mv:
    strategy.append(option)
    ##print("okay: (score {}) way {}".format(ika.score(), strategy))
    play(copy.deepcopy(ika.b), player, strategy)
else:
    print("Dead: (score {}) way {} + {}".format(ika.score(), strategy, option))
    return
else:
print("strategy is longer than allowed: {}".format(strategy))