# Mobile Application Requirements

## Prerequisites
- Node.js (version 14 or higher)
- npm (comes with Node.js)
- React Native CLI
- Android Studio (for Android development)
- Xcode (for iOS development, macOS only)

## Installation

1. Install project dependencies:
   ```bash
   npm install
   ```

2. For iOS development:
   ```bash
   cd ios
   pod install
   cd ..
   ```

## Running the Application

### iOS
```bash
npx react-native run-ios
```

### Android
```bash
npx react-native run-android
```

## Required Permissions

The app requires the following permissions:
- Location access (for mapping and navigation)
- Bluetooth (for proximity detection)
- Internet access (for communication with the server)

## Configuration

Create a `config.json` file in the root directory with the following structure:

```json
{
  "ip_adress": "YOUR_SERVER_IP"
}
```

Replace `YOUR_SERVER_IP` with the IP address of the machine running the SPADE server.

## Troubleshooting

### iOS
If you encounter build issues:
1. Clean the build folder: `cd ios && xcodebuild clean && cd ..`
2. Reinstall pods: `cd ios && pod install --repo-update && cd ..`

### Android
If you encounter build issues:
1. Clean the project: `cd android && ./gradlew clean && cd ..`
2. Check that Android Studio is properly configured with SDKs

### Common Issues
1. "config.json not found" - Make sure you've created the config.json file
2. "Network error" - Check that the SPADE server is running and accessible
3. "Permission denied" - Make sure all required permissions are granted in the app settings