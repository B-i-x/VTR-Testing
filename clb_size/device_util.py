import os
import re
import matplotlib.pyplot as plt

# Set the path to the directory containing the folders
path = r'clb_size_data/run006'
# Prepare lists to collect data
data_x = []
data_y = []
# Iterate through each folder in the directory
ble_count = 4
for folder in os.listdir(path):
    folder_path = os.path.join(path, folder)
    if os.path.isdir(folder_path):
        # Locate the vpr.out file
        vpr_file_path = os.path.join(folder_path, 'diffeq1.v', 'common')
        vpr_file_path = os.path.join(vpr_file_path, 'vpr.out')
        if os.path.exists(vpr_file_path):
            with open(vpr_file_path, 'r') as file:
                contents = file.read()
                # Use regex to extract the required data
                match = re.search(r"Device Utilization:\s*([\d.]+)", contents)
                print(match)
                if match:
                    data_y.append(float(match.group(1)))
                    data_x.append(ble_count)
        # Increment BLE count for each folder processed
        ble_count += 1

# Plotting the data
plt.scatter(data_x, data_y)

print(data_y)
plt.xlabel('BLE SIZE')
plt.ylabel('Device Utilization (%)')
plt.title('Device Utilization vs. BLE Sizes')
plt.show()