import os
import time
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from dataset import Data
from model import DeepCNN
import pandas as pd
from sklearn.model_selection import train_test_split

batch_size = 50       
device = torch.device("cuda:3" if torch.cuda.is_available() else "cpu")
model_path = '../models/deepcnn_model.pth' 

test_csv = 'test.csv'
test_dataset = Data(test_csv)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

output_dim = test_dataset.y.shape[1]
model = DeepCNN(input_channels=1, output_dim=output_dim)
model = model.to(device)

if os.path.exists(model_path):
    checkpoint = torch.load(model_path, map_location=device)
    model.load_state_dict(checkpoint)
    print("Loaded model from", model_path)
else:
    print("Model file not found:", model_path)
    exit(1)

model.eval()
criterion = nn.L1Loss() 

total_loss = 0.0
total_samples = 0

with torch.no_grad():
    for samples, labels in test_loader:

        samples = samples.to(device).float()
        labels = labels.to(device).float()
        
        # 调整输入尺寸为 (batch_size, 1, 18, 18)
        samples = samples.view(-1, 1, 18, 18)
        
        outputs = model(samples)
        loss = criterion(outputs, labels)

        total_loss += loss.item() * samples.size(0)
        total_samples += samples.size(0)

avg_loss = total_loss / total_samples
print("Average MAE on test dataset: {:.4f}".format(avg_loss))

os.remove(test_csv)