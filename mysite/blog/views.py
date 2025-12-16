from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Post
from .api.serializers import (
    AddPostSerializer,
    PostAuthorSerializer,
    AuthorPostsSerializer
)

# ---------------------------
#   Crear un nuevo Post
# ---------------------------

class AddPostView(APIView):
    def post(self, request):
        serializer = AddPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()   # DRF recomienda esto
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------
#   Listar TODOS los autores
# ---------------------------

class AllPostAuthorsView(generics.ListAPIView):
    queryset = Post.objects.all().distinct("author")
    serializer_class = PostAuthorSerializer


# ------------------------------------
#   Conseguir posts por autor
# ------------------------------------

class AuthorPostsView(APIView):
    def get(self, request):
        author_id = request.query_params.get("author")

        if not author_id:
            return Response(
                {"error": "Debe enviar ?author=<id>"},
                status=status.HTTP_400_BAD_REQUEST
            )

        posts = Post.objects.filter(
            author_id=author_id,
            status=Post.Status.PUBLISHED
        )

        serializer = AuthorPostsSerializer(posts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
