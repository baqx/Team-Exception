"use client";

import React, { useState } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Lightning, 
  Function as MathIcon, 
  Atom, 
  Flask, 
  GearSix, 
  Code,
  ArrowRight,
  GraduationCap
} from "@phosphor-icons/react";
import { SUBJECT_OPTIONS } from "@/lib/mock-data";
import { SubjectId } from "@/lib/types";

const SUBJECT_ICONS: Record<SubjectId, React.ElementType> = {
  electrical: Lightning,
  maths: MathIcon,
  physics: Atom,
  chemistry: Flask,
  mechanical: GearSix,
  computer_science: Code,
};

export function SubjectsGrid() {
  const [selectedSubject, setSelectedSubject] = useState<SubjectId>("electrical");
  const currentSubjectData = SUBJECT_OPTIONS.find((s) => s.id === selectedSubject) || SUBJECT_OPTIONS[0];

  return (
    <section 
      id="subjects" 
      className="relative py-20 sm:py-28 px-4 sm:px-6 lg:px-8 border-t border-[#E4E4E7] bg-[#FAFAFA]"
    >
      <div className="max-w-5xl mx-auto">
        {/* Section Header */}
        <motion.div 
          initial={{ opacity: 0, y: 15 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center max-w-2xl mx-auto mb-12"
        >
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-zinc-100 border border-zinc-200 text-xs font-semibold text-zinc-800 mb-4">
            <GraduationCap size={15} weight="fill" className="text-zinc-900" />
            <span>Universal Coursework & Topic Coverage</span>
          </div>
          <h2 className="font-bold text-3xl sm:text-4xl text-[#09090B] tracking-tight">
            Built for any challenging subject or complex problem.
          </h2>
          <p className="mt-3 text-base text-[#52525B]">
            From mathematics, physics, and circuit engineering to economic models, discrete algorithms, and chemical dynamics.
          </p>
        </motion.div>

        {/* Subject Tab Selectors */}
        <div className="flex flex-wrap justify-center gap-2 mb-10">
          {SUBJECT_OPTIONS.map((sub) => {
            const Icon = SUBJECT_ICONS[sub.id] || Lightning;
            const isSelected = selectedSubject === sub.id;
            return (
              <button
                key={sub.id}
                onClick={() => setSelectedSubject(sub.id)}
                className={`inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-semibold transition-all cursor-pointer ${
                  isSelected
                    ? "bg-[#09090B] text-white shadow-xs"
                    : "bg-white text-[#52525B] border border-[#E4E4E7] hover:text-[#09090B] hover:bg-zinc-50"
                }`}
              >
                <Icon size={16} weight={isSelected ? "fill" : "regular"} />
                <span>{sub.label}</span>
              </button>
            );
          })}
        </div>

        {/* Subject Detail Card with Animated Content */}
        <AnimatePresence mode="wait">
          <motion.div
            key={currentSubjectData.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.25 }}
            className="max-w-4xl mx-auto rounded-2xl bg-white border border-[#E4E4E7] p-6 sm:p-8 flex flex-col md:flex-row items-stretch justify-between gap-6 modern-card shadow-xs"
          >
            <div className="flex-1 flex flex-col justify-between">
              <div>
                <div className="flex items-center gap-2 text-xs font-semibold text-zinc-900 uppercase tracking-wider mb-2">
                  <span>{currentSubjectData.label}</span>
                </div>
                <h3 className="font-bold text-xl text-[#09090B]">
                  Core Concepts & Problem Modules
                </h3>

                {/* Topics */}
                <div className="flex flex-wrap gap-2 mt-4">
                  {currentSubjectData.popularTopics.map((topic, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1.5 rounded-lg bg-[#F4F4F5] border border-[#E4E4E7] text-xs font-medium text-[#18181B]"
                    >
                      {topic}
                    </span>
                  ))}
                </div>
              </div>

              <div className="mt-6 text-xs text-[#71717A]">
                Diagrams and derivations rendered stroke-by-stroke in 1080p.
              </div>
            </div>

            {/* Sample Problem Box with Direct Studio Link */}
            <div className="w-full md:w-80 rounded-xl bg-zinc-50 border border-zinc-200 p-5 flex flex-col justify-between">
              <div>
                <span className="text-xs font-semibold uppercase tracking-wider text-zinc-900 block mb-2">
                  Example Problem
                </span>
                <p className="text-xs sm:text-sm text-[#18181B] leading-relaxed italic">
                  "{currentSubjectData.sampleProblem}"
                </p>
              </div>

              <Link
                href={`/dashboard?query=${encodeURIComponent(currentSubjectData.sampleProblem)}&subject=${currentSubjectData.id}`}
                className="mt-5 w-full py-2.5 px-3 rounded-lg btn-primary text-xs inline-flex items-center justify-center gap-2 font-semibold cursor-pointer"
              >
                <span>Solve in Studio</span>
                <ArrowRight size={13} />
              </Link>
            </div>
          </motion.div>
        </AnimatePresence>
      </div>
    </section>
  );
}
