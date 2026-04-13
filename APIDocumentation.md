### Core API Endpoints

1. **Dashboard Data** - `GET /api/dashboard`
   - Returns user profile and daily task plan
   - Mock data for prototype phase

2. **Task Completion** - `POST /api/progress/complete/{taskId}`
   - Marks tasks as complete
   - Updates overall progress

3. **AI Vibe Story** - `GET /api/ai/vibestory`
   - Generates daily inspirational stories using ChatGPT
   - Optimized for text-to-speech output

4. **AI Schedule Generator** - `POST /api/ai/generateschedule`
   - Creates personalized task schedules
   - Uses ChatGPT JSON mode for structured output

**Run the application:**
   ```bash
   python app.py
   ```

The server will start on `http://localhost:5000`

## API Documentation

### 1. Dashboard Endpoint

**Request:**
```
GET /api/dashboard
```

**Response:**
```json
{
  "user": {
    "name": "Alex",
    "overallProgress": 0.25
  },
  "dailyPlan": [
    {
      "id": 1,
      "label": "Morning Meditation",
      "icon": "ph-leaf",
      "completed": true
    },
    {
      "id": 2,
      "label": "Knee Stretches",
      "icon": "ph-person-simple-run",
      "completed": false
    }
  ]
}
```

### 2. Complete Task Endpoint

**Request:**
```
POST /api/progress/complete/2
```

**Response:**
```json
{
  "success": true,
  "taskId": 2,
  "newOverallProgress": 0.26,
  "message": "Task 2 marked as complete"
}
```

### 3. AI Vibe Story Endpoint

**Request:**
```
GET /api/ai/vibestory
```

**Response:**
```json
{
  "storyText": "Today is a new chapter. Focus not on the mountain top, but on the single, steady step...",
  "success": true
}
```

### 4. AI Schedule Generator Endpoint

**Request:**
```
POST /api/ai/generateschedule
Content-Type: application/json

{
  "tasks": ["Knee Stretches", "10-min Walk", "Check Posture"]
}
```

**Response:**
```json
{
  "schedule": [
    { "time": "11:00 AM", "task": "Check Posture" },
    { "time": "1:00 PM", "task": "Knee Stretches" },
    { "time": "3:00 PM", "task": "Check Posture" },
    { "time": "5:00 PM", "task": "10-min Walk" },
    { "time": "7:00 PM", "task": "Check Posture" }
  ],
  "success": true
}
```