from drf_yasg import openapi

get_post_params = [
    openapi.Parameter(
        "category",
        openapi.IN_QUERY,
        description="카테고리 id",
        type=openapi.TYPE_INTEGER,
        default=""
    ),
    openapi.Parameter(
        "search",
        openapi.IN_QUERY,
        description="찾고싶은 키워드",
        type=openapi.TYPE_STRING,
        default=""
    )
]

request_body_post = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, description="제목"),
            'content': openapi.Schema(type=openapi.TYPE_STRING, description="본문 내용"),
            'category': openapi.Schema(type=openapi.TYPE_INTEGER, description="카테고리 id"),
        }
    )

request_body_comment = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={ 
            'comment': openapi.Schema(type=openapi.TYPE_STRING, description="댓글"),
        }
    )