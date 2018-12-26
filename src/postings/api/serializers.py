from rest_framework import serializers

from postings.models import BlogPost

#converts to JSON and validations for data passed
class BlogPostSerializer(serializers.ModelSerializer):
	url = serializers.SerializerMethodField(read_only = True)
	class Meta:
		model = BlogPost
		fields = [
			'url',
			'id',
			'user',
			'title',
			'content',
			'timestamp',
		]
		read_only_fields = ['user']

	#convert to JSON
	#validations for data passed

	def get_url(self, obj):
		#get request
		request = self.context.get("request")
		return obj.get_api_url(request = request)

	def validate_title(self, value):
		qs = BlogPost.objects.filter(title__iexact = value)
		if self.instance:
			qs = qs.exclude(id = self.instance.id)
		if qs.exists():
			raise serializers.ValidationError("This title has already been used")
		return value