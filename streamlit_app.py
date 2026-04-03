import streamlit as st
from collections import deque
from datetime import datetime

# --- MODULE 3: Late Entry Tracker (Linked List Class) ---
class Node:
    def __init__(self, student_id, name, entry_time):
        self.student_id = student_id
        self.name = name
        self.entry_time = entry_time
        self.next = None

# --- INITIALIZE DATA STRUCTURES (Using Session State) ---
# This ensures your Array, Queue, and Stack don't reset on every click
if 'db' not in st.session_state:
    st.session_state.db = [
        {"id": 101, "name": "Arjun", "dept": "CSE"},
        {"id": 102, "name": "Priya", "dept": "CSE"},
        {"id": 103, "name": "Rahul", "dept": "CSE"}
    ]
if 'queue' not in st.session_state:
    st.session_state.queue = deque()
if 'report' not in st.session_state:
    st.session_state.report = []
if 'stack' not in st.session_state:
    st.session_state.stack = []
if 'late_head' not in st.session_state:
    st.session_state.late_head = None

# --- APP LAYOUT ---
st.set_page_config(page_title="Student Tracker Pro", layout="wide")
st.title("🎓 Student Attendance & Late Tracker")

# Sidebar: Class Timing (Module 3 Setting)
st.sidebar.header("⚙️ Settings")
set_time = st.sidebar.time_input("Set Class Start Time", datetime.strptime("09:00", "%H:%M").time())

# --- MODULE 1: Student Database (Array) ---
st.header("1. Student Database Management")
with st.expander("➕ Register New Student"):
    c1, c2, c3 = st.columns(3)
    new_id = c1.number_input("Enter ID", step=1, value=104)
    new_name = c2.text_input("Enter Name")
    new_dept = c3.text_input("Enter Department")
    if st.button("Add to Database"):
        if new_name:
            st.session_state.db.append({"id": new_id, "name": new_name, "dept": new_dept})
            st.success(f"Added {new_name} to the database!")
            st.rerun()
        else:
            st.error("Please enter a name.")

# Display Database with Delete and Check-in options
st.subheader("Current Students (Array)")
for i, s in enumerate(st.session_state.db):
    col_name, col_check, col_del = st.columns([3, 1, 1])
    col_name.write(f"**{s['name']}** (ID: {s['id']} | Dept: {s['dept']})")
    
    # MODULE 2: Enqueue Logic
    if col_check.button("Check-in", key=f"chk_{i}"):
        st.session_state.queue.append(s)
        now = datetime.now().time()
        # MODULE 3: Linked List Late Check
        if now > set_time:
            new_node = Node(s['id'], s['name'], now.strftime("%H:%M"))
            if not st.session_state.late_head:
                st.session_state.late_head = new_node
            else:
                temp = st.session_state.late_head
                while temp.next: temp = temp.next
                temp.next = new_node
        st.toast(f"{s['name']} added to queue!")
    
    # Delete from Array
    if col_del.button("🗑️ Delete", key=f"del_{i}"):
        st.session_state.db.pop(i)
        st.rerun()

st.divider()

# --- MODULE 2 & 4: Queue & Stack ---
col_q, col_tools = st.columns(2)

with col_q:
    st.header("2. Attendance Queue (FIFO)")
    st.write(f"Students waiting in line: **{len(st.session_state.queue)}**")
    if st.button("Confirm Attendance for Next Student", type="primary"):
        if st.session_state.queue:
            student = st.session_state.queue.popleft()
            st.session_state.report.append(student)
            st.session_state.stack.append(student) # Push to Stack
            st.rerun()
        else:
            st.warning("No students in the queue.")

with col_tools:
    st.header("3. System Tools (LIFO)")
    if st.button("⏪ Undo Last Attendance Mark"):
        if st.session_state.stack:
            last = st.session_state.stack.pop() # Pop from Stack
            st.session_state.report = [r for r in st.session_state.report if r['id'] != last['id']]
            st.info(f"Attendance for {last['name']} has been removed.")
            st.rerun()
        else:
            st.error("No actions to undo.")

st.divider()

# --- REPORTS ---
st.header("4. System Reports")
rep_col, late_col = st.columns(2)

with rep_col:
    st.subheader("Attendance Report (Final Array)")
    if st.session_state.report:
        st.table(st.session_state.report)
    else:
        st.write("No attendance marked yet.")

with late_col:
    st.subheader("Late Comers (Linked List)")
    curr = st.session_state.late_head
    if not curr:
        st.write("No late entries recorded.")
    while curr:
        st.error(f"⚠️ **{curr.name}** (ID: {curr.student_id}) arrived late at **{curr.entry_time}**")
        curr = curr.next
