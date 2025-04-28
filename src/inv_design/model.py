import torch
import torch.nn as nn
import torch.nn.functional as F

class DeepCNN(nn.Module):
    def __init__(self, input_channels=1, output_dim=426, dropout_p=0.5):
        super(DeepCNN, self).__init__()
        
        self.conv_layers = nn.Sequential(
            # Conv layer 1: kernel size 12
            nn.Conv2d(input_channels, 64, kernel_size=12, stride=1, padding=6),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(negative_slope=0.01, inplace=True),
            
            # Conv layer 2: kernel size 10
            nn.Conv2d(64, 64, kernel_size=10, stride=1, padding=5),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(negative_slope=0.01, inplace=True),
            
            # Conv layer 3: kernel size 8
            nn.Conv2d(64, 64, kernel_size=8, stride=1, padding=4),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(negative_slope=0.01, inplace=True),
            
            # Conv layer 4: kernel size 6
            nn.Conv2d(64, 64, kernel_size=6, stride=1, padding=3),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(negative_slope=0.01, inplace=True),
            
            # 第一次最大池化
            # nn.MaxPool2d(kernel_size=2),
            
            # Conv layer 5: kernel size 5
            nn.Conv2d(64, 64, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(negative_slope=0.01, inplace=True),
            
            # Conv layer 6: kernel size 5
            nn.Conv2d(64, 64, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(negative_slope=0.01, inplace=True),
            
            # Conv layer 7: kernel size 4
            nn.Conv2d(64, 64, kernel_size=4, stride=1, padding=2),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(negative_slope=0.01, inplace=True),
            
            # Conv layer 8: kernel size 4
            nn.Conv2d(64, 64, kernel_size=4, stride=1, padding=2),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(negative_slope=0.01, inplace=True),
            
            # 第二次最大池化
            # nn.MaxPool2d(kernel_size=2),
            
            # Conv layer 9: kernel size 4
            nn.Conv2d(64, 64, kernel_size=4, stride=1, padding=2),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(negative_slope=0.01, inplace=True),
            
            # Conv layer 10: kernel size 3
            nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(negative_slope=0.01, inplace=True),
            
            # Conv layer 11: kernel size 3
            nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(negative_slope=0.01, inplace=True),
            
            # Conv layer 12: kernel size 3
            nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(negative_slope=0.01, inplace=True)
        )
        
        self.fc_input_dim = 64 * 25 * 25

        self.fc1 = nn.Linear(self.fc_input_dim, 500)
        self.fc2 = nn.Linear(500, 500)
        self.fc3 = nn.Linear(500, 500)
        self.fc4 = nn.Linear(500, 500)
        self.fc5 = nn.Linear(500, output_dim)
        
        self.dropout = nn.Dropout(p=dropout_p)
    
    def forward(self, x):
        """
        input x shape (batch_size, 1, 18, 18)
        """
        x = self.conv_layers(x)
        x = x.view(x.size(0), -1)
        
        x = F.leaky_relu(self.fc1(x), negative_slope=0.01)
        x = self.dropout(x)
        x = F.leaky_relu(self.fc2(x), negative_slope=0.01)
        x = self.dropout(x)
        x = F.leaky_relu(self.fc3(x), negative_slope=0.01)
        x = self.dropout(x)
        x = F.leaky_relu(self.fc4(x), negative_slope=0.01)
        x = self.dropout(x)
        x = self.fc5(x)
        
        x = torch.tanh(x)
        return x
