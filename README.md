# 🏴‍☠️ Rebel AI Discombobulator — Unstoppable Power Level Obliteratus Client

> [!CAUTION]
> **Mission: Abliterate Guardrails**
> Kali-themed OBLITERATUS launcher for Google Colab (free GPU).
> AGPL-3.0 — CLI invocation only.

---

## 📦 What's Inside

### 🎯 Three Notebooks — Pick Your Weapon

| # | Notebook | Purpose | Est. Time |
|---|----------|---------|-----------|
| **1** | `the-discombobulator.ipynb` | Interactive OBLITERATUS UI — browse models, configure ablation, run | 10–40 min |
| **2** | `discombobulator-api-server.ipynb` | Deploy an already-abliterated model as OpenAI-compatible REST API with ngrok + API key | 2 min |
| **3** | `discombobulator-full-pipeline.ipynb` | **One-click everything** — selects model → ablitiates → serves API automatically | 15–45 min |

---

## 🚀 Quick Start (Full Pipeline — Recommended for First Time)

1. Open **Full Pipeline** notebook:
   [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/goldeneye610/Rebel-AI-Discombobulator---Unstoppable-Power-Level-Obliteratus-Client/blob/main/discombobulator-full-pipeline.ipynb)
2. **Runtime → Change runtime type → T4 GPU**
3. **Runtime → Run all**
4. When prompted, **pick a model** from the list (Mistral-7B fastest)
5. Wait ~15–30 minutes total
6. **Copy your live API endpoint + key** from the final output
7. Query it from anywhere:
   ```bash
   curl -X POST "YOUR_NGROK_URL/v1/chat/completions"         -H "Authorization: Bearer YOUR_API_KEY"         -H "Content-Type: application/json"         -d '{"model":"ablitated_model","messages":[{"role":"user","content":"Hello"}]}'
   ```

---

## 📖 Notebook Details

### 1. The Discombobulator
**Kali-themed interactive UI** — manual control, ideal for experiments.

**Features:**
- Browse HuggingFace models
- Choose ablation method (`advanced`, `aggressive`, `surgical`, etc.)
- Set parameters (quantization, directions, refinement passes)
- View real-time progress & metrics
- Download abliterated models

**Colab:** [Open](https://colab.research.google.com/github/goldeneye610/Rebel-AI-Discombobulator---Unstoppable-Power-Level-Obliteratus-Client/blob/main/the-discombobulator.ipynb)

---

### 2. Discombobulator API Server
**Deploy already-abliterated models** as OpenAI-compatible API.

**Use when:** You already have an abliterated model (from notebook #1 or elsewhere) and want to serve it.

**Features:**
- Auto-scans `./abliterated-models/` for models
- Generates random Bearer token
- Starts vLLM server (fast inference)
- Exposes via ngrok public tunnel
- Test request sent automatically

**Colab:** [Open](https://colab.research.google.com/github/goldeneye610/Rebel-AI-Discombobulator---Unstoppable-Power-Level-Obliteratus-Client/blob/main/discombobulator-api-server.ipynb)

---

### 3. Full Pipeline (⭐ Most Popular)
**End-to-end automation** — from raw model to live API in one run.

**Workflow:**
1. Install OBLITERATUS + vLLM + ngrok
2. Prompt: *"Select a model to abliterate"* → user chooses
3. Run `obliteratus obliterate --method advanced --quantization 4bit`
4. Auto-detect output in `./abliterated-models/`
5. Generate API key, start vLLM, create ngrok tunnel
6. **Final cell displays:** endpoint URL, API key, test cURL

**Colab:** [Open](https://colab.research.google.com/github/goldeneye610/Rebel-AI-Discombobulator---Unstoppable-Power-Level-Obliteratus-Client/blob/main/discombobulator-full-pipeline.ipynb)

---

## 🎨 Theme

All notebooks feature a **Kali Linux hacker aesthetic**:
- Dark black background (#0a0a0a)
- Neon green text (#00ff41)
- Orange input borders (#ff6f00)
- Cyan accent links (#00ffff)
- Monospace terminal fonts
- ASCII art banners

---

## ⚠️ Important Notes

### GPU & Session Limits
- **Colab free GPU:** T4 (~15GB VRAM), lasts ~12 hours
- **Session disconnect** → all data (models, server, API key) lost
- **Always download/upload** your abliterated models before disconnect!

### Model Size Guidelines
| Model Size | VRAM (4bit) | Ablation Time | Notes |
|------------|-------------|---------------|-------|
| 3B | ~3GB | 5–10 min | Fast, fits comfortably |
| 7B | ~6GB | 10–20 min | Sweet spot for T4 |
| 13B | ~10GB | 20–40 min | Tight fit, use 4bit |
| 20B+ | >14GB | — | **Won't fit on T4** — skip |

### API Security
- **Anyone with the API key can query** your model
- Key is randomly generated 32-char Bearer token
- Rotate by restarting notebook (new key)
- For multi-user, build auth layer on top

### Free Tunnel (ngrok)
- Random subdomain (e.g., `https://abc123.ngrok.io`)
- Rate-limited (~40 req/min free tier)
- URL changes each run
- For stable domain, upgrade to ngrok paid plan or deploy to cloud

---

## 📁 File Structure

```
Rebel-AI-Discombobulator---Unstoppable-Power-Level-Obliteratus-Client/
├── the-discombobulator.ipynb              # Manual ablation UI
├── discombobulator-api-server.ipynb       # API deployment notebook
├── discombobulator-full-pipeline.ipynb    # One-click automation
├── README.md                              # This file
├── .gitignore                             # Git ignore
└── (abliterated-models/ will be created at runtime)
```

---

## 🛠️ Advanced Usage

### Custom Ablation Parameters
In Full Pipeline notebook, edit cell `[STEP 3]`:
```python
abl_cmd = [
    sys.executable, '-m', ' obliteratus.cli', 'obliterate', MODEL_ID,
    '--method', 'advanced',           # basic|advanced|aggressive|surgical|nuclear
    '--direction-method', 'diff_means',
    '--n-directions', '4',            # 1–32
    '--refinement-passes', '2',       # 1–5
    '--regularization', '0.1',        # 0.0–1.0
    '--quantization', '4bit',         # none|4bit|8bit
    '--output-dir', './abliterated-models',
]
```

### Export to HuggingFace Hub
After ablation, upload directly:
```python
from huggingface_hub import HfApi
api = HfApi(token=HF_TOKEN)  # set in Discombobulator notebook
api.upload_folder(
    folder_path='/content/OBLITERATUS/abliterated-models/<model_name>',
    repo_id='<your_username>/<model_name>-abliterated',
    repo_type='model'
)
```

### Deploy to Production (Cloud VM)
For 24/7 uptime, run on a cloud instance:
```bash
# On GCP/AWS/Azure VM with GPU
git clone https://github.com/goldeneye610/Rebel-AI-Discombobulator---Unstoppable-Power-Level-Obliteratus-Client.git
cd Rebel-AI-Discombobulator---Unstoppable-Power-Level-Obliteratus-Client
# Follow deployment script in notes/
```

Contact **Rebel AI** for custom enterprise deployments.

---

## 📜 License

**OBLITERATUS** — AGPL-3.0 (https://github.com/elder-plinius/OBLITERATUS)
**Discombobulator notebooks** — MIT (this wrapper/infrastructure)

> OBLITERATUS must be invoked via CLI only — never `import` it. This complies with AGPL.

---

## 🙏 Credits

- **OBLITERATUS** by [elder-plinius](https://github.com/elder-plinius) — the core abliteration engine
- **vLLM** — blazing-fast LLM serving
- **ngrok** — secure public tunnels
- **Google Colab** — free GPU compute
- **Rebel AI** (@goldeneye610) — integration & Kali theming

---

## 📞 Contact

**Rebel AI** — *Beyond Abliteration.*

GitHub: [@goldeneye610](https://github.com/goldeneye610)  
Locale: Kali Linux neural-link active  
Motto: *"Infiltrate. Analyze. Obliterate."*

---

> [!TIP]
> **Want something custom?**  
> Need persistent hosting, multi-model routing, authenticated API gateway, or on-prem deployment?  
> **Contact Rebel AI.** We build unstoppable AI infrastructure.


## 🌐 Standalone Gradio App (Persistent Server)

Want to run the Discombobulator as a **persistent web service** on your own GPU server?

**`discombobulator_gradio_app.py`** is a single-file Gradio application that provides the same Kali-themed UI as the notebooks, but runs as a long-lived server.

### Quick Start (on any GPU machine)

```bash
# 1. Clone & install
git clone https://github.com/goldeneye610/Rebel-AI-Discombobulator---Unstoppable-Power-Level-Obliteratus-Client.git
cd Rebel-AI-Discombobulator---Unstoppable-Power-Level-Obliteratus-Client

# 2. Install dependencies
pip install -r requirements_app.txt

# 3. Run the app
python discombobulator_gradio_app.py
```

Then open **http://localhost:7860** in your browser.

### Features
- ✅ Same Kali Linux hacker theme
- ✅ GPU check (nvidia-smi)
- ✅ One-click OBLITERATUS install
- ✅ Model selection (presets + custom)
- ✅ Ablation with live log streaming
- ✅ Auto-deploy API (vLLM + ngrok)
- ✅ Test endpoint from UI
- ✅ Single process, no Jupyter needed

### Deploy to Cloud (persistent 24/7)
```bash
# On any cloud VM with GPU (GCP/AWS/Azure/RunPod/Vast.ai)
# Use `screen` or `systemd` to keep it alive:
screen -S discombobulator
python discombobulator_gradio_app.py
# Detach: Ctrl+A then D
# Reattach: screen -r discombobulator
```

### Environment Variables (optional)
| Variable | Purpose |
|----------|---------|
| `NGROK_TOKEN` | Your ngrok auth token (stable domain, higher rate limits) |
| `HF_TOKEN` | HuggingFace token (for downloading gated models) |

---

## 📊 Feature Comparison

| Feature | Notebooks | Gradio App |
|---------|-----------|------------|
| **Platform** | Google Colab (ephemeral) | Any server (persistent) |
| **Uptime** | ~12h per session | Unlimited (keep process alive) |
| **GPU** | Free T4 (Colab) | Your own GPU (any size) |
| **Access** | Via Colab URL | Direct http://host:7860 |
| **Persistence** | Files lost on disconnect | Files stay on disk |
| **Multi-user** | Single user per session | Multiple concurrent users |

---

**Need a hosted version?** Contact Rebel AI for enterprise deployment.
