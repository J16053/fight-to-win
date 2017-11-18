import os
import timeit

start = timeit.default_timer()

x = 1000
for i in range(x):
  	os.system('python BattleshipBot.py')
# file = open('score.txt','r')
# content = file.read()
# numWins = content.count('1')
# numGames = len(content)
# print('Win rate = ' + str(numWins/numGames))

file = open('moves.txt','r')
total = 0
numGames = 0
for s in file:
	total += int(s)
	numGames += 1
print('numGames = ' + str(numGames))
print('avg moves = ' + str(total/numGames))

stop = timeit.default_timer()
tt = str(stop-start)

print('time = ' + tt)

