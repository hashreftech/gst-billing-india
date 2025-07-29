# GST Billing Mobile App

A React Native mobile application for GST billing, built with Expo. This app provides the same functionality as the web version but optimized for mobile devices.

## Features

- **Dashboard**: Overview of business metrics and quick actions
- **Bills Management**: Create, view, and manage invoices
- **Customer Management**: Maintain customer database
- **Product Catalog**: Manage products with GST rates
- **Company Settings**: Configure business information
- **Offline Support**: Local SQLite database for offline functionality

## Technology Stack

- **Framework**: React Native with Expo
- **Navigation**: React Navigation 6
- **Database**: Expo SQLite for local data storage
- **Icons**: Expo Vector Icons
- **Styling**: React Native StyleSheet

## Project Structure

```
src/
├── screens/           # App screens
│   ├── HomeScreen.js
│   ├── BillsScreen.js
│   ├── CreateBillScreen.js
│   ├── CustomersScreen.js
│   ├── ProductsScreen.js
│   └── CompanyConfigScreen.js
├── services/          # Business logic and database
│   └── DatabaseService.js
├── components/        # Reusable UI components
├── utils/            # Helper functions
└── styles/           # Global styles
```

## Development Status

- ✅ Project Setup Complete
- ✅ Navigation Structure
- ✅ Database Service Layer
- ✅ Home Dashboard
- ✅ Bills List Screen
- ⏳ Bill Creation Form (In Progress)
- ⏳ Customer Management (Planned)
- ⏳ Product Management (Planned)
- ⏳ PDF Generation (Planned)

## Getting Started

1. Navigate to the mobile app directory:
   ```bash
   cd mobile_app/gst-billing-app
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Use Expo Go app on your phone to scan the QR code, or run in simulator:
   - iOS: `npm run ios` (requires macOS)
   - Android: `npm run android` (requires Android SDK)
   - Web: `npm run web`

## Database Schema

The app uses SQLite with tables mirroring the web application:
- `company` - Business information
- `customers` - Customer details
- `products` - Product catalog
- `bills` - Invoice headers
- `bill_items` - Invoice line items
- `bill_sequence` - Auto-numbering

## Future Enhancements

- Barcode scanning for products
- Offline-to-online sync
- Push notifications
- Report generation and sharing
- Dark mode support
- Multi-language support

## Platform Support

- ✅ Android (Primary focus)
- ✅ iOS (Cross-platform compatible)
- ✅ Web (PWA capability)