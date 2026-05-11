import pandas as pd
import matplotlib.pyplot as plt

print("🚀 Telecom Switch Logs Analysis Started...\n")

# Load files
df1 = pd.read_csv("10.1.1.16_Switch_logs.csv")
df2 = pd.read_csv("10.1.3.17_-_Recent_switch_logs.csv")

df = pd.concat([df1, df2], ignore_index=True)

print(f"✅ Total Logs Loaded: {len(df)}")

# Clean timestamp
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
df = df.dropna(subset=['timestamp'])

print(f"✅ Valid timestamps: {len(df)}")

# === 1. Daily Log Volume Graph ===
df['date'] = df['timestamp'].dt.date
daily_logs = df.groupby('date').size()

plt.figure(figsize=(12, 6))
plt.bar(daily_logs.index, daily_logs.values, color='skyblue')
plt.title('Daily Log Volume - Switch Logs')
plt.xlabel('Date')
plt.ylabel('Number of Logs')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.savefig('daily_log_volume.png', dpi=300)
print("✅ Graph saved: daily_log_volume.png")

# Save cleaned data for Grafana
df.to_csv('cleaned_switch_logs.csv', index=False)
print("✅ Cleaned data saved for Grafana")

# === 4. Anomaly Detection ===
df['hour'] = df['timestamp'].dt.hour
hourly = df.groupby('hour').size()

mean_logs = hourly.mean()
std_logs = hourly.std()
anomalies = hourly[hourly > mean_logs + 2 * std_logs]

print(f"\n🔍 Anomaly Detection:")
print(f"High Activity Hours: {list(anomalies.index)}")
print(f"Total Anomalous Hours: {len(anomalies)}")

anomalies.to_csv('anomaly_hours.csv')
print("✅ Anomaly results saved")

print("\n🎉 ALL 4 POINTS COMPLETED SUCCESSFULLY!")