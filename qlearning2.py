import random
import matplotlib.pyplot as plt
import sys

grid=[[0 for i in range(4)] for j in range(3) ]
actions={}
converter={'u':0,'d':1,'l':2,'r':3}
epsilons = [0.0,0.2,0.4,0.6,0.8,1.0]

#Setting Up actions for each state
for i in range(3):
    for j in range(4):
        a=[]
        a.append(-1) if i==0 else a.append('u') #Up
        a.append(-1) if i==2 else a.append('d') #Down
        a.append(-1) if j==0 else a.append('l') #Left
        a.append(-1) if j==3 else a.append('r') #Right
        actions[str(i)+str(j)]=a              # Link actions with every state
actions['11']=[-1,-1,-1,-1]

#Set Up Rewards
rewards=[[0,0,0,0] for i in range(12)]
rewards[4][3]=100
rewards[6][2]=100
rewards[1][1]=100
rewards[9][0]=100

gamma= 0.9
iterations=450




def qlearning():

    for epsilon in epsilons:
        prevqsum = 0
        currqsum = 0
        dqsum = []
        qtable = [[-1 for i in range(4)] for i in range(12)]
        for i in range(12):
            for j in range(4):
                if actions[str(i/4)+str(i%4)][j]!=-1:
                    qtable[i][j]=random.uniform(0,1)*0.0001

        for i in range(iterations):
            state=random.randint(0,11)
            while state!=5: #(For GoalState6(i-1 standard in array)))
                row = state / 4
                col = (state % 4)
                next_actions = actions[str(row) + str(col)]

                if random.uniform(0,1)>(1-epsilon):
                    action = next_actions[random.randint(0, 3)]
                    while action == -1:
                        action = next_actions[random.randint(0, 3)]
                else:
                    maxAction=-sys.maxint
                    for i in next_actions:
                        if i!=-1:
                            maxAction=max(maxAction,qtable[state][converter[i]])
                    action = qtable[state].index(maxAction)
                    # print maxAction,
                    # print "#",
                    # print state,
                    # print action

                    for k,v in converter.iteritems():
                        if action==v:
                            action=k


                fstate = future_state(state, action)

                reward=rewards[state][converter[action]]
                maxq=findmaxq(state,action,qtable)
                score =(reward + gamma * maxq )
                qtable[state ][converter[action]]=score
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
        plt.xlabel("Iterations for Epsilon %s" %(epsilon))
        plt.show()
        print "Qtable for Epsilon="+str(epsilon)
        print '%15s %15s %15s %15s %15s' % ("State", "Up", "Down", "Left", "Right")
        for i in range(12):
            print '%15s'%str(i+1),
            for j in range(4):
                if qtable[i][j]!=-1:
                    print '%15.7f'%qtable[i][j],
                else:
                    print '%15s'%str(-1),
            print ''

            # print '%15s %15.7f %15.7f %15.7f %15.7f' % (
            # str(i + 1), (qtable[i][0]) if qtable[i][0]!=-1 else -1 , (qtable[i][1])if qtable[i][1]!=-1 else -1, (qtable[i][2])if qtable[i][2]!=-1 else -1, (qtable[i][3])if qtable[i][3]!=-1 else -1)






def findmaxq(state,action,qtable):

    fstate=future_state(state,action)
    row=fstate/4
    col=(fstate%4)
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