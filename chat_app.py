import streamlit as st
import requests
import uuid

logo = "https://img.freepik.com/free-vector/chatbot-chat-message-vectorart_78370-4104.jpg"

# Display the logo in the sidebar
st.sidebar.image(logo, width=227)

page = st.title("Real-time Search-powered Chatbot")

# Khởi tạo session_id
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Khởi tạo chat history trong session state nếu chưa có
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Xử lý input từ người dùng
if prompt := st.chat_input("Please type your question here..."):
    # Hiển thị câu hỏi của người dùng
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Thêm câu hỏi vào lịch sử
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Gọi API
    try:
        response = requests.post(
            "http://localhost:5001/api/v1/chat",
            json={
                "session_id": st.session_state.session_id,
                "query": prompt
            }
        )
        
        if response.status_code == 200:
            assistant_response = response.json()
            
            # Hiển thị câu trả lời
            with st.chat_message("assistant"):
                st.markdown(assistant_response["content"])
            
            # Thêm câu trả lời vào lịch sử
            st.session_state.messages.append({
                "role": "assistant",
                "content": assistant_response["content"]
            })
        else:
            st.error(f"Cannot connect to the server. Status code: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")

# Thêm nút để xóa lịch sử chat
if st.button("Delete chat history"):
    st.session_state.messages = []
    st.rerun() 