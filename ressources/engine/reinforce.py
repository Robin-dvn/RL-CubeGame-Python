import torch.nn as nn
import torch.optim as optim
from torch.distributions.categorical import Categorical
import numpy as np
import torch



def layer_init(layer,std=np.sqrt(2),bias_const = 0.1):
    nn.init.constant_(layer.weight,0)
    nn.init.constant_(layer.bias,bias_const)    
    return layer

class Agent(nn.Module):
    def __init__(self):
        super(Agent,self).__init__()
        self.net = nn.Sequential(
            layer_init(nn.Linear(53,64)),
            nn.Tanh(),
            layer_init(nn.Linear(64,64)),
            nn.Tanh(),
            layer_init(nn.Linear(64,6),std=0.01),
            nn.Softmax()
        ) 

    def forward(self, x):
        return self.net(x.float())


class REINFORCE:
    def __init__(self):
        
        #hyperparameters
        self.learning_rate = 0.01
        self.gamma  = 0.9
        self.eps = 1e-5

        self.probs = []
        self.rewards = []
        
        self.net = Agent()
        self.optimizer = optim.Adam(self.net.parameters(), lr=self.learning_rate, eps = self.eps)

    def sample_action(self, state):
        
        state = torch.tensor(np.array([state]))
        action_probs = self.net(state)
        
        #print(action_probs)


        distrib = Categorical(probs=action_probs)
        
        action = distrib.sample()
        
        prob = distrib.log_prob(action)

        action = action.numpy()

        self.probs.append(prob)

        return action, prob

    def update(self,bestplayer):
        """Updates the policy network's weights."""
        running_g = 0
        gs = []
        self.rewards = bestplayer.reward *1
        self.probs =bestplayer.probs *1
        
        

        # Discounted return (backwards) - [::-1] will return an array in reverse
        for R in self.rewards[::-1]:
            running_g = R + self.gamma * running_g
            gs.insert(0, running_g)

        deltas = torch.tensor(gs)
        
       
        
        loss = 0.

        
            

        # minimize -1 * prob * reward obtained
        for log_prob, delta in zip(self.probs, deltas):
            
            loss += log_prob.mean() * delta 
        print("loss",loss)
        if loss != 0.:
        
            # Update the policy network
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

            # Empty / zero out all episode-centric/related variables
            self.probs = []
            self.rewards = []