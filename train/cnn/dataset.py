import torch
from torch.utils.data import Dataset
import sys, os
import pandas as pd

class Data(Dataset):
    def __init__(self, csv_file, transform=None):
        print("--reading dataset--")
        self.data = pd.read_csv(csv_file, header=None)
        self.transform = transform
        
        input_lenth = 16
        input_width = 16
        # 2 port pixel need to be added
        input_num = (input_lenth + 2) * (input_width + 2)
        print("--processing dataset--")
        # 18 * 18 = 324
        self.X = self.data.iloc[:, -input_num:].values.astype('int')
        
        # 9 S params(3 in dB, 3 real part, 3 imaginary part) for 71 frequency points, 9 * 71 = 639
        # "dB(S(1,1))", "dB(S(1,2))", "dB(S(2,2))", "re(S(1,1))", "re(S(1,2))", "re(S(2,2))", "im(S(1,1))", "im(S(1,2))", "im(S(2,2))"
        # select the real part and the imaginary part
        # cols_to_select = [i for i in range(639) if i % 9 in [3,4,5,6,7,8]]
        
        # 54 output
        cols_to_select = []
        target_freqs = [30, 37, 40, 50, 60, 70, 80, 90, 100]

        for f in target_freqs:
            base = (f - 30) * 9
            cols_to_select += [base + i for i in range(3, 9)]
        
        self.y = self.data.iloc[:, cols_to_select].values.astype('float32')
        print("--dataset initialize successfully--")
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        sample = torch.tensor(self.X[idx])
        label = torch.tensor(self.y[idx])

        if self.transform:
            sample = self.transform(sample)

        return sample, label