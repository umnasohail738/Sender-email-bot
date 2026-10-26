
import os
import shutil
import logging
import time

logging.basicConfig(
    filename="file_organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

WATCH_DIRECTORY = os.path.expanduser("~/Downloads")
print(WATCH_DIRECTORY)

FILE_TYPES = {
    "Images": ["jpg", "jpeg", "png", "gif", "bmp", "tiff"],
    "Documents": ["doc", "docx", "pdf", "txt"],
    "Videos": ["mp4", "avi", "mkv", "mov"],
    "Spreadsheets": ["xls", "xlsx", "csv"],
    "Audio": ["mp3", "wav", "aac"],
    "Presentations": ["ppt", "pptx"],
    "Archives": ["zip", "rar", "tar", "gz", "7z"]
}


def organize_files(file_path, file_name, extension):
    folder_name = "Others"

    for category, extensions in FILE_TYPES.items():
        if extension in extensions:
            folder_name = category
            break

    dest_folder = os.path.join(WATCH_DIRECTORY, folder_name)

    try:
        os.makedirs(dest_folder, exist_ok=True)

        destination = os.path.join(dest_folder, file_name)

        # Avoid overwriting a file with the same name
        if os.path.exists(destination):
            logging.warning(
                f"Skipped {file_name}: destination already exists"
            )
            print(f"Skipped {file_name}: file already exists")
            return

        shutil.move(file_path, destination)

        logging.info(f"Moved {file_name} to {dest_folder}")
        print(f"Moved {file_name} to {dest_folder}")

    except Exception as e:
        logging.error(f"Error moving {file_name}: {e}")
        print(f"Error moving {file_name}: {e}")


def organize_existing_files():
    """Organize files already in the Downloads directory."""

    for file_name in os.listdir(WATCH_DIRECTORY):
        file_path = os.path.join(WATCH_DIRECTORY, file_name)

        if os.path.isfile(file_path):
            extension = os.path.splitext(file_name)[1][1:].lower()

            logging.info(
                f"Organizing {file_name}, extension: {extension}"
            )

            organize_files(file_path, file_name, extension)


def start_monitoring():
    """Continuously check the Downloads directory for new files."""

    already_processed = set(os.listdir(WATCH_DIRECTORY))

    logging.info(f"Started monitoring {WATCH_DIRECTORY}")
    print(f"Monitoring {WATCH_DIRECTORY} for new files...")

    try:
        while True:
            current_files = set(os.listdir(WATCH_DIRECTORY))
            new_files = current_files - already_processed

            for file_name in new_files:
                file_path = os.path.join(WATCH_DIRECTORY, file_name)

                if os.path.isfile(file_path):
                    extension = os.path.splitext(file_name)[1][1:].lower()

                    organize_files(file_path, file_name, extension)

            # Update after processing, including folders created by this script
            already_processed = set(os.listdir(WATCH_DIRECTORY))

            time.sleep(5)

    except KeyboardInterrupt:
        print("\nFile monitoring stopped.")
        logging.info("File monitoring stopped.")


if __name__ == "__main__":
    if os.path.isdir(WATCH_DIRECTORY):
        organize_existing_files()
        start_monitoring()
    else:
        print(f"Directory does not exist: {WATCH_DIRECTORY}")
        logging.error(f"Directory does not exist: {WATCH_DIRECTORY}")
