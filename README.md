vLLM-based OpenAI-Compatible Inference Server on Kubernetes (Qwen)
=================================================================

---

2. Overview & Motivation
------------------------

1. This project demonstrates how to deploy a **self-hosted large language model** using **vLLM** with an **OpenAI-compatible API**, running on **Kubernetes**.
2. The primary goal is to focus on **inference reliability, GPU efficiency, and deployment correctness**, rather than model training.
3. The system is designed to be:
   1. Reproducible
   2. Infrastructure-aware
   3. Model-agnostic at the serving layer
4. The project is intentionally minimal, emphasizing **real execution over architectural slides**.

---

3. System Architecture
----------------------

1. The system consists of the following layers:
   1. **Inference Engine**: vLLM OpenAI API server
   2. **Model Layer**: Qwen Instruct checkpoints from HuggingFace
   3. **Container Layer**: Docker image encapsulating runtime dependencies
   4. **Orchestration Layer**: Kubernetes Deployment + Service
   5. **Storage Layer**: PersistentVolumeClaim for HuggingFace cache
2. The API surface is compatible with OpenAI-style endpoints, enabling drop-in replacement for downstream consumers.

High-level flow:

1. Client sends request to Kubernetes Service
2. Traffic is routed to vLLM Pod
3. vLLM loads model weights from cached volume (or downloads once)
4. GPU-backed inference is executed
5. OpenAI-compatible JSON response is returned

---

4. Repository Structure
-----------------------

.
├── Dockerfile # Builds the vLLM inference container
├── server.py # Starts the vLLM OpenAI-compatible server
├── pvc-hf-cache.yaml # PersistentVolumeClaim for HuggingFace cache
├── qwen-vllm-config.yaml # ConfigMap for model and runtime parameters
├── qwen-vlllm-deploy.yaml # Kubernetes Deployment (GPU-enabled)
├── qwen-vllm-svc.yaml # Kubernetes Service exposing the API

---

5. Proof of Execution
---------------------

1. The system has been:
   1. Built locally using Docker
   2. Deployed on a Kubernetes cluster
   3. Verified via live API requests
2. Model weights are successfully loaded and cached.
3. Inference requests return valid OpenAI-compatible responses.
4. No mock components are used; all manifests correspond to running workloads.

---

6. Kubernetes Deployment Status
-------------------------------

1. Deployment characteristics:
   1. Single-replica GPU-backed Pod
   2. PersistentVolumeClaim mounted at `/root/models-hf` for model weight storage
   3. Environment-driven configuration via ConfigMap
2. Service exposure:
   1. Internal ClusterIP (default)
   2. Can be upgraded to NodePort / LoadBalancer without code changes
3. Resource usage is explicitly controlled to avoid GPU overcommit.

---

7. How to Run (High Level)
--------------------------

### 7.1 Build Image

```bash
docker build -t vllm-qwen:latest .
```

### 7.2 Deploy to Kubernetes

Create persistent storage:

```bash
kubectl apply -f pvc-hf-cache.yaml
```

Apply configuration:

```bash
kubectl apply -f qwen-vllm-config.yaml
```

Deploy inference server:

```bash
kubectl apply -f qwen-vlllm-deploy.yaml
```

Expose service:

```bash
kubectl apply -f qwen-vllm-svc.yaml
```

### 7.3 Send Test Request

```bash
curl http://<SERVICE_IP>:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen2.5-0.5B-Instruct",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

---

8. Design Decisions & Constraints (Senior Signal Section)
---------------------------------------------------------

**Chose vLLM for:**

- Efficient KV-cache management
- Better GPU memory utilization under constrained VRAM
- Production-grade inference semantics

**Validated locally before cluster deployment:**

- Docker-based local testing
- Kubernetes manifests tested on a local cluster (e.g., Minikube)

**Serving layer is model-agnostic:**

- Model name is injected via configuration
- Weights can be swapped without rebuilding infrastructure

**Inference-only scope:**

- Training and fine-tuning are explicitly out of scope
- This keeps the runtime lean and deployment-focused

**Persistent cache chosen over init downloads:**

- Reduces cold-start latency
- Avoids repeated network dependency
- Custom model mount path chosen over default HF cache path
Explicit mount (/root/models-hf) prevents hidden container-layer caching behavior and ensures deterministic storage control across Pod restarts.

**Single-replica by design:**

- Emphasizes correctness first
- Scaling is deferred intentionally

---

9. Relation to a Larger System
------------------------------

This service is designed to act as:

- A backend inference microservice
- A drop-in OpenAI API replacement

It can be integrated into:

- Agent frameworks
- RAG pipelines
- Internal tooling requiring LLM access

Authentication, routing, and rate-limiting are expected to be handled by upstream services.

---


11. Notes
---------

This project prioritizes:

- Correctness
- Reproducibility
- Real execution

All components included in this repository:

- Are running
- Are validated
- Reflect actual deployment artifacts

Polish is intentionally secondary to clarity and system integrity.

---



