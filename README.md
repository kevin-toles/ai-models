# AI Models

Model **storage repository** for the inference-service. Contains download scripts and actual model files (gitignored).

> **⚠️ Configuration Ownership**: All model configuration (metadata, runtime settings, presets) is owned by **inference-service**. This repo is storage-only.

## Structure

```
ai-models/
├── scripts/
│   └── download_models.py   # HuggingFace download helper (self-contained)
└── models/                  # GITIGNORED - actual .gguf files
    ├── phi-4/
    ├── deepseek-r1-7b/
    ├── qwen2.5-7b/
    ├── llama-3.2-3b/
    └── phi-3-medium-128k/
```

## Models

| Model | Size | Context | Role |
|-------|------|---------|------|
| phi-4 | 8.4GB | 16K | primary, thinker, coder |
| deepseek-r1-7b | 4.7GB | 32K | thinker |
| qwen2.5-7b | 4.5GB | 32K | coder, primary, fast |
| llama-3.2-3b | 2.0GB | 8K | fast |
| phi-3-medium-128k | 7.5GB | 128K | longctx, thinker |

**Total: ~27GB**

## Quick Start

### Download Models

```bash
# Ensure huggingface-cli is installed
pip install huggingface_hub

# Create model directories
mkdir -p models/{phi-4,deepseek-r1-7b,qwen2.5-7b,llama-3.2-3b,phi-3-medium-128k}

# Download each model
huggingface-cli download microsoft/phi-4-gguf phi-4-Q4_K_S.gguf --local-dir models/phi-4
huggingface-cli download unsloth/DeepSeek-R1-Distill-Qwen-7B-GGUF DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf --local-dir models/deepseek-r1-7b
huggingface-cli download Qwen/Qwen2.5-7B-Instruct-GGUF qwen2.5-7b-instruct-q4_k_m.gguf --local-dir models/qwen2.5-7b
huggingface-cli download hugging-quants/Llama-3.2-3B-Instruct-Q4_K_M-GGUF llama-3.2-3b-instruct-q4_k_m.gguf --local-dir models/llama-3.2-3b
huggingface-cli download microsoft/Phi-3-medium-128k-instruct-gguf Phi-3-medium-128k-instruct-Q4_K_M.gguf --local-dir models/phi-3-medium-128k
```

### Or Use Download Script

```bash
python scripts/download_models.py --all
# Or specific models:
python scripts/download_models.py --models phi-4 llama-3.2-3b
```

## Configuration

All model configuration is managed by **inference-service**:

```bash
# Point inference-service to this models directory
export INFERENCE_MODELS_DIR=/path/to/ai-models/models
export INFERENCE_CONFIG_DIR=/path/to/inference-service/config
```

See [inference-service/config/](https://github.com/kevin-toles/inference-service/tree/main/config) for:
- `models.yaml` - Model metadata, runtime settings (gpu_layers, context_length, roles)
- `presets.yaml` - 33 configuration presets (S1-S8, D1-D15, T1-T10, Q1-Q5, P1-P3)

## Related

- [inference-service](https://github.com/kevin-toles/inference-service) - Owns model configuration and runs inference
