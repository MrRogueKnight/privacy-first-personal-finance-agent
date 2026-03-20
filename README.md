# 🧾 Privacy-First Receipt Extractor
## Edge AI-Powered Document Intelligence

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Kaggle](https://img.shields.io/badge/Kaggle-GPU%20Ready-blue.svg)](https://www.kaggle.com/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> A production-ready, privacy-first receipt extraction system using local Vision-Language Models (VLM) with GPU acceleration. Process receipts entirely offline without external API calls.

---

## 📋 Table of Contents
- [🚀 Key Features](#-key-features)
- [🏃 Quick Start](#-quick-start)
- [🏗️ System Architecture](#️-system-architecture)
- [📦 Installation](#-installation)
- [💻 Usage Guide](#-usage-guide)
- [📊 Performance Metrics](#-performance-metrics)
- [📁 Project Structure](#-project-structure)
- [🔒 Privacy & Security](#-privacy--security)
- [👥 Team](#-team)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🚀 Key Features

| Feature | Description |
|--------|------------|
| 🔒 **Privacy-First** | 100% local processing, no external API calls |
| ⚡ **GPU Accelerated** | Optimized for Tesla T4/P100 (6.7GB VRAM) |
| 🧠 **Advanced AI** | Qwen2-VL-2B-Instruct with 4-bit quantization |
| 📊 **Smart Analytics** | Automatic expense categorization and insights |
| 📁 **Multi-format Export** | CSV, JSON, TXT, and visualization reports |
| 🎯 **High Accuracy** | ~93% extraction success rate |

---

## 🏃 Quick Start

```bash
git clone https://github.com/MrRogueKnight/privacy-first-personal-finance-agent.git
cd privacy-first-personal-finance-agent

pip install -r requirements.txt

python src/main.py --input data/sample_receipts/ --output results/

cat results/extraction_summary.txt
```

---

## 🏗️ System Architecture

```text
Data Loading 
   ↓
Image Preprocessing 
   ↓
VLM Extraction 
   ↓
JSON Parsing 
   ↓
Expense Categorization 
   ↓
Export & Visualization
```

---

## 📦 Installation

### Prerequisites

* Python 3.9+
* CUDA GPU (recommended)
* Kaggle or local setup

### Local Setup

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

## 💻 Usage Guide

### Basic Usage

```python
from src.extractor import ReceiptExtractor
from src.categorizer import ExpenseCategorizer

extractor = ReceiptExtractor(
    model_name="Qwen/Qwen2-VL-2B-Instruct",
    quantization="4bit",
    device="cuda"
)

receipt_data = extractor.process_receipt("receipt.jpg")

categorizer = ExpenseCategorizer()
categorized = categorizer.categorize(receipt_data)

extractor.export_results(categorized, format="csv")
```

---

## 📊 Performance Metrics

| Metric         | Value           |
| -------------- | --------------- |
| Total Receipts | 100             |
| Success Rate   | 93%             |
| Avg Time       | 12.65 sec/image |
| GPU Usage      | 39%             |
| VRAM           | 6.7 GB          |

---

## 📁 Project Structure

```text
src/
 ├── extractor.py
 ├── categorizer.py
 ├── model_manager.py
 ├── exporter.py
 └── utils.py
```

---

## 🔒 Privacy & Security

* No external API calls
* Fully local processing
* GDPR-ready
* Secure memory handling

---

## 👥 Team

| Role         | Name                       | Contribution                           |
| ------------ | -------------------------- | -------------------------------------- |
| Team Lead    | Prashant Ranjan            | System design, integration, deployment |
| Developer    | Ritik Prajapati            | Pipeline, GPU optimization, VLM        |
| ML Engineer  | Rayapurreadyy Hema Sundhar | Model optimization, quantization       |
| Data Analyst | Grihshant Manas Datta      | Categorization, analytics              |

---

## 🤝 Contributing

```bash
git clone https://github.com/MrRogueKnight/privacy-first-personal-finance-agent.git
pip install -r requirements-dev.txt
pytest
```

---

## 📄 License

MIT License

---

## ⭐ Support

* ⭐ Star the repo
* 🍴 Fork it
* 📢 Share it

---

<div align="center">
Made with ❤️ by Team Privacy-First AI
</div>
```