import pandas as pd
from datetime import datetime
from sklearn.metrics import mean_absolute_error

data = pd.read_csv("sphist.csv")

data["Date"] = pd.to_datetime(data["Date"])
#data["Date"] > datetime(year=2015, month=4, day=1)

data = data.sort_values(by='Date', ascending=True)

# Add in Year, Month and Day columns. Saturday and Sunday are marked as 5 and 6 respectively.

data["Year"] = data["Date"].apply(lambda x: x.year)
data["Month"] = data["Date"].apply(lambda x: x.month)

# Get weekday by integer
data["Day"] = data["Date"].apply(lambda x: x.weekday())

# Get dummies of weekday to determine trading days
data_week = pd.get_dummies(data["Day"], prefix="trading_day")

data = pd.concat([data, data_week], axis=1)

# Calculate the 5 day and 365 day rolling average and standard deviation of S&P500 prices. Note we have to shift the dataframe as the rolling function includes the current day's value, and we want it to be the previous five day's value averaged, not including the current day

data["5 Day Open Avg"] = data["Open"].rolling(center=False, window=5).mean().shift(1)
data["5 Day Open StDev"] = data["Open"].rolling(center=False, window=5).mean().shift(1)
data["365 Day Open Avg"] = data["Open"].rolling(center=False, window=365).mean().shift(1)
data["365 Day Open StDev"] = data["Open"].rolling(center=False, window=365).std().shift(1)

data["5 Day Close Avg"] = data["Close"].rolling(center=False, window=5).mean().shift(1)
data["5 Day Close StDev"] = data["Close"].rolling(center=False, window=5).mean().shift(1)
data["365 Day Close Avg"] = data["Close"].rolling(center=False, window=365).mean().shift(1)
data["365 Day Close StDev"] = data["Close"].rolling(center=False, window=365).std().shift(1)

data["5 Day High Avg"] = data["High"].rolling(center=False, window=5).mean().shift(1)
data["5 Day High StDev"] = data["High"].rolling(center=False, window=5).mean().shift(1)
data["365 Day High Avg"] = data["High"].rolling(center=False, window=365).mean().shift(1)
data["365 Day High StDev"] = data["High"].rolling(center=False, window=365).std().shift(1)

data["5 Day Low Avg"] = data["Low"].rolling(center=False, window=5).mean().shift(1)
data["5 Day Low StDev"] = data["Low"].rolling(center=False, window=5).mean().shift(1)
data["365 Day Low Avg"] = data["Low"].rolling(center=False, window=365).mean().shift(1)
data["365 Day Low StDev"] = data["Low"].rolling(center=False, window=365).std().shift(1)

data["5 Day Volume Avg"] = data["Volume"].rolling(center=False, window=5).mean().shift(1)
data["5 Day Volume StDev"] = data["Volume"].rolling(center=False, window=5).mean().shift(1)
data["365 Day Volume Avg"] = data["Volume"].rolling(center=False, window=365).mean().shift(1)
data["365 Day Volume StDev"] = data["Volume"].rolling(center=False, window=365).std().shift(1)

# Calculate 5 day and 365 day ratios
data["5_day_365_day_avg_volume_ratio"] = data["5 Day Volume Avg"] / data["365 Day Volume Avg"]
data["5_day_365_day_std_volume_ratio"] = data["5 Day Volume StDev"] / data["365 Day Volume StDev"] 

# Remove any rows before 1951-01-03 since we need to have a year's worth # of historical data for indicators

data = data[data["Date"] > datetime(year=1951, month=1, day=2)]

# Drop any NaN rows
data = data.dropna(axis=0)

# Create Test & Train data frames
train = data[data["Date"] < datetime(year=2013, month=1, day=1)]
test = data[data["Date"] > datetime(year=2013, month=1, day=1)]

# Initiate the LinearRegression model, determine features and calculate # mean_absolute_error of the closing price based on our features.

from sklearn.linear_model import LinearRegression

lr = LinearRegression()

features = ["5 Day Open Avg", "5 Day Close Avg", "5 Day High Avg", "5 Day Low Avg", "5 Day Volume Avg", "5_day_365_day_avg_volume_ratio", "5_day_365_day_std_volume_ratio", "365 Day Volume Avg", "365 Day Volume StDev"]
target = ["Close"]

lr.fit(train[features], train[target])

predictions = lr.predict(test[features])

mae = mean_absolute_error(predictions, test[target])

print(mae)
