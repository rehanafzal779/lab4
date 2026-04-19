#!/usr/bin/env python3
"""
Model management script
Downloads or configures YOLOv8 models for the ML inference API
"""

import os
import sys
import argparse
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.conf import settings
from ultralytics import YOLO


def download_model(model_name='yolov8m'):
    """Download a YOLOv8 model"""
    logger.info(f"Downloading YOLOv8 {model_name} model...")
    try:
        model = YOLO(f'{model_name}.pt')
        logger.info(f"✅ Model {model_name} downloaded successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to download model: {str(e)}")
        return False


def list_available_models():
    """List available YOLOv8 models"""
    models = ['yolov8n', 'yolov8s', 'yolov8m', 'yolov8l', 'yolov8x']
    print("\nAvailable YOLOv8 Models:")
    print("=" * 50)
    print("n (nano)   - Fastest, smallest (~13 MB)")
    print("s (small)  - Fast, small (~27 MB)")
    print("m (medium) - Balanced (~49 MB) [RECOMMENDED]")
    print("l (large)  - Slow, large (~99 MB)")
    print("x (xlarge) - Slowest, largest (~168 MB)")
    print("\nUse: python manage_model.py --download yolov8n")
    print("=" * 50 + "\n")


def check_model(model_path):
    """Check if a model file exists and is valid"""
    if not os.path.exists(model_path):
        logger.warning(f"Model not found at {model_path}")
        return False
    
    try:
        model = YOLO(model_path)
        logger.info(f"✅ Model is valid: {model_path}")
        logger.info(f"   Model: {model.names}")
        return True
    except Exception as e:
        logger.error(f"❌ Model is invalid: {str(e)}")
        return False


def main():
    parser = argparse.ArgumentParser(description='YOLOv8 Model Management')
    parser.add_argument('--download', type=str, default='yolov8m',
                       help='Download a model (default: yolov8m)')
    parser.add_argument('--list', action='store_true', help='List available models')
    parser.add_argument('--check', type=str, help='Check if model file is valid')
    parser.add_argument('--info', action='store_true', help='Show model info')
    
    args = parser.parse_args()
    
    if args.list:
        list_available_models()
        return 0
    
    if args.check:
        return 0 if check_model(args.check) else 1
    
    if args.info:
        logger.info(f"Base DIR: {settings.BASE_DIR}")
        logger.info(f"ML Model Path: {settings.ML_MODEL_PATH}")
        logger.info(f"DEBUG: {settings.DEBUG}")
        logger.info(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        return 0
    
    # Download model
    return 0 if download_model(args.download) else 1


if __name__ == '__main__':
    sys.exit(main())
