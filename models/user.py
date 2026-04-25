"""
User model - MongoDB schema
In production, this would define the user document structure
"""

from typing import List, Dict

class User:
    """User model for MongoDB"""
    
    def __init__(self, user_id: str, name: str, overall_progress: float = 0.0):
        self.user_id = user_id
        self.name = name
        self.overall_progress = overall_progress
    
    def to_dict(self) -> Dict:
        """Convert user to dictionary for API responses"""
        return {
            "userId": self.user_id,
            "name": self.name,
            "overallProgress": self.overall_progress
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'User':
        """Create User from dictionary"""
        return User(
            user_id=data.get('userId'),
            name=data.get('name'),
            overall_progress=data.get('overallProgress', 0.0)
        )


class Task:
    """Task model for MongoDB"""
    
    def __init__(self, task_id: int, label: str, icon: str, completed: bool = False):
        self.task_id = task_id
        self.label = label
        self.icon = icon
        self.completed = completed
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary for API responses"""
        return {
            "id": self.task_id,
            "label": self.label,
            "icon": self.icon,
            "completed": self.completed
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Task':
        """Create Task from dictionary"""
        return Task(
            task_id=data.get('id'),
            label=data.get('label'),
            icon=data.get('icon'),
            completed=data.get('completed', False)
        )

