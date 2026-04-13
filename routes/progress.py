from flask import Blueprint, jsonify

progress_bp = Blueprint('progress', __name__)

@progress_bp.route('/progress/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    """
    POST /api/progress/complete/{taskId}
    Marks a daily task as complete.
    For the prototype, this returns a success message without persisting to database.
    
    In production, this would:
    1. Validate the task_id belongs to the user
    2. Update the task status in the database
    3. Recalculate overall progress
    """
    # Mock calculation - in production, fetch from DB
    # Assume 3 total tasks, and completing one adds ~0.33
    new_progress = 0.26  # This would be calculated based on actual task completion
    
    response = {
        "success": True,
        "taskId": task_id,
        "newOverallProgress": new_progress,
        "message": f"Task {task_id} marked as complete"
    }
    
    return jsonify(response), 200

