from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import URLRecord
from .serializers import URLRecordSerializer

class URLRecordCreateView(generics.CreateAPIView):
    queryset = URLRecord.objects.all()
    serializer_class = URLRecordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        url = serializer.validated_data["url"]

        # Avoid duplicates
        url_record, created = URLRecord.objects.get_or_create(url=url)

        output_serializer = URLRecordSerializer(url_record)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

class URLRecordListView(generics.ListAPIView):
    queryset = URLRecord.objects.all().order_by("-id")  # latest first
    serializer_class = URLRecordSerializer
