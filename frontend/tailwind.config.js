/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
    './pages/**/*.{js,ts,jsx,tsx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f2f6ff',
          100: '#e6eeff',
          200: '#bcd6ff',
          300: '#8fbfff',
          400: '#5aa6ff',
          500: '#0b3d91',
          600: '#082d6e',
          700: '#061f4e',
          800: '#04132e',
          900: '#020712',
        },
        accent: {
          50: '#fff9f0',
          100: '#fff3e0',
          200: '#ffe0b8',
          300: '#f5c27a',
          400: '#e3a83f',
          500: '#c49a2e',
          600: '#a27920',
          700: '#7a5b17',
          800: '#4e3b0f',
          900: '#241b07',
        },
        tealish: {
          500: '#2aa198'
        }
      },
      fontFamily: {
        sans: ['var(--font-geist-sans)', 'Inter', 'ui-sans-serif', 'system-ui'],
      }
    },
  },
  plugins: [],
}
