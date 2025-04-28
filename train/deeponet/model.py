import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import OrderedDict


class tanh(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, x):
        return torch.tanh(x)


def xavier_init(layer):
    with torch.no_grad():
        if type(layer) == nn.Linear:
            if hasattr(layer, "weight"):
                nn.init.xavier_normal_(layer.weight)
        else:
            raise TypeError(f"Expecting nn.Linear got type={type(layer)} instead")


class FCBlock(nn.Module):

    def __init__(
        self,
        out_features=1,
        in_features=3,
        hidden_features=20,
        num_hidden_layers=3,
        nonlinearity="tanh",
        device=None,
    ):
        super().__init__()

        nl_init_dict = dict(
            hard_tanh=(nn.Hardtanh(min_val=-1, max_val=1), xavier_init),
            silu=(nn.SiLU(), xavier_init),
            tanh=(nn.Tanh(), xavier_init),
            relu=(nn.ReLU(), xavier_init),
        )
        nl, init = nl_init_dict[nonlinearity]

        self.net = OrderedDict()

        for i in range(num_hidden_layers + 2):
            if i == 0:
                self.net["fc1"] = nn.Linear(
                    in_features=in_features, out_features=hidden_features
                )
                self.net["nl1"] = nl
            elif i != num_hidden_layers + 1:
                self.net["fc%d" % (i + 1)] = nn.Linear(
                    in_features=hidden_features, out_features=hidden_features
                )
                self.net["nl%d" % (i + 1)] = nl

            else:
                self.net["fc%d" % (i + 1)] = nn.Linear(
                    in_features=hidden_features, out_features=out_features
                )

            init(self.net["fc%d" % (i + 1)])

        self.net = nn.Sequential(self.net)

        if device:
            self.net.to(device)

    def forward(self, x):
        return self.net(x)

class DeepCNN(nn.Module):
    def __init__(
        self, 
        input_channels=1, 
        output_dim=54, 
        dropout_p=0.3,
        ):
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
            
            # Conv layer 9: kernel size 4
            nn.Conv2d(64, 64, kernel_size=4, stride=1, padding=2),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(negative_slope=0.01, inplace=True),
            
            # nn.MaxPool2d(kernel_size=2),
            
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
        # activation = nn.Hardtanh(min_val=-1, max_val=1)
        # x = activation(x)
        return x

class DeepONet(nn.Module):

    def __init__(
        self,
        trunk_in_features=3,
        trunk_hidden_features=128,
        inner_prod_features=6,
        num_trunk_hidden_layers=3,
        nonlinearity="tanh",
        device=None,
    ):
        super().__init__()

        self.branch = DeepCNN(input_channels=1, output_dim=6, dropout_p=0.3)

        self.trunk = FCBlock(
            out_features=inner_prod_features,
            in_features=trunk_in_features,
            hidden_features=trunk_hidden_features,
            num_hidden_layers=num_trunk_hidden_layers,
            nonlinearity=nonlinearity,
            device=device,
        )

        self.b_0 = nn.Parameter(
            torch.zeros(1, device=device).uniform_(), requires_grad=True
        )

    def forward(self, model_input):

        branch_input = model_input["u"].clone().detach().float().requires_grad_(True)
        trunk_input = model_input["freq"].clone().detach().float().requires_grad_(True)
        label = model_input["y"]
        
        
        output_1 = self.branch(branch_input)
        output_2 = self.trunk(trunk_input)
        
        output = output_1 * output_2 + self.b_0

        return {"model_in": branch_input, "model_out": output, "label": label}
