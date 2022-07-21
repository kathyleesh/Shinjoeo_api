from django.urls import path,include
from .views import NewWordViewSet,NewWordListCreateTime,NewWordListLikeCount
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

#스웨거 적용 내용
schema_view = get_schema_view(
    openapi.Info(
        title="신조어 도감", # 타이틀
        default_version='v1', # 버전
        description="신조어도감 최초 배포", # 설명
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="duswlsdl0121@naver.com"),
    ),
    validators=['flex'],
    public=True,
    permission_classes=(AllowAny,)
)

#라우팅 설정
router = DefaultRouter()

router.register('newword',NewWordViewSet)

#신조어 목록 보여주기 + 새로운 게시글 생성
newword_list = NewWordViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

#신조어 삭제, 좋아요
newword_one = NewWordViewSet.as_view({
    # 'get': 'retrieve',
    'delete': 'destroy',
    'post': 'update',
})

urlpatterns =[
    path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
    path('', include(router.urls)),
    path('list/', NewWordListCreateTime.as_view()),
    path('listbylike/', NewWordListLikeCount.as_view()),
    path('newword/', newword_list,name='newword'),
    path('newword/<int:pk>/', newword_one),
]