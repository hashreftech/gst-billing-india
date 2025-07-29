#!/bin/bash

echo "Starting GST Billing Mobile App..."
echo "=================================="

cd mobile_app/gst-billing-app

# Kill any existing expo processes
pkill -f "expo start" 2>/dev/null

# Start the mobile app
echo "Starting Expo development server..."
npx expo start --web --port 8081 --host 0.0.0.0 --non-interactive &

# Wait for the server to start
sleep 8

echo ""
echo "🚀 GST Billing Mobile App is starting..."
echo ""
echo "📱 Testing Options:"
echo "1. Web Browser: http://localhost:8081"
echo "2. Android Phone: Install 'Expo Go' app and scan QR code"
echo "3. Use 'npx expo start' for full interactive mode"
echo ""
echo "✅ App features ready to test:"
echo "   - Dashboard with business stats"
echo "   - Bills list with search"
echo "   - Navigation drawer"
echo "   - SQLite database with sample data"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=================================="

# Keep the script running
wait