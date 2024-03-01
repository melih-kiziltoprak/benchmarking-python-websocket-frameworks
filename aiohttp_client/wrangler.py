import os
import pandas as pd
import matplotlib.pyplot as plt

# Function to plot average values for duplicate x values
def plot_average(ax, x_values, y_values, label):
    averaged_data = pd.DataFrame({'x': x_values, 'y': y_values}).groupby('x').mean()
    ax.plot(averaged_data.index, averaged_data['y'], label=label)

# List of CSV file paths
file_paths = ["benchmark.csv", "io_benchmark.csv", "signal_benchmark.csv"]

# Iterate through each CSV file
for file_path in file_paths:
    # Load the CSV file into a Pandas DataFrame
    df = pd.read_csv(file_path)

    # Drop rows with duplicate column names (assuming they are repeated headers)
    df = df.loc[df['Connection_Count'] != 'Connection_Count']

    # Drop the 'MAX_CONN' column
    df = df.drop(columns=['MAX_CONN'])

    # Convert columns to appropriate data types
    df['Connection_Count'] = df['Connection_Count'].astype(int)
    df['Seconds'] = df['Seconds'].astype(float)
    df['MSG_CNT'] = df['MSG_CNT'].astype(int)

    # Derive the throughput column using the specified formula
    df['THROUGHPUT'] = (df['MSG_CNT'] * df['Connection_Count']) / df['Seconds']

    # Create a subdirectory for saving images
    output_directory = f"output_images_{os.path.splitext(os.path.basename(file_path))[0]}"
    os.makedirs(output_directory, exist_ok=True)

    # Create separate plots for each unique value of MSG_CNT
    for msg_cnt_value, msg_cnt_data in df.groupby('MSG_CNT'):
        # Plotting Connection_Count vs Seconds for each server with average for duplicate x values
        fig, ax = plt.subplots()
        for server, data in msg_cnt_data.groupby('SERVER'):
            plot_average(ax, data['Connection_Count'], data['Seconds'], label=f'Server {server}')

        ax.set_xlabel('Connection_Count')
        ax.set_ylabel('Seconds')
        ax.legend()
        plt.title(f'Connection_Count vs Seconds for MSG_CNT={msg_cnt_value}')

        # Save the image with an appropriate name in the subdirectory
        image_path = os.path.join(output_directory, f'Connection_Count_vs_Seconds_MSG_CNT_{msg_cnt_value}.png')
        plt.savefig(image_path)
        plt.close()

        # Plotting Connection_Count vs THROUGHPUT for each server with average for duplicate x values
        fig, ax = plt.subplots()
        for server, data in msg_cnt_data.groupby('SERVER'):
            plot_average(ax, data['Connection_Count'], data['THROUGHPUT'], label=f'Server {server}')

        ax.set_xlabel('Connection_Count')
        ax.set_ylabel('THROUGHPUT')
        ax.legend()
        plt.title(f'Connection_Count vs THROUGHPUT for MSG_CNT={msg_cnt_value}')

        # Save the image with an appropriate name in the subdirectory
        image_path = os.path.join(output_directory, f'Connection_Count_vs_THROUGHPUT_MSG_CNT_{msg_cnt_value}.png')
        plt.savefig(image_path)
        plt.close()
