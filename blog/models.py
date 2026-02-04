# Django가 기본 제공하는 User 모델 import
# But, 프로젝트에서 AUTH_USER_MODEL 설정을 통해 커스텀 User 모델을 정의할 수 있음
# 커스텀 User 모델을 쓰고 있는데 기본 User를 직접 import 하면 !!실제로 존재하지 않는 모델을 참조!!
# from django.contrib.auth.models import User

# 현재 프로젝트에서 실제로 사용 중인 User 모델을 반환하는 함수/ 기본 User or 커스텀 User 둘 다 가능
# Django 공식 문서에서도 User 모델을 참조할 때는 항상 get_user_model()을 쓰라고 권장함.
from django.contrib.auth import get_user_model
User = get_user_model()

from django.db import models



# 제목
# 본문
# 작성자
# 작성일자
# 수정일자
# 카테고리

class Blog(models.Model):
    CATEGORY_CHOICES = (
        ('free','자유'),
        ('travel', '여행'),
        ('cat', '고양이'),
        ('dog', '강아지'),
    )
    category = models.CharField('카테고리', max_length=10, choices=CATEGORY_CHOICES)
    title = models.CharField('제목', max_length=100)
    content = models.TextField('본문')
    # 외래키 on_delete=
    # models.CASCADE 참조된 부모 데이터 삭제 시 자식 데이터도 함께 연쇄 삭제
    # models.PROTECT 참조된 부모 객체를 삭제 시도,자식 데이터가 있으면
    #                ProtectedError를 발생시켜 삭제를 막음. 참조 데이터 보호가 필요 시 무결성 지킴이
    # models.SET_NULL 널 값을 넣음 -> 유저 삭제시 블로그의 author 가 null이 됨. (모델에서 Null = True 여야 함.
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField('작성일자', auto_now_add=True)
    updated_at = models.DateTimeField('수정일자', auto_now=True)

    def __str__(self):
        return f'[{self.get_category_display()}] {self.title[:10]}'

    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'

