import { Transaction } from '@/types';
import { format } from 'date-fns';
import { Edit2, Trash2 } from 'lucide-react';

interface TransactionsTableProps {
  transactions: Transaction[];
  onEdit?: (id: string) => void;
  onDelete?: (id: string) => void;
}

export function TransactionsTable({
  transactions,
  onEdit,
  onDelete,
}: TransactionsTableProps) {
  const getCategoryColor = (category: string) => {
    const colors: Record<string, string> = {
      food: 'bg-orange-100 text-orange-800',
      travel: 'bg-blue-100 text-blue-800',
      shopping: 'bg-pink-100 text-pink-800',
      entertainment: 'bg-purple-100 text-purple-800',
      utilities: 'bg-gray-100 text-gray-800',
      healthcare: 'bg-red-100 text-red-800',
    };
    return colors[category] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="bg-card rounded-lg border border-border shadow-card overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-border bg-gray-50">
              <th className="px-6 py-3 text-left text-xs font-semibold text-secondary-text">
                Date
              </th>
              <th className="px-6 py-3 text-left text-xs font-semibold text-secondary-text">
                Merchant
              </th>
              <th className="px-6 py-3 text-left text-xs font-semibold text-secondary-text">
                Category
              </th>
              <th className="px-6 py-3 text-right text-xs font-semibold text-secondary-text">
                Amount
              </th>
              <th className="px-6 py-3 text-center text-xs font-semibold text-secondary-text">
                Actions
              </th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((transaction) => (
              <tr key={transaction.id} className="border-b border-border hover:bg-gray-50">
                <td className="px-6 py-4 text-sm text-primary-text">
                  {format(new Date(transaction.date), 'MMM dd, yyyy')}
                </td>
                <td className="px-6 py-4 text-sm text-primary-text">
                  {transaction.merchant || 'N/A'}
                </td>
                <td className="px-6 py-4">
                  <span
                    className={`inline-block px-3 py-1 rounded-full text-xs font-medium ${getCategoryColor(
                      transaction.category
                    )}`}
                  >
                    {transaction.category}
                  </span>
                </td>
                <td
                  className={`px-6 py-4 text-right font-semibold ${
                    transaction.type === 'income'
                      ? 'text-green-600'
                      : 'text-primary-text'
                  }`}
                >
                  {transaction.type === 'income' ? '+' : '-'}₹{transaction.amount}
                </td>
                <td className="px-6 py-4 text-center">
                  <div className="flex items-center justify-center gap-2">
                    {onEdit && (
                      <button
                        onClick={() => onEdit(transaction.id)}
                        className="p-1 hover:bg-gray-200 rounded transition-colors"
                      >
                        <Edit2 size={16} className="text-blue-600" />
                      </button>
                    )}
                    {onDelete && (
                      <button
                        onClick={() => onDelete(transaction.id)}
                        className="p-1 hover:bg-gray-200 rounded transition-colors"
                      >
                        <Trash2 size={16} className="text-red-600" />
                      </button>
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
