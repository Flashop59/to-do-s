import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import json

# Load Firebase credentials from Streamlit secrets
firebase_credentials = json.loads(st.secrets["firebase_credentials"])

# Initialize Firebase
cred = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Function to save to-dos to Firestore
def save_to_cloud(todo_list):
    doc_ref = db.collection("todos").document(datetime.now().strftime("%Y-%m-%d"))
    doc_ref.set({"tasks": todo_list})

# Function to load to-dos from Firestore
def load_from_cloud():
    doc_ref = db.collection("todos").document(datetime.now().strftime("%Y-%m-%d"))
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get("tasks", [])
    else:
        return []

# Streamlit UI
st.title("To-Do List")

todo_list = load_from_cloud()

new_todo = st.text_input("New To-Do")
if st.button("Add"):
    todo_list.append({"task": new_todo, "completed": False})
    save_to_cloud(todo_list)

for i, todo in enumerate(todo_list):
    todo_list[i]["completed"] = st.checkbox(todo["task"], value=todo["completed"])

if st.button("Save"):
    save_to_cloud(todo_list)

# End of day automatic save (can be triggered manually or scheduled)
if st.button("End of Day Save"):
    save_to_cloud(todo_list)
    st.success("Tasks saved successfully!")
