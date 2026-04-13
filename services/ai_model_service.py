"""
Fine-tuned AI Model Service
Handles integration with custom fine-tuned models for text and audio generation
"""

import json
import requests
from typing import Dict, Tuple, Optional
from config import Config
import time

class FineTunedModelService:
    """Service for interacting with fine-tuned AI models"""
    
    def __init__(self, model_endpoint: str = None):
        """
        Initialize the fine-tuned model service
        
        Args:
            model_endpoint: URL endpoint for the fine-tuned model API
        """
        self.model_endpoint = model_endpoint or Config.MODEL_ENDPOINT
        self.api_key = Config.MODEL_API_KEY
        
    def generate_story(self, context: Dict) -> Tuple[str, Optional[bytes]]:
        """
        Generate inspirational story using fine-tuned model
        
        Args:
            context: Dictionary with user context (e.g., progress, mood, tasks)
            
        Returns:
            Tuple of (text_output, audio_output)
            - text_output: Generated story text
            - audio_output: Audio bytes (WAV/MP3) or None
        """
        try:
            # Prepare request payload for fine-tuned model
            payload = {
                "task": "story_generation",
                "context": context,
                "parameters": {
                    "max_length": 150,
                    "temperature": 0.8,
                    "output_format": "both"  # text and audio
                }
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # Call fine-tuned model API
            response = requests.post(
                f"{self.model_endpoint}/generate",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                text_output = result.get('text', '')
                
                # Audio is returned as base64 or direct bytes
                audio_data = result.get('audio')
                audio_bytes = None
                
                if audio_data:
                    if isinstance(audio_data, str):
                        # If base64 encoded
                        import base64
                        audio_bytes = base64.b64decode(audio_data)
                    else:
                        # If direct bytes
                        audio_bytes = audio_data
                
                return text_output, audio_bytes
            else:
                raise Exception(f"Model API returned status {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            # Fallback to mock data if model is unavailable
            print(f"Model API unavailable: {e}. Using fallback.")
            return self._generate_fallback_story(context)
        except Exception as e:
            raise Exception(f"Failed to generate story: {str(e)}")
    
    def generate_schedule(self, tasks: list, user_profile: Dict = None) -> Dict:
        """
        Generate task schedule using fine-tuned model
        
        Args:
            tasks: List of task names to schedule
            user_profile: Optional user profile data for personalization
            
        Returns:
            Dictionary with schedule data and metadata
        """
        try:
            payload = {
                "task": "schedule_generation",
                "tasks": tasks,
                "user_profile": user_profile or {},
                "parameters": {
                    "current_time": "9:00 AM",
                    "scheduling_rules": {
                        "recurring_tasks": ["Check Posture"],
                        "preferred_times": {
                            "walk": "afternoon",
                            "stretches": "after_sitting"
                        }
                    }
                }
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            response = requests.post(
                f"{self.model_endpoint}/generate",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                schedule = result.get('schedule', [])
                
                # Validate schedule structure
                for item in schedule:
                    if 'time' not in item or 'task' not in item:
                        raise ValueError("Invalid schedule format from model")
                
                return {
                    "schedule": schedule,
                    "metadata": result.get('metadata', {}),
                    "confidence": result.get('confidence', 0.0)
                }
            else:
                raise Exception(f"Model API returned status {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"Model API unavailable: {e}. Using fallback.")
            return self._generate_fallback_schedule(tasks)
        except Exception as e:
            raise Exception(f"Failed to generate schedule: {str(e)}")
    
    def _generate_fallback_story(self, context: Dict) -> Tuple[str, None]:
        """Fallback story generation when model is unavailable"""
        stories = [
            "Today is a new chapter. Focus not on the mountain top, but on the single, steady step. "
            "Every small movement forward is progress. Your body is healing, and patience is your greatest strength.",
            
            "Like a river carving through stone, your consistent effort shapes your recovery. "
            "Celebrate the small victories - they are the building blocks of transformation.",
            
            "Recovery is not a race, it's a journey of rediscovery. Each stretch, each breath, "
            "each mindful moment brings you closer to the version of yourself you're becoming."
        ]
        
        # Simple rotation based on time
        index = int(time.time()) % len(stories)
        return stories[index], None
    
    def _generate_fallback_schedule(self, tasks: list) -> Dict:
        """Fallback schedule generation when model is unavailable"""
        schedule = []
        current_hour = 11
        
        for task in tasks:
            if "posture" in task.lower():
                # Add multiple posture checks
                for i in range(3):
                    schedule.append({
                        "time": f"{current_hour + (i * 2)}:00 AM" if current_hour + (i * 2) < 12 else f"{current_hour + (i * 2) - 12}:00 PM",
                        "task": task
                    })
            elif "walk" in task.lower():
                schedule.append({"time": "5:00 PM", "task": task})
            else:
                schedule.append({
                    "time": f"{current_hour}:00 AM" if current_hour < 12 else f"{current_hour - 12}:00 PM",
                    "task": task
                })
                current_hour += 2
        
        return {
            "schedule": schedule,
            "metadata": {"source": "fallback"},
            "confidence": 0.5
        }

