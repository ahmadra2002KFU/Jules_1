-- ==================================================================
-- MODERN ACCOUNTING SYSTEM - DATABASE SCHEMA
-- Database: SQLite (PoC) / PostgreSQL (Production)
-- Date: 2024-11-05
-- ==================================================================

-- Enable foreign key constraints (SQLite)
PRAGMA foreign_keys = ON;

-- ==================================================================
-- CORE SYSTEM TABLES
-- ==================================================================

-- Companies (Multi-tenancy support)
CREATE TABLE companies (
    id TEXT PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    name_en TEXT NOT NULL,
    name_ar TEXT,
    legal_name TEXT,
    tax_id TEXT,
    commercial_registration TEXT,
    base_currency TEXT NOT NULL DEFAULT 'USD',
    fiscal_year_start INTEGER NOT NULL DEFAULT 1, -- Month (1-12)
    address TEXT,
    phone TEXT,
    email TEXT,
    website TEXT,
    logo_url TEXT,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT
);

-- Fiscal Years
CREATE TABLE fiscal_years (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    year_code TEXT NOT NULL,
    name TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_closed BOOLEAN NOT NULL DEFAULT 0,
    closed_at TIMESTAMP,
    closed_by TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    UNIQUE(company_id, year_code)
);

-- Accounting Periods
CREATE TABLE accounting_periods (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    fiscal_year_id TEXT NOT NULL,
    period_number INTEGER NOT NULL,
    name TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_closed BOOLEAN NOT NULL DEFAULT 0,
    closed_at TIMESTAMP,
    closed_by TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (fiscal_year_id) REFERENCES fiscal_years(id),
    UNIQUE(company_id, fiscal_year_id, period_number)
);

-- ==================================================================
-- CHART OF ACCOUNTS
-- ==================================================================

CREATE TABLE chart_of_accounts (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    account_code TEXT NOT NULL,
    account_name_en TEXT NOT NULL,
    account_name_ar TEXT,
    parent_id TEXT,
    account_type TEXT NOT NULL, -- ASSET, LIABILITY, EQUITY, REVENUE, EXPENSE
    account_subtype TEXT, -- CURRENT, NON_CURRENT, OPERATING, etc.
    account_nature TEXT NOT NULL, -- DEBIT, CREDIT
    level INTEGER NOT NULL,
    is_parent BOOLEAN NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    currency TEXT,
    allow_manual_entry BOOLEAN NOT NULL DEFAULT 1,
    description TEXT,
    opening_balance DECIMAL(20, 4) DEFAULT 0,
    opening_balance_date DATE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (parent_id) REFERENCES chart_of_accounts(id),
    UNIQUE(company_id, account_code)
);

CREATE INDEX idx_coa_company ON chart_of_accounts(company_id);
CREATE INDEX idx_coa_parent ON chart_of_accounts(parent_id);
CREATE INDEX idx_coa_type ON chart_of_accounts(account_type);

-- ==================================================================
-- JOURNAL ENTRIES & GENERAL LEDGER
-- ==================================================================

CREATE TABLE journal_entries (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    entry_number TEXT NOT NULL,
    entry_date DATE NOT NULL,
    posting_date DATE NOT NULL,
    fiscal_year_id TEXT NOT NULL,
    period_id TEXT NOT NULL,
    entry_type TEXT NOT NULL, -- MANUAL, INVOICE, PAYMENT, SYSTEM, etc.
    reference TEXT,
    description TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'DRAFT', -- DRAFT, PENDING, APPROVED, POSTED, REVERSED
    total_debit DECIMAL(20, 4) NOT NULL DEFAULT 0,
    total_credit DECIMAL(20, 4) NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    exchange_rate DECIMAL(10, 6) DEFAULT 1,
    is_reversed BOOLEAN NOT NULL DEFAULT 0,
    reversed_entry_id TEXT,
    reversal_date DATE,
    source_document_type TEXT,
    source_document_id TEXT,
    approved_at TIMESTAMP,
    approved_by TEXT,
    posted_at TIMESTAMP,
    posted_by TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (fiscal_year_id) REFERENCES fiscal_years(id),
    FOREIGN KEY (period_id) REFERENCES accounting_periods(id),
    FOREIGN KEY (reversed_entry_id) REFERENCES journal_entries(id),
    UNIQUE(company_id, entry_number)
);

CREATE INDEX idx_je_company ON journal_entries(company_id);
CREATE INDEX idx_je_date ON journal_entries(entry_date);
CREATE INDEX idx_je_status ON journal_entries(status);
CREATE INDEX idx_je_fiscal_year ON journal_entries(fiscal_year_id);

CREATE TABLE journal_entry_lines (
    id TEXT PRIMARY KEY,
    journal_entry_id TEXT NOT NULL,
    company_id TEXT NOT NULL,
    line_number INTEGER NOT NULL,
    account_id TEXT NOT NULL,
    debit_amount DECIMAL(20, 4) NOT NULL DEFAULT 0,
    credit_amount DECIMAL(20, 4) NOT NULL DEFAULT 0,
    description TEXT,
    cost_center_id TEXT,
    project_id TEXT,
    department_id TEXT,
    currency TEXT,
    exchange_rate DECIMAL(10, 6) DEFAULT 1,
    reference TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (journal_entry_id) REFERENCES journal_entries(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (account_id) REFERENCES chart_of_accounts(id),
    FOREIGN KEY (cost_center_id) REFERENCES cost_centers(id),
    FOREIGN KEY (project_id) REFERENCES projects(id),
    UNIQUE(journal_entry_id, line_number)
);

CREATE INDEX idx_jel_entry ON journal_entry_lines(journal_entry_id);
CREATE INDEX idx_jel_account ON journal_entry_lines(account_id);
CREATE INDEX idx_jel_cost_center ON journal_entry_lines(cost_center_id);

-- General Ledger (Materialized view of posted journal entry lines)
CREATE TABLE general_ledger (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    account_id TEXT NOT NULL,
    entry_date DATE NOT NULL,
    posting_date DATE NOT NULL,
    fiscal_year_id TEXT NOT NULL,
    period_id TEXT NOT NULL,
    journal_entry_id TEXT NOT NULL,
    journal_entry_line_id TEXT NOT NULL,
    debit_amount DECIMAL(20, 4) NOT NULL DEFAULT 0,
    credit_amount DECIMAL(20, 4) NOT NULL DEFAULT 0,
    running_balance DECIMAL(20, 4),
    description TEXT,
    cost_center_id TEXT,
    project_id TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (account_id) REFERENCES chart_of_accounts(id),
    FOREIGN KEY (fiscal_year_id) REFERENCES fiscal_years(id),
    FOREIGN KEY (period_id) REFERENCES accounting_periods(id),
    FOREIGN KEY (journal_entry_id) REFERENCES journal_entries(id),
    FOREIGN KEY (journal_entry_line_id) REFERENCES journal_entry_lines(id)
);

CREATE INDEX idx_gl_company ON general_ledger(company_id);
CREATE INDEX idx_gl_account ON general_ledger(account_id);
CREATE INDEX idx_gl_date ON general_ledger(entry_date);
CREATE INDEX idx_gl_period ON general_ledger(period_id);

-- ==================================================================
-- CUSTOMERS & ACCOUNTS RECEIVABLE
-- ==================================================================

CREATE TABLE customers (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    customer_code TEXT NOT NULL,
    customer_name_en TEXT NOT NULL,
    customer_name_ar TEXT,
    customer_type TEXT DEFAULT 'REGULAR', -- REGULAR, VIP, CORPORATE
    contact_person TEXT,
    email TEXT,
    phone TEXT,
    mobile TEXT,
    website TEXT,
    tax_id TEXT,
    commercial_registration TEXT,
    billing_address TEXT,
    shipping_address TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    postal_code TEXT,
    payment_terms_id TEXT,
    credit_limit DECIMAL(20, 4) DEFAULT 0,
    price_list_id TEXT,
    salesperson_id TEXT,
    account_id TEXT, -- AR account in COA
    is_active BOOLEAN NOT NULL DEFAULT 1,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (payment_terms_id) REFERENCES payment_terms(id),
    FOREIGN KEY (account_id) REFERENCES chart_of_accounts(id),
    UNIQUE(company_id, customer_code)
);

CREATE INDEX idx_customers_company ON customers(company_id);
CREATE INDEX idx_customers_name ON customers(customer_name_en);

CREATE TABLE invoices (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    invoice_number TEXT NOT NULL,
    invoice_type TEXT NOT NULL DEFAULT 'STANDARD', -- STANDARD, CREDIT_NOTE, DEBIT_NOTE, PROFORMA
    invoice_date DATE NOT NULL,
    due_date DATE NOT NULL,
    customer_id TEXT NOT NULL,
    fiscal_year_id TEXT NOT NULL,
    period_id TEXT NOT NULL,
    currency TEXT NOT NULL DEFAULT 'USD',
    exchange_rate DECIMAL(10, 6) DEFAULT 1,
    subtotal DECIMAL(20, 4) NOT NULL DEFAULT 0,
    discount_percentage DECIMAL(5, 2) DEFAULT 0,
    discount_amount DECIMAL(20, 4) DEFAULT 0,
    tax_amount DECIMAL(20, 4) DEFAULT 0,
    total_amount DECIMAL(20, 4) NOT NULL DEFAULT 0,
    paid_amount DECIMAL(20, 4) DEFAULT 0,
    balance_amount DECIMAL(20, 4) NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'DRAFT', -- DRAFT, SENT, PARTIALLY_PAID, PAID, OVERDUE, CANCELLED
    payment_terms_id TEXT,
    reference TEXT,
    notes TEXT,
    internal_notes TEXT,
    journal_entry_id TEXT,
    related_invoice_id TEXT, -- For credit/debit notes
    is_posted BOOLEAN NOT NULL DEFAULT 0,
    posted_at TIMESTAMP,
    posted_by TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (fiscal_year_id) REFERENCES fiscal_years(id),
    FOREIGN KEY (period_id) REFERENCES accounting_periods(id),
    FOREIGN KEY (payment_terms_id) REFERENCES payment_terms(id),
    FOREIGN KEY (journal_entry_id) REFERENCES journal_entries(id),
    FOREIGN KEY (related_invoice_id) REFERENCES invoices(id),
    UNIQUE(company_id, invoice_number)
);

CREATE INDEX idx_invoices_company ON invoices(company_id);
CREATE INDEX idx_invoices_customer ON invoices(customer_id);
CREATE INDEX idx_invoices_date ON invoices(invoice_date);
CREATE INDEX idx_invoices_status ON invoices(status);

CREATE TABLE invoice_lines (
    id TEXT PRIMARY KEY,
    invoice_id TEXT NOT NULL,
    company_id TEXT NOT NULL,
    line_number INTEGER NOT NULL,
    item_id TEXT,
    description TEXT NOT NULL,
    quantity DECIMAL(20, 4) NOT NULL DEFAULT 1,
    unit_price DECIMAL(20, 4) NOT NULL DEFAULT 0,
    discount_percentage DECIMAL(5, 2) DEFAULT 0,
    discount_amount DECIMAL(20, 4) DEFAULT 0,
    tax_code_id TEXT,
    tax_percentage DECIMAL(5, 2) DEFAULT 0,
    tax_amount DECIMAL(20, 4) DEFAULT 0,
    line_total DECIMAL(20, 4) NOT NULL DEFAULT 0,
    account_id TEXT, -- Revenue account
    cost_center_id TEXT,
    project_id TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (item_id) REFERENCES items(id),
    FOREIGN KEY (tax_code_id) REFERENCES tax_codes(id),
    FOREIGN KEY (account_id) REFERENCES chart_of_accounts(id),
    FOREIGN KEY (cost_center_id) REFERENCES cost_centers(id),
    FOREIGN KEY (project_id) REFERENCES projects(id),
    UNIQUE(invoice_id, line_number)
);

CREATE INDEX idx_invoice_lines_invoice ON invoice_lines(invoice_id);
CREATE INDEX idx_invoice_lines_item ON invoice_lines(item_id);

-- ==================================================================
-- VENDORS & ACCOUNTS PAYABLE
-- ==================================================================

CREATE TABLE vendors (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    vendor_code TEXT NOT NULL,
    vendor_name_en TEXT NOT NULL,
    vendor_name_ar TEXT,
    vendor_type TEXT DEFAULT 'REGULAR', -- REGULAR, PREFERRED
    contact_person TEXT,
    email TEXT,
    phone TEXT,
    mobile TEXT,
    website TEXT,
    tax_id TEXT,
    commercial_registration TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    postal_code TEXT,
    payment_terms_id TEXT,
    bank_name TEXT,
    bank_account_number TEXT,
    iban TEXT,
    swift_code TEXT,
    payment_method TEXT, -- BANK_TRANSFER, CHECK, CASH
    account_id TEXT, -- AP account in COA
    is_active BOOLEAN NOT NULL DEFAULT 1,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (payment_terms_id) REFERENCES payment_terms(id),
    FOREIGN KEY (account_id) REFERENCES chart_of_accounts(id),
    UNIQUE(company_id, vendor_code)
);

CREATE INDEX idx_vendors_company ON vendors(company_id);
CREATE INDEX idx_vendors_name ON vendors(vendor_name_en);

CREATE TABLE bills (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    bill_number TEXT NOT NULL,
    bill_type TEXT NOT NULL DEFAULT 'STANDARD', -- STANDARD, CREDIT_NOTE, DEBIT_NOTE
    bill_date DATE NOT NULL,
    due_date DATE NOT NULL,
    vendor_id TEXT NOT NULL,
    vendor_invoice_number TEXT,
    fiscal_year_id TEXT NOT NULL,
    period_id TEXT NOT NULL,
    currency TEXT NOT NULL DEFAULT 'USD',
    exchange_rate DECIMAL(10, 6) DEFAULT 1,
    subtotal DECIMAL(20, 4) NOT NULL DEFAULT 0,
    discount_percentage DECIMAL(5, 2) DEFAULT 0,
    discount_amount DECIMAL(20, 4) DEFAULT 0,
    tax_amount DECIMAL(20, 4) DEFAULT 0,
    total_amount DECIMAL(20, 4) NOT NULL DEFAULT 0,
    paid_amount DECIMAL(20, 4) DEFAULT 0,
    balance_amount DECIMAL(20, 4) NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'DRAFT', -- DRAFT, APPROVED, PARTIALLY_PAID, PAID, OVERDUE, CANCELLED
    payment_terms_id TEXT,
    reference TEXT,
    notes TEXT,
    internal_notes TEXT,
    journal_entry_id TEXT,
    related_bill_id TEXT, -- For credit/debit notes
    purchase_order_id TEXT,
    is_posted BOOLEAN NOT NULL DEFAULT 0,
    posted_at TIMESTAMP,
    posted_by TEXT,
    approved_at TIMESTAMP,
    approved_by TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (vendor_id) REFERENCES vendors(id),
    FOREIGN KEY (fiscal_year_id) REFERENCES fiscal_years(id),
    FOREIGN KEY (period_id) REFERENCES accounting_periods(id),
    FOREIGN KEY (payment_terms_id) REFERENCES payment_terms(id),
    FOREIGN KEY (journal_entry_id) REFERENCES journal_entries(id),
    FOREIGN KEY (related_bill_id) REFERENCES bills(id),
    UNIQUE(company_id, bill_number)
);

CREATE INDEX idx_bills_company ON bills(company_id);
CREATE INDEX idx_bills_vendor ON bills(vendor_id);
CREATE INDEX idx_bills_date ON bills(bill_date);
CREATE INDEX idx_bills_status ON bills(status);

CREATE TABLE bill_lines (
    id TEXT PRIMARY KEY,
    bill_id TEXT NOT NULL,
    company_id TEXT NOT NULL,
    line_number INTEGER NOT NULL,
    item_id TEXT,
    description TEXT NOT NULL,
    quantity DECIMAL(20, 4) NOT NULL DEFAULT 1,
    unit_price DECIMAL(20, 4) NOT NULL DEFAULT 0,
    discount_percentage DECIMAL(5, 2) DEFAULT 0,
    discount_amount DECIMAL(20, 4) DEFAULT 0,
    tax_code_id TEXT,
    tax_percentage DECIMAL(5, 2) DEFAULT 0,
    tax_amount DECIMAL(20, 4) DEFAULT 0,
    line_total DECIMAL(20, 4) NOT NULL DEFAULT 0,
    account_id TEXT, -- Expense/Asset account
    cost_center_id TEXT,
    project_id TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (bill_id) REFERENCES bills(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (item_id) REFERENCES items(id),
    FOREIGN KEY (tax_code_id) REFERENCES tax_codes(id),
    FOREIGN KEY (account_id) REFERENCES chart_of_accounts(id),
    FOREIGN KEY (cost_center_id) REFERENCES cost_centers(id),
    FOREIGN KEY (project_id) REFERENCES projects(id),
    UNIQUE(bill_id, line_number)
);

CREATE INDEX idx_bill_lines_bill ON bill_lines(bill_id);
CREATE INDEX idx_bill_lines_item ON bill_lines(item_id);

-- ==================================================================
-- PAYMENTS
-- ==================================================================

CREATE TABLE payments (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    payment_number TEXT NOT NULL,
    payment_type TEXT NOT NULL, -- RECEIPT (AR), PAYMENT (AP)
    payment_date DATE NOT NULL,
    fiscal_year_id TEXT NOT NULL,
    period_id TEXT NOT NULL,
    party_type TEXT NOT NULL, -- CUSTOMER, VENDOR
    party_id TEXT NOT NULL, -- customer_id or vendor_id
    payment_method TEXT NOT NULL, -- CASH, CHECK, BANK_TRANSFER, CREDIT_CARD
    bank_account_id TEXT,
    reference TEXT,
    check_number TEXT,
    check_date DATE,
    currency TEXT NOT NULL DEFAULT 'USD',
    exchange_rate DECIMAL(10, 6) DEFAULT 1,
    total_amount DECIMAL(20, 4) NOT NULL DEFAULT 0,
    allocated_amount DECIMAL(20, 4) DEFAULT 0,
    unallocated_amount DECIMAL(20, 4) DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'DRAFT', -- DRAFT, POSTED, CLEARED, BOUNCED, CANCELLED
    notes TEXT,
    journal_entry_id TEXT,
    is_posted BOOLEAN NOT NULL DEFAULT 0,
    posted_at TIMESTAMP,
    posted_by TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (fiscal_year_id) REFERENCES fiscal_years(id),
    FOREIGN KEY (period_id) REFERENCES accounting_periods(id),
    FOREIGN KEY (bank_account_id) REFERENCES bank_accounts(id),
    FOREIGN KEY (journal_entry_id) REFERENCES journal_entries(id),
    UNIQUE(company_id, payment_number)
);

CREATE INDEX idx_payments_company ON payments(company_id);
CREATE INDEX idx_payments_party ON payments(party_id);
CREATE INDEX idx_payments_date ON payments(payment_date);
CREATE INDEX idx_payments_type ON payments(payment_type);

CREATE TABLE payment_allocations (
    id TEXT PRIMARY KEY,
    payment_id TEXT NOT NULL,
    company_id TEXT NOT NULL,
    document_type TEXT NOT NULL, -- INVOICE, BILL
    document_id TEXT NOT NULL, -- invoice_id or bill_id
    allocated_amount DECIMAL(20, 4) NOT NULL DEFAULT 0,
    allocation_date DATE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (payment_id) REFERENCES payments(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

CREATE INDEX idx_payment_allocations_payment ON payment_allocations(payment_id);
CREATE INDEX idx_payment_allocations_document ON payment_allocations(document_id);

-- ==================================================================
-- BANKING
-- ==================================================================

CREATE TABLE bank_accounts (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    account_code TEXT NOT NULL,
    account_name TEXT NOT NULL,
    bank_name TEXT NOT NULL,
    account_number TEXT,
    iban TEXT,
    swift_code TEXT,
    branch_name TEXT,
    currency TEXT NOT NULL DEFAULT 'USD',
    account_type TEXT DEFAULT 'CHECKING', -- CHECKING, SAVINGS, CREDIT
    gl_account_id TEXT NOT NULL, -- Link to COA
    opening_balance DECIMAL(20, 4) DEFAULT 0,
    current_balance DECIMAL(20, 4) DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (gl_account_id) REFERENCES chart_of_accounts(id),
    UNIQUE(company_id, account_code)
);

CREATE INDEX idx_bank_accounts_company ON bank_accounts(company_id);

CREATE TABLE bank_transactions (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    bank_account_id TEXT NOT NULL,
    transaction_date DATE NOT NULL,
    value_date DATE,
    description TEXT,
    reference TEXT,
    transaction_type TEXT NOT NULL, -- DEPOSIT, WITHDRAWAL, FEE, INTEREST
    amount DECIMAL(20, 4) NOT NULL,
    balance DECIMAL(20, 4),
    is_reconciled BOOLEAN NOT NULL DEFAULT 0,
    reconciliation_id TEXT,
    matched_journal_entry_id TEXT,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (bank_account_id) REFERENCES bank_accounts(id),
    FOREIGN KEY (reconciliation_id) REFERENCES bank_reconciliations(id),
    FOREIGN KEY (matched_journal_entry_id) REFERENCES journal_entries(id)
);

CREATE INDEX idx_bank_trans_company ON bank_transactions(company_id);
CREATE INDEX idx_bank_trans_account ON bank_transactions(bank_account_id);
CREATE INDEX idx_bank_trans_date ON bank_transactions(transaction_date);

CREATE TABLE bank_reconciliations (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    bank_account_id TEXT NOT NULL,
    reconciliation_date DATE NOT NULL,
    statement_date DATE NOT NULL,
    statement_balance DECIMAL(20, 4) NOT NULL,
    gl_balance DECIMAL(20, 4) NOT NULL,
    adjusted_balance DECIMAL(20, 4),
    is_balanced BOOLEAN NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'IN_PROGRESS', -- IN_PROGRESS, COMPLETED
    notes TEXT,
    completed_at TIMESTAMP,
    completed_by TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (bank_account_id) REFERENCES bank_accounts(id)
);

CREATE INDEX idx_bank_recon_company ON bank_reconciliations(company_id);
CREATE INDEX idx_bank_recon_account ON bank_reconciliations(bank_account_id);

-- ==================================================================
-- INVENTORY MANAGEMENT
-- ==================================================================

CREATE TABLE item_categories (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    code TEXT NOT NULL,
    name_en TEXT NOT NULL,
    name_ar TEXT,
    parent_id TEXT,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (parent_id) REFERENCES item_categories(id),
    UNIQUE(company_id, code)
);

CREATE TABLE items (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    item_code TEXT NOT NULL,
    item_name_en TEXT NOT NULL,
    item_name_ar TEXT,
    category_id TEXT,
    item_type TEXT NOT NULL DEFAULT 'INVENTORY', -- INVENTORY, NON_INVENTORY, SERVICE
    unit_of_measure TEXT NOT NULL,
    barcode TEXT,
    sku TEXT,
    description TEXT,
    costing_method TEXT NOT NULL DEFAULT 'WEIGHTED_AVG', -- FIFO, LIFO, WEIGHTED_AVG, SPECIFIC
    standard_cost DECIMAL(20, 4) DEFAULT 0,
    sales_price DECIMAL(20, 4) DEFAULT 0,
    purchase_price DECIMAL(20, 4) DEFAULT 0,
    reorder_level DECIMAL(20, 4) DEFAULT 0,
    reorder_quantity DECIMAL(20, 4) DEFAULT 0,
    track_inventory BOOLEAN NOT NULL DEFAULT 1,
    track_serial_numbers BOOLEAN NOT NULL DEFAULT 0,
    track_lot_numbers BOOLEAN NOT NULL DEFAULT 0,
    sales_account_id TEXT,
    purchase_account_id TEXT,
    inventory_account_id TEXT,
    cogs_account_id TEXT,
    default_tax_code_id TEXT,
    image_url TEXT,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (category_id) REFERENCES item_categories(id),
    FOREIGN KEY (sales_account_id) REFERENCES chart_of_accounts(id),
    FOREIGN KEY (purchase_account_id) REFERENCES chart_of_accounts(id),
    FOREIGN KEY (inventory_account_id) REFERENCES chart_of_accounts(id),
    FOREIGN KEY (cogs_account_id) REFERENCES chart_of_accounts(id),
    FOREIGN KEY (default_tax_code_id) REFERENCES tax_codes(id),
    UNIQUE(company_id, item_code)
);

CREATE INDEX idx_items_company ON items(company_id);
CREATE INDEX idx_items_category ON items(category_id);
CREATE INDEX idx_items_barcode ON items(barcode);

CREATE TABLE warehouses (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    location TEXT,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    UNIQUE(company_id, code)
);

CREATE TABLE inventory_transactions (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    transaction_number TEXT NOT NULL,
    transaction_date DATE NOT NULL,
    transaction_type TEXT NOT NULL, -- RECEIPT, ISSUE, TRANSFER, ADJUSTMENT
    item_id TEXT NOT NULL,
    warehouse_id TEXT NOT NULL,
    quantity DECIMAL(20, 4) NOT NULL,
    unit_cost DECIMAL(20, 4),
    total_cost DECIMAL(20, 4),
    reference TEXT,
    notes TEXT,
    source_document_type TEXT,
    source_document_id TEXT,
    journal_entry_id TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (item_id) REFERENCES items(id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id),
    FOREIGN KEY (journal_entry_id) REFERENCES journal_entries(id),
    UNIQUE(company_id, transaction_number)
);

CREATE INDEX idx_inv_trans_company ON inventory_transactions(company_id);
CREATE INDEX idx_inv_trans_item ON inventory_transactions(item_id);
CREATE INDEX idx_inv_trans_warehouse ON inventory_transactions(warehouse_id);
CREATE INDEX idx_inv_trans_date ON inventory_transactions(transaction_date);

CREATE TABLE stock_levels (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    item_id TEXT NOT NULL,
    warehouse_id TEXT NOT NULL,
    quantity_on_hand DECIMAL(20, 4) DEFAULT 0,
    quantity_committed DECIMAL(20, 4) DEFAULT 0,
    quantity_available DECIMAL(20, 4) DEFAULT 0,
    quantity_on_order DECIMAL(20, 4) DEFAULT 0,
    average_cost DECIMAL(20, 4) DEFAULT 0,
    total_value DECIMAL(20, 4) DEFAULT 0,
    last_updated TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (item_id) REFERENCES items(id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id),
    UNIQUE(company_id, item_id, warehouse_id)
);

CREATE INDEX idx_stock_levels_item ON stock_levels(item_id);
CREATE INDEX idx_stock_levels_warehouse ON stock_levels(warehouse_id);

-- ==================================================================
-- FIXED ASSETS
-- ==================================================================

CREATE TABLE asset_categories (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    depreciation_method TEXT DEFAULT 'STRAIGHT_LINE', -- STRAIGHT_LINE, DECLINING_BALANCE, UNITS_OF_PRODUCTION
    useful_life_years INTEGER,
    salvage_value_percentage DECIMAL(5, 2),
    asset_account_id TEXT,
    depreciation_account_id TEXT,
    accumulated_depreciation_account_id TEXT,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (asset_account_id) REFERENCES chart_of_accounts(id),
    FOREIGN KEY (depreciation_account_id) REFERENCES chart_of_accounts(id),
    FOREIGN KEY (accumulated_depreciation_account_id) REFERENCES chart_of_accounts(id),
    UNIQUE(company_id, code)
);

CREATE TABLE fixed_assets (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    asset_code TEXT NOT NULL,
    asset_name TEXT NOT NULL,
    category_id TEXT NOT NULL,
    serial_number TEXT,
    description TEXT,
    purchase_date DATE NOT NULL,
    purchase_cost DECIMAL(20, 4) NOT NULL,
    salvage_value DECIMAL(20, 4) DEFAULT 0,
    useful_life_years INTEGER NOT NULL,
    depreciation_method TEXT NOT NULL,
    depreciation_start_date DATE,
    location TEXT,
    custodian TEXT,
    vendor_id TEXT,
    warranty_expiry_date DATE,
    status TEXT DEFAULT 'ACTIVE', -- ACTIVE, DISPOSED, SCRAPPED
    disposal_date DATE,
    disposal_amount DECIMAL(20, 4),
    disposal_notes TEXT,
    image_url TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (category_id) REFERENCES asset_categories(id),
    FOREIGN KEY (vendor_id) REFERENCES vendors(id),
    UNIQUE(company_id, asset_code)
);

CREATE INDEX idx_assets_company ON fixed_assets(company_id);
CREATE INDEX idx_assets_category ON fixed_assets(category_id);

CREATE TABLE depreciation_schedules (
    id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    company_id TEXT NOT NULL,
    fiscal_year_id TEXT NOT NULL,
    period_id TEXT NOT NULL,
    depreciation_date DATE NOT NULL,
    opening_book_value DECIMAL(20, 4) NOT NULL,
    depreciation_amount DECIMAL(20, 4) NOT NULL,
    accumulated_depreciation DECIMAL(20, 4) NOT NULL,
    closing_book_value DECIMAL(20, 4) NOT NULL,
    journal_entry_id TEXT,
    is_posted BOOLEAN NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (asset_id) REFERENCES fixed_assets(id),
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (fiscal_year_id) REFERENCES fiscal_years(id),
    FOREIGN KEY (period_id) REFERENCES accounting_periods(id),
    FOREIGN KEY (journal_entry_id) REFERENCES journal_entries(id)
);

CREATE INDEX idx_depr_schedules_asset ON depreciation_schedules(asset_id);
CREATE INDEX idx_depr_schedules_period ON depreciation_schedules(period_id);

-- ==================================================================
-- COST CENTERS & PROJECTS
-- ==================================================================

CREATE TABLE cost_centers (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    code TEXT NOT NULL,
    name_en TEXT NOT NULL,
    name_ar TEXT,
    parent_id TEXT,
    type TEXT DEFAULT 'DEPARTMENT', -- DEPARTMENT, BRANCH, DIVISION
    manager TEXT,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (parent_id) REFERENCES cost_centers(id),
    UNIQUE(company_id, code)
);

CREATE INDEX idx_cost_centers_company ON cost_centers(company_id);

CREATE TABLE projects (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    customer_id TEXT,
    project_manager TEXT,
    start_date DATE,
    end_date DATE,
    budget DECIMAL(20, 4),
    status TEXT DEFAULT 'ACTIVE', -- ACTIVE, COMPLETED, CANCELLED
    is_billable BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    UNIQUE(company_id, code)
);

CREATE INDEX idx_projects_company ON projects(company_id);

-- ==================================================================
-- BUDGETS
-- ==================================================================

CREATE TABLE budgets (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    budget_code TEXT NOT NULL,
    budget_name TEXT NOT NULL,
    fiscal_year_id TEXT NOT NULL,
    budget_type TEXT DEFAULT 'ANNUAL', -- ANNUAL, QUARTERLY, MONTHLY
    version TEXT DEFAULT 'ORIGINAL', -- ORIGINAL, REVISED
    status TEXT DEFAULT 'DRAFT', -- DRAFT, APPROVED, ACTIVE, CLOSED
    description TEXT,
    approved_at TIMESTAMP,
    approved_by TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (fiscal_year_id) REFERENCES fiscal_years(id),
    UNIQUE(company_id, budget_code)
);

CREATE TABLE budget_lines (
    id TEXT PRIMARY KEY,
    budget_id TEXT NOT NULL,
    company_id TEXT NOT NULL,
    account_id TEXT NOT NULL,
    cost_center_id TEXT,
    project_id TEXT,
    period_id TEXT,
    budget_amount DECIMAL(20, 4) NOT NULL DEFAULT 0,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (budget_id) REFERENCES budgets(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (account_id) REFERENCES chart_of_accounts(id),
    FOREIGN KEY (cost_center_id) REFERENCES cost_centers(id),
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (period_id) REFERENCES accounting_periods(id)
);

CREATE INDEX idx_budget_lines_budget ON budget_lines(budget_id);
CREATE INDEX idx_budget_lines_account ON budget_lines(account_id);

-- ==================================================================
-- TAX MANAGEMENT
-- ==================================================================

CREATE TABLE tax_codes (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    tax_type TEXT NOT NULL, -- VAT, SALES_TAX, WITHHOLDING_TAX
    rate DECIMAL(5, 2) NOT NULL,
    description TEXT,
    is_compound BOOLEAN NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    tax_account_id TEXT, -- Tax payable/receivable account
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (tax_account_id) REFERENCES chart_of_accounts(id),
    UNIQUE(company_id, code)
);

CREATE INDEX idx_tax_codes_company ON tax_codes(company_id);

-- ==================================================================
-- CURRENCIES & EXCHANGE RATES
-- ==================================================================

CREATE TABLE currencies (
    id TEXT PRIMARY KEY,
    code TEXT NOT NULL UNIQUE, -- ISO 4217 (USD, EUR, SAR, AED)
    name TEXT NOT NULL,
    symbol TEXT,
    decimal_places INTEGER DEFAULT 2,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE exchange_rates (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    from_currency TEXT NOT NULL,
    to_currency TEXT NOT NULL,
    rate DECIMAL(10, 6) NOT NULL,
    effective_date DATE NOT NULL,
    source TEXT, -- MANUAL, API, CENTRAL_BANK
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (from_currency) REFERENCES currencies(code),
    FOREIGN KEY (to_currency) REFERENCES currencies(code),
    UNIQUE(company_id, from_currency, to_currency, effective_date)
);

CREATE INDEX idx_exchange_rates_company ON exchange_rates(company_id);
CREATE INDEX idx_exchange_rates_date ON exchange_rates(effective_date);

-- ==================================================================
-- PAYMENT TERMS
-- ==================================================================

CREATE TABLE payment_terms (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    net_days INTEGER NOT NULL DEFAULT 0,
    discount_percentage DECIMAL(5, 2) DEFAULT 0,
    discount_days INTEGER DEFAULT 0,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    UNIQUE(company_id, code)
);

-- ==================================================================
-- DOCUMENTS & ATTACHMENTS
-- ==================================================================

CREATE TABLE documents (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    document_number TEXT NOT NULL,
    document_type TEXT NOT NULL, -- RECEIPT, INVOICE, CONTRACT, etc.
    entity_type TEXT, -- JOURNAL_ENTRY, INVOICE, BILL, PAYMENT, etc.
    entity_id TEXT, -- ID of the related entity
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_size INTEGER,
    mime_type TEXT,
    file_hash TEXT, -- For deduplication
    description TEXT,
    upload_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    uploaded_by TEXT,
    is_processed BOOLEAN NOT NULL DEFAULT 0, -- For AI processing
    processing_status TEXT, -- PENDING, PROCESSING, COMPLETED, FAILED
    extraction_data TEXT, -- JSON data extracted by AI
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

CREATE INDEX idx_documents_company ON documents(company_id);
CREATE INDEX idx_documents_entity ON documents(entity_id);

-- ==================================================================
-- AI & MACHINE LEARNING
-- ==================================================================

CREATE TABLE ai_training_data (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    data_type TEXT NOT NULL, -- CATEGORIZATION, MATCHING, PREDICTION
    input_data TEXT NOT NULL, -- JSON
    output_data TEXT NOT NULL, -- JSON
    confidence_score DECIMAL(5, 4),
    is_validated BOOLEAN NOT NULL DEFAULT 0,
    validated_by TEXT,
    validated_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

CREATE INDEX idx_ai_training_company ON ai_training_data(company_id);
CREATE INDEX idx_ai_training_type ON ai_training_data(data_type);

CREATE TABLE ai_predictions (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    prediction_type TEXT NOT NULL, -- CASH_FLOW, SALES, CATEGORIZATION
    entity_type TEXT,
    entity_id TEXT,
    input_features TEXT, -- JSON
    prediction_value TEXT, -- JSON
    confidence_score DECIMAL(5, 4),
    model_version TEXT,
    prediction_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actual_value TEXT, -- For feedback loop
    accuracy_score DECIMAL(5, 4),
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

CREATE INDEX idx_ai_predictions_company ON ai_predictions(company_id);
CREATE INDEX idx_ai_predictions_type ON ai_predictions(prediction_type);

CREATE TABLE ai_chat_history (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    session_id TEXT NOT NULL,
    message_type TEXT NOT NULL, -- USER, ASSISTANT, SYSTEM
    message_text TEXT NOT NULL,
    message_metadata TEXT, -- JSON
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_ai_chat_company ON ai_chat_history(company_id);
CREATE INDEX idx_ai_chat_session ON ai_chat_history(session_id);

-- ==================================================================
-- USER MANAGEMENT & SECURITY
-- ==================================================================

CREATE TABLE users (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    full_name TEXT,
    phone TEXT,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    is_superuser BOOLEAN NOT NULL DEFAULT 0,
    last_login TIMESTAMP,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP,
    password_changed_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);

CREATE TABLE roles (
    id TEXT PRIMARY KEY,
    company_id TEXT,
    role_name TEXT NOT NULL,
    role_code TEXT NOT NULL,
    description TEXT,
    is_system_role BOOLEAN NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    UNIQUE(company_id, role_code)
);

CREATE TABLE permissions (
    id TEXT PRIMARY KEY,
    module TEXT NOT NULL,
    resource TEXT NOT NULL,
    action TEXT NOT NULL, -- CREATE, READ, UPDATE, DELETE, APPROVE, etc.
    description TEXT,
    UNIQUE(module, resource, action)
);

CREATE TABLE role_permissions (
    id TEXT PRIMARY KEY,
    role_id TEXT NOT NULL,
    permission_id TEXT NOT NULL,
    granted BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE,
    UNIQUE(role_id, permission_id)
);

CREATE TABLE user_roles (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    role_id TEXT NOT NULL,
    company_id TEXT NOT NULL,
    assigned_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    assigned_by TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    UNIQUE(user_id, role_id, company_id)
);

CREATE INDEX idx_user_roles_user ON user_roles(user_id);
CREATE INDEX idx_user_roles_company ON user_roles(company_id);

-- ==================================================================
-- AUDIT TRAIL
-- ==================================================================

CREATE TABLE audit_logs (
    id TEXT PRIMARY KEY,
    company_id TEXT,
    user_id TEXT,
    action TEXT NOT NULL, -- CREATE, UPDATE, DELETE, LOGIN, LOGOUT, etc.
    entity_type TEXT NOT NULL,
    entity_id TEXT,
    old_values TEXT, -- JSON
    new_values TEXT, -- JSON
    ip_address TEXT,
    user_agent TEXT,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_audit_company ON audit_logs(company_id);
CREATE INDEX idx_audit_user ON audit_logs(user_id);
CREATE INDEX idx_audit_timestamp ON audit_logs(timestamp);
CREATE INDEX idx_audit_entity ON audit_logs(entity_type, entity_id);

-- ==================================================================
-- SYSTEM CONFIGURATION
-- ==================================================================

CREATE TABLE system_settings (
    id TEXT PRIMARY KEY,
    company_id TEXT,
    setting_key TEXT NOT NULL,
    setting_value TEXT,
    setting_type TEXT, -- STRING, INTEGER, BOOLEAN, JSON
    description TEXT,
    is_editable BOOLEAN NOT NULL DEFAULT 1,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by TEXT,
    UNIQUE(company_id, setting_key)
);

CREATE TABLE sequences (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    sequence_type TEXT NOT NULL, -- INVOICE, BILL, PAYMENT, JOURNAL_ENTRY
    prefix TEXT,
    next_number INTEGER NOT NULL DEFAULT 1,
    suffix TEXT,
    padding INTEGER DEFAULT 5,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    UNIQUE(company_id, sequence_type)
);

-- ==================================================================
-- INITIAL DATA SETUP
-- ==================================================================

-- Insert default currencies
INSERT INTO currencies (id, code, name, symbol, decimal_places) VALUES
('USD', 'USD', 'US Dollar', '$', 2),
('EUR', 'EUR', 'Euro', '€', 2),
('SAR', 'SAR', 'Saudi Riyal', 'ر.س', 2),
('AED', 'AED', 'UAE Dirham', 'د.إ', 2),
('GBP', 'GBP', 'British Pound', '£', 2),
('JPY', 'JPY', 'Japanese Yen', '¥', 0);

-- Insert default permissions
INSERT INTO permissions (id, module, resource, action, description) VALUES
('perm_001', 'ACCOUNTING', 'CHART_OF_ACCOUNTS', 'CREATE', 'Create new accounts'),
('perm_002', 'ACCOUNTING', 'CHART_OF_ACCOUNTS', 'READ', 'View chart of accounts'),
('perm_003', 'ACCOUNTING', 'CHART_OF_ACCOUNTS', 'UPDATE', 'Modify accounts'),
('perm_004', 'ACCOUNTING', 'CHART_OF_ACCOUNTS', 'DELETE', 'Delete accounts'),
('perm_005', 'ACCOUNTING', 'JOURNAL_ENTRY', 'CREATE', 'Create journal entries'),
('perm_006', 'ACCOUNTING', 'JOURNAL_ENTRY', 'READ', 'View journal entries'),
('perm_007', 'ACCOUNTING', 'JOURNAL_ENTRY', 'UPDATE', 'Modify journal entries'),
('perm_008', 'ACCOUNTING', 'JOURNAL_ENTRY', 'DELETE', 'Delete journal entries'),
('perm_009', 'ACCOUNTING', 'JOURNAL_ENTRY', 'POST', 'Post journal entries'),
('perm_010', 'ACCOUNTING', 'JOURNAL_ENTRY', 'APPROVE', 'Approve journal entries'),
('perm_011', 'AR', 'INVOICE', 'CREATE', 'Create invoices'),
('perm_012', 'AR', 'INVOICE', 'READ', 'View invoices'),
('perm_013', 'AR', 'INVOICE', 'UPDATE', 'Modify invoices'),
('perm_014', 'AR', 'INVOICE', 'DELETE', 'Delete invoices'),
('perm_015', 'AR', 'INVOICE', 'POST', 'Post invoices'),
('perm_016', 'AP', 'BILL', 'CREATE', 'Create bills'),
('perm_017', 'AP', 'BILL', 'READ', 'View bills'),
('perm_018', 'AP', 'BILL', 'UPDATE', 'Modify bills'),
('perm_019', 'AP', 'BILL', 'DELETE', 'Delete bills'),
('perm_020', 'AP', 'BILL', 'POST', 'Post bills'),
('perm_021', 'AP', 'BILL', 'APPROVE', 'Approve bills'),
('perm_022', 'BANKING', 'BANK_ACCOUNT', 'CREATE', 'Create bank accounts'),
('perm_023', 'BANKING', 'BANK_ACCOUNT', 'READ', 'View bank accounts'),
('perm_024', 'BANKING', 'RECONCILIATION', 'PERFORM', 'Perform bank reconciliation'),
('perm_025', 'INVENTORY', 'ITEM', 'CREATE', 'Create inventory items'),
('perm_026', 'INVENTORY', 'ITEM', 'READ', 'View inventory items'),
('perm_027', 'INVENTORY', 'ITEM', 'UPDATE', 'Modify inventory items'),
('perm_028', 'INVENTORY', 'TRANSACTION', 'CREATE', 'Create inventory transactions'),
('perm_029', 'REPORTS', 'FINANCIAL_STATEMENTS', 'VIEW', 'View financial statements'),
('perm_030', 'REPORTS', 'MANAGEMENT_REPORTS', 'VIEW', 'View management reports'),
('perm_031', 'SYSTEM', 'USER', 'MANAGE', 'Manage users'),
('perm_032', 'SYSTEM', 'SETTINGS', 'MANAGE', 'Manage system settings');

-- ==================================================================
-- VIEWS FOR REPORTING
-- ==================================================================

-- Trial Balance View
CREATE VIEW view_trial_balance AS
SELECT
    c.id as company_id,
    c.name_en as company_name,
    coa.id as account_id,
    coa.account_code,
    coa.account_name_en,
    coa.account_type,
    coa.account_nature,
    COALESCE(SUM(gl.debit_amount), 0) as total_debit,
    COALESCE(SUM(gl.credit_amount), 0) as total_credit,
    CASE
        WHEN coa.account_nature = 'DEBIT' THEN
            coa.opening_balance + COALESCE(SUM(gl.debit_amount), 0) - COALESCE(SUM(gl.credit_amount), 0)
        ELSE
            coa.opening_balance + COALESCE(SUM(gl.credit_amount), 0) - COALESCE(SUM(gl.debit_amount), 0)
    END as closing_balance
FROM companies c
CROSS JOIN chart_of_accounts coa
LEFT JOIN general_ledger gl ON coa.id = gl.account_id AND coa.company_id = gl.company_id
WHERE coa.company_id = c.id AND coa.is_parent = 0
GROUP BY c.id, coa.id;

-- AR Aging View
CREATE VIEW view_ar_aging AS
SELECT
    i.company_id,
    i.customer_id,
    c.customer_code,
    c.customer_name_en,
    i.id as invoice_id,
    i.invoice_number,
    i.invoice_date,
    i.due_date,
    i.total_amount,
    i.paid_amount,
    i.balance_amount,
    CAST(julianday('now') - julianday(i.due_date) AS INTEGER) as days_overdue,
    CASE
        WHEN julianday('now') <= julianday(i.due_date) THEN i.balance_amount
        ELSE 0
    END as current_amount,
    CASE
        WHEN julianday('now') - julianday(i.due_date) BETWEEN 1 AND 30 THEN i.balance_amount
        ELSE 0
    END as days_1_30,
    CASE
        WHEN julianday('now') - julianday(i.due_date) BETWEEN 31 AND 60 THEN i.balance_amount
        ELSE 0
    END as days_31_60,
    CASE
        WHEN julianday('now') - julianday(i.due_date) BETWEEN 61 AND 90 THEN i.balance_amount
        ELSE 0
    END as days_61_90,
    CASE
        WHEN julianday('now') - julianday(i.due_date) > 90 THEN i.balance_amount
        ELSE 0
    END as days_over_90
FROM invoices i
JOIN customers c ON i.customer_id = c.id
WHERE i.balance_amount > 0 AND i.status != 'CANCELLED';

-- AP Aging View
CREATE VIEW view_ap_aging AS
SELECT
    b.company_id,
    b.vendor_id,
    v.vendor_code,
    v.vendor_name_en,
    b.id as bill_id,
    b.bill_number,
    b.bill_date,
    b.due_date,
    b.total_amount,
    b.paid_amount,
    b.balance_amount,
    CAST(julianday('now') - julianday(b.due_date) AS INTEGER) as days_overdue,
    CASE
        WHEN julianday('now') <= julianday(b.due_date) THEN b.balance_amount
        ELSE 0
    END as current_amount,
    CASE
        WHEN julianday('now') - julianday(b.due_date) BETWEEN 1 AND 30 THEN b.balance_amount
        ELSE 0
    END as days_1_30,
    CASE
        WHEN julianday('now') - julianday(b.due_date) BETWEEN 31 AND 60 THEN b.balance_amount
        ELSE 0
    END as days_31_60,
    CASE
        WHEN julianday('now') - julianday(b.due_date) BETWEEN 61 AND 90 THEN b.balance_amount
        ELSE 0
    END as days_61_90,
    CASE
        WHEN julianday('now') - julianday(b.due_date) > 90 THEN b.balance_amount
        ELSE 0
    END as days_over_90
FROM bills b
JOIN vendors v ON b.vendor_id = v.id
WHERE b.balance_amount > 0 AND b.status != 'CANCELLED';

-- ==================================================================
-- END OF SCHEMA
-- ==================================================================
