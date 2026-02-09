from pathlib import Path
import shutil

file_category = {
    "pdf": "Documents",
    "docx": "Documents",
    "doc": "Documents",
    "xlsx": "Documents",
    "png": "Images",
    "mov": "Videos",
    "mp4": "Videos",
    "zip": "Archives"
}


unsorted_moved_count = 0
moved_count = 0
moved_files = []
duplicates = True

def get_file_category(file_path):
    return file_path.suffix.lstrip('.')
    
def enable_duplicates():
    while True:
        enable_duplicates_select = input("Allow sending of duplicate files or skipping of duplicate files ? y/n: ").lower()
        if enable_duplicates_select == "y":
            return True
        elif enable_duplicates_select == "n":
            return False
        else:
            print("Invalid selection. Try again")
        
        
def organize_extension(file_path):
    global moved_count, moved_files
    
    for extension in file_category:
        
        if extension == get_file_category(file_path):
            parent_folder = Path(file_path).parent
            child_folder = parent_folder / file_category[extension]
            child_folder.mkdir(parents=True, exist_ok=True)
            destination = child_folder / file_path.name
            if destination.exists():
                duplicate_select = enable_duplicates()
                if duplicate_select:
                    new_duplicate_file_no = 1
                    new_file = child_folder / f"{file_path.stem}_{new_duplicate_file_no}{file_path.suffix}"
                    while new_file.exists():
                        new_duplicate_file_no += 1
                        new_file = child_folder / f"{file_path.stem}_{new_duplicate_file_no}{file_path.suffix}"
                    moved_files.append(new_file)
                    moved_count += 1
                    duplicate_destination = new_file
                    shutil.move(file_path, duplicate_destination)
                    break
                else: 
                    print(f"{file_path.name} is a duplicate file. Skipping")
                    break
                
            moved_files.append(file_path.name)
            moved_count += 1
            shutil.move(file_path, destination)
            
            
def organize_extension_dry_run(file_path):
    for extension in file_category:
        if extension == get_file_category(file_path):
            parent_folder = Path(file_path).parent
            child_folder = parent_folder / file_category[extension]
            child_folder.mkdir(parents=True, exist_ok=True)
            destination = child_folder / file_path.name
            print(f"Will move {file_path.name} from {file_path} to {destination}")
            
    
def organize_by_type(source_folder, dry_run=False):
    files_path = [file.resolve() for file in source_folder.iterdir() if file.is_file()]
    if not dry_run: 
        for file_path in files_path:
            organize_extension(file_path)
        unsorted(source_folder)
            
    else:
        for file_path in files_path:
            organize_extension_dry_run(file_path)
        unsorted_dry_run(source_folder)
        while True:
            move_file_select = input("Move files ? y/n: ").lower()
            if move_file_select == "y":
                for file_path in files_path:
                    organize_extension(file_path)
                unsorted(source_folder)
                break
            elif move_file_select == "n":
                print("\nNo files moved")
                break
            else:
                print("Invalid Input. Try again")
    
def organize_by_date(source_folder, dry_run=False):
    pass
    
def display_summary(source_folder, moved_files, total_files_count):

    for file in moved_files:
        print(f"Moved {file}")
    print(f"Total of files in folder: {total_files_count} \nMoved a total of {moved_count} files")
    
def unsorted(source_folder):
    global moved_count, moved_files, duplicates
    
    unsorted_location = source_folder / "unsorted"
    unsorted_location.mkdir(parents=True, exist_ok=True)
    
    all_files = [f for f in source_folder.iterdir() if f.is_file()]
    
    for file_path in all_files:
        if file_path.name not in moved_files:
            unsorted_destination = unsorted_location / file_path.name
            if unsorted_destination.exists():
                if duplicates:
                    new_duplicate_file_no = 1
                    new_file = unsorted_location / f"{file_path.stem}_{new_duplicate_file_no}{file_path.suffix}"
                    while new_file.exists():
                        new_duplicate_file_no += 1
                        new_file = unsorted_location / f"{file_path.stem}_{new_duplicate_file_no}{file_path.suffix}"
                    moved_files.append(new_file)
                    moved_count += 1
                    unsorted_duplicate_destination = new_file
                    shutil.move(file_path, unsorted_duplicate_destination)
            else:
                moved_count += 1
                shutil.move(file_path, unsorted_destination)
    
        
def unsorted_dry_run(source_folder):
    global duplicates
    
    unsorted_location = source_folder / "unsorted"
    unsorted_location.mkdir(parents=True, exist_ok=True)
    
    all_files = [f for f in source_folder.iterdir() if f.is_file()]
    
    for file_path in all_files:
        if file_path.name not in moved_files:
            unsorted_destination = unsorted_location / file_path.name
            if unsorted_destination.exists():
                if duplicates:
                    new_duplicate_file_no = 1
                    new_file = unsorted_location / f"{file_path.stem}_{new_duplicate_file_no}{file_path.suffix}"
                    while new_file.exists():
                        new_duplicate_file_no += 1
                        new_file = unsorted_location / f"{file_path.stem}_{new_duplicate_file_no}{file_path.suffix}"
                    
                    unsorted_duplicate_destination = new_file
                    print(f"Will move {file_path.name} from {file_path} to {unsorted_duplicate_destination}")
            else:
                print(f"Will move {file_path.name} from {file_path} to {unsorted_destination}")    
                

def main():
    source_folder = Path(input("Enter location of folder to sort: "))
    total_files_count = len([file for file in source_folder.iterdir() if file.is_file()])
    while True: 
        dry_run_select = input("Display files to be moved or move directly ? y/n: ").lower()
        if dry_run_select == "y":
            organize_by_type(source_folder, dry_run=True)
            break
        elif dry_run_select == "n":
            organize_by_type(source_folder, dry_run=False)
            break
        else:
            print("Invalid selection. Try again")
    
    display_summary(source_folder, moved_files, total_files_count)
    
if __name__ == "__main__":
    main()