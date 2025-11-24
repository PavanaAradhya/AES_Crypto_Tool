
  <h1>🔐 AES_Crypto_Tool</h1>
    <p class="lead">A simple AES (Fernet) encryption &amp; decryption tool — generate secret keys, encrypt text/files, and decrypt using the same key. Streamlit / Flask + Electron versions included.</p>

  <a class="btn" href="sandbox:/mnt/data/AES_Crypto_Tool.zip" download>📦 Download Project ZIP</a>

  <div class="section">
      <h2>Features</h2>
      <ul>
        <li>Generate a Fernet (AES) secret key and save as <code>secret.key</code></li>
        <li>Encrypt / decrypt plain text</li>
        <li>Encrypt / decrypt files (<code>.txt ↔ .enc</code>)</li>
        <li>Streamlit UI and Flask+Electron options included</li>
      </ul>
    </div>

  <div class="section">
      <h2>Quick Start — Streamlit (local)</h2>
      <pre>
# inside project folder
python -m venv venv
# Windows
.\venv\Scripts\activate
pip install -r requirements.txt
python -m streamlit run streamlit_crypto_tool.py
      </pre>
    </div>

  <div class="section">
      <h2>Quick Start — Flask + Electron (local)</h2>
      <pre>
# Backend
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python app.py

# Frontend (another terminal)
cd frontend
npm install
npm start
      </pre>
    </div>

  <div class="section">
      <h2>Recommended Workflow</h2>
      <ol>
        <li>Generate a secret key and save it (or download <code>secret.key</code>).</li>
        <li>Use the same exact key to encrypt text or files.</li>
        <li>To decrypt, provide the same key used in step 2.</li>
      </ol>
      <p><strong>Important:</strong> If you regenerate the key, previously encrypted files cannot be decrypted.</p>
    </div>

  <div class="section">
      <h2>Security Notes</h2>
      <ul>
        <li>This is a local demo tool. Do not use it to protect highly sensitive production data without a proper key management system.</li>
        <li>Keep <code>secret.key</code> private and do not commit it to git.</li>
      </ul>
    </div>

  <footer>
      Created for demo / mini-project submissions. For help running the project or packaging the Electron app into an executable, ask me and I’ll provide step-by-step scripts.
    </footer>
  </div>
</body>
</html>
