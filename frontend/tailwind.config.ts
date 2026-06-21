import type { Config } from 'tailwindcss';
import defaultTheme from 'tailwindcss/defaultTheme';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: '#F7F7F8',
        sidebar: '#FFFFFF',
        card: '#FFFFFF',
        'primary-text': '#111827',
        'secondary-text': '#6B7280',
        border: '#E5E7EB',
        success: '#22C55E',
        danger: '#EF4444',
        'chart-dark': '#2D2D2D',
        'chart-light': '#D9D9D9',
      },
      fontFamily: {
        sans: ['Inter', ...defaultTheme.fontFamily.sans],
      },
      boxShadow: {
        card: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
        lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
      },
      borderRadius: {
        DEFAULT: '0.5rem',
        lg: '0.75rem',
      },
    },
  },
  darkMode: 'class',
  plugins: [],
};

export default config;
