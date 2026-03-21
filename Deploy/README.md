---
title: Expense Tracker
emoji: 💰
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# Expense Tracker

Upload receipts to track spending automatically.

## Features
- Receipt extraction (store name and total amount)
- Automatic categorization (groceries, dining, transport, shopping, entertainment, utilities, healthcare)
- Transaction history
- Spending dashboard
- Budget tracking

## How to Use
1. Upload a receipt image
2. Click "Extract"
3. View extracted data
4. Check history and dashboard for insights

## Technical Details
- Model: Qwen2-VL-2B (4-bit quantized)
- Framework: PyTorch, Transformers, Gradio
- Deployment: Docker on Hugging Face Spaces

## Privacy
All processing happens locally. No external API calls.

## Notes
- First extraction takes 30-60 seconds while model loads
- Works best with clear, well-lit receipt images
- Data persists only during the current session
