#!/usr/bin/env python3
"""Test script for the ML Inference API"""

import requests
import argparse
import time
from pathlib import Path


def test_health(api_url="http://localhost:8000"):
    """Test health endpoint"""
    print(f"\n{'='*60}")
    print("Testing Health Endpoint")
    print(f"{'='*60}")
    
    try:
        response = requests.get(f"{api_url}/api/health/", timeout=10)
        if response.status_code == 200:
            print(f"✅ Health check passed")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_inference(image_path, api_url="http://localhost:8000", confidence=0.5):
    """Test inference endpoint"""
    print(f"\n{'='*60}")
    print("Testing Inference Endpoint")
    print(f"{'='*60}")
    
    if not Path(image_path).exists():
        print(f"❌ Image not found: {image_path}")
        return False
    
    try:
        print(f"📸 Testing with image: {image_path}")
        print(f"📊 Confidence threshold: {confidence}")
        
        with open(image_path, 'rb') as f:
            files = {'image': f}
            data = {'confidence': confidence}
            
            start = time.time()
            response = requests.post(
                f"{api_url}/api/inference/",
                files=files,
                data=data,
                timeout=300
            )
            elapsed = time.time() - start
            
            if response.status_code == 200:
                result = response.json()
                print(f"\n✅ Inference successful (took {elapsed:.2f}s)")
                print(f"Status: {result.get('status')}")
                print(f"Message: {result.get('message')}")
                print(f"Request ID: {result.get('request_id')}")
                print(f"Inference time: {result.get('inference_time')}s")
                
                if result.get('detections'):
                    print(f"\n🎯 Detections found:")
                    for i, det in enumerate(result['detections'], 1):
                        print(f"  {i}. {det['class_name']} (confidence: {det['confidence']:.2f})")
                else:
                    print("\n  No objects detected")
                
                return True
            else:
                print(f"❌ Inference failed ({response.status_code})")
                print(f"Response: {response.text}")
                return False
    
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to API at {api_url}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_history(api_url="http://localhost:8000"):
    """Test history endpoint"""
    print(f"\n{'='*60}")
    print("Testing History Endpoint")
    print(f"{'='*60}")
    
    try:
        response = requests.get(f"{api_url}/api/history/?limit=5", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ History retrieved")
            print(f"Status: {result.get('status')}")
            print(f"Count: {result.get('count')}")
            return True
        else:
            print(f"❌ Failed ({response.status_code})")
            return False
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Test ML Inference API')
    parser.add_argument('--image', type=str, help='Image file for inference test')
    parser.add_argument('--api-url', type=str, default='http://localhost:8000', help='API base URL')
    parser.add_argument('--confidence', type=float, default=0.5, help='Confidence threshold')
    parser.add_argument('--health', action='store_true', help='Test health endpoint')
    parser.add_argument('--all', action='store_true', help='Test all endpoints')
    
    args = parser.parse_args()
    
    if not args.image and not args.all and not args.health:
        args.health = True
    
    results = []
    
    if args.health or args.all:
        results.append(test_health(args.api_url))
    
    if args.image or args.all:
        if args.image:
            results.append(test_inference(args.image, args.api_url, args.confidence))
    
    if args.all:
        results.append(test_history(args.api_url))
    
    print(f"\n{'='*60}")
    print(f"Summary: {sum(results)}/{len(results)} passed")
    print(f"{'='*60}\n")
    
    return 0 if all(results) else 1


if __name__ == '__main__':
    exit(main())
