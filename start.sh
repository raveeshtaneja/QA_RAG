#!/bin/bash
# Start Flask API in the background
python3 app/main.py &

# Start Streamlit
streamlit run app/streamlit_app.py --server.port=8501 --server.address=0.0.0.0 