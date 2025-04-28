import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from dataset import Data
from model import DeepCNN

batch_size = 5000
init_lr = 0.001
lr_decay = 0.8
epochs = 40
l2_lambda = 0.0001

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

train_dataset = Data(csv_file='../dataset.csv')
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

model = DeepCNN(input_channels=1, output_dim=train_dataset.y.shape[1]).to(device)

criterion = nn.L1Loss()

optimizer = torch.optim.Adam(model.parameters(), lr=init_lr, weight_decay=l2_lambda)

scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=4, gamma=lr_decay)

for epoch in range(epochs):
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

    print(f'Epoch [{epoch+1}/{epochs}], Loss: {epoch_loss/len(train_loader):.4f}, LR: {scheduler.get_last_lr()[0]:.6f}')

torch.save(model.state_dict(), 'deepcnn_model.pth')