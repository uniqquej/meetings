from drf_yasg import openapi

request_body_recruitment = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, description="제목"),
            'content': openapi.Schema(type=openapi.TYPE_STRING, description="본문 내용"),
            'category': openapi.Schema(type=openapi.TYPE_INTEGER, description="카테고리 id"),
            'number_of_recruitments' : openapi.Schema(type=openapi.TYPE_INTEGER, description="모집인원"),
            'group' : openapi.Schema(type=openapi.TYPE_INTEGER, description="모집 그룹 id"),
        }
    )