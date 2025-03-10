import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# إنشاء قاعدة البيانات
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT,
                    deadline TEXT
                 )""")
conn.commit()

# دالة إضافة مهمة
def add_task():
    task = task_entry.get()
    deadline = deadline_entry.get()
    if task and deadline:
        cursor.execute("INSERT INTO tasks (task, deadline) VALUES (?, ?)", (task, deadline))
        conn.commit()
        update_list()
        task_entry.delete(0, tk.END)
        deadline_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("خطأ", "يجب ملء جميع الحقول!")

# دالة تحديث القائمة
def update_list():
    task_list.delete(0, tk.END)
    cursor.execute("SELECT * FROM tasks ORDER BY deadline")
    for row in cursor.fetchall():
        task_list.insert(tk.END, f"{row[1]} - {row[2]}")

# دالة حذف مهمة
def delete_task():
    selected = task_list.curselection()
    if selected:
        task_text = task_list.get(selected[0])
        task_name = task_text.split(" - ")[0]
        cursor.execute("DELETE FROM tasks WHERE task = ?", (task_name,))
        conn.commit()
        update_list()

# إنشاء الواجهة
root = tk.Tk()
root.title("📋 المساعد الذكي لإدارة المهام")
root.geometry("400x400")

tk.Label(root, text="📌 المهمة:").pack()
task_entry = tk.Entry(root, width=40)
task_entry.pack(pady=5)

tk.Label(root, text="⏳ الموعد النهائي (YYYY-MM-DD):").pack()
deadline_entry = tk.Entry(root, width=40)
deadline_entry.pack(pady=5)

tk.Button(root, text="✅ إضافة", command=add_task).pack(pady=5)
tk.Button(root, text="❌ حذف", command=delete_task).pack(pady=5)

task_list = tk.Listbox(root, width=50, height=10)
task_list.pack(pady=10)

update_list()
root.mainloop()
