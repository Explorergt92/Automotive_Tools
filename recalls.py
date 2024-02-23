import os
import requests
import zipfile
from io import BytesIO

url = 'https://static.nhtsa.gov/odi/ffdd/rcl/FLAT_RCL.zip'

print("Downloading file...")
response = requests.get(url, timeout=30)
zip_content = BytesIO(response.content)

print("Unzipping file...")
with zipfile.ZipFile(zip_content, 'r') as zip_ref:
    zip_ref.extractall(".")

file_name = 'FLAT_RCL.txt'

specified_brands = [
    "ACURA", "ALFA ROMEO", "ASTON MARTIN", "AUDI", "BMW", "BENTLEY MOTORS",
    "BUGATTI", "BUICK", "CADILLAC", "CHEVROLET", "CHRYSLER", "DODGE", "FERRARI",
    "FIAT", "FISKER", "FORD", "GMC", "GENESIS", "HONDA", "HUMMER", "HYUNDAI",
    "INEOS", "INFINITI", "JAGUAR", "JEEP", "KARMA", "KIA", "LAMBORGHINI",
    "LAND ROVER", "LEXUS", "LINCOLN", "LOTUS", "LUCID MOTORS", "MASERATI",
    "MAYBACH", "MAZDA", "MCLAREN", "MERCEDES-AMG", "MERCEDES-BENZ", "MERCEDES-MAYBACH", "MERCURY",
    "MINI", "MITSUBISHI", "NISSAN", "OLDSMOBILE", "POLESTAR", "PONTIAC", "PORSCHE",
    "PLYMOUTH", "RAM", "RIVIAN", "ROLLS-ROYCE", "SAAB", "SATURN", "SCION", "SMART",
    "SUBARU", "SUZUKI", "TESLA", "TOYOTA", "VOLKSWAGEN", "VOLVO"
]

recall_counts = {brand: 0 for brand in specified_brands}

with open('FLAT_RCL.txt', 'r') as file:
    for line in file:
        parts = line.split('\t')
        automaker = parts[2].upper()

        if automaker in specified_brands:
            recall_counts[automaker] += 1

recall_counts = {brand: count for brand, count in recall_counts.items() if count > 0}

if recall_counts:
    least_recalls = min(recall_counts, key=recall_counts.get)
    print(f"The automaker with the least recalls is {least_recalls} with {recall_counts[least_recalls]} recalls.")
else:
    print("No recalls found for the specified brands.")

for automaker, count in sorted(recall_counts.items(), key=lambda item: item[1]):
    print(f"{automaker}: {count}")
