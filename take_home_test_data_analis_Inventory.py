import pandas as pd

url = "https://drive.google.com/uc?id=1DBbnyF4AvHJQqj6JdfM3IOoH9lCwaoRj"
df = pd.read_csv(url)

print(df.head())


