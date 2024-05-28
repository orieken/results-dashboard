module.exports = {
  content: [
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        base: '#171923',
        primary: '#00ADB5',
        secondary: '#F7F9FC',
        success: '#28A745',
        warning: '#FFC107',
        error: '#DC3545',
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
