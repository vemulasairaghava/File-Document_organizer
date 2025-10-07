from typing import List, Dict
from src.dao.file_dao import FileDAO
from datetime import datetime

class FileServiceError(Exception):
    pass

class FileService:
    def __init__(self):
        self.dao = FileDAO()

    def add_file(self, user_id: int, file_name: str, file_type: str, file_size: int, category: str = None, tags: List[str] = None) -> Dict:
        data = {
            "user_id": user_id,
            "file_name": file_name,
            "file_type": file_type,
            "file_size": file_size,
            "category": category,
            "tags": tags,
            "upload_date": str(datetime.now())
        }
        return self.dao.create_file(data)

    def search_files(self, user_id: int, keyword: str) -> List[Dict]:
        files = self.dao.list_files(user_id)
        return [f for f in files if keyword.lower() in f["file_name"].lower()]

    def update_file(self, file_id: int, data: Dict) -> Dict:
        file = self.dao.get_file_by_id(file_id)
        if not file:
            raise FileServiceError("File not found")
        return self.dao.update_file(file_id, data)

    def delete_file(self, file_id: int):
        file = self.dao.get_file_by_id(file_id)
        if not file:
            raise FileServiceError("File not found")
        self.dao.delete_file(file_id)
        return {"message": "File deleted successfully"}
