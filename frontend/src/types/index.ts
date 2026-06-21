// Authentication
export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  role: 'user' | 'premium' | 'admin';
  createdAt: string;
  updatedAt: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
}

// Transaction
export interface Transaction {
  id: string;
  userId: string;
  type: 'expense' | 'income';
  amount: number;
  currency: string;
  category: TransactionCategory;
  merchant?: string;
  description: string;
  date: string;
  receiptId?: string;
  tags: string[];
  isRecurring: boolean;
  recurringFrequency?: 'daily' | 'weekly' | 'monthly' | 'yearly';
  notes?: string;
  createdAt: string;
  updatedAt: string;
}

export type TransactionCategory =
  | 'food'
  | 'travel'
  | 'shopping'
  | 'education'
  | 'healthcare'
  | 'utilities'
  | 'entertainment'
  | 'insurance'
  | 'investments'
  | 'bills'
  | 'subscriptions'
  | 'others';

// Budget
export interface Budget {
  id: string;
  userId: string;
  name: string;
  budgetType: 'category' | 'total' | 'custom';
  amount: number;
  currency: string;
  category?: TransactionCategory;
  startDate: string;
  endDate: string;
  spent: number;
  percentageUsed: number;
  status: 'active' | 'exceeded' | 'completed';
  createdAt: string;
  updatedAt: string;
}

// Goals
export interface Goal {
  id: string;
  userId: string;
  name: string;
  targetAmount: number;
  currentAmount: number;
  currency: string;
  deadline: string;
  category: string;
  priority: 'low' | 'medium' | 'high';
  status: 'active' | 'completed' | 'cancelled';
  monthlyTarget: number;
  createdAt: string;
  updatedAt: string;
}

// Receipt
export interface Receipt {
  id: string;
  userId: string;
  imageUrl: string;
  extractedData: {
    merchantName?: string;
    amount?: number;
    tax?: number;
    date?: string;
    currency?: string;
    items?: ReceiptItem[];
    category?: TransactionCategory;
    confidence: number;
  };
  status: 'pending' | 'processed' | 'failed';
  transactionId?: string;
  createdAt: string;
  updatedAt: string;
}

export interface ReceiptItem {
  description: string;
  quantity: number;
  unitPrice: number;
  total: number;
}

// Subscription
export interface Subscription {
  id: string;
  userId: string;
  name: string;
  amount: number;
  currency: string;
  renewalDate: string;
  frequency: 'monthly' | 'yearly' | 'weekly';
  status: 'active' | 'paused' | 'cancelled';
  category: string;
  paymentMethod?: string;
  createdAt: string;
  updatedAt: string;
}

// Financial Health
export interface FinancialHealth {
  score: number;
  status: 'poor' | 'fair' | 'good' | 'excellent';
  savingsRate: number;
  debtRatio: number;
  incomeStability: number;
  emergencyFund: number;
  budgetAdherence: number;
  recommendations: string[];
  lastUpdated: string;
}

// Insights
export interface Insight {
  id: string;
  userId: string;
  type: string;
  title: string;
  description: string;
  data?: Record<string, unknown>;
  severity: 'info' | 'warning' | 'alert';
  createdAt: string;
}

// Forecast
export interface Forecast {
  id: string;
  userId: string;
  type: 'expense' | 'income' | 'savings';
  period: 'weekly' | 'monthly' | 'annual';
  predictions: ForecastPoint[];
  confidenceInterval: number;
  trend: 'up' | 'down' | 'stable';
  createdAt: string;
}

export interface ForecastPoint {
  date: string;
  predicted: number;
  lower: number;
  upper: number;
}

// Dashboard Stats
export interface DashboardStats {
  totalBalance: number;
  totalIncome: number;
  totalExpenses: number;
  totalSavings: number;
  netWorth: number;
  financialHealthScore: number;
}

// Chat
export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface ChatHistory {
  id: string;
  userId: string;
  messages: ChatMessage[];
  createdAt: string;
  updatedAt: string;
}
