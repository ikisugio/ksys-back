from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Company, Jigyosyo
from ..serializers import CompanySerializer, JigyosyoSerializer


class JigyosyoList(APIView):
    def get(self, request):
        jigyosyos = Jigyosyo.objects.all()
        serializer = JigyosyoSerializer(jigyosyos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = JigyosyoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JigyosyoDetail(APIView):
    def get_object(self, uuid):
        try:
            return Jigyosyo.objects.get(pk=pk)
        except Jigyosyo.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        jigyosyo = self.get_object(pk)
        serializer = JigyosyoSerializer(jigyosyo)
        return Response(serializer.data)

    def put(self, request, pk):
        jigyosyo = self.get_object(pk)
        serializer = JigyosyoSerializer(jigyosyo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        jigyosyo = self.get_object(pk)
        jigyosyo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
