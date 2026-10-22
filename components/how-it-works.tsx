"use client";

import React from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { 
  UploadSimple, 
  LightbulbFilament, 
  ChalkboardTeacher, 
  ArrowRight,
  Lightning
} from "@phosphor-icons/react";

const STEPS = [
  {
    step: "01",
    title: "Input or Upload",
    description: "Type any equation or question, paste an assignment prompt, or attach a photo of notes, diagrams, or textbook pages.",
    icon: UploadSimple,
  },
  {
    step: "02",
    title: "Prerequisite Diagnosis",
    description: "Chalkka identifies the core concept, foundational theorems, and laws needed to solve the problem.",
    icon: LightbulbFilament,
  },
  {
    step: "03",
    title: "Watch It Solved Live",
    description: "Receive a step-by-step whiteboard video that writes equations and explains each transition aloud.",
    icon: ChalkboardTeacher,
  },
];

export function HowItWorks() {
  return (
    <section 
      id="how-it-works" 
      className="relative py-20 sm:py-28 px-4 sm:px-6 lg:px-8 border-t border-[#E4E4E7] bg-[#FFFFFF]"
    >
      <div className="max-w-5xl mx-auto">
        {/* Section Header */}
        <motion.div 
          initial={{ opacity: 0, y: 15 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center max-w-2xl mx-auto mb-14"
        >
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-zinc-100 border border-zinc-200 text-xs font-semibold text-zinc-800 mb-4">
            <Lightning size={14} weight="fill" className="text-zinc-900" />
            <span>Simple Workflow</span>
          </div>
          <h2 className="font-bold text-3xl sm:text-4xl text-[#09090B] tracking-tight">
            From stuck to understood in 3 minutes.
          </h2>
          <p className="mt-3 text-base text-[#52525B]">
            Designed to help you master any complex topic or coursework through clear step-by-step visual reasoning.
          </p>
        </motion.div>

        {/* 3 Process Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {STEPS.map((item, idx) => {
            const Icon = item.icon;
            return (
              <motion.div 
                key={idx}
                initial={{ opacity: 0, y: 15 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: idx * 0.1 }}
                className="modern-card p-7 flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between mb-5">
                    <span className="text-xs font-bold font-mono text-[#09090B] px-2.5 py-1 rounded-md bg-zinc-100 border border-zinc-200/60">
                      STEP {item.step}
                    </span>
                    <div className="w-10 h-10 rounded-xl bg-zinc-50 border border-zinc-200 flex items-center justify-center text-zinc-700">
                      <Icon size={20} weight="duotone" />
                    </div>
                  </div>

                  <h3 className="font-bold text-lg text-[#09090B] mb-2">
                    {item.title}
                  </h3>
                  <p className="text-sm text-[#52525B] leading-relaxed">
                    {item.description}
                  </p>
                </div>
              </motion.div>
            );
          })}
        </div>

        {/* Bottom CTA to Studio */}
        <motion.div 
          initial={{ opacity: 0, y: 15 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.4, delay: 0.3 }}
          className="mt-14 text-center"
        >
          <Link
            href="/dashboard"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-xl btn-primary text-sm font-semibold cursor-pointer shadow-sm"
          >
            <span>Launch Studio & Solve Your Problem</span>
            <ArrowRight size={15} />
          </Link>
        </motion.div>
      </div>
    </section>
  );
}
