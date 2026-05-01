from django.shortcuts import render
import datetime

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Vote
from .serializers import ResultItemV1Serializer, ResultItemV2Serializer, VoteSerializer
from .services import get_today_result

MIN_VERSION_FOR_V2 = 2


def _get_build_version(request):
    raw = request.headers.get('Build-Version', '1')
    try:
        return int(raw)
    except ValueError:
        return 1


class VoteView(APIView):
    '''Post /api/voting'''

    permission_classes = (permissions.IsAuthenticated,)

    def post(self,request):
        serializer = VoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        menu = serializer.validated_data['menu']
        today = datetime.date.today()

        if Vote.objects.filter(employee=request.user,date =today).exists():
            return Response({'message': 'Vote already exists'}, status=status.HTTP_409_CONFLICT)

        vote = Vote.objects.create(
            employee = request.user,
            menu = menu,
            date = today,
        )
        return Response({'message': 'Vote created'}, status=status.HTTP_201_CREATED)

class TodayResultsView(APIView):
    """
       GET /api/voting/results/today/

       Підтримує дві версії відповіді через хедер Build-Version:
         - v1 (старі клієнти): {restaurant, votes}
         - v2 (нові клієнти):  {restaurant, menu_id, votes, items}
       """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        results = get_today_result()
        build_version = _get_build_version(request)

        if build_version >= MIN_VERSION_FOR_V2:
            serializer = ResultItemV2Serializer(results, many=True)
        else:
            serializer = ResultItemV1Serializer(results, many=True)

        return Response(serializer.data)