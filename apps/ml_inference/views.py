from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from django.conf import settings

from .models import InferenceRequest
from .serializers import InferenceRequestSerializer
from .inference_utils import run_inference, draw_detections
import logging

logger = logging.getLogger(__name__)


class InferenceAPIView(APIView):
    """Run inference on uploaded image"""
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        try:
            if 'image' not in request.FILES:
                return Response(
                    {'error': 'No image provided'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            image_file = request.FILES['image']
            confidence = float(request.data.get('confidence', 0.5))
            save_result = request.data.get('save_result', 'true').lower() == 'true'
            
            if not 0 <= confidence <= 1:
                return Response(
                    {'error': 'Confidence must be between 0 and 1'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Save uploaded file
            temp_path = default_storage.save(
                f'uploads/{image_file.name}',
                ContentFile(image_file.read())
            )
            full_path = os.path.join(settings.MEDIA_ROOT, temp_path)
            
            # Run inference
            inference_result = run_inference(full_path, confidence=confidence)
            
            if not inference_result['success']:
                return Response(
                    {'error': inference_result.get('error', 'Inference failed')},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Create record
            inference_req = InferenceRequest.objects.create(
                user=request.user if request.user.is_authenticated else None,
                image=temp_path,
                detections=inference_result['detections'],
                confidence_threshold=confidence
            )
            
            # Draw detections if requested
            result_image_url = None
            if save_result and inference_result['detections']:
                result_path = draw_detections(
                    full_path,
                    inference_result['detections'],
                    os.path.join(settings.MEDIA_ROOT, 'results', f'result_{inference_req.id}.png')
                )
                if result_path:
                    relative_result = os.path.relpath(result_path, settings.MEDIA_ROOT)
                    inference_req.result_image = relative_result
                    inference_req.save()
                    result_image_url = default_storage.url(relative_result)
            
            # Response
            response_data = {
                'status': 'success',
                'request_id': inference_req.id,
                'detections': inference_result['detections'],
                'confidence_threshold': confidence,
                'image_url': default_storage.url(temp_path),
                'result_image_url': result_image_url,
                'inference_time': round(inference_result['inference_time'], 3),
                'model_info': inference_result['model_info'],
                'message': f'Found {len(inference_result["detections"])} objects'
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"API error: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HistoryAPIView(APIView):
    """Get inference history"""
    
    def get(self, request):
        try:
            limit = int(request.query_params.get('limit', 10))
            
            if request.user.is_authenticated:
                requests = InferenceRequest.objects.filter(user=request.user)[:limit]
            else:
                requests = InferenceRequest.objects.all()[:limit]
            
            serializer = InferenceRequestSerializer(requests, many=True)
            return Response({
                'status': 'success',
                'count': len(serializer.data),
                'results': serializer.data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"History error: {str(e)}")
            return Response({'error': 'Failed to fetch history'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DetailAPIView(APIView):
    """Get specific inference details"""
    
    def get(self, request, request_id):
        try:
            inference_req = InferenceRequest.objects.get(id=request_id)
            
            if inference_req.user and inference_req.user != request.user and not request.user.is_staff:
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = InferenceRequestSerializer(inference_req)
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
        
        except InferenceRequest.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Detail error: {str(e)}")
            return Response({'error': 'Failed to fetch details'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
