import sys
import os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.components import render_header, render_input_panel, render_output_panel, render_logs_panel
from agents.orchestrator import run_ticket_resolution

def initialize_state():
    if "current_result" not in st.session_state:
        st.session_state.current_result = None
    if "agent_logs" not in st.session_state:
        st.session_state.agent_logs = []

def main():
    st.set_page_config(
        page_title="Support Resolution Agent",
        page_icon="🎧",
        layout="wide"
    )
    
    initialize_state()
    render_header()
    
    ticket_text, order_context = render_input_panel()
    
    if ticket_text and order_context:
        with st.spinner("Multi-Agent Team is processing the ticket..."):
            try:
                result, logs = run_ticket_resolution(ticket_text, order_context)
                
                st.session_state.current_result = result
                st.session_state.agent_logs = logs
            except Exception as e:
                st.error(f"System Error: {str(e)}")
                st.session_state.current_result = None
                
    if st.session_state.current_result:
        render_output_panel(st.session_state.current_result)
        
    if st.session_state.agent_logs:
        render_logs_panel(st.session_state.agent_logs)

if __name__ == "__main__":
    main()