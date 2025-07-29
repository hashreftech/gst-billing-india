import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

export default function CustomersScreen({ navigation }) {
  return (
    <View style={styles.container}>
      <View style={styles.comingSoonContainer}>
        <Ionicons name="people-outline" size={64} color="#bdc3c7" />
        <Text style={styles.comingSoonText}>Customers</Text>
        <Text style={styles.comingSoonSubtext}>
          Customer management coming soon!
        </Text>
        
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => navigation.goBack()}
        >
          <Text style={styles.backButtonText}>Go Back</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  comingSoonContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 40,
  },
  comingSoonText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginTop: 20,
  },
  comingSoonSubtext: {
    fontSize: 16,
    color: '#7f8c8d',
    textAlign: 'center',
    marginTop: 10,
    marginBottom: 30,
  },
  backButton: {
    backgroundColor: '#2c3e50',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 8,
  },
  backButtonText: {
    color: '#fff',
    fontWeight: '500',
    fontSize: 16,
  },
});