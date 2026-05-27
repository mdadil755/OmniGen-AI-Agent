import os
import torch

PROJECT_PATH = '/content/drive/MyDrive/OmniGen_Image_Agent'
GROQ_API_KEY = ""

MODEL_ID = "stabilityai/sdxl-turbo"
IMAGE_SIZE = 512
NUM_STEPS = 2
GUIDANCE_SCALE = 0.0

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32

os.makedirs(os.path.join(PROJECT_PATH, 'templates'), exist_ok=True)
os.makedirs(os.path.join(PROJECT_PATH, 'static', 'css'), exist_ok=True)
os.makedirs(os.path.join(PROJECT_PATH, 'static', 'js'), exist_ok=True)
os.makedirs(os.path.join(PROJECT_PATH, 'cache_history', 'storage'), exist_ok=True)
