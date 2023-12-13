from rest_framework import serializers

from recruitment.models import Recruitment
from post.serializers import AuthorSerializer,CategorySerializer
from group.serializers import GroupSerializer

class RecruitmentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    applicant_count = serializers.SerializerMethodField(read_only=True)
    
    def get_applicant_count(self,obj):
        return obj.applicant.count()
    
    class Meta:
        model = Recruitment
        fields = "__all__"
        

class RecruitmentWriteSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Recruitment
        fields = ["category","number_of_recruits","title","content","group"]

class RecruitmentDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    author = AuthorSerializer(read_only=True)
    applicant_count = serializers.SerializerMethodField(read_only=True)
    group = GroupSerializer(read_only=True)
    
    def get_applicant_count(self,obj):
        return obj.applicant.count()
    
    class Meta:
        model = Recruitment
        fields = "__all__"