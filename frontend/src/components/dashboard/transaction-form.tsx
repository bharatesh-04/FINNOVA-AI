'use client';

import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { transactionService } from '@/services/transaction.service';
import { Button } from '@/components/ui/button';
import { Transaction, TransactionCategory } from '@/types';
import { Calendar, DollarSign, Tag } from 'lucide-react';

interface TransactionFormProps {
  transaction?: Transaction;
  onSuccess?: () => void;
}

const CATEGORIES: TransactionCategory[] = [
  'food',
  'travel',
  'shopping',
  'education',
  'healthcare',
  'utilities',
  'entertainment',
  'insurance',
  'investments',
  'bills',
  'subscriptions',
  'others',
];

export function TransactionForm({ transaction, onSuccess }: TransactionFormProps) {
  const [formData, setFormData] = useState({
    type: transaction?.type || 'expense',
    amount: transaction?.amount || 0,
    category: transaction?.category || 'others',
    merchant: transaction?.merchant || '',
    description: transaction?.description || '',
    date: transaction?.date || new Date().toISOString().split('T')[0],
    tags: transaction?.tags.join(',') || '',
    notes: transaction?.notes || '',
  });

  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const payload = {
        ...formData,
        amount: Number(formData.amount),
        tags: formData.tags.split(',').filter(Boolean),
      };

      if (transaction) {
        await transactionService.update(transaction.id, payload);
      } else {
        await transactionService.create(payload);
      }

      onSuccess?.();
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Type & Amount Row */}
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-primary-text mb-2">Type</label>
          <select
            value={formData.type}
            onChange={(e) => setFormData({ ...formData, type: e.target.value })}
            className="w-full p-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="expense">Expense</option>
            <option value="income">Income</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-primary-text mb-2">Amount</label>
          <div className="relative">
            <DollarSign className="absolute left-3 top-2.5 text-secondary-text" size={18} />
            <input
              type="number"
              value={formData.amount}
              onChange={(e) => setFormData({ ...formData, amount: parseFloat(e.target.value) })}
              className="w-full pl-10 pr-4 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
        </div>
      </div>

      {/* Category & Date Row */}
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-primary-text mb-2">Category</label>
          <select
            value={formData.category}
            onChange={(e) => setFormData({ ...formData, category: e.target.value as TransactionCategory })}
            className="w-full p-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {CATEGORIES.map((cat) => (
              <option key={cat} value={cat}>
                {cat.charAt(0).toUpperCase() + cat.slice(1)}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-primary-text mb-2">Date</label>
          <div className="relative">
            <Calendar className="absolute left-3 top-2.5 text-secondary-text" size={18} />
            <input
              type="date"
              value={formData.date}
              onChange={(e) => setFormData({ ...formData, date: e.target.value })}
              className="w-full pl-10 pr-4 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      </div>

      {/* Merchant */}
      <div>
        <label className="block text-sm font-medium text-primary-text mb-2">Merchant</label>
        <input
          type="text"
          value={formData.merchant}
          onChange={(e) => setFormData({ ...formData, merchant: e.target.value })}
          placeholder="e.g., Starbucks, Amazon"
          className="w-full p-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {/* Description */}
      <div>
        <label className="block text-sm font-medium text-primary-text mb-2">Description</label>
        <input
          type="text"
          value={formData.description}
          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
          placeholder="What was this transaction about?"
          className="w-full p-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>

      {/* Tags */}
      <div>
        <label className="block text-sm font-medium text-primary-text mb-2">Tags</label>
        <div className="relative">
          <Tag className="absolute left-3 top-2.5 text-secondary-text" size={18} />
          <input
            type="text"
            value={formData.tags}
            onChange={(e) => setFormData({ ...formData, tags: e.target.value })}
            placeholder="Separate tags with commas"
            className="w-full pl-10 pr-4 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      {/* Notes */}
      <div>
        <label className="block text-sm font-medium text-primary-text mb-2">Notes</label>
        <textarea
          value={formData.notes}
          onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
          placeholder="Add any notes..."
          rows={3}
          className="w-full p-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {/* Buttons */}
      <div className="flex gap-2 justify-end">
        <Button type="submit" variant="primary" isLoading={isLoading}>
          {transaction ? 'Update' : 'Add'} Transaction
        </Button>
      </div>
    </form>
  );
}
