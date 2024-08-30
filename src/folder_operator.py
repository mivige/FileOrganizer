import os
import shutil
import mimetypes
from datetime import datetime
from collections import defaultdict
import re

class AIFolderOperator:
    def __init__(self, target_folder, folder_names, organization_method, min_items_per_folder=1):
        self.target_folder = target_folder
        self.folder_names = folder_names
        self.organization_method = organization_method
        self.min_items_per_folder = min_items_per_folder
        self.file_type_categories = {
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'],
            'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
            'audio': ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a'],
            'video': ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm'],
            'archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
            'code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php', '.rb', '.swift', '.go'],
            'executables': ['.exe', '.msi', '.app', '.dmg'],
        }
        self.file_size_categories = {
            'Large Files': 100 * 1024 * 1024,  # 100 MB
            'Medium Files': 10 * 1024 * 1024,  # 10 MB
            'Small Files': 0
        }

    def run(self):
        print(f"AI Folder Operator is running using {self.organization_method} method...")
        self.organize_files()

    def organize_files(self):
        file_distribution = defaultdict(list)
        for filename in os.listdir(self.target_folder):
            file_path = os.path.join(self.target_folder, filename)
            if os.path.isfile(file_path):
                if self.organization_method == "Filetype":
                    destination_subfolder = self.decide_subfolder_by_type(filename)
                elif self.organization_method == "Date":
                    destination_subfolder = self.decide_subfolder_by_date(file_path)
                else:  # Filesize method
                    destination_subfolder = self.decide_subfolder_by_size(file_path)
                file_distribution[destination_subfolder].append(file_path)

        # Handle minimum items per folder requirement
        other_files = []
        for subfolder, files in list(file_distribution.items()):
            if len(files) < self.min_items_per_folder:
                other_files.extend(files)
                del file_distribution[subfolder]

        if other_files:
            file_distribution['Other'].extend(other_files)

        for subfolder, files in file_distribution.items():
            self.create_folder_and_move_files(subfolder, files)

    def decide_subfolder_by_type(self, filename):
        _, file_extension = os.path.splitext(filename)
        file_extension = file_extension.lower()

        for category, extensions in self.file_type_categories.items():
            if file_extension in extensions:
                return self.get_matching_folder(category)

        mime_type, _ = mimetypes.guess_type(filename)
        if mime_type:
            general_type = mime_type.split('/')[0]
            return self.get_matching_folder(general_type)

        return self.get_matching_folder('other')

    def decide_subfolder_by_date(self, file_path):
        mod_time = os.path.getmtime(file_path)
        date = datetime.fromtimestamp(mod_time)
        year = date.strftime("%Y")
        month = date.strftime("%m")

        # Check for year-only match
        year_match = self.get_matching_folder(year)
        if year_match != year:
            return year_match

        # Check for year-month match in various formats
        date_patterns = [
            f"{year}-{month}",
            f"{month}-{year}",
            f"{year}/{month}",
            f"{month}/{year}",
            f"{year}_{month}",
            f"{month}_{year}",
            f"{year}.{month}",
            f"{month}.{year}",
        ]

        for pattern in date_patterns:
            match = self.get_matching_folder(pattern)
            if match != pattern:
                return match

        # If no match found, return the full date string
        return f"{year}-{month}"

    def decide_subfolder_by_size(self, file_path):
        file_size = os.path.getsize(file_path)
        for category, size_limit in self.file_size_categories.items():
            if file_size >= size_limit:
                return self.get_matching_folder(category)
        return self.get_matching_folder('Small Files')

    def get_matching_folder(self, category):
        lowercase_folders = [folder.lower() for folder in self.folder_names]
        
        if category.lower() in lowercase_folders:
            return self.folder_names[lowercase_folders.index(category.lower())]
        
        for i, folder in enumerate(lowercase_folders):
            if self.organization_method == "Date":
                if self.is_date_match(category, folder):
                    return self.folder_names[i]
            elif category.lower() in folder or folder in category.lower():
                return self.folder_names[i]
        
        if 'other' in lowercase_folders:
            return self.folder_names[lowercase_folders.index('other')]
        elif self.folder_names:
            return self.folder_names[-1]
        else:
            return category

    def is_date_match(self, date_str, folder_name):
        # Extract year and month from date_str
        date_parts = re.split(r'[-/_.]+', date_str)
        if len(date_parts) == 2:
            year, month = date_parts if len(date_parts[0]) == 4 else date_parts[::-1]
        elif len(date_parts) == 1:
            year, month = date_parts[0], None
        else:
            return False

        # Check if folder_name contains the year
        if year in folder_name:
            return True
        
        # Check if folder_name contains both year and month in any order and with any separator
        if month:
            folder_parts = re.split(r'[-/_.]+', folder_name)
            return (year in folder_parts and month in folder_parts) or (month in folder_parts and year in folder_parts)

        return False

    def create_folder_and_move_files(self, subfolder, files):
        destination_path = os.path.join(self.target_folder, subfolder)
        os.makedirs(destination_path, exist_ok=True)
        for file_path in files:
            shutil.move(file_path, os.path.join(destination_path, os.path.basename(file_path)))
            print(f"Moved {os.path.basename(file_path)} to {subfolder}")

    def get_auto_folder_names(self):
        if self.organization_method == "Filetype":
            return self.get_auto_folder_names_by_type()
        elif self.organization_method == "Date":
            return self.get_auto_folder_names_by_date()
        else:  # Filesize method
            return self.get_auto_folder_names_by_size()

    def get_auto_folder_names_by_type(self):
        folder_counts = defaultdict(int)
        for filename in os.listdir(self.target_folder):
            file_path = os.path.join(self.target_folder, filename)
            if os.path.isfile(file_path):
                folder_name = self.decide_subfolder_by_type(filename)
                folder_counts[folder_name] += 1

        return [folder for folder, count in folder_counts.items() if count >= self.min_items_per_folder] + ['Other']

    def get_auto_folder_names_by_date(self):
        folder_counts = defaultdict(int)
        for filename in os.listdir(self.target_folder):
            file_path = os.path.join(self.target_folder, filename)
            if os.path.isfile(file_path):
                folder_name = self.decide_subfolder_by_date(file_path)
                folder_counts[folder_name] += 1

        return [folder for folder, count in folder_counts.items() if count >= self.min_items_per_folder] + ['Other']

    def get_auto_folder_names_by_size(self):
        return list(self.file_size_categories.keys()) + ['Other']
