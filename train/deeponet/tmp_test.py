import time
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import pandas as pd
from sklearn.model_selection import train_test_split
from dataset import Data

train_csv = './example.csv'

train_dataset = Data(csv_file=train_csv)

train_dataset.__getitem__(0)
train_dataset.__getitem__(1)
train_dataset.__getitem__(2)