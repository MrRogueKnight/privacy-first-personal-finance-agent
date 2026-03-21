import gradio as gr
import torch
from PIL import Image
import json
import re
import random
import pandas as pd
from datetime import datetime
import threading
import concurrent.futures

INFERENCE_TIMEOUT = 15
MAX_HISTORY = 50
MONTHLY_BUDGET = 2000

torch.set_num_threads(2)

CATEGORIES = {
    "groceries": ["walmart", "kroger", "target", "costco", "aldi", "supermarket", "grocery", "food mart"],
    "dining": ["restaurant", "cafe", "starbucks", "mcdonald", "kfc", "burger", "pizza", "food court"],
    "transport": ["uber", "lyft", "taxi", "bus", "train", "gas", "fuel", "petrol", "parking"],
    "shopping": ["amazon", "best buy", "mall", "clothing", "shoe", "department"],
    "entertainment": ["netflix", "spotify", "movie", "cinema", "theater", "concert"],
    "utilities": ["electric", "water", "internet", "phone bill"],
    "healthcare": ["pharmacy", "cvs", "walgreens", "doctor", "clinic"]
}

def categorize(store_name):
    if not store_name:
        return "other"
    store_lower = store_name.lower()
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in store_lower:
                return category
    return "other"

class ReceiptExtractor:
    def __init__(self):
        self.device = "cpu"
        self.model = None
        self.processor = None
        self.demo_mode = True
        self.loaded = False
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    def _load_model(self):
        try:
            print("Loading model...")
            from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
            model_id = "Qwen/Qwen2-VL-2B-Instruct"
            self.processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
            self.model = Qwen2VLForConditionalGeneration.from_pretrained(
                model_id, device_map="cpu", torch_dtype=torch.float32, low_cpu_mem_usage=True
            )
            self.model.eval()
            self.demo_mode = False
            self.loaded = True
            print("Model loaded")
        except Exception as e:
            print(f"Model load failed: {e}")

    def _run_inference(self, image):
        prompt = 'Extract store name and total amount. Return JSON: {"store_name": "", "total": 0}'
        messages = [{"role": "user", "content": [{"type": "image", "image": image}, {"type": "text", "text": prompt}]}]
        text = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = self.processor(text=[text], images=[image], return_tensors="pt")
        inputs = {k: v.to("cpu") for k, v in inputs.items()}
        with torch.no_grad():
            generated = self.model.generate(**inputs, max_new_tokens=60, do_sample=False)
        output = self.processor.decode(generated[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
        match = re.search(r'\{[^{}]*\}', output)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass
        return None

    def extract(self, image):
        if not self.loaded:
            if not hasattr(self, '_loading_started'):
                self._loading_started = True
                threading.Thread(target=self._load_model, daemon=True).start()
            demo_stores = ["WALMART", "STARBUCKS", "TARGET", "UBER", "NETFLIX", "COSTCO"]
            demo_amounts = [45.67, 5.25, 23.45, 15.50, 14.99, 89.99]
            idx = random.randint(0, len(demo_stores) - 1)
            return {
                "store_name": demo_stores[idx],
                "total_amount": demo_amounts[idx],
                "category": categorize(demo_stores[idx]),
                "status": "demo",
                "message": "Model loading in background"
            }

        try:
            future = self._executor.submit(self._run_inference, image)
            data = future.result(timeout=INFERENCE_TIMEOUT)
            if data:
                store = data.get("store_name")
                amount = data.get("total")
                if amount and 0.01 <= amount <= 10000:
                    return {
                        "store_name": store,
                        "total_amount": amount,
                        "category": categorize(store),
                        "status": "success",
                        "message": "Extraction successful"
                    }
            return {
                "store_name": None,
                "total_amount": None,
                "category": "other",
                "status": "failed",
                "message": "Could not extract data"
            }
        except Exception as e:
            return {
                "store_name": None,
                "total_amount": None,
                "category": "other",
                "status": "error",
                "message": str(e)[:100]
            }

extractor = ReceiptExtractor()
threading.Thread(target=extractor._load_model, daemon=True).start()

class HistoryManager:
    def __init__(self):
        self.history = []
        self.budget = MONTHLY_BUDGET

    def add(self, store, amount, category, confidence):
        transaction = {
            "date": datetime.now().isoformat(),
            "store": store,
            "amount": amount,
            "category": category,
            "confidence": confidence
        }
        self.history.insert(0, transaction)
        if len(self.history) > MAX_HISTORY:
            self.history = self.history[:MAX_HISTORY]
        return transaction

    def get_summary(self):
        if not self.history:
            return {"total": 0, "count": 0, "by_category": {}, "budget_remaining": self.budget}
        total = sum(t["amount"] for t in self.history)
        by_category = {}
        for t in self.history:
            cat = t["category"]
            by_category[cat] = by_category.get(cat, 0) + t["amount"]
        spent_this_month = sum(t["amount"] for t in self.history)
        remaining = max(0, self.budget - spent_this_month)
        return {
            "total": total,
            "count": len(self.history),
            "by_category": by_category,
            "spent_this_month": spent_this_month,
            "budget_remaining": remaining
        }

history_state = gr.State(HistoryManager())

def process(image, state):
    if image is None:
        return None, "Please upload an image", state
    result = extractor.extract(image)
    if result.get("status") == "success":
        state.add(result["store_name"], result["total_amount"], result["category"], 0.8)
    return result, result.get("message", ""), state

def refresh_history(state):
    transactions = state.history
    if not transactions:
        return "No transactions yet"
    html = "<div style='max-height:400px; overflow-y:auto;'>"
    for t in transactions[:20]:
        date = datetime.fromisoformat(t["date"]).strftime("%Y-%m-%d %H:%M")
        html += f"<div style='background:white; padding:12px; margin:8px 0; border-radius:8px;'>"
        html += f"<div><strong>{t['store']}</strong> <span style='float:right'>${t['amount']:.2f}</span></div>"
        html += f"<div style='font-size:12px; color:#666;'>{t['category'].upper()} | {date}</div>"
        html += "</div>"
    html += "</div>"
    return html

def refresh_dashboard(state):
    summary = state.get_summary()
    html = f"<div style='background:linear-gradient(135deg, #667eea, #764ba2); padding:20px; border-radius:10px; color:white;'>"
    html += f"<h3>Spending Summary</h3>"
    html += f"<div><strong>Total:</strong> ${summary['total']:.2f}</div>"
    html += f"<div><strong>Transactions:</strong> {summary['count']}</div>"
    html += f"<div><strong>Budget Remaining:</strong> ${summary['budget_remaining']:.2f}</div>"
    html += "</div><h3>Spending by Category</h3>"
    for cat, amt in sorted(summary["by_category"].items(), key=lambda x: x[1], reverse=True):
        pct = (amt / summary["total"] * 100) if summary["total"] > 0 else 0
        html += f"<div><strong>{cat.upper()}</strong> ${amt:.2f} ({pct:.1f}%)</div>"
        html += f"<div style='background:#ddd; border-radius:10px; height:8px;'><div style='background:#667eea; width:{pct}%; border-radius:10px; height:8px;'></div></div>"
    return html

with gr.Blocks(title="Expense Tracker", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Expense Tracker\nUpload receipts to track spending automatically")

    with gr.Row():
        with gr.Column():
            image_input = gr.Image(type="pil", label="Upload Receipt", height=300)
            btn = gr.Button("Extract", variant="primary")
        with gr.Column():
            output = gr.JSON(label="Extracted Data")
            message = gr.HTML()

    btn.click(
        fn=process,
        inputs=[image_input, history_state],
        outputs=[output, message, history_state]
    )

    with gr.Tabs():
        with gr.TabItem("History"):
            history_display = gr.HTML()
            refresh_btn = gr.Button("Refresh")
            refresh_btn.click(fn=refresh_history, inputs=[history_state], outputs=[history_display])
            demo.load(fn=refresh_history, inputs=[history_state], outputs=[history_display])

        with gr.TabItem("Dashboard"):
            dashboard_display = gr.HTML()
            refresh_dash_btn = gr.Button("Refresh")
            refresh_dash_btn.click(fn=refresh_dashboard, inputs=[history_state], outputs=[dashboard_display])
            demo.load(fn=refresh_dashboard, inputs=[history_state], outputs=[dashboard_display])

    gr.Markdown("---\n**Privacy:** All processing is local\n**First Use:** Model loads in background (30-60 seconds)")

demo.launch(server_name="0.0.0.0", server_port=7860)
