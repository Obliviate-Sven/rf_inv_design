import time
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import pandas as pd
from sklearn.model_selection import train_test_split
from dataset import Data
from model import DeepCNN


batch_size = 5000
init_lr = 0.001
lr_decay = 0.8
epochs = 120
l2_lambda = 0.0001

device = torch.device('cuda:3' if torch.cuda.is_available() else 'cpu')

train_csv = './train_temp.csv'

# df = pd.read_csv('../dataset.csv')

# train_df, test_df = train_test_split(df, test_size=0.15, random_state=42)

# test_csv = 'test.csv'
# test_df.to_csv(test_csv, index=False)

# train_csv = 'train_temp.csv'
# train_df.to_csv(train_csv, index=False)

train_dataset = Data(csv_file=train_csv)
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

model = DeepCNN(input_channels=1, output_dim=train_dataset.y.shape[1]).to(device)

criterion = nn.L1Loss()

optimizer = torch.optim.Adam(model.parameters(), lr=init_lr, weight_decay=l2_lambda)

scheduler = torch.optim.lr_scheduler.StepLR(optimizer, epochs/10, gamma=lr_decay)

start_time = time.time()
for epoch in range(epochs):
    epoch_start_time = time.time()
    model.train()
    epoch_loss = 0.0

    for i, (samples, labels) in enumerate(train_loader):
        samples = samples.to(device).float()
        labels = labels.to(device).float()

        samples = samples.view(-1, 1, 18, 18)

        outputs = model(samples)
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        epoch_loss += loss.item()

    scheduler.step()
    epoch_end_time = time.time()
    epoch_elapsed_time = epoch_end_time - epoch_start_time
    if len(train_loader)>0:
        print(f'Epoch [{epoch+1}/{epochs}], Loss: {epoch_loss/len(train_loader):.4f}, LR: {scheduler.get_last_lr()[0]:.6f}, epoch time: {epoch_elapsed_time:.6f}s')
    else:
        print(f'Epoch [{epoch+1}/{epochs}], Loss: {epoch_loss:.4f}, LR: {scheduler.get_last_lr()[0]:.6f}, epoch time: {epoch_elapsed_time:.6f}s')
end_time = time.time()
elapsed_time = end_time - start_time
torch.save(model.state_dict(), 'deepcnn_model.pth')

print(f"training time : {elapsed_time:.6f}s, {epochs} epochs")