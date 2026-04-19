@echo off
echo 🛡️ AI-Driven Ransomware Detection System
echo ========================================
echo.
echo Starting the system...
echo.
echo 📊 Dashboard will open at: http://localhost:8501
echo 🔍 Detection system will run in this window
echo.
echo Press Ctrl+C to stop the system
echo.

REM Start Streamlit dashboard in background
start "Ransomware Dashboard" cmd /c "streamlit run app.py --server.port 8501 --server.headless false"

REM Wait a moment for dashboard to start
timeout /t 3 /nobreak > nul

REM Start the main detection system
python main.py

pause