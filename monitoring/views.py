from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from .models import Keyword, ContentItem, Flag
from .serializers import KeywordSerializer, FlagSerializer, FlagUpdateSerializer
from .services import scan_content

class KeywordViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Keywords.
    """
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer

class FlagViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing and updating Flags.
    Supports filtering by status.
    """
    queryset = Flag.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_serializer_class(self):
        if self.action in ['partial_update', 'update']:
            return FlagUpdateSerializer
        return FlagSerializer

@api_view(['POST'])
def scan_view(request):
    """
    Trigger a scan of all ContentItems against all Keywords.
    """
    created, updated = scan_content()
    return Response({
        "message": "Scan completed successfully",
        "flags_created": created,
        "flags_updated": updated
    }, status=status.HTTP_200_OK)
