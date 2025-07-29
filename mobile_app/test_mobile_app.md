# How to Test Your GST Billing Mobile App

## Quick Test Methods

### Method 1: Web Browser (Instant Testing)
- Open your browser and go to: `http://localhost:8081`
- The app will load as a mobile web app
- Test all features: navigation, dashboard, bills list, search

### Method 2: Android Phone with Expo Go
1. Install "Expo Go" app from Google Play Store
2. Make sure your phone is on the same WiFi network
3. Run this command in terminal:
   ```bash
   cd mobile_app/gst-billing-app
   npx expo start
   ```
4. Scan the QR code that appears with Expo Go
5. App loads instantly on your phone with live updates

### Method 3: Android Studio Emulator
```bash
cd mobile_app/gst-billing-app
npx expo run:android
```

## Features to Test

### Dashboard Screen
- ✅ View business statistics (bills, customers, products, revenue)
- ✅ Quick action buttons (Create Bill, Add Customer, etc.)
- ✅ Recent bills list
- ✅ Navigation drawer access

### Bills Screen  
- ✅ View all bills with status colors
- ✅ Search bills by number or customer name
- ✅ Pull-to-refresh functionality
- ✅ Floating action button for new bills

### Navigation
- ✅ Drawer menu with all sections
- ✅ Professional styling and icons
- ✅ Screen transitions

### Database
- ✅ SQLite database auto-created
- ✅ Sample data automatically loaded
- ✅ Offline functionality (no internet needed)

## App Structure
```
Mobile App Features:
├── 🏠 Dashboard - Business overview
├── 📄 Bills - Invoice management  
├── ➕ Create Bill - New invoices
├── 👥 Customers - Client database
├── 📦 Products - Inventory catalog
└── ⚙️ Settings - Company config
```

## Testing Commands

Start development server:
```bash
cd mobile_app/gst-billing-app
npm start
```

Run on specific platform:
```bash
npm run web      # Browser testing
npm run android  # Android emulator
npm run ios      # iOS simulator (macOS only)
```

## Expected Results

When you open the app, you should see:
1. Professional GST Billing app with dark blue theme
2. Dashboard showing sample business data
3. Working navigation between all screens
4. Search functionality in bills section
5. Responsive mobile-first design

The app works completely offline using local SQLite database!