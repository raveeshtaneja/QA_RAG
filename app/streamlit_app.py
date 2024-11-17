import streamlit as st
import requests

st.title("RAG Q&A System")

question = st.text_input("Enter your question:")
if st.button("Get Answer"):
    response = requests.post(
        "http://localhost:5001/api/query",  # Updated port to 5000 for Flask
        json={"question": question}
    )
    if response.status_code == 200:
        data = response.json()
        st.write("Answer:", data["answer"])
        st.write("Context used:")
        for ctx in data["context"]:
            st.write("- " + ctx)
    else:
        st.error(f"Error: {response.json().get('error', 'Unknown error occurred')}") 