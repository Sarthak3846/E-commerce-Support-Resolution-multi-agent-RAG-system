import streamlit as st
import json

def render_header():
    st.title("E-commerce Support Resolution Agent")
    st.markdown("Multi-agent RAG system for resolving customer support tickets based on policy documents.")
    st.divider()

def render_input_panel():
    st.subheader("Ticket Input")
    ticket_text = st.text_area("Customer Ticket", height=150, placeholder="Enter the customer's message here...")
    
    st.subheader("Order Context")
    col1, col2 = st.columns(2)
    
    with col1:
        order_date = st.date_input("Order Date")
        delivery_date = st.date_input("Delivery Date", value=None)
        item_category = st.selectbox(
            "Item Category", 
            ["apparel", "electronics", "perishable", "hygiene", "final_sale", "other"]
        )
        fulfillment_type = st.selectbox(
            "Fulfillment Type", 
            ["first-party", "marketplace seller"]
        )
        
    with col2:
        shipping_region = st.text_input("Shipping Region", value="US-CA")
        order_status = st.selectbox(
            "Order Status", 
            ["placed", "shipped", "delivered", "returned", "cancelled"]
        )
        payment_method = st.selectbox(
            "Payment Method", 
            ["credit_card", "paypal", "store_credit", "gift_card"]
        )

    if st.button("Resolve Ticket", type="primary", use_container_width=True):
        if not ticket_text.strip():
            st.error("Please enter the ticket text.")
            return None, None
            
        order_context = {
            "order_date": str(order_date),
            "delivery_date": str(delivery_date) if delivery_date else None,
            "item_category": item_category,
            "fulfillment_type": fulfillment_type,
            "shipping_region": shipping_region,
            "order_status": order_status,
            "payment_method": payment_method
        }
        return ticket_text, order_context
        
    return None, None

def render_output_panel(result):
    st.divider()
    st.subheader("Agent Resolution Output")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Classification & Decision")
        st.write(f"**Issue Type:** {result.get('classification', 'N/A')}")
        st.write(f"**Confidence:** {result.get('confidence', 'N/A')}")
        
        decision = result.get('decision', 'N/A')
        decision_color = "green" if decision.lower() == "approve" else "red" if decision.lower() in ["deny", "needs escalation"] else "orange"
        st.markdown(f"**Decision:** :{decision_color}[{decision.upper()}]")
        
        st.markdown("### ❓ Clarifying Questions")
        questions = result.get('clarifying_questions', [])
        if questions:
            for q in questions:
                st.markdown(f"- {q}")
        else:
            st.write("None required.")
            
        st.markdown("### 📚 Citations")
        citations = result.get('citations', [])
        if citations:
            for cite in citations:
                st.markdown(f"- {cite}")
        else:
            st.error("No citations provided. Policy violation.")

    with col2:
        st.markdown("### 🧠 Rationale")
        st.info(result.get('rationale', 'N/A'))
        
        st.markdown("### 📝 Customer Response Draft")
        st.success(result.get('customer_response_draft', 'N/A'))
        
        st.markdown("### 🔄 Next Steps / Internal Notes")
        st.warning(result.get('next_steps', 'N/A'))

def render_logs_panel(logs):
    with st.expander("View Agent Execution Logs"):
        for log in logs:
            st.text(log)