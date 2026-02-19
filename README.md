# 🏆 Sportify Tournament Manager

A premium, high-performance web application designed to manage sports tournaments with ease. Built with **FastAPI** and **Vanilla Javascript**, Sportify offers a sleek, responsive experience for organizers and fans alike.

🔗 **Live Repo:** [https://github.com/Ravi2405-143/badminton.git](https://github.com/Ravi2405-143/badminton.git)

## ✨ Key Features

- **Multi-Sport Support**: Specialized logic for **Cricket** (Runs/Wickets) and **Badminton** (Sets).
- **Intelligent Fixtures**: Automatic fixture generation for League and Knockout formats (handles "Byes" for odd team counts).
- **Pro Standings**: Real-time points table with Wins/Losses, Points Gained/Lost, and **NRR (Point Differential)**.
- **Global Ecosystem**: 
  - **Recent Results**: A live feed of the last 10 completed matches across all tournaments.
  - **Top Rankings**: System-wide leaderboards for teams and players.
- **Premium UI/UX**: Modern dark mode with glassmorphism, fluid animations, and full mobile responsiveness.
- **Cloud Ready**: Pre-configured for seamless deployment on **Vercel**.

## 🛠️ Tech Stack

- **Backend**: Python 3.9+, FastAPI, SQLAlchemy (SQLite/Postgres).
- **Frontend**: HTML5, Vanilla CSS3 (Custom Design System), Modern Javascript.
- **Deployment**: Vercel Serverless Functions.

## 🚀 Getting Started

### Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Ravi2405-143/badminton.git
   cd badminton
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**:
   ```bash
   python main.py
   ```
   The app will be live at `http://localhost:8000`.

## ☁️ Deployment

This project is ready for **Vercel**. Simply connect your GitHub repo to Vercel, set the root directory to `backend`, and deploy! 

> [!NOTE]
> See `DEPLOYMENT.md` for detailed instructions on setting up permanent data storage with Vercel Postgres.

## 📄 License
MIT License. Free to use and modify! 🏁🥇
