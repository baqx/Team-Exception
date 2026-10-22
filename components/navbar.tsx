"use client";

import React, { useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { 
  Coins, 
  List, 
  X, 
  ArrowRight, 
  User, 
  SignOut 
} from "@phosphor-icons/react";
import { useAuth } from "@/lib/auth-context";

export function Navbar() {
  const { user, openAuthModal, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const scrollToSection = (id: string) => {
    setMobileMenuOpen(false);
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <header className="sticky top-0 z-40 w-full bg-[#FFFFFF]/90 backdrop-blur-md border-b border-[#E2E8F0] transition-all">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        {/* Brand */}
        <Link href="/" className="flex items-center gap-2.5 group">
          <div className="w-8 h-8 rounded-lg overflow-hidden flex items-center justify-center shrink-0">
            <Image 
              src="/logo.png" 
              alt="Chalkka Logo" 
              width={32} 
              height={32} 
              className="w-full h-full object-contain"
              priority
            />
          </div>
          <span className="font-bold text-xl text-[#09090B] tracking-tight">
            Chalkka
          </span>
        </Link>

        {/* Standard Navigation Links */}
        <nav className="hidden md:flex items-center gap-7 text-sm font-medium text-[#52525B]">
          <button 
            onClick={() => scrollToSection("interactive-demo")}
            className="hover:text-[#09090B] transition-colors cursor-pointer"
          >
            Demo Lesson
          </button>
          <button 
            onClick={() => scrollToSection("teaching-pillars")}
            className="hover:text-[#09090B] transition-colors cursor-pointer"
          >
            Pedagogy
          </button>
          <button 
            onClick={() => scrollToSection("subjects")}
            className="hover:text-[#09090B] transition-colors cursor-pointer"
          >
            Subjects
          </button>
          <button 
            onClick={() => scrollToSection("how-it-works")}
            className="hover:text-[#09090B] transition-colors cursor-pointer"
          >
            Workflow
          </button>
        </nav>

        {/* Right CTA Area */}
        <div className="hidden sm:flex items-center gap-3">
          {user ? (
            <div className="flex items-center gap-3">
              <Link
                href="/dashboard"
                className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold text-[#09090B] bg-[#F4F4F5] border border-[#E4E4E7]"
              >
                <Coins size={14} weight="fill" className="text-[#09090B]" />
                <span>{user.credits} Credits</span>
              </Link>
              <Link
                href="/dashboard"
                className="btn-primary text-xs px-3.5 py-2 inline-flex items-center gap-1.5"
              >
                <span>Dashboard</span>
                <ArrowRight size={13} />
              </Link>
            </div>
          ) : (
            <div className="flex items-center gap-3">
              <button
                onClick={() => openAuthModal("login")}
                className="text-sm font-medium text-[#52525B] hover:text-[#09090B] px-2 py-1 transition-colors cursor-pointer"
              >
                Sign In
              </button>
              <Link
                href="/dashboard"
                className="btn-primary text-xs px-3.5 py-2 inline-flex items-center gap-1.5"
              >
                <span>Get Started</span>
                <ArrowRight size={13} />
              </Link>
            </div>
          )}
        </div>

        {/* Mobile Hamburger */}
        <div className="flex sm:hidden items-center gap-2">
          {user && (
            <Link
              href="/dashboard"
              className="px-2.5 py-0.5 text-xs font-semibold text-[#09090B] bg-[#F4F4F5] border border-[#E4E4E7] rounded-full"
            >
              {user.credits}c
            </Link>
          )}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-1.5 text-[#475569] hover:text-[#0F172A] rounded-md transition-colors cursor-pointer"
            aria-label="Toggle navigation"
          >
            {mobileMenuOpen ? <X size={20} /> : <List size={20} />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="sm:hidden border-b border-[#E2E8F0] bg-[#FFFFFF] px-4 py-4 space-y-3">
          <nav className="flex flex-col gap-2.5 text-sm font-medium text-[#475569]">
            <button 
              onClick={() => scrollToSection("interactive-demo")}
              className="text-left py-1 hover:text-[#0F172A] transition-colors cursor-pointer"
            >
              Demo Lesson
            </button>
            <button 
              onClick={() => scrollToSection("teaching-pillars")}
              className="text-left py-1 hover:text-[#0F172A] transition-colors cursor-pointer"
            >
              How it Teaches
            </button>
            <button 
              onClick={() => scrollToSection("subjects")}
              className="text-left py-1 hover:text-[#0F172A] transition-colors cursor-pointer"
            >
              Subjects
            </button>
            <button 
              onClick={() => scrollToSection("how-it-works")}
              className="text-left py-1 hover:text-[#0F172A] transition-colors cursor-pointer"
            >
              Workflow
            </button>
          </nav>
          <div className="pt-3 border-t border-[#E2E8F0] flex flex-col gap-2">
            {user ? (
              <Link
                href="/dashboard"
                onClick={() => setMobileMenuOpen(false)}
                className="w-full py-2 text-xs font-medium text-center rounded-lg btn-primary"
              >
                Go to Dashboard ({user.credits} Credits)
              </Link>
            ) : (
              <>
                <button
                  onClick={() => { setMobileMenuOpen(false); openAuthModal("login"); }}
                  className="w-full py-2 text-xs font-medium text-[#475569] border border-[#E2E8F0] rounded-lg"
                >
                  Sign In
                </button>
                <Link
                  href="/dashboard"
                  onClick={() => setMobileMenuOpen(false)}
                  className="w-full py-2 text-xs font-medium text-center rounded-lg btn-primary"
                >
                  Get Started Free
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </header>
  );
}
