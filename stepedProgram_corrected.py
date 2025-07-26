
import os
import shutil
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('file_organizer.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def categorize_file(filepath):
    filename, extension = os.path.splitext(filepath)
    categories = {
        ".jpg": "images",
        ".jpeg": "images",
        ".png": "images",
        ".gif": "images",
        ".bmp": "images",
        ".svg": "images",
        ".pdf": "pdf",
        ".docx": "documents",
        ".doc": "documents",
        ".txt": "documents",
        ".pptx": "ppt",
        ".ppt": "ppt",
        ".mp4": "videos",
        ".avi": "videos",
        ".mkv": "videos",
        ".mov": "videos",
        ".exe": "apps",
        ".msi": "apps"
    }
    return categories.get(extension.lower(), "other")

def create_folders(directory):
    folders = ["images", "documents", "videos", "other", "apps", "pdf", "ppt"]
    for folder in folders:
        try:
            os.makedirs(os.path.join(directory, folder), exist_ok=True)
            logging.info(f"Ensured folder exists: {os.path.join(directory, folder)}")
        except Exception as e:
            logging.error(f"Error creating folder '{folder}': {e}")

def sort_files(source_directory, target_directory, summary):
    for root, _, files in os.walk(source_directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_category = categorize_file(filename)
            target_path = os.path.join(target_directory, file_category, filename)
            try:
                shutil.copy2(filepath, target_path)
                file_date = datetime.fromtimestamp(os.path.getmtime(filepath))
                sanitized_date = file_date.isoformat().replace(":", "-")
                new_filename = f"{sanitized_date}-{filename}"
                final_path = os.path.join(os.path.dirname(target_path), new_filename)
                os.rename(target_path, final_path)
                logging.info(f"Moved '{filepath}' to '{final_path}'")
                summary['organized'] += 1
            except Exception as e:
                logging.error(f"Error moving '{filepath}': {e}")
                summary['errors'] += 1

def main():
    source_directories = input("Enter source directories (comma-separated): ").split(",")
    source_directories = [d.strip() for d in source_directories if d.strip()]
    target_directory = input("Enter the destination directory: ").strip()

    create_folders(target_directory)
    total_files = 0
    summary = {'organized': 0, 'errors': 0}

    for src_dir in source_directories:
        if not os.path.isdir(src_dir):
            logging.error(f"Source directory does not exist: {src_dir}")
            continue
        logging.info(f"Processing directory: {src_dir}")
        for _, _, files in os.walk(src_dir):
            total_files += len(files)
        sort_files(src_dir, target_directory, summary)

    logging.info(f"File organization completed! {summary['organized']} files organized, {summary['errors']} errors.")
    print(f"File organization completed! {summary['organized']} files organized, {summary['errors']} errors. See 'file_organizer.log' for details.")

if __name__ == "__main__":
    main()
