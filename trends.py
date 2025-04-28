import tkinter as tk
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from logic.fatigue_score import get_fatigue_level

class ViewTrends:
    def __init__(self, email, is_manager=False):
        self.email = email
        self.is_manager = is_manager
        
        self.root = tk.Tk()
        self.root.title("Fatigue Trends")
        self.root.geometry("900x600")
        self.root.configure(bg="#f5f7fa")
        
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#0078D7", height=60)
        header_frame.pack(fill="x")
        
        title = "Team Fatigue Trends" if self.is_manager else "Your Fatigue Trends"
        tk.Label(header_frame, text=title, font=("Helvetica", 16), 
                fg="white", bg="#0078D7").pack(pady=15)
        
        # Content Frame
        content_frame = tk.Frame(self.root, bg="#f5f7fa", padx=20, pady=20)
        content_frame.pack(expand=True, fill="both")
        
        # Create figure
        fig, ax = plt.subplots(figsize=(8, 4))
        fig.patch.set_facecolor("#f5f7fa")
        ax.set_facecolor("#f5f7fa")
        
        # Get data
        conn = sqlite3.connect("users.db")
        if self.is_manager:
            cursor = conn.execute('''
                SELECT u.name, AVG(g.fatigue_score), strftime('%Y-%m-%d', g.timestamp)
                FROM game_sessions g
                JOIN users u ON g.user_email = u.email
                WHERE u.team = (SELECT team FROM users WHERE email = ?)
                GROUP BY u.name, strftime('%Y-%m-%d', g.timestamp)
                ORDER BY g.timestamp
            ''', (self.email,))
            
            # Group by user
            data = {}
            for name, score, date in cursor.fetchall():
                if name not in data:
                    data[name] = {'dates': [], 'scores': []}
                data[name]['dates'].append(date)
                data[name]['scores'].append(score)
            
            # Plot each user
            for name, values in data.items():
                ax.plot(values['dates'], values['scores'], 'o-', label=name)
            
            ax.legend()
            ax.set_title("Team Fatigue Over Time")
        else:
            cursor = conn.execute('''
                SELECT strftime('%Y-%m-%d', timestamp), AVG(fatigue_score)
                FROM game_sessions
                WHERE user_email = ?
                GROUP BY strftime('%Y-%m-%d', timestamp)
                ORDER BY timestamp
            ''', (self.email,))
            
            dates, scores = zip(*cursor.fetchall())
            ax.plot(dates, scores, 'o-', color="#0078D7")
            ax.set_title("Your Fatigue Over Time")
        
        conn.close()
        
        ax.set_ylim(0, 100)
        ax.set_ylabel("Fatigue Score")
        ax.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Embed plot in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")
        
        # Close Button
        ttk.Button(content_frame, text="Close", 
                  command=self.root.destroy).pack(pady=10)

if __name__ == "__main__":
    ViewTrends("test@example.com").root.mainloop()
