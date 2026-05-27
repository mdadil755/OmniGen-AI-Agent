import os
import gc
import io
import base64
import torch
import numpy as np
from PIL import Image
from diffusers import StableDiffusionXLControlNetPipeline, ControlNetModel
import config

class OmniGenPipelineEngine:
    def __init__(self):
        self.pipe = None
        self.controlnet = None

    def _clear_memory(self):
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    def load_unified_pipeline(self, need_controlnet=False):
        if self.pipe is not None:
            if need_controlnet and self.controlnet is not None:
                return
            if not need_controlnet and self.controlnet is None:
                return
            
            del self.pipe
            if self.controlnet is not None:
                del self.controlnet
                self.controlnet = None
            self.pipe = None
            self._clear_memory()

        if need_controlnet:
            print("🔄 Loading ControlNet Depth Engine for Precision Editing...")
            self.controlnet = ControlNetModel.from_pretrained(
                "xinsir/controlnet-depth-sdxl-1.0",
                torch_dtype=config.DTYPE,
                use_safetensors=True
            ).to(config.DEVICE)
            
            self.pipe = StableDiffusionXLControlNetPipeline.from_pretrained(
                config.MODEL_ID,
                controlnet=self.controlnet,
                torch_dtype=config.DTYPE,
                use_safetensors=True
            ).to(config.DEVICE)
        else:
            print("🔄 Loading Standard Fast Generation Engine...")
            from diffusers import StableDiffusionXLPipeline
            self.pipe = StableDiffusionXLPipeline.from_pretrained(
                config.MODEL_ID,
                torch_dtype=config.DTYPE,
                variant="fp16" if config.DEVICE == "cuda" else None,
                use_safetensors=True
            ).to(config.DEVICE)

        if config.DEVICE == "cuda":
            self.pipe.enable_attention_slicing()
            self.pipe.enable_xformers_memory_efficient_attention()
            self.pipe.enable_sequential_cpu_offload()
            
        self._clear_memory()

    def b64_to_pil(self, b64_str):
        img_data = base64.b64decode(b64_str.split(",")[-1])
        return Image.open(io.BytesIO(img_data)).convert("RGB")

    def pil_to_b64(self, pil_img):
        buffered = io.BytesIO()
        pil_img.save(buffered, format="JPEG", quality=85)
        return "data:image/jpeg;base64," + base64.b64encode(buffered.getvalue()).decode("utf-8")

    def run_generation(self, decision, input_image_b64=None):
        intent = decision["intent"]
        prompt = decision["expanded_prompt"]
        neg_prompt = decision["negative_prompt"]
        
        generator = torch.Generator(device=config.DEVICE).manual_seed(42)

        if intent == "TXT2IMG":
            self.load_unified_pipeline(need_controlnet=False)
            output = self.pipe(
                prompt=prompt,
                negative_prompt=neg_prompt,
                num_inference_steps=config.NUM_STEPS,
                guidance_scale=config.GUIDANCE_SCALE,
                generator=generator,
                target_size=(config.IMAGE_SIZE, config.IMAGE_SIZE),
                original_size=(config.IMAGE_SIZE, config.IMAGE_SIZE)
            ).images[0]

        elif intent == "IMG2IMG":
            if not input_image_b64:
                raise ValueError("Image modification requested but base canvas image is missing.")
            
            self.load_unified_pipeline(need_controlnet=True)
            init_img = self.b64_to_pil(input_image_b64)
            init_img = init_img.resize((config.IMAGE_SIZE, config.IMAGE_SIZE))
            
            output = self.pipe(
                prompt=prompt,
                negative_prompt=neg_prompt,
                image=init_img,
                control_image=init_img,
                strength=0.55,
                controlnet_conditioning_scale=0.7,
                num_inference_steps=config.NUM_STEPS,
                guidance_scale=config.GUIDANCE_SCALE,
                generator=generator
            ).images[0]

        return self.pil_to_b64(output)
