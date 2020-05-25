# custom_storages.py
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION

    def path(self, name):
        # FIXME below was added myself to try fix something
        return self.url(name)


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION

    def path(self, name):
        # FIXME below was added myself to try fix something
        return self.url(name)
