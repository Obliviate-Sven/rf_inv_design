import time
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import pandas as pd
from sklearn.model_selection import train_test_split
from dataset import Data
from model import DeepONet


init_lr = 0.001
lr_decay = 0.8
epochs = 5
l2_lambda = 0.0001

device = torch.device('cuda:3' if torch.cuda.is_available() else 'cpu')

train_csv = './data/test_temp.csv'

# df = pd.read_csv('../dataset.csv')

# train_df, test_df = train_test_split(df, test_size=0.15, random_state=42)

# test_csv = 'test.csv'
# test_df.to_csv(test_csv, index=False)

# train_csv = 'train_temp.csv'
# train_df.to_csv(train_csv, index=False)

dataset = Data(csv_file=train_csv, device=device)

model = DeepONet(
                trunk_in_features=1,
                trunk_hidden_features=32,
                inner_prod_features=6,
                num_trunk_hidden_layers=3,
                nonlinearity="tanh").to(device)

criterion = nn.L1Loss()
# criterion = nn.MSELoss()

optimizer = torch.optim.Adam(model.parameters(), lr=init_lr, weight_decay=l2_lambda)

scheduler = torch.optim.lr_scheduler.StepLR(optimizer, 4, gamma=lr_decay)

start_time = time.time()
for epoch in range(epochs):
    epoch_start_time = time.time()
    model.train()
    epoch_loss = 0.0

    for step in range(len(dataset)):
        model_input = dataset.train()

        model_output = model(model_input)
        
        labels = model_output["label"]
        outputs = model_output["model_out"]
        
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        epoch_loss += loss.item()

    scheduler.step()
    epoch_end_time = time.time()
    epoch_elapsed_time = epoch_end_time - epoch_start_time
    
    print(f'Epoch [{epoch+1}/{epochs}], Loss: {epoch_loss/len(dataset):.6f}, LR: {scheduler.get_last_lr()[0]:.6f}, epoch time: {epoch_elapsed_time:.6f}s')
end_time = time.time()
elapsed_time = end_time - start_time
torch.save(model.state_dict(), 'deeponet_model.pth')

print(f"training time : {elapsed_time:.6f}s, {epochs} epochs")