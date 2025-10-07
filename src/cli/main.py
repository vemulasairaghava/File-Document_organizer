import json
from src.services.file_service import FileService

class FileCLI:
    def __init__(self):
        self.service = FileService()

    def add_file(self):
        user_id = int(input("Enter User ID: "))
        name = input("Enter File Name: ")
        ftype = input("Enter File Type: ")
        size = int(input("Enter File Size (in bytes): "))
        category = input("Enter Category (optional): ") or None
        tags = input("Enter Tags (space-separated, optional): ").split()
        f = self.service.add_file(user_id, name, ftype, size, category, tags)
        print("File added:")
        print(json.dumps(f, indent=2))

    def list_files(self):
        user_id = int(input("Enter User ID: "))
        files = self.service.dao.list_files(user_id)
        print(json.dumps(files, indent=2))

    def search_files(self):
        user_id = int(input("Enter User ID: "))
        keyword = input("Enter search keyword: ")
        files = self.service.search_files(user_id, keyword)
        print(json.dumps(files, indent=2))

    def update_file(self):
        file_id = int(input("Enter File ID to update: "))
        name = input("Enter new File Name (leave blank to skip): ") or None
        category = input("Enter new Category (leave blank to skip): ") or None
        update_data = {}
        if name:
            update_data["file_name"] = name
        if category:
            update_data["category"] = category
        f = self.service.update_file(file_id, update_data)
        print("File updated:")
        print(json.dumps(f, indent=2))

    def delete_file(self):
        file_id = int(input("Enter File ID to delete: "))
        result = self.service.delete_file(file_id)
        print(result["message"])

    def menu(self):
        while True:
            print("\n--- File Organizer Menu ---")
            print("1. Add File")
            print("2. List Files")
            print("3. Search Files")
            print("4. Update File")
            print("5. Delete File")
            print("6. Exit")

            choice = input("Enter your choice (1-6): ").strip()
            if choice == "1":
                self.add_file()
            elif choice == "2":
                self.list_files()
            elif choice == "3":
                self.search_files()
            elif choice == "4":
                self.update_file()
            elif choice == "5":
                self.delete_file()
            elif choice == "6":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    FileCLI().menu()
