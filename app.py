from diffusers import StableDiffusion3Pipeline
import torch
from io import BytesIO
import base64
# import os

class InferlessPythonModel:
    def initialize(self):
        HF_TOKEN =  os.getenv("HUGGINGFACE_AUTH_TOKEN") # Access Hugging Face token from environment variable
        self.pipe = StableDiffusion3Pipeline.from_pretrained("stabilityai/stable-diffusion-3-medium-diffusers", torch_dtype=torch.float16,token=HF_TOKEN)
        self.pipe = self.pipe.to("cuda")
        
    def infer(self, inputs):
        prompt = inputs["prompt"]
        image = self.pipe(prompt,negative_prompt="low quality",num_inference_steps=28,guidance_scale=7.0,).images[0]
        buff = BytesIO()
        image.save(buff, format="JPEG")
        img_str = base64.b64encode(buff.getvalue()).decode()

        return {"generated_image_base64" : img_str }
    
    def finalize(self):
        self.pipe = None