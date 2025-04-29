import torch
import os
import pandas as pd
import numpy as np

def attach_ports(input_mat, ports_dict):
    '''this function combine the pixel and the ports and return the full input matrix with ports'''

    left = ports_dict["left"].T
    right = ports_dict["right"].T
    top = ports_dict["top"]
    bottom = ports_dict["bottom"]

    input_with_sides = torch.cat([left, input_mat, right], dim=1)

    top_padded = torch.cat([torch.zeros(1, 1, dtype=torch.int64), top, torch.zeros(1, 1, dtype=torch.int64)], dim=1) 
    bottom_padded = torch.cat([torch.zeros(1, 1, dtype=torch.int64), bottom, torch.zeros(1, 1, dtype=torch.int64)], dim=1)

    input_with_ports = torch.cat([top_padded, input_with_sides, bottom_padded], dim=0)

    return input_with_ports

def post_data_processing(project_dir, s12_tmp_data_file, s34_tmp_data_file, experiment_index, input_with_ports):
    '''this function extract S params from the original output csv file, and attach input matrix into the file, 
       formating the data file into dataset for training'''

    # processing input matrix
    top_bottom_flip = torch.flip(input_with_ports, dims=[0])
    left_right_flip = torch.flip(input_with_ports, dims=[1])
    
    rot_input_with_ports = torch.rot90(input_with_ports, k=1, dims=[0, 1])
    rot_top_bottom_flip = torch.flip(rot_input_with_ports, dims=[0])
    rot_left_right_flip = torch.flip(rot_input_with_ports, dims=[1])
    
    # flatterning input matrix into 1 line
    input_with_ports_flat = torch.flatten(input_with_ports).numpy()
    top_bottom_flip_flat = torch.flatten(top_bottom_flip).numpy()
    left_right_flip_flat = torch.flatten(left_right_flip).numpy()
    
    rot_input_with_ports_flat = torch.flatten(rot_input_with_ports).numpy()
    rot_top_bottom_flip_flat = torch.flatten(rot_top_bottom_flip).numpy()
    rot_left_right_flip_flat = torch.flatten(rot_left_right_flip).numpy()
    
    tmp_dir = os.path.join(project_dir, "tmp")
    tmp_result_dir = os.path.join(tmp_dir, experiment_index)
    
    s12 = pd.read_csv(os.path.join(tmp_result_dir, s12_tmp_data_file), sep=";", header=0)  
    s34 = pd.read_csv(os.path.join(tmp_result_dir, s34_tmp_data_file), sep=";", header=0)
    
    s12_data = s12[["re(S(1,1))", "re(S(1,2))", "re(S(2,2))", "im(S(1,1))", "im(S(1,2))", "im(S(2,2))"]]
    s34_data = s34[["re(S(3,3))", "re(S(3,4))", "re(S(4,4))", "im(S(3,3))", "im(S(3,4))", "im(S(4,4))"]]
    s21_data = s12[["re(S(2,2))", "re(S(1,2))", "re(S(1,1))", "im(S(2,2))", "im(S(1,2))", "im(S(1,1))"]]
    s43_data = s34[["re(S(4,4))", "re(S(3,4))", "re(S(3,3))", "im(S(4,4))", "im(S(3,4))", "im(S(3,3))"]]    
    
    # flatterning data into 1 line
    s12_data_flat = s12_data.to_numpy().flatten()
    s34_data_flat = s34_data.to_numpy().flatten()
    s21_data_flat = s21_data.to_numpy().flatten()
    s43_data_flat = s43_data.to_numpy().flatten()
    
    # concat s params and input matrix into 1 line
    s12_data_label = np.concatenate((s12_data_flat, input_with_ports_flat))
    s12_td_enhanced_data_label = np.concatenate((s12_data_flat, top_bottom_flip_flat))
    s12_lr_enhanced_data_label = np.concatenate((s21_data_flat, left_right_flip_flat))
    
    s34_data_label = np.concatenate((s34_data_flat, rot_input_with_ports_flat))
    s34_td_enhanced_data_label = np.concatenate((s34_data_flat, rot_top_bottom_flip_flat))
    s34_lr_enhanced_data_label = np.concatenate((s43_data_flat, rot_left_right_flip_flat))

    s12_df = pd.DataFrame([s12_data_label])
    s12_td_enhanced_df = pd.DataFrame([s12_td_enhanced_data_label])
    s12_lr_enhanced_df = pd.DataFrame([s12_lr_enhanced_data_label])
    s34_df = pd.DataFrame([s34_data_label])
    s34_td_enhanced_df = pd.DataFrame([s34_td_enhanced_data_label])
    s34_lr_enhanced_df = pd.DataFrame([s34_lr_enhanced_data_label])
    
    results_dir = os.path.join(project_dir, "results")
    dataset_dir = os.path.join(results_dir, experiment_index)
    os.makedirs(dataset_dir, exist_ok=True)
    output_file_name = f"{experiment_index}_data.csv"
    output_path = os.path.join(dataset_dir, output_file_name)
    
    # save labels
    s12_df.to_csv(output_path, mode='a', index=False, header=False)
    s12_td_enhanced_df.to_csv(output_path, mode='a', index=False, header=False)
    s12_lr_enhanced_df.to_csv(output_path, mode='a', index=False, header=False)
    s34_df.to_csv(output_path, mode='a', index=False, header=False)
    s34_td_enhanced_df.to_csv(output_path, mode='a', index=False, header=False)
    s34_lr_enhanced_df.to_csv(output_path, mode='a', index=False, header=False)
    
def deeponet_post_data_processing(project_dir, s12_tmp_data_file, s34_tmp_data_file, experiment_index, input_with_ports, dev_w, dev_l):
    ''' TBD '''

    window_w = 300
    window_l = 300
    
    mesh_points = window_w * window_l

    # processing input matrix
    top_bottom_flip = torch.flip(input_with_ports, dims=[0])
    left_right_flip = torch.flip(input_with_ports, dims=[1])
    
    rot_input_with_ports = torch.rot90(input_with_ports, k=1, dims=[0, 1])
    rot_top_bottom_flip = torch.flip(rot_input_with_ports, dims=[0])
    rot_left_right_flip = torch.flip(rot_input_with_ports, dims=[1])
    
    # flatterning input matrix into 1 line
    input_with_ports_flat = torch.flatten(input_with_ports).numpy()
    top_bottom_flip_flat = torch.flatten(top_bottom_flip).numpy()
    left_right_flip_flat = torch.flatten(left_right_flip).numpy()
    
    rot_input_with_ports_flat = torch.flatten(rot_input_with_ports).numpy()
    rot_top_bottom_flip_flat = torch.flatten(rot_top_bottom_flip).numpy()
    rot_left_right_flip_flat = torch.flatten(rot_left_right_flip).numpy()
    
    tmp_dir = os.path.join(project_dir, "tmp")
    tmp_result_dir = os.path.join(tmp_dir, experiment_index)
    
    s12 = pd.read_csv(os.path.join(tmp_result_dir, s12_tmp_data_file), sep=";", header=0)  
    s34 = pd.read_csv(os.path.join(tmp_result_dir, s34_tmp_data_file), sep=";", header=0)
    
    s12_data = s12[["re(S(1,1))", "re(S(1,2))", "re(S(2,2))", "im(S(1,1))", "im(S(1,2))", "im(S(2,2))"]]
    s34_data = s34[["re(S(3,3))", "re(S(3,4))", "re(S(4,4))", "im(S(3,3))", "im(S(3,4))", "im(S(4,4))"]]
    s21_data = s12[["re(S(2,2))", "re(S(1,2))", "re(S(1,1))", "im(S(2,2))", "im(S(1,2))", "im(S(1,1))"]]
    s43_data = s34[["re(S(4,4))", "re(S(3,4))", "re(S(3,3))", "im(S(4,4))", "im(S(3,4))", "im(S(3,3))"]]    
    
    # flatterning data into 1 line
    s12_data_flat = s12_data.to_numpy().flatten()
    s34_data_flat = s34_data.to_numpy().flatten()
    s21_data_flat = s21_data.to_numpy().flatten()
    s43_data_flat = s43_data.to_numpy().flatten()
    
    # concat s params and input matrix into 1 line
    s12_data_label = np.concatenate((s12_data_flat, input_with_ports_flat))
    s12_td_enhanced_data_label = np.concatenate((s12_data_flat, top_bottom_flip_flat))
    s12_lr_enhanced_data_label = np.concatenate((s21_data_flat, left_right_flip_flat))
    
    s34_data_label = np.concatenate((s34_data_flat, rot_input_with_ports_flat))
    s34_td_enhanced_data_label = np.concatenate((s34_data_flat, rot_top_bottom_flip_flat))
    s34_lr_enhanced_data_label = np.concatenate((s43_data_flat, rot_left_right_flip_flat))

    s12_df = pd.DataFrame([s12_data_label])
    s12_td_enhanced_df = pd.DataFrame([s12_td_enhanced_data_label])
    s12_lr_enhanced_df = pd.DataFrame([s12_lr_enhanced_data_label])
    s34_df = pd.DataFrame([s34_data_label])
    s34_td_enhanced_df = pd.DataFrame([s34_td_enhanced_data_label])
    s34_lr_enhanced_df = pd.DataFrame([s34_lr_enhanced_data_label])
    
    results_dir = os.path.join(project_dir, "results")
    dataset_dir = os.path.join(results_dir, experiment_index)
    os.makedirs(dataset_dir, exist_ok=True)
    output_file_name = f"{experiment_index}_data.csv"
    output_path = os.path.join(dataset_dir, output_file_name)
    
    # save labels
    s12_df.to_csv(output_path, mode='a', index=False, header=False)
    s12_td_enhanced_df.to_csv(output_path, mode='a', index=False, header=False)
    s12_lr_enhanced_df.to_csv(output_path, mode='a', index=False, header=False)
    s34_df.to_csv(output_path, mode='a', index=False, header=False)
    s34_td_enhanced_df.to_csv(output_path, mode='a', index=False, header=False)
    s34_lr_enhanced_df.to_csv(output_path, mode='a', index=False, header=False)
    
    
# x: width, y: lenth, z: thickness
class Input_Data:
    def __init__(self):
        self.input_with_ports = torch.empty(0, 0, dtype=torch.int64)
    
    def random_input(self, input_width, input_lenth):
        '''create random input and port tensor for simulation'''
        input_mat = torch.randint(0, 2, (input_width, input_lenth), dtype=torch.int64)

        ports = ["left", "top", "right", "bottom"]

        ports_dict = {key: None for key in ports}

        for i, port in enumerate(ports):
                
            if port == "top" or port == "bottom":
                
                tensor = torch.zeros(1, input_width, dtype=torch.int64)
                random_index = torch.randint(0, input_width, (1,)).item()
                tensor[0, random_index] = 1
                ports_dict[port] = tensor
                
            elif port == "left" or port == "right":
                
                tensor = torch.zeros(1, input_lenth, dtype=torch.int64)
                random_index = torch.randint(0, input_lenth, (1,)).item()
                tensor[0, random_index] = 1
                ports_dict[port] = tensor
            
        self.input_with_ports = attach_ports(input_mat, ports_dict)
        
        return input_mat, ports_dict
    
    def saved_input(self, input_width, input_lenth):
        '''create random matrix and port tensor, save them to disk'''
        input_mat = torch.randint(0, 2, (input_width, input_lenth), dtype=torch.int64)

        ports = ["left", "top", "right", "bottom"]

        ports_dict = {key: None for key in ports}

        for i, port in enumerate(ports):
                
            if port == "top" or port == "bottom":
                
                tensor = torch.zeros(1, input_width, dtype=torch.int64)
                random_index = torch.randint(0, input_width, (1,)).item()
                tensor[0, random_index] = 1
                ports_dict[port] = tensor
                
            elif port == "left" or port == "right":
                
                tensor = torch.zeros(1, input_lenth, dtype=torch.int64)
                random_index = torch.randint(0, input_lenth, (1,)).item()
                tensor[0, random_index] = 1
                ports_dict[port] = tensor
            
        self.input_with_ports = attach_ports(input_mat, ports_dict)
        torch.save({
            'input_mat': input_mat,
            'ports_dict': ports_dict
        }, 'input_data.pt')
        
    def load_input(self):
        '''load saved input matrix and port tensor'''
        data = torch.load('input_data.pt')
        input_mat_loaded = data['input_mat']
        ports_dict_loaded = data['ports_dict']

        return input_mat_loaded, ports_dict_loaded