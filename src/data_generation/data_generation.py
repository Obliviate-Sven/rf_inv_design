import random
import os
from simulation import em_simulation
from data_util import Input_Data, attach_ports
from data_util import post_data_processing
from plot import draw_plot
import time

# x: width, y: lenth, z: thickness
iteration = 1

current_time = time.localtime()
date = f"{current_time.tm_year % 100}.{current_time.tm_mon}.{current_time.tm_mday}"
experiment_index = f"{date}_{iteration}_iter"

# path setting
src_path = os.path.abspath(__file__) # data_generation.py
src_dir = os.path.dirname(src_path) # data_generation
# src_dir = os.path.dirname(src_dir) # src
project_dir = os.path.dirname(src_dir)
s12_tmp_data_file = "s12_output.csv"
s34_tmp_data_file = "s34_output.csv"

# device pixel num in width and lenth
input_width = 16
input_lenth = 16
# random pixel num
# input_range = [12, 14, 16, 18]
# input_width = random.choice(input_range)
# input_lenth = random.choice(input_range)

start_time = time.time()
for i in range(iteration):
    
    input_data = Input_Data()
    input_mat, ports_dict = input_data.random_input(input_width, input_lenth)
    
    # device shape
    dev_w = 300
    dev_l = 300
    # random device shape
    # device_range = [200, 220, 240, 260, 280, 300] 
    # dev_w = random.choice(input_range)
    # dev_l = random.choice(input_range)

    em_simulation(project_dir, s12_tmp_data_file, s34_tmp_data_file, experiment_index, input_mat, ports_dict, dev_w, dev_l)
    
    input_with_ports = attach_ports(input_mat, ports_dict)    

    post_data_processing(project_dir, s12_tmp_data_file, s34_tmp_data_file, experiment_index, input_with_ports)
    
    print(f"--iteration {i} completed--")

end_time = time.time()
elapsed_time = end_time - start_time

print(f"simulation time : {elapsed_time:.6f}s, {iteration} iterations, average simulation time : {(elapsed_time/iteration):.6f}s")