import streamlit as st
from query import query_law  # Uses LangChain internally

st.set_page_config(page_title="Pakistan Law Assistant", layout="wide")
st.title("⚖️ Lexi")
st.markdown("Ask a legal question and get simplified answers from Pakistan Penal Code.")

# User input
query = st.text_input("🔍 Enter your legal question:")

if st.button("Get Answer") and query.strip():
    with st.spinner("Searching law database and generating answer..."):

        try:
            response = query_law(query)

            st.success("✅ Answer:")
            st.write(response["result"])

            # Show scrollable source law sections
            if response["source_documents"]:
                with st.expander("📄 View Source Law Sections"):
                    for doc in response["source_documents"]:
                        section = doc.metadata.get("section", "Unknown")
                        st.markdown(f"**Section {section}**")
                        st.text(doc.page_content)

        except Exception as e:
            st.error(f"❌ Error: {e}")
