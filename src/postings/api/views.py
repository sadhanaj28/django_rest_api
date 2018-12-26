#generic view

from django.db.models import Q
from rest_framework import generics, mixins

from .permissions import IsOwnerOrReadOnly
from postings.models import BlogPost
from .serializers import BlogPostSerializer


class BlogPostAPIView(mixins.CreateModelMixin, generics.ListAPIView):
	lookup_field = 'id'
	serializer_class = BlogPostSerializer
	#queryset = BlogPost.objects.all()

	def get_queryset(self):
		qs = BlogPost.objects.all()
		query = self.request.GET.get("q")
		if query is not None:
			qs = qs.filter(Q(title__icontains=query) | Q(content__icontains=query)).distinct()
		return qs 

	def perform_create(self, serializer):
		serializer.save(user = self.request.user)

	#create
	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

	def get_serializer_context(self, *args, **kwargs):
		return {"request" : self.request}

	#put
	#def put(self, request, *args, **kwargs):
	#	return self.update(request, *args, **kwargs)

	#patch
	#def patch(self, request, *args, **kwargs):
	#	return self.update(request, *args, **kwargs)

class BlogPostRudView(generics.RetrieveUpdateDestroyAPIView):
	lookup_field = 'id'
	serializer_class = BlogPostSerializer
	permissions_classes = [IsOwnerOrReadOnly]
	#queryset = BlogPost.objects.all()

	def get_queryset(self):
		return BlogPost.objects.all()

	def get_serializer_context(self, *args, **kwargs):
		return {"request" : self.request}
	#def get_object(self):
	#	id = self.kwargs.get("id")
	#	return BlogPost.objects.get(id = id)
