import os
import sys
from flask import Flask, render_template, request, jsonify

# Project root path settings
PROJECT_PATH = '/content/drive/MyDrive/OmniGen_Image_Agent'
sys.path.append(PROJECT_PATH)

import config
from agent_brain import OmniGenBrain
from image_pipeline import OmniGenPipelineEngine

app = Flask(__name__, 
            template_folder=os.path.join(PROJECT_PATH, 'templates'), 
            static_folder=os.path.join(PROJECT_PATH, 'static'))

# Initialize engines
brain = OmniGenBrain()
engine = OmniGenPipelineEngine()

# In-memory conversational tracking state
session_memory = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_chat', methods=['POST'])
def process_chat():
    global session_memory
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()
        last_image_b64 = data.get("last_image", None)

        if not user_message:
            return jsonify({"error": "Prompt token empty."}), 400

        # Run Phase 1: Intent & Prompt Expansion
        has_canvas_image = True if last_image_b64 else False
        decision = brain.analyze_input(
            user_prompt=user_message, 
            history=session_memory, 
            has_image=has_canvas_image
        )

        # Run Phase 2 & 3: Optimized Inference Core
        output_image_b64 = engine.run_generation(
            decision=decision, 
            input_image_b64=last_image_b64
        )

        # Append to conversational tracking list
        session_memory.append({
            "user": user_message,
            "intent": decision["intent"]
        })

        return jsonify({
            "status": "success",
            "active_image": output_image_b64,
            "intent_used": decision["intent"],
            "expanded_prompt": decision["expanded_prompt"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # 1. Purane saare blocked background processes ko system level par kill karo
    import subprocess
    try:
        subprocess.run(["pkill", "-f", "ngrok"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass

    # 2. Ngrok Tunnel ko initialize karo dynamic tracking ke liye
    from pyngrok import ngrok
    try:
        # Apni static dashboard problem bypass karne ke liye disconnect protocol
        ngrok.disconnect_all()
    except:
        pass
        
    # Apna Ngrok Auth Token yahan set karo (Agar config me hai toh config.NGROK_TOKEN use kar sakte ho)
    ngrok.set_auth_token("")
    
    try:
        # Dynamic link generate karne ke liye bind_tls forcing
        public_url = ngrok.connect(5000, bind_tls=True)
        print("\n" + "="*60)
        print(f"🚀 OMNIGEN PLATFORM IS LIVE ON INTERNET!")
        print(f"👉 CLICK THIS LINK TO OPEN ON YOUR PHONE: {public_url.public_url}")
        print("="*60 + "\n")
    except Exception as e:
        print(f"Tunnel Initialization Failed: {e}")

    # 3. Flask Server Production Trigger
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)


