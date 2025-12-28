# AI Models

Model storage repository for the inference-service. Contains configuration files and download scripts - actual model files are gitignored.

## Structure

```
ai-models/
├── config/
│   ├── models.yaml      # Model registry (metadata, sources, roles)
│   └── configs.yaml     # 33 configuration presets (S1-S5, D1-D10, T1-T10, Q1-Q5, P1-P3)
├── scripts/
│   └── download_models.py
└── models/              # GITIGNORED - actual .gguf files
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

## Configuration Presets

### By Model Count

| Category | Count | Example |
|----------|-------|---------|
| Single (S) | 5 | S1 = phi-4 only |
| Dual (D) | 10 | D3 = phi-4 + deepseek debate |
| Triple (T) | 10 | T1 = pipeline: llama→qwen→phi-4 |
| Quad (Q) | 5 | Q1 = four-way ensemble |
| Quint (P) | 3 | P1 = all five models |

### Mac 16GB Recommendations

| RAM Pressure | Configs |
|--------------|---------|
| Light | S1, S2, S4, D5, D7 |
| Medium | D1, D2, D4, D9, D10 |
| Full | T1, T3, T5, T10 |

See [configs.yaml](config/configs.yaml) for full details.

## Related

- [inference-service](https://github.com/kevin-toles/inference-service) - The service that uses these models
