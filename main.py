import pandas as pd
import matplotlib.pyplot as plt

print("🚀 Final Anomaly Detection for Switch Logs...\n")

# Load data
df1 = pd.read_csv("10.1.1.16_Switch_logs.csv")
df2 = pd.read_csv("10.1.3.17_-_Recent_switch_logs.csv")
df = pd.concat([df1, df2], ignore_index=True)

df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
df = df.dropna(subset=['timestamp'])

print(f"Total Logs: {len(df)}\n")

# Hour-wise log count
df['hour'] = df['timestamp'].dt.hour
hourly = df.groupby('hour').size().reset_index(name='log_count')

# === Better Logic for Small Dataset ===
# Top 20% busiest hours marked as potential anomaly
threshold = hourly['log_count'].quantile(0.8)   # Top 20%
anomalies = hourly[hourly['log_count'] >= threshold]

print("🔍 ANOMALY DETECTION RESULTS (Top Busy Hours):")
print(anomalies.sort_values('log_count', ascending=False))

# Save
anomalies.to_csv('anomaly_detection_results.csv', index=False)
print("\n✅ Anomaly results saved!")

# Plot
plt.figure(figsize=(14, 8))
plt.bar(hourly['hour'], hourly['log_count'], alpha=0.7, label='Normal')
plt.bar(anomalies['hour'], anomalies['log_count'], color='red', label='High Activity (Anomaly)')
plt.title('Hourly Log Activity - Anomalies Highlighted')
plt.xlabel('Hour of Day')
plt.ylabel('Number of Logs')
plt.legend()
plt.grid(axis='y')
plt.savefig('anomaly_detection_plot.png', dpi=300)
print("✅ Plot saved: anomaly_detection_plot.png")

print("\n🎉 4th Point Completed Successfully!")