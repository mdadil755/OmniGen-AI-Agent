import json
from groq import Groq
import config

class OmniGenBrain:
    def __init__(self):
        self.client = Groq(api_key=config.GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"
        self.style_presets = {
            "anime": "anime style, vibrant colors, studio ghibli aesthetic, detailed sketch",
            "realistic": "photorealistic studio portrait, 4k resolution, cinematic dramatic lighting, highly detailed textures",
            "cyberpunk": "cyberpunk theme, neon glow, wet rainy streets, futuristic augmentations",
            "disney": "pixar 3d animated style, smooth character rendering, expressive cartoon features",
            "oil painting": "classical canvas texture, rich brushstrokes, fine art masterpiece look"
        }

    def analyze_input(self, user_prompt, history, has_image=False):
        history_context = "\n".join([f"User: {h['user']}\nAgent: {h['intent']}" for h in history[-3:]])
        
        system_matrix = f"""
        Act as the primary NLP Decision Brain for a multi-modal image generation agent.
        
        Context of previous turns:
        {history_context}
        
        Current User Request: "{user_prompt}"
        Active Canvas Has Image: {has_image}
        
        Tasks:
        1. Classify Intent: Determine if the user wants a new image ("TXT2IMG") or wants to modify/edit the current existing image ("IMG2IMG"). If they want changes in the previous image, mark it "IMG2IMG".
        2. Expand Prompt: Enrich the raw user input into a highly descriptive prompt with lighting, composition, and high-quality keywords. 
        3. Style Application: Check if any style from {json.dumps(self.style_presets)} matches or should be applied.
        
        Return ONLY a strict valid JSON object:
        {{
            "intent": "TXT2IMG" or "IMG2IMG",
            "expanded_prompt": "highly detailed expanded prompt string",
            "negative_prompt": "blurry, deformed, low quality, distorted"
        }}
        Do not include any markdowns or explanations.
        """
        
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": system_matrix}],
            model=self.model,
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
