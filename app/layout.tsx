import type { Metadata, Viewport } from "next";
import { Plus_Jakarta_Sans } from "next/font/google";
import "./globals.css";
import "katex/dist/katex.min.css";
import { AuthProvider } from "@/lib/auth-context";

const fontSans = Plus_Jakarta_Sans({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800"],
  variable: "--font-sans",
  display: "swap",
});

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
};

export const metadata: Metadata = {
  title: "Chalkka — Turn Any Complex Concept into an Animated Chalkboard Lesson",
  description:
    "Upload any question, homework diagram, or study notes. Chalkka diagnoses foundational prerequisites and generates a step-by-step whiteboard derivation video with natural voice narration across STEM, quantitative fields, economics, and beyond.",
  keywords: [
    "AI chalkboard tutor",
    "whiteboard video generator",
    "concept explainer",
    "math video explanation",
    "STEM explainer",
    "physics and economics tutor",
    "Chalkka",
  ],
  authors: [{ name: "Chalkka Team" }],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={fontSans.variable}>
      <body className="bg-[#FAFAFA] text-[#09090B] font-sans antialiased selection:bg-zinc-200 selection:text-zinc-900 min-h-screen flex flex-col relative">
        {/* Soft Tactile Grain Texture Overlay for Light Theme */}
        <div className="chalk-grain-overlay" aria-hidden="true" />
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
