import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { NavigationContainer } from '@react-navigation/native';
import { createDrawerNavigator } from '@react-navigation/drawer';
import { createStackNavigator } from '@react-navigation/stack';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';

// Import screens
import HomeScreen from './src/screens/HomeScreen';
import BillsScreen from './src/screens/BillsScreen';
import CreateBillScreen from './src/screens/CreateBillScreen';
import CustomersScreen from './src/screens/CustomersScreen';
import ProductsScreen from './src/screens/ProductsScreen';
import CompanyConfigScreen from './src/screens/CompanyConfigScreen';
import LoginScreen from './src/screens/LoginScreen';

// Import services
import { DatabaseService } from './src/services/DatabaseService';

const Drawer = createDrawerNavigator();
const Stack = createStackNavigator();

// Main app navigation for authenticated users
function MainApp() {
  return (
    <Drawer.Navigator
      initialRouteName="Home"
      screenOptions={{
        headerStyle: {
          backgroundColor: '#2c3e50',
        },
        headerTintColor: '#fff',
        drawerActiveTintColor: '#2c3e50',
      }}
    >
      <Drawer.Screen 
        name="Home" 
        component={HomeScreen}
        options={{
          title: 'Dashboard',
          drawerIcon: ({ color, size }) => (
            <Ionicons name="home" size={size} color={color} />
          ),
        }}
      />
      <Drawer.Screen 
        name="Bills" 
        component={BillsScreen}
        options={{
          title: 'Bills',
          drawerIcon: ({ color, size }) => (
            <Ionicons name="receipt" size={size} color={color} />
          ),
        }}
      />
      <Drawer.Screen 
        name="CreateBill" 
        component={CreateBillScreen}
        options={{
          title: 'Create Bill',
          drawerIcon: ({ color, size }) => (
            <Ionicons name="add-circle" size={size} color={color} />
          ),
        }}
      />
      <Drawer.Screen 
        name="Customers" 
        component={CustomersScreen}
        options={{
          title: 'Customers',
          drawerIcon: ({ color, size }) => (
            <Ionicons name="people" size={size} color={color} />
          ),
        }}
      />
      <Drawer.Screen 
        name="Products" 
        component={ProductsScreen}
        options={{
          title: 'Products',
          drawerIcon: ({ color, size }) => (
            <Ionicons name="cube" size={size} color={color} />
          ),
        }}
      />
      <Drawer.Screen 
        name="CompanyConfig" 
        component={CompanyConfigScreen}
        options={{
          title: 'Company Settings',
          drawerIcon: ({ color, size }) => (
            <Ionicons name="settings" size={size} color={color} />
          ),
        }}
      />
    </Drawer.Navigator>
  );
}

// Root navigation with authentication
function RootStack() {
  const [isLoggedIn, setIsLoggedIn] = React.useState(false);

  React.useEffect(() => {
    // Initialize database and check authentication status
    DatabaseService.initializeDatabase().then(() => {
      // For now, skip authentication and go directly to main app
      setIsLoggedIn(true);
    });
  }, []);

  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      {isLoggedIn ? (
        <Stack.Screen name="MainApp" component={MainApp} />
      ) : (
        <Stack.Screen name="Login" component={LoginScreen} />
      )}
    </Stack.Navigator>
  );
}

export default function App() {
  return (
    <SafeAreaProvider>
      <NavigationContainer>
        <RootStack />
        <StatusBar style="light" />
      </NavigationContainer>
    </SafeAreaProvider>
  );
}
