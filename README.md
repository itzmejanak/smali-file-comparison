# Smali File Comparison
This Repository designed for Reverse-engineering Of Moded apk &amp; Original Apk Finding Differences Between Them.....

---

# Smali File Comparison Script

This Python script is designed to **compare two sets of Smali files** from two different APKs (unzipped from `ori.zip` and `mod.zip`). The comparison is based on class names, method names, and method content, using custom or default keywords. It highlights the differences between these files and outputs them with color-coded results.

## Features

- **Unzip APKs**: Automatically extracts the APK files into directories for comparison.
- **File Comparison**: Compares class files, method names, or method content from the two sets of files.
- **Default and Custom Keywords**: Search using default keywords (like `isPro`, `isPremium`, etc.) or specify custom ones.
- **Color-Coded Output**: Differences are highlighted in color to make them easily identifiable:
  - Green (`+`): Added lines
  - Red (`-`): Removed lines
  - Blue: Informational messages

## Installation

To use this script, you'll need to have Python installed on your system.

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/smali-file-comparison.git
    cd smali-file-comparison
    ```

2. **Install dependencies** (if any are added later, such as `termcolor` for enhanced coloring):
    ```bash
    pip install -r requirements.txt
    ```

> Note: As of now, the script only uses built-in Python libraries like `zipfile`, `shutil`, `difflib`, etc., so no external dependencies are required.

## Generating ZIP Files for Comparison

To use the script, you need two sets of **Smali files** in `.zip` format (`ori.zip` and `mod.zip`). Here’s how to generate these `.zip` files from `.dex` files:

### Prerequisites

You need the **Apktool** to disassemble `.dex` files into `.smali` format. Apktool is a popular tool used to reverse-engineer Android applications. *If you are android User then you can Use MT manager to convert dex to smali*.

1. **Download Apktool**: You can download Apktool from [here](https://ibotpeaches.github.io/Apktool/).
2. **Install Apktool**: Follow the instructions on the Apktool website to install it on your system.

### Steps to Convert `.dex` to `.smali` and Create ZIPs

1. **Extract `.dex` file from APK**:
   - First, you need to extract the `.dex` file from an APK. You can open the APK file (it's a ZIP archive) and navigate to the `classes.dex` file.
   - Copy `classes.dex` to your working directory.

2. **Convert `.dex` to `.smali`**:
   - Use Apktool to disassemble the `.dex` file and convert it into `.smali` files:
     ```bash
     apktool d classes.dex -o smali_output
     ```
   - This will create a directory named `smali_output` containing all `.smali` files.

3. **Compress the `.smali` files into a ZIP**:
   - Navigate into the `smali_output` directory and compress its contents into a `.zip` file.
     ```bash
     zip -r smali_files.zip .
     ```
   - You can rename this ZIP to `ori.zip` or `mod.zip` depending on whether it’s the original or modified APK.

4. **Repeat for the second APK**:
   - Repeat the above steps for the second APK and generate a second ZIP (`mod.zip`).

Now you should have two ZIP files: `ori.zip` and `mod.zip`, which you can use with the script.

## Usage

Once you have `ori.zip` and `mod.zip` prepared and Putting this two files in same dir including Scripts then, follow these steps to compare the files:

To run the script:
```bash
python compare_smali.py
```

The script will unzip both files and provide a menu interface to compare directories based on **class names**, **method names**, or **method content**.

### Menu Options:

- **Compare using default keywords**: The script will search through the files using pre-defined keywords (`isPro`, `isPremium`, `isVip`, etc.).
- **Compare using custom keywords**: You can input your own keywords to search in the files.
- **Exit**: Exits the script.

### Search Type Menu:

When choosing to compare files, you'll also be asked to choose how you want to compare them:

1. **Class Name**: Compares two directories based on a specific class name.
2. **Method Name**: Compares the methods found inside class files based on their names.
3. **Method Content**: Compares the actual content of methods, searching for specific keywords.

## Example Output

```
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

## Customizing the Script

### Adding Default Keywords

You can modify the default keywords by editing the `DEFAULT_KEYWORDS` list in the script:
```python
DEFAULT_KEYWORDS = [
    "isPro", "isPremium", "isVip", "isPurchased", "isActive",
    "isUser", "sharedPrefences", "pro", "premium", "vip",
    "lifetime", "purchased", "unlimited", "unlocked"
]
```

### Adjusting Output Color

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
