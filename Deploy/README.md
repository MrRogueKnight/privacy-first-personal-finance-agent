---
title: Privacy-First Receipt Extractor
emoji: 🧾
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# Privacy-First Receipt Extractor

Extract receipt data with 100% local inference. Your images never leave the server.

## Features
- Store name extraction
- Total amount extraction
- Local processing - no API calls
- Privacy-first design

## How to Use
1. Upload a receipt image (JPG, PNG)
2. Click "Extract Data"
3. View extracted information

## Technical Details
- Model: Qwen2-VL-2B (4-bit quantized)
- Framework: PyTorch, Transformers, Gradio
- Inference: 100% local

## Privacy Guarantee
This Space runs entirely on Hugging Face infrastructure. Your images are processed locally and never shared with any external service.

---

Built with Hugging Face Spaces, Docker, and Gradio
