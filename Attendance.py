import tkinter as tk
from tkinter import messagebox, ttk
import csv
import matplotlib.pyplot as plt

root = tk.Tk()
root.title("College Attendance Management System")
root.geometry("900x650")
root.configure(bg="whiteclear")

title_label = tk.Label(root,
    text="PRINCY'S INSTITUTE OF SCIENCE AND TECHNOLOGY",
    font=("Algerian", 22, "bold"),
    fg="darkblue",
    bg="lightyellow")
title_label.pack(pady=15)

students = []

class Student:
    def __init__(self, student_id, name, age, course):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.course = course
        self.total_classes = 0
        self.attended_classes = 0

    def mark_attendance(self, present):
        self.total_classes += 1
        if present:
            self.attended_classes += 1

    def attendance_percentage(self):
        if self.total_classes == 0:
            return 0
        return (self.attended_classes / self.total_classes) * 100

# --- Functions ---
def add_student():
    name = entry_name.get()
    age = entry_age.get()
    course = entry_course.get()

    if not name or not age or not course:
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    student_id = len(students) + 1
    students.append(Student(student_id, name, int(age), course))
    messagebox.showinfo("Success", "Student added successfully!")
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_course.delete(0, tk.END)
    load_students()
def mark_attendance():
    selected = student_list.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Select a student first!")
        return

    student_id = student_list.item(selected[0])["values"][0]
    present = var_present.get()

    for student in students:
        if student.student_id == student_id:
            student.mark_attendance(present)
            break

    messagebox.showinfo("Success", "Attendance marked successfully!")
    load_students()

def load_students():
    for row in student_list.get_children():
        student_list.delete(row)

    for student in students:
        student_list.insert("", tk.END, values=(student.student_id, student.name, student.age, student.course))

def search_student():
    query = entry_search.get().lower()
    for row in student_list.get_children():
        student_list.delete(row)

    for student in students:
        if query in student.name.lower() or query in student.course.lower():
            student_list.insert("", tk.END, values=(student.student_id, student.name, student.age, student.course))

def display_report():
    report_window = tk.Toplevel(root)
    report_window.title("Attendance Report")
    report_window.geometry("600x400")

    tree = ttk.Treeview(report_window, columns=("ID", "Name", "Course", "Total", "Attended", "Percentage"), show="headings")
    tree.pack(fill=tk.BOTH, expand=True)

    for col in tree["columns"]:
        tree.heading(col, text=col)

    names = []
    percentages = []

    for student in students:
        percentage = student.attendance_percentage()
        tree.insert("", tk.END, values=(student.student_id, student.name, student.course,
                                        student.total_classes, student.attended_classes, f"{percentage:.2f}%"))
        names.append(student.name)
        percentages.append(percentage)

    # --- Plot Chart ---
    if percentages:
        plt.figure(figsize=(6,4))
        plt.bar(names, percentages, color="skyblue")
        plt.axhline(y=75, color="red", linestyle="--", label="Threshold 75%")
        plt.title("Attendance Percentage")
        plt.xlabel("Students")
        plt.ylabel("Percentage")
        plt.legend()
        plt.show()

def export_csv():
    with open("attendance_report.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Course", "Total Classes", "Attended", "Percentage"])
        for student in students:
            writer.writerow([student.student_id, student.name, student.course,
                             student.total_classes, student.attended_classes, f"{student.attendance_percentage():.2f}%"])
    messagebox.showinfo("Exported", "Report saved as attendance_report.csv")

def view_history():
    selected = student_list.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Select a student first!")
        return

    student_id = student_list.item(selected[0])["values"][0]

    history_window = tk.Toplevel(root)
    history_window.title("Attendance History")
    history_window.geometry("400x300")

    tree = ttk.Treeview(history_window, columns=("Class No", "Present"), show="headings")
    tree.pack(fill=tk.BOTH, expand=True)

    tree.heading("Class No", text="Class No")
    tree.heading("Present", text="Present")

    for student in students:
        if student.student_id == student_id:
            for i in range(1, student.total_classes + 1):
                present = "Yes" if i <= student.attended_classes else "No"
                tree.insert("", tk.END, values=(i, present))

# --- GUI Layout ---
frame = tk.Frame(root, bg="whiteclear", padx=20, pady=20)
frame.pack(pady=10)

tk.Label(frame, text="Name:", bg="whiteclear").grid(row=0, column=0)
entry_name = tk.Entry(frame)
entry_name.grid(row=0, column=1)

tk.Label(frame, text="Age:", bg="lightyellow").grid(row=1, column=0)
entry_age = tk.Entry(frame)
entry_age.grid(row=1, column=1)

tk.Label(frame, text="Course:", bg="lightyellow").grid(row=2, column=0)
entry_course = tk.Entry(frame)
entry_course.grid(row=2, column=1)

tk.Button(frame, text="Add Student", command=add_student, bg="lightgreen").grid(row=3, columnspan=2, pady=10)

# Search Bar
entry_search = tk.Entry(root)
entry_search.pack(pady=5)
tk.Button(root, text="Search Student", command=search_student, bg="lightblue").pack(pady=5)

# Student List
student_list = ttk.Treeview(root, columns=("ID", "Name", "Age", "Course"), show="headings")
student_list.pack(fill=tk.BOTH, expand=True)

for col in student_list["columns"]:
    student_list.heading(col, text=col)

load_students()
# Attendance Marking
var_present = tk.IntVar()
tk.Checkbutton(root, text="Present", variable=var_present, bg="lightyellow").pack()
tk.Button(root, text="Mark Attendance", command=mark_attendance, bg="orange").pack(pady=10)

# Report & Extra Features
tk.Button(root, text="Display Report", command=display_report, bg="lightpink").pack(pady=10)
tk.Button(root, text="Export Report to CSV", command=export_csv, bg="lightgrey").pack(pady=10)
tk.Button(root, text="View Attendance History", command=view_history, bg="lightcoral").pack(pady=10)

root.mainloop()