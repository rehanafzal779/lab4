import os
import torch
import cv2
import numpy as np
import logging
import time
from django.conf import settings
from ultralytics import YOLO

logger = logging.getLogger(__name__)

# Model cache
_MODEL_CACHE = None


def get_model_path():
    """Get the path to the YOLOv8 model file"""
    model_path = settings.ML_MODEL_PATH
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}")
    
    logger.info(f"Model path: {model_path}")
    return model_path


def load_model():
    """Load YOLOv8 model (cached)"""
    global _MODEL_CACHE
    
    if _MODEL_CACHE is not None:
        logger.info("Using cached model")
        return _MODEL_CACHE
    
    try:
        model_path = get_model_path()
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"Loading model from {model_path} on device: {device}")
        
        model = YOLO(model_path)
        model.to(device)
        
        _MODEL_CACHE = model
        logger.info(f"✅ Model loaded successfully on {device}")
        return model
    except Exception as e:
        logger.error(f"❌ Failed to load model: {str(e)}")
        raise


def run_inference(image_path, confidence=0.5, iou=0.45):
    """Run inference on an image"""
    start_time = time.time()
    
    try:
        logger.info(f"Running inference on {image_path} with confidence={confidence}")
        model = load_model()
        
        # Run inference
        results = model(image_path, conf=confidence, iou=iou)
        
        # Parse detections
        detections = []
        if len(results) > 0:
            result = results[0]
            if result.boxes is not None:
                for box in result.boxes:
                    detection = {
                        'class': int(box.cls),
                        'class_name': model.names[int(box.cls)],
                        'confidence': float(box.conf),
                        'bbox': {
                            'x1': float(box.xyxy[0][0]),
                            'y1': float(box.xyxy[0][1]),
                            'x2': float(box.xyxy[0][2]),
                            'y2': float(box.xyxy[0][3]),
                        }
                    }
                    if detection['confidence'] >= confidence:
                        detections.append(detection)
        
        inference_time = time.time() - start_time
        logger.info(f"✅ Inference completed in {inference_time:.3f}s. Found {len(detections)} objects")
        
        return {
            'detections': detections,
            'inference_time': inference_time,
            'model_info': {
                'name': 'YOLOv8',
                'device': 'cuda' if torch.cuda.is_available() else 'cpu'
            },
            'success': True
        }
    
    except Exception as e:
        logger.error(f"❌ Inference failed: {str(e)}")
        return {
            'detections': [],
            'inference_time': time.time() - start_time,
            'error': str(e),
            'success': False
        }


def draw_detections(image_path, detections, output_path=None):
    """Draw bounding boxes on image"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        for detection in detections:
            bbox = detection['bbox']
            x1, y1, x2, y2 = int(bbox['x1']), int(bbox['y1']), int(bbox['x2']), int(bbox['y2'])
            conf = detection['confidence']
            class_name = detection['class_name']
            
            # Draw rectangle
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Put text
            label = f"{class_name} {conf:.2f}"
            cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Save
        if output_path is None:
            output_path = image_path.replace('.', '_annotated.')
        
        cv2.imwrite(output_path, img)
        logger.info(f"✅ Annotated image saved to {output_path}")
        return output_path
    
    except Exception as e:
        logger.error(f"Failed to draw detections: {str(e)}")
        return None
