import streamlit as st
import json
import os
from datetime import datetime
import random

# Set a custom theme using Streamlit config
st.set_page_config(page_title="Digital Diary", layout="wide")

# Define a new dark theme with fully visible text
theme_css = """
    <style>
        body {
            background-color: #121212;
            color: #FFFFFF; /* Ensuring all text is white */
        }
        .stApp {
            background-color: #121212;
        }
        h1, h2, h3, h4, h5, h6, p, label {
            color: #FFFFFF !important; /* All text is now white */
        }
        .stTextInput>div>div>input, .stTextArea>div>textarea {
            background-color: #1E1E1E;
            color: #FFFFFF; /* White text inside inputs */
            border-radius: 6px;
            border: 1px solid #6200EA;
        }
        .stButton>button {
            background-color: #6200EA;
            color: #FFFFFF;
            border-radius: 8px;
            padding: 8px 16px;
        }
        .stButton>button:hover {
            background-color: #7E57C2;
        }
        .stSidebar {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        .stSidebar h3, .stSidebar p, .stSidebar label {
            color: #FFFFFF !important;
        }
        .footer {
            text-align: center;
            font-size: 16px;
            font-weight: bold;
            margin-top: 50px;
            padding: 10px;
            color: #FFFFFF;
        }
    </style>
"""
st.markdown(theme_css, unsafe_allow_html=True)

# File storage for diary entries
DIARY_FILE = "diary_entries.json"
IMAGE_FOLDER = "static/uploads/"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Load existing diary entries
def load_entries():
    if os.path.exists(DIARY_FILE):
        with open(DIARY_FILE, "r") as f:
            return json.load(f)
    return []

# Save diary entries
def save_entries(entries):
    with open(DIARY_FILE, "w") as f:
        json.dump(entries, f, indent=4)

# Load quotes
quotes = [
    "Believe in yourself.",
    "Every day is a new beginning.",
    "Strive for progress, not perfection.",
    "The best way to predict the future is to create it."
]

# Sidebar - Select Mood
mood_colors = {
    "Happy": "#FFD700",
    "Sad": "#4682B4",
    "Excited": "#FFA500",
    "Angry": "#FF4500",
    "Neutral": "#808080"
}

st.sidebar.title("🌟 Digital Diary")
mood = st.sidebar.selectbox("How are you feeling?", list(mood_colors.keys()))
st.sidebar.markdown(f"<h3 style='color: {mood_colors[mood]};'>Current Mood: {mood}</h3>", unsafe_allow_html=True)

# Main Diary Entry
st.markdown("<h1>📖 My Digital Diary</h1>", unsafe_allow_html=True)  # Ensuring title is white
title = st.text_input("Title of Entry", key="title_input")
content = st.text_area("Write your thoughts...")

# Image Upload
uploaded_image = st.file_uploader("Upload an image (optional)", type=["png", "jpg", "jpeg"])
if uploaded_image:
    image_path = os.path.join(IMAGE_FOLDER, uploaded_image.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_image.getbuffer())
    st.image(image_path, caption="Uploaded Image")

# To-Do List for the Entry
if "todo_list" not in st.session_state:
    st.session_state.todo_list = []

st.markdown("<h2>✅ To-Do List</h2>", unsafe_allow_html=True)
new_task = st.text_input("Add a task")
if st.button("Add Task"):
    if new_task:
        st.session_state.todo_list.append(new_task)

for task in st.session_state.todo_list:
    st.write(f"- {task}")

# Quote Selection
if "selected_quote" not in st.session_state:
    st.session_state.selected_quote = random.choice(quotes)

st.markdown("<h2>📜 Motivational Quote</h2>", unsafe_allow_html=True)
st.write(f"💡 *{st.session_state.selected_quote}*")

# Save Entry
if st.button("Save Entry"):
    if title and content:
        entries = load_entries()
        entry_data = {
            "title": title,
            "content": content,
            "date": str(datetime.now().strftime("%Y-%m-%d %H:%M")),
            "mood": mood,
            "image": uploaded_image.name if uploaded_image else None,
            "todo_list": st.session_state.todo_list
        }
        entries.append(entry_data)
        save_entries(entries)
        st.success("Entry saved successfully!")
    else:
        st.error("Please enter a title and content.")

# Search & Filter
st.sidebar.subheader("🔍 Search Entries")
search_query = st.sidebar.text_input("Search by title or tag")
filtered_entries = [entry for entry in load_entries() if search_query.lower() in entry["title"].lower()]

# Display Past Entries
st.sidebar.subheader("📚 Past Entries")
selected_entry = st.sidebar.selectbox("Choose an entry", [entry["title"] for entry in filtered_entries] if filtered_entries else [])

if selected_entry:
    selected_entry_data = next(entry for entry in load_entries() if entry["title"] == selected_entry)
    st.markdown(f"<h2>📌 {selected_entry_data['title']}</h2>", unsafe_allow_html=True)
    st.write(selected_entry_data["content"])
    st.write(f"🕒 {selected_entry_data['date']} | 😃 {selected_entry_data['mood']}")

    if selected_entry_data.get("image"):
        st.image(os.path.join(IMAGE_FOLDER, selected_entry_data["image"]), caption="Saved Image")

    if selected_entry_data.get("todo_list"):
        st.markdown("<h2>✅ Saved To-Do List</h2>", unsafe_allow_html=True)
        for task in selected_entry_data["todo_list"]:
            st.write(f"- {task}")

# Footer with your name
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<div class="footer">💖 Developed by Ayesha Farooq 💖</div>', unsafe_allow_html=True)
