import sqlite3
import csv
import tkinter as tk
from tkinter import messagebox, ttk

class ExportReport:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Export HR Report")
        self.root.geometry("400x200")
        self.root.configure(bg="#f5f7fa")
        
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#0078D7", height=60)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="Export HR Report", font=("Helvetica", 16), 
                fg="white", bg="#0078D7").pack(pady=15)
        
        # Content Frame
        content_frame = tk.Frame(self.root, bg="#f5f7fa", padx=20, pady=20)
        content_frame.pack(expand=True, fill="both")
        
        # Export Button
        ttk.Button(content_frame, text="Export to CSV", 
                  command=self.export_to_csv,
                  style="Accent.TButton").pack(fill="x", pady=10)
        
        # Close Button
        ttk.Button(content_frame, text="Close", 
                  command=self.root.destroy).pack(fill="x", pady=10)
        
        # Style configuration
        style = ttk.Style()
        style.configure("Accent.TButton", foreground="white", background="#0078D7")
    
    def export_to_csv(self):
        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.execute('''
                SELECT u.email, u.name, u.role, u.team, 
                       AVG(g.fatigue_score) as avg_score,
                       COUNT(g.id) as sessions
                FROM users u
                LEFT JOIN game_sessions g ON u.email = g.user_email
                GROUP BY u.email
            ''')
            
            with open("fatigue_report.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Email", "Name", "Role", "Team", "Avg Fatigue Score", "Sessions Completed"])
                writer.writerows(cursor)
            
            conn.close()
            messagebox.showinfo("Success", "Report exported as 'fatigue_report.csv'")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {str(e)}")

# For backward compatibility (if any code still uses the old function name)
def export_report():
    ExportReport()
