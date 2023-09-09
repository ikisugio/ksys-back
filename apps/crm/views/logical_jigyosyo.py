from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import LogicalJigyosyo
from ..serializers import LogicalJigyosyoSerializer


class LogicalJigyosyoList(APIView):
    def get(self, request):
        jigyosyos = LogicalJigyosyo.objects.all()
        serializer = LogicalJigyosyoSerializer(jigyosyos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LogicalJigyosyoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogicalJigyosyoDetail(APIView):
    def get_object(self, pk):
        try:
            return LogicalJigyosyo.objects.get(pk=pk)
        except LogicalJigyosyo.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        jigyosyo = self.get_object(pk)
        serializer = LogicalJigyosyoSerializer(jigyosyo)
        return Response(serializer.data)

    def put(self, request, pk):
        jigyosyo = self.get_object(pk)
        serializer = LogicalJigyosyoSerializer(jigyosyo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        jigyosyo = self.get_object(pk)
        jigyosyo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
