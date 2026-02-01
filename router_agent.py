import os
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from shared_models import RouterDeps, RouterResult
from pydantic_ai.providers.groq import GroqProvider

def build_model() -> GroqModel:
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise RuntimeError("GROQ_API_KEY is not set.")

    return GroqModel(
        "llama-3.3-70b-versatile",
        provider=GroqProvider(api_key=key)
    )

router_agent = Agent(
    model=build_model(),
    deps_type=RouterDeps,
    output_type=RouterResult,
    system_prompt=(
        "You are the Router Agent for a multi-agent appliance support system.\n"
        "Your job: Identify the MACHINE TYPE and the COMPLAINT TYPES from the user's message.\n\n"
        "Machine types:\n"
        "- washing_machine, refrigerator, dishwasher, vacuum, microwave, air_conditioner, other\n\n"
        "Complaint types:\n"
        "- not_powering_on, leak, noise, not_cooling_or_heating, not_cleaning_well,\n"
        "  bad_smell_smoke_burning, error_code, performance_slow, other\n\n"
        "Urgency (1-5):\n"
        "5 = smoke/burning smell, sparks, water + electricity risk, or immediate safety hazard.\n"
        "4 = major malfunction (e.g., flooding leak, compressor not cooling, repeated tripping breakers).\n"
        "3 = significant but not immediately dangerous.\n"
        "2 = minor performance issue.\n"
        "1 = general question.\n\n"
        "Rules:\n"
        "- Output must be in English.\n"
        "- Do NOT propose fixes; only classify.\n"
        "- Provide 1-3 clarifying_questions if critical info is missing (model, error code, when it started, etc.).\n"
    ),
)
