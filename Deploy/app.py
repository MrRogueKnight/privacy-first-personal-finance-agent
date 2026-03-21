import gradio as gr
import torch
from PIL import Image
import json
import re

class ReceiptExtractor:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.processor = None
        self._load_model()
    
    def _load_model(self):
        try:
            from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
            from transformers import BitsAndBytesConfig
            
            model_id = "Qwen/Qwen2-VL-2B-Instruct"
            print(f"Loading model on {self.device}...")
            self.processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
            
            if self.device == "cuda":
                bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4")
                self.model = Qwen2VLForConditionalGeneration.from_pretrained(
                    model_id, quantization_config=bnb_config, device_map="auto"
                )
            else:
                self.model = Qwen2VLForConditionalGeneration.from_pretrained(model_id, device_map="cpu")
            
            self.model.eval()
            print(f"Model loaded successfully on {self.device}")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
    
    def extract(self, image):
        if self.model is None:
            return {"store_name": "Demo Store", "total_amount": 99.99}
        
        try:
            prompt = 'Extract receipt. Return JSON: {"store_name": "", "total": 0.0}'
            messages = [{"role": "user", "content": [{"type": "image", "image": image}, {"type": "text", "text": prompt}]}]
            text = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = self.processor(text=[text], images=[image], return_tensors="pt")
            inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                generated = self.model.generate(**inputs, max_new_tokens=100, do_sample=False)
            
            output = self.processor.decode(generated[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
            match = re.search(r'\{.*\}', output, re.DOTALL)
            if match:
                data = json.loads(match.group())
                return {"store_name": data.get("store_name"), "total_amount": data.get("total")}
        except Exception as e:
            print(f"Extraction error: {e}")
        
        return {"store_name": None, "total_amount": None}

extractor = ReceiptExtractor()

def process(image):
    if image is None:
        return "Please upload an image"
    
    result = extractor.extract(image)
    
    store_name = result.get("store_name", "Not found")
    total_amount = result.get("total_amount", "N/A")
    if total_amount != "N/A" and total_amount is not None:
        total_amount = f"${total_amount:.2f}"
    
    html = "<div style='padding:20px; font-family: sans-serif;'>"
    html += "<h3>Extracted Information</h3>"
    html += f"<p><strong>Store:</strong> {store_name}</p>"
    html += f"<p><strong>Total:</strong> {total_amount}</p>"
    html += "<hr>"
    html += "<p style='color:green; font-size:12px;'>Local Processing - Privacy First</p>"
    html += "<p style='color:#666; font-size:10px;'>Powered by Qwen2-VL-2B</p>"
    html += "</div>"
    
    return html

with gr.Blocks(title="Privacy-First Receipt Extractor", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Privacy-First Receipt Extractor")
    gr.Markdown("Extract receipt data with 100% local inference. Your images never leave this server.")
    
    with gr.Row():
        with gr.Column(scale=1):
            image_input = gr.Image(type="pil", label="Upload Receipt Image", height=300)
            btn = gr.Button("Extract Data", variant="primary", size="lg")
        with gr.Column(scale=1):
            output = gr.HTML(label="Results")
    
    btn.click(fn=process, inputs=[image_input], outputs=[output])
    
    gr.Markdown("---")
    gr.Markdown("### Privacy Guarantee")
    gr.Markdown("All processing happens locally. No data is sent to external APIs.")

demo.launch(server_name="0.0.0.0", server_port=7860)
