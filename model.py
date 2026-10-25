"""
model.py
--------
Defines the SalaryNet architecture in one place so that both the training
script (train.py) and the web app (app.py) use the exact same network.
"""

import os

import torch
from torch import nn

# Where the trained weights live on disk.
MODEL_PATH = os.path.join(os.path.dirname(__file__), "salary_net.pth")


class SalaryNet(nn.Module):
    """A tiny feed-forward network: 1 input -> 2 hidden (ReLU) -> 1 output."""

    def __init__(self):
        super().__init__()
        self.hidden = nn.Linear(1, 2)
        self.relu = nn.ReLU()
        self.output = nn.Linear(2, 1)

    def forward(self, x):
        h = self.hidden(x)   # Weighted sums
        h = self.relu(h)     # Activation
        salary = self.output(h)
        return salary


def load_model(path: str = MODEL_PATH) -> "SalaryNet":
    """Load a trained SalaryNet from disk and put it in eval mode."""
    model = SalaryNet()
    model.load_state_dict(torch.load(path, map_location="cpu"))
    model.eval()
    return model
