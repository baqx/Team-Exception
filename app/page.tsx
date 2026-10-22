"use client";

import React, { useState } from "react";
import { Navbar } from "@/components/navbar";
import { HeroChalkboard } from "@/components/hero-chalkboard";
import { InteractiveDemo } from "@/components/interactive-demo";
import { TeachingPillars } from "@/components/teaching-pillars";
import { SubjectsGrid } from "@/components/subjects-grid";
import { HowItWorks } from "@/components/how-it-works";
import { EducationalDisclaimer } from "@/components/educational-disclaimer";
import { Footer } from "@/components/footer";
import { AuthModal } from "@/components/auth-modal";

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col bg-[#F8FAFC] text-[#0F172A]">
      {/* Top Minimal Navbar */}
      <Navbar />

      {/* Hero Showcase (Editorial narrative, no prompt clutter) */}
      <main className="flex-1">
        <HeroChalkboard />

        {/* Live Output Preview / Sample Chalkboard Video Player */}
        <InteractiveDemo />

        {/* Why Chalkka Actually Teaches (4 Pedagogical Pillars) */}
        <TeachingPillars />

        {/* Subjects & Popular Topic Exploration */}
        <SubjectsGrid />

        {/* How Chalkka Works (Student Workflow) */}
        <HowItWorks />

        {/* Academic Integrity & Educational Disclaimer */}
        <EducationalDisclaimer />
      </main>

      {/* Footer */}
      <Footer />

      {/* Chalkboard Auth Modal */}
      <AuthModal />
    </div>
  );
}
