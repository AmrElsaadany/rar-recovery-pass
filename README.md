# RAR Password Recovery Tool

A Python-based GUI application for recovering lost or forgotten passwords from RAR archives using multiple attack methods including brute force and dictionary attacks.

## Features

✨ **Three Attack Modes:**
- **Numeric Brute Force** - Tests sequential numbers (1, 2, 3, ...)
- **Dictionary Attack** - Tests passwords from a custom wordlist file
- **Alphanumeric Brute Force** - Tests combinations of letters, numbers, and symbols with customizable length range (a-z, A-Z, 0-9, !@#, etc.)

🎯 **Key Capabilities:**
- User-friendly Tkinter GUI interface
- Real-time password testing display
- Stop/resume functionality during attacks
- Automatic file opening upon successful password recovery
- Progress feedback with live status updates
- Support for custom wordlists
- Customizable password length parameters for brute force attacks

## Requirements

- Python 3.6+
- `rarfile` library (automatically checked on startup)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/AmrElsaadany/rar-recovery-pass.git
cd rar-recovery-pass
```

### 2. Install Dependencies
```bash
pip install rarfile
```

**Note:** The application will display an error dialog if `rarfile` is not installed and provide instructions to install it.

## Usage

### Running the Application

#### Option 1: Using Python Directly
```bash
python Rar_pass_remover_v2.py
```

#### Option 2: Using the Original Version
```bash
python Rar_pass_remover.py
```

### Step-by-Step Guide

1. **Select Target RAR File**
   - Click "Browse" next to "RAR File"
   - Choose the password-protected RAR archive you want to recover

2. **Choose Attack Method**
   - **Numeric Brute Force**: For numeric-only passwords
   - **Dictionary Attack**: For passwords from a wordlist (select your wordlist file)
   - **Alphanumeric Brute Force**: For complex passwords (specify min/max character length)

3. **Configure Options** (if applicable)
   - For Dictionary Attack: Browse and select your `.txt` wordlist file
   - For Alphanumeric Brute Force: Set minimum and maximum password lengths

4. **Start Attack**
   - Click "Start Attack" button
   - Monitor progress in the "Live Progress" section
   - Click "Stop" to halt the attack at any time

5. **Results**
   - Success: Password found and displayed; RAR file opens automatically
   - Failure: "Password not discovered" message after exhausting all attempts

## Versions

### Version 1 (`Rar_pass_remover.py`)
- Basic password recovery with three attack modes
- Fixed alphanumeric length range (1-8 characters)
- Stable, tested implementation

### Version 2 (`Rar_pass_remover_v2.py`) ⭐ **RECOMMENDED**
- All features from V1
- **Enhanced:** Customizable password length range for alphanumeric attacks
- **Improved:** Better UI state management
- **Fixed:** Corrected code indentation
- **Better UX:** Length input fields only appear when needed

## Included Resources

- **10k-most-common.txt** - Wordlist containing 10,000 most common passwords (73 KB)
- **pass.txt** - Alternative wordlist with common passwords
- **Common.rar** - Sample test RAR file for testing purposes

## Performance Tips

⚡ **For Faster Results:**
1. Use **Dictionary Attack** mode with a quality wordlist (fastest method)
2. Start with small length ranges in Alphanumeric mode (1-4 characters)
3. Use **Numeric Brute Force** for numeric-only passwords (most efficient for small numbers)
4. Increase password length gradually if short lengths don't work

⏱️ **Performance Considerations:**
- Alphanumeric brute force with 8+ character lengths can take hours/days
- Dictionary attack speed depends on wordlist size (10,000 entries = seconds to minutes)
- Numeric brute force speed depends on password value (higher = longer time)

## Technical Details

### Architecture
- **GUI Framework:** Tkinter (cross-platform)
- **Threading:** Uses daemon threads to prevent UI freezing
- **RAR Testing:** Uses `rarfile.RarFile.testrar()` for password validation
- **Error Handling:** Graceful exception handling for corrupt files and invalid input

### Code Structure
```
RarRecoveryApp
├── create_widgets()       # Build GUI interface
├── update_ui_state()      # Manage field visibility
├── test_password()        # Validate password against RAR
├── start_process()        # Initialize attack
├── recovery_loop()        # Main attack execution
├── browse_rar()          # File selection
├── browse_wordlist()     # Wordlist selection
├── open_target_file()    # Open RAR after success
└── stop_process()        # Stop attack
```

## Security & Legal Notice

⚠️ **Important:**
- This tool is designed for recovering your own lost passwords
- **Unauthorized access** to computer systems or files you do not own is **illegal**
- Use responsibly and only on archives you have permission to recover
- The authors are not responsible for misuse

## Troubleshooting

### Issue: "Missing Dependency" Error
**Solution:** Install rarfile library
```bash
pip install rarfile
```

### Issue: "Invalid RAR file" Error
**Solution:** 
- Verify the selected file is a valid RAR archive
- Try opening the file with WinRAR or 7-Zip to confirm it's not corrupted

### Issue: Attack taking too long
**Solution:**
- For alphanumeric attacks, reduce max length (e.g., from 8 to 6)
- Use dictionary attack with a relevant wordlist
- Try numeric mode if password is numeric-only

### Issue: GUI freezing
**Solution:**
- The app uses threading to prevent freezing; if it occurs, restart the application
- Ensure you're using Python 3.6 or higher

## License

GNU General Public License v3.0 - See [LICENSE](LICENSE) file for details

## Contributing

Contributions are welcome! Feel free to:
- Report bugs or issues
- Suggest improvements
- Submit pull requests

## Author

**AmrElsaadany** - [GitHub Profile](https://github.com/AmrElsaadany)

## Changelog

### v2.0 (Current)
- Fixed critical indentation error in `recovery_loop()` method
- Added customizable password length control for alphanumeric attacks
- Improved UI state management
- Enhanced user feedback messages

### v1.0
- Initial release
- Three attack modes implemented
- Tkinter GUI interface
- Basic password recovery functionality

---

**Last Updated:** June 19, 2026
