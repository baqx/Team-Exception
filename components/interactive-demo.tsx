"use client";

import React, { useState, useEffect, useRef } from "react";
import { 
  Play, 
  Pause, 
  ArrowCounterClockwise, 
  SpeakerHigh, 
  DownloadSimple, 
  ArrowsClockwise, 
  GraduationCap, 
  Lightning,
  Clock,
  CornersOut,
  Waveform,
  FilmStrip,
  PencilSimpleLine
} from "@phosphor-icons/react";
import { DEMO_LESSON_ELEVATOR } from "@/lib/mock-data";
import { GeneratedDemoLesson } from "@/lib/types";
import { MathTex, FormattedChalkContent } from "@/components/math-tex";
import { motion } from "framer-motion";

interface InteractiveDemoProps {
  customLesson?: GeneratedDemoLesson | null;
  videoUrl?: string | null;
}

export function InteractiveDemo({ customLesson, videoUrl }: InteractiveDemoProps) {
  const [activeStepIndex, setActiveStepIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackProgress, setPlaybackProgress] = useState(15);
  const [isRegenerating, setIsRegenerating] = useState(false);
  const [speed, setSpeed] = useState<"1x" | "1.25x" | "1.5x">("1x");
  const [playerMode, setPlayerMode] = useState<"video" | "stroke">("video");
  const videoRef = useRef<HTMLVideoElement>(null);

  const lesson = customLesson || DEMO_LESSON_ELEVATOR;
  const currentStep = lesson.steps[Math.min(activeStepIndex, lesson.steps.length - 1)] || DEMO_LESSON_ELEVATOR.steps[0];
  const effectiveVideoUrl = videoUrl || "https://res.cloudinary.com/dzbruqmmb/video/upload/v1792766925/chalkka_lessons/lesson_0c0b9730-696.mp4";

  // Playback timer & auto-advance
  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isPlaying && playerMode === "stroke") {
      const speedMultiplier = speed === "1x" ? 1 : speed === "1.25x" ? 1.25 : 1.5;
      interval = setInterval(() => {
        setPlaybackProgress((prev) => {
          if (prev >= 100) {
            // Automatically advance to next step or loop back to step 0
            setActiveStepIndex((current) => (current + 1) % lesson.steps.length);
            return 0;
          }
          return prev + 1.2 * speedMultiplier;
        });
      }, 100);
    }
    return () => clearInterval(interval);
  }, [isPlaying, speed, playerMode, lesson.steps.length]);

  const handleRegenerateStep = () => {
    setIsRegenerating(true);
    setIsPlaying(false);
    setPlaybackProgress(0);
    setTimeout(() => {
      setIsRegenerating(false);
      setIsPlaying(true);
    }, 1000);
  };

  const handleStepSelect = (idx: number) => {
    setActiveStepIndex(idx);
    setPlaybackProgress(5);
  };

  // Determine progressive line revelation
  const visibleLinesCount = Math.max(
    1,
    Math.min(
      currentStep.boardContent.length,
      Math.floor((playbackProgress / 100) * (currentStep.boardContent.length + 1))
    )
  );

  return (
    <section 
      id="interactive-demo" 
      className="relative py-20 sm:py-28 px-4 sm:px-6 lg:px-8 border-t border-[#E2E8F0] bg-[#FFFFFF]"
    >
      <div className="max-w-5xl mx-auto">
        {/* Section Header */}
        <motion.div 
          initial={{ opacity: 0, y: 15 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center max-w-2xl mx-auto mb-10"
        >
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-zinc-100 border border-zinc-200 text-xs font-semibold text-zinc-800 mb-4">
            <GraduationCap size={15} weight="fill" className="text-zinc-900" />
            <span>✦ Newton&apos;s Second Law and Normal Force</span>
          </div>
          <h2 className="font-bold text-3xl sm:text-4xl text-[#09090B] tracking-tight">
            Apparent Weight in an Accelerating Elevator
          </h2>
          <p className="mt-3 text-xs sm:text-sm text-[#52525B] font-mono bg-zinc-50 border border-zinc-200/80 rounded-xl px-4 py-2.5 max-w-xl mx-auto shadow-2xs">
            &ldquo;Teach me Motion in an elevator in terms of g, weight and f and a with diagrams&rdquo;
          </p>

          {/* Mode Selector */}
          <div className="mt-6 inline-flex items-center p-1 rounded-xl bg-zinc-100 border border-zinc-200/80">
            <button
              type="button"
              onClick={() => setPlayerMode("stroke")}
              className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                playerMode === "stroke"
                  ? "bg-[#09090B] text-white shadow-xs font-semibold"
                  : "text-[#52525B] hover:text-[#09090B]"
              }`}
            >
              <PencilSimpleLine size={15} weight="bold" />
              <span>Chalkboard Derivation Board</span>
            </button>
            <button
              type="button"
              onClick={() => setPlayerMode("video")}
              className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                playerMode === "video"
                  ? "bg-[#09090B] text-white shadow-xs font-semibold"
                  : "text-[#52525B] hover:text-[#09090B]"
              }`}
            >
              <FilmStrip size={15} weight="bold" />
              <span>Rendered Video (MP4)</span>
            </button>
          </div>
        </motion.div>

        {/* Centered Wide Cinematic Chalkboard Stage */}
        <div className="w-full flex flex-col gap-4">
          <div className="relative rounded-2xl bg-[#0F172A] border border-slate-800 p-2.5 sm:p-4 shadow-2xl">
            {/* The Chalkboard Stage */}
            <div className="relative aspect-video sm:aspect-[16/9.5] w-full rounded-xl bg-[#000000] chalkboard-surface border border-white/10 p-4 sm:p-7 flex flex-col justify-between overflow-hidden shadow-2xl">
              {/* Top Video Header */}
              <div className="relative z-10 flex items-center justify-between border-b border-white/[0.08] pb-2.5 text-xs text-[#8E95A2]">
                <div className="flex items-center gap-2">
                  <span className={`w-2 h-2 rounded-xs ${isPlaying ? "bg-emerald-400 animate-pulse" : "bg-[#E8D479]"}`} />
                  <span className="font-mono text-white text-[11px] uppercase tracking-wider">
                    Chapter {currentStep.id} of {lesson.steps.length}: {currentStep.title}
                  </span>
                </div>
                <div className="flex items-center gap-3 font-mono text-[11px] text-[#709AD8]">
                  <span className="hidden sm:inline-flex items-center gap-1.5 px-2 py-0.5 rounded bg-[#1A1F28] border border-white/[0.06]">
                    <span className="w-1.5 h-1.5 rounded-xs bg-[#709AD8]" />
                    {currentStep.category.toUpperCase()}
                  </span>
                  <span>{playerMode === "video" ? "MP4 VIDEO PLAYER" : "PROGRESSIVE CHALKBOARD"}</span>
                </div>
              </div>

              {/* Main Content Area based on Selected Mode */}
              {playerMode === "video" ? (
                /* MP4 Rendered Video Player */
                <div className="relative z-10 my-auto py-2 flex flex-col items-center justify-center w-full h-full max-h-[440px]">
                  <video
                    ref={videoRef}
                    key={effectiveVideoUrl}
                    src={effectiveVideoUrl}
                    controls
                    playsInline
                    preload="auto"
                    onPlay={() => setIsPlaying(true)}
                    onPause={() => setIsPlaying(false)}
                    onError={(e) => {
                      // Fallback to local demo if proxied URL is unavailable
                      const target = e.currentTarget;
                      if (!target.src.endsWith("/demo_lesson.mp4")) {
                        target.src = "/demo_lesson.mp4";
                      }
                    }}
                    className="w-full max-h-[420px] rounded-lg object-contain bg-black border border-white/10 shadow-2xl"
                  />
                </div>
              ) : (
                /* Interactive Progressive Chalkboard */
                <div className="relative z-10 my-auto py-3 sm:py-5 flex flex-col gap-4">
                  {/* Board Content Box with dynamic progressive chalk strokes */}
                  <div className="p-4 sm:p-6 rounded-xl bg-black border border-white/[0.08] relative overflow-hidden">
                    {/* Subtle chalk wipe animation when regenerating */}
                    {isRegenerating && (
                      <div className="absolute inset-0 bg-[#000000]/95 z-20 flex items-center justify-center gap-2 text-xs font-mono text-[#E8D479] animate-pulse">
                        <ArrowsClockwise size={18} className="animate-spin text-[#E8D479]" />
                        <span>Erasing board & re-deriving alternative step...</span>
                      </div>
                    )}

                    {/* Dynamic Step Title */}
                    <div className="flex items-center justify-between mb-4 border-b border-white/[0.08] pb-2">
                      <span className="font-semibold text-xl sm:text-2xl text-[#E8D479] tracking-tight">
                        {currentStep.title}
                      </span>
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-white/[0.04] text-[#8E95A2] border border-white/[0.06]">
                        {currentStep.duration}
                      </span>
                    </div>

                    {/* Single Unified Blackboard Canvas Flowing Downward */}
                    <div className="flex flex-col gap-4">
                      {/* Prerequisite / Active Reference Recall */}
                      {currentStep.latexSnippets?.[0] && (
                        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-white/[0.04] border border-[#E8D479]/30 text-xs text-[#E8D479] w-fit">
                          <span className="font-mono font-bold">✎ Recall / Rule:</span>
                          <MathTex math={currentStep.latexSnippets[0]} displayMode={false} />
                        </div>
                      )}

                      {/* Progressive Derivation Lines */}
                      <div className="flex flex-col gap-3 font-sans text-sm sm:text-base text-[#F5F5F0]/95">
                        {currentStep.boardContent.map((line, idx) => {
                          const isVisible = idx < visibleLinesCount;
                          const isCurrentlyWriting = isPlaying && idx === visibleLinesCount - 1;

                          return (
                            <div 
                              key={idx} 
                              className={`flex items-start gap-2.5 transition-all duration-300 ${
                                isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-2 pointer-events-none"
                              }`}
                            >
                              <span className="text-[#709AD8] select-none font-bold text-sm shrink-0">›</span>
                              <div className="leading-relaxed relative flex-1">
                                <FormattedChalkContent text={line} />
                                {/* Angled chalk stick leading the active writing stroke */}
                                {isCurrentlyWriting && (
                                  <span className="inline-flex items-center gap-1 ml-2 align-middle">
                                    <span className="w-4 h-2 bg-[#E8D479] rounded-xs shadow-xs transform rotate-45 inline-block opacity-95 animate-pulse border border-yellow-200" />
                                    <span className="w-1.5 h-1.5 rounded-full bg-white shadow-glow inline-block" />
                                  </span>
                                )}
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    </div>

                    {/* Bottom Full-Width Banner: Verified Result Box */}
                    <div className="mt-3 p-3.5 rounded-xl bg-[#161920] border-2 border-[#E8D479]/60 shadow-lg flex flex-wrap items-center justify-between gap-3">
                      <div className="flex items-center gap-3">
                        <span className="text-xs font-mono text-[#E8D479] font-bold uppercase tracking-wider flex items-center gap-1">
                          <span>★</span>
                          <span>Boxed Result:</span>
                        </span>
                        <div className="text-xs sm:text-sm text-[#E8D479] chalk-yellow-glow font-bold">
                          <MathTex 
                            math={currentStep.latexSnippets?.[currentStep.latexSnippets.length - 1] || lesson.targetEquation || "\\text{Result Verified}"} 
                            displayMode={false} 
                          />
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="text-emerald-400 font-bold text-sm">✦</span>
                        <span className="text-[11px] font-mono text-emerald-400">✓ Pedagogically Verified</span>
                      </div>
                    </div>
                  </div>

                  {/* Subtitle / Live Spoken Script Bar with Animated Waveform Equalizer */}
                  <div className="flex items-center justify-between gap-3 px-3.5 py-2.5 rounded-lg bg-[#0F1115]/95 border border-white/[0.08] text-xs text-[#8E95A2]">
                    <div className="flex items-center gap-2.5 overflow-hidden">
                      <SpeakerHigh size={16} weight="duotone" className={`shrink-0 ${isPlaying ? "text-[#E8D479] animate-pulse" : "text-[#5E6778]"}`} />
                      <span className="italic truncate text-[#D0D4DD]">
                        "{currentStep.spokenScript}"
                      </span>
                    </div>

                    {/* Animated Voice Equalizer Bars */}
                    <div className="flex items-center gap-1 shrink-0 px-2 py-0.5 rounded bg-black/40 border border-white/[0.04]">
                      <span className={`w-0.5 rounded-xs bg-[#E8D479] transition-all duration-150 ${isPlaying ? "h-3 animate-pulse" : "h-1 opacity-40"}`} />
                      <span className={`w-0.5 rounded-xs bg-[#E8D479] transition-all duration-200 ${isPlaying ? "h-4 animate-bounce" : "h-1 opacity-40"}`} />
                      <span className={`w-0.5 rounded-xs bg-[#E8D479] transition-all duration-100 ${isPlaying ? "h-2.5 animate-pulse" : "h-1 opacity-40"}`} />
                      <span className={`w-0.5 rounded-xs bg-[#E8D479] transition-all duration-300 ${isPlaying ? "h-4.5 animate-bounce" : "h-1 opacity-40"}`} />
                      <span className={`w-0.5 rounded-xs bg-[#E8D479] transition-all duration-150 ${isPlaying ? "h-2 animate-pulse" : "h-1 opacity-40"}`} />
                    </div>
                  </div>
                </div>
              )}

              {/* Bottom Video Timeline & Controls (in stroke mode) */}
              {playerMode === "stroke" && (
                <div className="relative z-10 pt-2 border-t border-white/[0.08] flex flex-col gap-2">
                  {/* Scrubbing Bar */}
                  <div 
                    onClick={(e) => {
                      const rect = e.currentTarget.getBoundingClientRect();
                      const clickX = e.clientX - rect.left;
                      const newProgress = Math.max(0, Math.min(100, (clickX / rect.width) * 100));
                      setPlaybackProgress(newProgress);
                    }}
                    className="relative w-full h-2 bg-white/10 rounded-sm overflow-hidden cursor-pointer hover:h-2.5 transition-all"
                    title="Click to seek"
                  >
                    <div 
                      className="h-full bg-[#E8D479] transition-all duration-150 shadow-[0_0_8px_rgba(232,212,121,0.5)]"
                      style={{ width: `${playbackProgress}%` }}
                    />
                  </div>

                  {/* Control Actions */}
                  <div className="flex items-center justify-between text-xs text-[#8E95A2] pt-1">
                    <div className="flex items-center gap-3">
                      {/* Big Play / Pause Toggle */}
                      <button
                        type="button"
                        onClick={() => setIsPlaying(!isPlaying)}
                        className="px-3 py-1.5 rounded-md bg-white/10 hover:bg-[#E8D479] text-[#F5F5F0] hover:text-[#191605] flex items-center gap-1.5 font-medium transition-all cursor-pointer shadow-sm"
                        title={isPlaying ? "Pause Demo" : "Play Demo"}
                      >
                        {isPlaying ? (
                          <>
                            <Pause size={14} weight="fill" />
                            <span>Pause</span>
                          </>
                        ) : (
                          <>
                            <Play size={14} weight="fill" />
                            <span>Play Step</span>
                          </>
                        )}
                      </button>

                      <button
                        type="button"
                        onClick={() => setPlaybackProgress(0)}
                        className="p-1 hover:text-[#F5F5F0] transition-colors cursor-pointer"
                        title="Rewind Current Step"
                      >
                        <ArrowCounterClockwise size={16} />
                      </button>

                      <span className="font-mono text-[11px] text-[#8E95A2]">
                        0:{Math.floor((playbackProgress / 100) * 45) < 10 ? `0${Math.floor((playbackProgress / 100) * 45)}` : Math.floor((playbackProgress / 100) * 45)} / {currentStep.duration}
                      </span>
                    </div>

                    <div className="flex items-center gap-2 sm:gap-3">
                      {/* Regenerate Step Support */}
                      <button
                        type="button"
                        onClick={handleRegenerateStep}
                        disabled={isRegenerating}
                        className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-[#1A1F28] hover:bg-[#242A36] text-[#709AD8] hover:text-[#F5F5F0] border border-[#709AD8]/30 transition-all text-xs cursor-pointer disabled:opacity-50"
                        title="Request an alternative derivation for this specific step"
                      >
                        <ArrowsClockwise size={13} className={isRegenerating ? "animate-spin" : ""} />
                        <span>{isRegenerating ? "Erasing..." : "Regenerate Step"}</span>
                      </button>

                      {/* Speed Selector */}
                      <button
                        type="button"
                        onClick={() => {
                          if (speed === "1x") setSpeed("1.25x");
                          else if (speed === "1.25x") setSpeed("1.5x");
                          else setSpeed("1x");
                        }}
                        className="px-2 py-0.5 rounded bg-white/[0.04] text-[11px] font-mono text-[#8E95A2] hover:text-[#F5F5F0] border border-white/[0.06] cursor-pointer"
                      >
                        {speed}
                      </button>

                      {/* Download Button */}
                      <a
                        href={effectiveVideoUrl}
                        download="chalkka_lesson.mp4"
                        className="p-1 rounded text-[#8E95A2] hover:text-[#F5F5F0] transition-colors cursor-pointer inline-flex items-center"
                        title="Download Lesson Video"
                      >
                        <DownloadSimple size={16} />
                      </a>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Step Chapter Navigation Tabs Underneath */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 mt-3">
              {lesson.steps.map((step, idx) => {
                const isCurrent = activeStepIndex === idx;
                return (
                  <button
                    key={step.id || idx}
                    onClick={() => handleStepSelect(idx)}
                    className={`text-left p-3 rounded-xl border transition-all text-xs cursor-pointer ${
                      isCurrent
                        ? "bg-[#181C23] border-[#709AD8]/60 text-[#F5F5F0] shadow-md ring-1 ring-[#709AD8]/20"
                        : "bg-[#121417] border-white/[0.06] text-[#8E95A2] hover:bg-white/[0.03] hover:text-[#F5F5F0]"
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className={`font-mono text-[10px] ${isCurrent ? "text-[#E8D479] font-bold" : "text-[#709AD8]"}`}>
                        Step {step.id}
                      </span>
                      <span className="font-mono text-[10px] text-[#5E6778]">{step.duration}</span>
                    </div>
                    <div className="truncate font-medium">{step.title}</div>
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

