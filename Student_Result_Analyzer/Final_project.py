# ==========================
# Student Result Analyzer (MySQL + Average Marks + Sorted Graph)
# ==========================

import tkinter as tk
from tkinter import messagebox
import mysql.connector as sql
import matplotlib.pyplot as plt

# --------------------------
# MySQL Connection Setup
# --------------------------
try:
    con = sql.connect(
        host="localhost",
        user="root",
        password="gora123",  # 🔹 Change this to your MySQL password
        database="student_db"
    )
    cursor = con.cursor()
    print("✅ MySQL Connected Successfully!")
except Exception as e:
    print("❌ Connection Error:", e)

# --------------------------
# Create Table if not exists
# --------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    marks FLOAT
)
""")
con.commit()

# --------------------------
# Tkinter GUI Setup
# --------------------------
root = tk.Tk()
root.title("Student Result Analyzer (MySQL Version)")
root.geometry("450x350")
root.config(bg="#eef2ff")

# --------------------------
# Labels and Input Fields
# --------------------------
tk.Label(root, text="Enter Student Name:", font=("Arial", 12), bg="#eef2ff").pack(pady=5)
name_entry = tk.Entry(root, width=30)
name_entry.pack()

tk.Label(root, text="Enter Marks (comma-separated):", font=("Arial", 12), bg="#eef2ff").pack(pady=5)
marks_entry = tk.Entry(root, width=30)
marks_entry.pack()

# --------------------------
# Save Data Function
# --------------------------
def save_data():
    name = name_entry.get().strip()
    marks = marks_entry.get().strip()

    if name == "" or marks == "":
        messagebox.showerror("Error", "Please fill all fields!")
        return

    try:
        # Convert marks like "89,78,83" → [89, 78, 83]
        mark_list = [int(x.strip()) for x in marks.split(",") if x.strip().isdigit()]

        if not mark_list:
            messagebox.showerror("Error", "Please enter valid marks (numbers only).")
            return

        avg = sum(mark_list) / len(mark_list)

        # Save average mark in MySQL
        cursor.execute("INSERT INTO students (name, marks) VALUES (%s, %s)", (name, avg))
        con.commit()

        messagebox.showinfo("Success", f"Data Saved! Average Marks = {avg:.2f}")
        name_entry.delete(0, tk.END)
        marks_entry.delete(0, tk.END)

        # ✅ Automatically show sorted graph (non-blocking)
        show_graph()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# --------------------------
# Show Data Function
# --------------------------
def show_data():
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    if not data:
        messagebox.showinfo("Info", "No data found in database.")
        return

    result_window = tk.Toplevel(root)
    result_window.title("All Student Records")
    result_window.geometry("400x300")

    text = tk.Text(result_window, wrap=tk.WORD, font=("Arial", 11))
    text.pack(fill="both", expand=True)

    for row in data:
        text.insert(tk.END, f"ID: {row[0]} | Name: {row[1]} | Avg Marks: {row[2]:.2f}\n")
    text.config(state="disabled")

# --------------------------
# Show Graph Function
# --------------------------
def show_graph():
    cursor.execute("SELECT name, marks FROM students")
    data = cursor.fetchall()
    if not data:
        messagebox.showinfo("Info", "No data found to display graph.")
        return

    # 🔹 Sort data by average marks (descending)
    data.sort(key=lambda x: x[1], reverse=True)

    names = [row[0] for row in data]
    marks = [row[1] for row in data]

    plt.figure(figsize=(7,4))
    bars = plt.bar(names, marks, color='lightgreen', edgecolor='black')

    plt.xlabel("Student Name", fontsize=12)
    plt.ylabel("Average Marks", fontsize=12)
    plt.title("Student Performance (High to Low)", fontsize=14)
    plt.xticks(rotation=30)

    # Add labels on bars
    for bar in bars:
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                 f'{bar.get_height():.1f}', ha='center', fontsize=10)

    plt.tight_layout()
    plt.show(block=False)  # ✅ Prevents loop / freeze issue

# --------------------------
# Buttons
# --------------------------
tk.Button(root, text="Save Data", command=save_data, bg="#4CAF50", fg="white", width=15).pack(pady=10)
tk.Button(root, text="Show Data", command=show_data, bg="#2196F3", fg="white", width=15).pack(pady=5)
tk.Button(root, text="Show Graph", command=show_graph, bg="#9C27B0", fg="white", width=15).pack(pady=5)

# --------------------------
# Run the App
# --------------------------
root.mainloop()
con.close()