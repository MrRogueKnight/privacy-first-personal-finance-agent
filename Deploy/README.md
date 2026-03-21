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
- OCR-based receipt extraction with deskew and preprocessing
- Store name detection
- Amount extraction using list accumulation (O(n) algorithm)
- Automatic categorization (7 categories)
- Real-time spending charts
- Daily trend visualization
- Category breakdown pie chart
- Budget tracking with progress bar
- CSV export
- Debug logging for troubleshooting

## How to Use
1. Upload a receipt image
2. Click Extract Data
3. View extracted information
4. Check Dashboard for charts and insights

## Technical Details
- OCR: Tesseract with image preprocessing (deskew, thresholding, denoise)
- Algorithm: O(n) scanning for amounts, O(n) max finding
- Charts: Matplotlib with Agg backend (memory efficient)
- Storage: Session-based in-memory

## Privacy
All processing is local. No external API calls.
