-- ==============================================================================
-- Chalkka Database Schema for Supabase
-- Paste and run this script in the Supabase Dashboard -> SQL Editor
-- ==============================================================================

-- 1. Users Table (Stores user accounts and credit balance)
CREATE TABLE IF NOT EXISTS public.users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    name TEXT NOT NULL,
    credits INTEGER NOT NULL DEFAULT 50,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 2. User Jobs Table (Stores lesson synthesis history and video URLs)
CREATE TABLE IF NOT EXISTS public.user_jobs (
    job_id TEXT PRIMARY KEY,
    user_id TEXT REFERENCES public.users(id) ON DELETE SET NULL,
    query TEXT NOT NULL,
    subject TEXT,
    length TEXT,
    status TEXT DEFAULT 'pending',
    video_url TEXT,
    lesson_plan_json TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    completed_at TIMESTAMP WITH TIME ZONE
);

-- 3. Sessions Table (Stores persistent auth session tokens)
CREATE TABLE IF NOT EXISTS public.sessions (
    token TEXT PRIMARY KEY,
    user_id TEXT REFERENCES public.users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Indices for rapid lookups
CREATE INDEX IF NOT EXISTS idx_users_email ON public.users(email);
CREATE INDEX IF NOT EXISTS idx_user_jobs_user_id ON public.user_jobs(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_token ON public.sessions(token);

-- Row Level Security (RLS) policies
-- Service role key (used by backend) automatically bypasses RLS
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sessions ENABLE ROW LEVEL SECURITY;

-- Allow read access to public if needed, or service role full access
CREATE POLICY IF NOT EXISTS "Allow service role full access on users" ON public.users
    FOR ALL USING (true);

CREATE POLICY IF NOT EXISTS "Allow service role full access on user_jobs" ON public.user_jobs
    FOR ALL USING (true);

CREATE POLICY IF NOT EXISTS "Allow service role full access on sessions" ON public.sessions
    FOR ALL USING (true);
