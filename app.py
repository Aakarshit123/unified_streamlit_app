import streamlit as st
import os
import smtplib
import requests
from email.message import EmailMessage
from twilio.rest import Client
import google.generativeai as genai

# ------------------ Streamlit UI Setup ------------------
st.set_page_config(page_title="All-in-One Dashboard", layout="centered")
st.sidebar.title("🧭 Tool Selector")
choice = st.sidebar.selectbox("Choose Functionality", [
    "🤖 AI Chatbot",
    "📸 Camera Capture",
    "🐳 Docker Control",
    "📧 Send Email",
    "📞 Make Call",
    "📘 Facebook Post",
    "📷 Instagram Post",
    "🧾 HTML Interpreter",
    "🌍 Location Finder",
    "📩 Send SMS",
    "🔗 LinkedIn Post"
])

# ------------------ AI Chatbot ------------------
if choice == "🤖 AI Chatbot":
    genai.configure(api_key="YOUR_GEMINI_API_KEY")
    model = genai.GenerativeModel("gemini-2.5-flash")
    def AI(prompt):
        return model.generate_content(prompt).text

    st.title("🎥 AI-Powered Recommender Bot")
    category = st.selectbox("Choose type", ["Anime", "Manga", "Movie", "Web Series"])
    title = st.text_input(f"Enter the name of the {category.lower()}:")
    if st.button("Get Summary and Ratings") and title:
        prompt = (
            f"You are an expert in {category}. Give a summary, studio, "
            f"and rate the {category.lower()} titled '{title}' on story, animation, "
            "characters, soundtrack, and say whether you recommend it or not."
        )
        try:
            st.markdown(AI(prompt))
        except Exception as e:
            st.error(f"Gemini Error: {str(e)}")

# ------------------ Camera Capture ------------------
elif choice == "📸 Camera Capture":
    st.title("📸 Camera Capture")
    st.info("Use a supported browser for camera access.")
    photo = st.camera_input("Take a photo")
    if photo:
        st.image(photo)
        st.success("Photo captured!")

# ------------------ Docker Control ------------------
elif choice == "🐳 Docker Control":
    st.title("🐳 Docker Control")
    action = st.selectbox("Docker Operation", [
        "Launch New Container", "Stop Container", "Remove Container", 
        "Start Container", "List Docker Images"
    ])
    name = st.text_input("Container name")
    image = st.text_input("Image (if applicable)")
    if st.button("Execute"):
        cmd = ""
        if action == "Launch New Container":
            cmd = f"docker run -dit --name {name} {image}"
        elif action == "Stop Container":
            cmd = f"docker stop {name}"
        elif action == "Remove Container":
            cmd = f"docker rm -f {name}"
        elif action == "Start Container":
            cmd = f"docker start {name}"
        if cmd:
            os.system(cmd)
            st.success(f"{action} executed.")
    if action == "List Docker Images" and st.button("List Images"):
        output = os.popen("docker images").read()
        st.text_area("Docker Images", output, height=300)

# ------------------ Email ------------------
elif choice == "📧 Send Email":
    st.title("📧 Email Sender")
    sender = st.text_input("Your Email")
    recipient = st.text_input("Recipient Email")
    subject = st.text_input("Subject")
    body = st.text_area("Message")
    password = st.text_input("App Password", type="password")
    if st.button("Send"):
        msg = EmailMessage()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.set_content(body)
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as s:
                s.starttls()
                s.login(sender, password)
                s.send_message(msg)
                st.success("Email sent!")
        except Exception as e:
            st.error(f"Email Error: {str(e)}")

# ------------------ Twilio Call ------------------
elif choice == "📞 Make Call":
    st.title("📞 Twilio Call")
    sid = st.text_input("Twilio SID")
    token = st.text_input("Auth Token", type="password")
    from_no = st.text_input("Twilio Number (+country code)")
    to_no = st.text_input("To Number (+country code)")
    if st.button("Make Call"):
        try:
            client = Client(sid, token)
            call = client.calls.create(to=to_no, from_=from_no, url="http://demo.twilio.com/docs/voice.xml")
            st.success(f"Call initiated! SID: {call.sid}")
        except Exception as e:
            st.error(f"Call Error: {str(e)}")

# ------------------ Facebook ------------------
elif choice == "📘 Facebook Post":
    st.title("📘 Facebook Page Post")
    page_id = st.text_input("Page ID")
    token = st.text_input("Page Access Token")
    message = st.text_area("Message")
    if st.button("Post"):
        r = requests.post(
            f"https://graph.facebook.com/{page_id}/feed",
            data={"message": message, "access_token": token}
        )
        st.success("Posted!" if r.status_code == 200 else str(r.json()))

# ------------------ Instagram ------------------
elif choice == "📷 Instagram Post":
    st.title("📷 Instagram Post")
    access_token = st.text_input("Access Token")
    account_id = st.text_input("Business Account ID")
    img_url = st.text_input("Image URL")
    caption = st.text_area("Caption")
    if st.button("Post to Instagram"):
        container = requests.post(
            f"https://graph.facebook.com/v18.0/{account_id}/media",
            data={"image_url": img_url, "caption": caption, "access_token": access_token}
        ).json()
        cont_id = container.get("id")
        if cont_id:
            publish = requests.post(
                f"https://graph.facebook.com/v18.0/{account_id}/media_publish",
                data={"creation_id": cont_id, "access_token": access_token}
            )
            st.success("Posted!" if publish.status_code == 200 else str(publish.json()))
        else:
            st.error(f"Container Error: {container}")

# ------------------ HTML Interpreter ------------------
elif choice == "🧾 HTML Interpreter":
    st.title("🧾 HTML Interpreter")
    html = st.text_area("Write HTML", placeholder="<h1>Hello</h1>")
    if html:
        st.components.v1.html(html, height=400, scrolling=True)

# ------------------ Location Finder ------------------
elif choice == "🌍 Location Finder":
    st.title("🌍 Address to Coordinates")
    location = st.text_input("Enter address or place")
    if st.button("Get Location") and location:
        try:
            res = requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={location}").json()
            if res:
                st.success(f"📍 Latitude: {res[0]['lat']} | Longitude: {res[0]['lon']}")
            else:
                st.warning("No results found.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# ------------------ Textlocal SMS ------------------
elif choice == "📩 Send SMS":
    st.title("📩 Send SMS via Textlocal")
    api_key = st.text_input("API Key")
    numbers = st.text_input("Recipient Number(s)")
    msg = st.text_area("Message")
    if st.button("Send SMS"):
        data = {'apikey': api_key, 'numbers': numbers, 'message': msg, 'sender': 'TXTLCL'}
        try:
            r = requests.post("https://api.textlocal.in/send/", data=data)
            st.json(r.json())
        except Exception as e:
            st.error(f"SMS Error: {str(e)}")

# ------------------ LinkedIn Post ------------------
elif choice == "🔗 LinkedIn Post":
    st.title("🔗 LinkedIn OAuth")
   # st.markdown("1. Click below to authenticate.\n2. Then visit `/post` on your Flask server.")
    st.markdown("🔗 Run your Flask LinkedIn OAuth on Replit or locally to use this feature.")
     st.link_button("Login via LinkedIn", "http://localhost:8000/")
