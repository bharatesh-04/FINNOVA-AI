import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';

export function SpendingChart({ data }: { data: any[] }) {
  return (
    <div className="bg-card rounded-lg border border-border shadow-card p-6">
      <h3 className="text-lg font-semibold text-primary-text mb-4">Monthly Spending</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="expenses"
            stroke="#EF4444"
            strokeWidth={2}
            dot={{ fill: '#EF4444' }}
          />
          <Line
            type="monotone"
            dataKey="income"
            stroke="#22C55E"
            strokeWidth={2}
            dot={{ fill: '#22C55E' }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export function CategoryBreakdown({ data }: { data: any[] }) {
  const colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899'];

  return (
    <div className="bg-card rounded-lg border border-border shadow-card p-6">
      <h3 className="text-lg font-semibold text-primary-text mb-4">Spending by Category</h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie data={data} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={100}>
            {data.map((_, index) => (
              <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export function IncomeVsExpenses({ data }: { data: any[] }) {
  return (
    <div className="bg-card rounded-lg border border-border shadow-card p-6">
      <h3 className="text-lg font-semibold text-primary-text mb-4">Income vs Expenses</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="income" fill="#22C55E" />
          <Bar dataKey="expenses" fill="#EF4444" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
