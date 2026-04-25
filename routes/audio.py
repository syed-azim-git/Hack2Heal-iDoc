"""
Audio serving routes
Handles audio file retrieval and management
"""

from flask import Blueprint, send_file, jsonify, request
from services.audio_handler import AudioHandler
from io import BytesIO

audio_bp = Blueprint('audio', __name__)

# Initialize audio handler
audio_handler = AudioHandler()

@audio_bp.route('/audio/<filename>', methods=['GET'])
def get_audio_file(filename):
    """
    GET /api/audio/{filename}
    Retrieve and stream an audio file
    
    Args:
        filename: Name of the audio file to retrieve
        
    Returns:
        Audio file stream or error
    """
    try:
        audio_data = audio_handler.get_audio(filename)
        
        if audio_data is None:
            return jsonify({
                "error": "Audio file not found",
                "filename": filename
            }), 404
        
        # Determine MIME type based on extension
        if filename.endswith('.wav'):
            mimetype = 'audio/wav'
        elif filename.endswith('.mp3'):
            mimetype = 'audio/mpeg'
        elif filename.endswith('.ogg'):
            mimetype = 'audio/ogg'
        else:
            mimetype = 'application/octet-stream'
        
        # Return audio file as stream
        return send_file(
            BytesIO(audio_data),
            mimetype=mimetype,
            as_attachment=False,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "filename": filename
        }), 500


@audio_bp.route('/audio/<filename>/info', methods=['GET'])
def get_audio_info(filename):
    """
    GET /api/audio/{filename}/info
    Get metadata about an audio file
    
    Returns:
        JSON with audio file metadata
    """
    try:
        info = audio_handler.get_audio_info(filename)
        
        if info is None:
            return jsonify({
                "error": "Audio file not found",
                "filename": filename
            }), 404
        
        return jsonify(info), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@audio_bp.route('/audio/list', methods=['GET'])
def list_audio_files():
    """
    GET /api/audio/list
    List all available audio files
    
    Query params:
        permanent_only: If true, only list permanent files
        
    Returns:
        JSON array of audio file metadata
    """
    try:
        permanent_only = request.args.get('permanent_only', 'false').lower() == 'true'
        files = audio_handler.list_audio_files(permanent_only=permanent_only)
        
        return jsonify({
            "files": files,
            "count": len(files)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@audio_bp.route('/audio/<filename>', methods=['DELETE'])
def delete_audio_file(filename):
    """
    DELETE /api/audio/{filename}
    Delete an audio file
    
    Returns:
        Success/error message
    """
    try:
        success = audio_handler.delete_audio(filename)
        
        if success:
            return jsonify({
                "success": True,
                "message": f"Audio file {filename} deleted",
                "filename": filename
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "Audio file not found",
                "filename": filename
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@audio_bp.route('/audio/cleanup', methods=['POST'])
def cleanup_temp_audio():
    """
    POST /api/audio/cleanup
    Clean up temporary audio files
    
    Request body (optional):
        {
            "max_age_hours": 24
        }
        
    Returns:
        Number of files deleted
    """
    try:
        data = request.get_json() or {}
        max_age_hours = data.get('max_age_hours', 24)
        
        deleted_count = audio_handler.cleanup_temp_files(max_age_hours=max_age_hours)
        
        return jsonify({
            "success": True,
            "deleted_count": deleted_count,
            "message": f"Cleaned up {deleted_count} temporary audio files"
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

