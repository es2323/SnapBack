import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from dashboard import launch_dashboard

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SnapBack - Login")
        self.root.geometry("500x400")
        self.root.configure(bg="#f0f8ff")
        self.root.resizable(False, False)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg="#0078D7", height=80)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="SnapBack", font=("Helvetica", 24, "bold"), 
                fg="white", bg="#0078D7").pack(pady=15)
        
        # Main Content Frame
        content_frame = tk.Frame(self.root, bg="#f0f8ff", padx=40, pady=20)
        content_frame.pack(expand=True, fill="both")
        
        tk.Label(content_frame, text="Welcome Back!", font=("Helvetica", 14), 
                bg="#f0f8ff").pack(pady=(10, 5))
        tk.Label(content_frame, text="Ready to get playing?", font=("Helvetica", 10), 
                bg="#f0f8ff").pack(pady=(0, 20))
        
        # Email Entry
        tk.Label(content_frame, text="Email", bg="#f0f8ff", anchor="w").pack(fill="x")
        self.email_entry = ttk.Entry(content_frame)
        self.email_entry.pack(fill="x", pady=5)
        
        # Password Entry
        tk.Label(content_frame, text="Password", bg="#f0f8ff", anchor="w").pack(fill="x")
        self.password_entry = ttk.Entry(content_frame, show="*")
        self.password_entry.pack(fill="x", pady=5)
        
        # Login Button
        login_btn = ttk.Button(content_frame, text="Login", command=self.verify_login, 
                             style="Accent.TButton")
        login_btn.pack(pady=20)
        
        # Footer Links
        footer_frame = tk.Frame(self.root, bg="#f0f8ff", pady=10)
        footer_frame.pack(fill="x")
        
        tk.Label(footer_frame, text="Forgot Password?", fg="#0078D7", bg="#f0f8ff", 
                cursor="hand2").pack()
        tk.Label(footer_frame, text="Don't have an account? Please contact your HR.", 
                font=("Helvetica", 8), bg="#f0f8ff").pack(pady=10)
        
        # Style configuration
        style = ttk.Style()
        style.configure("Accent.TButton", foreground="white", background="#0078D7")
    
    def verify_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, role FROM users WHERE email = ? AND password = ?", 
                      (email, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            name, role = result
            self.root.destroy()
            launch_dashboard(email, name, role)
        else:
            messagebox.showerror("Login Failed", "Incorrect email or password.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
