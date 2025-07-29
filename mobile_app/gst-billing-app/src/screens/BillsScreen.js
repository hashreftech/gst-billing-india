import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  Alert,
  RefreshControl,
  TextInput,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { DatabaseService } from '../services/DatabaseService';

export default function BillsScreen({ navigation }) {
  const [bills, setBills] = useState([]);
  const [filteredBills, setFilteredBills] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    loadBills();
  }, []);

  useEffect(() => {
    filterBills();
  }, [searchQuery, bills]);

  const loadBills = async () => {
    try {
      const billsData = await DatabaseService.getAllBills();
      setBills(billsData);
    } catch (error) {
      console.error('Error loading bills:', error);
      Alert.alert('Error', 'Failed to load bills');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const filterBills = () => {
    if (!searchQuery.trim()) {
      setFilteredBills(bills);
      return;
    }

    const filtered = bills.filter((bill) =>
      bill.bill_number.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (bill.customer_name && bill.customer_name.toLowerCase().includes(searchQuery.toLowerCase()))
    );
    setFilteredBills(filtered);
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadBills();
  };

  const formatCurrency = (amount) => {
    return `₹${parseFloat(amount || 0).toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Paid': return '#28a745';
      case 'Sent': return '#17a2b8';
      case 'Cancelled': return '#dc3545';
      default: return '#6c757d';
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-IN');
  };

  const renderBillItem = ({ item }) => (
    <TouchableOpacity
      style={styles.billCard}
      onPress={() => {
        // Navigate to bill details screen (to be implemented)
        Alert.alert('Bill Details', `Bill: ${item.bill_number}\nCustomer: ${item.customer_name}\nAmount: ${formatCurrency(item.total_amount)}`);
      }}
    >
      <View style={styles.billHeader}>
        <Text style={styles.billNumber}>{item.bill_number}</Text>
        <View style={[styles.statusBadge, { backgroundColor: getStatusColor(item.status) }]}>
          <Text style={styles.statusText}>{item.status}</Text>
        </View>
      </View>
      
      <Text style={styles.customerName}>{item.customer_name || 'Guest Customer'}</Text>
      
      <View style={styles.billFooter}>
        <View>
          <Text style={styles.billDate}>{formatDate(item.bill_date)}</Text>
          <Text style={styles.createdDate}>Created: {formatDate(item.created_at)}</Text>
        </View>
        <Text style={styles.billAmount}>{formatCurrency(item.total_amount)}</Text>
      </View>
    </TouchableOpacity>
  );

  if (loading) {
    return (
      <View style={[styles.container, styles.centered]}>
        <Text>Loading bills...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Search Bar */}
      <View style={styles.searchContainer}>
        <Ionicons name="search" size={20} color="#7f8c8d" style={styles.searchIcon} />
        <TextInput
          style={styles.searchInput}
          placeholder="Search bills by number or customer..."
          value={searchQuery}
          onChangeText={setSearchQuery}
        />
      </View>

      {/* Bills List */}
      <FlatList
        data={filteredBills}
        renderItem={renderBillItem}
        keyExtractor={(item) => item.id.toString()}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
        contentContainerStyle={styles.listContainer}
        ListEmptyComponent={
          <View style={styles.emptyState}>
            <Ionicons name="receipt-outline" size={64} color="#bdc3c7" />
            <Text style={styles.emptyStateText}>
              {searchQuery ? 'No bills found for your search' : 'No bills created yet'}
            </Text>
            {!searchQuery && (
              <TouchableOpacity
                style={styles.createBillButton}
                onPress={() => navigation.navigate('CreateBill')}
              >
                <Text style={styles.createBillText}>Create Your First Bill</Text>
              </TouchableOpacity>
            )}
          </View>
        }
      />

      {/* Floating Action Button */}
      <TouchableOpacity
        style={styles.fab}
        onPress={() => navigation.navigate('CreateBill')}
      >
        <Ionicons name="add" size={24} color="#fff" />
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  centered: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    margin: 15,
    paddingHorizontal: 15,
    paddingVertical: 10,
    borderRadius: 25,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  searchIcon: {
    marginRight: 10,
  },
  searchInput: {
    flex: 1,
    fontSize: 16,
    color: '#2c3e50',
  },
  listContainer: {
    paddingHorizontal: 15,
    paddingBottom: 80,
  },
  billCard: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 10,
    marginBottom: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  billHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  billNumber: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2c3e50',
  },
  statusBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
  },
  statusText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '500',
  },
  customerName: {
    fontSize: 14,
    color: '#7f8c8d',
    marginBottom: 10,
  },
  billFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-end',
  },
  billDate: {
    fontSize: 14,
    color: '#2c3e50',
    fontWeight: '500',
  },
  createdDate: {
    fontSize: 12,
    color: '#95a5a6',
    marginTop: 2,
  },
  billAmount: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#27ae60',
  },
  emptyState: {
    alignItems: 'center',
    padding: 40,
    marginTop: 50,
  },
  emptyStateText: {
    fontSize: 16,
    color: '#95a5a6',
    marginTop: 15,
    marginBottom: 20,
    textAlign: 'center',
  },
  createBillButton: {
    backgroundColor: '#2c3e50',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 8,
  },
  createBillText: {
    color: '#fff',
    fontWeight: '500',
    fontSize: 16,
  },
  fab: {
    position: 'absolute',
    right: 20,
    bottom: 20,
    backgroundColor: '#2c3e50',
    width: 56,
    height: 56,
    borderRadius: 28,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 6,
    elevation: 8,
  },
});