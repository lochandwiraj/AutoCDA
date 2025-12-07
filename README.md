# AutoCDA - AI Circuit Design Assistant

> Transform natural language into KiCad circuit schematics with AI

## Overview

AutoCDA converts plain English circuit descriptions into production-ready KiCad netlists. Describe what you want, and get working circuits with calculated component values in seconds.

**Example:**
```
Input:  "Design a low-pass RC filter with 1kHz cutoff frequency"
Output: Complete KiCad netlist with calculated components
Time:   ~5 seconds
```

## Features

- 🤖 **AI-Powered** - Natural language processing via Claude 3.5 Sonnet
- ⚡ **Fast** - Generate circuits in 5-10 seconds
- 🎯 **Accurate** - Component values within 7% tolerance
- 📐 **Smart Calculations** - Automatic component selection from standard series
- 📊 **Detailed Explanations** - Step-by-step math showing how values were chosen
- 🎨 **Modern UI** - Beautiful React interface with animations
- 🔌 **KiCad Ready** - Direct integration with KiCad 9.0+

## Supported Circuits

- RC Low-Pass Filter
- RC High-Pass Filter  
- Voltage Divider

## Quick Start

### Prerequisites

- Python 3.14+
- Node.js 18+
- OpenRouter API key ([Get one](https://openrouter.ai/))

### Installation

```bash
# Clone repository
git clone <repo-url>
cd autocda-mvp

# Install Python dependencies
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Install frontend dependencies
cd client
npm install
cd ..
```

### Running

**Terminal 1 - Backend:**
```bash
set OPENROUTER_API_KEY=your-key-here
python backend/api.py
```

**Terminal 2 - Frontend:**
```bash
cd client
npm run dev
```

Open http://localhost:5173

## Usage

1. Enter your circuit description (e.g., "Design a 1kHz low-pass filter")
2. Click Generate
3. View detailed calculations and explanation
4. Download KiCad netlist
5. Open in KiCad to view/edit schematic

## API

### POST /generate
```json
{
  "prompt": "Design a low-pass RC filter with 1kHz cutoff"
}
```

### Response
```json
{
  "success": true,
  "explanation": "Detailed explanation with calculations...",
  "download_url": "/download/circuit_abc/circuit.zip"
}
```

## Tech Stack

**Backend:**
- Python 3.14
- Flask (REST API)
- SKiDL (Circuit generation)
- Claude 3.5 Sonnet (AI)

**Frontend:**
- React 18
- Vite
- Custom animations

## Project Structure

```
autocda-mvp/
├── backend/           # Python API and circuit generation
├── client/            # React frontend
├── prompts/           # AI prompt templates
├── output/            # Generated circuits
└── tests/             # Test suite
```

## Testing

```bash
python test_complete_system.py
```

## License

MIT License - see LICENSE file

## Acknowledgments

- SKiDL - Circuit description language
- KiCad - Open-source EDA
- OpenRouter - AI API gateway
- Anthropic Claude - NLP engine

---

**Status:** Production Ready ✅  
**Version:** 2.0.0
