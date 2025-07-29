import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Image,
} from 'react-native';

export default function LoginScreen({ navigation }) {
  return (
    <View style={styles.container}>
      <View style={styles.logoContainer}>
        <Text style={styles.appName}>GST Billing</Text>
        <Text style={styles.tagline}>Professional Invoice Management</Text>
      </View>
      
      <View style={styles.contentContainer}>
        <Text style={styles.welcomeText}>Welcome!</Text>
        <Text style={styles.descriptionText}>
          Create and manage GST-compliant invoices with ease
        </Text>
        
        <TouchableOpacity style={styles.loginButton}>
          <Text style={styles.loginButtonText}>Get Started</Text>
        </TouchableOpacity>
      </View>
      
      <View style={styles.footer}>
        <Text style={styles.footerText}>Made for Indian Businesses</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#2c3e50',
    justifyContent: 'center',
  },
  logoContainer: {
    alignItems: 'center',
    marginBottom: 50,
  },
  appName: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 10,
  },
  tagline: {
    fontSize: 16,
    color: '#bdc3c7',
  },
  contentContainer: {
    paddingHorizontal: 30,
    alignItems: 'center',
  },
  welcomeText: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 10,
  },
  descriptionText: {
    fontSize: 16,
    color: '#bdc3c7',
    textAlign: 'center',
    marginBottom: 40,
    lineHeight: 24,
  },
  loginButton: {
    backgroundColor: '#3498db',
    paddingHorizontal: 40,
    paddingVertical: 15,
    borderRadius: 8,
    width: '100%',
  },
  loginButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
    textAlign: 'center',
  },
  footer: {
    position: 'absolute',
    bottom: 30,
    left: 0,
    right: 0,
    alignItems: 'center',
  },
  footerText: {
    color: '#95a5a6',
    fontSize: 14,
  },
});