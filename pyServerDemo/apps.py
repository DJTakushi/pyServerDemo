from django.apps import AppConfig
from django.conf import settings
from django.template.loader import render_to_string
import os

class DblogAppConfig(AppConfig):
    name = "dblog"

    def ready(self):
        if settings.WRITE_BLOG_TEMPLATES_ON_STARTUP:
            sourceTemplateDir = str(settings.BASE_DIR)+"/pyServerDemo/templates/dblog/djangoTemplates/"
            destinationDir = str(settings.BASE_DIR)+"/dblog/djangoTemplates/"
            context = {'user':None}
            context['USE_USERS_FALSE']=True

            for root, dirs, files in os.walk(sourceTemplateDir):
                for file in files:
                    sourcePath = sourceTemplateDir+file
                    html = render_to_string(sourcePath, context)
                    dest_path = destinationDir + file
                    with open(dest_path, "w") as f:
                        f.write(html)
