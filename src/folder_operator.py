import os
import shutil
import mimetypes
from datetime import datetime
from collections import defaultdict
import re

class AIFolderOperator:
    def __init__(self, target_folder, folder_names, organization_method, min_items_per_folder=1):
        self.target_folder = target_folder
        self.subfolder_names = folder_names
        self.organization_method = organization_method
        self.min_items_per_subfolder = min_items_per_folder
        self.file_type_categories_map = {
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'],
            'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
            'audio': ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a'],
            'video': ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm'],
            'archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
            'code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php', '.rb', '.swift', '.go'],
            'executables': ['.exe', '.msi', '.app', '.dmg'],
        }
        self.file_size_thresholds = {
            'Large Files': 100 * 1024 * 1024,  # 100 MB
            'Medium Files': 10 * 1024 * 1024,  # 10 MB
            'Small Files': 0
        }

    def run(self):
        print(f"AI Folder Operator is running using {self.organization_method} method...")
        self.organize_files_into_subfolders()

    def organize_files_into_subfolders(self):
        file_distribution = defaultdict(list)
        for filename in os.listdir(self.target_folder):
            file_path = os.path.join(self.target_folder, filename)
            if os.path.isfile(file_path):
                if self.organization_method == "Filetype":
                    destination_subfolder = self.determine_subfolder_for_type(filename)
                elif self.organization_method == "Date":
                    destination_subfolder = self.determine_subfolder_for_date(file_path)
                else:  # Filesize method
                    destination_subfolder = self.determine_subfolder_for_size(file_path)
                file_distribution[destination_subfolder].append(file_path)

        # Handle minimum items per folder requirement
        other_files = []
        for subfolder, files in list(file_distribution.items()):
            if len(files) < self.min_items_per_subfolder:
                other_files.extend(files)
                del file_distribution[subfolder]

        if other_files:
            file_distribution['Other'].extend(other_files)

        for subfolder, files in file_distribution.items():
            self.create_folder_and_move_files(subfolder, files)

    def determine_subfolder_for_type(self, filename):
        _, file_extension = os.path.splitext(filename)
        file_extension = file_extension.lower()
        
        for category, extensions in self.file_type_categories_map.items():
            if file_extension in extensions:
                return self.find_matching_subfolder(category)

        mime_type, _ = mimetypes.guess_type(filename)
        if mime_type:
            general_type = mime_type.split('/')[0]
            return self.find_matching_subfolder(general_type)

        return self.find_matching_subfolder('other')

    def determine_subfolder_for_date(self, file_path):
        mod_time = os.path.getmtime(file_path)
        date = datetime.fromtimestamp(mod_time)
        year = date.strftime("%Y")
        month = date.strftime("%m")

        # Check for year-only match
        year_match = self.find_matching_subfolder(year)
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
            match = self.find_matching_subfolder(pattern)
            if match != pattern:
                return match

        # If no match found, return the full date string
        return f"{year}-{month}"

    def determine_subfolder_for_size(self, file_path):
        file_size = os.path.getsize(file_path)
        for category, size_limit in self.file_size_thresholds.items():
            if file_size >= size_limit:
                return self.find_matching_subfolder(category)
        return self.find_matching_subfolder('Small Files')

    def find_matching_subfolder(self, category):

        normalized_category = category.lower()
        lowercase_folders = [folder.lower() for folder in self.subfolder_names]

        #Check if category is exact match
        if normalized_category in lowercase_folders:
            return self.subfolder_names[lowercase_folders.index(normalized_category)]
        
        #Try for soft matches based on organization strategy
        for subfolder in self.subfolder_names:
            normalized_folder = subfolder.lower()

            if self.organization_method == "Date":
                if self.is_date_match(normalized_category, normalized_folder):
                    return subfolder
            elif normalized_category in normalized_folder or normalized_folder in normalized_category:
                return subfolder
        
        if 'other' in lowercase_folders:
            return self.subfolder_names[lowercase_folders.index('other')]
        elif self.subfolder_names:
            return self.subfolder_names[-1]
        
        #Return category if no match is found
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
        if self.organization_method !="Filetype" and self.organization_method !="Date": #Filesystems
            return list(self.file_size_thresholds.keys()) + ['Other']
        folder_counts = defaultdict(int)
        for filename in os.listdir(self.target_folder):
            file_path = os.path.join(self.target_folder, filename)
            if os.path.isfile(file_path):
                if self.organization_method == "Filetype":
                    folder_name = self.determine_subfolder_for_type(filename)
                elif self.organization_method == "Date":
                    folder_name = self.determine_subfolder_for_date(filename)
                folder_counts[folder_name] += 1

        return [folder for folder, count in folder_counts.items() if count >= self.min_items_per_subfolder] + ['Other']