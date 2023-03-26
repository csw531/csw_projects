import csv
import requests
from bs4 import BeautifulSoup

# Read the CSV file and store the references in a list
input_file = "references.csv"
references = []

with open(input_file, mode="r", newline="", encoding="utf-8") as file:
    reader = csv.reader(file)
    for row in reader:
        references.append(row)

# Process each reference, fetch the first URL, and store it in the reference
for i, reference in enumerate(references):
    print(f"Processing reference {i + 1}/{len(references)}")
    try:
        # Fetch the reference content
        response = requests.get(reference[0])
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the first URL in the content
        first_url = soup.find("a")["href"]
        # Store the first URL in the reference
        reference.append(first_url)
    except Exception as e:
        print(f"Error processing reference {i + 1}: {e}")
        reference.append("")

# Write the updated references to the output CSV file
output_file = "references_with_first_url.csv"
with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    for reference in references:
        writer.writerow(reference)

print("Web crawling completed. Check the output file for results.")