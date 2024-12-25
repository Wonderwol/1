import sys
from flasgger import Swagger
from app import app

swagger = Swagger(app)  # Инициализация Swagger для Flask-приложения
with open('openapi.yaml', 'w') as f:
    f.write(swagger.spec.to_yaml())  # Запись OpenAPI спецификации в файл
