import torch
import torch.nn as nn
from model import DeepCNN
from data_generation.data_util import Input_Data, attach_ports
from data_generation.data_generation import input_width, input_lenth

model = DeepCNN()
input_data = Input_Data()

model.load_state_dict(torch.load('../models/cnn_model.pth'))
model.eval()

input_mat, ports_dict = input_data.random_input(input_width, input_lenth)
input_with_ports = attach_ports(input_mat, ports_dict)
output = model(input_with_ports)