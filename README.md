# Android Temp File Cleaner 🔧

A user-friendly Python application developed to solve system file bloat issues that occur on Redmi and other Android phones by cleaning temporary files.

## ⚠️ Important Notice

> **IMPORTANT**: This application has not been fully tested yet. It is in active testing phase and will continue to be developed.
> 
> We are looking forward to feedback from you. Please report any bugs or suggestions you encounter.
> 
> **Use at your own risk. Please backup important data before use.**

## Features

✨ **User-Friendly Interface**: Modern and intuitive GUI built with Tkinter
📱 **Automatic Device Detection**: Automatically detects all connected Android devices
🗑️ **Safe Cleaning**: Cleans temporary files in the `/data/local/tmp/` directory
📊 **Size Check**: View folder size before cleaning
📝 **Detailed Logging**: All operations logged with timestamps
🔒 **Confirmation System**: User confirmation for critical operations
🌐 **Language Support**: Turkish and English interface options

## Requirements

### 1. Python
- Python 3.6 or higher is required
- Tkinter (usually comes with Python)

### 2. ADB (Android Debug Bridge)
ADB must be installed and added to PATH.

**For Windows:**
1. Download [Android SDK Platform Tools](https://developer.android.com/tools/releases/platform-tools)
2. Extract the ZIP to a folder (e.g., `C:\platform-tools`)
3. Add to PATH:
   - System Properties → Advanced → Environment Variables
   - Add `C:\platform-tools` to the Path variable

**For Linux/Mac:**
```bash
# Linux (Ubuntu/Debian)
sudo apt-get install android-tools-adb

# Mac (Homebrew)
brew install android-platform-tools
```

**Verify ADB installation:**
```bash
adb version
```

### 3. Android Device Settings
- USB Debugging must be enabled
- Developer Options must be accessible

**How to Enable Developer Options:**
1. Settings → About Phone
2. Tap "Build Number" or "MIUI Version" 7 times
3. Settings → Additional Settings → Developer Options
4. Enable "USB Debugging"

## Installation

1. **Download the file:**
   ```bash
   # Only one file is needed
   android_temp_cleaner.py
   ```

2. **Run the application:**
   ```bash
   python android_temp_cleaner.py
   ```

   Or double-click the file on Windows.

## Language Selection 🌐

When you launch the application, you'll be prompted to select your preferred language:
- **🇹🇷 Türkçe**: Full Turkish interface
- **🇬🇧 English**: Full English interface

After selecting your language, all interface elements and messages will be displayed in the selected language.

## Usage

### Step 1: Connect Your Device
- Connect your Android device to your computer via USB
- Approve "USB debugging" on your phone

### Step 2: Launch the Application
```bash
python android_temp_cleaner.py
```

### Step 3: Select Your Language
- Choose between Turkish (Türkçe) or English

### Step 4: Select Your Device
- The application will automatically scan for connected devices
- If multiple devices are connected, select one from the dropdown
- Click "🔄 Refresh Devices" to update the device list

### Step 5: Check Folder Size (Optional)
- Click "📊 Check Folder Size" button
- View the current size of the temp folder

### Step 6: Clean Files
- Click "🗑️ Clean Temp Files" button
- Confirm your action in the confirmation dialog
- Monitor the operation log

## Security Notes

⚠️ **IMPORTANT:**
- This application **only** cleans the `/data/local/tmp/` directory
- It does not touch system files or user data
- Root access is not required
- All operations are permanent, so be careful

## Troubleshooting

### "ADB Not Found" Error
- Make sure ADB is installed
- Check if `adb version` works in Terminal/CMD
- Verify PATH settings

### "No Devices Found"
- Check your USB cable
- Verify USB Debugging is enabled
- Approve the "Allow USB debugging" prompt on your phone
- Try a different USB port
- Manually check with `adb devices` command

### "Unauthorized Device"
- Check the approval prompt on your phone
- Approve it and try again

### Device Appears but Operation Fails
- Root access might be required on some devices
- You can try using a different ADB command:
  ```bash
  adb -s DEVICE_ID shell su -c "rm -rf /data/local/tmp/*"
  ```

## Technical Details

- **Language**: Python 3.x
- **GUI Framework**: Tkinter (standard Python library)
- **ADB Command**: `adb -s <device_id> shell rm -rf /data/local/tmp/*`
- **Threading**: Operations run in separate threads to prevent UI freezing
- **Translation System**: Dictionary-based i18n (internationalization) support

## Version Information

**Current Version**: v0.1-beta
- ⚠️ **Beta Version**: Not fully tested yet
- 🧪 **Active Development**: Regular updates and improvements
- 📊 **Testing Phase**: We are waiting for your feedback
- 🔄 **Feedback**: Please report bugs and suggestions

## License

This application is developed for educational and personal use. **The user is responsible for any issues that may arise from its use.**

⚠️ **Legal Disclaimer**: Any operations you perform on your device are your sole responsibility. Please backup important data.

## Contributing

If you want to help develop this open-source project:

1. **Bug Reports**: Document any bugs you find in detail
2. **Suggestions**: Submit feature requests and improvements
3. **Translations**: Add support for new languages
4. **Code Quality**: Submit pull requests for quality improvements

## Feedback

We're looking forward to your feedback! Please report:
- 🐛 Any bugs you encounter
- 💡 Feature suggestions
- 🌐 Translation improvements
- 🎯 Any other feedback

Your feedback helps us improve this application.

---

**Developer Note:** This application is designed specifically to solve the temporary file bloat issue that occurs on Redmi and Xiaomi devices. MIUI sometimes doesn't automatically clean the /data/local/tmp/ directory, causing gigabytes of unnecessary files to accumulate.
