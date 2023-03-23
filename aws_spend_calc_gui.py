import csv
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

def update_sku_instances(sku_name, instances):
    for sku in skus:
        if sku['name'] == sku_name:
            sku['instances'] = int(instances)

def calculate_and_display():
    selected_sku1 = sku1_dropdown.get()
    selected_sku2 = sku2_dropdown.get()
    entered_instances1 = float(sku1_entry.get())
    entered_instances2 = float(sku2_entry.get())
    entered_csp_commit = float(csp_commit_entry.get())

    update_sku_instances(selected_sku1, entered_instances1)
    update_sku_instances(selected_sku2, entered_instances2)

    results = calculate_spend(skus, entered_csp_commit)


    # Display results in the result_label
    result_label.config(text='Total on-demand cost: ${:.2f}\n'.format(results[5]) +
                            'Total discounted cost: ${:.2f}\n'.format(results[6]) +
                            'Blended savings rate: {:.2%}\n\n'.format(results[9]) +
                            '{}\n'.format(selected_sku1) +
                            'On-demand instances: {:.2f}'.format(results[2][selected_sku1]) +
                            ', Discounted instances: {:.2f}\n'.format(results[1][selected_sku1]) +
                            '{}\n'.format(selected_sku2) +
                            'On-demand instances: {:.2f}'.format(results[2][selected_sku2]) +
                            ', Discounted instances: {:.2f}'.format(results[1][selected_sku2]))    

def get_skus(file_path):
    skus = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            skus.append({
                'name': row['name'],
                'od': float(row['od']),
                'savingspct': float(row['savingspct']),
                'instances': float(row['instances'])
            })
    return skus

csv_file_path = 'aws.csv'
skus = get_skus(csv_file_path)

def load_csv_data():
    file_path = csv_input.get()
    global pricing_data, skus
    pricing_data, file_name = read_pricing_data(file_path)
    skus = get_skus(file_path)

    data.configure(text=f"Data Source: {file_name}")

    for option_menu, var in zip(option_menus, [sku1_label, sku2_label]):  # Add more variables if needed.
        option_menu["menu"].delete(0, "end")
        for skus in skus:
            option_menu["menu"].add_command(label=skus, command=tk._setit(var, skus))

""""        
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
    return skus"""


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

# Create the main window
root = tk.Tk()
root.title("AWS Savings Calculation")

# Create and configure the main frame
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Add title label
title_label = ttk.Label(main_frame, text="AWS Savings Calculation", font=("Arial", 16))
title_label.grid(row=0, column=0, columnspan=3, pady=10)

# Add SKU dropdowns and instance entries
sku_names = [sku['name'] for sku in skus]
sku1_dropdown = ttk.Combobox(main_frame, values=sku_names)
sku1_dropdown.set(sku_names[0])
sku1_dropdown.grid(row=1, column=0, padx=(5, 5), pady=(5, 5))
sku1_entry = ctk.CTkEntry(main_frame, width=75)
sku1_entry.grid(row=1, column=1, padx=(5, 5), pady=(5, 5))

sku2_dropdown = ttk.Combobox(main_frame, values=sku_names)
sku2_dropdown.set(sku_names[1])
sku2_dropdown.grid(row=2, column=0, padx=(5, 5), pady=(5, 5))
sku2_entry = ctk.CTkEntry(main_frame, width=75)
sku2_entry.grid(row=2, column=1, padx=(5, 5), pady=(5, 5))

# Add CSP Commit label and entry
csp_commit_label = ttk.Label(main_frame, text="CSP Commitment")
csp_commit_label.grid(row=3, column=0, pady=5)
csp_commit_entry = ctk.CTkEntry(main_frame, width=75)
csp_commit_entry.grid(row=3, column=1)

# Add the calculate button
calculate_button = ctk.CTkButton(main_frame, text="Calculate", command=calculate_and_display)
calculate_button.grid(row=4, column=0, columnspan=2, pady=10)

# Add the result label
result_label = ttk.Label(main_frame, text="", justify=tk.LEFT)
result_label.grid(row=5, column=0, columnspan=2, pady=5)

# Add the SKU result label
sku_result_label = ttk.Label(main_frame, text="", justify=tk.LEFT)
sku_result_label.grid(row=6, column=0, columnspan=2, pady=5)

# Start the main loop
root.mainloop()
