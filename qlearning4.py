from __future__ import division
import random
import matplotlib.pyplot as plt
import sys


grid=[[0 for i in range(4)] for j in range(3) ]
actions={}
converter={'u':0,'d':1,'l':2,'r':3}
probability=0.70
epsilons = [0.2,0.4,0.6,0.8]

#Setting Up actions for each state
for i in range(3):
    for j in range(4):
        a=[]
        a.append(-1) if i==0 else a.append('u') #Up
        a.append(-1) if i==2 else a.append('d') #Down
        a.append(-1) if j==0 else a.append('l') #Left
        a.append(-1) if j==3 else a.append('r') #Right
        actions[str(i)+str(j)]=a                # Link actions with every state
actions['11']=[-1,-1,-1,-1]

#Set Up Rewards
rewards=[[0,0,0,0] for i in range(12)]
rewards[4][3]=100
rewards[6][2]=100
rewards[1][1]=100
rewards[9][0]=100




gamma= 0.9
iterations=300

def qlearning():
    for epsilon in epsilons:
        prevqsum = 0
        currqsum = 0
        visit = [[0, 0, 0, 0] for i in range(12)]
        nrewards = [[0, 0, 0, 0] for i in range(12)]
        dqsum = []
        qtable = [[-1 for i in range(4)] for i in range(12)]
        for i in range(12):
            for j in range(4):
                if actions[str(int(i/4))+str(int(i%4))][j]!=-1:
                    qtable[i][j]=random.uniform(0,1)*0.0001

        for i in range(iterations):
            state=random.randint(0,11)
            while state!=5: #(For GoalState6(i-1 standard in array)))
                # print state
                row = int(state / 4)
                col = int(state % 4)
                next_actions = actions[str(row) + str(col)]

                if random.uniform(0, 1) > (1 - epsilon):
                    plannedAction = next_actions[random.randint(0, 3)]
                    while plannedAction == -1:
                        plannedAction = next_actions[random.randint(0, 3)]
                else:
                    maxAction = -sys.maxint
                    for i in next_actions:
                        if i != -1:
                            maxAction = max(maxAction, qtable[state][converter[i]])
                    plannedAction = qtable[state].index(maxAction)
                    for k, v in converter.iteritems():
                        if plannedAction == v:
                            plannedAction = k

                fstate = future_state(state, plannedAction)
                visit[state][converter[plannedAction]]+=1
                alpha = 1 / (1 + visit[state][converter[plannedAction]])
                randomValue=random.uniform(0,1)

                if randomValue<probability: #For Desired Action
                    reward = rewards[state][converter[plannedAction]]
                    nrewards[state][converter[plannedAction]] += rewards[state][converter[plannedAction]]
                    old_qsa = qtable[state][converter[plannedAction]]
                    new_qsa = (1 - alpha) * old_qsa + alpha * (reward + gamma * findmaxq(state,plannedAction,qtable))
                    qtable[state][converter[plannedAction]] = new_qsa
                else:                       #For Undesired Action
                    randomAction=next_actions[random.randint(0, 3)]
                    while randomAction==plannedAction or randomAction==-1:
                        randomAction = next_actions[random.randint(0, 3)]
                    reward = rewards[state][converter[randomAction]]
                    nrewards[state][converter[plannedAction]] += rewards[state][converter[randomAction]]
                    old_qsa = qtable[state][converter[plannedAction]]
                    new_qsa = (1 - alpha) * old_qsa + alpha * (reward + gamma * findmaxq(state, randomAction,qtable))
                    qtable[state][converter[plannedAction]] = new_qsa

                state=fstate
            prevqsum=currqsum
            currqsum=0
            for i in range(12):
                for j in range(4):
                    if qtable[i][j]!=-1:
                        currqsum+=qtable[i][j]
            dqsum.append(abs(currqsum-prevqsum))
        plt.plot(dqsum)
        plt.ylabel("Delta Qsum")
        plt.xlabel("Iterations for Epsilon=%s"%(epsilon))
        plt.show()


        print "QTable for Epsilon=%s"%(str(epsilon))
        print '%15s %15s %15s %15s %15s' % ("State", "Up", "Down", "Left", "Right")
        for i in range(12):
            print '%15s' % str(i + 1),
            for j in range(4):
                if qtable[i][j] != -1:
                    print '%15.7f' % qtable[i][j],
                else:
                    print '%15s' % str(-1),
            print ''

        print "Expected Rewards"
        print '%15s %15s %15s %15s %15s' % ("State", "Up", "Down", "Left", "Right")
        showstates=[1,4,6,9]
        for i in range(12):
            if i in showstates:
                print '%15s' % str(i + 1),
                for j in range(4):
                    if nrewards[i][j]!=0:
                        print '%15.7f' % (nrewards[i][j]/visit[i][j]),
                    else:
                        print '%15s' % str(-1),
                print ''

def findmaxq(state,action,qtable):
    # print "here"
    fstate=future_state(state,action)
    row=int(fstate/4)
    col=int(fstate%4)
    future_actions=actions[str(row) +str(col)]
    m=0
    for i in future_actions:
        if i!=-1:
            m=max(m,qtable[fstate][converter[i]])
    return m

def future_state(state,action):
    fstate=0
    if action=='u':
        fstate=state-4
    elif action=='d':
        fstate=state+4
    elif action=='l':
        fstate=state-1
    elif action=='r':
        fstate=state+1
    return fstate


qlearning()