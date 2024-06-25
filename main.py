#Assistant for playing a game of Battleships 
#   ___            __       
#  / _ | ___ __ __/ /_____ _
# / __ |(_-</ // /  '_/ _ `/
#/_/ |_/___/\_,_/_/\_\\_,_/ 

import tkinter as tk
import random

cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
rows = range(1, 11)
used = []

def reset():
    global used
    used = []
    display_message("Game has been reset.")

def manually():
    global used
    field = manual_entry.get()
    
    # Validate the input
    if len(field) == 2 and field[0] in cols and field[1].isdigit() and int(field[1]) in rows:
        if field not in used:
            used.append(field)
            display_message(f"Field {field} added to used.")
        else:
            display_message(f"Field {field} is already used.")
    else:
        display_message("Invalid input. Please enter a valid field (e.g., 'a1', 'b2').")

def gen():
    global used
    if len(used) == 100:
        display_message("You ran out of options.")
        return
    
    while True:
        a = str(random.choice(cols)) + str(random.choice(rows))
        if a not in used:
            used.append(a)
            display_message(f"Generated field: {a}")
            break

def display_message(message):
    message_text.insert(tk.END, message + "\n")
    message_text.see(tk.END)

# Creating the main window
root = tk.Tk()
root.title("Battleships")

# Creating buttons for each function
reset_button = tk.Button(root, text="Reset", command=reset)
manual_button = tk.Button(root, text="Manually", command=manually)
gen_button = tk.Button(root, text="Generate", command=gen)

# Creating an Entry widget for manual input
manual_entry = tk.Entry(root)
manual_entry_label = tk.Label(root, text="Enter field manually:")

# Creating a Text widget to display messages
message_text = tk.Text(root, height=10, width=50)

# Placing widgets on the window
reset_button.pack(pady=10)
manual_entry_label.pack()
manual_entry.pack(pady=5)
manual_button.pack(pady=10)
gen_button.pack(pady=10)
message_text.pack(pady=10)

# Running the GUI loop
root.mainloop()