import torch
from torch.optim import Adam
from torch.nn import MSELoss


def handle_multi_dimension_values(state_prev, action, reward, state_next, status):
    state_prev = torch.tensor(state_prev, dtype=torch.float)
    action = torch.tensor(action, dtype=torch.long)
    reward = torch.tensor(reward, dtype=torch.float)
    state_next = torch.tensor(state_next, dtype=torch.float)
    # handling set of 1-d values (1, x)
    if len(state_prev.shape) == 1:
        state_prev = torch.unsqueeze(state_prev, dim=0)
        action = torch.unsqueeze(action, dim=0)
        reward = torch.unsqueeze(reward, dim=0)
        state_next = torch.unsqueeze(state_next, dim=0)
        status = (status, )
    return state_prev, action, reward, state_next, status


class QTrainer:
    def __init__(self, model, lr: float, gamma: float):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = Adam(model.parameters(), lr=lr)
        self.criterion = MSELoss()

    def train_step(self, state_prev, action, reward, state_next, status):
        state_prev, action, reward, state_next, status = handle_multi_dimension_values(
            state_prev, action, reward, state_next, status
        )
        # Using the Bellman equation:
        # 1. Predicted Q values with the current state: Q = model.predict(state_prev)
        prediction = self.model(state_prev)  # actions: [a1, a2, a3]
        target = prediction.clone()
        # 2. Q_new = reward + gamma * max(Q(state_next))
        for i in range(len(status)):
            Q_new = reward[i]
            if not status[i]:  # if not done
                Q_new = reward[i] + self.gamma * torch.max(self.model(state_next[i]))
            selected_action = torch.argmax(action).item()
            target[i][selected_action] = Q_new
        # 3. Loss: (Q_new - Q) ** 2
        self.optimizer.zero_grad()
        loss = self.criterion(target, prediction)
        loss.backward()
        self.optimizer.step()
