import streamlit as st
import requests
from PIL import Image
import io

API_URL = "http://localhost:8000/upload-id/"

st.set_page_config(page_title="AI Housing ID Verification", layout="centered")
st.title("🧠 AI Housing ID Verifier")
st.write("Upload a scanned South African ID to verify RDP title eligibility.")

uploaded_file = st.file_uploader("📎 Upload ID Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Show image preview
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded ID Preview", use_column_width=True)

    # Send to backend
    if st.button("🔍 Extract & Verify ID"):
        with st.spinner("Processing..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            response = requests.post(API_URL, files=files)

        if response.status_code == 200:
            data = response.json()

            if "error" in data:
                st.error(data["error"])
            else:
                st.success("✅ ID Verification Completed")
                st.write(f"**Extracted ID Number:** `{data['extracted_id']}`")
                st.write("**Validation Result:**")
                st.json(data["validation"])
                st.write("**Full Extracted Text:**")
                st.code(data["raw_text"])
        else:
            st.error("❌ Something went wrong. Please try again.")