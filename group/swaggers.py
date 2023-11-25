from drf_yasg import openapi

request_body_group = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'group_name': openapi.Schema(type=openapi.TYPE_STRING, description="그룹 이름"),
        }
    )

request_body_put_group = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'group_name': openapi.Schema(type=openapi.TYPE_STRING, description="그룹 이름"),
            'leader': openapi.Schema(type=openapi.TYPE_INTEGER, description="리더 아이디"),
        }
    )

request_body_meeting = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'calender_date' : openapi.Schema(type=openapi.FORMAT_DATE, description="일정 날짜"),
            'title' : openapi.Schema(type=openapi.TYPE_STRING, description="일정 내용"),
            'time': openapi.Schema(type=openapi.FORMAT_DATETIME, description="일정 시간"),    
        }
    )

request_body_to_do = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'date' : openapi.Schema(type=openapi.FORMAT_DATE, description="할일 날짜"),
            'task' : openapi.Schema(type=openapi.TYPE_STRING, description="할일 내용"),
            
        }
    )

request_body_notice = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title' : openapi.Schema(type=openapi.TYPE_STRING, description="공지 제목"),
            'content' : openapi.Schema(type=openapi.TYPE_STRING, description="공지 본문")
            
        }
    )