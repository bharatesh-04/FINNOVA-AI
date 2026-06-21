'use client';

import { useQuery } from '@tanstack/react-query';
import { transactionService } from '@/services/transaction.service';
import { analyticsService } from '@/services/analytics.service';
import { StatCard } from '@/components/dashboard/stat-card';
import { SpendingChart, CategoryBreakdown, IncomeVsExpenses } from '@/components/dashboard/charts';
import { TransactionsTable } from '@/components/dashboard/transactions-table';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { SPENDING_DATA, CATEGORY_DATA } from '@/lib/constants';
import {
  TrendingDown,
  TrendingUp,
  Wallet,
  PiggyBank,
  Activity,
  Plus,
} from 'lucide-react';
import Link from 'next/link';

export default function DashboardPage() {
  // Fetch dashboard stats
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: () => transactionService.getDashboardStats(),
  });

  // Fetch recent transactions
  const { data: transactions } = useQuery({
    queryKey: ['transactions', { limit: 5, offset: 0 }],
    queryFn: () =>
      transactionService.getAll({
        limit: 5,
        offset: 0,
      }),
  });

  // Fetch financial health
  const { data: health } = useQuery({
    queryKey: ['financial-health'],
    queryFn: () => analyticsService.getFinancialHealth(),
  });

  // Mock data for charts (in production, fetch from API)
  const spendingData = SPENDING_DATA;
  const categoryData = CATEGORY_DATA;

  if (statsLoading) {
    return (
      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-24 bg-gray-200 rounded-lg animate-shimmer"></div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Top Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        <StatCard
          title="Total Balance"
          value={`₹${stats?.total_balance || 0}`}
          icon={<Wallet size={24} />}
          color="blue"
          trend={{ value: 12, isPositive: true }}
        />
        <StatCard
          title="Income"
          value={`₹${stats?.total_income || 0}`}
          icon={<TrendingUp size={24} />}
          color="green"
        />
        <StatCard
          title="Expenses"
          value={`₹${stats?.total_expenses || 0}`}
          icon={<TrendingDown size={24} />}
          color="red"
        />
        <StatCard
          title="Savings"
          value={`₹${stats?.total_savings || 0}`}
          icon={<PiggyBank size={24} />}
          color="purple"
        />
        <StatCard
          title="Health Score"
          value={`${health?.score || 0}/100`}
          icon={<Activity size={24} />}
          color="blue"
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <SpendingChart data={spendingData} />
        <CategoryBreakdown data={categoryData} />
      </div>

      {/* Income vs Expenses */}
      <IncomeVsExpenses data={spendingData} />

      {/* Recent Transactions */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Recent Transactions</CardTitle>
            <Link href="/dashboard/transactions">
              <Button variant="primary" size="sm">
                <Plus size={16} />
                Add Transaction
              </Button>
            </Link>
          </div>
        </CardHeader>
        <CardContent>
          {transactions && transactions.transactions && transactions.transactions.length > 0 ? (
            <TransactionsTable transactions={transactions.transactions} />
          ) : (
            <p className="text-center text-secondary-text py-8">No transactions yet</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
