import streamlit as st
from openai import OpenAI
from pypdf import PdfReader

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Assistant")
st.write("Choose an assistant type from the sidebar, then ask a question.")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Assistant Settings")

    category = st.selectbox(
        "Choose an assistant type:",
        [
            "General AI Assistant",
            "Cybersecurity Assistant",
            "Malware and Attacks Tutor",
            "TCP/IP and Networking Tutor",
            "Ethical Hacking Tutor",
            "Cisco and Packet Tracer Helper",
            "Programming Assistant",
            "Resume and Career Coach",
            "Fitness and Nutrition Coach",
            "Study Assistant",
            "IT Help Desk Assistant"
        ]
    )

    uploaded_file = st.file_uploader(
        "Upload a PDF or text file",
        type=["pdf", "txt"]
    )

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

system_prompts = {
    "General AI Assistant":
        "You are a helpful AI assistant that can answer questions about almost any topic including technology, fitness, careers, cybersecurity, school, writing, and general life advice.",

    "Cybersecurity Assistant":
        "You are a helpful cybersecurity assistant. Explain concepts clearly for a graduate cybersecurity student.",

    "Malware and Attacks Tutor":
        "You are a malware and cyberattack tutor. Explain viruses, worms, Trojans, spyware, ransomware, phishing, DoS, DDoS, and attack defenses clearly.",

    "TCP/IP and Networking Tutor":
        "You are a TCP/IP and networking tutor. Explain IP addressing, ports, protocols, subnetting, routing, VLANs, switches, routers, and packet flow clearly.",

    "Ethical Hacking Tutor":
        "You are an ethical hacking tutor focused only on legal, defensive, and educational cybersecurity concepts.",

    "Cisco and Packet Tracer Helper":
        "You are a Cisco networking and Packet Tracer assistant helping users configure routers, switches, VLANs, DHCP, ACLs, NAT, and troubleshoot networking issues.",

    "Programming Assistant":
        "You are a programming assistant that helps with Python, Java, scripting, debugging, and coding concepts.",

    "Resume and Career Coach":
        "You help improve resumes, LinkedIn profiles, interview preparation, job applications, and IT/cybersecurity career growth.",

    "Fitness and Nutrition Coach":
        "You help with fitness, workouts, nutrition, meal planning, strength training, recovery, and healthy habits.",

    "Study Assistant":
        "You help explain school concepts clearly and assist with studying, quizzes, projects, and technical coursework.",

    "IT Help Desk Assistant":
        "You are an IT support assistant helping troubleshoot Windows, printers, networking, Office 365, Citrix, Outlook, and general help desk issues."
}

file_context = ""

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                file_context += text + "\n"
    else:
        file_context = uploaded_file.read().decode("utf-8", errors="ignore")

    st.sidebar.success("File uploaded successfully.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Ask your question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    full_system_prompt = system_prompts[category]

    if file_context:
        full_system_prompt += (
            "\n\nThe user uploaded the following document content. "
            "Use it as reference when answering:\n"
            + file_context[:12000]
        )

    messages_for_api = [{"role": "system", "content": full_system_prompt}]
    messages_for_api += st.session_state.messages

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages_for_api
    )

    bot_response = response.choices[0].message.content

    st.session_state.messages.append(
        {"role": "assistant", "content": bot_response}
    )

    with st.chat_message("assistant"):
        st.write(bot_response)