from django.db import models


class TimestampModel(models.Model):
    created_at = models.DateTimeField('작성일자', auto_now_add=True)
    updated_at = models.DateTimeField('수정일자', auto_now=True)

    class Meta:
        # 실제로 모델의 테이블을 만들지는 않음.
        # 상속용으로만 사용.
        abstract = True