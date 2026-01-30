import os
import subprocess

MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-0.5B-Instruct")
MAX_MODEL_LEN = os.getenv("MAX_MODEL_LEN", "512")
DTYPE = os.getenv("DTYPE", "float16")
GPU_MEM_UTIL = os.getenv("GPU_MEMORY_UTILIZATION", "0.70")
MAX_NUM_SEQS = os.getenv("MAX_NUM_SEQS", "1")
PORT = os.getenv("PORT", "8080")

cmd = [
    "python3",
    "-m",
    "vllm.entrypoints.openai.api_server",
    "--model", MODEL_NAME,
    "--host", "0.0.0.0",
    "--port", PORT,

    "--dtype", DTYPE,
    "--max-model-len", MAX_MODEL_LEN,
    "--gpu-memory-utilization", GPU_MEM_UTIL,
    "--max-num-seqs", MAX_NUM_SEQS,

    "--swap-space", "1",
    "--enforce-eager",
]

print("Starting vLLM with:", " ".join(cmd))
subprocess.run(cmd, check=True)
