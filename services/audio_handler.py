"""
Audio Output Handler
Manages audio file generation, storage, and serving
"""

import os
import uuid
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime, timedelta
import base64

class AudioHandler:
    """Handler for audio file operations"""
    
    def __init__(self, storage_dir: str = "audio_outputs"):
        """
        Initialize audio handler
        
        Args:
            storage_dir: Directory to store audio files
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        self.temp_dir = self.storage_dir / "temp"
        self.permanent_dir = self.storage_dir / "permanent"
        self.temp_dir.mkdir(exist_ok=True)
        self.permanent_dir.mkdir(exist_ok=True)
        
    def save_audio(self, audio_data: bytes, filename: str = None, 
                   permanent: bool = False, format: str = "wav") -> Dict:
        """
        Save audio data to file
        
        Args:
            audio_data: Raw audio bytes
            filename: Optional custom filename
            permanent: If True, save to permanent storage, else temp
            format: Audio format (wav, mp3, ogg)
            
        Returns:
            Dictionary with file info (path, url, metadata)
        """
        if not audio_data:
            raise ValueError("No audio data provided")
        
        # Generate unique filename
        if not filename:
            unique_id = str(uuid.uuid4())
            filename = f"audio_{unique_id}.{format}"
        elif not filename.endswith(f".{format}"):
            filename = f"{filename}.{format}"
        
        # Determine storage location
        target_dir = self.permanent_dir if permanent else self.temp_dir
        file_path = target_dir / filename
        
        # Write audio data
        with open(file_path, 'wb') as f:
            f.write(audio_data)
        
        # Create metadata
        file_size = len(audio_data)
        created_at = datetime.now().isoformat()
        
        metadata = {
            "filename": filename,
            "path": str(file_path),
            "relative_path": f"audio_outputs/{'permanent' if permanent else 'temp'}/{filename}",
            "url": f"/api/audio/{filename}",
            "format": format,
            "size_bytes": file_size,
            "size_kb": round(file_size / 1024, 2),
            "created_at": created_at,
            "permanent": permanent
        }
        
        return metadata
    
    def get_audio(self, filename: str) -> Optional[bytes]:
        """
        Retrieve audio file data
        
        Args:
            filename: Name of the audio file
            
        Returns:
            Audio bytes or None if not found
        """
        # Check both directories
        for directory in [self.temp_dir, self.permanent_dir]:
            file_path = directory / filename
            if file_path.exists():
                with open(file_path, 'rb') as f:
                    return f.read()
        
        return None
    
    def get_audio_info(self, filename: str) -> Optional[Dict]:
        """
        Get metadata about an audio file
        
        Args:
            filename: Name of the audio file
            
        Returns:
            Metadata dictionary or None if not found
        """
        for directory in [self.temp_dir, self.permanent_dir]:
            file_path = directory / filename
            if file_path.exists():
                stats = file_path.stat()
                return {
                    "filename": filename,
                    "path": str(file_path),
                    "size_bytes": stats.st_size,
                    "size_kb": round(stats.st_size / 1024, 2),
                    "created_at": datetime.fromtimestamp(stats.st_ctime).isoformat(),
                    "modified_at": datetime.fromtimestamp(stats.st_mtime).isoformat(),
                    "exists": True
                }
        
        return None
    
    def delete_audio(self, filename: str) -> bool:
        """
        Delete an audio file
        
        Args:
            filename: Name of the audio file
            
        Returns:
            True if deleted, False if not found
        """
        for directory in [self.temp_dir, self.permanent_dir]:
            file_path = directory / filename
            if file_path.exists():
                file_path.unlink()
                return True
        
        return False
    
    def cleanup_temp_files(self, max_age_hours: int = 24) -> int:
        """
        Clean up temporary audio files older than specified age
        
        Args:
            max_age_hours: Maximum age in hours before deletion
            
        Returns:
            Number of files deleted
        """
        deleted_count = 0
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        for file_path in self.temp_dir.glob("*.wav"):
            if file_path.is_file():
                modified_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if modified_time < cutoff_time:
                    file_path.unlink()
                    deleted_count += 1
        
        for file_path in self.temp_dir.glob("*.mp3"):
            if file_path.is_file():
                modified_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if modified_time < cutoff_time:
                    file_path.unlink()
                    deleted_count += 1
        
        return deleted_count
    
    def list_audio_files(self, permanent_only: bool = False) -> list:
        """
        List all audio files
        
        Args:
            permanent_only: If True, only list permanent files
            
        Returns:
            List of file metadata dictionaries
        """
        files = []
        
        directories = [self.permanent_dir] if permanent_only else [self.temp_dir, self.permanent_dir]
        
        for directory in directories:
            for file_path in directory.glob("*.*"):
                if file_path.suffix.lower() in ['.wav', '.mp3', '.ogg']:
                    stats = file_path.stat()
                    files.append({
                        "filename": file_path.name,
                        "path": str(file_path),
                        "size_kb": round(stats.st_size / 1024, 2),
                        "created_at": datetime.fromtimestamp(stats.st_ctime).isoformat(),
                        "permanent": directory == self.permanent_dir
                    })
        
        return sorted(files, key=lambda x: x['created_at'], reverse=True)
    
    def audio_to_base64(self, audio_data: bytes) -> str:
        """
        Convert audio bytes to base64 string for API responses
        
        Args:
            audio_data: Raw audio bytes
            
        Returns:
            Base64 encoded string
        """
        return base64.b64encode(audio_data).decode('utf-8')
    
    def base64_to_audio(self, base64_string: str) -> bytes:
        """
        Convert base64 string to audio bytes
        
        Args:
            base64_string: Base64 encoded audio
            
        Returns:
            Raw audio bytes
        """
        return base64.b64decode(base64_string)

