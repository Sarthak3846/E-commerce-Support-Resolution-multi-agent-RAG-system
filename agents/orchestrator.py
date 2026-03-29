from agents.triage_agent import TriageAgent
from agents.retriever_agent import RetrieverAgent
from agents.resolver_agent import ResolverAgent
from agents.compliance_agent import ComplianceAgent

from rag.retriever import Retriever
from utils.llm import gemini_llm


triage_agent = TriageAgent(gemini_llm)
retriever_agent = RetrieverAgent(Retriever())
resolver_agent = ResolverAgent(gemini_llm)
compliance_agent = ComplianceAgent(gemini_llm)


def run_ticket_resolution(ticket_text, order_context):
    logs = []

    # 1. TRIAGE
    triage_result = triage_agent.run(ticket_text, order_context)
    logs.append(f"Triage Output: {triage_result}")

    if not isinstance(triage_result, dict):
        return {"error": "Triage failed"}, logs

    clarifying_questions = triage_result.get("clarifying_questions", [])

    if clarifying_questions:
        return {
            "classification": triage_result.get("issue_type"),
            "confidence": triage_result.get("confidence"),
            "clarifying_questions": clarifying_questions,
            "decision": "needs more info",
            "rationale": "Insufficient data to proceed",
            "citations": [],
            "customer_response_draft": "Please provide additional details.",
            "next_steps": "Await customer clarification"
        }, logs

    # 2. RETRIEVE (IMPORTANT FIX: include context)
    query = f"{ticket_text}\n{order_context}"
    retrieved_docs = retriever_agent.run(query)
    logs.append(f"Retrieved Docs: {retrieved_docs}")

    if not retrieved_docs:
        return {
            "classification": triage_result.get("issue_type"),
            "confidence": triage_result.get("confidence"),
            "clarifying_questions": [],
            "decision": "needs escalation",
            "rationale": "No policy evidence found",
            "citations": [],
            "customer_response_draft": "We are escalating your request for further review.",
            "next_steps": "Escalate to human support"
        }, logs

    # 3. RESOLUTION
    resolution = resolver_agent.run(ticket_text, order_context, retrieved_docs)
    logs.append(f"Resolution Output: {resolution}")

    if not isinstance(resolution, dict):
        return {"error": "Resolution failed"}, logs

    # 4. COMPLIANCE
    compliance = compliance_agent.run(resolution)
    logs.append(f"Compliance Output: {compliance}")

    final_output = resolution

    if not compliance.get("is_valid", True):
        final_output = compliance.get("corrected_output", resolution)

    # HARD RULE: enforce citations
    if not final_output.get("citations"):
        final_output["decision"] = "needs escalation"
        final_output["rationale"] = "Missing citations"
        final_output["customer_response_draft"] = "We are escalating your request for further review."
        final_output["next_steps"] = "Escalate to human support"

    structured_output = {
        "classification": triage_result.get("issue_type"),
        "confidence": triage_result.get("confidence"),
        "clarifying_questions": clarifying_questions,
        "decision": final_output.get("decision"),
        "rationale": final_output.get("rationale"),
        "citations": final_output.get("citations"),
        "customer_response_draft": final_output.get("customer_response_draft"),
        "next_steps": final_output.get("next_steps")
    }

    return structured_output, logs