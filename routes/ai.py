from flask import Blueprint, jsonify, request
from services.ai_model_service import FineTunedModelService
from services.audio_handler import AudioHandler
from services.text_handler import TextHandler

ai_bp = Blueprint('ai', __name__)

# Initialize services
model_service = FineTunedModelService()
audio_handler = AudioHandler()
text_handler = TextHandler()

@ai_bp.route('/vibestory', methods=['GET'])
def generate_vibe_story():
    """
    GET /api/ai/vibestory
    Generates a unique, inspirational story with text and optional audio output.
    
    Query params:
        include_audio: If true, also returns audio file URL
        save_audio: If true, saves audio permanently
    
    Returns:
        JSON with storyText, optional audioUrl, and metadata
    """
    try:
        # Get query parameters
        include_audio = request.args.get('include_audio', 'true').lower() == 'true'
        save_audio_permanent = request.args.get('save_audio', 'false').lower() == 'true'
        
        # Prepare context for model
        context = {
            "user_type": "rehabilitation_patient",
            "content_type": "inspirational_story",
            "max_words": 100,
            "themes": ["patience", "resilience", "small_victories"]
        }
        
        # Generate story using fine-tuned model
        story_text, audio_data = model_service.generate_story(context)
        
        # Save text output
        text_info = text_handler.save_story(story_text, metadata=context)
        
        # Log generation
        text_handler.log_generation("story", True, {"story_id": text_info["id"]})
        
        response = {
            "storyText": story_text,
            "storyId": text_info["id"],
            "wordCount": text_info["word_count"],
            "success": True
        }
        
        # Handle audio if available and requested
        if include_audio and audio_data:
            audio_info = audio_handler.save_audio(
                audio_data, 
                filename=f"story_{text_info['id']}",
                permanent=save_audio_permanent,
                format="wav"
            )
            response["audioUrl"] = audio_info["url"]
            response["audioFilename"] = audio_info["filename"]
            response["audioSize"] = audio_info["size_kb"]
        
        return jsonify(response), 200
        
    except Exception as e:
        text_handler.log_generation("story", False, {"error": str(e)})
        return jsonify({
            "error": str(e),
            "success": False,
            "storyText": "Unable to generate story at this time. Remember: every small step counts."
        }), 500


@ai_bp.route('/generateschedule', methods=['POST'])
def generate_schedule():
    """
    POST /api/ai/generateschedule
    Generates a customized reminder schedule based on pending tasks using fine-tuned model.
    
    Expected request body:
    {
        "tasks": ["Knee Stretches", "10-min Walk", "Check Posture"],
        "user_profile": {  // optional
            "preferred_wake_time": "8:00 AM",
            "activity_level": "moderate"
        }
    }
    
    Returns:
        JSON with schedule array, metadata, and confidence score
    """
    try:
        data = request.get_json()
        
        if not data or 'tasks' not in data:
            return jsonify({
                "error": "Missing 'tasks' field in request body",
                "success": False
            }), 400
        
        tasks = data['tasks']
        user_profile = data.get('user_profile', {})
        
        if not isinstance(tasks, list) or len(tasks) == 0:
            return jsonify({
                "error": "Tasks must be a non-empty array",
                "success": False
            }), 400
        
        # Generate schedule using fine-tuned model
        result = model_service.generate_schedule(tasks, user_profile)
        
        # Save schedule output
        schedule_info = text_handler.save_schedule(
            result['schedule'], 
            metadata={
                "tasks": tasks,
                "user_profile": user_profile,
                "confidence": result.get('confidence', 0.0)
            }
        )
        
        # Log generation
        text_handler.log_generation("schedule", True, {
            "schedule_id": schedule_info["id"],
            "task_count": len(tasks)
        })
        
        response = {
            "schedule": result['schedule'],
            "scheduleId": schedule_info["id"],
            "taskCount": schedule_info["task_count"],
            "confidence": result.get('confidence', 0.0),
            "metadata": result.get('metadata', {}),
            "success": True
        }
        
        return jsonify(response), 200
        
    except ValueError as e:
        text_handler.log_generation("schedule", False, {"error": str(e)})
        return jsonify({
            "error": f"Failed to parse schedule: {str(e)}",
            "success": False
        }), 500
    except Exception as e:
        text_handler.log_generation("schedule", False, {"error": str(e)})
        return jsonify({
            "error": str(e),
            "success": False
        }), 500

