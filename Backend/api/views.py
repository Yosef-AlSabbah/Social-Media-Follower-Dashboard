from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

# Create your views here.

@require_http_methods(["GET"])
def health_check(request):
    """Health check endpoint to verify the backend is running"""
    return JsonResponse({"status": "healthy", "message": "Backend is running"})
