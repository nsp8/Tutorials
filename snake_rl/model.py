import os
import torch
import torch.nn as nn
import torch.nn.functional as f


class LinearQNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear_1 = nn.Linear(input_size, hidden_size)
        self.linear_2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = f.relu(self.linear_1(x))
        x = self.linear_2(x)
        # no activation required here for now
        return x

    def save(self, file_name: str = "model.pth"):
        folder = "./model"
        if not os.path.exists(folder):
            os.makedirs(folder)
        file_name = os.path.join(folder, file_name)
        torch.save(self.state_dict(), file_name)
