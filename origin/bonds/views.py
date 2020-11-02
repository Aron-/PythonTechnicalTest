from rest_framework.views import APIView
from rest_framework.response import Response

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Bond
from .serializers import BondSerializer

import requests


class HelloWorld(APIView):
    def get(self, request):
        return Response("Hello World!")


# Token authenticated POST and GET request methods at the endpoint /bonds/
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def bonds(request):
    if request.method == 'GET':
        bond_results = Bond.objects.all()

        legal_name = request.query_params.get('legal_name', None)
        if legal_name is not None:
            bond_results = bond_results.filter(legal_name__icontains=legal_name)

        bond_serializer = BondSerializer(bond_results, many=True)
        return JsonResponse(bond_serializer.data, safe=False)

    elif request.method == 'POST':
        bond_data = JSONParser().parse(request)
        bond_serializer = BondSerializer(data=bond_data)
        if bond_serializer.is_valid():
            request_uri = 'https://leilookup.gleif.org/api/v2/leirecords?lei=' + bond_data['lei']
            r = requests.get(request_uri)
            if r.status_code == 200:
                leilookup_response = r.json()
                try:
                    legal_name = leilookup_response[0]['Entity']['LegalName']['$']
                except IndexError:
                    return JsonResponse({"lei": ["LEI lookup failed or not found. Request not saved."]},
                                        status=status.HTTP_400_BAD_REQUEST)
                bond_serializer.save(legal_name=legal_name)
                return JsonResponse(bond_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(bond_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
