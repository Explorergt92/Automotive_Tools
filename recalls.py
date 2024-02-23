
import zipfile
from io import BytesIO
import requests
import matplotlib.pyplot as plt

URL = 'https://static.nhtsa.gov/odi/ffdd/rcl/FLAT_RCL.zip'

print("Downloading file...")
response = requests.get(URL, timeout=30)
zip_content = BytesIO(response.content)

print("Unzipping file...")
with zipfile.ZipFile(zip_content, 'r') as zip_ref:
    zip_ref.extractall(".")

specified_brands = [
    "ACURA", "ALFA ROMEO", "ASTON MARTIN", "AUDI", "BMW", "BENTLEY MOTORS",
    "BUGATTI", "BUICK", "CADILLAC", "CHEVROLET", "CHRYSLER", "DODGE",
    "FERRARI", "FIAT", "FISKER", "FORD", "GMC", "GENESIS", "HONDA",
    "HUMMER", "HYUNDAI", "INEOS", "INFINITI", "JAGUAR", "JEEP",
    "KARMA", "KIA", "LAMBORGHINI", "LAND ROVER", "LEXUS", "LINCOLN",
    "LOTUS", "LUCID MOTORS", "MASERATI", "MAZDA", "MCLAREN",
    "MERCEDES-BENZ", "MERCEDES-MAYBACH", "MERCURY", "MINI",
    "MITSUBISHI", "NISSAN", "OLDSMOBILE", "POLESTAR", "PONTIAC",
    "PORSCHE", "PLYMOUTH", "RAM", "RIVIAN", "ROLLS-ROYCE", "SAAB",
    "SATURN", "SCION", "SMART", "SUBARU", "SUZUKI", "TESLA", "TOYOTA",
    "VOLKSWAGEN", "VOLVO"
]

recall_counts = {brand: 0 for brand in specified_brands}

with open('FLAT_RCL.txt', 'r', encoding='utf-8') as file:
    for line in file:
        parts = line.split('\t')
        automaker = parts[2].upper()

        if automaker in specified_brands:
            recall_counts[automaker] += 1

recall_counts = {brand: count for brand, count in recall_counts.items() if count > 0}

RESULTS_FILENAME = 'recall_counts.txt'
with open(RESULTS_FILENAME, 'w', encoding='utf-8') as results_file:
    for automaker, count in sorted(recall_counts.items(), key=lambda item: item[1]):
        results_file.write(f"{automaker}: {count}\n")
    print(f"Results saved to {RESULTS_FILENAME}")

sorted_recall_counts = dict(sorted(recall_counts.items(), key=lambda item: item[1]))
automakers = list(sorted_recall_counts.keys())
recall_counts_values = list(sorted_recall_counts.values())

plt.figure(figsize=(10, 8))
plt.barh(automakers, recall_counts_values, color='skyblue')
plt.xlabel('Number of Recalls')
plt.ylabel('Automaker')
plt.title('Recall Counts by Automaker')
plt.tight_layout()

plt.savefig('recalls_bar_graph.png')
print("Bar graph saved as 'recalls_bar_graph.png'")

plt.show()
