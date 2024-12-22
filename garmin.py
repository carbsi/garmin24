import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
csv_file = "Activities (1).csv"  # Replace with your actual file path
data = pd.read_csv(csv_file)

# Extract and print only the names of the activities
data['Activity Name'] = data['Activity Type'].str.split(',').str[0]  # Extract the activity name before the first comma
print("Extracted Activity Names:")
print(data['Activity Name'].unique())

# Inspect the "Time" column format
print("Inspecting 'Time' column format:")
print(data.iloc[:, 6].head())  # Print the first few entries of the column at index 6

# Verify if 'Time' is in index 6 and extract it correctly
if data.columns[6] == 'Time':
    try:
        # Attempt to parse "Time" as durations (hh:mm:ss)
        data['Time'] = pd.to_timedelta(data['Time']).dt.total_seconds() / 60  # Convert to minutes
    except Exception as e:
        print(f"Failed to parse 'Time' as durations: {e}")
        try:
            # Attempt to coerce "Time" to numeric if not duration format
            data['Time'] = pd.to_numeric(data['Time'], errors='coerce')
        except Exception as e_numeric:
            raise ValueError(f"Unable to parse 'Time' column: {e_numeric}")
else:
    raise ValueError("'Time' column is not in the expected index 6. Please check the CSV structure.")

# Extract the data by "Activity Type"
activity_counts = data['Activity Name'].value_counts()

# 1. Plot a chart of all activities
plt.figure(figsize=(12, 6))
activity_counts.plot(kind='bar', color='skyblue')
plt.title('Activity Frequency')
plt.xlabel('Activity Name')
plt.ylabel('Number of Activities')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("activity_frequency_chart.png")  # Save the chart
plt.show()

# 2. Print the 3 most frequent activities with their counts
most_frequent_activities = activity_counts.head(3)
print("Top 3 most frequent activities:")
print(most_frequent_activities)

# 3. Calculate total hours spent playing "Padel"
padel_data = data[data['Activity Name'] == 'Padel']
padel_time_minutes = padel_data['Time'].sum()  # Assuming time is in minutes
padel_time_hours = padel_time_minutes / 60
print(f"Total hours spent playing Padel: {padel_time_hours:.2f} hours")

# 4. Calculate total minutes and number of activities for "Running"
running_data = data[data['Activity Name'] == 'Running']
running_time_minutes = running_data['Time'].sum()  # Assuming time is in minutes
running_activities = running_data.shape[0]
print(f"You spent {running_time_minutes} minutes running over {running_activities} activities.")

# 5. Calculate total minutes and number of activities for skiing activities
skiing_data = data[data['Activity Name'].isin(['Resort Skiing', 'Cross Country Skate Skiing'])]
skiing_time_minutes = skiing_data['Time'].sum()
skiing_activities = skiing_data.shape[0]
print(f"You spent {skiing_time_minutes} minutes skiing (Resort + Cross Country) over {skiing_activities} activities.")
