# ------ DJANGO FORM --------------
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, renderers, generics, permissions
from rest_framework.parsers import JSONParser
from rest_framework.reverse import reverse

# ---- REST FRAMEWORK (FUNCTION BASED) ------
from rest_framework.decorators import api_view

# ------ REST FRAMEWORK (CLASS BASED)
from rest_framework.views import APIView

from rest_framework.response import Response

from snippets.models import Snippet, Travel
from snippets.serializers import SnippetSerializer, TravelSerializer, UserSerializer, UserTravelSerializer

from snippets.permissions import IsOwnerOrReadOnly

# ---------------------- DJANGO FORM ---------------------------
@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=400)
    
    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser.parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)

#----------------------------------------------------------------


# ----------------- DJANGO REST FORM (FUNCTION BASED) ------------
@api_view(['GET', 'POST'])
def snippet_list_rest(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializers = SnippetSerializer(snippets, many=True)
        return Response(serializers.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail_rest(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ---------------------------------------------------------------------


# ------------------------ DJANGO REST FORM (CLASS BASED)--------------
class SnippetList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SnippetDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            snippet = Snippet.objects.get(pk=pk)
            return snippet
        except Snippet.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SnippetListGenerics(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SnippetDetailGenerics(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

class UserListTravel(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserTravelSerializer

class UserDetailTravel(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserTravelSerializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# ------------------------------- DJANGO FORM -------------------------
@csrf_exempt
def travel_list(request):
    if request.method == 'GET':
        travels = Travel.objects.all()
        serializer = TravelSerializer(travels, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser.parse(request)
        serializer = TravelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def travel_detail(request):
    try:
        travel = Travel.objects.get(pk=pk)
    except Travel.DoesNotExist:
        return HttpResponse(status=400)
    
    if request.method == 'GET':
        serializer = TravelSerializer(travel)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser.parse(request)
        serializer = TravelSerializer(travel, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        travel.delete()
        return HttpResponse(status=204)

# ------------------------------------------------------------


# ------------ DJANGO REST FORM (FUNCTION BASED) -------------
@api_view(['GET', 'POST'])
def travel_list_rest(request, format=None):
    if request.method == 'GET':
        travels = Travel.objects.all()
        serializer = TravelSerializer(travels, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TravelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_RESQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def travel_detail_rest(request, pk, format=None):
    try:
        travel = Travel.objects.get(pk=pk)
    except Travel.DoesNotExist:
        return Response(stats=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TravelSerializer(travel)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = TravelSerializer(travel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.dat)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        travel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ------------ DJANGO REST FORM (CLASS BASED) ---------------------

class TravelListView(APIView):
    def get(self, request, format=None):
        travels = Travel.objects.all()
        serializer = TravelSerializer(travels, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = TravelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TravelDetailView(APIView):
    def get_object(self, pk):
        try:
            travel = Travel.objects.get(pk=pk)
            return travel
        except Travel.DoesNotExist:
            return Http404
    
    def get(self, request, pk, format=None):
        travel = self.get_object(pk=pk)
        serializer = TravelSerializer(travel)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        travel = self.get_object(pk=pk)
        serializer = TravelSerializer(travel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        travel = self.get_object(pk=pk)
        travel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TravelListGenerics(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Travel.objects.all()
    serializer_class = TravelSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TravelDetailGenerics(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Travel.objects.all()
    serializer_class = TravelSerializer


# ---------------- Endpoint for the root of API -------

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })

class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


@api_view(['GET'])
def api_root_travel(request, format=None):
    return Response({
        'users-travel': reverse('user-travel-list', request=request, format=format),
        'travels': reverse('travel-list', request=request, format=format)
    })