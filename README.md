# 🤖 OmniGen AI Agent
### Multi-Modal Intelligent Image Generation & Editing System

OmniGen AI Agent is a powerful Generative AI system that can **understand user intent and generate or edit images intelligently** using advanced diffusion models and LLM reasoning.

Built with a focus on **low VRAM usage**, this system runs efficiently even on **Google Colab Free Tier (T4 GPU)** without crashes.

---

## 🚀 Features

- 🧠 **Smart AI Brain**
  - Uses Llama 3 (via Groq API) to understand prompts
  - Automatically decides:
    - `TXT2IMG` (generate new image)
    - `IMG2IMG` (edit existing image)

- ⚡ **Ultra-Fast Image Generation**
  - Powered by SDXL-Turbo
  - High-quality images in very few steps

- 🎯 **Precision Image Editing**
  - ControlNet Depth preserves:
    - Face structure
    - Pose
    - Layout
  - Only modifies requested parts (style, background, etc.)

- 🛡️ **Memory Optimized (No Crashes)**
  - Attention slicing
  - CPU offloading
  - VRAM-safe pipeline design

- 🌐 **Live Public Access**
  - Ngrok integration for instant public URL
 
## 🧪 Usage

### 1. Open the Web Interface

After running the project, open the ngrok public URL in your browser.

---

### 2. Enter Your Prompt

Type your request in the input box. Examples:

- "Generate a futuristic city at night"
- "Make this image cyberpunk style"
- "Change background to beach"

---

### 3. Let AI Decide

The system will automatically:

- Detect whether you want to generate a new image (`TXT2IMG`)
- Or edit an existing image (`IMG2IMG`)

---

### 4. Get Result

- The generated/edited image will appear on the screen
- Results are processed in real-time

---

## 📝 Example Use Cases

- 🎨 Generate AI art from text
- 🖼️ Edit existing images (style, background, theme)
- 👤 Modify portraits while keeping face structure
- 🌆 Convert scenes into different styles (cyberpunk, anime, etc.)

---

## 🏗️ Project Structure
OmniGen_Image_Agent/
├── main.py              # Starts server and handles ngrok
├── agent_brain.py       # AI logic (decides what to do)
├── image_pipeline.py    # Handles image generation/editing
├── config.py            # API keys and configuration
│
├── templates/
│   └── index.html       # Frontend UI page
│
├── static/
│   ├── css/
│   │   └── style.css    # Styling
│   └── js/
│       └── app.js       # Frontend logic
├── .env                 # Secret keys (not uploaded)
├── .gitignore           # Ignore sensitive files
└── README.md            # Project documentation
