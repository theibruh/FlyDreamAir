/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/**/*.js"
  ],
  theme: {
    extend: {
      // Custom colors for FlyDreamAir branding, instead of using Tailwind's default color palette
        colors: {
        'dreamAir-purple': '#8B5CF6',
        'dreamAir-cream': '#FFF8DC',
      }
  },
  },
  plugins: [],
}

