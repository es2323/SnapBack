import tkinter as tk

def show_feedback(score, reaction_time, accuracy, errors):
    level = "Good" if score >= 80 else "Mild Fatigue" if score >= 60 else "Tired" if score >= 40 else "Very Fatigued"
    message = {
        "Good": "Keep it up!",
        "Mild Fatigue": "Take a short break soon.",
        "Tired": "You're running low. Take a break.",
        "Very Fatigued": "Stop and recover now."
    }[level]

    popup = tk.Tk()
    popup.title("Fatigue Score Summary")
    popup.geometry("350x280")
    popup.configure(bg="#F5F7FA")

    tk.Label(popup, text="Your Fatigue Score", font=("Helvetica", 16, "bold"), bg="#F5F7FA").pack(pady=10)
    tk.Label(popup, text=f"{score} – {level}", font=("Helvetica", 14), fg="#0078D7", bg="#F5F7FA").pack()
    tk.Label(popup, text=message, font=("Helvetica", 10), bg="#F5F7FA").pack(pady=10)

    tk.Label(popup, text=f"Reaction Time: {reaction_time} ms", bg="#F5F7FA").pack()
    tk.Label(popup, text=f"Accuracy: {accuracy}%", bg="#F5F7FA").pack()
    tk.Label(popup, text=f"Errors: {errors}", bg="#F5F7FA").pack()

    tk.Button(popup, text="OK", command=popup.destroy).pack(pady=15)
    popup.mainloop()
