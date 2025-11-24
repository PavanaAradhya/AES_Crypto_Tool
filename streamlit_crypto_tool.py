import streamlit as st

# Custom CSS
st.markdown("""
    <style>

    /* Main background */
    .stApp {
        background: linear-gradient(to bottom right, #0a4b78, #e3f2fd);
        color: white;
    }

    /* Title style */
    .title {
        text-align: center;
        font-size: 36px;
        font-weight: 700;
        color: #ffffff;
        padding: 10px;
        margin-bottom: 20px;
    }

    /* Card style */
    .crypto-card {
        background: rgba(255,255,255,0.15);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        backdrop-filter: blur(6px);
        color: #ffffff;
    }

    /* Buttons */
    .stButton > button {
        background-color: #ffffff;
        color: #0a4b78 !important;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 10px;
        border: none;
        font-weight: 600;
    }
    .stButton > button:hover {
        background-color: #0a4b78;
        color: white !important;
        border: 2px solid white;
        transition: 0.3s;
    }

    /* Text inputs */
    .stTextInput > div > div > input {
        background-color: rgba(255,255,255,0.8);
        color: #0a4b78;
        border-radius: 8px;
    }

    textarea {
        background-color: rgba(255,255,255,0.85) !important;
        color: #0a4b78 !important;
        border-radius: 10px !important;
    }

    </style>
""", unsafe_allow_html=True)

# streamlit_crypto_tool.py
import streamlit as st
from cryptography.fernet import Fernet, InvalidToken
import os

st.set_page_config(page_title="AES Crypto Tool ", layout="centered")

KEY_FILE = "secret.key"

# ---------------------------
# Helpers
# ---------------------------
def save_key_to_file(key_bytes):
    with open(KEY_FILE, "wb") as f:
        f.write(key_bytes)

def read_saved_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    return None

def is_valid_fernet_key(key_bytes):
    try:
        Fernet(key_bytes)
        return True
    except Exception:
        return False

# ---------------------------
# Sidebar: page selector (acts like pages/sides)
# ---------------------------
page = st.sidebar.radio("Choose page", ["Generate Key", "Encrypt", "Decrypt"])

st.title("AES Crypto Tool")
st.write("Follow the flow: 1) Generate key → 2) Use same key to Encrypt → 3) Use same key to Decrypt")

# ---------------------------
# PAGE: Generate Key
# ---------------------------
if page == "Generate Key":
    st.header("1) Generate a new secret.key")
    st.write("Click **Generate** to create a new Fernet (AES) key. Save it securely. You will need the exact key to encrypt and decrypt.")
    if st.button("Generate Key"):
        new_key = Fernet.generate_key()
        save_key_to_file(new_key)
        st.success("New key generated and saved to `secret.key` in this folder.")
        st.code(new_key.decode(), language=None)
        st.info("Copy this key and use it exactly (paste in Encrypt/Decrypt pages). If you lose it, encrypted files cannot be recovered.")
    else:
        saved = read_saved_key()
        if saved:
            st.write("A `secret.key` already exists in this folder. You can regenerate if you want a new key.")
            with st.expander("Show saved key"):
                st.code(saved.decode(), language=None)
            if st.button("Delete saved key"):
                try:
                    os.remove(KEY_FILE)
                    st.success("Saved `secret.key` deleted. You can generate a new one.")
                except Exception as e:
                    st.error(f"Failed to delete key: {e}")
        else:
            st.info("No saved key found. Click Generate Key to create one.")

# ---------------------------
# PAGE: Encrypt
# ---------------------------
elif page == "Encrypt":
    st.header("2) Encrypt — enter the same secret key to use for encryption")
    st.write("Paste the exact base64 key (generated earlier) into the Key field below. The app will use THAT key to encrypt your text or uploaded .txt file.")
    key_text = st.text_input("Enter secret key (paste exactly)", type="password")
    show_key = st.checkbox("Show key text", key="enc_show_key")
    if show_key:
        st.text(key_text)

    if key_text:
        key_bytes = key_text.encode()
        if not is_valid_fernet_key(key_bytes):
            st.error("This does not look like a valid Fernet key. Re-check the key you pasted.")
        else:
            f = Fernet(key_bytes)
            st.subheader("Encrypt text")
            plain = st.text_area("Enter plain text to encrypt", height=150)
            if st.button("Encrypt Text"):
                if not plain:
                    st.warning("Please enter text to encrypt.")
                else:
                    encrypted = f.encrypt(plain.encode())
                    st.success("Text encrypted.")
                    st.code(encrypted.decode())
                    st.download_button("Download encrypted text (.txt)", encrypted, file_name="encrypted.txt")

            st.markdown("---")
            st.subheader("Encrypt a text file (.txt)")
            uploaded = st.file_uploader("Upload a .txt file to encrypt", type=["txt"])
            if uploaded is not None:
                data = uploaded.read()
                if st.button("Encrypt uploaded file"):
                    try:
                        encrypted_file = f.encrypt(data)
                        st.success("File encrypted.")
                        # suggest filename
                        suggested = uploaded.name + ".enc"
                        st.download_button("Download encrypted file (.enc)", encrypted_file, file_name=suggested)
                    except Exception as e:
                        st.error(f"Encryption failed: {e}")
    else:
        st.info("Paste the secret key (generated earlier) to enable encryption.")

# ---------------------------
# PAGE: Decrypt
# ---------------------------
elif page == "Decrypt":
    st.header("3) Decrypt — enter the same secret key to decrypt")
    st.write("Paste the exact key used to encrypt files/text. The app will attempt to decrypt.")
    key_text_d = st.text_input("Enter secret key (paste exactly)", type="password", key="dec_key")
    show_key_d = st.checkbox("Show key text", key="dec_show_key")
    if show_key_d:
        st.text(key_text_d)

    if key_text_d:
        key_bytes = key_text_d.encode()
        if not is_valid_fernet_key(key_bytes):
            st.error("This does not look like a valid Fernet key. Re-check the key you pasted.")
        else:
            f = Fernet(key_bytes)
            st.subheader("Decrypt text")
            enc_text = st.text_area("Paste encrypted text here", height=150)
            if st.button("Decrypt Text"):
                if not enc_text:
                    st.warning("Please paste encrypted text to decrypt.")
                else:
                    try:
                        decrypted = f.decrypt(enc_text.encode())
                        st.success("Text decrypted.")
                        st.code(decrypted.decode())
                        st.download_button("Download decrypted text (.txt)", decrypted, file_name="decrypted.txt")
                    except InvalidToken:
                        st.error("Decryption failed: Invalid key or corrupted ciphertext.")
                    except Exception as e:
                        st.error(f"Decryption failed: {e}")

            st.markdown("---")
            st.subheader("Decrypt an encrypted file (.enc)")
            uploaded_enc = st.file_uploader("Upload an encrypted file (.enc) to decrypt", type=["enc"])
            if uploaded_enc is not None:
                enc_bytes = uploaded_enc.read()
                if st.button("Decrypt uploaded file"):
                    try:
                        decrypted_file = f.decrypt(enc_bytes)
                        st.success("File decrypted.")
                        suggested = uploaded_enc.name
                        if suggested.lower().endswith(".enc"):
                            suggested = suggested[:-4]
                        suggested = suggested + "_decrypted.txt"
                        st.download_button("Download decrypted file (.txt)", decrypted_file, file_name=suggested)
                    except InvalidToken:
                        st.error("Decryption failed: Invalid key or corrupted file.")
                    except Exception as e:
                        st.error(f"Decryption failed: {e}")
    else:
        st.info("Paste the secret key (generated earlier) to enable decryption.")
