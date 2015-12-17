# MancalaGame
Agent that plays the mancala game-implements greedy, minimax and alpha beta pruning algorithms in Python

Input should be in the following format:
<Task#> Greedy=1, MiniMax=2, Alpha-Beta=3, Competition=4
<Your player: 1 or 2>
<Cutting off depth>
<Board state for player-2>
<Board state for player-1>
<#stones in player-2’s mancala>
<#stones in player-1’s mancala>

eg:
2
2
2
8 8 8
8 8 10
0
0


Output will be 2 text files:
“next_state.txt” showing the next state of the board after the greedy move and
“traverse_log.txt” showing the traverse log of your program in the following format:
Node,Depth,Value
root,0,-Infinity
B2,1,Infinity
B3,1,Infinity
A2,2,1
B3,1,1
A3,2,1
B3,1,1
A4,2,1
B3,1,1
B2,1,1
...
