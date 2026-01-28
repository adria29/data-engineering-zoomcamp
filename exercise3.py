import pandas as pd


df = pd.read_parquet('green_tripdata_2025-11.parquet')
df_2 = pd.read_csv('taxi_zone_lookup.csv')

#print(df.head())
#print(df_2.head())

print(df.columns)

selected_trips = df[(df["lpep_pickup_datetime"].dt.month == 11) & (df["trip_distance"]<= 1) ]
print(selected_trips.head())
print(len(selected_trips))

df_under_100_miles = df[df["trip_distance"] < 100]
longest_trip = df_under_100_miles.loc[df_under_100_miles["trip_distance"].idxmax()]
#print(longest_trip)

trips_on_nov_18 = df[df["lpep_pickup_datetime"].dt.date == pd.to_datetime("2025-11-18").date()]
total_revenue_nov_18 = trips_on_nov_18["total_amount"].groupby("PULocationID").sum()
print(total_revenue_nov_18)
