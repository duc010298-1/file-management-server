from rest_framework import permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from file_management_app.models import File
from file_management_app.serializers import FileSerializer


class GetListFileView(APIView, PageNumberPagination):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        page_size = self.request.query_params.get('page_size')
        page = self.request.query_params.get('page')

        if page_size is None:
            return Response({
                'page_size': ['Missing page_size param.']
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            page_size_int = int(page_size)
        except ValueError:
            return Response({
                'page_size': ['Invalid page_size.']
            }, status=status.HTTP_400_BAD_REQUEST)

        if page is None:
            return Response({
                'page': ['Missing page param.']
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            page_int = int(page)
        except ValueError:
            return Response({
                'page': ['Invalid page.']
            }, status=status.HTTP_400_BAD_REQUEST)

        PageNumberPagination.page_size = page_size_int

        files = File.objects.filter(owner=user)
        try:
            results_files = self.paginate_queryset(files, request, view=self)
            count = self.page.paginator.count
        except:
            results_files = []
            count = 0

        fields = ('id', 'file_name', 'file_size', 'created')
        serializer = FileSerializer(
            results_files, many=True, fields=fields
        )
        return Response({
            'count': count,
            'page_size': page_size_int,
            'page_number': page_int,
            'results': serializer.data
        })
