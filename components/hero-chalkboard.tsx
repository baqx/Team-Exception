"use client";

import React from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { 
  ArrowRight, 
  PlayCircle, 
  Brain, 
  Lightning,
  PencilSimpleLine,
  VideoCamera,
  CursorClick
} from "@phosphor-icons/react";
import { MathTex } from "@/components/math-tex";
import KineticGrid from "@/components/ui/kinetic-grid";

export function HeroChalkboard() {
  const scrollToDemo = () => {
    const el = document.getElementById("interactive-demo");
    if (el) {
      el.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <section className="relative overflow-hidden">
      {/* Interactive Kinetic Grid Canvas Background (White bg with soft charcoal lines) */}
      <KineticGrid 
        globalColor="light" 
        className="pt-20 pb-24 sm:pt-28 sm:pb-32 px-4 sm:px-6 lg:px-8 border-b border-[#E4E4E7]"
      >
        <div className="max-w-5xl mx-auto text-center relative z-10">
          

          {/* Broadened Modern Bold Heading */}
          <motion.h1 
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="font-bold text-4xl sm:text-6xl text-[#09090B] tracking-tight leading-[1.12] max-w-3xl mx-auto"
          >
            Turn any complex idea into an animated chalkboard lesson.
          </motion.h1>

          {/* Broadened Crisp Subtitle */}
          <motion.p 
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="mt-5 text-base sm:text-lg text-[#52525B] max-w-2xl mx-auto leading-relaxed"
          >
            Chalkka diagnoses your question or study notes, uncovers missing foundational prerequisites, and derives the solution on a live animated slate with natural teacher voice pacing. Tuned for STEM, economics, quantitative logic, and complex problem-solving.
          </motion.p>

          {/* Primary Action Buttons */}
          <motion.div 
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3 sm:gap-4"
          >
            <Link
              href="/dashboard"
              className="w-full sm:w-auto px-6 py-3.5 rounded-xl text-sm font-semibold btn-primary inline-flex items-center justify-center gap-2 shadow-sm cursor-pointer"
            >
              <PencilSimpleLine size={18} weight="bold" />
              <span>Open Chalkboard Studio</span>
              <ArrowRight size={15} />
            </Link>

            <button
              onClick={scrollToDemo}
              className="w-full sm:w-auto px-5 py-3.5 rounded-xl text-sm font-medium btn-secondary inline-flex items-center justify-center gap-2 cursor-pointer shadow-2xs"
            >
              <PlayCircle size={18} weight="duotone" className="text-zinc-700" />
              <span>Watch Demo Lesson</span>
            </button>
          </motion.div>

          {/* Free Credits Note */}
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="mt-4 text-xs text-[#71717A] flex items-center justify-center gap-2 font-medium"
          >
            <span className="text-[#09090B] font-semibold">50 free credits upon signup</span>
            <span>•</span>
            <span>No credit card required</span>
          </motion.div>

          {/* Interactive Showcase Mockup Frame with Reveal (Centerpiece Classroom Blackboard) */}
          <motion.div 
            initial={{ opacity: 0, y: 25 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.35 }}
            className="mt-14 max-w-4xl mx-auto rounded-2xl bg-[#09090B] p-2.5 sm:p-4 shadow-2xl text-left border border-zinc-800"
          >
            <div className="rounded-xl bg-[#0F0F12] text-[#F8FAFC] p-5 sm:p-7 relative overflow-hidden border border-zinc-800/80">
              {/* Header */}
              <div className="flex items-center justify-between pb-3 border-b border-zinc-800 text-xs">
                <div className="flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-emerald-400" />
                  <span className="font-semibold text-zinc-200">Thevenin Equivalent Analysis</span>
                  <span className="text-zinc-400 hidden sm:inline">• Circuit Theory & Vector Logic</span>
                </div>
                <span className="text-xs text-zinc-400 font-mono">1080p Voice Narration</span>
              </div>

              {/* Screen Content */}
              <div className="py-6 sm:py-8 space-y-4">
                <div className="text-sm font-medium text-amber-300">
                  Step 1: Deactivate Independent Sources to find Thevenin Resistance (R_th)
                </div>
                <div className="p-4 rounded-lg bg-zinc-900/90 border border-zinc-800 max-w-xl shadow-inner">
                  <MathTex 
                    math="R_{th} = (R_1 \parallel R_3) + (R_2 \parallel R_4) = \frac{R_1 R_3}{R_1 + R_3} + \frac{R_2 R_4}{R_2 + R_4}" 
                    displayMode={true} 
                  />
                </div>
                <div className="text-xs sm:text-sm text-zinc-300 italic">
                  "Notice how zeroing the 12V voltage source turns nodes A and B into two parallel dividers connected in series..."
                </div>
              </div>

              {/* Bottom Bar */}
              <div className="pt-3 border-t border-zinc-800 flex items-center justify-between text-xs text-zinc-400">
                <div className="flex items-center gap-2">
                  <VideoCamera size={15} className="text-emerald-400" />
                  <span>Synthesized in 15 seconds</span>
                </div>
                <Link 
                  href="/dashboard"
                  className="text-zinc-300 hover:text-white font-semibold inline-flex items-center gap-1 transition-colors"
                >
                  <span>Try this with your problem</span>
                  <ArrowRight size={13} />
                </Link>
              </div>
            </div>
          </motion.div>

          {/* 3 Core Highlights (Broadened beyond just STEM) */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="mt-14 grid grid-cols-1 sm:grid-cols-3 gap-5 text-left max-w-4xl mx-auto"
          >
            <div className="modern-card p-6 shadow-xs hover:border-zinc-300 transition-all">
              <div className="w-10 h-10 rounded-xl bg-zinc-100 text-zinc-900 flex items-center justify-center mb-3.5 border border-zinc-200/80">
                <Brain size={22} weight="duotone" />
              </div>
              <h3 className="font-semibold text-base text-[#09090B] mb-1">
                Prerequisite Diagnosis
              </h3>
              <p className="text-xs sm:text-sm text-[#71717A] leading-relaxed">
                Detects why you got stuck and reviews foundational theorems, governing laws, and definitions first.
              </p>
            </div>

            <div className="modern-card p-6 shadow-xs hover:border-zinc-300 transition-all">
              <div className="w-10 h-10 rounded-xl bg-zinc-100 text-zinc-900 flex items-center justify-center mb-3.5 border border-zinc-200/80">
                <Lightning size={22} weight="duotone" />
              </div>
              <h3 className="font-semibold text-base text-[#09090B] mb-1">
                Dynamic Board Derivations
              </h3>
              <p className="text-xs sm:text-sm text-[#71717A] leading-relaxed">
                Draws live formulas, circuit schematics, vector diagrams, economic curves, and boxes verified results.
              </p>
            </div>

            <div className="modern-card p-6 shadow-xs hover:border-zinc-300 transition-all">
              <div className="w-10 h-10 rounded-xl bg-zinc-100 text-zinc-900 flex items-center justify-center mb-3.5 border border-zinc-200/80">
                <PlayCircle size={22} weight="duotone" />
              </div>
              <h3 className="font-semibold text-base text-[#09090B] mb-1">
                Natural Voice Pacing
              </h3>
              <p className="text-xs sm:text-sm text-[#71717A] leading-relaxed">
                Synchronized classroom cadence with deliberate teacher pauses so difficult concepts truly sink in.
              </p>
            </div>
          </motion.div>
        </div>
      </KineticGrid>
    </section>
  );
}

