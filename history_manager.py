import os
import json
import pandas as pd
from datetime import datetime
from typing import List, Dict

class TestCaseHistory:
    """Manages history of generated test cases"""
    
    def __init__(self, history_file="testcases/history.json"):
        self.history_file = history_file
        self.ensure_history_file_exists()
    
    def ensure_history_file_exists(self):
        """Create history file if it doesn't exist"""
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        if not os.path.exists(self.history_file):
            self.save_history([])
    
    def load_history(self) -> List[Dict]:
        """Load history from JSON file"""
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_history(self, history: List[Dict]):
        """Save history to JSON file"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    
    def add_entry(self, jira_ticket: str, priority: str, acceptance_criteria: str, 
                  file_path: str, provider: str, component: str = "Web Application", 
                  test_type: str = "Functional"):
        """Add a new entry to history"""
        history = self.load_history()
        
        # Get file size
        file_size = 0
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
        
        entry = {
            "id": len(history) + 1,
            "jira_ticket": jira_ticket,
            "priority": priority,
            "acceptance_criteria": acceptance_criteria,
            "file_path": file_path,
            "file_name": os.path.basename(file_path),
            "file_size": file_size,
            "provider": provider,
            "component": component,
            "test_type": test_type,
            "created_date": datetime.now().isoformat(),
            "created_timestamp": datetime.now().timestamp()
        }
        
        history.append(entry)
        self.save_history(history)
        return entry
    
    def get_all_entries(self) -> List[Dict]:
        """Get all history entries, sorted by creation date (newest first)"""
        history = self.load_history()
        return sorted(history, key=lambda x: x.get('created_timestamp', 0), reverse=True)
    
    def get_entry_by_id(self, entry_id: int) -> Dict:
        """Get a specific entry by ID"""
        history = self.load_history()
        for entry in history:
            if entry.get('id') == entry_id:
                return entry
        return None
    
    def delete_entry(self, entry_id: int) -> bool:
        """Delete an entry by ID"""
        history = self.load_history()
        new_history = [entry for entry in history if entry.get('id') != entry_id]
        
        if len(new_history) < len(history):
            self.save_history(new_history)
            return True
        return False
    
    def get_stats(self) -> Dict:
        """Get statistics about the history"""
        history = self.load_history()
        
        if not history:
            return {
                "total_entries": 0,
                "total_files": 0,
                "providers_used": [],
                "most_recent": None
            }
        
        providers = list(set(entry.get('provider', 'unknown') for entry in history))
        total_size = sum(entry.get('file_size', 0) for entry in history)
        
        return {
            "total_entries": len(history),
            "total_files": len([e for e in history if os.path.exists(e.get('file_path', ''))]),
            "total_size": total_size,
            "providers_used": providers,
            "most_recent": max(history, key=lambda x: x.get('created_timestamp', 0))
        }
