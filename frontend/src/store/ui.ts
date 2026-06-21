import { create } from 'zustand';

interface UIStore {
  sidebarOpen: boolean;
  darkMode: boolean;
  currency: string;
  setSidebarOpen: (open: boolean) => void;
  toggleDarkMode: () => void;
  setCurrency: (currency: string) => void;
}

export const useUIStore = create<UIStore>((set) => ({
  sidebarOpen: true,
  darkMode: false,
  currency: 'INR',
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
  toggleDarkMode: () => set((state) => ({ darkMode: !state.darkMode })),
  setCurrency: (currency) => set({ currency }),
}));
