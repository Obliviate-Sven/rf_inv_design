# Inverse-design

conda env is : inv
"conda activate inv" before run.sh

iteration number defined in data_generation.py line 10

check the experiment index before running in data_generation.py line 11

run command:

nohup ./run.sh < /dev/null > run.log 2>&1 &

# original version
each data point has 963 numbers in 1 line in dataset.csv
639 labels(S parameter), 324 input(boolean matrix)

# 4.5 update simulation.py
remove dB from S params
now each data point has 750 numbers in 1 line in dataset.csv
426 labels(S parameter), 324 input(boolean matrix)

adjust simulation modeling:
port location
GND

# 4.15 update simulation.py data_generation.py data_util.py plot.py run.sh simulation.py