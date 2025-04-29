import ansys.aedt.core
import torch
import time
import os
import tempfile
import platform   
from data_util import attach_ports

# x: width, y: lenth, z: thickness

def em_simulation(project_dir, s12_tmp_data_file, s34_tmp_data_file, experiment_index, input_mat, ports_dict, dev_w, dev_l):
    '''call hfss simulation and save S params to csv files'''
    # check os
    system_name = platform.system().lower() 
    if system_name == "windows":
        os.environ["ANSYSEM_ROOT232"] = r"C:\Program Files\AnsysEM\v232"
        HFSS_VERSION = "2023.2"
        NUM_CORES = 1
    elif system_name == "linux":
        HFSS_VERSION = "2024.1"
        NUM_CORES = 1
    
    PROJECT_NAME = os.path.basename(os.path.normpath(f"{project_dir}_{experiment_index}_project"))
    DESIGN_NAME = os.path.basename(os.path.normpath(f"{project_dir}_{experiment_index}_design"))
    # SOLUTION_TYPE = "Modal"
    SOLUTION_TYPE = "Terminal"

    temp_folder = tempfile.TemporaryDirectory(suffix=".ansys")
    tmp_dir = os.path.join(project_dir, "tmp")
    os.makedirs(tmp_dir, exist_ok=True)
    result_dir = os.path.join(tmp_dir, experiment_index)
    os.makedirs(result_dir, exist_ok=True)
    
    # set ansys params
    NO_GUI = False
    PRINT_ON = False
    
    # launch ansys simulation
    start_time = time.time()
    ansys.aedt.core.Desktop(version=HFSS_VERSION, non_graphical=NO_GUI, new_desktop=True, close_on_exit=True, student_version=False)
    hfss = ansys.aedt.core.Hfss(project=PROJECT_NAME, design=DESIGN_NAME, solution_type=SOLUTION_TYPE, non_graphical=NO_GUI)

    if PRINT_ON == True:
        if hfss.design_name is None:
            print("Design creation failed.")
        else:
            print(f"Design '{hfss.design_name}' created successfully.")
        
    # set unit
    hfss.modeler.model_units = "um"

    # substrate shape and creation
    sub_w = 1000
    sub_l = 1000
    sub_h = 750
    
    hfss.modeler.create_box([-sub_w/2, -sub_l/2, -sub_h], 
                            [sub_w, sub_l, sub_h], 
                            name = "Substrate", 
                            material = "silicon")

    # dielectric layer shape
    ox_w = sub_w
    ox_l = sub_l
    
    # set dielectric and metal layers elvation and thickness
    ox0_elv = 0
    ox0_th  = 0.64
    m1_elv  = ox0_elv + ox0_th
    m1_th   = 0.42
    ox1_elv = ox0_elv + ox0_th
    ox1_th  = 0.54 + m1_th
    m2_elv  = ox1_elv + ox1_th
    m2_th   = 0.49
    ox2_elv = ox1_elv + ox1_th
    ox2_th  = 0.54 + m2_th
    m3_elv  = ox2_elv + ox2_th
    m3_th   = 0.49
    ox3_elv = ox2_elv + ox2_th
    ox3_th  = 0.54 + m3_th
    m4_elv  = ox3_elv + ox3_th
    m4_th   = 0.49
    ox4_elv = ox3_elv + ox3_th
    ox4_th  = 0.54 + m4_th
    m5_elv  = ox4_elv + ox4_th
    m5_th   = 0.49
    ox5_elv = ox4_elv + ox4_th
    ox5_th  = 0.85 + m5_th
    m6_elv  = ox5_elv + ox5_th
    m6_th   = 2.00
    ox6_elv = ox5_elv + ox5_th
    ox6_th  = 2.80 + m6_th
    
    # set dielectric layer material
    pdk_material = hfss.materials.add_material("pdk_material")
    pdk_material.permittivity = 4.1
    pdk_material.permeability = 1
    pdk_material.mass_density = 2220
    ox_mater = "pdk_material"
    
    # create dielectric layers
    ox_elv    = [ox0_elv, ox1_elv, ox2_elv, ox3_elv, ox4_elv, ox5_elv, ox6_elv]
    ox_th     = [ox0_th , ox1_th , ox2_th , ox3_th , ox4_th , ox5_th , ox6_th ]
    metal_elv = [0,       m1_elv , m2_elv , m3_elv , m4_elv , m5_elv , m6_elv ]
    metal_th  = [0,       m1_th  , m2_th  , m3_th  , m4_th  , m5_th  , m6_th  ]
  
    for i in range(len(ox_elv)):
        layer_name = f"Ox{i}"
        hfss.modeler.create_box([-ox_w/2, -ox_l/2, ox_elv[i]], 
                                [ox_w, ox_l, ox_th[i]], 
                                name = layer_name, 
                                material = ox_mater)

    # set pixel shape(pixel number : input matrix length/width adds 2 port pixels)
    pix_l = dev_l / input_mat.shape[0]
    pix_w = dev_w / input_mat.shape[1]
    # diagonal connections have a width of 6.6 µm due to pixel overlaps
    joint_width = 6.6
    joint_pix_width = (joint_width/(2**0.5))/2
    
    # GND (with hole) metal shape and creation
    gnd_w = dev_w+200 
    gnd_l = dev_l+200
    hole_w = dev_w-joint_pix_width-pix_w
    hole_l = dev_l-joint_pix_width-pix_l

    hfss.modeler.create_box([-gnd_w/2, -gnd_l/2, m5_elv], 
                            [gnd_w, gnd_l, m5_th], 
                            name = "GND", 
                            material = "copper")
    
    hfss.modeler.create_box([-hole_w/2, -hole_l/2, m5_elv], 
                            [hole_w, hole_l, m5_th], 
                            name = "hole")
    
    hfss.modeler.subtract("GND", "hole", False)

    if PRINT_ON == True:
        print(f"input matrix shape : ({input_mat.shape[0]}, {input_mat.shape[1]})")

    unite_obj_list = []

    # create device pixel
    for i in range(input_mat.shape[0]):
        for j in range(input_mat.shape[1]):
            if input_mat[i, j].item() == 1:
                
                pix_name = f"pix_{i}_{j}"
                pix_mater = "copper"
                
                pix_x = -dev_w/2+i*pix_w-joint_pix_width
                pix_y = -dev_l/2+j*pix_l-joint_pix_width

                pixel = hfss.modeler.create_box(origin = [pix_x, pix_y, m6_elv], 
                                                sizes = [pix_w+2*joint_pix_width, pix_l+2*joint_pix_width, m6_th], 
                                                name = pix_name, 
                                                material = pix_mater)
                
                unite_obj_list.append(pixel)

    # create port
    for key, tensor in ports_dict.items():
        
        if PRINT_ON == True:
            print(f"Port: {key}, Tensor: {tensor}")

        port_w = pix_w+2*joint_pix_width
        port_l = pix_l+2*joint_pix_width
        port_h = m6_elv-m5_elv-m5_th
        
        # fix port location, Move 10 um inward from the edge of the device 
        port_loc_fix = 10
        
        if key == "left":
            if PRINT_ON == True:
                print(f"current port is {key}")
            
            for i in range(tensor.shape[1]):
                if tensor[0,i].item() == 1:
                    
                    pix_name = f"{key}_port_pix"
                    pix_mater = "copper"
                    pix_x = -dev_w/2-joint_pix_width-pix_w
                    pix_y = -dev_l/2+i*pix_l-joint_pix_width

                    pixel = hfss.modeler.create_box(origin = [pix_x, pix_y, m6_elv], 
                                                    sizes = [port_w, port_l, m6_th], 
                                                    name = pix_name, 
                                                    material = pix_mater)
                    
                    unite_obj_list.append(pixel)

                    port_x = pix_x+port_loc_fix
                    port_y = pix_y
                
                    if SOLUTION_TYPE == "Modal":
                        hfss.modeler.create_rectangle(
                            orientation = ansys.aedt.core.constants.PLANE.YZ,
                            origin = [port_x, port_y, m6_elv],
                            sizes = [port_l, -port_h],
                            name = 'port1'
                        )
                        
                        hfss.lumped_port(assignment = 'port1',
                                        integration_line = [[port_x, port_y+port_l/2, m6_elv], [port_x, port_y+port_l/2, m6_elv-port_h]],
                                        terminals_rename = True)
                    elif SOLUTION_TYPE == "Terminal":
                        hfss.modeler.create_rectangle(
                            orientation = ansys.aedt.core.constants.PLANE.YZ,
                            origin = [port_x, port_y, m6_elv],
                            sizes = [port_l, -port_h],
                            name = 'port1'
                        )                        
                        
                        hfss.lumped_port(assignment = 'port1',
                                        reference = 'GND',
                                        integration_line = hfss.AxisDir.ZNeg,
                                        name = 'port1',
                                        terminals_rename = True)

        elif key == "right":
            if PRINT_ON == True:
                print(f"current port is {key}")
            
            for i in range(tensor.shape[1]):
                if tensor[0,i].item() == 1:

                    pix_name = f"{key}_port_pix"
                    pix_mater = "copper"
                    pix_x = -dev_w/2+input_mat.shape[0]*pix_w-joint_pix_width
                    pix_y = -dev_l/2+i*pix_l-joint_pix_width

                    pixel = hfss.modeler.create_box(origin = [pix_x, pix_y, m6_elv], 
                                                    sizes = [port_w, port_l, m6_th], 
                                                    name = pix_name, 
                                                    material = pix_mater)
                    
                    unite_obj_list.append(pixel)
                    
                    port_x = pix_x+pix_w+2*joint_pix_width-port_loc_fix
                    port_y = pix_y
                
                    if SOLUTION_TYPE == "Modal":                    
                        hfss.modeler.create_rectangle(
                            orientation = ansys.aedt.core.constants.PLANE.YZ,
                            origin = [port_x, port_y, m6_elv],
                            sizes = [port_l, -port_h],
                            name = 'port2'
                        )

                        hfss.lumped_port(assignment = 'port2',
                                        integration_line = [[port_x, port_y+port_l/2, m6_elv], [port_x, port_y+port_l/2, m6_elv-port_h]],
                                        terminals_rename = False)        
                    elif SOLUTION_TYPE == "Terminal": 
                        hfss.modeler.create_rectangle(
                            orientation = ansys.aedt.core.constants.PLANE.YZ,
                            origin = [port_x, port_y, m6_elv],
                            sizes = [port_l, -port_h],
                            name = 'port2'
                        )                        
                           
                        hfss.lumped_port(assignment = 'port2',
                                        reference = 'GND',
                                        integration_line = hfss.AxisDir.ZNeg,
                                        name = 'port2',
                                        terminals_rename = True)     

        elif key == "top":
            if PRINT_ON == True:
                print(f"current port is {key}")
            
            for i in range(tensor.shape[1]):
                if tensor[0,i].item() == 1:

                    pix_name = f"{key}_port_pix"
                    pix_mater = "copper"
                    pix_x = -dev_w/2+i*pix_w-joint_pix_width
                    pix_y = -dev_l/2+input_mat.shape[1]*pix_l-joint_pix_width

                    pixel = hfss.modeler.create_box(origin = [pix_x, pix_y, m6_elv], 
                                                    sizes = [port_w, port_l, m6_th], 
                                                    name = pix_name, 
                                                    material = pix_mater)
                    
                    unite_obj_list.append(pixel)              
                    
                    port_x = pix_x
                    port_y = pix_y+pix_l+2*joint_pix_width-port_loc_fix
                
                    if SOLUTION_TYPE == "Modal":
                        hfss.modeler.create_rectangle(
                            orientation = ansys.aedt.core.constants.PLANE.ZX,
                            origin = [port_x, port_y, m6_elv],
                            sizes = [-port_h, port_w],
                            name = 'port3'
                        )

                        hfss.lumped_port(assignment = 'port3',
                                        integration_line = [[port_x+port_w/2, port_y, m6_elv], [port_x+port_w/2, port_y, m6_elv-port_h]],
                                        terminals_rename = False)
                    elif SOLUTION_TYPE == "Terminal":   
                        hfss.modeler.create_rectangle(
                            orientation = ansys.aedt.core.constants.PLANE.ZX,
                            origin = [port_x, port_y, m6_elv],
                            sizes = [-port_h, port_w],
                            name = 'port3'
                        )                        
                         
                        hfss.lumped_port(assignment = 'port3',
                                        reference = 'GND',
                                        integration_line = hfss.AxisDir.ZNeg,
                                        name = 'port3',
                                        terminals_rename = True)

        elif key == "bottom":
            if PRINT_ON == True:
                print(f"current port is {key}")
            
            for i in range(tensor.shape[1]):
                if tensor[0,i].item() == 1:

                    pix_name = f"{key}_port_pix"
                    pix_mater = "copper"
                    pix_x = -dev_w/2+i*pix_w-joint_pix_width
                    pix_y = -dev_l/2-joint_pix_width-pix_l

                    pixel = hfss.modeler.create_box(origin = [pix_x, pix_y, m6_elv], 
                                                    sizes = [port_w, port_l, m6_th], 
                                                    name = pix_name, 
                                                    material = pix_mater)
                    
                    unite_obj_list.append(pixel)
                    
                    port_x = pix_x
                    port_y = pix_y+port_loc_fix
                
                    if SOLUTION_TYPE == "Modal":
                        hfss.modeler.create_rectangle(
                            orientation = ansys.aedt.core.constants.PLANE.ZX,
                            origin = [port_x, port_y, m6_elv],
                            sizes = [-port_h, port_w],
                            name = 'port4'
                        )

                        hfss.lumped_port(assignment = 'port4',
                                        integration_line = [[port_x+port_w/2, port_y, m6_elv], [port_x+port_w/2, port_y, m6_elv-port_h]],
                                        terminals_rename = False)
                    elif SOLUTION_TYPE == "Terminal":  
                        hfss.modeler.create_rectangle(
                            orientation = ansys.aedt.core.constants.PLANE.ZX,
                            origin = [port_x, port_y, m6_elv],
                            sizes = [-port_h, port_w],
                            name = 'port4'
                        )                        
                           
                        hfss.lumped_port(assignment = 'port4',
                                        reference = 'GND',
                                        integration_line = hfss.AxisDir.ZNeg,
                                        name = 'port4',
                                        terminals_rename = True)
                    
    # for i in range(input_mat.shape[0] - 1):  
    #     for j in range(input_mat.shape[1] - 1): 

    #         if (input_mat[i, j] == 1 and input_mat[i+1, j] == 0 and input_mat[i, j+1] == 0 and input_mat[i+1, j+1] == 1) or \
    #         (input_mat[i, j] == 0 and input_mat[i+1, j] == 1 and input_mat[i, j+1] == 1 and input_mat[i+1, j+1] == 0):
                

    #             joint_name = f"joint_{i}{j}_{i+1}{j}_{i}{j+1}_{i+1}{j+1}"
    #             joint_mater = "copper"
    #             joint_x = -dev_w/2+(i+1)*pix_w-joint_pix_width/2
    #             joint_y = -dev_l/2+(j+1)*pix_l-joint_pix_width/2
                
    #             joint_pixel = hfss.modeler.create_box(origin = [joint_x, joint_y, m6_elv], 
    #                                             sizes = [joint_pix_width, joint_pix_width, m6_th], 
    #                                             name = joint_name, 
    #                                             material = joint_mater)
                
    #             joint_coord = hfss.modeler.create_object_coordinate_system(joint_pixel, 
    #                                                          origin = [-dev_w/2+(i+1)*pix_w, -dev_l/2+(j+1)*pix_l, m6_elv],
    #                                                          x_axis = ansys.aedt.core.constants.AXIS.X,
    #                                                          y_axis = ansys.aedt.core.constants.AXIS.Y,
    #                                                          name = "joint_coord")
                
    #             joint_pixel.rotate(axis = joint_coord.)
                
    #             unite_obj_list.append(joint_pixel)

    hfss.modeler.unite(unite_obj_list)

    hfss.modeler.create_box([-sub_w/2, -sub_l/2, -sub_h], 
                       [sub_w, sub_l, 2*sub_h],
                       name="airbox",
                       material="air",
    )

    hfss.assign_radiation_boundary_to_objects("airbox")
    hfss.change_material_override()

    setup = hfss.create_setup(name="setup")

    setup.props["Frequency"] = "100GHz"
    setup.props["MaxDeltaS"] = 0.01
    setup.props["MaximumPasses"] = 60
    setup.props["PercentRefinement"] = 20
    setup.props["MinimumConvergedPasses"] = 2
    setup.props["MinimumPasses"] = 2
    setup.update()

    hfss.create_linear_count_sweep(
        setup="setup",
        units="GHz",
        start_frequency=30,
        stop_frequency=100,
        num_of_freq_points=71,
        sweep_type="Interpolating",
    )

    hfss.analyze(cores=NUM_CORES)
    
    s12_data = hfss.post.get_solution_data(
        expressions=["re(S(1,1))", "re(S(1,2))", "re(S(2,2))", "im(S(1,1))", "im(S(1,2))", "im(S(2,2))"]   
    )

    s34_data = hfss.post.get_solution_data(
        expressions=["re(S(3,3))", "re(S(3,4))", "re(S(4,4))", "im(S(3,3))", "im(S(3,4))", "im(S(4,4))"]   
    )

    s12_data.export_data_to_csv(os.path.join(result_dir, s12_tmp_data_file))
    s34_data.export_data_to_csv(os.path.join(result_dir, s34_tmp_data_file))
    
    hfss.close_project()
    hfss.release_desktop()
    temp_folder.cleanup()

    end_time = time.time()

    elapsed_time = end_time - start_time

    if PRINT_ON == True:
        print(f"simulation time : {elapsed_time:.6f}s")