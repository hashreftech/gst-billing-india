import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

export default function CreateBillScreen({ navigation }) {
  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Create New Bill</Text>
      </View>
      
      <View style={styles.comingSoonContainer}>
        <Ionicons name="construct-outline" size={64} color="#bdc3c7" />
        <Text style={styles.comingSoonText}>Create Bill Screen</Text>
        <Text style={styles.comingSoonSubtext}>
          Bill creation functionality coming soon!
        </Text>
        
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => navigation.goBack()}
        >
          <Text style={styles.backButtonText}>Go Back</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  header: {
    padding: 20,
    backgroundColor: '#2c3e50',
    borderBottomLeftRadius: 20,
    borderBottomRightRadius: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  comingSoonContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 40,
    marginTop: 100,
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