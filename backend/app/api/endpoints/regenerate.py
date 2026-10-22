import uuid
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from app.worker.queue import jobs, worker

router = APIRouter()

class RegenerateStepRequest(BaseModel):
    job_id: str
    step_number: int
    focus_angle: str = "Explain the intuition and algebraic steps more slowly with an alternative diagram."

@router.post("/regenerate-step")
async def regenerate_single_step(
    payload: RegenerateStepRequest,
    background_tasks: BackgroundTasks,
):
    if payload.job_id not in jobs:
        raise HTTPException(status_code=404, detail=f"Job {payload.job_id} not found.")

    job = jobs[payload.job_id]
    if not job.lesson_plan:
        raise HTTPException(status_code=400, detail="Cannot regenerate step: original lesson plan not ready.")

    background_tasks.add_task(
        worker.run_step_regeneration_job,
        job_id=payload.job_id,
        step_number=payload.step_number,
        focus_angle=payload.focus_angle,
    )

    return {
        "job_id": payload.job_id,
        "step_number": payload.step_number,
        "status": "regenerating",
        "message": f"Step {payload.step_number} scheduled for re-derivation.",
    }
