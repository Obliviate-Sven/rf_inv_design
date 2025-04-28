import pandas as pd
import matplotlib.pyplot as plt
import os

def draw_plot(project_dir, experiment_index, s12_tmp_data_file, s34_tmp_data_file, iteration):

    plot_dir = os.path.join(project_dir, "plot")
    os.makedirs(plot_dir, exist_ok=True)
    tmp_dir = os.path.join(project_dir, "tmp")
    experiment_dir = os.path.join(tmp_dir, experiment_index)
    s12_csv_path = os.path.join(experiment_dir, s12_tmp_data_file)
    s34_csv_path = os.path.join(experiment_dir, s34_tmp_data_file)

    s12_data = pd.read_csv(s12_csv_path, delimiter=';')
    s34_data = pd.read_csv(s34_csv_path, delimiter=';')

    freq = s12_data['Freq [GHz]']
    re_s11 = s12_data['re(S(1,1))']
    re_s12 = s12_data['re(S(1,2))']
    re_s22 = s12_data['re(S(2,2))']

    im_s11 = s12_data['im(S(1,1))']
    im_s12 = s12_data['im(S(1,2))']
    im_s22 = s12_data['im(S(2,2))']
    
    s12_fig_path = os.path.join(plot_dir, f'/S12_Parameters_vs_Frequency_{iteration}.png')
    s34_fig_path = os.path.join(plot_dir, f'/S34_Parameters_vs_Frequency_{iteration}.png')

    plt.figure(figsize=(12, 8))
    plt.plot(freq, re_s11, label='re(S(1,1))')
    plt.plot(freq, re_s12, label='re(S(1,2))')
    plt.plot(freq, re_s22, label='re(S(2,2))')
    plt.plot(freq, im_s11, label='im(S(1,1))')
    plt.plot(freq, im_s12, label='im(S(1,2))')
    plt.plot(freq, im_s22, label='im(S(2,2))')

    plt.title('S12 Parameters vs Frequency')
    plt.xlabel('Frequency [GHz]')
    plt.ylabel('')
    plt.legend()
    plt.grid(True)
    plt.savefig(s12_fig_path)
    plt.close()

    freq = s34_data['Freq [GHz]']
    re_s33 = s34_data['re(S(3,3))']
    re_s34 = s34_data['re(S(3,4))']
    re_s44 = s34_data['re(S(4,4))']
    im_s33 = s34_data['im(S(3,3))']
    im_s34 = s34_data['im(S(3,4))']
    im_s44 = s34_data['im(S(4,4))']

    plt.figure(figsize=(12, 8))
    plt.plot(freq, re_s33, label='re(S(3,3))')
    plt.plot(freq, re_s34, label='re(S(3,4))')
    plt.plot(freq, re_s44, label='re(S(4,4))')
    plt.plot(freq, im_s33, label='im(S(3,3))')
    plt.plot(freq, im_s34, label='im(S(3,4))')
    plt.plot(freq, im_s44, label='im(S(4,4))')

    plt.title('S34 Parameters vs Frequency')
    plt.xlabel('Frequency [GHz]')
    plt.ylabel('')
    plt.legend()
    plt.grid(True)
    plt.savefig(s34_fig_path)
    plt.close()
