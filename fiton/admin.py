from django.contrib import admin
from django.apps import apps

# fiton 앱의 모든 모델 자동 등록
fiton_models = apps.get_app_config('fiton').get_models()
for model in fiton_models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass