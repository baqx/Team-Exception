import uuid
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from typing import Optional
from app.core.models import JobStatus
from app.worker.queue import jobs, worker

router = APIRouter()

@router.post("/generate")
async def start_generation(
    background_tasks: BackgroundTasks,
    query: str = Form(..., description="Problem statement or student question"),
    subject: str = Form("general", description="Academic discipline"),
    length: str = Form("standard", description="Video length: short (~3m), standard (~5m), detailed (~8m)"),
    voice: Optional[str] = Form("edge:en-US-ChristopherNeural", description="Voice ID or tutor accent"),
    language: Optional[str] = Form("en", description="Instructional dialect or language: en, pidgin, yo, ha, ig"),
    file: Optional[UploadFile] = File(None, description="Optional photo or PDF of assignment, lecture notes, textbook, or diagram (PNG, JPG, WebP, PDF)"),
    user_id: Optional[str] = Form(None, description="Optional authenticated user ID for credit deduction & history tracking"),
):
    from app.services import user_service

    clean_user_id = (user_id or "").strip() or None

    # Check and deduct credits if user is provided
    if clean_user_id:
        user = user_service.get_user_by_id(clean_user_id)
        if user:
            if user["credits"] < 5:
                raise HTTPException(
                    status_code=402, 
                    detail="Insufficient credits. You need 5 chalkboard credits to generate a lesson. Please request a grant top-up from your dashboard."
                )
            user_service.check_and_deduct_credits(clean_user_id, cost=5)

    job_id = str(uuid.uuid4())[:12]
    clean_subject = (subject or "").strip() or "general"
    clean_voice = (voice or "edge:en-US-ChristopherNeural").strip()
    clean_language = (language or "en").strip().lower()

    # Map length string to target seconds
    duration_map = {
        "short": 180,
        "standard": 300,
        "detailed": 480,
    }
    target_duration_sec = duration_map.get(length.lower(), 300)

    # Read image bytes if uploaded
    image_bytes = None
    image_mime = None
    if file:
        image_bytes = await file.read()
        image_mime = file.content_type or "image/png"

    # Record job in persistent database
    if clean_user_id:
        user_service.record_job_start(job_id, clean_user_id, query, clean_subject, length)

    # Initialize Job
    jobs[job_id] = JobStatus(
        job_id=job_id,
        status="pending",
        progress_percent=0,
        current_step_text="Job queued...",
    )

    # Launch background worker
    background_tasks.add_task(
        worker.run_generation_job,
        job_id=job_id,
        query=query,
        subject=clean_subject,
        target_duration_sec=target_duration_sec,
        voice=clean_voice,
        language=clean_language,
        image_bytes=image_bytes,
        image_mime=image_mime,
        user_id=clean_user_id,
    )

    remaining_credits = user_service.get_user_by_id(clean_user_id)["credits"] if clean_user_id else None

    return {
        "job_id": job_id,
        "status": "pending",
        "message": "Video generation job started in background.",
        "remaining_credits": remaining_credits,
    }

@router.get("/status/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found.")
    return jobs[job_id]
