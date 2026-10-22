"use client";

import React from "react";
import { motion } from "framer-motion";
import { 
  ChalkboardTeacher, 
  Brain, 
  Waveform, 
  ArrowsClockwise, 
  TreeStructure
} from "@phosphor-icons/react";

const PILLARS = [
  {
    icon: TreeStructure,
    title: "Prerequisite Diagnosis",
    description: "Uncovers foundational theorems and formulas you need before solving the target problem.",
  },
  {
    icon: ChalkboardTeacher,
    title: "Step-by-Step Derivation",
    description: "Draws mathematical equations and circuit schematics stroke-by-stroke on a digital blackboard.",
  },
  {
    icon: Waveform,
    title: "Synchronized Voice Narration",
    description: "Natural conversational cadence with deliberate classroom pauses timed to the writing.",
  },
  {
    icon: ArrowsClockwise,
    title: "Adaptive Regeneration",
    description: "Confused by a step? Regenerate alternative explanations for that specific section instantly.",
  }
];

export function TeachingPillars() {
  return (
    <section 
      id="teaching-pillars" 
      className="relative py-20 sm:py-28 px-4 sm:px-6 lg:px-8 border-t border-[#E4E4E7] bg-[#FFFFFF]"
    >
      <div className="max-w-5xl mx-auto">
        {/* Section Title */}
        <motion.div 
          initial={{ opacity: 0, y: 15 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center max-w-2xl mx-auto mb-14"
        >
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-zinc-100 border border-zinc-200 text-xs font-semibold text-zinc-800 mb-4">
            <Brain size={14} weight="duotone" className="text-zinc-900" />
            <span>Pedagogical Core</span>
          </div>
          <h2 className="font-bold text-3xl sm:text-4xl text-[#09090B] tracking-tight">
            Built for deep comprehension, not shortcuts.
          </h2>
          <p className="mt-3 text-base text-[#52525B]">
            Recreating the experience of an expert professor working through problems on a chalkboard.
          </p>
        </motion.div>

        {/* 4 Pillars Grid (Clean, uncrowded) */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {PILLARS.map((pillar, idx) => {
            const Icon = pillar.icon;
            return (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 15 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: idx * 0.08 }}
                className="modern-card p-7 flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between mb-5">
                    <div className="w-11 h-11 rounded-xl bg-zinc-100 text-zinc-900 flex items-center justify-center">
                      <Icon size={24} weight="duotone" />
                    </div>
                    <span className="font-mono text-xs text-[#A1A1AA] font-semibold">
                      0{idx + 1}
                    </span>
                  </div>

                  <h3 className="font-bold text-lg text-[#09090B] mb-2">
                    {pillar.title}
                  </h3>
                  <p className="text-sm text-[#52525B] leading-relaxed">
                    {pillar.description}
                  </p>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
