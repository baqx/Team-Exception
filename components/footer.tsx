"use client";

import React from "react";
import Image from "next/image";
import { Heart } from "@phosphor-icons/react";

export function Footer() {
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <footer className="w-full border-t border-[#E4E4E7] bg-[#FFFFFF] py-10 px-4 sm:px-6 lg:px-8 text-xs text-[#71717A]">
      <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
        {/* Brand & Mission */}
        <div className="flex flex-col sm:flex-row items-center gap-3 text-center sm:text-left">
          <div className="w-7 h-7 rounded-lg overflow-hidden flex items-center justify-center shrink-0">
            <Image 
              src="/logo.png" 
              alt="Chalkka Logo" 
              width={28} 
              height={28} 
              className="w-full h-full object-contain"
            />
          </div>
          <div>
            <div className="font-bold text-base text-[#09090B] tracking-tight">
              Chalkka
            </div>
            <div className="text-[11px] text-[#71717A]">
              Your personal chalkboard tutor that actually teaches.
            </div>
          </div>
        </div>

        {/* Roadmap tags */}
        <div className="flex flex-wrap items-center justify-center gap-2 text-[10px] font-medium text-[#52525B]">
          <span className="px-2.5 py-1 rounded-md bg-[#F4F4F5] border border-[#E4E4E7]">
            Yoruba / Pidgin Voice
          </span>
          <span className="px-2.5 py-1 rounded-md bg-[#F4F4F5] border border-[#E4E4E7]">
            Student Attempt Compare
          </span>
          <span className="px-2.5 py-1 rounded-md bg-[#F4F4F5] border border-[#E4E4E7]">
            Mobile PWA
          </span>
        </div>

        {/* Copyright & DevFest */}
        <div className="flex items-center gap-4 text-center sm:text-right">
          <div className="text-[11px] text-[#71717A]">
            DevFest Abeokuta Buildathon 2026
          </div>
          <button
            onClick={scrollToTop}
            className="hover:text-[#09090B] transition-colors cursor-pointer text-[11px] underline underline-offset-4"
          >
            Back to Top
          </button>
        </div>
      </div>
    </footer>
  );
}
