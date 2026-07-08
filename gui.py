import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import database
import webbrowser


# ----------------------------------------
# Load Data from Database
# ----------------------------------------
def load_data():

    # Remove old rows
    for row in table.get_children():
        table.delete(row)

    # Get data
    rows = database.get_all_history()

    total_label.config(text=f"Total Records : {len(rows)}")

    # Insert rows
    for row in rows:
        table.insert("", tk.END, values=row)

    # Last Updated Time
    current = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
    last_updated.config(text=f"Last Updated : {current}")


# ----------------------------------------
# Search Function
# ----------------------------------------
def search():

    keyword = search_entry.get().strip()

    for row in table.get_children():
        table.delete(row)

    rows = database.search_history(keyword)

    total_label.config(text=f"Results : {len(rows)}")

    for row in rows:
        table.insert("", tk.END, values=row)


# ----------------------------------------
# Refresh Function
# ----------------------------------------
def refresh():

    search_entry.delete(0, tk.END)

    load_data()


# ----------------------------------------
# Auto Refresh
# ----------------------------------------
def auto_refresh():

    load_data()

    window.after(5000, auto_refresh)


# ----------------------------------------
# Export CSV
# ----------------------------------------
def export_csv():

    database.export_to_csv()

    messagebox.showinfo(
        "Export Successful",
        "History exported successfully to history_export.csv"
    )


# ----------------------------------------
# Open URL on Double Click
# ----------------------------------------
def open_url(event):

    selected = table.focus()

    if not selected:
        return

    values = table.item(selected, "values")

    if len(values) >= 3:
        webbrowser.open(values[2])


# ----------------------------------------
# Main Window
# ----------------------------------------
window = tk.Tk()

window.title("Browser History Utility")

window.geometry("1200x650")

window.resizable(True, True)

# Dark Background
window.configure(bg="#1e1e1e")


# ----------------------------------------
# Heading
# ----------------------------------------
heading = tk.Label(
    window,
    text="Browser History Utility",
    font=("Arial", 18, "bold"),
    bg="#1e1e1e",
    fg="white"
)

heading.pack(pady=10)


# ----------------------------------------
# Status
# ----------------------------------------
status_label = tk.Label(
    window,
    text="🟢 Monitoring Running",
    font=("Arial", 11, "bold"),
    bg="#1e1e1e",
    fg="lightgreen"
)

status_label.pack()


# ----------------------------------------
# Last Updated
# ----------------------------------------
last_updated = tk.Label(
    window,
    text="Last Updated : --",
    font=("Arial", 10),
    bg="#1e1e1e",
    fg="white"
)

last_updated.pack(pady=5)


# ----------------------------------------
# Total Records
# ----------------------------------------
total_label = tk.Label(
    window,
    text="Total Records : 0",
    font=("Arial", 12),
    bg="#1e1e1e",
    fg="white"
)

total_label.pack()


# ----------------------------------------
# Search Frame
# ----------------------------------------
frame = tk.Frame(window, bg="#1e1e1e")

frame.pack(pady=10)


# Search Box
search_entry = tk.Entry(
    frame,
    width=50,
    bg="#2d2d2d",
    fg="white",
    insertbackground="white"
)

search_entry.grid(row=0, column=0, padx=5)


# Search Button
search_button = tk.Button(
    frame,
    text="Search",
    command=search,
    width=12,
    bg="#3c3c3c",
    fg="white"
)

search_button.grid(row=0, column=1, padx=5)


# Refresh Button
refresh_button = tk.Button(
    frame,
    text="Refresh",
    command=refresh,
    width=12,
    bg="#3c3c3c",
    fg="white"
)

refresh_button.grid(row=0, column=2, padx=5)


# Export Button
export_button = tk.Button(
    frame,
    text="Export CSV",
    command=export_csv,
    width=12,
    bg="#3c3c3c",
    fg="white"
)

export_button.grid(row=0, column=3, padx=5)
# ----------------------------------------
# Treeview Style (Dark)
# ----------------------------------------
style = ttk.Style()

try:
    style.theme_use("clam")
except:
    pass

style.configure(
    "Treeview",
    background="#2d2d2d",
    foreground="white",
    fieldbackground="#2d2d2d",
    rowheight=25
)

style.configure(
    "Treeview.Heading",
    font=("Arial", 10, "bold")
)

style.map(
    "Treeview",
    background=[("selected", "#0078D7")]
)

# ----------------------------------------
# Table
# ----------------------------------------
columns = (
    "ID",
    "Title",
    "URL",
    "Saved Time"
)

table_frame = tk.Frame(window)

table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

table.heading("ID", text="ID")
table.heading("Title", text="Title")
table.heading("URL", text="URL")
table.heading("Saved Time", text="Saved Time")

table.column("ID", width=80, anchor="center")
table.column("Title", width=250)
table.column("URL", width=600)
table.column("Saved Time", width=180)

# ----------------------------------------
# Scrollbars
# ----------------------------------------
vertical_scroll = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=table.yview
)

horizontal_scroll = ttk.Scrollbar(
    table_frame,
    orient="horizontal",
    command=table.xview
)

table.configure(
    yscrollcommand=vertical_scroll.set,
    xscrollcommand=horizontal_scroll.set
)

table.grid(row=0, column=0, sticky="nsew")
vertical_scroll.grid(row=0, column=1, sticky="ns")
horizontal_scroll.grid(row=1, column=0, sticky="ew")

table_frame.rowconfigure(0, weight=1)
table_frame.columnconfigure(0, weight=1)

# ----------------------------------------
# Double Click Event
# ----------------------------------------
table.bind("<Double-1>", open_url)

# ----------------------------------------
# Load Data
# ----------------------------------------
load_data()

# ----------------------------------------
# Auto Refresh
# ----------------------------------------
auto_refresh()

# ----------------------------------------
# Run Application
# ----------------------------------------
window.mainloop()