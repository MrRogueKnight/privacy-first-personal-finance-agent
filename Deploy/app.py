import gradio as gr
import cv2
import numpy as np
import pytesseract
import re
import pandas as pd
from datetime import datetime, timedelta
import concurrent.futures
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io
import base64
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_HISTORY = 100
MONTHLY_BUDGET = 2000
MIN_AMOUNT = 0.01
MAX_AMOUNT = 10000

CATEGORIES = {
    "groceries": ["walmart", "kroger", "target", "costco", "aldi", "supermarket", "grocery", "food mart", "safeway", "publix"],
    "dining": ["restaurant", "cafe", "starbucks", "mcdonald", "kfc", "burger", "pizza", "food court", "chipotle", "subway"],
    "transport": ["uber", "lyft", "taxi", "bus", "train", "gas", "fuel", "petrol", "parking", "shell", "chevron"],
    "shopping": ["amazon", "best buy", "mall", "clothing", "shoe", "department", "zara", "uniqlo"],
    "entertainment": ["netflix", "spotify", "movie", "cinema", "theater", "concert", "hulu", "disney"],
    "utilities": ["electric", "water", "internet", "phone bill", "comcast", "at&t", "verizon"],
    "healthcare": ["pharmacy", "cvs", "walgreens", "doctor", "clinic", "medical", "rite aid"]
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

def preprocess_image(image):
    """Advanced preprocessing for better OCR"""
    img = np.array(image)
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img
    
    # Deskew (rotate to correct orientation)
    coords = np.column_stack(np.where(gray > 0))
    if len(coords) > 0:
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = 90 + angle
        if abs(angle) > 0.5:
            (h, w) = gray.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            gray = cv2.warpAffine(gray, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    
    # Apply thresholding
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Denoise
    denoised = cv2.medianBlur(thresh, 3)
    
    return denoised

class OCRReceiptExtractor:
    def __init__(self):
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    
    def extract(self, image):
        logger.info("Starting OCR extraction")
        
        try:
            processed = preprocess_image(image)
            text = pytesseract.image_to_string(processed, lang='eng')
            logger.info(f"OCR extracted {len(text)} characters")
            
            lines = text.split("\n")
            logger.info(f"Found {len(lines)} lines of text")
            
            # Extract store name (first non-empty, non-numeric line)
            store = None
            for line in lines[:10]:
                line_clean = line.strip()
                if len(line_clean) > 3 and not re.match(r'^[\d\W]+$', line_clean):
                    store = line_clean
                    break
            logger.info(f"Store name extracted: {store}")
            
            # Extract amounts using list accumulation (O(n) + O(n) max)
            amounts = []
            amount_pattern = r'\d+\.\d{2}'
            
            for line in lines:
                matches = re.findall(amount_pattern, line)
                for match in matches:
                    try:
                        val = float(match)
                        if MIN_AMOUNT <= val <= MAX_AMOUNT:
                            amounts.append(val)
                    except:
                        pass
            
            max_amount = max(amounts) if amounts else 0
            logger.info(f"Found {len(amounts)} amount candidates, max: {max_amount}")
            
            # Calculate confidence based on extraction quality
            confidence = 0.5
            if store:
                confidence += 0.2
            if max_amount > 0:
                confidence += 0.3
            confidence = min(confidence, 1.0)
            
            # Return structured result
            result = {
                "store_name": store,
                "total_amount": max_amount if max_amount > 0 else None,
                "category": categorize(store) if store else "other",
                "method": "ocr",
                "confidence": confidence,
                "status": "success" if max_amount > 0 else "partial",
                "message": f"Extracted: ${max_amount:.2f}" if max_amount > 0 else "Amount not found in receipt",
                "ocr_text_preview": text[:200]
            }
            
            logger.info(f"Extraction result: {result['status']} - {result['message']}")
            return result
                
        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
            return {
                "store_name": None,
                "total_amount": None,
                "category": "other",
                "method": "error",
                "confidence": 0.0,
                "status": "error",
                "message": f"OCR error: {str(e)[:100]}",
                "ocr_text_preview": ""
            }

extractor = OCRReceiptExtractor()

class HistoryManager:
    def __init__(self):
        self.history = []
        self.budget = MONTHLY_BUDGET

    def add(self, store, amount, category, confidence, method):
        if amount is None:
            return None
        
        transaction = {
            "date": datetime.now().isoformat(),
            "store": store or "Unknown Store",
            "amount": amount,
            "category": category,
            "confidence": confidence,
            "method": method
        }
        self.history.insert(0, transaction)
        if len(self.history) > MAX_HISTORY:
            self.history = self.history[:MAX_HISTORY]
        return transaction

    def clear(self):
        self.history = []
        self.budget = MONTHLY_BUDGET

    def get_summary(self):
        if not self.history:
            return {"total": 0, "count": 0, "by_category": {}, "budget_remaining": self.budget, "spent_this_month": 0}
        
        total = sum(t["amount"] for t in self.history)
        by_category = {}
        for t in self.history:
            cat = t["category"]
            by_category[cat] = by_category.get(cat, 0) + t["amount"]
        spent_this_month = total
        remaining = max(0, self.budget - spent_this_month)
        
        return {
            "total": total,
            "count": len(self.history),
            "by_category": by_category,
            "spent_this_month": spent_this_month,
            "budget_remaining": remaining
        }
    
    def get_daily_trend(self, days=30):
        if not self.history:
            return [], []
        
        cutoff = datetime.now() - timedelta(days=days)
        daily = {}
        
        for t in self.history:
            date = datetime.fromisoformat(t["date"]).date()
            if datetime.combine(date, datetime.min.time()) >= cutoff:
                daily[date] = daily.get(date, 0) + t["amount"]
        
        dates = sorted(daily.keys())
        amounts = [daily[d] for d in dates]
        return dates, amounts
    
    def get_category_pie_data(self):
        summary = self.get_summary()
        categories = list(summary["by_category"].keys())
        amounts = list(summary["by_category"].values())
        return categories, amounts
    
    def get_top_stores(self, limit=5):
        store_counts = {}
        for t in self.history:
            store = t["store"]
            store_counts[store] = store_counts.get(store, 0) + 1
        sorted_stores = sorted(store_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_stores[:limit]

history_state = gr.State(HistoryManager())

def process_single(image, state):
    """Process a single receipt image with debug logging"""
    logger.info("Button clicked - processing started")
    
    if image is None:
        logger.warning("No image provided")
        return {"error": "No image"}, '<div style="color:red">Please upload an image</div>', state
    
    result = extractor.extract(image)
    logger.info(f"Extraction result: {result}")
    
    if result["status"] == "success":
        state.add(
            result["store_name"], 
            result["total_amount"], 
            result["category"], 
            result["confidence"],
            result.get("method", "ocr")
        )
        status_html = f'<div style="color:green; padding:10px; background:#e8f5e9; border-radius:5px;">✓ Success: {result["message"]}</div>'
    elif result["status"] == "partial":
        status_html = f'<div style="color:#f39c12; padding:10px; background:#fff3cd; border-radius:5px;">⚠ Partial: {result["message"]}<br><small>Store: {result["store_name"] or "Not detected"}</small></div>'
    else:
        status_html = f'<div style="color:red; padding:10px; background:#ffebee; border-radius:5px;">✗ Error: {result["message"]}</div>'
    
    return result, status_html, state

def get_history_html(state):
    transactions = state.history
    if not transactions:
        return "<div style='text-align:center; padding:40px; color:#666;'>No transactions yet. Upload a receipt to get started.</div>"
    
    html = "<div style='max-height:500px; overflow-y:auto;'>"
    for t in transactions[:20]:
        date = datetime.fromisoformat(t["date"]).strftime("%Y-%m-%d %H:%M")
        conf_color = "#2ecc71" if t["confidence"] > 0.7 else "#f39c12"
        
        html += f"<div style='background:white; padding:12px; margin:8px 0; border-radius:8px; border-left:4px solid {conf_color}; box-shadow:0 1px 3px rgba(0,0,0,0.1);'>"
        html += f"<div><strong>{t['store'][:40]}</strong> <span style='float:right; font-weight:bold;'>${t['amount']:.2f}</span></div>"
        html += f"<div style='font-size:12px; color:#666; margin-top:4px;'>{t['category'].upper()} | {date} | Confidence: {t['confidence']:.0%}</div>"
        html += "</div>"
    html += "</div>"
    return html

def generate_trend_chart(state):
    dates, amounts = state.get_daily_trend(30)
    if not dates:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(dates, amounts, marker='o', linewidth=2, markersize=4, color='#2ecc71')
    ax.fill_between(dates, amounts, alpha=0.3, color='#2ecc71')
    ax.set_xlabel('Date', fontsize=10)
    ax.set_ylabel('Amount ($)', fontsize=10)
    ax.set_title('Daily Spending Trend (Last 30 Days)', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode()
    plt.close()
    
    return f'<img src="data:image/png;base64,{img_base64}" style="width:100%; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.1);">'

def generate_category_chart(state):
    categories, amounts = state.get_category_pie_data()
    if not categories:
        return None
    
    colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22']
    
    fig, ax = plt.subplots(figsize=(8, 6))
    wedges, texts, autotexts = ax.pie(amounts, labels=categories, autopct='%1.1f%%', 
                                        colors=colors[:len(categories)], startangle=90)
    ax.set_title('Spending by Category', fontsize=12, fontweight='bold')
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode()
    plt.close()
    
    return f'<img src="data:image/png;base64,{img_base64}" style="width:100%; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.1);">'

def get_dashboard_html(state):
    summary = state.get_summary()
    if summary["count"] == 0:
        return "<div style='text-align:center; padding:60px; color:#666;'>No transactions yet. Upload receipts to see insights.</div>"
    
    budget_percent = min(100, (summary["spent_this_month"] / state.budget * 100)) if state.budget > 0 else 0
    budget_color = "#e74c3c" if budget_percent > 90 else "#f39c12" if budget_percent > 70 else "#2ecc71"
    
    # Get top stores
    top_stores = state.get_top_stores(3)
    top_stores_html = ""
    for store, count in top_stores:
        top_stores_html += f"<div>{store[:25]}: {count} receipts</div>"
    
    # Generate charts
    trend_chart = generate_trend_chart(state)
    category_chart = generate_category_chart(state)
    
    html = f"""
    <div style="background:linear-gradient(135deg, #667eea, #764ba2); padding:20px; border-radius:10px; color:white; margin-bottom:20px;">
        <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:15px; text-align:center;">
            <div><strong>Total Spent</strong><br><span style="font-size:24px;">${summary['total']:.2f}</span></div>
            <div><strong>Transactions</strong><br><span style="font-size:24px;">{summary['count']}</span></div>
            <div><strong>Average</strong><br><span style="font-size:24px;">${summary['total']/summary['count']:.2f}</span></div>
        </div>
    </div>
    
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:20px;">
        <div style="background:white; padding:15px; border-radius:10px; box-shadow:0 1px 3px rgba(0,0,0,0.1);">
            <h3 style="margin-top:0;">Budget Progress</h3>
            <div style="font-size:14px;">Spent: ${summary['spent_this_month']:.2f} / ${state.budget:.2f}</div>
            <div style="background:#ddd; border-radius:10px; height:25px; margin-top:10px;">
                <div style="background:{budget_color}; width:{budget_percent:.0f}%; border-radius:10px; height:25px; text-align:center; color:white; line-height:25px;">
                    {budget_percent:.0f}%
                </div>
            </div>
            <div style="margin-top:10px;">Remaining: <strong>${summary['budget_remaining']:.2f}</strong></div>
        </div>
        <div style="background:white; padding:15px; border-radius:10px; box-shadow:0 1px 3px rgba(0,0,0,0.1);">
            <h3 style="margin-top:0;">Frequent Stores</h3>
            {top_stores_html if top_stores_html else '<div>No data yet</div>'}
        </div>
    </div>
    
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px;">
        <div style="background:white; padding:15px; border-radius:10px; box-shadow:0 1px 3px rgba(0,0,0,0.1);">
            <h3 style="margin-top:0;">Spending Trend</h3>
            {trend_chart if trend_chart else '<div style="text-align:center; padding:40px;">Insufficient data for trend</div>'}
        </div>
        <div style="background:white; padding:15px; border-radius:10px; box-shadow:0 1px 3px rgba(0,0,0,0.1);">
            <h3 style="margin-top:0;">Category Breakdown</h3>
            {category_chart if category_chart else '<div style="text-align:center; padding:40px;">Insufficient data for categories</div>'}
        </div>
    </div>
    """
    return html

def clear_history_handler(state):
    state.clear()
    return state, get_history_html(state), get_dashboard_html(state)

def export_csv_handler(state):
    if not state.history:
        return None
    df = pd.DataFrame(state.history)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"/tmp/export_{timestamp}.csv"
    df.to_csv(path, index=False)
    return path

def set_budget_handler(state, budget):
    if budget:
        state.budget = float(budget)
    return state, get_dashboard_html(state)

def refresh_history(state):
    return get_history_html(state)

def refresh_dashboard(state):
    return get_dashboard_html(state)

with gr.Blocks(title="Expense Tracker", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Expense Tracker")
    gr.Markdown("Upload receipts to track spending automatically")
    
    with gr.Row():
        with gr.Column(scale=1):
            image_input = gr.Image(type="pil", label="Upload Receipt", height=350)
            extract_btn = gr.Button("Extract Data", variant="primary", size="lg")
        with gr.Column(scale=1):
            output_json = gr.JSON(label="Extracted Data")
            output_message = gr.HTML(label="Status")
    
    with gr.Tabs():
        # DASHBOARD TAB FIRST
        with gr.TabItem("Dashboard"):
            dashboard_display = gr.HTML(label="Spending Dashboard")
            refresh_dashboard_btn = gr.Button("Refresh Dashboard")
            budget_input = gr.Number(label="Monthly Budget ($)", value=MONTHLY_BUDGET)
            budget_btn = gr.Button("Set Budget")
            
            refresh_dashboard_btn.click(
                fn=refresh_dashboard,
                inputs=[history_state],
                outputs=[dashboard_display]
            )
            budget_btn.click(
                fn=set_budget_handler,
                inputs=[history_state, budget_input],
                outputs=[history_state, dashboard_display]
            )
        
        # TRANSACTION HISTORY TAB
        with gr.TabItem("Transaction History"):
            history_display = gr.HTML(label="Recent Transactions")
            refresh_history_btn = gr.Button("Refresh History")
            with gr.Row():
                clear_btn = gr.Button("Clear History", variant="stop")
                export_btn = gr.Button("Export CSV", variant="secondary")
                export_file = gr.File(label="Download CSV")
            
            refresh_history_btn.click(
                fn=refresh_history,
                inputs=[history_state],
                outputs=[history_display]
            )
            clear_btn.click(
                fn=clear_history_handler,
                inputs=[history_state],
                outputs=[history_state, history_display, dashboard_display]
            )
            export_btn.click(
                fn=export_csv_handler,
                inputs=[history_state],
                outputs=[export_file]
            )
    
    # CORRECT WIRING FOR EXTRACT BUTTON
    extract_btn.click(
        fn=process_single,
        inputs=[image_input, history_state],
        outputs=[output_json, output_message, history_state]
    ).then(
        fn=refresh_history,
        inputs=[history_state],
        outputs=[history_display]
    ).then(
        fn=refresh_dashboard,
        inputs=[history_state],
        outputs=[dashboard_display]
    )
    
    demo.load(
        fn=lambda s: (refresh_history(s), refresh_dashboard(s)),
        inputs=[history_state],
        outputs=[history_display, dashboard_display]
    )
    
    gr.Markdown("---")
    gr.Markdown("All processing is local. OCR extraction completes in under one second. Check logs for debugging information.")

demo.launch(server_name="0.0.0.0", server_port=7860)
