# 1. vLLM-based OpenAI-Compatible Inference Server on Kubernetes (Qwen)

1.1 GPU-backed vLLM inference server for Qwen deployed on Kubernetes with persistent model storage and an OpenAI-compatible API.

---

# 2. Overview & Motivation

2.1 This project demonstrates how to deploy a **self-hosted large language model** using **vLLM** with an **OpenAI-compatible API**, running on **Kubernetes**.

2.2 The primary goal is to focus on:

   2.2.1 Inference reliability  
   2.2.2 GPU efficiency  
   2.2.3 Deployment correctness  

2.3 The system is designed to be:

   2.3.1 Reproducible  
   2.3.2 Infrastructure-aware  
   2.3.3 Model-agnostic at the serving layer  

2.4 The project is intentionally minimal, emphasizing **real execution over architectural slides**.

---

# 3. System Architecture

## 3.1 Architecture Layers

3.1.1 The system consists of the following layers:

   3.1.1.1 **Inference Engine** – vLLM OpenAI API server  
   3.1.1.2 **Model Layer** – Qwen Instruct checkpoints from HuggingFace  
   3.1.1.3 **Container Layer** – Docker image encapsulating runtime dependencies  
   3.1.1.4 **Orchestration Layer** – Kubernetes Deployment + Service  
   3.1.1.5 **Storage Layer** – PersistentVolumeClaim mounted at `/root/models-hf` for persistent model weight storage  

3.1.2 The API surface is compatible with OpenAI-style endpoints, enabling drop-in replacement for downstream consumers.

## 3.2 High-Level Flow

3.2.1 Client sends request to Kubernetes Service.  
3.2.2 Traffic is routed to the vLLM Pod.  
3.2.3 vLLM loads model weights from the persistent volume (or downloads once).  
3.2.4 GPU-backed inference is executed.  
3.2.5 OpenAI-compatible JSON response is returned.  

---

# 4. Repository Structure

4.1 Project directory layout:

```
vllm-qwen-kubernetes/
├── Dockerfile
├── server.py
├── README.md
└── k8s/
    ├── pvc-hf-cache.yaml
    ├── qwen-vllm-config.yaml
    ├── qwen-vllm-deploy.yaml
    └── qwen-vllm-svc.yaml
```

---

# 5. Proof of Execution

5.1 The system has been:

   5.1.1 Built locally using Docker  
   5.1.2 Deployed on a Kubernetes cluster  
   5.1.3 Verified via live API requests  

5.2 Model weights are successfully loaded and cached.

5.3 Inference requests return valid OpenAI-compatible responses.

5.4 No mock components are used. All manifests correspond to running workloads.

---

# 6. Kubernetes Deployment Details

## 6.1 Deployment Characteristics

6.1.1 Single-replica GPU-backed Pod.  
6.1.2 PersistentVolumeClaim mounted at `/root/models-hf`.  
6.1.3 Environment-driven configuration via ConfigMap.  
6.1.4 Explicit GPU resource requests to avoid overcommit.  

## 6.2 Service Exposure

6.2.1 Internal ClusterIP (default).  
6.2.2 Can be upgraded to NodePort or LoadBalancer without code changes.  

---

# 7. How to Run

## 7.1 Build Docker Image

7.1.1 Run:

```bash
docker build -t vllm-qwen:latest .
```

## 7.2 Deploy to Kubernetes

7.2.1 Create persistent storage:

```bash
kubectl apply -f k8s/pvc-hf-cache.yaml
```

7.2.2 Apply configuration:

```bash
kubectl apply -f k8s/qwen-vllm-config.yaml
```

7.2.3 Deploy inference server:

```bash
kubectl apply -f k8s/qwen-vllm-deploy.yaml
```

7.2.4 Expose service:

```bash
kubectl apply -f k8s/qwen-vllm-svc.yaml
```

## 7.3 Send Test Request

7.3.1 Execute:

```bash
curl http://<SERVICE_IP>:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen2.5-0.5B-Instruct",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

---

# 8. Design Decisions & Constraints

## 8.1 Why vLLM

8.1.1 Efficient KV-cache management.  
8.1.2 Better GPU memory utilization under constrained VRAM.  
8.1.3 Production-grade inference semantics.  
8.1.4 Native OpenAI-compatible API support.  

## 8.2 Persistent Model Storage

8.2.1 PersistentVolumeClaim used instead of container-layer caching.  
8.2.2 Custom mount path `/root/models-hf`.  
8.2.3 Prevents hidden container-layer cache behavior.  
8.2.4 Ensures deterministic storage control across Pod restarts.  
8.2.5 Reduces cold-start latency.  

## 8.3 Model-Agnostic Serving Layer

8.3.1 Model name injected via configuration.  
8.3.2 Weights can be swapped without rebuilding infrastructure.  
8.3.3 Serving layer remains unchanged when models change.  

## 8.4 Inference-Only Scope

8.4.1 Training intentionally excluded.  
8.4.2 Fine-tuning intentionally excluded.  
8.4.3 Runtime remains lean and deployment-focused.  

## 8.5 Single Replica by Design

8.5.1 Emphasizes correctness before scale.  
8.5.2 Horizontal scaling intentionally deferred.  
8.5.3 Architecture supports scaling without structural changes.  

---

# 9. Integration Possibilities

9.1 This service is designed to act as:

   9.1.1 A backend inference microservice.  
   9.1.2 A drop-in OpenAI API replacement.  

9.2 It can be integrated into:

   9.2.1 Agent frameworks.  
   9.2.2 RAG pipelines.  
   9.2.3 Internal tooling requiring LLM access.  

9.3 Authentication, routing, rate-limiting, and observability are expected to be handled by upstream infrastructure.

---

# 10. Notes

10.1 This project prioritizes:

   10.1.1 Correctness.  
   10.1.2 Reproducibility.  
   10.1.3 Real execution.  

10.2 All components in this repository:

   10.2.1 Are running.  
   10.2.2 Are validated.  
   10.2.3 Reflect actual deployment artifacts.  

10.3 Polish is intentionally secondary to clarity and system integrity.
