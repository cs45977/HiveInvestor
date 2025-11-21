/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'text-primary': '#20262E',
        'text-secondary': '#BABABA',
        'accent': '#FACEDA',
        'action': '#FF5722',
        'success': '#4CAF50',
        'info': '#2196F3',
      },
      fontFamily: {
        'heading': ['Tisa Pro', 'Georgia', 'serif'],
        'body': ['Open Sans', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
