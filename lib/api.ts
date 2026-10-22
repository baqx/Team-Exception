// API client for interacting with Chalkka's FastAPI backend

export interface ChalkAction {
  action_type: "write_latex" | "draw_circuit" | "circle_term" | "box_answer" | "strike_through";
  content: string;
  color: "white" | "yellow" | "cyan";
  duration_sec?: number;
}

export interface ScenePlan {
  step_number: number;
  title: string;
  category: "prerequisite" | "concept" | "solution" | "verification";
  spoken_script: string;
  chalk_actions: ChalkAction[];
  key_latex_formula?: string;
}

export interface LessonPlan {
  problem_title: string;
  subject: string;
  core_concept: string;
  prerequisites: string[];
  estimated_duration_sec: number;
  scenes: ScenePlan[];
}

export interface JobStatus {
  job_id: string;
  status: "pending" | "analyzing" | "synthesizing_audio" | "rendering_video" | "stitching" | "completed" | "failed";
  progress_percent: number;
  current_step_text: string;
  video_url?: string;
  lesson_plan?: LessonPlan;
  error_message?: string;
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "/api/backend";

export interface StartGenerationResult {
  job_id: string;
  status: string;
  message: string;
  remaining_credits?: number;
}

/**
 * Initiates video generation job with problem query, subject, length, optional attachment, and optional userId.
 */
export async function startGenerationJob(payload: {
  query: string;
  subject?: string;
  length?: string;
  file?: File | null;
  userId?: string;
}): Promise<StartGenerationResult> {
  const formData = new FormData();
  formData.append("query", payload.query);
  formData.append("subject", payload.subject || "auto");
  formData.append("length", payload.length || "standard");
  if (payload.file) {
    formData.append("file", payload.file);
  }
  if (payload.userId) {
    formData.append("user_id", payload.userId);
  }

  const res = await fetch(`${API_BASE}/generate`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Server returned ${res.status}`);
  }

  return res.json();
}

/**
 * Register a new user account (awards initial 50 credits)
 */
export async function registerUser(payload: {
  email: string;
  password: string;
  name: string;
}): Promise<{ success: boolean; token: string; user: import("@/lib/types").User; message: string }> {
  const res = await fetch(`${API_BASE}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Registration failed (${res.status})`);
  }

  return res.json();
}

/**
 * Log in an existing user
 */
export async function loginUser(payload: {
  email: string;
  password: string;
}): Promise<{ success: boolean; token: string; user: import("@/lib/types").User }> {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Login failed (${res.status})`);
  }

  return res.json();
}

/**
 * Fetch current user profile and credit balance
 */
export async function fetchCurrentUser(token: string): Promise<{ user: import("@/lib/types").User }> {
  const res = await fetch(`${API_BASE}/auth/me`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!res.ok) {
    throw new Error("Session expired or invalid.");
  }

  return res.json();
}

/**
 * Request a free classroom credit top-up / grant
 */
export async function rechargeCredits(
  token: string, 
  amount: number = 25
): Promise<{ success: boolean; credits: number; message: string }> {
  const res = await fetch(`${API_BASE}/user/credits/recharge`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ amount }),
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || "Failed to recharge credits.");
  }

  return res.json();
}

/**
 * Fetch list of all past generated videos and jobs for user
 */
export async function fetchUserHistory(
  token: string
): Promise<{ jobs: import("@/lib/types").UserJob[]; credits: number }> {
  const res = await fetch(`${API_BASE}/user/history`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || "Failed to fetch user history.");
  }

  return res.json();
}

/**
 * Fetches the current status of a generation job.
 */
export async function fetchJobStatus(jobId: string): Promise<JobStatus> {
  const res = await fetch(`${API_BASE}/status/${jobId}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch status for job ${jobId}`);
  }
  return res.json();
}

/**
 * Polls job status until it reaches 'completed' or 'failed'.
 * Resilient against transient network dropouts and supports extended video renders up to 10 minutes.
 */
export async function pollJobUntilFinished(
  jobId: string,
  onProgress?: (status: JobStatus) => void,
  intervalMs: number = 2000,
  maxAttempts: number = 300
): Promise<JobStatus> {
  let attempts = 0;
  let consecutiveErrors = 0;

  while (attempts < maxAttempts) {
    attempts++;
    try {
      const status = await fetchJobStatus(jobId);
      consecutiveErrors = 0;

      if (onProgress) {
        onProgress(status);
      }

      if (status.status === "completed") {
        return status;
      }
      if (status.status === "failed") {
        throw new Error(status.error_message || "Video generation failed on backend.");
      }
    } catch (err: any) {
      // If the error was an explicit failed job from backend, propagate it
      if (err?.message?.includes("Video generation failed on backend") || err?.message?.includes("failed")) {
        throw err;
      }

      consecutiveErrors++;
      console.warn(`[Chalkka Polling] Transient connection error for job ${jobId} (attempt ${attempts}/${maxAttempts}):`, err);

      // Only give up if connection fails repeatedly 8 times in a row
      if (consecutiveErrors >= 8) {
        throw new Error("Lost connection to generation server. Please check your network connection.");
      }
    }

    await new Promise((resolve) => setTimeout(resolve, intervalMs));
  }

  throw new Error("Job rendering is taking longer than expected. You can monitor it in My Lessons.");
}

/**
 * Requests regeneration of a single specific scene/step.
 */
export async function requestStepRegeneration(payload: {
  jobId: string;
  sceneIndex: number;
  feedback?: string;
}): Promise<{ job_id: string; message: string }> {
  const formData = new FormData();
  formData.append("job_id", payload.jobId);
  formData.append("scene_index", payload.sceneIndex.toString());
  if (payload.feedback) {
    formData.append("feedback", payload.feedback);
  }

  const res = await fetch(`${API_BASE}/regenerate-step`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Server returned ${res.status}`);
  }

  return res.json();
}

import { GeneratedDemoLesson, LessonStep } from "@/lib/types";

/**
 * Transforms a backend LessonPlan into the frontend GeneratedDemoLesson format.
 */
export function lessonPlanToDemoLesson(plan: LessonPlan): GeneratedDemoLesson {
  return {
    id: "generated-lesson",
    title: plan.problem_title || "Step-by-Step Chalkboard Lesson",
    subject: plan.subject || "General Engineering",
    targetEquation: plan.scenes[0]?.key_latex_formula || "\\text{Derivation}",
    estimatedDuration: `~${Math.max(1, Math.round(plan.estimated_duration_sec / 60))} min`,
    conceptDetected: plan.core_concept || "Core Fundamentals",
    prerequisites: plan.prerequisites || [],
    steps: plan.scenes.map((scene, idx): LessonStep => ({
      id: scene.step_number || idx + 1,
      title: scene.title,
      duration: "0:45",
      category: scene.category || "concept",
      boardContent: scene.chalk_actions?.map((a) => a.content) || [scene.title],
      spokenScript: scene.spoken_script || "",
      latexSnippets: scene.key_latex_formula ? [scene.key_latex_formula] : [],
    })),
  };
}

