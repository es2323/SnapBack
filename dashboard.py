import tkinter as tk
from tkinter import ttk
from survey import DailyCheckIn
from games.game_menu import GameMenu
from trends import ViewTrends
from report import ExportReport
import sqlite3

class Dashboard:
    def __init__(self, root, email, name, role):
        self.root = root
        self.email = email
        self.name = name
        self.role = role
        
        self.root.title(f"SnapBack - {role.capitalize()} Dashboard")
        self.root.geometry("900x600")
        self.root.configure(bg="#f5f7fa")
        
        self.setup_ui()
    
    def setup_ui(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg="#0078D7", height=80)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text=f"Welcome, {self.name}!", font=("Helvetica", 16), 
                fg="white", bg="#0078D7").pack(side="left", padx=20)
        
        # Logout Button
        logout_btn = ttk.Button(header_frame, text="Logout", command=self.root.destroy,
                              style="Accent.TButton")
        logout_btn.pack(side="right", padx=20)
        
        # Main Content Frame
        content_frame = tk.Frame(self.root, bg="#f5f7fa")
        content_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Dashboard Cards
        if self.role == "employee":
            self.setup_employee_dashboard(content_frame)
        elif self.role == "manager":
            self.setup_manager_dashboard(content_frame)
        elif self.role == "hr":
            self.setup_hr_dashboard(content_frame)
        
        # Style configuration
        style = ttk.Style()
        style.configure("Accent.TButton", foreground="white", background="#0078D7")
        style.configure("Card.TFrame", background="white", borderwidth=1, 
                       relief="solid", bordercolor="#e1e5ea")
    
    def setup_employee_dashboard(self, parent):
        # Current Status Card
        status_card = ttk.Frame(parent, style="Card.TFrame", padding=15)
        status_card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        tk.Label(status_card, text="Your Current Status", font=("Helvetica", 12, "bold"), 
                bg="white").pack(anchor="w")
        
        # Get latest fatigue score
        conn = sqlite3.connect("users.db")
        cursor = conn.execute("SELECT fatigue_score FROM game_sessions WHERE user_email = ? ORDER BY timestamp DESC LIMIT 1", (self.email,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            score = result[0]
            status = self.get_fatigue_status(score)
            color = self.get_status_color(score)
            
            tk.Label(status_card, text=f"Fatigue Score: {score}", font=("Helvetica", 24), 
                     fg=color, bg="white").pack(pady=10)
            tk.Label(status_card, text=status, font=("Helvetica", 14), 
                     fg=color, bg="white").pack()
        else:
            tk.Label(status_card, text="No data available", bg="white").pack(pady=10)
        
        # Quick Actions Card
        actions_card = ttk.Frame(parent, style="Card.TFrame", padding=15)
        actions_card.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        tk.Label(actions_card, text="Quick Actions", font=("Helvetica", 12, "bold"), 
                bg="white").pack(anchor="w")
        
        ttk.Button(actions_card, text="Daily Check-In", 
                  command=lambda: DailyCheckIn(self.email)).pack(fill="x", pady=5)
        ttk.Button(actions_card, text="Play Fatigue Games", 
                  command=GameMenu).pack(fill="x", pady=5)
        ttk.Button(actions_card, text="View My Trends", 
                  command=lambda: ViewTrends(self.email)).pack(fill="x", pady=5)
        
        # Configure grid weights
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure(0, weight=1)
    
    def setup_manager_dashboard(self, parent):
        # Team Overview Card
        overview_card = ttk.Frame(parent, style="Card.TFrame", padding=15)
        overview_card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        tk.Label(overview_card, text="Team Overview", font=("Helvetica", 12, "bold"), 
                bg="white").pack(anchor="w")
        
        # Get team data
        conn = sqlite3.connect("users.db")
        cursor = conn.execute('''
            SELECT u.name, AVG(g.fatigue_score) 
            FROM game_sessions g
            JOIN users u ON g.user_email = u.email
            WHERE u.team = (SELECT team FROM users WHERE email = ?)
            GROUP BY u.email
        ''', (self.email,))
        results = cursor.fetchall()
        conn.close()
        
        if results:
            for name, score in results:
                status = self.get_fatigue_status(score)
                color = self.get_status_color(score)
                
                frame = tk.Frame(overview_card, bg="white")
                frame.pack(fill="x", pady=5)
                
                tk.Label(frame, text=name, bg="white", width=15, anchor="w").pack(side="left")
                tk.Label(frame, text=f"{score:.1f}", bg="white", width=10, 
                        fg=color, anchor="w").pack(side="left")
                tk.Label(frame, text=status, bg="white", fg=color).pack(side="left")
        else:
            tk.Label(overview_card, text="No team data available", bg="white").pack(pady=10)
        
        # Actions Card
        actions_card = ttk.Frame(parent, style="Card.TFrame", padding=15)
        actions_card.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        tk.Label(actions_card, text="Actions", font=("Helvetica", 12, "bold"), 
                bg="white").pack(anchor="w")
        
        ttk.Button(actions_card, text="View Team Trends", 
                  command=lambda: ViewTrends(self.email, is_manager=True)).pack(fill="x", pady=5)
        
        # Configure grid weights
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
    
    def setup_hr_dashboard(self, parent):
        # HR Overview Card
        overview_card = ttk.Frame(parent, style="Card.TFrame", padding=15)
        overview_card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        tk.Label(overview_card, text="Organization Overview", font=("Helvetica", 12, "bold"), 
                bg="white").pack(anchor="w")
        
        # Get organization data
        conn = sqlite3.connect("users.db")
        cursor = conn.execute('''
            SELECT team, AVG(fatigue_score) 
            FROM game_sessions g
            JOIN users u ON g.user_email = u.email
            GROUP BY team
        ''')
        results = cursor.fetchall()
        conn.close()
        
        if results:
            for team, score in results:
                status = self.get_fatigue_status(score)
                color = self.get_status_color(score)
                
                frame = tk.Frame(overview_card, bg="white")
                frame.pack(fill="x", pady=5)
                
                tk.Label(frame, text=team, bg="white", width=15, anchor="w").pack(side="left")
                tk.Label(frame, text=f"{score:.1f}", bg="white", width=10, 
                        fg=color, anchor="w").pack(side="left")
                tk.Label(frame, text=status, bg="white", fg=color).pack(side="left")
        else:
            tk.Label(overview_card, text="No organization data available", bg="white").pack(pady=10)
        
        # Actions Card
        actions_card = ttk.Frame(parent, style="Card.TFrame", padding=15)
        actions_card.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        tk.Label(actions_card, text="Actions", font=("Helvetica", 12, "bold"), 
                bg="white").pack(anchor="w")
        
        ttk.Button(actions_card, text="Generate HR Report", 
                  command=ExportReport).pack(fill="x", pady=5)
        
        # Configure grid weights
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
    
    def get_fatigue_status(self, score):
        if score >= 80:
            return "Optimal"
        elif score >= 60:
            return "Mild Fatigue"
        elif score >= 40:
            return "Tired"
        else:
            return "Very Fatigued"
    
    def get_status_color(self, score):
        if score >= 80:
            return "#2ecc71"  # Green
        elif score >= 60:
            return "#f39c12"  # Orange
        elif score >= 40:
            return "#e74c3c"  # Red
        else:
            return "#c0392b"  # Dark Red

def launch_dashboard(email, name, role):
    root = tk.Tk()
    Dashboard(root, email, name, role)
    root.mainloop()
