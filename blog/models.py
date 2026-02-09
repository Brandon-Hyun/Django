# Django가 기본 제공하는 User 모델 import
# But, 프로젝트에서 AUTH_USER_MODEL 설정을 통해 커스텀 User 모델을 정의할 수 있음
# 커스텀 User 모델을 쓰고 있는데 기본 User를 직접 import 하면 !!실제로 존재하지 않는 모델을 참조!!
# from django.contrib.auth.models import User

# 현재 프로젝트에서 실제로 사용 중인 User 모델을 반환하는 함수/ 기본 User or 커스텀 User 둘 다 가능
# Django 공식 문서에서도 User 모델을 참조할 때는 항상 get_user_model()을 쓰라고 권장함.
from io import BytesIO
from pathlib import Path

from PIL import Image
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from utils.models import TimestampModel


User = get_user_model()

# 제목
# 본문
# 작성자
# 작성일자
# 수정일자
# 카테고리

class Blog(TimestampModel):
    CATEGORY_CHOICES = (
        ('free','자유'),
        ('travel', '여행'),
        ('cat', '고양이'),
        ('dog', '강아지'),
    )
    category = models.CharField('카테고리', max_length=10, choices=CATEGORY_CHOICES, default='free')
    title = models.CharField('제목', max_length=100)
    content = models.TextField('본문')
    # 외래키 on_delete=
    # models.CASCADE 참조된 부모 데이터 삭제 시 자식 데이터도 함께 연쇄 삭제
    # models.PROTECT 참조된 부모 객체를 삭제 시도,자식 데이터가 있으면
    #                ProtectedError를 발생시켜 삭제를 막음. 참조 데이터 보호가 필요 시 무결성 지킴이
    # models.SET_NULL 널 값을 넣음 -> 유저 삭제시 블로그의 author 가 null이 됨. (모델에서 Null = True 여야 함.
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField('이미지', null=True, blank=True, upload_to='blog/%y/%m/%d')
    thumbnail = models.ImageField('썸네일', null= True, blank=True, upload_to='blog/%y/%m/%d/thumbnail')


    # created_at = models.DateTimeField('작성일자', auto_now_add=True)
    # updated_at = models.DateTimeField('수정일자', auto_now=True)
    # from utils.models import TimestampModel **

    def __str__(self):
        return f'[{self.get_category_display()}] {self.title[:10]}'

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'blog_pk': self.pk})

    def get_thumbmail_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        elif self.image:
            return self.image.url
        return None


    def save(self, *args, **kwargs):
        if not self.image:
            return super().save(*args, **kwargs)

        image = Image.open(self.image)
        image.thumbnail((300,300))

        # Path 라이브러리를 사용해 이미지 경로를 가져옴
        image_path = Path(self.image.name)

        thumbnail_name = image_path.stem
        thumbnail_extension = image_path.suffix
        thumbnail_filename = f'{thumbnail_name}_thumb{thumbnail_extension}'

        if thumbnail_extension in ['.jpg', 'jpeg']:
            file_type = 'JPEG'
        elif thumbnail_extension == '.gif':
            file_type = 'GIF'
        elif thumbnail_extension == '.png':
            file_type = 'PNG'
        else:
            return super().save(*args, **kwargs)

        temp_thumb = BytesIO()
        image.save(temp_thumb, file_type)
        temp_thumb.seek(0)

        self.thumbnail.save(thumbnail_filename, temp_thumb, save=False)
        temp_thumb.close()
        return super().save(*args, **kwargs)


    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'

class Comment(TimestampModel):
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE)
    content = models.CharField('본문',max_length=255)
    author = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return f'[{self.blog.title} 댓글'

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글 목록'
        ordering = ['-created_at', '-id'] # 역정렬



