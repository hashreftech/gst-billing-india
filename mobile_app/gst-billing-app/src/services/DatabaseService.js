import * as SQLite from 'expo-sqlite';

export class DatabaseService {
  static db = null;

  static async initializeDatabase() {
    try {
      this.db = await SQLite.openDatabaseAsync('gst_billing.db');
      await this.createTables();
      await this.insertDefaultData();
      console.log('Database initialized successfully');
    } catch (error) {
      console.error('Database initialization error:', error);
    }
  }

  static async createTables() {
    try {
      // Company table
      await this.db.execAsync(`
        CREATE TABLE IF NOT EXISTS company (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          address TEXT,
          phone TEXT,
          email TEXT,
          gst_number TEXT,
          state_code TEXT DEFAULT '27',
          logo_path TEXT,
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
      `);

      // Customers table
      await this.db.execAsync(`
        CREATE TABLE IF NOT EXISTS customers (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          address TEXT,
          phone TEXT,
          email TEXT,
          gst_number TEXT,
          state_code TEXT,
          is_guest BOOLEAN DEFAULT 0,
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
      `);

      // Products table
      await this.db.execAsync(`
        CREATE TABLE IF NOT EXISTS products (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          description TEXT,
          hsn_code TEXT,
          unit TEXT DEFAULT 'Nos',
          price REAL DEFAULT 0,
          gst_rate REAL DEFAULT 18,
          category TEXT,
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
      `);

      // Bills table
      await this.db.execAsync(`
        CREATE TABLE IF NOT EXISTS bills (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          bill_number TEXT NOT NULL UNIQUE,
          customer_id INTEGER,
          bill_date DATE NOT NULL,
          due_date DATE,
          status TEXT DEFAULT 'Draft',
          subtotal REAL DEFAULT 0,
          discount_type TEXT DEFAULT 'none',
          discount_value REAL DEFAULT 0,
          discount_amount REAL DEFAULT 0,
          cgst_amount REAL DEFAULT 0,
          sgst_amount REAL DEFAULT 0,
          igst_amount REAL DEFAULT 0,
          total_amount REAL DEFAULT 0,
          notes TEXT,
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
          updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY (customer_id) REFERENCES customers (id)
        );
      `);

      // Bill Items table
      await this.db.execAsync(`
        CREATE TABLE IF NOT EXISTS bill_items (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          bill_id INTEGER,
          product_id INTEGER,
          product_name TEXT NOT NULL,
          description TEXT,
          hsn_code TEXT,
          quantity REAL DEFAULT 1,
          unit TEXT DEFAULT 'Nos',
          rate REAL DEFAULT 0,
          amount REAL DEFAULT 0,
          gst_rate REAL DEFAULT 18,
          cgst_amount REAL DEFAULT 0,
          sgst_amount REAL DEFAULT 0,
          igst_amount REAL DEFAULT 0,
          FOREIGN KEY (bill_id) REFERENCES bills (id) ON DELETE CASCADE,
          FOREIGN KEY (product_id) REFERENCES products (id)
        );
      `);

      // Bill sequence table for auto-numbering
      await this.db.execAsync(`
        CREATE TABLE IF NOT EXISTS bill_sequence (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          year INTEGER NOT NULL,
          sequence_number INTEGER DEFAULT 0,
          UNIQUE(year)
        );
      `);

    } catch (error) {
      console.error('Error creating tables:', error);
    }
  }

  static async insertDefaultData() {
    try {
      // Check if company exists
      const companyResult = await this.db.getFirstAsync('SELECT COUNT(*) as count FROM company');
      if (companyResult.count === 0) {
        await this.db.runAsync(`
          INSERT INTO company (name, address, phone, email, gst_number, state_code) 
          VALUES (?, ?, ?, ?, ?, ?)
        `, ['Your Company Name', 'Your Company Address', '+91-9999999999', 'info@yourcompany.com', '27ABCDE1234F1Z5', '27']);
      }

      // Insert sample products
      const productResult = await this.db.getFirstAsync('SELECT COUNT(*) as count FROM products');
      if (productResult.count === 0) {
        await this.db.runAsync(`
          INSERT INTO products (name, description, hsn_code, unit, price, gst_rate, category) 
          VALUES (?, ?, ?, ?, ?, ?, ?)
        `, ['Sample Product 1', 'Description for sample product', '1234', 'Nos', 100.00, 18.00, 'General']);
        
        await this.db.runAsync(`
          INSERT INTO products (name, description, hsn_code, unit, price, gst_rate, category) 
          VALUES (?, ?, ?, ?, ?, ?, ?)
        `, ['Sample Product 2', 'Another sample product', '5678', 'Kg', 50.00, 12.00, 'Food']);
      }

      // Insert sample customer
      const customerResult = await this.db.getFirstAsync('SELECT COUNT(*) as count FROM customers');
      if (customerResult.count === 0) {
        await this.db.runAsync(`
          INSERT INTO customers (name, address, phone, email, gst_number, state_code, is_guest) 
          VALUES (?, ?, ?, ?, ?, ?, ?)
        `, ['Sample Customer', 'Customer Address', '+91-8888888888', 'customer@email.com', '27XYZTE9876A1B2', '27', 0]);
      }

    } catch (error) {
      console.error('Error inserting default data:', error);
    }
  }

  // Company methods
  static async getCompany() {
    return await this.db.getFirstAsync('SELECT * FROM company LIMIT 1');
  }

  static async updateCompany(companyData) {
    const { name, address, phone, email, gst_number, state_code } = companyData;
    await this.db.runAsync(`
      UPDATE company SET 
        name = ?, address = ?, phone = ?, email = ?, gst_number = ?, state_code = ?
      WHERE id = 1
    `, [name, address, phone, email, gst_number, state_code]);
  }

  // Customer methods
  static async getAllCustomers() {
    return await this.db.getAllAsync('SELECT * FROM customers ORDER BY name');
  }

  static async getCustomerById(id) {
    return await this.db.getFirstAsync('SELECT * FROM customers WHERE id = ?', [id]);
  }

  static async createCustomer(customerData) {
    const { name, address, phone, email, gst_number, state_code, is_guest } = customerData;
    const result = await this.db.runAsync(`
      INSERT INTO customers (name, address, phone, email, gst_number, state_code, is_guest) 
      VALUES (?, ?, ?, ?, ?, ?, ?)
    `, [name, address || '', phone || '', email || '', gst_number || '', state_code || '', is_guest || 0]);
    return result.lastInsertRowId;
  }

  // Product methods
  static async getAllProducts() {
    return await this.db.getAllAsync('SELECT * FROM products ORDER BY name');
  }

  static async getProductById(id) {
    return await this.db.getFirstAsync('SELECT * FROM products WHERE id = ?', [id]);
  }

  static async createProduct(productData) {
    const { name, description, hsn_code, unit, price, gst_rate, category } = productData;
    const result = await this.db.runAsync(`
      INSERT INTO products (name, description, hsn_code, unit, price, gst_rate, category) 
      VALUES (?, ?, ?, ?, ?, ?, ?)
    `, [name, description || '', hsn_code || '', unit || 'Nos', price || 0, gst_rate || 18, category || 'General']);
    return result.lastInsertRowId;
  }

  // Bill methods
  static async getAllBills() {
    return await this.db.getAllAsync(`
      SELECT b.*, c.name as customer_name 
      FROM bills b 
      LEFT JOIN customers c ON b.customer_id = c.id 
      ORDER BY b.created_at DESC
    `);
  }

  static async getBillById(id) {
    return await this.db.getFirstAsync('SELECT * FROM bills WHERE id = ?', [id]);
  }

  static async getBillItems(billId) {
    return await this.db.getAllAsync('SELECT * FROM bill_items WHERE bill_id = ?', [billId]);
  }

  static async generateBillNumber() {
    const year = new Date().getFullYear();
    
    // Get or create sequence for current year
    let sequence = await this.db.getFirstAsync('SELECT * FROM bill_sequence WHERE year = ?', [year]);
    
    if (!sequence) {
      await this.db.runAsync('INSERT INTO bill_sequence (year, sequence_number) VALUES (?, ?)', [year, 1]);
      return `INV-${year}-001`;
    } else {
      const newSequence = sequence.sequence_number + 1;
      await this.db.runAsync('UPDATE bill_sequence SET sequence_number = ? WHERE year = ?', [newSequence, year]);
      return `INV-${year}-${newSequence.toString().padStart(3, '0')}`;
    }
  }

  static async createBill(billData) {
    try {
      const billNumber = await this.generateBillNumber();
      const { customer_id, bill_date, due_date, status, notes, items, subtotal, total_amount, cgst_amount, sgst_amount, igst_amount, discount_type, discount_value, discount_amount } = billData;
      
      const billResult = await this.db.runAsync(`
        INSERT INTO bills (bill_number, customer_id, bill_date, due_date, status, subtotal, 
                          total_amount, cgst_amount, sgst_amount, igst_amount, notes,
                          discount_type, discount_value, discount_amount) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      `, [billNumber, customer_id, bill_date, due_date, status || 'Draft', subtotal, 
          total_amount, cgst_amount, sgst_amount, igst_amount, notes || '',
          discount_type || 'none', discount_value || 0, discount_amount || 0]);
      
      const billId = billResult.lastInsertRowId;
      
      // Insert bill items
      for (const item of items) {
        await this.db.runAsync(`
          INSERT INTO bill_items (bill_id, product_id, product_name, description, hsn_code, 
                                quantity, unit, rate, amount, gst_rate, cgst_amount, sgst_amount, igst_amount) 
          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        `, [billId, item.product_id, item.product_name, item.description || '', item.hsn_code || '',
            item.quantity, item.unit, item.rate, item.amount, item.gst_rate,
            item.cgst_amount, item.sgst_amount, item.igst_amount]);
      }
      
      return { billId, billNumber };
    } catch (error) {
      console.error('Error creating bill:', error);
      throw error;
    }
  }

  // Dashboard methods
  static async getDashboardStats() {
    const totalBills = await this.db.getFirstAsync('SELECT COUNT(*) as count FROM bills');
    const totalCustomers = await this.db.getFirstAsync('SELECT COUNT(*) as count FROM customers WHERE is_guest = 0');
    const totalProducts = await this.db.getFirstAsync('SELECT COUNT(*) as count FROM products');
    const totalRevenue = await this.db.getFirstAsync('SELECT SUM(total_amount) as total FROM bills WHERE status != "Cancelled"');
    
    return {
      totalBills: totalBills.count,
      totalCustomers: totalCustomers.count,
      totalProducts: totalProducts.count,
      totalRevenue: totalRevenue.total || 0
    };
  }

  static async getRecentBills(limit = 5) {
    return await this.db.getAllAsync(`
      SELECT b.*, c.name as customer_name 
      FROM bills b 
      LEFT JOIN customers c ON b.customer_id = c.id 
      ORDER BY b.created_at DESC 
      LIMIT ?
    `, [limit]);
  }
}