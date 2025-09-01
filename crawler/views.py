from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Page
from .utils import is_allowed, extract_metadata

@api_view(["POST"])
def crawl_url(request):
    url = request.data.get("url")
    if not url:
        return Response({"error": "URL required"}, status=status.HTTP_400_BAD_REQUEST)

    # Check robots.txt
    if not is_allowed(url):
        return Response({"error": "Blocked by robots.txt"}, status=status.HTTP_403_FORBIDDEN)

    try:
        data = extract_metadata(url)
        page, created = Page.objects.update_or_create(
            url=url,
            defaults=data
        )
        return Response({
            "url": page.url,
            "title": page.title,
            "description": page.description,
            "body": page.body[:300] + "...",  # preview
            "created_at": page.created_at,
            "updated_at": page.updated_at,
        })
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
