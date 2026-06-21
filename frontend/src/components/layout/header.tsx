'use client';

import { useAuthStore } from '@/store/auth';
import { useUIStore } from '@/store/ui';
import { Bell, Search, Moon, Sun, User } from 'lucide-react';

export function Header() {
  const user = useAuthStore((state) => state.user);
  const darkMode = useUIStore((state) => state.darkMode);
  const toggleDarkMode = useUIStore((state) => state.toggleDarkMode);

  return (
    <header className="bg-sidebar border-b border-border px-6 py-4 flex items-center justify-between">
      <div className="flex-1">
        <div className="relative">
          <Search
            size={18}
            className="absolute left-3 top-1/2 transform -translate-y-1/2 text-secondary-text"
          />
          <input
            type="text"
            placeholder="Search transactions, budgets..."
            className="w-full pl-10 pr-4 py-2 bg-gray-100 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      <div className="flex items-center gap-4 ml-6">
        <button
          onClick={toggleDarkMode}
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          {darkMode ? <Sun size={20} /> : <Moon size={20} />}
        </button>

        <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors relative">
          <Bell size={20} />
          <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
        </button>

        <div className="flex items-center gap-3 pl-4 border-l border-border">
          <div className="text-right">
            <p className="text-sm font-medium text-primary-text">{user?.name}</p>
            <p className="text-xs text-secondary-text">{user?.role}</p>
          </div>
          <div className="w-10 h-10 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full flex items-center justify-center">
            {user?.avatar ? (
              <img src={user.avatar} alt={user.name} className="w-full h-full rounded-full" />
            ) : (
              <User size={20} className="text-white" />
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
