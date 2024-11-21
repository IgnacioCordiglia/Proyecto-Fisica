import pandas as pd

# Load the data
df = pd.read_csv('output_data.csv')

# Calculate initial velocity and deceleration rate
initial_velocity = (df['x_center'][14] - df['x_center'][2]) / 12
deceleration_rate = (initial_velocity - (df['x_center'][62] - df['x_center'][14]) / 48) / 48

# Generate missing frames
missing_frames = range(16, 63)
missing_data = []
for i in missing_frames:
    x_center = df['x_center'][15] + initial_velocity * (i - 15) - 0.5 * deceleration_rate * (i - 15) ** 2
    y_center = df['y_center'][15]
    missing_data.append([i, x_center, y_center])

# Create a DataFrame for missing data
missing_df = pd.DataFrame(missing_data, columns=['frame_index', 'x_center', 'y_center'])

# Combine original and missing data
combined_df = pd.concat([df, missing_df], ignore_index=True)

# Estimate bounding box coordinates based on center coordinates
combined_df['x_min'] = combined_df['x_center'] - 30
combined_df['x_max'] = combined_df['x_center'] + 30
combined_df['y_min'] = combined_df['y_center'] - 15
combined_df['y_max'] = combined_df['y_center'] + 15

# Fill in other columns with appropriate values
combined_df['class_id'] = 1
combined_df['confidence'] = 0.8  # Adjust as needed
combined_df['tracker_id'] = ''
combined_df['class_name'] = 'golf ball'

# Sort by frame index
combined_df = combined_df.sort_values(by='frame_index')

# Save the modified data
combined_df.to_csv('golf_ball_data_filled.csv', index=False)