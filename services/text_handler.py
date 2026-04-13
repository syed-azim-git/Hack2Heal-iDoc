"""
Text Output Handler
Manages text generation output, storage, and formatting
"""

import os
import uuid
import json
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime, timedelta

class TextHandler:
    """Handler for text output operations"""
    
    def __init__(self, storage_dir: str = "text_outputs"):
        """
        Initialize text handler
        
        Args:
            storage_dir: Directory to store text files
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        self.stories_dir = self.storage_dir / "stories"
        self.schedules_dir = self.storage_dir / "schedules"
        self.logs_dir = self.storage_dir / "logs"
        
        self.stories_dir.mkdir(exist_ok=True)
        self.schedules_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
    
    def save_story(self, story_text: str, metadata: Dict = None) -> Dict:
        """
        Save generated story text
        
        Args:
            story_text: The generated story text
            metadata: Additional metadata (user_id, context, etc.)
            
        Returns:
            Dictionary with file info and metadata
        """
        if not story_text:
            raise ValueError("No story text provided")
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"story_{timestamp}_{unique_id}.json"
        
        file_path = self.stories_dir / filename
        
        # Prepare data structure
        data = {
            "id": unique_id,
            "text": story_text,
            "word_count": len(story_text.split()),
            "char_count": len(story_text),
            "created_at": datetime.now().isoformat(),
            "metadata": metadata or {},
            "type": "story"
        }
        
        # Save to file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return {
            "id": unique_id,
            "filename": filename,
            "path": str(file_path),
            "text": story_text,
            "word_count": data["word_count"],
            "char_count": data["char_count"],
            "created_at": data["created_at"]
        }
    
    def save_schedule(self, schedule: List[Dict], metadata: Dict = None) -> Dict:
        """
        Save generated schedule
        
        Args:
            schedule: List of scheduled tasks with time and task fields
            metadata: Additional metadata
            
        Returns:
            Dictionary with file info and metadata
        """
        if not schedule:
            raise ValueError("No schedule data provided")
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"schedule_{timestamp}_{unique_id}.json"
        
        file_path = self.schedules_dir / filename
        
        # Prepare data structure
        data = {
            "id": unique_id,
            "schedule": schedule,
            "task_count": len(schedule),
            "created_at": datetime.now().isoformat(),
            "metadata": metadata or {},
            "type": "schedule"
        }
        
        # Save to file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return {
            "id": unique_id,
            "filename": filename,
            "path": str(file_path),
            "schedule": schedule,
            "task_count": data["task_count"],
            "created_at": data["created_at"]
        }
    
    def get_story(self, story_id: str) -> Optional[Dict]:
        """
        Retrieve a saved story by ID
        
        Args:
            story_id: Unique story identifier
            
        Returns:
            Story data or None if not found
        """
        for file_path in self.stories_dir.glob(f"story_*_{story_id}.json"):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return None
    
    def get_schedule(self, schedule_id: str) -> Optional[Dict]:
        """
        Retrieve a saved schedule by ID
        
        Args:
            schedule_id: Unique schedule identifier
            
        Returns:
            Schedule data or None if not found
        """
        for file_path in self.schedules_dir.glob(f"schedule_*_{schedule_id}.json"):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return None
    
    def list_stories(self, limit: int = 10) -> List[Dict]:
        """
        List recent stories
        
        Args:
            limit: Maximum number of stories to return
            
        Returns:
            List of story metadata
        """
        stories = []
        
        for file_path in sorted(self.stories_dir.glob("story_*.json"), reverse=True):
            if len(stories) >= limit:
                break
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                stories.append({
                    "id": data["id"],
                    "text_preview": data["text"][:100] + "..." if len(data["text"]) > 100 else data["text"],
                    "word_count": data["word_count"],
                    "created_at": data["created_at"]
                })
        
        return stories
    
    def list_schedules(self, limit: int = 10) -> List[Dict]:
        """
        List recent schedules
        
        Args:
            limit: Maximum number of schedules to return
            
        Returns:
            List of schedule metadata
        """
        schedules = []
        
        for file_path in sorted(self.schedules_dir.glob("schedule_*.json"), reverse=True):
            if len(schedules) >= limit:
                break
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                schedules.append({
                    "id": data["id"],
                    "task_count": data["task_count"],
                    "created_at": data["created_at"]
                })
        
        return schedules
    
    def format_for_speech(self, text: str) -> str:
        """
        Format text for better text-to-speech output
        
        Args:
            text: Raw text
            
        Returns:
            Formatted text optimized for TTS
        """
        # Add pauses with punctuation
        formatted = text.replace(". ", "... ")
        formatted = formatted.replace("! ", "!.. ")
        formatted = formatted.replace("? ", "?.. ")
        
        # Remove special characters that might confuse TTS
        formatted = formatted.replace("*", "")
        formatted = formatted.replace("_", "")
        
        return formatted
    
    def log_generation(self, generation_type: str, success: bool, 
                       metadata: Dict = None) -> None:
        """
        Log text generation events
        
        Args:
            generation_type: Type of generation (story, schedule)
            success: Whether generation was successful
            metadata: Additional context
        """
        timestamp = datetime.now().strftime("%Y%m%d")
        log_file = self.logs_dir / f"generation_log_{timestamp}.json"
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": generation_type,
            "success": success,
            "metadata": metadata or {}
        }
        
        # Append to log file
        logs = []
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        
        logs.append(log_entry)
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
    
    def cleanup_old_files(self, max_age_days: int = 30) -> Dict[str, int]:
        """
        Clean up old text files
        
        Args:
            max_age_days: Maximum age in days before deletion
            
        Returns:
            Dictionary with count of deleted files by type
        """
        cutoff_time = datetime.now() - timedelta(days=max_age_days)
        deleted = {"stories": 0, "schedules": 0, "logs": 0}
        
        for directory, key in [(self.stories_dir, "stories"), 
                               (self.schedules_dir, "schedules"),
                               (self.logs_dir, "logs")]:
            for file_path in directory.glob("*.json"):
                if file_path.is_file():
                    modified_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if modified_time < cutoff_time:
                        file_path.unlink()
                        deleted[key] += 1
        
        return deleted

