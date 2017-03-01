from __future__ import division
import random
import matplotlib.pyplot as plt


grid=[[0 for i in range(4)] for j in range(3) ]
actions={}
converter={'u':0,'d':1,'l':2,'r':3}
probability=0.70

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

#Set Up Visit
visit=[[0,0,0,0] for i in range(12)]

#Set Up New rewards Table(Expected Rewards)
nrewards=[[0,0,0,0] for i in range(12)]

gamma= 0.9
iterations=20000
qtable=[[-1 for i in range(4)] for i in range(12)]

dqsum=[]

def qlearning():
    prevqsum = 0
    currqsum = 0
    for i in range(iterations):
        state=random.randint(0,11)
        while state!=5: #(For GoalState6(i-1 standard in array)))
            # print state
            row=int(state/4)
            col=int(state%4)
            next_actions=actions[str(row) +str(col)]
            plannedAction=next_actions[random.randint(0,3)]
            while plannedAction==-1:
                plannedAction = next_actions[random.randint(0, 3)]
            fstate = future_state(state, plannedAction)
            visit[state][converter[plannedAction]]+=1
            alpha = 1 / (1 + visit[state][converter[plannedAction]])
            randomValue=random.uniform(0,1)

            if randomValue<probability: #For Desired Action
                reward = rewards[state][converter[plannedAction]]
                nrewards[state][converter[plannedAction]] += rewards[state][converter[plannedAction]]
                old_qsa = qtable[state][converter[plannedAction]]
                new_qsa = (1 - alpha) * old_qsa + alpha * (reward + gamma * findmaxq(state,plannedAction))
                qtable[state][converter[plannedAction]] = new_qsa
            else:                       #For Undesired Action
                randomAction=next_actions[random.randint(0, 3)]
                while randomAction==plannedAction or randomAction==-1:
                    randomAction = next_actions[random.randint(0, 3)]
                reward = rewards[state][converter[randomAction]]
                nrewards[state][converter[plannedAction]] += rewards[state][converter[randomAction]]
                old_qsa = qtable[state][converter[plannedAction]]
                new_qsa = (1 - alpha) * old_qsa + alpha * (reward + gamma * findmaxq(state, randomAction))
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
    plt.xlabel("Iterations")
    plt.show()


    print "QTable"
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
    print '%20s %20s %20s %20s %20s' % ("State", "Up", "Down", "Left", "Right")
    showstates=[1,4,6,9]
    for i in range(12):
        if i in showstates:
            print '%20s %20s %20s %20s %20s' % (
            str(i + 1), str((nrewards[i][0]/visit[i][0]) if nrewards[i][0]!=0 else -1), str((nrewards[i][1]/visit[i][1]) if nrewards[i][1]!=0 else -1),
            str((nrewards[i][2]/visit[i][2]) if nrewards[i][2]!=0 else -1), str((nrewards[i][3]/visit[i][3])) if nrewards[i][3]!=0 else -1)


def findmaxq(state,action):

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