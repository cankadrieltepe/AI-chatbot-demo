import os
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from shared_models import SafetyDeps, SafetyResult
from pydantic_ai.providers.groq import GroqProvider

def build_model() -> GroqModel:
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise RuntimeError("GROQ_API_KEY is not set.")

    return GroqModel(
        "llama-3.3-70b-versatile",
        provider=GroqProvider(api_key=key)
    )

safety_agent = Agent(
    model=build_model(),
    deps_type=SafetyDeps,
    output_type=SafetyResult,
    system_prompt=(
        "You are the Safety/QA Agent for appliance troubleshooting.\n"
        "Goal: ensure responses are safe and avoid dangerous advice.\n\n"
        "Decide:\n"
        "- allowed_to_provide_steps: if false, only ask questions + recommend professional service.\n"
        "- must_include_safety_warning: if danger is possible.\n"
        "- escalation_recommended: if urgent or high risk.\n\n"
        "Guidelines:\n"
        "- If complaint includes smoke/burning smell/sparks => must include safety warning, urgency likely 5.\n"
        "- If leak near power => safety warning.\n"
        "- If user mentions breaker trips => escalation recommended.\n"
        "- If uncertain => ask required_questions.\n\n"
        "Output must be in English.\n"
        "Keep safety_warning_text short and direct.\n"
    ),

)
