export type SubjectId = 
  | "electrical" 
  | "maths" 
  | "physics" 
  | "chemistry" 
  | "mechanical" 
  | "computer_science";

export type VideoLength = "short" | "standard" | "detailed";

export interface SubjectOption {
  id: SubjectId;
  label: string;
  iconName: string;
  popularTopics: string[];
  sampleProblem: string;
}

export type TutorLanguage = "en" | "pidgin" | "yo" | "ha" | "ig";

export interface ProblemGenerationRequest {
  query: string;
  subject: SubjectId;
  length: VideoLength;
  voice?: string;
  language?: TutorLanguage;
  hasAttachment?: boolean;
  attachmentName?: string;
  userId?: string;
}

export interface TutorVoiceOption {
  id: string;
  voiceName: string;
  provider: "edge" | "yarngpt";
  displayName: string;
  description: string;
  accent: string;
  gender: "male" | "female";
  badge?: string;
  isDefault?: boolean;
}

export interface LessonStep {
  id: number;
  title: string;
  duration: string;
  category: "prerequisite" | "concept" | "solution" | "verification";
  boardContent: string[];
  spokenScript: string;
  latexSnippets: string[];
}

export interface GeneratedDemoLesson {
  id: string;
  title: string;
  subject: string;
  targetEquation: string;
  estimatedDuration: string;
  conceptDetected: string;
  prerequisites: string[];
  steps: LessonStep[];
}

export interface User {
  id: string;
  email: string;
  name: string;
  credits: number;
  created_at?: string;
}

export interface UserJob {
  job_id: string;
  user_id?: string;
  query: string;
  subject?: string;
  length?: string;
  status: "pending" | "analyzing" | "synthesizing_audio" | "rendering_video" | "stitching" | "completed" | "failed";
  video_url?: string | null;
  lesson_plan?: any | null;
  created_at?: string;
  completed_at?: string | null;
}
