import numpy as np
import pandas as pd
from random import seed
from random import random
import matplotlib.pyplot as plt
import pylab
import networkx as nx


G = nx.DiGraph()
G2 = nx.DiGraph()

#Edges
G.add_edges_from([('A', 'B'),('C','D'),('G','D')], weight=1)
G.add_edges_from([('D','A'),('D','E'),('B','D'),('D','E')], weight=2)
G.add_edges_from([('B','C'),('E','F')], weight=3)
G.add_edges_from([('C','H')], weight=4)

G2.add_edges_from([('A', 'B'),('C','D'),('G','D')], weight=1)
G2.add_edges_from([('D','A'),('D','F'),('B','C'),('D','H')], weight=2)
G2.add_edges_from([('H','B'),('E','F')], weight=3)
G2.add_edges_from([('C','H'),('F','H')], weight=4)

#Nodes Colors
val_map = {'A': 0.234 ,'D': 0.5714285714285714,'H': 0.0}
values = [val_map.get(node, 0.45) for node in G.nodes()]

val_map2 = {'A': 0.657 ,'D': 0.73213,'H': 0.123}
values2 = [val_map2.get(node, 0.45) for node in G2.nodes()]

edge_labels=dict([((u,v,),d['weight']) for u,v,d in G.edges(data=True)])
edge_labels2=dict([((u,v,),d['weight']) for u,v,d in G2.edges(data=True)])

red_edges = [('C','D'),('D','A')]
red_edges2 = [('C','H'),('D','E')]

edge_colors = ['black' if not edge in red_edges else 'red' for edge in G.edges()]
edge_colors2 = ['black' if not edge in red_edges else 'red' for edge in G2.edges()]

pos=nx.spring_layout(G)
pos2=nx.spring_layout(G2, center=(1, 1) )

nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
nx.draw(G, pos, node_color = values, node_size=1500,edge_color=edge_colors, edge_cmap=plt.cm.Reds, with_labels = True)

nx.draw_networkx_edge_labels(G2,pos2,edge_labels=edge_labels2)
nx.draw(G2, pos2, node_color = values2, node_size=1500,edge_color=edge_colors2, edge_cmap=plt.cm.Reds, with_labels = True)

pylab.show()

#mkv IMPLEMENTATION

P = np.array([[0.2, 0.7, 0.1],
              [0.9, 0.0, 0.1],
              [0.2, 0.8, 0.0]])

stateChangeHist = np.array([[0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0]])

state = np.array([[1.0, 0.0, 0.0]])
currentState = 0
nextState = 0
stateHist = state
dfStateHist = pd.DataFrame(state)
distr_hist = [[0, 0, 0]]
seed(4)

# Simulate from multinomial distribution

def simulate_multinomial(vmultinomial, nextState):
    r = np.random.uniform(0.0, 1.0)
    CS = np.cumsum(vmultinomial)
    CS = np.insert(CS, 0, 0)
    m = (np.where(CS < r))[0]
    nextState = m[len(m) - 1]
    return nextState


for x in range(1000):
    currentRow = np.ma.masked_values((P[currentState]), 0.0)
    nextState = simulate_multinomial(currentRow, nextState)

    # Keep track of state changes
    stateChangeHist[currentState, nextState] += 1

    # Keep track of the state vector itself
    state = np.array([[0, 0, 0]])
    state[0, nextState] = 1.0

    # Keep track of state history
    stateHist = np.append(stateHist, state, axis=0)

    currentState = nextState

    # calculate the actual distribution over the 3 states so far
    totals = np.sum(stateHist, axis=0)
    gt = np.sum(totals)
    distrib = totals / gt
    distrib = np.reshape(distrib, (1, 3))
    distr_hist = np.append(distr_hist, distrib, axis=0)

print(distrib)

P_hat = stateChangeHist / stateChangeHist.sum(axis=1)[:, None]

# Check estimated state transition probabilities based on history so far:
print(P_hat)
dfDistrHist = pd.DataFrame(distr_hist)

# Plot the distribution as the simulation progresses over time
dfDistrHist.plot(title="Simulation History")
#plt.show()