import streamlit as st
import os
import smtplib
import requests
from email.message import EmailMessage
from twilio.rest import Client
import google.generativeai as genai

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
    "📩 Send SMS"
])

# ------------------ AI Chatbot ------------------
if choice == "🤖 AI Chatbot":
    genai.configure(api_key="st.secrets")  # Replace this or use st.secrets
    model = genai.GenerativeModel("gemini-2.5-flash")

    def AI(prompt):
        return model.generate_content(prompt).text

    st.title("🎥 AI-Powered Recommender Bot")
    category = st.selectbox("Choose type", ["Anime", "Manga", "Movie", "Web Series"])
    title = st.text_input(f"Enter the name of the {category.lower()}:")
    if st.button("Get Summary and Ratings") and title:
        prompt = (
            f"You are an expert in {category}. Give a summary, studio (if any), "
            f"and rate the {category.lower()} titled '{title}' on story, animation, characters, soundtrack, "
            "and say whether you recommend it or not."
        )
        try:
            st.markdown(AI(prompt))
        except Exception as e:
            st.error(f"Gemini API Error: {str(e)}")

# ------------------ Camera Capture ------------------
elif choice == "📸 Camera Capture":
    st.title("📸 Camera Capture")
    st.info("Works in supported browsers only.")
    photo = st.camera_input("Take a picture")
    if photo:
        st.image(photo)
        st.success("Photo captured successfully!")

# ------------------ Docker Control ------------------
elif choice == "🐳 Docker Control":
    st.title("🐳 Docker Control Panel")
    operation = st.selectbox("Docker Operation", [
        "Launch New Container", "Stop Container", "Remove Container",
        "Start Container", "List Docker Images"
    ])
    name = st.text_input("Container name")
    image = st.text_input("Image name (if needed)")
    if st.button("Execute"):
        cmd = ""
        if operation == "Launch New Container":
            cmd = f"docker run -dit --name {name} {image}"
        elif operation == "Stop Container":
            cmd = f"docker stop {name}"
        elif operation == "Remove Container":
            cmd = f"docker rm -f {name}"
        elif operation == "Start Container":
            cmd = f"docker start {name}"
        if cmd:
            os.system(cmd)
            st.success(f"{operation} executed.")
    if operation == "List Docker Images" and st.button("List Images"):
        output = os.popen("docker images").read()
        st.text_area("Docker Images:", output, height=300)

# ------------------ Send Email ------------------
elif choice == "📧 Send Email":
    st.title("📧 Email Sender")
    sender = st.text_input("Your Email")
    recipient = st.text_input("Recipient Email")
    subject = st.text_input("Subject")
    body = st.text_area("Message")
    password = st.text_input("App Password", type="password")
    if st.button("Send Email"):
        msg = EmailMessage()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.set_content(body)
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender, password)
                server.send_message(msg)
                st.success("✅ Email sent!")
        except Exception as e:
            st.error(f"Email Error: {str(e)}")

# ------------------ Twilio Call ------------------
elif choice == "📞 Make Call":
    st.title("📞 Twilio Call")
    sid = st.text_input("Twilio SID")
    token = st.text_input("Auth Token", type="password")
    from_no = st.text_input("Twilio Number (+countrycode)")
    to_no = st.text_input("Recipient Number (+countrycode)")
    if st.button("Make Call"):
        try:
            client = Client(sid, token)
            call = client.calls.create(
                to=to_no,
                from_=from_no,
                url="http://demo.twilio.com/docs/voice.xml"
            )
            st.success(f"Call initiated! SID: {call.sid}")
        except Exception as e:
            st.error(f"Call Error: {str(e)}")

# ------------------ Facebook Post ------------------
elif choice == "📘 Facebook Post":
    st.title("📘 Facebook Page Post")
    page_id = st.text_input("Page ID")
    token = st.text_input("Page Access Token")
    message = st.text_area("Message")
    if st.button("Post to Facebook"):
        r = requests.post(
            f"https://graph.facebook.com/{page_id}/feed",
            data={"message": message, "access_token": token}
        )
        if r.status_code == 200:
            st.success("✅ Post published!")
        else:
            st.error(f"Facebook API Error: {r.json()}")

# ------------------ Instagram Post ------------------
elif choice == "📷 Instagram Post":
    st.title("📷 Instagram Business Post")
    access_token = st.text_input("Access Token")
    account_id = st.text_input("Business Account ID")
    image_url = st.text_input("Public Image URL")
    caption = st.text_area("Caption")
    if st.button("Post to Instagram"):
        try:
            container_res = requests.post(
                f"https://graph.facebook.com/v18.0/{account_id}/media",
                data={
                    "image_url": image_url,
                    "caption": caption,
                    "access_token": access_token
                }
            ).json()
            cont_id = container_res.get("id")
            if cont_id:
                publish_res = requests.post(
                    f"https://graph.facebook.com/v18.0/{account_id}/media_publish",
                    data={"creation_id": cont_id, "access_token": access_token}
                )
                if publish_res.status_code == 200:
                    st.success("✅ Post published to Instagram!")
                else:
                    st.error(f"Instagram Publish Error: {publish_res.json()}")
            else:
                st.error(f"Container Error: {container_res}")
        except Exception as e:
            st.error(f"Instagram Error: {str(e)}")

# ------------------ HTML Interpreter ------------------
elif choice == "🧾 HTML Interpreter":
    st.title("🧾 Live HTML Preview")
    html_code = st.text_area("Write HTML below:", height=300, placeholder="<h1>Hello World!</h1>")
    if html_code:
        st.components.v1.html(html_code, height=400, scrolling=True)
    else:
        st.info("Live preview will appear here.")

# ------------------ Location Finder ------------------
elif choice == "🌍 Location Finder":
    st.title("🌍 Address to Coordinates")
    place = st.text_input("Enter location/address:")
    if st.button("Get Coordinates") and place:
        try:
            response = requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={place}").json()
            if response:
                lat = response[0]['lat']
                lon = response[0]['lon']
                st.success(f"📍 Latitude: {lat} | Longitude: {lon}")
            else:
                st.warning("⚠️ No results found.")
        except Exception as e:
            st.error(f"Location API Error: {str(e)}")

# ------------------ Textlocal SMS ------------------
elif choice == "📩 Send SMS":
    st.title("📩 Send SMS via Textlocal")
    api_key = st.text_input("API Key")
    numbers = st.text_input("Recipient Number(s)")
    message = st.text_area("Message")
    if st.button("Send SMS"):
        data = {
            'apikey': api_key,
            'numbers': numbers,
            'message': message,
            'sender': 'TXTLCL'
        }
        try:
            response = requests.post("https://api.textlocal.in/send/", data=data)
            st.json(response.json())
        except Exception as e:
            st.error(f"SMS Error: {str(e)}")
