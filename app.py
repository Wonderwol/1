from flask import Flask, jsonify, send_from_directory
from flasgger import Swagger
import os
import json

app = Flask(__name__)
swagger = Swagger(app)

# Папка для хранения swagger.json
swagger_files_dir = 'swagger_files'

# Убедитесь, что папка существует
if not os.path.exists(swagger_files_dir):
    os.makedirs(swagger_files_dir)

@app.route('/swagger.json')
def swagger_spec():
    # Получаем спецификацию Swagger
    api_spec = swagger.get_apispecs()
    
    # Путь для сохранения swagger.json
    swagger_file_path = os.path.join(swagger_files_dir, 'swagger.json')
    
    # Сохраняем спецификацию в файл
    with open(swagger_file_path, 'w') as f:
        json.dump(api_spec, f)
    
    # Возвращаем спецификацию в формате JSON
    return jsonify(api_spec)

@app.route('/download_swagger')
def download_swagger():
    # Путь к сохраненному swagger.json
    swagger_file_path = os.path.join(swagger_files_dir, 'swagger.json')

    # Проверяем, существует ли файл, и если существует, отдаем его для скачивания
    if os.path.exists(swagger_file_path):
        return send_from_directory(swagger_files_dir, 'swagger.json', as_attachment=True)
    else:
        return jsonify({"error": "swagger.json file not found"}), 404
