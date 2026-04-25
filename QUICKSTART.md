# Quick Start Guide

Get the VibeRehab backend up and running in 5 minutes!

## Prerequisites

- Python 3.8+ installed

## Installation Steps

### 1. Set Up Virtual Environment

```powershell
# Create virtual environment
python -m venv venv
```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 3. Configure Environment


Edit .env with your text editor

For example
```
notepad .env
```

### 4. Run the Server

```powershell
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
```

### 5. Test the API

Open a new PowerShell window and run:

```powershell
# First activate the venv
# Install requests if needed
pip install requests

# Run tests
python test_api.py
```

## Quick API Tests

### Using PowerShell

```powershell
# Test health
Invoke-RestMethod -Uri "http://localhost:5000/health"

# Get dashboard
Invoke-RestMethod -Uri "http://localhost:5000/api/dashboard"

# Complete a task
Invoke-RestMethod -Uri "http://localhost:5000/api/progress/complete/2" -Method POST

# Generate story (requires OpenAI key)
Invoke-RestMethod -Uri "http://localhost:5000/api/ai/vibestory"

# Generate schedule (requires OpenAI key)
$body = @{tasks = @("Knee Stretches", "10-min Walk")} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5000/api/ai/generateschedule" -Method POST -Body $body -ContentType "application/json"
```

### Using Browser

Open these URLs in your browser:
- http://localhost:5000/ (API info)
- http://localhost:5000/health (Health check)
- http://localhost:5000/api/dashboard (Dashboard data)
- http://localhost:5000/api/ai/vibestory (Generate story)

## Troubleshooting

### Port 5000 Already in Use
- Change PORT in `.env` to another port (e.g., 5001)
- Or find and kill the process using port 5000

### Import Errors
- Ensure you're in the right directory
- Activate virtual environment
- Reinstall dependencies

## Next Steps

1. **Connect Frontend:** Update your frontend to call these endpoints
2. **Test AI Features:** Try generating stories and schedules
3. **Customize:** Modify prompts in `routes/ai.py` to change AI behavior
4. **Database:** Set up MongoDB for persistent storage

## Project Structure

```
C:\hackathon\
├── app.py              # Main application - start here
├── config.py           # Configuration settings
├── .env               # Your environment variables (create this)
├── routes/            # API endpoint handlers
├── services/          # Business logic (OpenAI integration)
├── models/            # Data models
└── utils/             # Helper utilities
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/api/dashboard` | Get user dashboard data |
| POST | `/api/progress/complete/{taskId}` | Mark task complete |
| GET | `/api/ai/vibestory` | Generate inspirational story |
| POST | `/api/ai/generateschedule` | Generate task schedule |


