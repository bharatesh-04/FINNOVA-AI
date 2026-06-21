'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import clsx from 'clsx';
import {
  LayoutDashboard,
  CreditCard,
  PieChart,
  Target,
  BarChart3,
  Zap,
  TrendingUp,
  Heart,
  Bell,
  MessageCircle,
  Settings,
  LogOut,
  Menu,
  X,
  Receipt,
  AlertTriangle,
} from 'lucide-react';
import { useState } from 'react';
import { useAuthStore } from '@/store/auth';

const menuItems = [
  { label: 'Dashboard', icon: LayoutDashboard, href: '/dashboard' },
  {
    label: 'Transactions',
    icon: CreditCard,
    href: '/dashboard/transactions',
    submenu: [
      { label: 'All', href: '/dashboard/transactions' },
      { label: 'Expenses', href: '/dashboard/transactions?type=expense' },
      { label: 'Income', href: '/dashboard/transactions?type=income' },
      { label: 'Categories', href: '/dashboard/transactions/categories' },
    ],
  },
  { label: 'Budgets', icon: PieChart, href: '/dashboard/budgets' },
  { label: 'Goals', icon: Target, href: '/dashboard/goals' },
  { label: 'Reports', icon: BarChart3, href: '/dashboard/reports' },
  { label: 'Insights', icon: Zap, href: '/dashboard/insights' },
  { label: 'Forecasting', icon: TrendingUp, href: '/dashboard/forecasting' },
  { label: 'Financial Health', icon: Heart, href: '/dashboard/health' },
  { label: 'Subscriptions', icon: Bell, href: '/dashboard/subscriptions' },
  { label: 'Fraud Detection', icon: AlertTriangle, href: '/dashboard/fraud' },
  { label: 'Receipt Scanner', icon: Receipt, href: '/dashboard/receipts' },
  { label: 'AI Assistant', icon: MessageCircle, href: '/dashboard/chat' },
  { label: 'Settings', icon: Settings, href: '/dashboard/settings' },
];

export function Sidebar() {
  const [isOpen, setIsOpen] = useState(true);
  const [expandedMenu, setExpandedMenu] = useState<string | null>(null);
  const pathname = usePathname();
  const logout = useAuthStore((state) => state.logout);

  const toggleSubmenu = (label: string) => {
    setExpandedMenu(expandedMenu === label ? null : label);
  };

  const isActive = (href: string) => pathname.startsWith(href);

  return (
    <aside
      className={clsx(
        'bg-sidebar border-r border-border h-screen overflow-y-auto transition-all duration-300',
        isOpen ? 'w-64' : 'w-20'
      )}
    >
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-border">
        {isOpen && <h1 className="text-xl font-bold text-primary-text">Finnova AI</h1>}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="p-1 hover:bg-gray-100 rounded-lg"
        >
          {isOpen ? <X size={20} /> : <Menu size={20} />}
        </button>
      </div>

      {/* Navigation */}
      <nav className="p-4 space-y-1">
        {menuItems.map((item) => (
          <div key={item.label}>
            {item.submenu ? (
              <button
                onClick={() => toggleSubmenu(item.label)}
                className={clsx(
                  'w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors',
                  expandedMenu === item.label
                    ? 'bg-blue-50 text-blue-600'
                    : 'text-secondary-text hover:bg-gray-50'
                )}
              >
                <item.icon size={20} />
                {isOpen && <span className="flex-1 text-left text-sm">{item.label}</span>}
              </button>
            ) : (
              <Link
                href={item.href}
                className={clsx(
                  'flex items-center gap-3 px-3 py-2 rounded-lg transition-colors',
                  isActive(item.href)
                    ? 'bg-blue-600 text-white'
                    : 'text-secondary-text hover:bg-gray-50'
                )}
              >
                <item.icon size={20} />
                {isOpen && <span className="text-sm">{item.label}</span>}
              </Link>
            )}
            {isOpen && item.submenu && expandedMenu === item.label && (
              <div className="mt-1 ml-6 space-y-1 border-l border-border pl-3">
                {item.submenu.map((subitem) => (
                  <Link
                    key={subitem.label}
                    href={subitem.href}
                    className={clsx(
                      'flex items-center px-3 py-2 rounded text-xs transition-colors',
                      isActive(subitem.href)
                        ? 'text-blue-600 font-medium'
                        : 'text-secondary-text hover:text-primary-text'
                    )}
                  >
                    {subitem.label}
                  </Link>
                ))}
              </div>
            )}
          </div>
        ))}
      </nav>

      {/* Footer */}
      {isOpen && (
        <div className="absolute bottom-0 w-full p-4 border-t border-border bg-sidebar">
          <button
            onClick={() => {
              logout();
              window.location.href = '/login';
            }}
            className="w-full flex items-center gap-2 px-3 py-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors text-sm"
          >
            <LogOut size={18} />
            Logout
          </button>
        </div>
      )}
    </aside>
  );
}
