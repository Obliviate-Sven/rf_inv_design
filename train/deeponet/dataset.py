import torch
from torch.utils.data import Dataset
import sys, os
import pandas as pd

class Data(Dataset):
    def __init__(self, csv_file, device):
        self.mode = "train"
        self.device = device
        
        print("--reading dataset--")
        self.data = pd.read_csv(csv_file, header=None)

        # shape: [71]
        self.freq = torch.arange(30, 101, dtype=torch.float32)
        
        input_lenth = 16
        input_width = 16
        # 2 port pixel need to be added
        input_num = (input_lenth + 2) * (input_width + 2)
        
        print("--processing dataset--")
        # 18 * 18 = 324
        self.u = self.data.iloc[:, -input_num:].values.astype('int')
        
        # 9 S params(3 in dB, 3 real part, 3 imaginary part) for 71 frequency points, 9 * 71 = 639
        # "dB(S(1,1))", "dB(S(1,2))", "dB(S(2,2))", "re(S(1,1))", "re(S(1,2))", "re(S(2,2))", "im(S(1,1))", "im(S(1,2))", "im(S(2,2))"
        # select the real part and the imaginary part
        cols_to_select = [i for i in range(639) if i % 9 in [3,4,5,6,7,8]]
        
        self.y = self.data.iloc[:, cols_to_select].values.astype('float32')
        print("--dataset initialize successfully--")
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        u = torch.tensor(self.u[idx])
        u = u.unsqueeze(0).repeat(71, 1)
        u = u.view(71, 1, 18, 18)
        # print(f"u shape: {u.shape}")
        y = self.y[idx]
        y = torch.tensor(y.reshape(71, 6))
        # print(f"y shape: {y.shape}")
        freq = self.freq
        freq = freq.unsqueeze(-1)
        # print(f"freq shape: {freq.shape}")
        return u, y, freq
            
    def train(self):
        self.mode = "train"
        u, y, freq = next(iter(self))

        return {"u": u.to(self.device), "y": y.to(self.device), "freq": freq.to(self.device)}

    def eval(self):
        self.mode = "eval"
        u, y, freq = next(iter(self))

        return {"u": u.to(self.device), "y": y.to(self.device), "freq": freq.to(self.device)}
    