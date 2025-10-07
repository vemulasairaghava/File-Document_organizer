import streamlit as st
from src.services.file_service import FileService, FileServiceError
from datetime import datetime
import os
import os
from dotenv import load_dotenv

load_dotenv() 
# Initialize service
service = FileService()

# Page title
st.set_page_config(page_title="📁 File / Document Organizer", layout="centered")
st.title("📁 File / Document Organizer (Supabase + Python OOP)")
st.write("Manage and organize your uploaded files easily.")

# Sidebar Menu
menu = st.sidebar.selectbox(
    "Menu",
    ["Upload File", "View Files", "Search Files", "Update File", "Delete File"]
)

# 1️⃣ UPLOAD FILE
if menu == "Upload File":
    st.header("📤 Upload a New File")

    user_id = st.number_input("Enter User ID", min_value=1, step=1)
    uploaded_file = st.file_uploader("Choose a file", type=None)

    category = st.text_input("Enter Category (optional)")
    tags = st.text_input("Enter Tags (space-separated)").split()

    if uploaded_file and st.button("Upload"):
        try:
            # Save temporarily to get path & size
            temp_path = f"/tmp/{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            file_size = os.path.getsize(temp_path)
            file_type = uploaded_file.type or "unknown"

            # Add file metadata to DB
            file_info = service.add_file(
                user_id=user_id,
                file_name=uploaded_file.name,
                file_type=file_type,
                file_size=file_size,
                category=category,
                tags=tags
            )
            st.success("✅ File uploaded successfully!")
            st.json(file_info)

        except FileServiceError as e:
            st.error(f"Error: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

# 2️⃣ VIEW FILES
elif menu == "View Files":
    st.header("📂 View Uploaded Files")
    user_id = st.number_input("Enter User ID", min_value=1, step=1)
    if st.button("Show Files"):
        files = service.dao.list_files(user_id)
        if files:
            st.success(f"Found {len(files)} files.")
            st.dataframe(files)
        else:
            st.warning("No files found for this user.")

# 3️⃣ SEARCH FILES
elif menu == "Search Files":
    st.header("🔍 Search Files")
    user_id = st.number_input("Enter User ID", min_value=1, step=1)
    keyword = st.text_input("Enter search keyword")

    if st.button("Search"):
        results = service.search_files(user_id, keyword)
        if results:
            st.success(f"Found {len(results)} matching files.")
            st.dataframe(results)
        else:
            st.warning("No matching files found.")

# 4️⃣ UPDATE FILE
elif menu == "Update File":
    st.header("✏️ Update File Details")

    file_id = st.number_input("Enter File ID", min_value=1, step=1)
    new_name = st.text_input("Enter new file name (leave blank to skip)")
    new_category = st.text_input("Enter new category (leave blank to skip)")

    if st.button("Update"):
        data = {}
        if new_name:
            data["file_name"] = new_name
        if new_category:
            data["category"] = new_category

        try:
            updated_file = service.update_file(file_id, data)
            st.success("✅ File updated successfully!")
            st.json(updated_file)
        except FileServiceError as e:
            st.error(f"Error: {e}")

# 5️⃣ DELETE FILE
elif menu == "Delete File":
    st.header("🗑️ Delete File")

    file_id = st.number_input("Enter File ID to delete", min_value=1, step=1)
    if st.button("Delete File"):
        try:
            result = service.delete_file(file_id)
            st.success(result["message"])
        except FileServiceError as e:
            st.error(f"Error: {e}")
