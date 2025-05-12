# 🧠 SnapBack – Employee Fatigue Monitoring System

**SnapBack** is a fatigue monitoring web application designed to promote workplace wellness by blending quick cognitive games with daily check-in surveys. It offers tailored dashboards for employees, managers, and HR staff to visualise fatigue trends and intervene early when necessary.

---

## 🚀 Features

### 👩‍💼 Multi-Role Login
- **Employee**: Access daily check-ins, play fatigue games, and view performance insights.
- **Manager**: View team-wide fatigue trends, role-based alerts, and check-in compliance rates.
- **HR**: Generate downloadable CSV reports with department-wide analytics.

### 🎮 Fatigue Detection Games
- **Reaction Game**: Measures reaction time over 10 rounds; difficulty increases progressively.
- **Focus Game**: Identify the odd word out under time pressure and distraction.
- Games are randomly selected and opened in separate windows upon clicking "Start Game".

### 📝 Daily Check-In Survey
- Interactive sliders for rest, alertness, and motivation.
- Radio button for physical discomfort.
- Submits to backend and contributes to fatigue score calculation.

### 📊 Smart Dashboards
- **Employee Dashboard**: Personalised fatigue score blending game results and survey responses.
- **Manager Dashboard**: 
  - Avg. fatigue score across team.
  - High-fatigue alerts from past 3 days.
  - 7-day trend graph.
  - Role-based breakdown.
- **HR Dashboard**: 
  - Generate CSV reports for department fatigue and key trends.

---

## 🛠️ Technologies Used

| Stack        | Tooling                            |
|--------------|-------------------------------------|
| Backend      | Flask, SQLite                       |
| Frontend     | HTML, CSS (custom), Chart.js        |
| Game Engine  | `pygame` for local game execution   |
| Visualisation| Chart.js (line graphs)              |
| Reports      | CSV via Flask `send_file`           |

---

## 🧩 System Architecture

- **Modular Blueprints**: Flask routes organised into `auth.py` and `main.py`.
- **MVC-lite**: Templates (Views), Routes (Controllers), Database (Model).
- **Game Integration**:
  - `run_game.py` selects and launches a game in a subprocess.
  - Games submit results via REST POST to `/submit_score`.

---

## 🧪 Example Users for Testing

| Email                  | Password     | Role     | Team     |
|------------------------|--------------|----------|----------|
| levi@example.com       | pass123      | employee | Team A   |
| manager1@example.com   | managerpass  | manager  | Team A   |
| hr@example.com         | hrpass       | hr       | HR       |


---



