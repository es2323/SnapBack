import tkinter as tk
from tkinter import ttk
import sqlite3

class DailyCheckIn:
    def __init__(self, email):
        self.email = email
        self.root = tk.Toplevel()
        self.root.title("Daily Check-In")
        self.root.geometry("400x400")
        self.root.configure(bg="#f5f7fa")
        
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#0078D7", height=60)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="Daily Check-In", font=("Helvetica", 16), 
                fg="white", bg="#0078D7").pack(pady=15)
        
        # Content Frame
        content_frame = tk.Frame(self.root, bg="#f5f7fa", padx=20, pady=20)
        content_frame.pack(expand=True, fill="both")
        
        # Rest Score
        tk.Label(content_frame, text="How well-rested do you feel? (1-5)", 
                bg="#f5f7fa").pack(anchor="w")
        self.rest_score = ttk.Combobox(content_frame, values=[1, 2, 3, 4, 5])
        self.rest_score.pack(fill="x", pady=5)
        
        # Discomfort
        tk.Label(content_frame, text="Any physical discomfort today?", 
                bg="#f5f7fa").pack(anchor="w")
        self.discomfort = ttk.Combobox(content_frame, values=["Yes", "No"])
        self.discomfort.pack(fill="x", pady=5)
        
        # Notes
        tk.Label(content_frame, text="Additional notes:", 
                bg="#f5f7fa").pack(anchor="w")
        self.notes = tk.Text(content_frame, height=5)
        self.notes.pack(fill="x", pady=5)
        
        # Submit Button
        ttk.Button(content_frame, text="Submit", 
                  command=self.save_check_in,
                  style="Accent.TButton").pack(fill="x", pady=20)
        
        # Style configuration
        style = ttk.Style()
        style.configure("Accent.TButton", foreground="white", background="#0078D7")
    
    def save_check_in(self):
        try:
            rest = int(self.rest_score.get())
            disc = self.discomfort.get()
            notes = self.notes.get("1.0", tk.END).strip()
            
            conn = sqlite3.connect('users.db')
            conn.execute("""
                INSERT INTO check_ins 
                (user_email, rest_score, discomfort, notes) 
                VALUES (?, ?, ?, ?)
            """, (self.email, rest, disc, notes))
            conn.commit()
            conn.close()
            
            tk.messagebox.showinfo("Success", "Check-in submitted successfully!")
            self.root.destroy()
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter valid values for all fields")

# For backward compatibility (if any code still uses the old function name)
def daily_check_in(email):
    DailyCheckIn(email)
