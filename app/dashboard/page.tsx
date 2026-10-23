"use client";

import React, { Suspense, useEffect, useState, useRef } from "react";
import Link from "next/link";
import Image from "next/image";
import { useSearchParams } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Chalkboard, 
  Coins, 
  SignOut, 
  DownloadSimple, 
  Copy, 
  Clock, 
  FilmStrip, 
  PencilSimpleLine,
  UploadSimple,
  X,
  PlusCircle,
  Lightning,
  CircleNotch,
  BookOpen,
  Compass,
  Brain,
  ArrowRight,
  CheckCircle,
  WarningCircle,
  VideoCamera,
  FilePdf,
  Image as ImageIcon,
  Flask
} from "@phosphor-icons/react";
import { useAuth } from "@/lib/auth-context";
import { 
  fetchUserHistory, 
  startGenerationJob, 
  pollJobUntilFinished,
  fetchJobStatus
} from "@/lib/api";
import { UserJob, SubjectId, VideoLength } from "@/lib/types";
import { AuthModal } from "@/components/auth-modal";

type DashboardTab = "studio" | "archive" | "credits";

const SUBJECT_OPTIONS: { id: SubjectId; label: string; icon: React.ElementType }[] = [
  { id: "electrical", label: "Electrical Engineering", icon: Lightning },
  { id: "physics", label: "Classical & Modern Physics", icon: Compass },
  { id: "maths", label: "Calculus & Linear Algebra", icon: Brain },
  { id: "chemistry", label: "General Chemistry", icon: Flask },
  { id: "mechanical", label: "Mechanical Engineering", icon: BookOpen },
  { id: "computer_science", label: "Computer Science & Logic", icon: BookOpen },
];

const pageContainerVariants = {
  initial: { opacity: 0, y: 14 },
  animate: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.35,
      ease: [0.16, 1, 0.3, 1] as const,
      staggerChildren: 0.08,
      delayChildren: 0.04,
    },
  },
  exit: {
    opacity: 0,
    y: -8,
    transition: { duration: 0.18, ease: "easeOut" as const },
  },
};

const revealItemVariants = {
  initial: { opacity: 0, y: 16 },
  animate: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.4, ease: [0.16, 1, 0.3, 1] as const },
  },
};

const cardStaggerVariants = {
  initial: { opacity: 0 },
  animate: {
    opacity: 1,
    transition: {
      staggerChildren: 0.07,
      delayChildren: 0.05,
    },
  },
};

const cardRevealVariants = {
  initial: { opacity: 0, y: 16, scale: 0.98 },
  animate: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: { duration: 0.38, ease: [0.16, 1, 0.3, 1] as const },
  },
};

function DashboardContent() {
  const searchParams = useSearchParams();
  const initialQuery = searchParams.get("query") || "";
  const initialSubject = (searchParams.get("subject") as SubjectId) || "electrical";

  const { 
    user, 
    token, 
    logout, 
    recharge, 
    openAuthModal, 
    deductLocalCredits, 
    refreshUser,
  } = useAuth();

  // Active Tab: "studio" | "archive" | "credits"
  const [activeTab, setActiveTab] = useState<DashboardTab>("studio");

  // Studio form states
  const [query, setQuery] = useState(initialQuery);
  const [selectedSubject, setSelectedSubject] = useState<SubjectId>(initialSubject);
  const [selectedLength, setSelectedLength] = useState<VideoLength>("standard");
  const [attachment, setAttachment] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  // Generation progress states
  const [isGenerating, setIsGenerating] = useState(false);
  const [generationStage, setGenerationStage] = useState<string>("");
  const [progressPercent, setProgressPercent] = useState<number>(0);
  const [creditNotice, setCreditNotice] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Archive & Job history states
  const [jobs, setJobs] = useState<UserJob[]>([]);
  const [isLoadingJobs, setIsLoadingJobs] = useState(true);
  const [isRecharging, setIsRecharging] = useState(false);
  const [rechargeSuccess, setRechargeSuccess] = useState(false);
  const [copiedJobId, setCopiedJobId] = useState<string | null>(null);

  useEffect(() => {
    if (initialQuery) {
      setQuery(initialQuery);
      setActiveTab("studio");
    }
    if (initialSubject) {
      setSelectedSubject(initialSubject);
    }
  }, [initialQuery, initialSubject]);

  const loadHistory = () => {
    if (token) {
      setIsLoadingJobs(true);
      fetchUserHistory(token)
        .then((res) => {
          setJobs(res.jobs);
        })
        .catch((err) => {
          console.error("Failed to load user history:", err);
        })
        .finally(() => {
          setIsLoadingJobs(false);
        });
    } else {
      setIsLoadingJobs(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, [token]);

  // Auto-resume active job if user refreshed or navigated back
  useEffect(() => {
    const activeJobId = typeof window !== "undefined" ? localStorage.getItem("active_chalkka_job_id") : null;
    if (activeJobId && !isGenerating) {
      fetchJobStatus(activeJobId)
        .then((status) => {
          if (status.status === "completed" || status.status === "failed") {
            localStorage.removeItem("active_chalkka_job_id");
            loadHistory();
          } else {
            setIsGenerating(true);
            setGenerationStage(status.current_step_text || "Synthesizing chalkboard lesson on server...");
            setProgressPercent(Math.max(20, status.progress_percent));
            pollJobUntilFinished(
              activeJobId,
              (s) => {
                setGenerationStage(s.current_step_text);
                setProgressPercent(Math.max(20, s.progress_percent));
              }
            )
              .then(() => {
                localStorage.removeItem("active_chalkka_job_id");
                setIsGenerating(false);
                setProgressPercent(100);
                loadHistory();
                setActiveTab("archive");
              })
              .catch(() => {
                localStorage.removeItem("active_chalkka_job_id");
                setIsGenerating(false);
                loadHistory();
              });
          }
        })
        .catch(() => {
          localStorage.removeItem("active_chalkka_job_id");
        });
    }
  }, [token]);

  // Auto-refresh My Lessons tab while any job is pending on the server
  useEffect(() => {
    const hasPendingJobs = jobs.some(
      (j) => j.status === "pending" || (!j.status?.includes("completed") && !j.status?.includes("failed"))
    );
    if (!hasPendingJobs || !token) return;

    const pollTimer = setInterval(() => {
      fetchUserHistory(token)
        .then((res) => {
          setJobs(res.jobs);
        })
        .catch(() => {});
    }, 4000);

    return () => clearInterval(pollTimer);
  }, [jobs, token]);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setAttachment(file.name);
      setSelectedFile(file);
      if (!query.trim()) {
        setQuery(`Solve the attached assignment problem step-by-step.`);
      }
    }
  };

  const handleRecharge = async () => {
    setIsRecharging(true);
    setRechargeSuccess(false);
    try {
      await recharge(25);
      setRechargeSuccess(true);
      setTimeout(() => setRechargeSuccess(false), 3000);
    } catch (e) {
      console.error("Recharge failed:", e);
    } finally {
      setIsRecharging(false);
    }
  };

  const handleCopyLink = (url: string, jobId: string) => {
    navigator.clipboard.writeText(url);
    setCopiedJobId(jobId);
    setTimeout(() => setCopiedJobId(null), 2000);
  };

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setCreditNotice(null);

    if (!user) {
      openAuthModal("signup");
      return;
    }

    if (user.credits < 5) {
      setCreditNotice("You need at least 5 credits to generate a new chalkboard lesson.");
      return;
    }

    const effectiveQuery = query.trim();
    if (!effectiveQuery && !selectedFile) {
      setCreditNotice("Please enter a question or attach an assignment schematic / notes.");
      return;
    }

    setIsGenerating(true);
    setProgressPercent(10);
    setGenerationStage("Connecting to Chalkka pipeline...");

    try {
      const genResult = await startGenerationJob({
        query: effectiveQuery || "Solve the attached assignment problem step-by-step.",
        subject: "auto",
        length: selectedLength,
        file: selectedFile,
        userId: user.id,
      });

      if (typeof window !== "undefined") {
        localStorage.setItem("active_chalkka_job_id", genResult.job_id);
      }

      deductLocalCredits(5);
      refreshUser();

      setGenerationStage("Diagnosing prerequisites & foundational gaps...");
      setProgressPercent(20);

      await pollJobUntilFinished(
        genResult.job_id,
        (status) => {
          setGenerationStage(status.current_step_text);
          setProgressPercent(Math.max(15, status.progress_percent));
        }
      );

      if (typeof window !== "undefined") {
        localStorage.removeItem("active_chalkka_job_id");
      }

      setIsGenerating(false);
      setProgressPercent(100);

      // Refresh history and open archive
      loadHistory();
      setActiveTab("archive");
      setQuery("");
      setAttachment(null);
      setSelectedFile(null);
    } catch (err: any) {
      if (typeof window !== "undefined") {
        localStorage.removeItem("active_chalkka_job_id");
      }
      setIsGenerating(false);
      loadHistory();
      const errMsg = err?.message || "";
      if (errMsg.includes("Insufficient credits") || errMsg.includes("402")) {
        setCreditNotice("Insufficient credits (5 required). Claim a classroom grant below!");
      } else if (errMsg.includes("longer than expected")) {
        setCreditNotice("Your lesson is still rendering in the background. You can monitor it here in My Lessons.");
        setActiveTab("archive");
      } else {
        setCreditNotice(errMsg || "Generation failed. Please try again.");
      }
    }
  };

  return (
    <div className="min-h-screen bg-[#FAFAFA] text-[#09090B] flex flex-col md:flex-row relative pb-20 md:pb-0">
      {/* =========================================================================
          DESKTOP SIDE NAVIGATION (Strictly the 3 requested items)
      ========================================================================== */}
      <aside className="hidden md:flex md:w-64 lg:w-72 flex-col justify-between border-r border-[#E4E4E7] bg-[#FFFFFF] p-5 sticky top-0 h-screen shrink-0">
        <div className="space-y-6">
          {/* Brand Header */}
          <div className="flex items-center justify-between pb-3 border-b border-[#F4F4F5]">
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
              <span className="font-bold text-lg text-[#09090B] tracking-tight">
                Chalkka
              </span>
            </Link>
            <span className="text-[10px] font-semibold text-zinc-700 bg-zinc-100 border border-zinc-200 px-2 py-0.5 rounded-md">
              Studio
            </span>
          </div>

          {/* Navigation Links: Strictly New Lesson Studio, My Lessons, Credits & Billing */}
          <nav className="space-y-1.5">
            <button
              onClick={() => setActiveTab("studio")}
              className="relative w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-semibold cursor-pointer text-left transition-colors"
            >
              {activeTab === "studio" && (
                <motion.div
                  layoutId="sidebarActivePill"
                  className="absolute inset-0 bg-[#09090B] rounded-xl shadow-xs"
                  transition={{ type: "spring", stiffness: 450, damping: 35 }}
                />
              )}
              <span className={`relative z-10 flex items-center gap-3 transition-colors ${
                activeTab === "studio" ? "text-white" : "text-[#52525B] hover:text-[#09090B]"
              }`}>
                <PencilSimpleLine size={18} weight={activeTab === "studio" ? "bold" : "regular"} />
                <span>New Lesson Studio</span>
              </span>
            </button>

            <button
              onClick={() => setActiveTab("archive")}
              className="relative w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold cursor-pointer text-left transition-colors"
            >
              {activeTab === "archive" && (
                <motion.div
                  layoutId="sidebarActivePill"
                  className="absolute inset-0 bg-[#09090B] rounded-xl shadow-xs"
                  transition={{ type: "spring", stiffness: 450, damping: 35 }}
                />
              )}
              <div className={`relative z-10 flex items-center gap-3 transition-colors ${
                activeTab === "archive" ? "text-white" : "text-[#52525B] hover:text-[#09090B]"
              }`}>
                <FilmStrip size={18} weight={activeTab === "archive" ? "bold" : "regular"} />
                <span>My Lessons</span>
              </div>
              <span 
                className={`relative z-10 px-2 py-0.5 rounded-full text-[11px] font-semibold transition-colors ${
                  activeTab === "archive" 
                    ? "bg-zinc-800 text-zinc-200" 
                    : "bg-[#F4F4F5] text-[#52525B]"
                }`}
              >
                {jobs.length}
              </span>
            </button>

            <button
              onClick={() => setActiveTab("credits")}
              className="relative w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold cursor-pointer text-left transition-colors"
            >
              {activeTab === "credits" && (
                <motion.div
                  layoutId="sidebarActivePill"
                  className="absolute inset-0 bg-[#09090B] rounded-xl shadow-xs"
                  transition={{ type: "spring", stiffness: 450, damping: 35 }}
                />
              )}
              <div className={`relative z-10 flex items-center gap-3 transition-colors ${
                activeTab === "credits" ? "text-white" : "text-[#52525B] hover:text-[#09090B]"
              }`}>
                <Coins size={18} weight={activeTab === "credits" ? "fill" : "regular"} className={activeTab === "credits" ? "text-zinc-300" : "text-[#71717A]"} />
                <span>Credits & Billing</span>
              </div>
              <span className={`relative z-10 text-[11px] font-semibold px-2 py-0.5 rounded-full transition-colors ${
                activeTab === "credits"
                  ? "bg-zinc-800 text-zinc-200"
                  : "bg-zinc-100 text-zinc-800 border border-zinc-200"
              }`}>
                {user?.credits ?? 0}
              </span>
            </button>
          </nav>
        </div>

        {/* Sidebar Footer: Credit Balance Card & User Profile */}
        <div className="space-y-4 pt-4 border-t border-[#E4E4E7]">
          {/* Credit grant mini-card */}
          <div className="p-4 rounded-xl bg-[#F4F4F5] border border-[#E4E4E7]">
            <div className="flex items-center justify-between text-xs text-[#71717A] mb-1">
              <span className="font-semibold text-[#09090B]">Classroom Balance</span>
              <Coins size={14} weight="fill" className="text-[#09090B]" />
            </div>
            <div className="flex items-baseline justify-between mb-3">
              <span className="text-2xl font-extrabold text-[#09090B]">
                {user?.credits ?? 0}
              </span>
              <span className="text-xs text-[#71717A] font-medium">Credits</span>
            </div>
            <button
              onClick={handleRecharge}
              disabled={isRecharging}
              className="w-full py-2 px-2.5 rounded-lg text-xs font-semibold bg-[#FFFFFF] border border-[#E4E4E7] hover:bg-[#F4F4F5] text-[#09090B] flex items-center justify-center gap-1.5 transition-colors cursor-pointer disabled:opacity-50 shadow-2xs"
            >
              <PlusCircle size={15} weight="bold" className="text-[#09090B]" />
              <span>{isRecharging ? "Adding..." : "+25 Grant Credits"}</span>
            </button>
            {rechargeSuccess && (
              <span className="text-[11px] text-green-700 font-medium block text-center mt-1.5">
                Added 25 credits!
              </span>
            )}
          </div>

          {/* User profile row */}
          {user ? (
            <div className="flex items-center justify-between pt-1">
              <div className="flex items-center gap-2.5 overflow-hidden">
                <div className="w-8 h-8 rounded-full bg-[#09090B] text-[#FFFFFF] flex items-center justify-center font-bold text-xs shrink-0">
                  {user.name.charAt(0).toUpperCase()}
                </div>
                <div className="overflow-hidden">
                  <div className="text-xs font-semibold text-[#09090B] truncate">{user.name}</div>
                  <div className="text-[11px] text-[#71717A] truncate">{user.email}</div>
                </div>
              </div>
              <button
                onClick={logout}
                className="p-1.5 text-[#71717A] hover:text-[#09090B] rounded-md hover:bg-[#F4F4F5] transition-colors cursor-pointer"
                title="Sign Out"
              >
                <SignOut size={16} />
              </button>
            </div>
          ) : (
            <button
              onClick={() => openAuthModal("login")}
              className="w-full py-2 px-3 text-xs font-semibold rounded-lg btn-primary text-center"
            >
              Sign In to Save Lessons
            </button>
          )}
        </div>
      </aside>

      {/* =========================================================================
          MAIN WORKSPACE CONTENT (Standard Modern Layout, Clean White Space)
      ========================================================================== */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top Header Bar */}
        <header className="h-16 border-b border-[#E4E4E7] bg-[#FFFFFF]/90 backdrop-blur-md px-4 sm:px-8 flex items-center justify-between sticky top-0 z-30">
          <div className="flex items-center gap-2">
            <div className="md:hidden flex items-center gap-2 mr-2">
              <div className="w-7 h-7 rounded-md overflow-hidden flex items-center justify-center shrink-0">
                <Image 
                  src="/logo.png" 
                  alt="Chalkka Logo" 
                  width={28} 
                  height={28} 
                  className="w-full h-full object-contain"
                />
              </div>
              <span className="font-bold text-base text-[#09090B]">Chalkka</span>
            </div>
            <div className="hidden md:flex items-center gap-2 text-xs font-medium text-[#71717A]">
              <span>Dashboard</span>
              <span>/</span>
              <span className="text-[#09090B] font-semibold">
                {activeTab === "studio" ? "New Lesson" : activeTab === "archive" ? "My Lessons" : "Credits"}
              </span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {/* Credits pill indicator */}
            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-zinc-100 border border-zinc-200 text-xs font-semibold text-zinc-800">
              <Coins size={13} weight="fill" className="text-[#09090B]" />
              <span>{user?.credits ?? 0} Credits</span>
            </div>

            <button
              onClick={handleRecharge}
              disabled={isRecharging}
              className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold btn-secondary cursor-pointer"
            >
              <PlusCircle size={14} className="text-[#09090B]" />
              <span>Add Credits</span>
            </button>

            {user ? (
              <div className="w-8 h-8 rounded-full bg-[#09090B] text-white flex items-center justify-center font-bold text-xs">
                {user.name.charAt(0).toUpperCase()}
              </div>
            ) : (
              <button
                onClick={() => openAuthModal("login")}
                className="text-xs font-semibold px-3.5 py-1.5 rounded-lg btn-primary"
              >
                Sign In
              </button>
            )}
          </div>
        </header>

        {/* Workspace Body */}
        <main className="flex-1 p-4 sm:p-8 lg:p-10 max-w-4xl mx-auto w-full">
          {/* =========================================================================
              PERSISTENT ACTIVE GENERATION STATUS DOCK (Visible across ALL tabs)
          ========================================================================== */}
          {isGenerating && (
            <motion.div
              initial={{ opacity: 0, y: -12, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -12, scale: 0.98 }}
              transition={{ duration: 0.3 }}
              className="mb-8 p-4 sm:p-5 rounded-2xl bg-[#09090B] text-white shadow-xl border border-zinc-800 relative overflow-hidden flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4"
            >
              {/* Iridescent Rainbow Accent Bar */}
              <div className="absolute top-0 left-0 right-0 h-1 rainbow-gradient" />

              <div className="flex items-center gap-3.5">
                {/* Mini Radiant Orb */}
                <div className="relative w-8 h-8 shrink-0 flex items-center justify-center">
                  <div className="absolute inset-0 rounded-full rainbow-gradient opacity-85 animate-spin" />
                  <div className="relative z-10 w-4 h-4 rounded-full bg-white shadow-[0_0_12px_rgba(255,255,255,0.9)]" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-white tracking-wide uppercase">
                      Chalkboard Lesson Synthesizing
                    </span>
                    <span className="text-[11px] font-mono px-2 py-0.5 rounded-full bg-zinc-800 text-zinc-300 font-bold">
                      {progressPercent}%
                    </span>
                  </div>
                  <p className="text-xs text-zinc-300 mt-0.5 line-clamp-1">
                    {generationStage || "Diagnosing prerequisites and deriving chalkboard scenes..."}
                  </p>
                  
                </div>
              </div>

              <div className="flex items-center gap-3 w-full sm:w-auto justify-between sm:justify-end">
                <div className="w-28 sm:w-44 h-2 bg-zinc-800 rounded-full overflow-hidden shrink-0">
                  <div 
                    className="h-full rainbow-gradient transition-all duration-300 rounded-full"
                    style={{ width: `${progressPercent}%` }}
                  />
                </div>
                {activeTab !== "studio" && (
                  <button
                    type="button"
                    onClick={() => setActiveTab("studio")}
                    className="px-3 py-1.5 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-white text-xs font-semibold shrink-0 cursor-pointer transition-colors"
                  >
                    View Studio
                  </button>
                )}
              </div>
            </motion.div>
          )}

          <AnimatePresence mode="wait">
            {/* =====================================================================
                VIEW 1: STUDIO (Creative AI Canvas with Orb & Rainbow Processing)
            ====================================================================== */}
            {activeTab === "studio" && (
              <motion.div 
                key="studio"
                variants={pageContainerVariants}
                initial="initial"
                animate="animate"
                exit="exit"
                className="space-y-6"
              >
                {/* Header */}
                <motion.div variants={revealItemVariants}>
                  <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-zinc-100 border border-zinc-200 text-xs font-semibold text-zinc-800 w-fit mb-3">
                    <Brain size={14} weight="bold" className="text-zinc-900" />
                    <span>AI Chalkboard Studio</span>
                  </div>
                  <h1 className="font-bold text-2xl sm:text-3xl text-[#09090B] tracking-tight">
                    Generate an Animated Lesson
                  </h1>
                  <p className="text-sm text-[#52525B] mt-1 max-w-2xl">
                    Enter any problem, academic topic, or study notes. DAI automatically identifies the subject, breaks down foundational laws, and generates a step-by-step whiteboard derivation across STEM, quantitative fields, economics, and beyond.
                  </p>
                </motion.div>

                {/* Credit Notice or Grant Alert */}
                {creditNotice && (
                  <motion.div 
                    variants={revealItemVariants}
                    className="p-4 bg-red-50 border border-red-200 rounded-xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs text-red-700"
                  >
                    <div className="flex items-center gap-2">
                      <WarningCircle size={16} className="text-red-600 shrink-0" />
                      <span>{creditNotice}</span>
                    </div>
                    {user ? (
                      <button
                        type="button"
                        onClick={handleRecharge}
                        disabled={isRecharging}
                        className="px-3 py-1.5 rounded-lg bg-[#FFFFFF] border border-red-300 text-red-800 text-xs font-semibold cursor-pointer shrink-0"
                      >
                        {isRecharging ? "Adding..." : "+25 Grant Credits"}
                      </button>
                    ) : (
                      <button
                        type="button"
                        onClick={() => openAuthModal("signup")}
                        className="px-3 py-1.5 rounded-lg btn-primary text-xs font-semibold cursor-pointer shrink-0"
                      >
                        Claim 50 Free Credits
                      </button>
                    )}
                  </motion.div>
                )}

                {/* Processing State: Radiant Multi-Layer AI Orb & Rainbow Aura */}
                {isGenerating ? (
                  <motion.div 
                    initial={{ opacity: 0, scale: 0.97 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.97 }}
                    transition={{ duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
                    className="relative rounded-3xl p-8 sm:p-12 overflow-hidden border border-[#E4E4E7] bg-[#FFFFFF] shadow-xl text-center flex flex-col items-center justify-center min-h-[460px]"
                  >
                    {/* Ambient Rainbow Aura Glow */}
                    <div className="absolute -inset-8 rainbow-gradient rainbow-glow pointer-events-none opacity-30" />

                    {/* Centered Multi-Layer Radiant AI Processing Orb */}
                    <div className="ai-orb-container my-4">
                      <div className="ai-orb-outer" />
                      <div className="ai-orb-middle" />
                      <div className="ai-orb-core" />
                    </div>

                    {/* Stage Heading */}
                    <div className="relative z-10 max-w-md mx-auto space-y-2 mt-4">
                      <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-zinc-100 border border-zinc-200 text-[11px] font-semibold text-zinc-800 uppercase tracking-wider">
                        <CircleNotch size={14} className="animate-spin text-zinc-900" />
                        <span>Chalkboard Engine Active</span>
                      </div>

                      <h2 className="text-xl sm:text-2xl font-bold text-zinc-900 tracking-tight">
                        {generationStage || "Synthesizing Chalkboard Lesson..."}
                      </h2>

                      <p className="text-xs sm:text-sm text-zinc-500 max-w-sm mx-auto">
                        Diagnosing subject theorems, drawing vector equations, and synchronizing classroom audio.
                      </p>
                    </div>

                    {/* Progress Bar & Numerical Metrics */}
                    <div className="relative z-10 w-full max-w-md mt-6 space-y-2">
                      <div className="flex items-center justify-between text-xs font-semibold text-zinc-700">
                        <span>Generation Stage</span>
                        <span className="font-mono text-zinc-900 font-bold">{progressPercent}%</span>
                      </div>
                      <div className="w-full h-2.5 bg-zinc-100 rounded-full overflow-hidden p-0.5 border border-zinc-200">
                        <div 
                          className="h-full rainbow-gradient rounded-full transition-all duration-300"
                          style={{ width: `${progressPercent}%` }}
                        />
                      </div>
                    </div>

                    {/* Diagnostic Progress Steps */}
                    <div className="relative z-10 grid grid-cols-2 sm:grid-cols-4 gap-2 mt-8 w-full max-w-xl text-[11px]">
                      <div className="p-2.5 rounded-xl bg-zinc-50 border border-zinc-200/80 text-zinc-700 flex items-center justify-center gap-1.5 font-medium">
                        <CheckCircle size={14} weight="fill" className="text-emerald-600" />
                        <span>Discipline Auto-Found</span>
                      </div>
                      <div className="p-2.5 rounded-xl bg-zinc-50 border border-zinc-200/80 text-zinc-700 flex items-center justify-center gap-1.5 font-medium">
                        <CheckCircle size={14} weight="fill" className="text-emerald-600" />
                        <span>Text Formatted</span>
                      </div>
                      <div className="p-2.5 rounded-xl bg-zinc-50 border border-zinc-200/80 text-zinc-700 flex items-center justify-center gap-1.5 font-medium">
                        <CircleNotch size={14} className="animate-spin text-zinc-900" />
                        <span>Voice Cadence</span>
                      </div>
                      <div className="p-2.5 rounded-xl bg-zinc-50 border border-zinc-200/80 text-zinc-700 flex items-center justify-center gap-1.5 font-medium">
                        <VideoCamera size={14} className="text-zinc-600" />
                        <span>MP4 Video</span>
                      </div>
                    </div>

                    <p className="relative z-10 text-[11px] text-zinc-400 mt-6">
                      You can navigate to <strong className="text-zinc-600">My Lessons</strong> anytime. The persistent dock keeps your status live.
                    </p>
                  </motion.div>
                ) : (
                  /* Studio Form Canvas with Iridescent Rainbow Edge */
                  <form onSubmit={handleGenerate} className="space-y-6">
                    <motion.div 
                      variants={revealItemVariants}
                      className="relative rounded-2xl p-[1px] group"
                    >
                      {/* Ambient Iridescent Rainbow Border Glow on Hover/Focus */}
                      <div className="absolute -inset-0.5 rounded-2xl rainbow-gradient opacity-0 group-hover:opacity-20 group-focus-within:opacity-35 blur-xs transition-opacity duration-500" />

                      <div className="relative rounded-2xl bg-[#FFFFFF] border border-[#E4E4E7] p-6 sm:p-8 shadow-xs space-y-6">
                        
                        

                        {/* Problem Statement Input */}
                        <div>
                          <label className="flex items-center gap-2 text-xs uppercase font-semibold tracking-wider text-[#52525B] mb-2.5">
                            <PencilSimpleLine size={16} className="text-[#09090B]" />
                            <span>Problem Statement or Equation</span>
                          </label>
                          <textarea
                            rows={5}
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            placeholder="e.g. Find the Thevenin equivalent circuit with independent sources, evaluate the integral of x*e^(2x) dx, explain IS-LM macroeconomic equilibrium, or derive equations of motion with full algebraic rigor..."
                            className="w-full p-4 rounded-xl border border-[#E4E4E7] bg-[#FFFFFF] text-sm text-[#09090B] placeholder-[#A1A1AA] focus:outline-none focus:ring-2 focus:ring-zinc-900/10 focus:border-zinc-900 transition-all resize-y leading-relaxed"
                          />
                        </div>

                        {/* File Attachment: PDFs and Images */}
                        <div>
                          <label className="flex items-center gap-2 text-xs uppercase font-semibold tracking-wider text-[#52525B] mb-2.5">
                            <UploadSimple size={16} className="text-[#09090B]" />
                            <span>Attach Notes, Diagram, or Assignment (PDF or Images)</span>
                          </label>

                          <input 
                            type="file" 
                            ref={fileInputRef} 
                            onChange={handleFileUpload} 
                            accept="image/*,.pdf" 
                            className="hidden" 
                          />

                          {attachment ? (
                            <div className="flex items-center justify-between p-3.5 rounded-xl bg-zinc-50 border border-zinc-200">
                              <div className="flex items-center gap-3 text-xs text-zinc-900 font-semibold truncate">
                                {selectedFile?.type.includes("pdf") ? (
                                  <FilePdf size={22} weight="fill" className="text-red-500 shrink-0" />
                                ) : (
                                  <ImageIcon size={22} weight="fill" className="text-blue-500 shrink-0" />
                                )}
                                <div className="truncate">
                                  <div className="truncate font-semibold text-zinc-900">{attachment}</div>
                                  <div className="text-[10px] text-zinc-500 font-normal">
                                    {selectedFile ? `${(selectedFile.size / 1024).toFixed(0)} KB • Ready for AI vision extraction` : "Attached file"}
                                  </div>
                                </div>
                              </div>
                              <button
                                type="button"
                                onClick={() => {
                                  setAttachment(null);
                                  setSelectedFile(null);
                                  if (fileInputRef.current) fileInputRef.current.value = "";
                                }}
                                className="p-1.5 text-zinc-400 hover:text-red-600 transition-colors cursor-pointer rounded-md hover:bg-zinc-100"
                                title="Remove file"
                              >
                                <X size={16} />
                              </button>
                            </div>
                          ) : (
                            <div 
                              onClick={() => fileInputRef.current?.click()}
                              className="border-2 border-dashed border-[#E4E4E7] hover:border-[#09090B] rounded-xl p-5 text-center cursor-pointer transition-colors bg-[#FAFAFA] hover:bg-[#F4F4F5] group"
                            >
                              <UploadSimple size={24} className="mx-auto text-[#A1A1AA] group-hover:text-[#09090B] mb-1.5 transition-colors" />
                              <div className="text-xs font-semibold text-[#09090B]">
                                Click to upload assignment notes, circuit schematic, or diagram
                              </div>
                              <div className="text-[11px] text-[#71717A] mt-0.5">
                                Accepts PDFs and Images (PNG, JPG, WebP) up to 20MB
                              </div>
                            </div>
                          )}
                        </div>

                        {/* Lesson Duration Setting */}
                        <div className="pt-2 border-t border-[#F4F4F5]">
                          <label className="block text-xs uppercase font-semibold tracking-wider text-[#52525B] mb-2">
                            Lesson Depth & Duration
                          </label>
                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                            <button
                              type="button"
                              onClick={() => setSelectedLength("standard")}
                              className={`p-3.5 rounded-xl border text-left transition-all cursor-pointer ${
                                selectedLength === "standard"
                                  ? "bg-[#09090B] text-white border-[#09090B] shadow-xs"
                                  : "bg-white text-[#52525B] border-[#E4E4E7] hover:bg-[#F4F4F5]"
                              }`}
                            >
                              <div className="flex items-center justify-between mb-1">
                                <span className={`text-xs font-bold ${selectedLength === "standard" ? "text-white" : "text-zinc-900"}`}>
                                  Standard Lesson
                                </span>
                                <span className="font-mono text-[10px] px-2 py-0.5 rounded bg-zinc-200/40 text-zinc-300">
                                  ~5 min
                                </span>
                              </div>
                              <p className={`text-[11px] leading-relaxed ${selectedLength === "standard" ? "text-zinc-300" : "text-zinc-500"}`}>
                                4-5 chapters. Core theorem derivation, step-by-step calculus, and boxed solution.
                              </p>
                            </button>

                            <button
                              type="button"
                              onClick={() => setSelectedLength("detailed")}
                              className={`p-3.5 rounded-xl border text-left transition-all cursor-pointer ${
                                selectedLength === "detailed"
                                  ? "bg-[#09090B] text-white border-[#09090B] shadow-xs"
                                  : "bg-white text-[#52525B] border-[#E4E4E7] hover:bg-[#F4F4F5]"
                              }`}
                            >
                              <div className="flex items-center justify-between mb-1">
                                <span className={`text-xs font-bold ${selectedLength === "detailed" ? "text-white" : "text-zinc-900"}`}>
                                  In-Depth Masterclass
                                </span>
                                <span className="font-mono text-[10px] px-2 py-0.5 rounded bg-zinc-200/40 text-zinc-300">
                                  ~8 min
                                </span>
                              </div>
                              <p className={`text-[11px] leading-relaxed ${selectedLength === "detailed" ? "text-zinc-300" : "text-zinc-500"}`}>
                                Up to 8 scenes. Derives every intermediate algebraic step with zero shortcuts, pitfalls, and verification.
                              </p>
                            </button>
                          </div>
                        </div>

                        {/* Action Row */}
                        <div className="pt-4 border-t border-[#F4F4F5] flex flex-col sm:flex-row items-center justify-between gap-4">
                          <div className="text-xs text-[#71717A] flex items-center gap-2">
                            <Coins size={15} weight="fill" className="text-[#09090B]" />
                            <span className="font-semibold text-[#09090B]">5 Credits</span>
                            <span>per lesson</span>
                            <span>•</span>
                            <span>{user?.credits ?? 0} available</span>
                          </div>

                          <button
                            type="submit"
                            disabled={isGenerating}
                            className="w-full sm:w-auto px-6 py-3 rounded-xl btn-primary text-sm font-semibold inline-flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50 shadow-sm"
                          >
                            <VideoCamera size={17} weight="bold" className="text-zinc-200" />
                            <span>Generate Chalkboard Lesson</span>
                            <ArrowRight size={15} />
                          </button>
                        </div>
                      </div>
                    </motion.div>
                  </form>
                )}
              </motion.div>
            )}

            {/* =====================================================================
                VIEW 2: LESSON ARCHIVE (History of all past generated videos)
            ====================================================================== */}
            {activeTab === "archive" && (
              <motion.div 
                key="archive"
                variants={pageContainerVariants}
                initial="initial"
                animate="animate"
                exit="exit"
                className="space-y-6"
              >
                <motion.div variants={revealItemVariants} className="flex items-center justify-between">
                  <div>
                    <h1 className="font-bold text-2xl sm:text-3xl text-[#09090B] tracking-tight">
                      My Chalkboard Archive
                    </h1>
                    <p className="text-sm text-[#52525B] mt-1">
                      Past derivations, circuit videos, and lesson plans generated on your account.
                    </p>
                  </div>
                  <button
                    onClick={() => setActiveTab("studio")}
                    className="px-4 py-2 rounded-xl btn-primary text-xs font-semibold inline-flex items-center gap-1.5 cursor-pointer shadow-sm hover:scale-[1.02] active:scale-[0.98] transition-transform"
                  >
                    <PencilSimpleLine size={15} />
                    <span>New Lesson</span>
                  </button>
                </motion.div>

                {isLoadingJobs ? (
                  <motion.div variants={revealItemVariants} className="py-20 text-center text-[#71717A] text-xs">
                    <CircleNotch size={24} className="animate-spin mx-auto mb-2 text-[#09090B]" />
                    <span>Loading lesson archives...</span>
                  </motion.div>
                ) : jobs.length === 0 ? (
                  <motion.div 
                    variants={revealItemVariants}
                    className="p-12 text-center rounded-2xl bg-[#FFFFFF] border border-dashed border-[#E4E4E7]"
                  >
                    <FilmStrip size={40} className="mx-auto text-[#A1A1AA] mb-3" />
                    <h3 className="font-bold text-xl text-[#09090B] mb-1">No Lessons Yet</h3>
                    <p className="text-xs text-[#71717A] max-w-sm mx-auto mb-5">
                      Your archive is empty. Head over to the studio to generate your first step-by-step chalkboard lesson!
                    </p>
                    <button
                      onClick={() => setActiveTab("studio")}
                      className="px-4 py-2 rounded-xl btn-primary text-xs font-semibold cursor-pointer shadow-sm"
                    >
                      Create First Lesson
                    </button>
                  </motion.div>
                ) : (
                  <motion.div 
                    variants={cardStaggerVariants}
                    className="grid grid-cols-1 md:grid-cols-2 gap-6"
                  >
                    {jobs.map((job) => {
                      const isCompleted = job.status === "completed";
                      const isPending = !isCompleted && job.status !== "failed";
                      const dateStr = job.created_at 
                        ? new Date(job.created_at).toLocaleDateString(undefined, { 
                            month: "short", 
                            day: "numeric", 
                            year: "numeric" 
                          }) 
                        : "Recently";

                      return (
                        <motion.div 
                          key={job.job_id}
                          variants={cardRevealVariants}
                          whileHover={{ y: -3, transition: { duration: 0.2 } }}
                          className="rounded-2xl bg-[#FFFFFF] border border-[#E4E4E7] overflow-hidden flex flex-col justify-between shadow-xs hover:border-[#D4D4D8] transition-colors"
                        >
                          {/* Video Player or Thumbnail */}
                          <div className="relative aspect-video bg-[#09090B] overflow-hidden flex items-center justify-center">
                            {isCompleted && job.video_url ? (
                              <video 
                                src={job.video_url} 
                                controls 
                                preload="metadata" 
                                className="w-full h-full object-contain bg-black" 
                              />
                            ) : isPending ? (
                              <div className="flex flex-col items-center gap-2 text-zinc-300 text-center px-4">
                                <div className="flex items-center gap-2">
                                  <CircleNotch size={20} className="animate-spin text-zinc-300" />
                                  <span className="text-xs font-semibold text-white">Synthesizing on server...</span>
                                </div>
                                <span className="text-[10px] text-zinc-400 leading-normal max-w-xs">
                                  Deriving chalkboard video with voiceover. Automatically checks for updates — you can safely leave this page.
                                </span>
                              </div>
                            ) : (
                              <div className="text-xs text-red-400 font-medium">Derivation Failed</div>
                            )}

                            <div className="absolute top-2 left-2 px-2.5 py-0.5 rounded-md bg-black/80 text-[10px] font-semibold text-white">
                              {job.subject?.toUpperCase() || "GENERAL"}
                            </div>

                            <div className="absolute top-2 right-2 px-2.5 py-0.5 rounded-md bg-black/80 text-[10px] font-semibold text-zinc-300">
                              {isCompleted ? "COMPLETED" : isPending ? "PROCESSING" : "FAILED"}
                            </div>
                          </div>

                          {/* Card Content */}
                          <div className="p-4 sm:p-5 flex-1 flex flex-col justify-between">
                            <div>
                              <h3 className="font-semibold text-base text-[#09090B] line-clamp-1 mb-1">
                                {job.lesson_plan?.problem_title || job.query}
                              </h3>
                              {job.lesson_plan?.core_concept && (
                                <p className="text-xs font-medium text-[#52525B] line-clamp-1 mb-2">
                                  ✦ {job.lesson_plan.core_concept}
                                </p>
                              )}
                              <p className="text-xs text-[#71717A] line-clamp-2">
                                "{job.query}"
                              </p>
                            </div>

                            <div className="mt-4 pt-3 border-t border-[#F4F4F5] flex items-center justify-between text-[11px] text-[#A1A1AA]">
                              <span className="flex items-center gap-1 font-medium text-[#71717A]">
                                <Clock size={13} />
                                {dateStr}
                              </span>
                              <span>ID: {job.job_id.slice(0, 8)}</span>
                            </div>
                          </div>

                          {/* Actions */}
                          {isCompleted && job.video_url && (
                            <div className="px-4 py-3 bg-[#F4F4F5] border-t border-[#E4E4E7] flex items-center justify-between gap-2">
                              <button
                                onClick={() => handleCopyLink(job.video_url!, job.job_id)}
                                className="flex-1 py-1.5 px-3 rounded-lg border border-[#E4E4E7] bg-[#FFFFFF] hover:bg-[#F4F4F5] text-xs font-semibold text-[#52525B] flex items-center justify-center gap-1.5 transition-colors cursor-pointer"
                              >
                                {copiedJobId === job.job_id ? (
                                  <span className="text-green-700 font-semibold">Copied!</span>
                                ) : (
                                  <>
                                    <Copy size={13} />
                                    <span>Copy Link</span>
                                  </>
                                )}
                              </button>

                              <a
                                href={job.video_url}
                                download={`chalkka_${job.job_id}.mp4`}
                                target="_blank"
                                rel="noreferrer"
                                className="py-1.5 px-3 rounded-lg btn-primary text-xs font-semibold flex items-center justify-center gap-1.5 cursor-pointer shadow-xs"
                              >
                                <DownloadSimple size={13} />
                                <span>Download</span>
                              </a>
                            </div>
                          )}
                        </motion.div>
                      );
                    })}
                  </motion.div>
                )}
              </motion.div>
            )}

            {/* =====================================================================
                VIEW 3: CREDITS & LEDGER (Balance, Classroom Grants, Usage breakdown)
            ====================================================================== */}
            {activeTab === "credits" && (
              <motion.div 
                key="credits"
                variants={pageContainerVariants}
                initial="initial"
                animate="animate"
                exit="exit"
                className="space-y-6"
              >
                <motion.div variants={revealItemVariants}>
                  <h1 className="font-bold text-2xl sm:text-3xl text-[#09090B] tracking-tight">
                    Credits & Billing
                  </h1>
                  <p className="text-sm text-[#52525B] mt-1">
                    Transparent credit balance and usage breakdown for chalkboard video generations.
                  </p>
                </motion.div>

                {/* Main Balance Card */}
                <motion.div 
                  variants={revealItemVariants}
                  className="rounded-2xl bg-[#FFFFFF] border border-[#E4E4E7] p-6 sm:p-8 shadow-xs"
                >
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-6 pb-6 border-b border-[#F4F4F5]">
                    <div>
                      <span className="text-xs uppercase font-semibold text-[#71717A] tracking-wider block mb-1">
                        Available Balance
                      </span>
                      <div className="flex items-baseline gap-2">
                        <span className="font-extrabold text-5xl text-[#09090B]">
                          {user?.credits ?? 0}
                        </span>
                        <span className="text-sm font-semibold text-[#52525B]">Credits Remaining</span>
                      </div>
                      <span className="text-xs text-[#71717A] block mt-1.5">
                        Each complete whiteboard video lesson consumes 5 credits.
                      </span>
                    </div>

                    <div className="flex flex-col sm:items-end gap-2">
                      <button
                        onClick={handleRecharge}
                        disabled={isRecharging}
                        className="px-5 py-2.5 rounded-xl btn-primary text-xs font-semibold inline-flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50 shadow-sm hover:scale-[1.02] active:scale-[0.98] transition-transform"
                      >
                        <PlusCircle size={16} weight="bold" />
                        <span>{isRecharging ? "Adding..." : "Request +25 Grant Credits"}</span>
                      </button>
                      {rechargeSuccess && (
                        <span className="text-xs text-green-700 font-semibold">
                          ✓ 25 credits added to your account!
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Usage Breakdown */}
                  <motion.div 
                    variants={cardStaggerVariants}
                    className="pt-6 grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs"
                  >
                    <motion.div 
                      variants={cardRevealVariants}
                      whileHover={{ y: -2 }}
                      className="p-5 rounded-xl bg-[#F4F4F5] border border-[#E4E4E7] transition-shadow"
                    >
                      <span className="font-semibold text-[#09090B] block mb-1">AI Lesson Planning</span>
                      <p className="text-[#52525B]">Diagnoses missing fundamentals and structures pedagogical chapters.</p>
                    </motion.div>
                    <motion.div 
                      variants={cardRevealVariants}
                      whileHover={{ y: -2 }}
                      className="p-5 rounded-xl bg-[#F4F4F5] border border-[#E4E4E7] transition-shadow"
                    >
                      <span className="font-semibold text-[#09090B] block mb-1">Video Rendering</span>
                      <p className="text-[#52525B]">Draws stroke-by-stroke equations and schematic diagrams in 1080p.</p>
                    </motion.div>
                    <motion.div 
                      variants={cardRevealVariants}
                      whileHover={{ y: -2 }}
                      className="p-5 rounded-xl bg-[#F4F4F5] border border-[#E4E4E7] transition-shadow"
                    >
                      <span className="font-semibold text-[#09090B] block mb-1">Voice Synthesis</span>
                      <p className="text-[#52525B]">Generates natural classroom pacing timed directly to board writing.</p>
                    </motion.div>
                  </motion.div>
                </motion.div>
              </motion.div>
            )}
          </AnimatePresence>
        </main>
      </div>

      {/* =========================================================================
          MOBILE BOTTOM NAVIGATION (Strictly the 3 core items with animated indicator)
      ========================================================================== */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-[#FFFFFF] border-t border-[#E4E4E7] flex items-center justify-around py-2.5 px-3 shadow-lg">
        <button
          onClick={() => setActiveTab("studio")}
          className={`relative flex flex-col items-center gap-1 p-1 text-[11px] font-semibold transition-colors ${
            activeTab === "studio" ? "text-[#09090B]" : "text-[#71717A]"
          }`}
        >
          {activeTab === "studio" && (
            <motion.div
              layoutId="mobileActiveIndicator"
              className="absolute -top-2.5 w-8 h-1 bg-[#09090B] rounded-full"
              transition={{ type: "spring", stiffness: 450, damping: 35 }}
            />
          )}
          <PencilSimpleLine size={20} weight={activeTab === "studio" ? "bold" : "regular"} />
          <span>Studio</span>
        </button>

        <button
          onClick={() => setActiveTab("archive")}
          className={`relative flex flex-col items-center gap-1 p-1 text-[11px] font-semibold transition-colors ${
            activeTab === "archive" ? "text-[#09090B]" : "text-[#71717A]"
          }`}
        >
          {activeTab === "archive" && (
            <motion.div
              layoutId="mobileActiveIndicator"
              className="absolute -top-2.5 w-8 h-1 bg-[#09090B] rounded-full"
              transition={{ type: "spring", stiffness: 450, damping: 35 }}
            />
          )}
          <FilmStrip size={20} weight={activeTab === "archive" ? "bold" : "regular"} />
          <span>Lessons ({jobs.length})</span>
        </button>

        <button
          onClick={() => setActiveTab("credits")}
          className={`relative flex flex-col items-center gap-1 p-1 text-[11px] font-semibold transition-colors ${
            activeTab === "credits" ? "text-[#09090B]" : "text-[#71717A]"
          }`}
        >
          {activeTab === "credits" && (
            <motion.div
              layoutId="mobileActiveIndicator"
              className="absolute -top-2.5 w-8 h-1 bg-[#09090B] rounded-full"
              transition={{ type: "spring", stiffness: 450, damping: 35 }}
            />
          )}
          <Coins size={20} weight={activeTab === "credits" ? "fill" : "regular"} />
          <span>Credits ({user?.credits ?? 0})</span>
        </button>
      </nav>

      {/* Auth Modal */}
      <AuthModal />
    </div>
  );
}

export default function DashboardPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center text-xs font-mono">Loading Studio...</div>}>
      <DashboardContent />
    </Suspense>
  );
}
