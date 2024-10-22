import zipfile
import os
import shutil
import difflib
from pathlib import Path

# ANSI escape codes for colors
RESET = "\033[0m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"

# Default keywords to search for
DEFAULT_KEYWORDS = [
    "isPro", "isPremium", "isVip", "isPurchased", "isActive",
    "isUser", "sharedPrefences", "pro", "premium", "vip",
    "lifetime", "purchased", "unlimited", "unlocked"
]

### UTILITY FUNCTIONS ###

def print_colored(text, color):
    """Prints text in the specified color."""
    print(f"{color}{text}{RESET}")

def unzip_file(zip_path, extract_dir):
    """Unzips a given zip file to the specified directory."""
    print_colored(f"Unzipping {zip_path}...", BLUE)
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
    except zipfile.BadZipFile:
        print_colored(f"Error: {zip_path} is not a valid zip file.", RED)

def cleanup_directories(*dirs):
    """Deletes the provided directories."""
    for directory in dirs:
        shutil.rmtree(directory, ignore_errors=True)

def color_diff_with_line(diff_line, line_num):
    """Highlights differences in unified diff output with line numbers."""
    if diff_line.startswith('-'):
        return f"{RED}{line_num}: {diff_line}{RESET}"
    elif diff_line.startswith('+'):
        return f"{GREEN}{line_num}: {diff_line}{RESET}"
    else:
        return f"{line_num}: {diff_line}"

### FILE COMPARISON FUNCTIONS ###

def find_class_file(directory, class_name):
    """Finds a specific class file by name in a given directory."""
    for smali_file in Path(directory).rglob('*.smali'):
        if smali_file.stem == class_name:
            return smali_file
    return None

def compare_class_files(class_file1, class_file2):
    """Compares two class files and highlights differences."""
    with open(class_file1, 'r', encoding='utf-8', errors='ignore') as f1, \
         open(class_file2, 'r', encoding='utf-8', errors='ignore') as f2:
         
        lines1 = f1.readlines()
        lines2 = f2.readlines()
        
        diff = difflib.ndiff(lines1, lines2)
        file_diff = [
            color_diff_with_line(line, idx + 1) 
            for idx, line in enumerate(diff) if line.startswith('-') or line.startswith('+')
        ]
        
        if file_diff:
            print_colored(f"Differences found between {class_file1.name} and {class_file2.name}:", BLUE)
            print("\n".join(file_diff))

def find_method_boundaries(lines):
    """Identifies method boundaries in a given list of lines."""
    method_boundaries = []
    current_method = None

    for index, line in enumerate(lines):
        if line.strip().startswith('.method'):
            current_method = index
        elif line.strip().startswith('.end method') and current_method is not None:
            method_boundaries.append((current_method, index))
            current_method = None

    return method_boundaries

def compare_methods(lines1, lines2, keyword, file):
    """Compares methods between two sets of lines and highlights differences."""
    method_boundaries1 = find_method_boundaries(lines1)
    method_boundaries2 = find_method_boundaries(lines2)

    for method1 in method_boundaries1:
        method_content1 = lines1[method1[0]:method1[1] + 1]
        method_name1 = method_content1[0].strip()

        if keyword in method_name1:
            for method2 in method_boundaries2:
                method_content2 = lines2[method2[0]:method2[1] + 1]
                method_name2 = method_content2[0].strip()

                if keyword in method_name2:
                    method_diff = difflib.ndiff(method_content1, method_content2)
                    file_diff = [
                        color_diff_with_line(line, method1[0] + idx + 1) 
                        for idx, line in enumerate(method_diff) if line.startswith('-') or line.startswith('+')
                    ]
                    if file_diff:
                        print_colored(f"Differences found in file: {file} (inside method '{keyword}')", BLUE)
                        print("\n".join(file_diff))
                        with open("differences.txt", "a") as f:
                            f.write(f"Differences found in file: {file} (inside method '{keyword}')")
                            f.write("\n".join(file_diff))

### DIRECTORY COMPARISON FUNCTIONS ###

def compare_directories(dir1, dir2, keyword, search_type):
    """Compares two directories for differences based on a keyword and search type."""
    print_colored(f"Comparing with keyword: '{keyword}', Search Type: '{search_type}'", YELLOW)
    
    # Get the relative file paths in both directories
    dir1_files = {f.relative_to(dir1) for f in Path(dir1).rglob('*') if f.is_file()}
    dir2_files = {f.relative_to(dir2) for f in Path(dir2).rglob('*') if f.is_file()}
    
    # Find the common files between both directories
    common_files = dir1_files & dir2_files
    differences_found = False

    if search_type == "class":
        # Find class files for the given keyword in both directories
        class_file1 = find_class_file(dir1, keyword)
        class_file2 = find_class_file(dir2, keyword)

        if class_file1 and class_file2:
            # Compare the class files only once and check for differences
            compare_class_files(class_file1, class_file2)
            differences_found = True
        else:
            print_colored(f"Class '{keyword}' not found in one or both directories.", RED)
            return

    else:
        # Loop through the common files and compare based on the search type
        for file in common_files:
            file1 = Path(dir1) / file
            file2 = Path(dir2) / file

            with open(file1, 'r', encoding='utf-8', errors='ignore') as f1, \
                 open(file2, 'r', encoding='utf-8', errors='ignore') as f2:
                
                lines1 = f1.readlines()
                lines2 = f2.readlines()

                if search_type == "method_name":
                    compare_methods(lines1, lines2, keyword, file)
                    differences_found = True

                elif search_type == "method_content":
                    method_boundaries1 = find_method_boundaries(lines1)
                    method_boundaries2 = find_method_boundaries(lines2)

                    for method1 in method_boundaries1:
                        if any(keyword in line for line in lines1[method1[0]:method1[1] + 1]) or \
                           any(keyword in line for line in lines2[method1[0]:method1[1] + 1]):
                            method_diff = difflib.ndiff(
                                lines1[method1[0]:method1[1] + 1],
                                lines2[method1[0]:method1[1] + 1]
                            )

                            file_diff = [
                                color_diff_with_line(line, method1[0] + idx + 1) 
                                for idx, line in enumerate(method_diff) if line.startswith('-') or line.startswith('+')
                            ]
                            if file_diff:
                                print_colored(f"Differences found in file: {file} (method content containing '{keyword}')", BLUE)
                                print("\n".join(file_diff))

    if not differences_found:
        print_colored(f"No More differences found for keyword: '{keyword}' with search type: '{search_type}'", RED)

### MENU FUNCTIONS ###

def display_menu():
    """Displays the main menu."""
    print(f"""
░▀█▀░░░░░█▀▄░█▀▀░█░█░░      
░░█░░░░░░█▀▄░█▀▀░▄▀▄░░      
░░▀░░▀▀▀░▀░▀░▀▀▀░▀░▀░░      
░█▀▀░█▀█░█▄█░█▀█░█▀█░█▀▄░█▀▀
░█░░░█░█░█░█░█▀▀░█▀█░█▀▄░█▀▀
░▀▀▀░▀▀▀░▀░▀░▀░░░▀░▀░▀░▀░▀▀▀
    """)
    print(f"\n{BLUE}Choose an option:{RESET}")
    print(f"1) {YELLOW}Compare using default keywords{RESET}")
    print(f"2) {YELLOW}Compare using custom keywords{RESET}")
    print(f"3) {RED}Exit{RESET}")

def search_type_menu():
    """Displays the search type menu."""
    while True:
        print_colored("Choose a search type:", BLUE)
        print(f"1) {YELLOW}Class Name{RESET}")
        print(f"2) {YELLOW}Method Name{RESET}")
        print(f"3) {YELLOW}Method Content{RESET}")
        print(f"4) {RED}Back to Main Menu{RESET}")

        search_type = input(f"{BLUE}Enter your choice (1-4): {RESET}")
        if search_type == "1":
            return "class"
        elif search_type == "2":
            return "method_name"
        elif search_type == "3":
            return "method_content"
        elif search_type == "4":
            return None
        else:
            print_colored("Invalid choice, please select 1, 2, 3, or 4.", RED)

### MAIN FUNCTION ###

def main():
    """Main function to control the flow of the script."""
    current_dir = Path().resolve()

    original_zip = current_dir / "ori.zip"
    modified_zip = current_dir / "mod.zip"

    if not (original_zip.is_file() and modified_zip.is_file()):
        print_colored("One or both of the zip files (ori.zip or mod.zip) do not exist in the current directory. Exiting.", RED)
        return

    original_dir = Path("original_smali_unzipped")
    modified_dir = Path("modified_smali_unzipped")

    try:
        unzip_file(original_zip, original_dir)
        unzip_file(modified_zip, modified_dir)
    except zipfile.BadZipFile as e:
        print_colored(f"Error unzipping files: {e}", RED)
        return

    while True:
        display_menu()
        choice = input(f"{BLUE}Enter your choice (1-3): {RESET}")

        if choice == "1":
            for keyword in DEFAULT_KEYWORDS:
                search_type = search_type_menu()
                if search_type is None:
                    break
                compare_directories(original_dir, modified_dir, keyword, search_type)

                cont = input(f"{YELLOW}Do you want to continue with the next keyword? (yes/no): {RESET}")
                if cont.lower() != "yes":
                    break

        elif choice == "2":
            while True:
                keyword = input(f"{BLUE}Enter a custom keyword to search for (or 'exit' to go back to the menu): {RESET}")
                if keyword.lower() == "exit":
                    break
                search_type = search_type_menu()
                if search_type is None:
                    break
                compare_directories(original_dir, modified_dir, keyword, search_type)

                cont = input(f"{YELLOW}Do you want to search with another custom keyword? (yes/no): {RESET}")
                if cont.lower() != "yes":
                    break

        elif choice == "3":
            print_colored("Exiting the comparison script.", RED)
            break
        else:
            print_colored("Invalid choice, please select 1, 2, or 3.", RED)

    cleanup_directories(original_dir, modified_dir)

if __name__ == "__main__":
    main()
