/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        lilac: { 50: "#F7F2FB", 100: "#EFE4F6", 300: "#C9B7E6", 500: "#8D82C4", 700: "#544B82" },
        blush: { 50: "#FDF1F5", 100: "#FCE4EC", 300: "#F5B8CC" },
        ink: { DEFAULT: "#211C30", soft: "#6B6380" },
        onyx: "#16141F",
      },
      fontFamily: {
        display: ["Baloo 2", "system-ui", "sans-serif"],
        body: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      boxShadow: {
        soft: "0 8px 30px -12px rgba(84, 75, 130, 0.25)",
      },
      keyframes: {
        breathe: {
          "0%, 100%": { transform: "scale(1)" },
          "50%": { transform: "scale(1.04)" },
        },
        blink: {
          "0%, 90%, 100%": { transform: "scaleY(1)" },
          "95%": { transform: "scaleY(0.1)" },
        },
      },
      animation: {
        breathe: "breathe 4s ease-in-out infinite",
        blink: "blink 4.5s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};
