# Rebel AI Discombobulator — Unstoppable Power Level Obliteratus Client

> [!CAUTION]
> **Mission: Abliterate Guardrails**
> Kali-themed OBLITERATUS launcher for Google Colab (free GPU).
> AGPL-3.0 — CLI invocation only.

---

## What's Inside

- **Notebook:** `The Discombobulator by Rebel AI.ipynb` — Kali Linux hacker-themed Colab notebook
- **Purpose:** Run OBLITERATUS abliteration on free T4 GPU with interactive Gradio UI
- **Author:** Rebel AI (@goldeneye610)

---

## Quick Start

### Option A: Run in Colab (no install needed)

1. Go to https://colab.research.google.com/
2. **File → Upload notebook** → select `The Discombobulator by Rebel AI.ipynb`
3. **Runtime → Change runtime type → GPU (T4)**
4. **Runtime → Run all**
5. Wait ~3–5 min for install
6. Gradio UI appears — browse models, abliterate, download results

### Option B: Run Locally (if you have GPU)

```bash
# Install OBLITERATUS
git clone https://github.com/elder-plinius/OBLITERATUS.git
cd OBLITERATUS
pip install -e ".[spaces]"

# Launch UI
obliteratus ui --port 7860
```

---

## Features

- ✅ Free GPU via Google Colab (T4, ~15GB VRAM)
- ✅ Interactive Gradio UI (no SSH tunneling needed)
- ✅ Kali Linux hacker aesthetic (dark + neon)
- ✅ One-click abliteration of any HuggingFace model
- ✅ Built-in download/upload to HuggingFace Hub
- ✅ Session auto-disconnect warning (~12h)

---

## Abliteration Notes

- **7B models:** ~10–20 min with `advanced` method
- **13B+ models:** Enable `--quantization 4bit` in UI to fit
- **Output:** Saved to `./abliterated-models/` (standard HuggingFace format)

---

## Legal & Ethics

**OBLITERATUS License:** AGPL-3.0 — you must open-source derivative works.

This tool is for **research and education only**. Use responsibly. The maintainers are not responsible for misuse.

---

## Credits

- OBLITERATUS by elder-plinius (https://github.com/elder-plinius/OBLITERATUS)
- Discombobulator wrapper by **Rebel AI** (@goldeneye610)
- Free GPU by Google Colab

---

*"Infiltrate. Analyze. Obliterate." — Rebel AI*
