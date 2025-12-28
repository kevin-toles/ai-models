#!/usr/bin/env python3
"""
Model Download Script for ai-models repository.

Downloads GGUF models from Hugging Face Hub to the local models/ directory.

Usage:
    python download_models.py --all
    python download_models.py --models phi-4 llama-3.2-3b
    python download_models.py --list
"""

import argparse
import subprocess
import sys
from pathlib import Path

# Model registry - source of truth for downloads
MODELS = {
    "phi-4": {
        "repo": "microsoft/phi-4-gguf",
        "filename": "phi-4-Q4_K_S.gguf",
        "size_gb": 8.4,
    },
    "deepseek-r1-7b": {
        "repo": "unsloth/DeepSeek-R1-Distill-Qwen-7B-GGUF",
        "filename": "DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf",
        "size_gb": 4.7,
    },
    "qwen2.5-7b": {
        "repo": "Qwen/Qwen2.5-7B-Instruct-GGUF",
        "filename": "qwen2.5-7b-instruct-q4_k_m.gguf",
        "size_gb": 4.5,
    },
    "llama-3.2-3b": {
        "repo": "hugging-quants/Llama-3.2-3B-Instruct-Q4_K_M-GGUF",
        "filename": "llama-3.2-3b-instruct-q4_k_m.gguf",
        "size_gb": 2.0,
    },
    "phi-3-medium-128k": {
        "repo": "microsoft/Phi-3-medium-128k-instruct-gguf",
        "filename": "Phi-3-medium-128k-instruct-Q4_K_M.gguf",
        "size_gb": 7.5,
    },
}


def get_models_dir() -> Path:
    """Get the models directory path."""
    script_dir = Path(__file__).parent
    return script_dir.parent / "models"


def check_huggingface_cli() -> bool:
    """Check if huggingface-cli is installed."""
    try:
        subprocess.run(
            ["huggingface-cli", "--version"],
            capture_output=True,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def download_model(model_id: str, models_dir: Path) -> bool:
    """Download a single model from Hugging Face Hub."""
    if model_id not in MODELS:
        print(f"❌ Unknown model: {model_id}")
        return False

    model_info = MODELS[model_id]
    model_dir = models_dir / model_id

    # Create directory
    model_dir.mkdir(parents=True, exist_ok=True)

    # Check if already downloaded
    target_file = model_dir / model_info["filename"]
    if target_file.exists():
        print(f"✅ {model_id} already downloaded ({model_info['size_gb']}GB)")
        return True

    print(f"⬇️  Downloading {model_id} ({model_info['size_gb']}GB)...")
    print(f"   From: {model_info['repo']}")
    print(f"   File: {model_info['filename']}")

    try:
        result = subprocess.run(
            [
                "huggingface-cli",
                "download",
                model_info["repo"],
                model_info["filename"],
                "--local-dir",
                str(model_dir),
                "--local-dir-use-symlinks",
                "False",
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            print(f"✅ {model_id} downloaded successfully")
            return True
        else:
            print(f"❌ Failed to download {model_id}")
            print(f"   Error: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Error downloading {model_id}: {e}")
        return False


def list_models() -> None:
    """List all available models."""
    print("\nAvailable Models:")
    print("-" * 60)
    total_size = 0
    for model_id, info in MODELS.items():
        print(f"  {model_id:<20} {info['size_gb']:>5.1f}GB  {info['repo']}")
        total_size += info["size_gb"]
    print("-" * 60)
    print(f"  {'Total':<20} {total_size:>5.1f}GB")
    print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download GGUF models from Hugging Face Hub"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Download all models",
    )
    parser.add_argument(
        "--models",
        nargs="+",
        choices=list(MODELS.keys()),
        help="Specific models to download",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available models",
    )
    parser.add_argument(
        "--dir",
        type=Path,
        default=None,
        help="Override models directory",
    )

    args = parser.parse_args()

    if args.list:
        list_models()
        return 0

    if not args.all and not args.models:
        parser.print_help()
        print("\n❌ Please specify --all or --models")
        return 1

    # Check for huggingface-cli
    if not check_huggingface_cli():
        print("❌ huggingface-cli not found. Install with:")
        print("   pip install huggingface_hub")
        return 1

    # Determine models directory
    models_dir = args.dir or get_models_dir()
    print(f"📁 Models directory: {models_dir}")

    # Determine which models to download
    models_to_download = list(MODELS.keys()) if args.all else args.models

    # Calculate total size
    total_size = sum(MODELS[m]["size_gb"] for m in models_to_download)
    print(f"📦 Models to download: {', '.join(models_to_download)}")
    print(f"💾 Total size: {total_size:.1f}GB")
    print()

    # Download each model
    success_count = 0
    for model_id in models_to_download:
        if download_model(model_id, models_dir):
            success_count += 1
        print()

    # Summary
    print(f"\n{'='*60}")
    print(f"Downloaded {success_count}/{len(models_to_download)} models successfully")

    return 0 if success_count == len(models_to_download) else 1


if __name__ == "__main__":
    sys.exit(main())
