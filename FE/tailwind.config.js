/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "ui-monospace", "monospace"],
      },
      colors: {
        bg: "#FAFAF9",
        surface: "#FFFFFF",
        border: "#E4E4E7",
        ink: {
          DEFAULT: "#18181B",
          secondary: "#71717A",
          tertiary: "#A1A1AA",
        },
        accent: {
          DEFAULT: "#3B5BFB",
          hover: "#2E48D9",
          soft: "#EEF1FF",
        },
        danger: {
          DEFAULT: "#DC2626",
          soft: "#FEF2F2",
        },
      },
      boxShadow: {
        subtle: "0 1px 2px 0 rgb(0 0 0 / 0.04)",
        panel: "0 1px 3px 0 rgb(0 0 0 / 0.06), 0 1px 2px -1px rgb(0 0 0 / 0.04)",
      },
      keyframes: {
        dotPulse: {
          "0%, 80%, 100%": { opacity: "0.25", transform: "translateY(0)" },
          "40%": { opacity: "1", transform: "translateY(-2px)" },
        },
        fadeIn: {
          "0%": { opacity: "0", transform: "translateY(4px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
      animation: {
        dotPulse: "dotPulse 1.2s ease-in-out infinite",
        fadeIn: "fadeIn 0.2s ease-out",
      },
    },
  },
  plugins: [],
};
