import tkinter as tk
import numpy as np
from scipy.stats import beta

# Constants
cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
rows = range(1, 11)
grid_size = 10

# Initialize the alpha and beta matrices
alpha = np.ones((grid_size, grid_size))
beta_params = np.ones((grid_size, grid_size))
hits = np.zeros((grid_size, grid_size), dtype=bool)

# Variables to keep track of used fields and current prediction
used = []
current_prediction = None

def reset():
    global used, alpha, beta_params, hits, current_prediction
    used = []
    alpha = np.ones((grid_size, grid_size))
    beta_params = np.ones((grid_size, grid_size))
    hits = np.zeros((grid_size, grid_size), dtype=bool)
    current_prediction = None
    display_message("Game has been reset.")

def mark_hit():
    global current_prediction
    if current_prediction:
        update_thompson_sampling(current_prediction, 'hit')
        display_message(f"Marked {current_prediction} as hit.")
        current_prediction = None
    else:
        display_message("No current prediction to mark.")

def mark_miss():
    global current_prediction
    if current_prediction:
        update_thompson_sampling(current_prediction, 'miss')
        display_message(f"Marked {current_prediction} as miss.")
        current_prediction = None
    else:
        display_message("No current prediction to mark.")

def update_thompson_sampling(field, result):
    col, row = cols.index(field[0]), int(field[1]) - 1
    if result == 'hit':
        alpha[row, col] += 1
        hits[row, col] = True
    else:
        beta_params[row, col] += 1
    used.append(field)

def thompson_sampling():
    global used, current_prediction
    if len(used) == 100:
        display_message("You ran out of options.")
        return
    
    samples = np.zeros((grid_size, grid_size))
    for i in range(grid_size):
        for j in range(grid_size):
            samples[i, j] = beta.rvs(alpha[i, j], beta_params[i, j])
    
    best_move = np.unravel_index(np.argmax(samples), samples.shape)
    field = f"{cols[best_move[1]]}{best_move[0] + 1}"
    if field not in used:
        current_prediction = field
        display_message(f"Thompson Sampling selected field: {field}")
    else:
        thompson_sampling()  # Retry if field already used

def display_message(message):
    message_text.insert(tk.END, message + "\n")
    message_text.see(tk.END)

# Creating the main window
root = tk.Tk()
root.title("Field Selector")

# Creating buttons for each function
reset_button = tk.Button(root, text="Reset", command=reset)
ts_button = tk.Button(root, text="Thompson Sampling", command=thompson_sampling)
hit_button = tk.Button(root, text="Mark Hit", command=mark_hit)
miss_button = tk.Button(root, text="Mark Miss", command=mark_miss)

# Creating a Text widget to display messages
message_text = tk.Text(root, height=10, width=50)

# Placing widgets on the window
reset_button.pack(pady=10)
ts_button.pack(pady=10)
hit_button.pack(pady=10)
miss_button.pack(pady=10)
message_text.pack(pady=10)

# Running the GUI loop
root.mainloop()