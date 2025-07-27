import requests
import time
import base64
import os
import jwt
import asyncio
import httpx
from typing import Optional, Dict, Any
from PIL import Image
import io

class KlingAIClient:
    """
    KlingAI API client for virtual try-on functionality
    Uses the working Singapore endpoint implementation
    """

    def __init__(self, access_key: Optional[str] = None, secret_key: Optional[str] = None):
        """
        Initialize KlingAI client

        Args:
            access_key: KlingAI Access Key
            secret_key: KlingAI Secret Key
        """
        self.access_key = access_key or os.getenv('KLING_ACCESS_KEY')
        self.secret_key = secret_key or os.getenv('KLING_SECRET_KEY')

        if not self.access_key or not self.secret_key:
            raise ValueError("KlingAI credentials are required. Set KLING_ACCESS_KEY and KLING_SECRET_KEY environment variables")

        # KlingAI API configuration (working Singapore endpoint)
        self.base_url = "https://api-singapore.klingai.com"
        self.model_name = "kolors-virtual-try-on-v1-5"

    def _encode_jwt_token(self) -> str:
        """Generate JWT token for KlingAI API authentication"""
        headers = {
            "alg": "HS256",
            "typ": "JWT"
        }
        payload = {
            "iss": self.access_key,
            "exp": int(time.time()) + 1800,  # Expires in 30 minutes
            "nbf": int(time.time()) - 5      # Not before (5 seconds ago)
        }
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        return token

    def _get_auth_headers(self) -> Dict[str, str]:
        """Get headers with fresh JWT token"""
        token = self._encode_jwt_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def _prepare_image(self, image_data: str) -> str:
        """
        Prepare and encode image for KlingAI API

        Args:
            image_data: Base64 encoded image data URL or raw base64

        Returns:
            Clean base64 string (without data: prefix)
        """
        try:
            # Remove data URL prefix if present
            if image_data.startswith('data:image'):
                image_data = image_data.split(',')[1]

            # Decode and validate image
            image_bytes = base64.b64decode(image_data)

            # Validate file size (max 10MB)
            if len(image_bytes) > 10 * 1024 * 1024:
                # Compress image if too large
                img = Image.open(io.BytesIO(image_bytes))

                # Convert to RGB if necessary
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                # Resize if too large
                max_size = 1024
                if max(img.size) > max_size:
                    img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

                # Save compressed image
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='JPEG', quality=85)
                image_bytes = img_byte_arr.getvalue()

                # Re-encode to base64
                image_data = base64.b64encode(image_bytes).decode('utf-8')

            return image_data

        except Exception as e:
            raise ValueError(f"Invalid image data: {str(e)}")

    async def submit_try_on_task(self, person_image: str, garment_image: str) -> str:
        """
        Submit a virtual try-on task to KlingAI

        Args:
            person_image: Base64 encoded person image
            garment_image: Base64 encoded garment image

        Returns:
            Task ID for polling status
        """
        try:
            # Prepare images
            human_base64 = self._prepare_image(person_image)
            cloth_base64 = self._prepare_image(garment_image)

            # Prepare payload according to KlingAI documentation
            payload = {
                "model_name": self.model_name,
                "human_image": human_base64,  # No data: prefix
                "cloth_image": cloth_base64   # No data: prefix
            }

            # Get fresh auth headers
            headers = self._get_auth_headers()

            # Submit task
            response = requests.post(
                f"{self.base_url}/v1/images/kolors-virtual-try-on",
                headers=headers,
                json=payload,
                timeout=60
            )

            # Check for HTML responses (error pages)
            content_type = response.headers.get('content-type', '').lower()
            if 'html' in content_type:
                raise Exception("Received HTML error page instead of JSON")

            # Parse JSON response
            try:
                response_json = response.json()
            except Exception as e:
                raise Exception(f"Failed to parse JSON response: {e}")

            # Check response format according to documentation
            if response_json.get("code") != 0:
                error_msg = response_json.get("message", "Unknown error")
                error_code = response_json.get("code", "unknown")
                raise Exception(f"API Error - Code: {error_code}, Message: {error_msg}")

            # Extract task information
            data = response_json.get("data", {})
            task_id = data.get("task_id")

            if not task_id:
                raise Exception("No task_id in response")

            return task_id

        except Exception as e:
            raise Exception(f"Failed to submit try-on task: {str(e)}")

    async def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Get the status of a try-on task

        Args:
            task_id: Task ID returned from submit_try_on_task

        Returns:
            Task status information
        """
        try:
            # Get fresh auth headers for status check
            headers = self._get_auth_headers()

            response = requests.get(
                f"{self.base_url}/v1/images/kolors-virtual-try-on/{task_id}",
                headers=headers,
                timeout=30
            )

            if response.status_code != 200:
                raise Exception(f"Status check failed: HTTP {response.status_code}")

            status_json = response.json()

            # Check API response format
            if status_json.get("code") != 0:
                error_msg = status_json.get("message", "Unknown error")
                raise Exception(f"Status API Error: {error_msg}")

            return status_json.get("data", {})

        except Exception as e:
            raise Exception(f"Failed to get task status: {str(e)}")

    async def wait_for_completion(self, task_id: str, max_wait_time: int = 600, poll_interval: int = 15) -> Dict[str, Any]:
        """
        Wait for a try-on task to complete

        Args:
            task_id: Task ID to poll
            max_wait_time: Maximum time to wait in seconds (default: 10 minutes)
            poll_interval: How often to check status in seconds (default: 15 seconds)

        Returns:
            Final task result with image URLs
        """
        start_time = time.time()
        max_checks = max_wait_time // poll_interval

        for i in range(max_checks):
            elapsed_time = time.time() - start_time

            if elapsed_time > max_wait_time:
                raise Exception(f"Task {task_id} timed out after {max_wait_time} seconds")

            try:
                # Wait before checking (except first check)
                if i > 0:
                    await asyncio.sleep(poll_interval)

                status_data = await self.get_task_status(task_id)

                task_status = status_data.get("task_status", "unknown")
                task_status_msg = status_data.get("task_status_msg", "")

                if task_status == "succeed":
                    # Extract image URLs according to documentation
                    task_result = status_data.get("task_result", {})
                    images = task_result.get("images", [])

                    if images:
                        return {
                            "success": True,
                            "status": "completed",
                            "images": images,
                            "task_id": task_id
                        }
                    else:
                        raise Exception("No images found in successful result")

                elif task_status == "failed":
                    error_msg = task_status_msg or "Task failed without specific reason"
                    raise Exception(f"Task failed: {error_msg}")

                elif task_status in ["submitted", "processing"]:
                    # Task is still running, continue polling
                    continue

                else:
                    # Unknown status, continue polling
                    continue

            except Exception as e:
                if "timeout" in str(e).lower() or "failed" in str(e).lower():
                    raise
                # For other errors, continue polling
                continue

        raise Exception(f"Task did not complete within {max_wait_time} seconds")

    async def process_try_on(self, person_image: str, garment_image: str) -> Dict[str, Any]:
        """
        Complete try-on process: submit task and wait for result

        Args:
            person_image: Base64 encoded person image
            garment_image: Base64 encoded garment image

        Returns:
            Result dictionary with success status and image URLs
        """
        try:
            # Submit task
            task_id = await self.submit_try_on_task(person_image, garment_image)

            # Wait for completion
            result = await self.wait_for_completion(task_id)

            return result

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Virtual try-on processing failed"
            }

    async def health_check(self) -> bool:
        """
        Check if the KlingAI API is accessible

        Returns:
            True if API is accessible, False otherwise
        """
        try:
            headers = self._get_auth_headers()

            # Simple connectivity test
            response = requests.get(
                f"{self.base_url}/v1/images/kolors-virtual-try-on",
                headers=headers,
                timeout=10
            )

            # Even if we get an error, if we can connect it means the API is up
            return response.status_code < 500

        except Exception:
            return False


# Utility functions for integration
def create_kling_client() -> KlingAIClient:
    """Create and return a KlingAI client instance"""
    access_key = os.getenv('KLING_ACCESS_KEY', 'AJeTKte39b4nNKTGmh8ErCQEb9yM9pDg')
    secret_key = os.getenv('KLING_SECRET_KEY', 'ef4G4CeGYfkDmTgfBdGhLJAkFCeGyANE')
    return KlingAIClient(access_key, secret_key)

async def process_virtual_tryon_kling(person_image: str, garment_image: str) -> Dict[str, Any]:
    """
    Process virtual try-on using KlingAI

    Args:
        person_image: Base64 encoded person image
        garment_image: Base64 encoded garment image

    Returns:
        Result dictionary with success status and image data
    """
    try:
        client = create_kling_client()
        result = await client.process_try_on(person_image, garment_image)

        if result.get("success"):
            # Extract the first image URL from the results
            images = result.get("images", [])
            if images:
                first_image = images[0]
                image_url = first_image.get("url", "")

                # Download the image and convert to base64 data URL
                try:
                    async with httpx.AsyncClient(timeout=30.0) as client:
                        img_response = await client.get(image_url)
                        img_response.raise_for_status()
                        img_bytes = img_response.content

                        # Convert to base64 data URL
                        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
                        data_url = f"data:image/png;base64,{img_base64}"

                        return {
                            'success': True,
                            'result_image': data_url,
                            'message': 'Virtual try-on completed successfully',
                            'provider': 'ai_processing',
                            'task_id': result.get('task_id'),
                            'original_url': image_url
                        }
                except Exception as download_error:
                    # If download fails, return the URL
                    return {
                        'success': True,
                        'result_image': image_url,
                        'message': 'Virtual try-on completed successfully',
                        'provider': 'ai_processing',
                        'task_id': result.get('task_id'),
                        'download_error': str(download_error)
                    }
            else:
                return {
                    'success': False,
                    'error': 'No result images generated',
                    'message': 'Processing completed but no images were generated',
                    'provider': 'ai_processing'
                }
        else:
            return {
                'success': False,
                'error': result.get('error', 'Unknown error'),
                'message': result.get('message', 'Virtual try-on failed'),
                'provider': 'ai_processing'
            }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': 'Virtual try-on processing failed',
            'provider': 'ai_processing'
        }
