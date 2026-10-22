"use client";

import React, { useState } from "react";
import Image from "next/image";
import { motion } from "framer-motion";
import { 
  X, 
  Coins, 
  EnvelopeSimple, 
  LockKey, 
  User as UserIcon,
  WarningCircle,
  ArrowRight
} from "@phosphor-icons/react";
import { useAuth } from "@/lib/auth-context";

export function AuthModal() {
  const { 
    isAuthModalOpen, 
    closeAuthModal, 
    authModalMode, 
    openAuthModal,
    login, 
    signup 
  } = useAuth();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!isAuthModalOpen) return null;

  const isSignUp = authModalMode === "signup";

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      if (isSignUp) {
        if (!name.trim()) {
          throw new Error("Please enter your name or nickname.");
        }
        await signup(email, password, name);
      } else {
        await login(email, password);
      }
    } catch (err: any) {
      setError(err?.message || "Authentication failed. Please check your credentials.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 bg-slate-900/40 backdrop-blur-xs">
      <motion.div 
        initial={{ opacity: 0, scale: 0.96, y: 8 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.96 }}
        transition={{ duration: 0.2, ease: "easeOut" }}
        className="relative w-full max-w-md bg-[#FFFFFF] border border-[#CBD5E1] rounded-2xl shadow-2xl p-6 sm:p-8 text-[#0F172A] overflow-hidden"
      >
        {/* Close button */}
        <button
          onClick={closeAuthModal}
          className="absolute top-4 right-4 p-2 text-[#64748B] hover:text-[#0F172A] hover:bg-[#F1F5F9] rounded-lg transition-colors cursor-pointer"
          aria-label="Close"
        >
          <X size={18} />
        </button>

        {/* Modal Header */}
        <div className="text-center mb-6">
          <div className="w-10 h-10 mx-auto mb-3 rounded-xl overflow-hidden flex items-center justify-center">
            <Image 
              src="/logo.png" 
              alt="Chalkka Logo" 
              width={40} 
              height={40} 
              className="w-full h-full object-contain"
              priority
            />
          </div>
          <h2 className="text-2xl font-bold tracking-tight text-[#09090B]">
            {isSignUp ? "Create Your Account" : "Welcome Back"}
          </h2>
          <p className="text-xs sm:text-sm text-[#52525B] mt-1">
            {isSignUp 
              ? "Start generating step-by-step chalkboard lessons." 
              : "Sign in to access your previous lessons and studio."}
          </p>
        </div>

        {/* Credit Bonus Announcement */}
        {isSignUp && (
          <div className="mb-5 p-3.5 bg-zinc-100 border border-zinc-200 rounded-xl flex items-center gap-2.5">
            <Coins size={18} weight="fill" className="text-zinc-900 shrink-0" />
            <div className="text-xs text-zinc-800">
              <span className="font-bold">50 Free Credits</span> granted automatically on signup to create your first 10 lessons.
            </div>
          </div>
        )}

        {/* Auth Mode Tabs */}
        <div className="flex border-b border-[#E4E4E7] mb-5">
          <button
            type="button"
            onClick={() => { setError(null); openAuthModal("login"); }}
            className={`flex-1 py-2.5 text-xs font-semibold text-center transition-all cursor-pointer border-b-2 ${
              !isSignUp 
                ? "border-[#09090B] text-[#09090B]" 
                : "border-transparent text-[#71717A] hover:text-[#09090B]"
            }`}
          >
            Sign In
          </button>
          <button
            type="button"
            onClick={() => { setError(null); openAuthModal("signup"); }}
            className={`flex-1 py-2.5 text-xs font-semibold text-center transition-all cursor-pointer border-b-2 ${
              isSignUp 
                ? "border-[#09090B] text-[#09090B]" 
                : "border-transparent text-[#71717A] hover:text-[#09090B]"
            }`}
          >
            Create Account
          </button>
        </div>

        {/* Error notification */}
        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-xs text-red-700 flex items-start gap-2">
            <WarningCircle size={16} className="shrink-0 mt-0.5 text-red-600" />
            <span>{error}</span>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {isSignUp && (
            <div>
              <label className="block text-xs uppercase tracking-wider text-[#475569] mb-1.5 font-semibold">
                Your Name
              </label>
              <div className="relative">
                <span className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[#94A3B8]">
                  <UserIcon size={16} />
                </span>
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="e.g. Richard Feynman"
                  className="w-full pl-9 pr-3.5 py-2.5 bg-[#FFFFFF] border border-[#E4E4E7] rounded-xl text-sm text-[#09090B] placeholder-[#A1A1AA] focus:outline-none focus:ring-2 focus:ring-zinc-900/10 focus:border-zinc-900 transition-colors"
                />
              </div>
            </div>
          )}

          <div>
            <label className="block text-xs uppercase tracking-wider text-[#52525B] mb-1.5 font-semibold">
              Email Address
            </label>
            <div className="relative">
              <span className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[#A1A1AA]">
                <EnvelopeSimple size={16} />
              </span>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="student@university.edu"
                className="w-full pl-9 pr-3.5 py-2.5 bg-[#FFFFFF] border border-[#E4E4E7] rounded-xl text-sm text-[#09090B] placeholder-[#A1A1AA] focus:outline-none focus:ring-2 focus:ring-zinc-900/10 focus:border-zinc-900 transition-colors"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs uppercase tracking-wider text-[#52525B] mb-1.5 font-semibold">
              Password
            </label>
            <div className="relative">
              <span className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[#A1A1AA]">
                <LockKey size={16} />
              </span>
              <input
                type="password"
                required
                minLength={4}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-9 pr-3.5 py-2.5 bg-[#FFFFFF] border border-[#E4E4E7] rounded-xl text-sm text-[#09090B] placeholder-[#A1A1AA] focus:outline-none focus:ring-2 focus:ring-zinc-900/10 focus:border-zinc-900 transition-colors"
              />
            </div>
          </div>

          <div className="pt-2">
            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full py-3 px-4 rounded-xl font-semibold text-sm transition-all flex items-center justify-center gap-2 cursor-pointer btn-primary disabled:opacity-50 shadow-sm"
            >
              {isSubmitting ? (
                <span>Processing...</span>
              ) : isSignUp ? (
                <>
                  <Coins size={15} weight="fill" className="text-zinc-200" />
                  <span>Create Account (+50 Credits)</span>
                  <ArrowRight size={14} />
                </>
              ) : (
                <>
                  <span>Sign In</span>
                  <ArrowRight size={14} />
                </>
              )}
            </button>
          </div>
        </form>

        {/* Modal footer switch */}
        <div className="mt-5 pt-3 border-t border-[#F4F4F5] text-center text-xs text-[#71717A]">
          {isSignUp ? (
            <p>
              Already have an account?{" "}
              <button
                type="button"
                onClick={() => { setError(null); openAuthModal("login"); }}
                className="text-[#09090B] hover:underline font-semibold cursor-pointer ml-1"
              >
                Sign In
              </button>
            </p>
          ) : (
            <p>
              New student to Chalkka?{" "}
              <button
                type="button"
                onClick={() => { setError(null); openAuthModal("signup"); }}
                className="text-[#09090B] hover:underline font-semibold cursor-pointer ml-1"
              >
                Create Account (+50 Credits)
              </button>
            </p>
          )}
        </div>
      </motion.div>
    </div>
  );
}
