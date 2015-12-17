import re
import sys
from collections import namedtuple
from copy import copy, deepcopy
bestChild=-50001
NEXT_MOVE=[]
GLOB_CAPEND=False
def Tostring(a):
    if a==-50001:
        return "-Infinity"
    elif a==+50001:
        return "Infinity"
    else:
        return str(a)
def alpha(p):
    if p==0:
        return "B"
    else:
        return "A"
def otherP(p):
    if p==MAX:
        return MIN
    else:
        return MAX
def checkTerminal(node,p,d): #reaches equiv end game state and returns true if endgame or depth=0
    p2=otherP(p)
    flag=0
    for e in node.state[p2][:NPITS]: #NPITS has number of pits minus mancala
        if e!=0:
            flag=1
            break
    if flag==0:
        for e in range(NPITS):
            node.state[p][NPITS]+=node.state[p][e]
            node.state[p][e]=0
    for e in node.state[p][:NPITS]:
        if e!=0:
            if d==0:
                return True
            return False
    for e in range(NPITS):
        node.state[p2][NPITS]+=node.state[p2][e]
        node.state[p2][e]=0
    return True
def makeMove(nodeS,e,ind,p): #return node result for a move and true only if move end in player's mancala and not end game
    global GLOB_CAPEND
    pos=ind
    p2=p
    nodeS[p][ind]=0
    while e!=0:
        if pos+1==NPITS+1:
            p2=otherP(p2)
            pos=0
        elif pos+1==NPITS:
            if p2==otherP(p):
                p2=otherP(p2)
                pos=0
            else:
                pos+=1
        else:
            pos+=1
        nodeS[p2][pos]+=1
        e-=1
    if p2==p and pos!=NPITS and nodeS[p][pos]==1:
        nodeS[p][NPITS]+=1
        nodeS[p][NPITS]+=nodeS[otherP(p)][NPITS-1-pos]
        nodeS[p][pos]=0
        nodeS[otherP(p)][NPITS-1-pos]=0
    flag=0
    for k in nodeS[p2][:NPITS]:
        if k!=0:
            flag=1
            break
    if p2==p and pos==NPITS and flag==0:
        GLOB_CAPEND=True
    if p2==p and pos==NPITS and flag==1:
        return (nodeS,True)
    else:
        return (nodeS,False)
def minimax(node,depth):
    global NEXT_MOVE
    global algoType
    bestV=-50001
    NEXT_MOVE=[]
    MAXVAL=max_val(node,depth,bestV,False)
    answer=""
    if not NEXT_MOVE==[]:
        nxt=NEXT_MOVE[1][:NPITS]
        nxt.reverse()
        for e in nxt:
            answer+=str(e)+" "
        writeOutput.write(answer)
        answer="\n"
        for e in NEXT_MOVE[0][:NPITS]:
            answer+=str(e)+" "
        writeOutput.write(answer)
        answer="\n"+str(NEXT_MOVE[1][NPITS])+"\n"+str(NEXT_MOVE[0][NPITS])
        writeOutput.write(answer)
        
def max_val(node,depth,parentVal,nodeCap):
    global NEXT_MOVE
    global bestChild
    global GLOB_CAPEND
    bestV=parentVal   
    if nodeCap:
        bestV=50001
    if depth!=0 or (depth==0 and nodeCap) or (depth==0 and GLOB_CAPEND):
        GLOB_CAPEND=False
        if algoType==2:
            traverse_log=node.name+","+str(cutOff-depth)+","+Tostring(bestV)+"\n"
            writeTrav.write(traverse_log)
    if not nodeCap and (checkTerminal(node,node.player,depth)):
        if algoType==2:
            value=str(node.state[MAX][NPITS]-node.state[MIN][NPITS])
            traverse_log=node.name+","+str(cutOff-depth)+","+value+"\n"
            writeTrav.write(traverse_log)
        return node.state[MAX][NPITS]-node.state[MIN][NPITS]
    for ind in range(NPITS):
        if node.player==1:
            ind=NPITS-ind-1
        if node.state[node.player][ind]!=0: 
            val=node.state[node.player][ind]
            childState=deepcopy(node.state)
            childState,capable=makeMove(childState,val,ind,node.player)
            if capable:
                CP=node.player
            else:
                CP=otherP(node.player)
            if node.player==1:
                move=NPITS-ind+1
            else:
                move=ind+2
            oldV=bestV
            if nodeCap:
                pl=alpha(node.player)
                name=pl+str(move)
                child=Node(name,childState,CP)
                bestV=min(bestV,max_val(child,depth,-50001,capable))
                if algoType==2:
                    traverse_log=node.name+","+str(cutOff-depth)+","+Tostring(bestV)+"\n"
                    writeTrav.write(traverse_log)
            else:
                pl=alpha(node.player)
                name=pl+str(move)
                child=Node(name,childState,CP)
                bestV=max(bestV,min_val(child,depth-1,50001,capable))
                if depth==cutOff and bestV!=oldV:
                    if bestV>bestChild:
                        bestChild=bestV
                        NEXT_MOVE=child.state[:]
                if algoType==2:
                    traverse_log=node.name+","+str(cutOff-depth)+","+Tostring(bestV)+"\n"
                    writeTrav.write(traverse_log)
    return bestV
def min_val(node,depth,parentVal,nodeCap):
    global NEXT_MOVE
    global bestChild
    global GLOB_CAPEND
    bestV=parentVal
    if nodeCap:
        bestV=-50001
    if depth!=0 or (depth==0 and nodeCap) or (depth==0 and GLOB_CAPEND):
        GLOB_CAPEND=False
        if algoType==2:
            traverse_log=node.name+","+str(cutOff-depth)+","+Tostring(bestV)+"\n"
            writeTrav.write(traverse_log)
    if not nodeCap and (checkTerminal(node,node.player,depth)):
        if algoType==2:
            value=str(node.state[MAX][NPITS]-node.state[MIN][NPITS])
            traverse_log=node.name+","+str(cutOff-depth)+","+value+"\n"
            writeTrav.write(traverse_log)
        return node.state[MAX][NPITS]-node.state[MIN][NPITS]
    for ind in range(NPITS):
        if node.player==1:
            ind=NPITS-ind-1
        if node.state[node.player][ind]!=0:
            val=node.state[node.player][ind]
            childState=deepcopy(node.state)
            childState,capable=makeMove(childState,val,ind,node.player)
            if capable:
                CP=node.player                
            else:
                CP=otherP(node.player)
            if node.player==1:
                move=NPITS-ind+1
            else:
                move=ind+2
            oldV=bestV
            if nodeCap:
                pl=alpha(node.player)
                name=pl+str(move)
                child=Node(name,childState,CP)
                bestV=max(bestV,min_val(child,depth,50001,capable))
                if depth==cutOff-1 and bestV!=oldV:
                    if bestV>bestChild:
                        bestChild=bestV
                        NEXT_MOVE=child.state[:]
                if algoType==2:
                    traverse_log=node.name+","+str(cutOff-depth)+","+Tostring(bestV)+"\n"
                    writeTrav.write(traverse_log)
            else:
                pl=alpha(node.player)
                name=pl+str(move)
                child=Node(name,childState,CP)
                bestV=min(bestV,max_val(child,depth-1,-50001,capable))
                if algoType==2:
                    traverse_log=node.name+","+str(cutOff-depth)+","+Tostring(bestV)+"\n"
                    writeTrav.write(traverse_log)
    return bestV
def alphabeta(node,depth):
    global NEXT_MOVE
    global algoType
    bestV=-50001
    NEXT_MOVE=[]
    MAXVAL=max_ab(node,depth,-50001,False,-50001,50001)
    answer=""
    if not NEXT_MOVE==[]:
        nxt=NEXT_MOVE[1][:NPITS]
        nxt.reverse()
        for e in nxt:
            answer+=str(e)+" "
        writeOutput.write(answer)
        answer="\n"
        for e in NEXT_MOVE[0][:NPITS]:
            answer+=str(e)+" "
        writeOutput.write(answer)
        answer="\n"+str(NEXT_MOVE[1][NPITS])+"\n"+str(NEXT_MOVE[0][NPITS])
        writeOutput.write(answer)
        
def max_ab(node,depth,parentVal,nodeCap,alph,beta):
    global NEXT_MOVE
    global bestChild
    global GLOB_CAPEND
    bestV=parentVal
    if nodeCap:
        bestV=50001
    if depth!=0 or (depth==0 and nodeCap) or (depth==0 and GLOB_CAPEND):
        GLOB_CAPEND=False
        traverse_log=node.name+","+str(cutOff-depth)+","+Tostring(bestV)+","+Tostring(alph)+","+Tostring(beta)+"\n"
        writeTrav.write(traverse_log)
    if not nodeCap and (checkTerminal(node,node.player,depth)):
        value=str(node.state[MAX][NPITS]-node.state[MIN][NPITS])
        traverse_log=node.name+","+str(cutOff-depth)+","+Tostring(value)+","+Tostring(alph)+","+Tostring(beta)+"\n"
        writeTrav.write(traverse_log)
        return node.state[MAX][NPITS]-node.state[MIN][NPITS]
    for ind in range(NPITS):
        if node.player==1:
            ind=NPITS-ind-1
        if node.state[node.player][ind]!=0:
            val=node.state[node.player][ind]
            childState=deepcopy(node.state)
            childState,capable=makeMove(childState,val,ind,node.player)
            if capable:
                CP=node.player
            else:
                CP=otherP(node.player)
            if node.player==1:
                move=NPITS-ind+1
            else:
                move=ind+2
            oldV=bestV
            if nodeCap:
                pl=alpha(node.player)
                name=pl+str(move)
                child=Node(name,childState,CP)
                bestV=min(bestV,max_ab(child,depth,-50001,capable,alph,beta))
                if bestV<=alph:
                    traverse_log=node.name+","+str(cutOff-depth)+","+Tostring(bestV)+","+Tostring(alph)+","+Tostring(beta)+"\n"
                    writeTrav.write(traverse_log)
                    return bestV
                beta=min(beta,bestV)
                traverse_log=node.name+","+str(cutOff-depth)+","+Tostring(bestV)+","+Tostring(alph)+","+Tostring(beta)+"\n"
                writeTrav.write(traverse_log)
            else:
                pl=alpha(node.player)
                name=pl+str(move)
                child=Node(name,childState,CP)
                bestV=max(bestV,min_ab(child,depth-1,50001,capable,alph,beta))
                if depth==cutOff and bestV!=oldV:
                    if bestV>bestChild:
                        bestChild=bestV
                        NEXT_MOVE=child.state[:]
                if bestV>=beta:
                    traverse_log=node.name+","+str(cutOff-depth)+","+Tostring(bestV)+","+Tostring(alph)+","+Tostring(beta)+"\n"
                    writeTrav.write(traverse_log)
                    return bestV
                alph=max(alph,bestV)
                traverse_log=node.name+","+str(cutOff-depth)+","+Tostring(bestV)+","+Tostring(alph)+","+Tostring(beta)+"\n"
                writeTrav.write(traverse_log)
    return bestV
def min_ab(node,depth,parentVal,nodeCap,alph,beta):
    global NEXT_MOVE
    global bestChild
    global GLOB_CAPEND
    bestV=parentVal
    if nodeCap:
        bestV=-50001
    if depth!=0 or (depth==0 and nodeCap) or (depth==0 and GLOB_CAPEND):
        GLOB_CAPEND=False
        traverse_log=node.name+","+str(cutOff-depth)+","+Tostring(bestV)+","+Tostring(alph)+","+Tostring(beta)+"\n"
        writeTrav.write(traverse_log)
    if not nodeCap and (checkTerminal(node,node.player,depth)):
        value=str(node.state[MAX][NPITS]-node.state[MIN][NPITS])
        traverse_log=node.name+","+str(cutOff-depth)+","+Tostring(value)+","+Tostring(alph)+","+Tostring(beta)+"\n"
        writeTrav.write(traverse_log)
        return node.state[MAX][NPITS]-node.state[MIN][NPITS]
    for ind in range(NPITS):
        if node.player==1:
            ind=NPITS-ind-1
        if node.state[node.player][ind]!=0:
            val=node.state[node.player][ind]
            childState=deepcopy(node.state)
            childState,capable=makeMove(childState,val,ind,node.player)
            if capable:
                CP=node.player                
            else:
                CP=otherP(node.player)
            if node.player==1:
                move=NPITS-ind+1
            else:
                move=ind+2
            oldV=bestV
            if nodeCap:
                pl=alpha(node.player)
                name=pl+str(move)
                child=Node(name,childState,CP)
                bestV=max(bestV,min_ab(child,depth,50001,capable,alph,beta))
                if depth==cutOff-1 and bestV!=oldV:
                    if bestV>bestChild:
                        bestChild=bestV
                        NEXT_MOVE=child.state[:]
                if bestV>=beta:
                    traverse_log=node.name+","+str(cutOff-depth)+","+Tostring(bestV)+","+Tostring(alph)+","+Tostring(beta)+"\n"
                    writeTrav.write(traverse_log)
                    return bestV
                alph=max(alph,bestV)
                traverse_log=node.name+","+str(cutOff-depth)+","+Tostring(bestV)+","+Tostring(alph)+","+Tostring(beta)+"\n"
                writeTrav.write(traverse_log)
            else:
                pl=alpha(node.player)
                name=pl+str(move)
                child=Node(name,childState,CP)
                bestV=min(bestV,max_ab(child,depth-1,-50001,capable,alph,beta))
                if bestV<=alph:
                    traverse_log=node.name+","+str(cutOff-depth)+","+Tostring(bestV)+","+Tostring(alph)+","+Tostring(beta)+"\n"
                    writeTrav.write(traverse_log)
                    return bestV
                beta=min(beta,bestV)
                traverse_log=node.name+","+str(cutOff-depth)+","+Tostring(bestV)+","+Tostring(alph)+","+Tostring(beta)+"\n"
                writeTrav.write(traverse_log)
    return bestV
#readInput=open(str(sys.argv[2]),'r').readlines() 
readInput=open("input_8.txt",'r').readlines()
i=0
for e in readInput:
    readInput[i]=e.strip()
    i+=1
writeOutput = open('next_state.txt', 'w')
algoType=int(readInput[0])
playerNum=int(readInput[1])
global cutOff
cutOff=int(readInput[2])
boardState=[]
boardState.append(readInput[3].split(' '))
boardState.insert(0,readInput[4].split(' '))
for i in range(len(boardState[0])):
    boardState[0][i]=int(boardState[0][i])
    boardState[1][i]=int(boardState[1][i])
stones2=int(readInput[5])
stones1=int(readInput[6])
boardState[1].reverse()
boardState[0].append(stones1)
boardState[1].append(stones2)

Node = namedtuple("Node", ['name','state','player'])
player=playerNum
global MAX
global MIN
global NPITS

MAX=player-1
MIN=((2*player)%3)-1
NPITS=len(boardState[0])-1
root=Node('root',boardState,MAX)
if algoType==1:
    cutOff=1
    minimax(root,cutOff)
elif algoType==2:
    writeTrav= open('traverse_log.txt', 'w')
    writeTrav.write("Node,Depth,Value\n")
    minimax(root,cutOff)
    writeTrav.close()
else:
    writeTrav= open('traverse_log.txt', 'w')
    writeTrav.write("Node,Depth,Value,Alpha,Beta\n")
    alphabeta(root,cutOff)
    writeTrav.close()
writeOutput.close()
