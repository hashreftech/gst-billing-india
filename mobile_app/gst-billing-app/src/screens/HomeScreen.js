import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
  RefreshControl,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { DatabaseService } from '../services/DatabaseService';

export default function HomeScreen({ navigation }) {
  const [stats, setStats] = useState({});
  const [recentBills, setRecentBills] = useState([]);
  const [refreshing, setRefreshing] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const dashboardStats = await DatabaseService.getDashboardStats();
      const recent = await DatabaseService.getRecentBills(5);
      
      setStats(dashboardStats);
      setRecentBills(recent);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
      Alert.alert('Error', 'Failed to load dashboard data');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadDashboardData();
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

  if (loading) {
    return (
      <View style={[styles.container, styles.centered]}>
        <Text>Loading...</Text>
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
    >
      <View style={styles.header}>
        <Text style={styles.welcomeText}>Welcome to GST Billing</Text>
        <Text style={styles.subText}>Manage your business efficiently</Text>
      </View>

      {/* Quick Stats */}
      <View style={styles.statsContainer}>
        <View style={styles.statCard}>
          <Ionicons name="receipt-outline" size={24} color="#2c3e50" />
          <Text style={styles.statNumber}>{stats.totalBills || 0}</Text>
          <Text style={styles.statLabel}>Total Bills</Text>
        </View>
        
        <View style={styles.statCard}>
          <Ionicons name="people-outline" size={24} color="#2c3e50" />
          <Text style={styles.statNumber}>{stats.totalCustomers || 0}</Text>
          <Text style={styles.statLabel}>Customers</Text>
        </View>
        
        <View style={styles.statCard}>
          <Ionicons name="cube-outline" size={24} color="#2c3e50" />
          <Text style={styles.statNumber}>{stats.totalProducts || 0}</Text>
          <Text style={styles.statLabel}>Products</Text>
        </View>
        
        <View style={styles.statCard}>
          <Ionicons name="trending-up-outline" size={24} color="#2c3e50" />
          <Text style={styles.statNumber}>{formatCurrency(stats.totalRevenue)}</Text>
          <Text style={styles.statLabel}>Revenue</Text>
        </View>
      </View>

      {/* Quick Actions */}
      <View style={styles.quickActionsContainer}>
        <Text style={styles.sectionTitle}>Quick Actions</Text>
        <View style={styles.actionsGrid}>
          <TouchableOpacity
            style={[styles.actionCard, { backgroundColor: '#e3f2fd' }]}
            onPress={() => navigation.navigate('CreateBill')}
          >
            <Ionicons name="add-circle-outline" size={32} color="#1976d2" />
            <Text style={styles.actionText}>Create Bill</Text>
          </TouchableOpacity>
          
          <TouchableOpacity
            style={[styles.actionCard, { backgroundColor: '#f3e5f5' }]}
            onPress={() => navigation.navigate('Customers')}
          >
            <Ionicons name="person-add-outline" size={32} color="#7b1fa2" />
            <Text style={styles.actionText}>Add Customer</Text>
          </TouchableOpacity>
          
          <TouchableOpacity
            style={[styles.actionCard, { backgroundColor: '#e8f5e8' }]}
            onPress={() => navigation.navigate('Products')}
          >
            <Ionicons name="cube-outline" size={32} color="#388e3c" />
            <Text style={styles.actionText}>Add Product</Text>
          </TouchableOpacity>
          
          <TouchableOpacity
            style={[styles.actionCard, { backgroundColor: '#fff3e0' }]}
            onPress={() => navigation.navigate('Bills')}
          >
            <Ionicons name="list-outline" size={32} color="#f57c00" />
            <Text style={styles.actionText}>View Bills</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* Recent Bills */}
      <View style={styles.recentBillsContainer}>
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Recent Bills</Text>
          <TouchableOpacity onPress={() => navigation.navigate('Bills')}>
            <Text style={styles.viewAllText}>View All</Text>
          </TouchableOpacity>
        </View>
        
        {recentBills.length > 0 ? (
          recentBills.map((bill) => (
            <View key={bill.id} style={styles.billCard}>
              <View style={styles.billHeader}>
                <Text style={styles.billNumber}>{bill.bill_number}</Text>
                <View style={[styles.statusBadge, { backgroundColor: getStatusColor(bill.status) }]}>
                  <Text style={styles.statusText}>{bill.status}</Text>
                </View>
              </View>
              <Text style={styles.customerName}>{bill.customer_name || 'Guest Customer'}</Text>
              <View style={styles.billFooter}>
                <Text style={styles.billDate}>{new Date(bill.bill_date).toLocaleDateString()}</Text>
                <Text style={styles.billAmount}>{formatCurrency(bill.total_amount)}</Text>
              </View>
            </View>
          ))
        ) : (
          <View style={styles.emptyState}>
            <Ionicons name="receipt-outline" size={48} color="#ccc" />
            <Text style={styles.emptyStateText}>No bills created yet</Text>
            <TouchableOpacity
              style={styles.createFirstBillButton}
              onPress={() => navigation.navigate('CreateBill')}
            >
              <Text style={styles.createFirstBillText}>Create Your First Bill</Text>
            </TouchableOpacity>
          </View>
        )}
      </View>
    </ScrollView>
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
  header: {
    padding: 20,
    backgroundColor: '#2c3e50',
    borderBottomLeftRadius: 20,
    borderBottomRightRadius: 20,
  },
  welcomeText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  subText: {
    fontSize: 16,
    color: '#bdc3c7',
    marginTop: 5,
  },
  statsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    padding: 15,
    justifyContent: 'space-between',
  },
  statCard: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
    width: '48%',
    marginBottom: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  statNumber: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginTop: 5,
  },
  statLabel: {
    fontSize: 12,
    color: '#7f8c8d',
    marginTop: 2,
  },
  quickActionsContainer: {
    padding: 15,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 15,
  },
  actionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  actionCard: {
    width: '48%',
    padding: 20,
    borderRadius: 10,
    alignItems: 'center',
    marginBottom: 10,
  },
  actionText: {
    marginTop: 8,
    fontSize: 14,
    fontWeight: '500',
    textAlign: 'center',
  },
  recentBillsContainer: {
    padding: 15,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  viewAllText: {
    color: '#2c3e50',
    fontSize: 14,
    fontWeight: '500',
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
    marginBottom: 5,
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
    marginBottom: 8,
  },
  billFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  billDate: {
    fontSize: 12,
    color: '#95a5a6',
  },
  billAmount: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#27ae60',
  },
  emptyState: {
    alignItems: 'center',
    padding: 40,
  },
  emptyStateText: {
    fontSize: 16,
    color: '#95a5a6',
    marginTop: 10,
    marginBottom: 20,
  },
  createFirstBillButton: {
    backgroundColor: '#2c3e50',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 8,
  },
  createFirstBillText: {
    color: '#fff',
    fontWeight: '500',
  },
});