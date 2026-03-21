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
    
    def _validate_extraction(self, data):
        if data.get("is_receipt") is False:
            return None, None, "not_receipt"
        
        store = data.get("store_name")
        total = data.get("total")
        
        fake_store_patterns = ["demo store", "store", "receipt", "example", "sample", "test", "placeholder", "unknown", "none", "null"]
        fake_amount_patterns = [99.99, 0.0, 0, 100.00, 9.99, 49.99, 29.99]
        
        if store:
            store_lower = str(store).lower().strip()
            if len(store_lower) < 2:
                store = None
            elif any(pattern in store_lower for pattern in fake_store_patterns):
                store = None
        
        if total:
            try:
                amount = float(total)
                if amount <= 0 or amount > 10000:
                    total = None
                elif amount in fake_amount_patterns:
                    total = None
            except:
                total = None
        
        if store is None and total is None:
            return None, None, "not_detected"
        
        return store, total, "receipt"
    
    def extract(self, image):
        if self.model is None:
            return {"store_name": None, "total_amount": None, "status": "error", "message": "Model not loaded"}
        
        try:
            prompt = "Analyze this image carefully. If this is a RECEIPT (contains store name, items, prices, total amount), extract: {\"store_name\": \"full merchant name\", \"total\": numeric total amount}. If this is NOT a receipt (screenshot, badge, logo, random image, or no financial data), return: {\"is_receipt\": false}. Return ONLY valid JSON. Do not invent information."
            
            messages = [{
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": prompt}
                ]
            }]
            
            text = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = self.processor(text=[text], images=[image], return_tensors="pt")
            inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                generated = self.model.generate(**inputs, max_new_tokens=150, do_sample=False)
            
            output = self.processor.decode(generated[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
            
            json_match = re.search(r'\{.*\}', output, re.DOTALL)
            if json_match:
                try:
                    data = json.loads(json_match.group())
                    store, amount, status = self._validate_extraction(data)
                    
                    if status == "not_receipt":
                        return {"store_name": None, "total_amount": None, "status": "not_receipt", "message": "This does not appear to be a receipt. Please upload a valid receipt image."}
                    
                    return {"store_name": store, "total_amount": amount, "status": status, "message": "Extraction successful" if status == "receipt" else "No receipt data detected"}
                except:
                    pass
            
            return {"store_name": None, "total_amount": None, "status": "no_data", "message": "Could not extract receipt data. Please ensure the image contains a clear receipt."}
            
        except Exception as e:
            return {"store_name": None, "total_amount": None, "status": "error", "message": f"Processing error: {str(e)[:100]}"}


extractor = ReceiptExtractor()

def process(image):
    if image is None:
        return "Please upload an image"
    
    result = extractor.extract(image)
    
    store_name = result.get("store_name")
    total_amount = result.get("total_amount")
    status = result.get("status", "unknown")
    message = result.get("message", "")
    
    if status == "not_receipt":
        html = "<div style='padding:20px; background:#fff3cd; border-radius:10px; border-left:4px solid #ffc107;'>"
        html += "<h3 style='color:#856404; margin-top:0;'>No Receipt Detected</h3>"
        html += "<p style='color:#856404;'>" + message + "</p>"
        html += "<p style='color:#856404; font-size:12px;'>Please upload a valid receipt image with store name and total amount visible.</p>"
        html += "</div>"
        return html
    
    if status == "error" or status == "no_data":
        html = "<div style='padding:20px; background:#f8d7da; border-radius:10px; border-left:4px solid #dc3545;'>"
        html += "<h3 style='color:#721c24; margin-top:0;'>Extraction Failed</h3>"
        html += "<p style='color:#721c24;'>" + message + "</p>"
        html += "<p style='color:#721c24; font-size:12px;'>Try uploading a clearer image or different receipt.</p>"
        html += "</div>"
        return html
    
    store_display = store_name if store_name else "Not detected"
    amount_display = f"${total_amount:.2f}" if total_amount else "Not detected"
    
    confidence_score = 0.0
    if store_name:
        confidence_score += 0.5
    if total_amount:
        confidence_score += 0.5
    
    confidence_color = "#2ecc71" if confidence_score >= 0.8 else "#f39c12" if confidence_score >= 0.4 else "#e74c3c"
    
    html = "<div style='padding:20px; background:#f8f9fa; border-radius:10px;'>"
    html += "<h3 style='margin-top:0; color:#2c3e50;'>Extracted Information</h3>"
    html += "<div style='background:white; padding:15px; border-radius:8px; margin:10px 0;'>"
    html += "<strong>Store Name:</strong>"
    html += "<span style='color:" + confidence_color + "; font-size:16px;'> " + store_display + "</span>"
    html += "</div>"
    html += "<div style='background:white; padding:15px; border-radius:8px; margin:10px 0;'>"
    html += "<strong>Total Amount:</strong>"
    html += "<span style='color:" + confidence_color + "; font-size:16px;'> " + amount_display + "</span>"
    html += "</div>"
    html += "<div style='background:white; padding:15px; border-radius:8px; margin:10px 0;'>"
    html += "<strong>Confidence:</strong>"
    html += "<div style='background:#ddd; border-radius:10px; margin-top:5px;'>"
    html += "<div style='background:" + confidence_color + "; width:" + str(int(confidence_score*100)) + "%; border-radius:10px; text-align:center; color:white;'>"
    html += str(int(confidence_score*100)) + "%"
    html += "</div></div></div>"
    html += "<div style='background:#e8f5e9; padding:10px; border-radius:8px; margin:10px 0; text-align:center;'>"
    html += "Local Processing - Privacy First"
    html += "</div></div>"
    
    return html


with gr.Blocks(title="Privacy-First Receipt Extractor", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Privacy-First Receipt Extractor")
    gr.Markdown("Extract receipt data with 100% local inference. Your images never leave this server.")
    
    with gr.Row():
        with gr.Column(scale=1):
            image_input = gr.Image(type="pil", label="Upload Receipt Image", height=350)
            btn = gr.Button("Extract Data", variant="primary", size="lg")
            gr.Markdown("### Tips for Best Results\n- Use clear, well-lit receipt images\n- Ensure store name and total amount are visible\n- Portrait orientation works best")
        with gr.Column(scale=1):
            output = gr.HTML(label="Results")
    
    btn.click(fn=process, inputs=[image_input], outputs=[output])
    
    gr.Markdown("---")
    gr.Markdown("### Privacy Guarantee")
    gr.Markdown("All processing happens locally. No data is sent to external APIs. The model will reject non-receipt images.")

demo.launch(server_name="0.0.0.0", server_port=7860)
