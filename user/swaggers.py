from drf_yasg import openapi

request_body_login = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={ 
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description="핸드폰 번호"),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description="비밀번호"),
        }
    )

request_body_auth = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={ 
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description="핸드폰 번호"),
            'input_number': openapi.Schema(type=openapi.TYPE_STRING, description="인증 번호"),
        }
    )