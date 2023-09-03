from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CrawlList, CrawlDetail
from .serializers import CrawlListSerializer, CrawlDetailSerializer


class CrawlListList(APIView):
    def get(self, request):
        crawl_lists = CrawlList.objects.all()
        serializer = CrawlListSerializer(crawl_lists, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CrawlListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CrawlListDetail(APIView):
    def get_object(self, pk):
        try:
            return CrawlList.objects.get(pk=pk)
        except CrawlList.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        crawl_list = self.get_object(pk)
        serializer = CrawlListSerializer(crawl_list)
        return Response(serializer.data)

    def put(self, request, pk):
        crawl_list = self.get_object(pk)
        serializer = CrawlListSerializer(crawl_list, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        crawl_list = self.get_object(pk)
        crawl_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CrawlDetailList(APIView):
    def get(self, request):
        crawl_details = CrawlDetail.objects.all()
        serializer = CrawlDetailSerializer(crawl_details, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CrawlDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CrawlDetailDetail(APIView):
    def get_object(self, pk):
        try:
            return CrawlDetail.objects.get(pk=pk)
        except CrawlDetail.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        crawl_detail = self.get_object(pk)
        serializer = CrawlDetailSerializer(crawl_detail)
        return Response(serializer.data)

    def put(self, request, pk):
        crawl_detail = self.get_object(pk)
        serializer = CrawlDetailSerializer(crawl_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        crawl_detail = self.get_object(pk)
        crawl_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
