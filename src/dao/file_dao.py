from typing import List, Dict, Optional
from src.config import get_supabase

class FileDAO:
    def __init__(self):
        self.sb = get_supabase()

    def create_file(self, data: Dict) -> Optional[Dict]:
        self.sb.table("files").insert(data).execute()
        resp = self.sb.table("files").select("*").eq("file_name", data["file_name"]).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_file_by_id(self, file_id: int) -> Optional[Dict]:
        resp = self.sb.table("files").select("*").eq("file_id", file_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def list_files(self, user_id: int) -> List[Dict]:
        resp = self.sb.table("files").select("*").eq("user_id", user_id).execute()
        return resp.data or []

    def update_file(self, file_id: int, data: Dict) -> Optional[Dict]:
        self.sb.table("files").update(data).eq("file_id", file_id).execute()
        return self.get_file_by_id(file_id)

    def delete_file(self, file_id: int):
        self.sb.table("files").delete().eq("file_id", file_id).execute()
