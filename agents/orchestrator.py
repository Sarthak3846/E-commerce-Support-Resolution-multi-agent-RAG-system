from agents.triage_agent import TriageAgent
from agents.retriever_agent import RetrieverAgent
from agents.resolver_agent import ResolverAgent
from agents.compliance_agent import ComplianceAgent

# Replace with actual LLM + retriever
def dummy_llm(prompt):
    return {}

class DummyRetriever:
    def get_relevant_documents(self, query):
        return []

triage_agent = TriageAgent(dummy_llm)
retriever_agent = RetrieverAgent(DummyRetriever())
resolver_agent = ResolverAgent(dummy_llm)
compliance_agent = ComplianceAgent(dummy_llm)


def run_ticket_resolution(ticket_text, order_context):
    logs = []

    # 1. TRIAGE
    triage_result = triage_agent.run(ticket_text, order_context)
    logs.append(f"Triage Output: {triage_result}")

    clarifying_questions = triage_result.get("clarifying_questions", [])

    # If missing critical info → stop early
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

    # 2. RETRIEVE
    retrieved_docs = retriever_agent.run(ticket_text)
    logs.append(f"Retrieved Docs: {retrieved_docs}")

    # Hard constraint: must have evidence
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

    # 4. COMPLIANCE CHECK
    compliance = compliance_agent.run(resolution)
    logs.append(f"Compliance Output: {compliance}")

    final_output = resolution

    if not compliance.get("is_valid", True):
        final_output = compliance.get("corrected_output", resolution)

    # FINAL FORMAT (match Streamlit UI)
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