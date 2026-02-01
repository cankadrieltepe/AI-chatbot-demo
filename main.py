import asyncio
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(__file__).with_name(".env"))

from router_agent import router_agent, RouterDeps
from safety_agent import safety_agent
from shared_models import SafetyDeps, ExpertDeps

from experts import (
    washing_machine_expert,
    refrigerator_expert,
    dishwasher_expert,
    microwave_expert,
    vacuum_expert,
    aircon_expert,
    generic_expert
)



st.set_page_config(page_title="Appliance Complaint Dispatch", layout="centered")
st.title("Appliance Complaint Dispatch (Multi-Agent)")
st.caption("Router → Safety QA → Specialized Expert Agent (English-only)")

if "history" not in st.session_state:
    st.session_state["history"] = []

user_text = st.text_area(
    "Describe the customer's complaint:",
    height=140,
    placeholder="Example: My dishwasher smells bad and leaves residue on glasses."
)

def pick_expert(machine_type: str):
    return {
        "washing_machine": washing_machine_expert,
        "refrigerator": refrigerator_expert,
        "dishwasher": dishwasher_expert,
        "microwave": microwave_expert,
        "vacuum": vacuum_expert,
        "air_conditioner": aircon_expert
    }.get(machine_type, generic_expert)

async def run_system(text: str):
    # 1) Router
    route = await router_agent.run(text, deps=RouterDeps())

    # 2) Safety
    safety = await safety_agent.run(
        "Evaluate safety and decide if we can provide troubleshooting steps.",
        deps=SafetyDeps(
            user_text=text,
            machine_type=route.output.machine_type,
            complaint_types=route.output.complaint_types,
            urgency=route.output.urgency
        )
    )

    # 3) Dispatch to expert
    expert_agent = pick_expert(route.output.machine_type)

    # Merge router questions + safety required questions (deduplicate)
    questions = []
    for q in (route.output.clarifying_questions or []):
        if q not in questions:
            questions.append(q)
    for q in (safety.output.required_questions or []):
        if q not in questions:
            questions.append(q)

    expert_deps = ExpertDeps(
        user_text=text,
        machine_type=route.output.machine_type,
        complaint_types=route.output.complaint_types,
        urgency=route.output.urgency,
        required_questions=questions,
        must_include_safety_warning=safety.output.must_include_safety_warning,
        safety_warning_text=safety.output.safety_warning_text
    )

    # IMPORTANT: pass safety decisions as part of the prompt text too (so expert uses them)
    expert_prompt = (
        "Generate the final customer-support response.\n"
        f"Safety allowed_to_provide_steps={safety.output.allowed_to_provide_steps}\n"
        f"Escalation recommended={safety.output.escalation_recommended}\n"
        "Use deps for machine type, complaint types, and safety warning.\n"
    )

    expert_result = await expert_agent.run(expert_prompt, deps=expert_deps)

    return route.output, safety.output, expert_result.output, safety.output.allowed_to_provide_steps

if st.button("Submit"):
    if not user_text.strip():
        st.warning("Please type a complaint first.")
    else:
        try:
            route, safety, expert, allowed = asyncio.run(run_system(user_text))

            st.subheader("✅ Final Response")
            st.write(expert.final_reply)

            if expert.checklist:
                st.markdown("**Checklist:**")
                for item in expert.checklist:
                    st.markdown(f"- {item}")

            if expert.questions_to_ask:
                st.markdown("**Questions to ask the customer:**")
                for q in expert.questions_to_ask:
                    st.markdown(f"- {q}")

            with st.expander("Debug (Agent Outputs)"):
                st.json({
                    "router": route.model_dump(),
                    "safety": safety.model_dump(),
                    "expert": expert.model_dump()
                })

            st.session_state["history"].append({
                "user": user_text,
                "assistant": expert.final_reply,
                "machine": route.machine_type
            })

        except Exception as e:
            st.error(f"Error: {e}")

if st.session_state["history"]:
    st.subheader("Recent Conversations")
    for item in reversed(st.session_state["history"][-8:]):
        st.markdown(f"**Customer:** {item['user']}")
        st.markdown(f"**Agent ({item['machine']}):** {item['assistant']}")
        st.divider()