import csv
import customtkinter as ctk
import tkinter as tk

def get_sku_list(file_path):
    sku_list = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sku_list.append(row['sku'])
    return sku_list

def read_pricing_data(file_path):
    pricing_data = {}
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = row['sku']
            pricing_data[key] = {
                'od': float(row['od']),
                'savings': float(row['savings']),
                'savingspct': float(row['savingspct']),
                'ec2savings': float(row['ec2savings']),
                'ec2pct': float(row['ec2pct'])
            }
    return pricing_data, file_path

def load_csv_data():
    file_path = csv_input.get()
    global pricing_data, sku_list
    pricing_data, file_name = read_pricing_data(file_path)
    sku_list = get_sku_list(file_path)

    data.configure(text=f"Data Source: {file_name}")

    for option_menu, var in zip(option_menus, [sku1_label, sku2_label]):  # Add more variables if needed.
        option_menu["menu"].delete(0, "end")
        for sku in sku_list:
            option_menu["menu"].add_command(label=sku, command=tk._setit(var, sku))


def calculate_savings():
    sku1_instances = int(sku1_amt.get())
    sku2_instances = int(sku2_amt.get())

    sku1_rate = pricing_data[sku1_label.get()]['od']
    sku2_rate = pricing_data[sku2_label.get()]['od']

    sku1_savingspct = pricing_data[sku1_label.get()]['savingspct']
    sku2_savingspct = pricing_data[sku2_label.get()]['savingspct']

    sku1_savings = sku1_instances * sku1_rate * sku1_savingspct
    sku2_savings = sku2_instances * sku2_rate * sku2_savingspct

    total_savings = sku1_savings + sku2_savings

    result_label.configure(text=f"Total Savings: ${total_savings:.2f}")
    result_label.grid(row=9, column=0, padx=(5, 5), pady=(5, 5))



root = tk.Tk()
root.title("AWS Savings Calculator")

app_frame = ctk.CTkFrame(root)
app_frame.pack(padx=10, pady=10)

csv_input = ctk.CTkEntry(app_frame, width=120)
csv_input.grid(row=0, column=0, padx=(5, 5), pady=(5, 5))

load_button = ctk.CTkButton(app_frame, text="Load CSV", command=load_csv_data)
load_button.grid(row=0, column=2, padx=(5, 0), pady=(0, 5))

data = ctk.CTkLabel(app_frame, text="Instance Code")
data.grid(row=1, column=0, padx=(5, 5), pady=(5, 5))

data_source_label = ctk.CTkLabel(app_frame, text="Qty ")
data_source_label.grid(row=1, column=1, pady=(5, 0))

sku1_label = tk.StringVar()
sku1_dropdown = tk.OptionMenu(app_frame, sku1_label, '')
sku1_dropdown.grid(row=2, column=0, padx=(5, 5), pady=(5, 5))

sku1_amt = ctk.CTkEntry(app_frame, width=20)
sku1_amt.grid(row=2, column=1, padx=(5, 5), pady=(5, 5))

sku2_label = tk.StringVar()
sku2_dropdown = tk.OptionMenu(app_frame, sku2_label, '')
sku2_dropdown.grid(row=3, column=0, padx=(5, 5), pady=(5, 5))

sku2_amt = ctk.CTkEntry(app_frame, width=20)
sku2_amt.grid(row=3, column=1, padx=(5, 5), pady=(5, 5))

"""sku3_label = ctk.CTkEntry(app_frame, width=120)
sku3_label.grid(row=4, column=0, padx=(5, 5), pady=(5, 5))

sku3_amt = ctk.CTkEntry(app_frame, width=20)
sku3_amt.grid(row=4, column=1, padx=(5, 5), pady=(5, 5))

sku4_label = ctk.CTkEntry(app_frame, width=120)
sku4_label.grid(row=5, column=0, padx=(5, 5), pady=(5, 5))

sku4_amt = ctk.CTkEntry(app_frame, width=20)
sku4_amt.grid(row=5, column=1, padx=(5, 5), pady=(5, 5))

sku5_label = ctk.CTkEntry(app_frame, width=120)
sku5_label.grid(row=6, column=0, padx=(5, 5), pady=(5, 5))

sku5_amt = ctk.CTkEntry(app_frame, width=20)
sku5_amt.grid(row=6, column=1, padx=(5, 5), pady=(5, 5))

sku6_label = ctk.CTkEntry(app_frame, width=120)
sku6_label.grid(row=7, column=0, padx=(5, 5), pady=(5, 5))

sku6_amt = ctk.CTkEntry(app_frame, width=20)
sku6_amt.grid(row=7, column=1, padx=(5, 5), pady=(5, 5))"""

calculate_button = ctk.CTkButton(app_frame, text="Calculate Savings", command=calculate_savings)
calculate_button.grid(row=8, column=0, columnspan=2, padx=(5, 5), pady=(5, 5))

result_label = ctk.CTkLabel(app_frame, text="")
result_label.grid(row=9, column=0, columnspan=2, padx=(5, 5), pady=(5, 5))


option_menus = [sku1_dropdown, sku2_dropdown]

root.mainloop()

#add read_pricing_csv button made
#read the data 