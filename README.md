# Smali File Comparison

This repository is designed for the reverse engineering of modified APKs and original APKs by finding differences between them.

---

This Python script is designed to **compare two sets of Smali files** extracted from two different APKs (unzipped from `ori.zip` and `mod.zip`). The comparison is based on class names, method names, and method content, using custom or default keywords. It highlights the differences between these files and outputs them with color-coded results.

### Features

- **Unzip APKs**: Automatically extracts APK files into directories for comparison.
- **File Comparison**: Compares class files, method names, or method content from the two sets of files.
- **Default and Custom Keywords**: Search using default keywords (like `isPro`, `isPremium`, etc.) or specify custom ones.
- **Color-Coded Output**: Differences are highlighted in color for easy identification:

    ```plaintext
    273: -     move-result v0
    274: +     const/4 v0, 0x1
    ```
    - Green (`+`): Added lines
    - Red (`-`): Removed lines
    - Blue: Informational messages
    - `273` and `274`: Line numbers where the changes are made in the code

### Installation

To use this script, you'll need to have Python installed on your system.

1. **Clone the repository**:
    ```bash
    git clone https://github.com/itzmejanak/smali-file-comparison.git
    cd smali-file-comparison
    ```

2. **Install dependencies** (if any are added later, such as `termcolor` for enhanced coloring):
    ```bash
    pip install -r requirements.txt
    ```

    > **Note**: Currently, the script uses only built-in Python libraries like `zipfile`, `shutil`, `difflib`, etc., so no external dependencies are required.

### Generating ZIP Files for Comparison

To use the script, you need two sets of **Smali files** in `.zip` format (`ori.zip` and `mod.zip`). Here’s how to generate these `.zip` files from `.dex` files:

#### Prerequisites

You need **Apktool** to disassemble `.dex` files into `.smali` format. Apktool is a popular tool used to reverse-engineer Android applications. If you are an Android user, you can use **MT Manager** to convert `.dex` to `.smali`.

1. **Download Apktool**: You can download Apktool from [here](https://ibotpeaches.github.io/Apktool/).
2. **Install Apktool**: Follow the instructions on the Apktool website to install it on your system.

#### Steps to Convert `.dex` to `.smali` and Create ZIPs

1. **Extract `.dex` file from APK**:
   - Open the APK file (it's a ZIP archive) and navigate to the `classes.dex` file.
   - Copy `classes.dex` to your working directory.

2. **Convert `.dex` to `.smali`**:
   - Use Apktool to disassemble the `.dex` file and convert it into `.smali` files:
     ```bash
     apktool d classes.dex -o smali_output
     ```
   - This will create a directory named `smali_output` containing all `.smali` files.

3. **Compress the `.smali` files into a ZIP**:
   - Navigate into the `smali_output` directory and compress its contents into a `.zip` file:
     ```bash
     zip -r smali_files.zip .
     ```
   - Rename this ZIP to `ori.zip` or `mod.zip` depending on whether it’s the original or modified APK.

4. **Repeat for the second APK**:
   - Follow the same steps for the second APK to generate a second ZIP (`mod.zip`).

Now you should have two ZIP files: `ori.zip` and `mod.zip`, which you can use with the script.

### Usage

Once you have `ori.zip` and `mod.zip` prepared, place these two files in the same directory as the script, then follow these steps to compare the files:

To run the script:
```bash
python compare_smali.py
```

The script will unzip both files and provide a menu interface to compare directories based on **class names**, **method names**, or **method content**.

#### Menu Options:

- **Compare using default keywords**: The script will search through the files using predefined keywords (`isPro`, `isPremium`, `isVip`, etc.).
- **Compare using custom keywords**: You can input your own keywords to search in the files.
- **Exit**: Exits the script.

#### Search Type Menu:

When you choose to compare files, you'll be asked to select how you want to compare them:

1. **Class Name**: Compares two directories based on a specific class name.
2. **Method Name**: Compares the methods found inside class files based on their names.
3. **Method Content**: Compares the actual content of methods, searching for specific keywords.

### Example Output

```python
Choose an option:
1) Compare using default keywords
2) Compare using custom keywords
3) Exit

Enter your choice (1-3): 1
Comparing with keyword: 'isPro', Search Type: 'class'
Differences found between MyApplication.smali and MyApplication.smali:
273: -     move-result v0
274: +     const/4 v0, 0x1
```

### Customizing the Script

#### Adding Default Keywords

You can modify the default keywords by editing the `DEFAULT_KEYWORDS` list in the script:
```python
DEFAULT_KEYWORDS = [
    "isPro", "isPremium", "isVip", "isPurchased", "isActive",
    "isUser", "sharedPrefences", "pro", "premium", "vip",
    "lifetime", "purchased", "unlimited", "unlocked"
]
```

#### Adjusting Output Color

The script uses ANSI escape codes for colored output. You can customize these colors by modifying the variables at the top of the script:
```python
RESET = "\033[0m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

--- 
