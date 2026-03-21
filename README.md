# Privacy-First Personal Finance Agent

**Edge AI • Document Intelligence • Fully Local Inference**

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Kaggle](https://img.shields.io/badge/Kaggle-GPU%20Ready-blue.svg)](https://www.kaggle.com/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## What This Project Does

This system converts **unstructured receipt images → structured financial data → actionable insights** using a Vision-Language Model (VLM) — all while keeping data **100% private and local**.

**No APIs. No cloud calls. No data leakage.**

### Core Capabilities
- Extract store names, dates, line items, and total amounts
- Categorize expenses into 8 budget categories
- Generate financial insights and spending analytics
- Export to CSV, JSON, Excel, and professional visualizations
- Auto-save progress with intelligent checkpointing
- Cache model for instant loading on subsequent runs

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Privacy-First** | Fully offline inference — zero external API calls |
| **Efficient LLM** | 2B model with 4-bit quantization (6.7 GB VRAM) |
| **Production-Ready** | Checkpointing, error handling, multi-format exports |
| **Optimized** | 4 parallel workers → 20-30 images/minute |
| **Intelligent Caching** | Model cache saves 10+ minutes per session |

---

## Performance Metrics

| Metric | Value |
|--------|-------|
| Dataset | SROIE (973 receipts) |
| Model | Qwen2-VL-2B (2B parameters) |
| GPU | Tesla T4 / P100 (15-16 GB) |
| Avg Time per Receipt | 1.9-3.0 seconds |
| Total Processing Time | 35-50 minutes |
| Throughput | 20-30 images per minute |
| Store Name Accuracy | 89.9% |
| Total Amount Accuracy | 68.4% |
| Privacy Compliance | 100% Local |

---

## System Architecture

```
Receipt Images → Preprocessing → VLM Extraction → JSON Cleaning
→ Categorization → Analytics → Multi-Format Export
```

| Stage | Description |
|-------|-------------|
| **Data Loader** | Recursive dataset discovery, 973 receipts |
| **Preprocessing** | Resize 512px, EXIF correction, BILINEAR resampling |
| **Model Cache** | Persistent storage (1.5 GB model + 10 MB processor) |
| **VLM Extraction** | Qwen2-VL-2B, 4-bit NF4, 50 tokens, greedy decoding |
| **Post-Processing** | Regex parsing, field normalization |
| **Categorization** | 8 categories, 100+ keywords |
| **Analytics** | Spend trends, store analysis |
| **Export** | CSV, JSON, Excel, TXT, PNG |

---

## Optimization Results

| Optimization | Original | Optimized | Improvement |
|--------------|----------|-----------|-------------|
| Image Size | 1024px | 512px | 75% reduction |
| Generation Tokens | 512 | 50 | 90% reduction |
| Decoding | Beam Search | Greedy | 2x faster |
| Parsing | Full JSON | Regex | 50% faster |
| Workers | 1 | 4 | 4x throughput |
| **Combined** | 14s/image | **1.9-3.0s/image** | **75-85% faster** |

---

## Output Files

```
/kaggle/working/
├── extracted_receipts_all.csv          # Main extraction results
├── extracted_receipts_all.json         # Complete extraction data
├── extracted_receipts.xlsx             # Formatted Excel (7+ sheets)
├── receipt_insights.json               # Analytical insights
├── extraction_summary.txt              # Human-readable summary
├── financial_report.txt                # Financial analysis
├── store_analysis.txt                  # Store-wise analysis
├── performance_summary.json            # Performance metrics
├── FINAL_PROJECT_REPORT.txt            # Complete project report
├── receipt_visualizations.png          # Basic visualizations
├── performance_dashboard_enhanced.png  # Performance metrics
├── extraction_summary_chart.png        # Summary chart
├── model_cache/                        # Cached model (1.5 GB)
│   ├── model.pkl                       # Quantized model
│   └── processor.pkl                   # Tokenizer processor
└── checkpoint.pkl                      # Progress checkpoint
```

---

## Getting Started

### Prerequisites
- Python 3.9+
- GPU with 8+ GB VRAM (recommended)
- Kaggle account (optional, for notebook)

### Installation

```bash
# Clone the repository
git clone https://github.com/MrRogueKnight/privacy-first-personal-finance-agent.git
cd privacy-first-personal-finance-agent

# Install dependencies
pip install -r requirements.txt
```

### Usage

**Option A: Kaggle Notebook (Recommended)**

1. Open the notebook on Kaggle
2. Enable GPU accelerator
3. Run all cells sequentially

**Option B: Local Python Script**

```bash
python main.py --input_dir /path/to/images --output_dir ./outputs
```

---

## Project Structure

```
privacy-first-personal-finance-agent/
├── notebooks/
│   └── privacy_first_receipt_extractor.ipynb
├── outputs/                          # Generated output files
├── src/
│   ├── data_loader.py                # SROIE dataset loader
│   ├── extractor.py                  # VLM wrapper with caching
│   ├── pipeline.py                   # Processing with checkpointing
│   ├── analyzer.py                   # Analytics and categorization
│   └── utils.py                      # Helper functions
├── cache/
│   └── model_cache/                  # Cached model
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| GPU memory crashes | Aggressive cleanup: `gc.collect()`, `torch.cuda.empty_cache()` |
| Model compatibility | Switched to Qwen2-VL-2B with eager attention |
| Malformed JSON outputs | Multi-stage sanitization with regex fallbacks |
| Progress loss on interruption | Checkpoint system (auto-save every 20 images) |
| Re-downloading model | Model caching to persistent storage |

---

## Future Improvements

### Short-term
- AI-based categorization with zero-shot classification
- Confidence scoring for extractions
- Precision/Recall/F1 evaluation metrics
- Micro-batching for throughput optimization

### Long-term
- Fine-tuning on receipt datasets
- Multi-language support
- Streamlit / FastAPI interface
- ONNX / TensorRT optimization
- Mobile deployment

---

## Team

| Role | Name |
|------|------|
| Team Lead | Prashant Ranjan |
| Developer | Ritik Prajapati |
| ML Engineer | Rayapurreadyy Hema Sundhar |
| Data Analyst | Grihshant Manas Datta |

---

## License

MIT License — see [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [Kaggle](https://www.kaggle.com/) for GPU resources
- [HuggingFace](https://huggingface.co/) for Transformers library
- [ICDAR](https://rrc.cvc.uab.es/?ch=13) for SROIE dataset
- [Qwen Team](https://qwenlm.github.io/) for the vision-language model

---

<p align="center">
  <b>Privacy-First AI • Edge Deployment • Document Intelligence</b>
</p>
