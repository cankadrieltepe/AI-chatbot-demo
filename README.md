# Appliance Complaint Dispatch (Multi-Agent)

A small **multi-agent AI system** built with **PydanticAI + Streamlit** that routes customer complaints about household appliances to the correct expert agent and generates safe, structured support responses.

## How it works

**Multi-agent pipeline:**
1. **Router Agent** – Identifies the appliance type and complaint category from user input.
2. **Safety QA Agent** – Checks for potential hazards and decides whether troubleshooting is safe.
3. **Specialized Expert Agent** – Provides appliance-specific guidance (e.g. dishwasher, washing machine, microwave).

All responses are **English-only** and follow safety-aware rules.

## Supported appliances

- Washing machine  
- Refrigerator  
- Dishwasher  
- Microwave  
- Vacuum cleaner  
- Air conditioner  
- Generic fallback agent

## Example input

<img width="607" height="833" alt="image" src="https://github.com/user-attachments/assets/9e90899a-bfa1-485a-952d-7e0a86b9849c" />


## Tech stack

- Python  
- Streamlit  
- PydanticAI  
- Groq LLMs  

