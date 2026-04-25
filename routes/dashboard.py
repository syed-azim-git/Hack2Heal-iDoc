from flask import Blueprint, jsonify

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """
    GET /api/dashboard
    Fetches all data needed to render the main page for the logged-in user.
    For the prototype, this returns static mock data.
    """
    mock_data = {
        "user": {
            "name": "Alex",
            "overallProgress": 0.25
        },
        "dailyPlan": [
            {
                "id": 1,
                "label": "Morning Meditation",
                "icon": "ph-leaf",
                "completed": True
            },
            {
                "id": 2,
                "label": "Knee Stretches",
                "icon": "ph-person-simple-run",
                "completed": False
            },
            {
                "id": 3,
                "label": "10-min Walk",
                "icon": "ph-person-simple-walk",
                "completed": False
            }
        ]
    }
    
    return jsonify(mock_data), 200

