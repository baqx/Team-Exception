from typing import List, Literal, Optional
from pydantic import BaseModel, Field, field_validator

class ChalkAction(BaseModel):
    action_type: Literal[
        "write_latex", 
        "draw_schematic", 
        "circle_term", 
        "strike_through", 
        "box_answer"
    ] = Field(description="The chalkboard action to perform")
    content: str = Field(description="The LaTeX math formula, circuit label, or text content")
    color: Literal["white", "yellow", "cyan", "green", "red"] = "white"
    target_id: Optional[str] = Field(default=None, description="Optional target element identifier")
    timing: Optional[Literal["write_first", "synchronous", "write_last"]] = Field(
        default="synchronous", 
        description="Pedagogical timing: 'write_first' (anchor visual before speech), 'synchronous', or 'write_last' (derived result/summary)"
    )
    cancel_label: Optional[str] = Field(
        default=None, 
        description="Optional simplification label to write above/below canceled terms (e.g. '1', '0', 'x')"
    )

    @field_validator("timing", mode="before")
    @classmethod
    def normalize_timing(cls, v):
        if not v:
            return "synchronous"
        v_str = str(v).lower().strip()
        if "first" in v_str or "before" in v_str or "start" in v_str:
            return "write_first"
        if "last" in v_str or "after" in v_str or "end" in v_str:
            return "write_last"
        return "synchronous"

    @field_validator("action_type", mode="before")
    @classmethod
    def normalize_action_type(cls, v):
        if not v:
            return "write_latex"
        v_str = str(v).lower().strip()
        if "schematic" in v_str or "diagram" in v_str or "circuit" in v_str:
            return "draw_schematic"
        if "circle" in v_str or "highlight" in v_str:
            return "circle_term"
        if "strike" in v_str or "cancel" in v_str:
            return "strike_through"
        if "box" in v_str:
            return "box_answer"
        return "write_latex"

class ScenePlan(BaseModel):
    step_number: int = Field(description="1-indexed sequence order")
    title: str = Field(description="Short human-readable title for the chapter")
    category: Literal["prerequisite", "concept", "solution", "verification"] = Field(
        description="Pedagogical category of the scene"
    )
    spoken_script: str = Field(
        description="The exact conversational words spoken by the tutor, with pauses and emphasis"
    )
    chalk_actions: List[ChalkAction] = Field(
        default_factory=list,
        description="Chronological chalkboard drawing commands matching this scene"
    )
    key_latex_formula: str = Field(
        description="Main LaTeX formula or boxed derivation featured in this scene"
    )

    @field_validator("category", mode="before")
    @classmethod
    def normalize_category(cls, v):
        if not v:
            return "concept"
        v_str = str(v).lower().strip()
        if "prereq" in v_str:
            return "prerequisite"
        if "verif" in v_str or "sum" in v_str or "conclu" in v_str or "check" in v_str:
            return "verification"
        if "concept" in v_str or "dive" in v_str or "theory" in v_str or "intro" in v_str:
            return "concept"
        return "solution"

class LessonPlan(BaseModel):
    problem_title: str = Field(description="Concise description of the problem being solved")
    subject: str = Field(description="Discipline (e.g., Electrical Eng, Calculus, Physics, Chemistry)")
    core_concept: str = Field(description="Identified concept behind the problem")
    prerequisites: List[str] = Field(description="Prerequisites taught first before solving")
    estimated_duration_sec: int = Field(description="Target duration in seconds")
    scenes: List[ScenePlan] = Field(description="List of scenes comprising the full chalkboard lesson")

class JobStatus(BaseModel):
    job_id: str
    status: Literal["pending", "analyzing", "synthesizing_audio", "rendering_video", "stitching", "completed", "failed"]
    progress_percent: int
    current_step_text: str
    video_url: Optional[str] = None
    lesson_plan: Optional[LessonPlan] = None
    error_message: Optional[str] = None
