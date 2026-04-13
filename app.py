from flask import Flask
from flask_cors import CORS
from config import Config
from routes.dashboard import dashboard_bp
from routes.progress import progress_bp
from routes.ai import ai_bp
from routes.audio import audio_bp

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS for frontend communication
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(dashboard_bp, url_prefix='/api')
    app.register_blueprint(progress_bp, url_prefix='/api')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    app.register_blueprint(audio_bp, url_prefix='/api')
    
    @app.route('/')
    def index():
        return {
            'message': 'VibeRehab Backend API',
            'version': '1.0.0',
            'status': 'running'
        }
    
    @app.route('/health')
    def health():
        return {'status': 'healthy'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )

