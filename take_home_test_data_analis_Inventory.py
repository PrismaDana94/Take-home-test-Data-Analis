import gdown
import pandas as pd

# ID file Google Drive
file_id = "1DBbnyF4AvHJQqj6JdfM3IOoH9lCwaoRj"
url = f"https://drive.google.com/uc?id={file_id}"
output = "inventory_clean.csv"

# download file
gdown.download(url, output, quiet=False)

# baca file CSV
df = pd.read_csv(output)
print(df.head())



