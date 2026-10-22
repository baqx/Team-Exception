"use client";

import React from "react";
import { motion } from "framer-motion";
import { ShieldCheck, GraduationCap } from "@phosphor-icons/react";

export function EducationalDisclaimer() {
  return (
    <section className="py-14 px-4 sm:px-6 lg:px-8 border-t border-[#E4E4E7] bg-[#FAFAFA]">
      <motion.div 
        initial={{ opacity: 0, y: 15 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.4 }}
        className="max-w-4xl mx-auto rounded-2xl bg-white border border-[#E4E4E7] p-6 sm:p-7 flex flex-col sm:flex-row items-start sm:items-center gap-5 modern-card shadow-xs"
      >
        <div className="w-12 h-12 rounded-xl bg-zinc-100 border border-zinc-200 flex items-center justify-center text-[#09090B] shrink-0">
          <ShieldCheck size={26} weight="duotone" />
        </div>

        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-semibold uppercase tracking-wider text-[#71717A]">
              Academic Integrity Pledge
            </span>
          </div>
          <h3 className="font-bold text-lg text-[#09090B]">
            Built for students who want to understand, not just copy.
          </h3>
          <p className="mt-1 text-xs sm:text-sm text-[#52525B] leading-relaxed">
            Chalkka is designed as a pedagogical tool. It reveals foundational principles, walks through algebraic derivations step-by-step, and verifies boundary conditions.
          </p>
        </div>

        <div className="sm:text-right shrink-0">
          <div className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-zinc-100 border border-zinc-200 text-xs font-semibold text-zinc-800">
            <GraduationCap size={16} className="text-[#09090B]" />
            <span>DevFest Abeokuta '26</span>
          </div>
        </div>
      </motion.div>
    </section>
  );
}
