'use client';

import { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { transactionService } from '@/services/transaction.service';
import { TransactionsTable } from '@/components/dashboard/transactions-table';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Plus, Download } from 'lucide-react';
import { TransactionForm } from '@/components/dashboard/transaction-form';

export default function TransactionsPage() {
  const [showForm, setShowForm] = useState(false);
  const [filterType, setFilterType] = useState<'all' | 'expense' | 'income'>('all');

  const { data: transactions, isLoading, refetch } = useQuery({
    queryKey: ['transactions', filterType],
    queryFn: () =>
      transactionService.getAll(
        filterType !== 'all' ? { type: filterType as 'expense' | 'income' } : {}
      ),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => transactionService.delete(id),
    onSuccess: () => refetch(),
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-primary-text">Transactions</h1>
        <Button
          variant="primary"
          onClick={() => setShowForm(!showForm)}
        >
          <Plus size={18} />
          Add Transaction
        </Button>
      </div>

      {/* Form */}
      {showForm && (
        <Card>
          <CardContent className="pt-6">
            <TransactionForm onSuccess={() => { setShowForm(false); refetch(); }} />
          </CardContent>
        </Card>
      )}

      {/* Filters */}
      <div className="flex gap-2">
        {(['all', 'expense', 'income'] as const).map((type) => (
          <button
            key={type}
            onClick={() => setFilterType(type)}
            className={`px-4 py-2 rounded-lg border transition-colors ${
              filterType === type
                ? 'bg-blue-600 text-white border-blue-600'
                : 'border-border text-secondary-text hover:border-primary-text'
            }`}
          >
            {type.charAt(0).toUpperCase() + type.slice(1)}
          </button>
        ))}
      </div>

      {/* Table */}
      <Card>
        <CardHeader>
          <CardTitle>All Transactions</CardTitle>
        </CardHeader>
        <CardContent>
          {transactions && transactions.transactions && transactions.transactions.length > 0 ? (
            <TransactionsTable
              transactions={transactions.transactions}
              onDelete={(id) => deleteMutation.mutate(id)}
            />
          ) : (
            <p className="text-center text-secondary-text py-8">No transactions found</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
