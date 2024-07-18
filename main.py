from modules.streamlit_interface import streamlit_interface
from modules.streamlit_objects import launch_streamlit

streamlit_interface()


# LAUNCH STREAMLIT DIRECTLY
import os

# Get file path
file_path = os.path.abspath(__file__)
# Run streamlit
launch_streamlit(file_path)
