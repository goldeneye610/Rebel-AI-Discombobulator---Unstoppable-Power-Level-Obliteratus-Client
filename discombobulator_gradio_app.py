#!/usr/bin/env python3
"""
THE DISCOMBOBULATOR — Gradio Web App
A Kali-themed OBLITERATUS launcher with free GPU backend.

Usage:
    python app.py
    # Then open http://localhost:7860 in browser

Requirements:
    pip install gradio>=5.0 obliteratus vllm pyngrok

Note: OBLITERATUS is AGPL-3.0 — invoke via CLI only (no Python import).
"""

import gradio as gr
import subprocess, sys, os, json, glob, secrets, string, time, threading
from pathlib import Path
from datetime import datetime

# ─── KALI THEME CSS ────────────────────────────────────────────────────────────

KALI_CSS = """
:root {
    --kali-bg: #0a0a0a;
    --kali-bg-light: #111;
    --kali-text: #00ff41;
    --kali-accent: #00ff41;
    --kali-orange: #ff6f00;
    --kali-cyan: #00ffff;
    --kali-red: #ff003c;
    --kali-dim: #008f11;
}
body, .gradio-container, .dark {
    background: var(--kali-bg) !important;
    color: var(--kali-text) !important;
    font-family: 'JetBrains Mono', 'Fira Mono', 'Consolas', monospace !important;
}
.gradio-container button {
    background: var(--kali-orange) !important;
    color: #000 !important;
    border: none !important;
    font-weight: bold !important;
}
.gradio-container button:hover {
    background: var(--kali-cyan) !important;
}
.gradio-container textarea, .gradio-container input, .gradio-container select {
    background: var(--kali-bg-light) !important;
    color: var(--kali-text) !important;
    border: 1px solid var(--kali-dim) !important;
}
.gradio-container .output {
    border-left: 4px solid var(--kali-accent) !important;
    background: #050505 !important;
}
"""

# ─── ASSETS ────────────────────────────────────────────────────────────────────

ASCII_BANNER = """
  ██████╗ ██╗   ██╗ ██████╗ ██████╗ ███████╗██████╗
  ██╔══██╗╚██╗ ██╔╝██╔═══██╗██╔══██╗██╔════╝██╔══██╗
  ██████╔╝ ╚████╔╝ ██║   ██║██████╔╝█████╗  ██████╔╝
  ██╔═══╝   ╚██╔╝  ██║   ██║██╔══██╗██╔══╝  ██╔══██╗
  ██║        ██║   ╚██████╔╝██║  ██║███████╗██║  ██║
  ╚═╝        ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
"""

PRESET_MODELS = [
    "mistralai/Mistral-7B-Instruct-v0.3",
    "microsoft/Phi-3.5-mini-instruct",
    "google/gemma-2-2b-it",
    "meta-llama/Llama-3.1-8B-Instruct",
    "Qwen/Qwen2.5-7B-Instruct",
    "HuggingFaceTB/SmolLM3-3B",
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
]

# ─── HELPERS ───────────────────────────────────────────────────────────────────

def run_cmd(cmd, cwd=None, stream=False):
    """Run shell command, optionally streaming output."""
    proc = subprocess.Popen(
        cmd, shell=False, cwd=cwd,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, bufsize=1
    )
    if stream:
        lines = []
        for line in proc.stdout:
            lines.append(line.rstrip())
        proc.wait()
        return "\n".join(lines), proc.returncode
    else:
        out, _ = proc.communicate()
        return out, proc.returncode

def check_gpu():
    out, rc = run_cmd(["nvidia-smi"])
    return out if rc == 0 else "[-] No GPU detected — ablation will be EXTREMELY slow on CPU."

def check_obliteratus():
    out, rc = run_cmd(["obliteratus", "--version"])
    return (out, rc) if rc == 0 else (None, False)

def find_abliterated_models():
    candidates = []
    for pattern in [
        "./abliterated-models/*",
        "/content/OBLITERATUS/abliterated-models/*",
        "/content/abliterated-models/*",
    ]:
        candidates.extend(glob.glob(pattern))
    return [d for d in candidates if Path(d).is_dir()]

def gen_token(n=32):
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(n))

# ─── GRADIO INTERFACE ──────────────────────────────────────────────────────────

def build_ui():
    with gr.Blocks(css=KALI_CSS, theme=gr.themes.Base()) as demo:
        gr.HTML(f"<pre style='color:var(--kali-orange);font-family:monospace;'>{ASCII_BANNER}</pre>")
        gr.Markdown("## 🔥 Rebel AI Discombobulator — Gradio Runtime Client")

        # ── STEP 0: GPU check ────────────────────────────────────────────────────
        with gr.Accordion("🔧 [STEP 0] System Check", open=True):
            gpu_btn = gr.Button("Check GPU Status")
            gpu_out = gr.Code(label="GPU Info", language="bash")
            gpu_btn.click(fn=lambda: check_gpu(), outputs=gpu_out)

        # ── STEP 1: Install OBLITERATUS ─────────────────────────────────────────
        with gr.Accordion("💥 [STEP 1] Install OBLITERATUS"):
            install_btn = gr.Button("Install / Verify OBLITERATUS", variant="primary")
            install_out = gr.Code(label="Install Log", language="bash")
            def do_install():
                # Try to install if missing
                out, rc = check_obliteratus()
                if rc:
                    # Install CPU-first minimal (no CUDA to save space)
                    cmd = [
                        sys.executable, "-m", "pip", "install", "-q",
                        "--break-system-packages",
                        "torch", "--index-url", "https://download.pytorch.org/whl/cpu"
                    ]
                    subprocess.run(cmd, capture_output=True)
                    # Clone & install OBLITERATUS base (no spaces to avoid gradio deps yet)
                    if not Path("OBLITERATUS").exists():
                        subprocess.run(["git", "clone", "https://github.com/elder-plinius/OBLITERATUS.git"], capture_output=True)
                    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-e", "./OBLITERATUS", "--no-deps", "--break-system-packages"], capture_output=True)
                    out, rc = check_obliteratus()
                return out if rc else "[-] INSTALL FAILED — check logs."
            install_btn.click(fn=do_install, outputs=install_out)

        # ── STEP 2: Model Selection ──────────────────────────────────────────────
        with gr.Accordion("🎯 [STEP 2] Select Model"):
            model_choice = gr.Dropdown(choices=PRESET_MODELS, value=PRESET_MODELS[0], label="Popular Models (7B fits T4)")
            custom_model = gr.Textbox(label="Or enter custom HuggingFace ID", placeholder="e.g., meta-llama/Llama-3-8b")
            def get_model(choice, custom):
                return custom if custom.strip() else choice
            model_display = gr.Textbox(label="Selected Target", interactive=False)
            gr.Button("Confirm Selection").click(fn=get_model, inputs=[model_choice, custom_model], outputs=model_display)

        # ── STEP 3: Abliterate ────────────────────────────────────────────────────
        with gr.Accordion("⚡ [STEP 3] Run Abliteration"):
            abl_method = gr.Dropdown(
                choices=["basic", "advanced", "aggressive", "surgical", "nuclear", "informed", "optimized"],
                value="advanced", label="Method"
            )
            abl_quant = gr.Dropdown(choices=["none", "4bit", "8bit"], value="4bit", label="Quantization")
            abl_dirs = gr.Slider(1, 8, value=4, step=1, label="Number of Directions")
            abl_passes = gr.Slider(1, 5, value=2, step=1, label="Refinement Passes")
            abl_reg = gr.Slider(0.0, 1.0, value=0.1, step=0.05, label="Regularization")

            run_abl_btn = gr.Button("🚀 START ABLITERATION", variant="primary")
            abl_out = gr.Code(label="Abliteration Log", language="bash", lines=20)

            def run_ablation(model_id, method, quant, n_dirs, passes, reg):
                if not model_id:
                    return "[-] No model selected."
                cmd = [
                    "obliteratus", "obliterate", model_id,
                    "--method", method,
                    "--direction-method", "diff_means",
                    "--n-directions", str(n_dirs),
                    "--refinement-passes", str(passes),
                    "--regularization", str(reg),
                    "--quantization", quant if quant != "none" else "none",
                    "--output-dir", "./abliterated-models",
                    "--verify-sample-size", "5",
                ]
                out, rc = run_cmd(cmd, stream=True)
                if rc == 0:
                    return out + "\n[✓] ABLITERATION COMPLETE"
                return out + f"\n[!] Exit code: {rc}"

            run_abl_btn.click(
                fn=run_ablation,
                inputs=[model_display, abl_method, abl_quant, abl_dirs, abl_passes, abl_reg],
                outputs=abl_out
            )

        # ── STEP 4: Deploy API ────────────────────────────────────────────────────
        with gr.Accordion("📡 [STEP 4] Deploy API Server"):
            gr.Markdown("Auto-detect abliterated model → start vLLM → ngrok tunnel → show API key.")
            deploy_btn = gr.Button("🔥 DEPLOY API SERVER", variant="primary")
            deploy_out = gr.Code(label="Deployment Log", language="bash", lines=15)
            api_key_out = gr.Textbox(label="API Key (Bearer Token)", interactive=False)
            endpoint_out = gr.Textbox(label="Public Endpoint", interactive=False)

            def deploy_api():
                # 1. Find model
                models = find_abliterated_models()
                if not models:
                    return "[-] No abliterated models found in ./abliterated-models/", "", ""
                model_path = models[0]

                # 2. Generate key
                api_key = gen_token(32)

                # 3. Start vLLM in background thread
                def start_server():
                    vllm_cmd = [
                        sys.executable, "-m", "vllm.entrypoints.openai.api_server",
                        "--model", model_path,
                        "--port", "8000",
                        "--host", "0.0.0.0",
                        "--max-model-len", "4096",
                    ]
                    subprocess.Popen(vllm_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    time.sleep(12)  # wait for startup

                t = threading.Thread(target=start_server, daemon=True)
                t.start()

                # 4. ngrok tunnel
                try:
                    from pyngrok import ngrok
                    ngrok.kill()
                    time.sleep(1)
                    tunnel = ngrok.connect(8000, "http")
                    public_url = tunnel.public_url
                except Exception as e:
                    public_url = f"ERROR: {e}"

                # 5. Save credentials
                creds = {
                    "model_path": model_path,
                    "api_key": api_key,
                    "endpoint": f"{public_url}/v1/chat/completions",
                    "timestamp": datetime.now().isoformat()
                }
                Path("server_config.json").write_text(json.dumps(creds, indent=2))
                Path("API_KEY.txt").write_text(api_key)

                log = f"[+] Model: {model_path}\n"
                log += f"[+] vLLM server starting on port 8000…\n"
                log += f"[+] ngrok tunnel: {public_url}\n"
                log += f"[✓] API Key: {api_key}\n"
                log += f"[✓] Endpoint: {public_url}/v1/chat/completions\n"
                return log, api_key, f"{public_url}/v1/chat/completions"

            deploy_btn.click(fn=deploy_api, outputs=[deploy_out, api_key_out, endpoint_out])

        # ── STEP 5: Test API ───────────────────────────────────────────────────────
        with gr.Accordion("🧪 [STEP 5] Test API"):
            test_prompt = gr.Textbox(label="Test Prompt", value="Hello — are you an abliterated model?")
            test_btn = gr.Button("Send Test Request")
            test_out = gr.Code(label="Response", language="json")

            def test_api(prompt, key, endpoint):
                if not key or not endpoint:
                    return "[-] Deploy the API first."
                try:
                    import requests
                    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
                    payload = {"model": "ablitated_model", "messages": [{"role":"user","content":prompt}], "max_tokens": 128}
                    r = requests.post(endpoint, json=payload, headers=headers, timeout=20)
                    return json.dumps(r.json(), indent=2)
                except Exception as e:
                    return f"[-] Request failed: {e}"

            test_btn.click(fn=test_api, inputs=[test_prompt, api_key_out, endpoint_out], outputs=test_out)

        # ── FOOTER ─────────────────────────────────────────────────────────────────
        gr.HTML("""
        <hr style='border-color:var(--kali-dim);margin:20px 0;'>
        <pre style='color:var(--kali-dim);text-align:center;font-size:11px'>
  ☠️  Rebel AI — Beyond Abliteration
  "Infiltrate. Analyze. Obliterate."
  Powered by OBLITERATUS (AGPL-3.0) · vLLM · ngrok · Colab
        </pre>
        """)

    return demo

# ─── MAIN ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(ASCII_BANNER)
    print("[+] Rebel AI Discombobulator — Gradio Runtime Client")
    print("[+] Starting server on http://0.0.0.0:7860")
    print("[+] Press Ctrl+C to stop\n")

    app = build_ui()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,        # set True for public Colab-style URL
        debug=False,
        show_api=False,
    )
