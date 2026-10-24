# Chalkka — Product Requirement Document (PRD)
**Autonomous AI Chalkboard Lecture Synthesizer for STEM & Engineering Education**

> **Document Version**: 2.0.0 (Production Release & Hackathon Submission)  
> **Target Track**: AI for Education / Cultural AI / Multimodal Generative Media  
> **Status**: Live / Production Ready  
> **Platform**: Web Application (Next.js 14 + FastAPI + Gemini + YarnGPT + Cloudinary + Supabase)  

---

## 1. Executive Summary

### 1.1 The Vision
**Chalkka** is the world’s first autonomous AI chalkboard lecture synthesizer engineered specifically for STEM and quantitative reasoning. By combining multimodal vision, structured pedagogical prompt engineering, programmatic chalkboard visual simulation, and dual-engine neural voice synthesis (featuring authentic African voices powered by **YarnGPT**), Chalkka turns any handwritten problem statement, textbook schematic, or homework roadblock into an engaging, 1080p animated chalkboard video lecture in under 20 seconds.

### 1.2 The Innovation
Traditional AI educational tools produce either dense, unreadable walls of markdown text or static ASCII diagrams that fail to communicate spatial relationships. Conversely, video repositories like YouTube force students to scrub through 40-minute generic lectures hoping someone touches their specific diagram.

Chalkka bridges this divide through a **Neuro-Symbolic Chalkboard Engine**:
1. **Multimodal Diagnostic Extraction**: Students can paste questions or upload handwritten notes/PDFs. The system automatically extracts circuit schematics, free-body diagrams, and algebraic constraints using **Google Gemini Vision**.
2. **First-Principles Blackboard Derivations**: Formulates a scene-by-scene lesson plan that draws diagrams, circles variables, applies theorems, and derives results step-by-step.
3. **Cultural & Vernacular Localization**: Spoken narration adapts to the student’s native linguistic context—supporting **Academic English, Naija Pidgin, Yorùbá, Hausa, and Ìgbò**—while keeping mathematical derivations 100% rigorous.
4. **Dual-Engine Neural Audio**: Dynamically routes between **Global Academic** voices (Dr. Christopher via Edge-TTS) and **Authentic African Accents** (Idera, Prof. Emma, Umar, Chinenye via **YarnGPT AI**), demystifying abstract engineering concepts in voices students trust.

---

## 2. Problem Statement & Market Opportunity

### 2.1 The Core Dilemma in STEM Learning
STEM students globally (and especially across emerging markets in Africa) encounter three compounding friction points when studying complex quantitative disciplines:

| Problem Vector | Current Alternative | Failure Mode |
|---|---|---|
| **Text-Only AI (ChatGPT / Claude)** | Generates 800-word text responses filled with detached LaTeX strings. | **Cognitive Overload**: 82% of students report mental fatigue when attempting to parse spatial math concepts without progressive visual derivation. |
| **Static Video Libraries (YouTube / Coursera)** | 35-minute prerecorded video lectures. | **The Scrubbing Trap**: One-size-fits-all content that never addresses the student's exact boundary conditions, resistor values, or custom circuit topologies. |
| **Cultural & Linguistic Alienation** | Foreign, robotic American/British synthetic voices. | **Comprehension Drop-off**: Foreign accents create cognitive friction for non-native English speakers. Relatable campus cadence and native dialects dramatically enhance concept retention. |

```mermaid
graph TD
    A[Student Stuck on Complex Problem] --> B{Existing Tools}
    B -->|Text Chatbots| C[Dense Walls of LaTeX Text<br/>No Spatial Diagramming]
    B -->|Video Platforms| D[35-Minute Video Scrubbing<br/>Generic, Non-personalized]
    B -->|Human Tutoring| E[$40-$80/hr Cost<br/>Unavailable at 2 AM]
    
    A --> F[Chalkka Solution]
    F --> G[1. Multimodal Schematic Diagnosis]
    F --> H[2. Animated Chalkboard Derivation]
    F --> I[3. Culturally Fluent YarnGPT Audio]
    F --> J[15-Second Personalized 1080p Video]
```

### 2.2 Market Size (TAM / SAM / SOM)
- **Total Addressable Market (TAM)**: $340B Global EdTech and Digital Tutoring Market.
- **Serviceable Addressable Market (SAM)**: $42B STEM Higher Education & Test Prep Market across Sub-Saharan Africa, South Asia, and North America.
- **Serviceable Obtainable Market (SOM)**: $3.8M Initial Year 1 focus targeting 150,000 engineering, physics, and mathematics university students in Nigeria, Ghana, Kenya, and global STEM diaspora.

---

## 3. Target Audience & User Personas

### Persona 1: "The Stalled Engineering Undergrad" (Tunde, 21 — University of Lagos)
- **Background**: 3rd-year Electrical & Electronics Engineering student.
- **Pain Point**: Stymied at 1:00 AM by a complex Thevenin equivalent circuit with independent dependent sources. Standard textbooks skip intermediate algebraic steps.
- **Chalkka Use Case**: Takes a phone photo of the exam past question, selects **Naija Pidgin** with **Prof. Emma (YarnGPT)**. In 15 seconds, watches the circuit deconstruct node-by-node with intuitive campus explanations.

### Persona 2: "The Overburdened STEM High Schooler" (Amina, 17 — Abuja)
- **Background**: Preparing for WASSCE and UTME Physics examinations.
- **Pain Point**: Struggles with vector decomposition and projectile motion angles in static textbook figures.
- **Chalkka Use Case**: Types `"Teach me motion in an accelerating elevator in terms of normal force, weight, and g"`. Chooses **Idera (YarnGPT)**. Watches an elevator diagram appear on the chalkboard with force vector arrows dynamically color-coded.

### Persona 3: "The Global Academic / AP Student" (Ethan, 19 — Toronto)
- **Background**: 1st-year University Physics student.
- **Pain Point**: Needs rigorous, deliberate derivations of Maxwell’s equations or multivariable integrals.
- **Chalkka Use Case**: Selects **Academic English** with **Dr. Christopher (Global Academic)** for a formal lecture pacing.

---

## 4. Product Architecture & System Pipeline

Chalkka operates on an asynchronous multi-stage pipeline designed for low latency, zero hallucinatory drift, and high visual clarity.

### 4.1 System Topology Diagram

```mermaid
flowchart TB
    subgraph Client["Next.js 14 Frontend (App Router)"]
        UI[Studio Form / Attachment Upload]
        LangSelect[Language & Dialect Selector<br/>EN, Pidgin, Yoruba, Hausa, Igbo]
        VoiceSelect[Tutor Voice Selector<br/>Edge-TTS vs YarnGPT]
        LiveDock[Persistent Generation Status Dock]
        Player[Interactive Chalkboard Player]
    end

    subgraph Backend["FastAPI Microservice (:8000)"]
        Router["/api/generate Endpoint"]
        Worker["Background Task Queue (VideoGenerationWorker)"]
        JobStore["Persistent Job Store (SQLite + Supabase)"]
    end

    subgraph AI["Cognitive & Language Layer"]
        Gemini["Google Gemini 1.5/2.0 Flash<br/>Multimodal Vision + LaTeX Structuring"]
        PromptEngine["Pedagogical Engine & Language Directives"]
    end

    subgraph Synthesis["Media Generation Layer"]
        Pillow["PIL Blackboard Renderer<br/>Chalk Texture, Glow, Schematics"]
        MoviePy["MoviePy Compositor<br/>Clip Assembly & Frame Timing"]
        
        subgraph TTS["SmartTTSProvider Dispatcher"]
            YarnGPT["YarnGPT AI Service<br/>(Prepared Streaming & African Accents)"]
            EdgeTTS["Microsoft Edge-TTS<br/>(Dr. Christopher / Academic English)"]
        end
    end

    subgraph Storage["Cloud Delivery Layer"]
        Cloudinary["Cloudinary Video CDN<br/>(HLS / MP4 Delivery)"]
        SupabaseDB["Supabase Postgres & Auth"]
    end

    UI -->|Multipart POST /api/generate| Router
    Router --> Worker
    Worker --> PromptEngine
    PromptEngine --> Gemini
    Gemini -->|Structured LessonPlan JSON| Worker
    Worker --> TTS
    TTS --> YarnGPT
    TTS --> EdgeTTS
    Worker --> Pillow
    Pillow --> MoviePy
    TTS --> MoviePy
    MoviePy --> Cloudinary
    Worker --> JobStore
    JobStore -.->|Status Polling 2s| LiveDock
    Cloudinary -.->|Stream URL| Player
```

### 4.2 Core Technological Subsystems

#### 1. Multimodal Cognitive Ingestion
- Accepts raw text prompts or image attachments (JPEG, PNG, WebP) and PDF assignments.
- Uses `google-genai` (Gemini Flash) with vision capabilities to transcribe handwriting, locate diagrams, and isolate boundary conditions.

#### 2. Pedagogical Schema Enforcement (`LessonPlan`)
- The output of the AI reasoning layer is strictly validated against a Pydantic schema:
  - `LessonPlan`: Contains `lesson_title`, `discipline`, `prerequisites`, and a sequence of `scenes`.
  - `Scene`: Each scene contains `step_number`, `board_heading`, `latex_equations`, `chalk_diagram`, and `spoken_script`.

#### 3. Programmatic Chalkboard Visual Engine (`ChalkRenderer`)
- Rather than using slow diffusion video models (which suffer from text jitter and formula distortion), Chalkka renders crisp 1080p vectors:
  - **Tactile Background**: Simulates charcoal slate chalkboard (`#0F1412`) with random chalk dust particulate noise.
  - **Mathematical Layout Engine**: Automatically formats equation steps with progressive color coding (amber for substitutions, cyan for theorems, emerald for final boxed answers).
  - **Dynamic Schematic Drawing**: Renders circuit nodes, resistors, capacitors, and free-body vectors programmatically with simulated chalk-stroke roughness.

#### 4. Dual-Engine Neural Voice Dispatcher (`SmartTTSProvider`)
- **YarnGPT AI Provider**:
  - Connects to `https://api.yarngpt.ai/api/v1/tts/prepare` and follows 303 redirects on streaming tickets to synthesize African-accented speech.
  - Curated catalog: `Idera`, `Prof. Emma`, `Umar`, `Chinenye`, `Remi`, `Osagie`, `Nonso`, `Adaora`.
- **Edge-TTS Provider**:
  - High-fidelity Microsoft Edge Neural TTS (`en-US-ChristopherNeural`) for formal global academic lectures.
- **Language Guard**: Dr. Christopher is strictly constrained to English. When non-English dialects are chosen, the worker queue automatically routes to YarnGPT.

#### 5. Audio-Video Stitching & Cloud CDN Delivery
- Synchronizes audio clip length with visual frame persistence so equations appear exactly as spoken.
- Stitches multi-scene clips using MoviePy into a seamless MP4.
- Uploads directly to **Cloudinary** for adaptive bitrate streaming, CDN caching, and instant cross-device sharing.

---

## 5. Feature Requirements & Functional Specifications

### 5.1 Studio Creation Suite
- **Requirement ID**: `FEAT-01`
- **Description**: Central workspace where users formulate their query or upload problem materials.
- **Specifications**:
  - Auto-growing multiline problem statement input with high-impact placeholder prompts.
  - File uploader supporting drag-and-drop of PDFs and Images up to 20MB.
  - Subject auto-detection with fallback manual selector (Electrical Engineering, Physics, Calculus, Chemistry, Mechanical, Computer Science).
  - Target duration picker: *Express (45s)*, *Standard (90s)*, or *Comprehensive (180s)*.

### 5.2 Multilingual Dialect Selector
- **Requirement ID**: `FEAT-02`
- **Description**: Spoken audio language selection while chalkboard formulas remain rigorous.
- **Supported Languages**:
  1. `en` — Academic English (Structured global classroom standard).
  2. `pidgin` — Naija Pidgin (Relatable campus analogies, "no-stress" problem solving).
  3. `yo` — Yorùbá (Indigenous linguistic intuition for deep conceptual retention).
  4. `ha` — Hausa (Direct, methodical step-by-step logic).
  5. `ig` — Ìgbò (Expressive, engaging derivations and practical metaphors).

### 5.3 Tutor Voice & Accent Selector
- **Requirement ID**: `FEAT-03`
- **Description**: Dynamic audio voice selector with live filtering between YarnGPT (African) and Edge-TTS (Global).
- **Behavioral Constraints**:
  - Filtering tabs: *All (8)*, *🇳🇬 African (YarnGPT)*, *🎓 Global (Edge)*.
  - English-Only Protection: Dr. Christopher card displays an `English Only` badge. If a user selects a vernacular dialect, Dr. Christopher is visually marked with a reminder and clicking it switches the dialect back to English.
  - Server-Side Guard: The worker queue intercepts any non-English generation requests directed to Dr. Christopher and auto-routes them to YarnGPT.

### 5.4 Persistent Generation Status Dock
- **Requirement ID**: `FEAT-04`
- **Description**: Real-time progress feedback visible across all dashboard navigation tabs.
- **Specifications**:
  - Multi-stage diagnostic progress tracking (0% → 100%):
    1. *Connecting to Chalkka pipeline...* (10%)
    2. *Analyzing problem statement & diagrams...* (25%)
    3. *Formulating first-principles chalk derivation...* (45%)
    4. *Synthesizing voice narration with classroom pacing...* (60%)
    5. *Drawing chalkboard equations & circuit schematics...* (80%)
    6. *Assembling video & CDN streaming upload...* (95%)
  - Persistent state in `localStorage` allows users to reload or navigate tabs without losing their render state.

### 5.5 Interactive Blackboard Player & Step Regeneration
- **Requirement ID**: `FEAT-05`
- **Description**: High-resolution video player with deep-dive pedagogical controls.
- **Specifications**:
  - 1080p embedded video player with playback rate controls (0.75x, 1x, 1.25x, 1.5x) and full-screen toggle.
  - **Scene Navigation**: Clickable scene timestamps to jump directly to Step 1, Step 2, or Step 3.
  - **Step Regeneration**: If a student is confused by Step 2, they can click *"Re-explain Step 2"* with custom focus angles (e.g. *"Explain with an everyday plumbing analogy"* or *"Show the algebraic proof"*). The system regenerates just that scene clip and restitches the video.
  - Direct 1-click MP4 Download and Copy Shareable URL.

### 5.6 Lesson Archive & Cloud Sync
- **Requirement ID**: `FEAT-06`
- **Description**: Complete historical record of all generated lessons for authenticated users.
- **Specifications**:
  - Grid view of previously generated lessons with subject badges, video duration, and creation timestamp.
  - Cloud database persistence with **Supabase Postgres** and fallback to local SQLite when offline.

---

## 6. Non-Functional Requirements (NFRs)

### 6.1 Performance & Latency
- **End-to-End Generation Time**: $\le 18$ seconds for Standard (90s) lesson on GPU/CPU cloud instance.
- **Audio Synthesis**: $\le 3.5$ seconds for full 4-scene script via YarnGPT prepare endpoint or Edge-TTS.
- **Video Assembly**: 1080p MP4 encoding at 24fps in $\le 6.0$ seconds.

### 6.2 Availability & Resilience
- **Fail-Safe Fallbacks**: If the YarnGPT API encounters an unexpected rate limit or connection timeout, the system automatically falls back to Edge-TTS without aborting the lesson render.
- **Offline / Local Mode**: The backend automatically falls back to SQLite database storage if Supabase credentials are not supplied.

### 6.3 Security & Secret Hygiene
- **Strict Environment Isolation**: API keys (`YARNGPT_API_KEY`, `GOOGLE_GENERATIVE_AI_API_KEY`, `CLOUDINARY_API_SECRET`, `SUPABASE_SECRET_KEY`) are read strictly from `.env.local` / `.env` or system environment variables. No secrets are hardcoded in application logic.
- **Git Scrubbing**: Zero secret leakage verified via continuous repository scanning (`git grep "sk_live_"`).

### 6.4 Visual Craft & Anti-Slop Frontend
- Adheres strictly to modern design standards:
  - Generous whitespace, refined zinc palette (`#09090B`, `#27272A`, `#FAFAFA`).
  - Tactile typography (Geist / Inter / JetBrains Mono for equations).
  - Micro-animations via Framer Motion.
  - No generic purple AI gradients or low-craft stock assets.

---

## 7. Data Models & API Specifications

### 7.1 Core Schema Models (Pydantic / TypeScript)

```typescript
// Lesson Scene Definition
export interface ScenePlan {
  step_number: number;
  board_heading: string;
  latex_equations: string[];
  chalk_diagram?: "circuit_schematic" | "free_body_diagram" | "coordinate_plot" | "vector_graph" | "none";
  spoken_script: string;
}

// Complete Lesson Plan
export interface LessonPlan {
  lesson_title: string;
  discipline: string;
  prerequisites: string[];
  core_theorems: string[];
  scenes: ScenePlan[];
  estimated_duration_sec: number;
}

// User Job State
export interface UserJob {
  id: string;
  query: string;
  subject: string;
  status: "pending" | "analyzing" | "synthesizing_audio" | "rendering_video" | "stitching" | "completed" | "failed";
  progress_percent: number;
  current_step_text: string;
  video_url?: string;
  lesson_plan?: LessonPlan;
  created_at: string;
  voice?: string;
  language?: string;
}
```

### 7.2 REST API Specification

| Endpoint | Method | Payload / Parameters | Description |
|---|---|---|---|
| `/api/generate` | `POST` | `multipart/form-data`: `query`, `subject`, `length`, `voice`, `language`, `file` | Initiates an asynchronous lesson video synthesis job. |
| `/api/jobs/{id}` | `GET` | Path param `id` | Polls the current status, progress percent, stage text, and video URL. |
| `/api/voices` | `GET` | None | Returns the catalog of supported voices across YarnGPT and Edge-TTS. |
| `/api/regenerate-step` | `POST` | JSON: `job_id`, `step_number`, `focus_angle`, `voice` | Re-synthesizes a specific scene derivation with an adjusted angle. |
| `/api/user/history` | `GET` | Header: `Authorization: Bearer <token>` | Retrieves past generated lesson videos for the authenticated student. |
| `/api/user/recharge` | `POST` | JSON: `credits` | Adds credits to the user's account for video generation. |

---

## 8. Unit Economics & Cost Analysis

Chalkka achieves an ultra-low compute cost per video, unlocking high-margin software economics ($> 85\%$ gross margin) even on low-cost student subscription tiers:

| Component | Provider | Unit Consumption | Cost per 90s Lesson |
|---|---|---|---|
| **Cognitive Reasoning** | Google Gemini 1.5 Flash | ~1,200 input tokens + ~800 output tokens | $0.0004 |
| **Neural Voice Synthesis** | YarnGPT AI / Edge-TTS | ~220 spoken words (~1,400 characters) | $0.0050 |
| **Video Rendering Compute** | CPU/GPU Worker (Render / Railway) | ~8 seconds execution time | $0.0040 |
| **Video CDN & Storage** | Cloudinary / Supabase | 1080p MP4 (~8.5 MB) with CDN delivery | $0.0020 |
| **Total COGS per Lesson** | — | — | **$0.0114** (~1.1 cents) |

*Comparison*: A private human tutor costs **$25.00 – $60.00 per hour**. Chalkka provides personalized, infinite 1-on-1 derivations for approximately **1 cent per question**.

---

## 9. Product Roadmap

```mermaid
gantt
    title Chalkka Product Evolution Roadmap
    dateFormat  YYYY-MM-DD
    section Phase 1 (Live MVP)
    Multimodal Vision Ingestion       :done, 2026-09-01, 2026-10-01
    PIL Chalkboard Video Engine       :done, 2026-10-01, 2026-10-15
    YarnGPT African Voice AI          :done, 2026-10-15, 2026-10-22
    Multilingual Dialect Engine       :done, 2026-10-22, 2026-10-24
    section Phase 2 (Q1 2027)
    Real-Time Interactive Voice Q&A   :active, 2026-11-01, 2027-01-15
    LaTeX Drawing Pad on Canvas       :2026-12-01, 2027-02-01
    Native iOS & Android Apps         :2027-01-15, 2027-03-30
    section Phase 3 (Q2 2027)
    B2B Campus LMS Integration (Moodle/Canvas) :2027-03-01, 2027-05-30
    Offline Low-Bandwidth School Mesh Nodes   :2027-05-01, 2027-07-31
```

### Phase 1: Hackathon Release (Current State)
- Full end-to-end video synthesis pipeline (< 20s).
- 8 curated voices across Edge-TTS and YarnGPT AI.
- 5 spoken dialects (English, Naija Pidgin, Yorùbá, Hausa, Ìgbò).
- Interactive dashboard, lesson history, step regeneration, and Cloudinary CDN distribution.

### Phase 2: Conversational Chalkboard (Q1 2027)
- **Live Voice Interruption**: Pause the teacher mid-derivation to ask *"Wait, why did the normal force equal mg cos theta here?"* and have the blackboard adapt in real time.
- **Handwritten Canvas**: Interactive digital slate where students can write equations directly with Apple Pencil / stylus.

### Phase 3: Institutional Campus Scale (Q2 2027)
- **LMS Connector**: Ingest entire university syllabus PDFs and automatically generate supplementary derivation videos for every tutorial sheet.
- **Offline Mesh Sync**: Deploy lightweight Docker containers to local university intranet servers for zero-data video streaming in regions with high internet tariffs.

---

## 10. Conclusion & Hackathon Submission Impact

Chalkka transforms abstract mathematics and engineering from a source of intimidation into an intuitive, visually captivating experience. By bridging high-performance multimodal AI with the cultural warmth and pedagogical power of **YarnGPT African voice synthesis**, Chalkka proves that generative AI can honor regional identity while upholding the highest standards of scientific and algebraic rigor.
