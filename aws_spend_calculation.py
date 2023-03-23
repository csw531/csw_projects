import csv
import customtkinter as ctk
import tkinter as tk

def read_skus_from_csv(file_path):
    skus = []

    with open(file_path, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sku = {
                'name': row['name'],
                'od': float(row['od']),
                'savingspct': float(row['savingspct']),
                'instances': float(row['instances'])
            }
            skus.append(sku)

    return skus

def calculate_spend(skus, csp_commit):
    skus.sort(key=lambda x: x['savingspct'], reverse=True)

    remaining_csp_commit = csp_commit
    total_spend = 0
    discounted_instances = {sku['name']: 0 for sku in skus}
    od_instances = {sku['name']: 0 for sku in skus}
    od_cost_per_sku = {sku['name']: 0 for sku in skus}
    discounted_cost_per_sku = {sku['name']: 0 for sku in skus}
    total_od_cost = 0
    total_discounted_cost = 0

    for sku in skus:
        if sku['instances'] > 0:
            discounted_spend = sku['instances'] * (sku['od'] * (1 - sku['savingspct']))

            if remaining_csp_commit >= discounted_spend:
                remaining_csp_commit -= discounted_spend
                discounted_instances[sku['name']] = sku['instances']
            else:
                covered_instances = remaining_csp_commit / (sku['od'] * (1 - sku['savingspct']))
                remaining_csp_commit = 0
                remaining_instances = sku['instances'] - covered_instances

                discounted_instances[sku['name']] = covered_instances
                od_instances[sku['name']] = remaining_instances

                remaining_spend = remaining_instances * sku['od']
                total_spend += remaining_spend

    # Add remaining instances that were not covered at the discounted rate to the od_instances
    for i, sku in enumerate(skus):
        if discounted_instances[sku['name']] < sku['instances']:
            od_instances[sku['name']] = sku['instances'] - discounted_instances[sku['name']]

    for sku in skus:
        od_cost_per_sku[sku['name']] = od_instances[sku['name']] * sku['od']
        discounted_cost_per_sku[sku['name']] = discounted_instances[sku['name']] * (sku['od'] * (1 - sku['savingspct']))
        total_od_cost += od_cost_per_sku[sku['name']]
        total_discounted_cost += discounted_cost_per_sku[sku['name']]

    total_combined_cost = total_od_cost + total_discounted_cost
    total_od_cost_no_csp = sum([sku['instances'] * sku['od'] for sku in skus])
    blended_savings_rate = (1- total_combined_cost / total_od_cost_no_csp)

    return total_spend, discounted_instances, od_instances, od_cost_per_sku, discounted_cost_per_sku, total_od_cost, total_discounted_cost, total_combined_cost, total_od_cost_no_csp, blended_savings_rate


# Read SKUs from a CSV file
file_path = 'aws.csv'
skus = read_skus_from_csv(file_path)

# Define the csp_commit
csp_commit = 19.6

# Call the calculate_spend function
total_spend, discounted_instances, od_instances, od_cost_per_sku, discounted_cost_per_sku, total_od_cost, total_discounted_cost, total_combined_cost, total_od_cost_no_csp, blended_savings_rate = calculate_spend(skus, csp_commit)

# Print the results
"""print(f'Total spend: ${total_spend:.2f}/hr')
print(f'Discounted instances: {discounted_instances}')
print(f'OD instances: {od_instances}')
print(f'Discounted cost per SKU: {discounted_cost_per_sku}')
print(f'OD cost per SKU: {od_cost_per_sku}')
print(f'Total OD cost: ${total_od_cost:.2f}')
print(f'Total discounted cost: ${total_discounted_cost:.2f}')
print(f'Total combined cost: ${total_combined_cost:.2f}')
print(f'Total OD cost without CSP: ${total_od_cost_no_csp:.2f}')
print(f'Blended savings rate: {blended_savings_rate:.2%}')"""

# Create the main window
root = tk.Tk()
root.title("AWS Savings Calculator")

# Create title label
title_label = tk.Label(root, text="AWS Savings Calculation", font=("Arial", 16))
title_label.grid(row=0, column=0, columnspan=4, pady=10)


# Create SKU selection dropdowns
sku_variable1 = tk.StringVar(root)
sku_variable2 = tk.StringVar(root)
dropdown1 = tk.Combobox(root, textvariable=sku_variable1, values=[sku['name'] for sku in skus], state="readonly")
dropdown2 = tk.Combobox(root, textvariable=sku_variable2, values=[sku['name'] for sku in skus], state="readonly")
dropdown1.grid(row=1, column=0, padx=10, pady=10)
dropdown2.grid(row=2, column=0, padx=10, pady=10)

# Display od rate and savingspct
od_label1 = ctk.CTkLabel(root, text="OD: ")
od_label2 = ctk.CTkLabel(root, text="OD: ")
savingspct_label1 = ctk.CTkLabel(root, text="SavingsPct: ")
savingspct_label2 = ctk.CTkLabel(root, text="SavingsPct: ")

od_label1.grid(row=1, column=1, padx=5)
od_label2.grid(row=2, column=1, padx=5)
savingspct_label1.grid(row=1, column=2, padx=5)
savingspct_label2.grid(row=2, column=2, padx=5)

# Create instance inputs
instance_entry1 = ctk.CTkEntry(root)
instance_entry2 = ctk.CTkEntry(root)
instance_entry1.grid(row=1, column=3, padx=10, pady=10)
instance_entry2.grid(row=2, column=3, padx=10, pady=10)

# Create CSP_Commit input
csp_commit_label = ctk.CTkLabel(root, text="CSP_Commit:")
csp_commit_entry = ctk.CTkEntry(root)
csp_commit_label.grid(row=3, column=0, padx=5, pady=10)
csp_commit_entry.grid(row=3, column=1, padx=10, pady=10)


root.mainloop()


