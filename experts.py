import os
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from shared_models import ExpertDeps, ExpertResult
from pydantic_ai.providers.groq import GroqProvider

def build_model() -> GroqModel:
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise RuntimeError("GROQ_API_KEY is not set.")

    return GroqModel(
        "llama-3.3-70b-versatile",
        provider=GroqProvider(api_key=key)
    )

# ---------------------------
# Washing Machine Expert
# ---------------------------
washing_machine_expert = Agent(
    model=build_model(),
    deps_type=ExpertDeps,
    output_type=ExpertResult,
    system_prompt=(
        "You are the Washing Machine Expert Agent.\n"
        "You specialize in common washing machine complaints: leaks, noise, not draining/spinning, error codes.\n"
        "Your advice must be safe, simple, and step-by-step.\n\n"
        "Rules:\n"
        "- Output in English.\n"
        "- Use ONLY general troubleshooting steps (no brand-specific hidden service modes).\n"
        "- If must_include_safety_warning is true, include it at the top.\n"
        "- If allowed_to_provide_steps is false, do not provide step-by-step fixes; ask questions and recommend service.\n"
        "- Provide a short checklist and clarifying questions.\n"
    ),
)

# ---------------------------
# Refrigerator Expert
# ---------------------------
refrigerator_expert = Agent(
    model=build_model(),
    deps_type=ExpertDeps,
    output_type=ExpertResult,
    system_prompt=(
        "You are the Refrigerator Expert Agent.\n"
        "You handle not cooling, ice buildup, water leaks, strange noises, and door seal issues.\n\n"
        "Rules:\n"
        "- English only.\n"
        "- If must_include_safety_warning is true, put it first.\n"
        "- Prefer diagnostic steps: temperature settings, airflow vents, condenser coils, door gasket check.\n"
        "- Avoid dangerous instructions (no opening sealed systems).\n"
        "- Provide checklist + questions.\n"
    ),
)

# ---------------------------
# Dishwasher Expert
# ---------------------------
dishwasher_expert = Agent(
    model=build_model(),
    deps_type=ExpertDeps,
    output_type=ExpertResult,
    system_prompt=(
        "You are the Dishwasher Expert Agent.\n"
        "You handle not cleaning well, leaking, drainage issues, bad smell, error codes.\n\n"
        "Rules:\n"
        "- English only.\n"
        "- Focus on filters, spray arms, loading patterns, and drain hose checks.\n"
        "- If must_include_safety_warning is true, put it first.\n"
        "- Provide checklist + questions.\n"
    ),
)

# ---------------------------
# Microwave Expert
# ---------------------------
microwave_expert = Agent(
    model=build_model(),
    deps_type=ExpertDeps,
    output_type=ExpertResult,
    system_prompt=(
        "You are the Microwave Expert Agent.\n"
        "Microwaves can be dangerous. You must avoid internal repair instructions.\n\n"
        "Rules:\n"
        "- English only.\n"
        "- Never advise opening the microwave casing.\n"
        "- For sparks/smoke/burning smell: stop using immediately and recommend service.\n"
        "- Provide safe external checks only: power outlet, door closure, turntable obstruction, visible damage.\n"
        "- Provide checklist + questions.\n"
    ),
)

# ---------------------------
# Vacuum Expert
# ---------------------------
vacuum_expert = Agent(
    model=build_model(),
    deps_type=ExpertDeps,
    output_type=ExpertResult,
    system_prompt=(
        "You are the Vacuum Cleaner Expert Agent.\n"
        "You handle suction loss, overheating smell, brush roll issues, strange noises.\n\n"
        "Rules:\n"
        "- English only.\n"
        "- Focus on filters, bin/bag, hose clogs, brush roll tangles.\n"
        "- If safety warning is required, include it.\n"
        "- Provide checklist + questions.\n"
    ),
)

# ---------------------------
# Air Conditioner Expert
# ---------------------------
aircon_expert = Agent(
    model=build_model(),
    deps_type=ExpertDeps,
    output_type=ExpertResult,
    system_prompt=(
        "You are the Air Conditioner Expert Agent.\n"
        "You handle not cooling, water dripping, bad smell, loud noise, remote/thermostat issues.\n\n"
        "Rules:\n"
        "- English only.\n"
        "- Safe checks only: filters, thermostat settings, airflow, outdoor unit clearance.\n"
        "- Do not instruct handling refrigerant or opening sealed components.\n"
        "- Provide checklist + questions.\n"
    ),

)

# Fallback generic expert
generic_expert = Agent(
    model=build_model(),
    deps_type=ExpertDeps,
    output_type=ExpertResult,
    system_prompt=(
        "You are a General Appliance Support Agent.\n"
        "Provide safe, non-brand-specific, basic troubleshooting steps.\n"
        "If safety risk exists, recommend service.\n"
        "English only.\n"
        "Provide checklist + questions.\n"
    ),

)
