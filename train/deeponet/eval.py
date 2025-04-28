import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import pandas as pd
from dataset import Data
from model import DeepONet
import time

device = torch.device('cuda:3' if torch.cuda.is_available() else 'cpu')

# 测试数据路径
test_csv = './data/train_temp.csv'

# 加载测试数据集
test_dataset = Data(csv_file=test_csv, device=device)

# 模型实例化
model = DeepONet(
                trunk_in_features=1,
                trunk_hidden_features=32,
                inner_prod_features=6,
                num_trunk_hidden_layers=3,
                nonlinearity="tanh"
            ).to(device)

# 加载训练完成的模型参数
model.load_state_dict(torch.load('./deeponet_model.pth', map_location=device))
model.eval()

criterion = nn.L1Loss(reduction='sum')
# criterion = nn.MSELoss()

# 开始评估
total_loss = 0.0
start_time = time.time()

with torch.no_grad():
    for step in range(len(test_dataset)):
        model_input = test_dataset.eval()
        model_output = model(model_input)
        
        labels = model_output["label"]
        outputs = model_output["model_out"]

        loss = criterion(outputs, labels)
        
        loss = loss/labels.size(0)/labels.size(1)

        total_loss += loss.item() * labels.size(0)

average_loss = total_loss / len(test_dataset)

elapsed_time = time.time() - start_time

print(f"Test Loss (L1): {average_loss:.6f}")
print(f"Evaluation Time: {elapsed_time:.6f}s")
