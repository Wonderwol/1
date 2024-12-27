from flask import Flask, jsonify, request
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

# Хранилище данных
contacts = {}
contact_id_counter = 1


@app.route('/contacts', methods=['POST'])
def create_contact():
    """
    Создание нового контакта
    ---
    tags:
      - Контакты
    parameters:
      - name: body
        in: body
        required: true
        description: Данные нового контакта
        schema:
          type: object
          required:
            - name
            - phone
          properties:
            name:
              type: string
              example: Artem Beard
            phone:
              type: string
              example: "+123456789"
    responses:
      201:
        description: Контакт успешно создан
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: Artem Beard
            phone:
              type: string
              example: "+123456789"
      400:
        description: Ошибка в запросе
    """
    global contact_id_counter
    data = request.json
    if not data or 'name' not in data or 'phone' not in data:
        return jsonify({'error': 'Name and phone are required'}), 400

    contact_id = contact_id_counter
    contact_id_counter += 1
    contacts[contact_id] = {
        'id': contact_id,
        'name': data['name'],
        'phone': data['phone']
    }
    return jsonify(contacts[contact_id]), 201


@app.route('/contacts/<int:contact_id>', methods=['GET'])
def get_contact(contact_id):
    """
    Получение информации о контакте по ID
    ---
    tags:
      - Контакты
    parameters:
      - name: contact_id
        in: path
        required: true
        type: integer
        description: Идентификатор контакта
    responses:
      200:
        description: Информация о контакте
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: Artem Beard
            phone:
              type: string
              example: "+123456789"
      404:
        description: Контакт не найден
    """
    contact = contacts.get(contact_id)
    if not contact:
        return jsonify({'error': 'Contact not found'}), 404
    return jsonify(contact)


@app.route('/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    """
    Удаление контакта по ID
    ---
    tags:
      - Контакты
    parameters:
      - name: contact_id
        in: path
        required: true
        type: integer
        description: Идентификатор контакта
    responses:
      200:
        description: Контакт успешно удален
        schema:
          type: object
          properties:
            message:
              type: string
              example: Contact deleted
      404:
        description: Контакт не найден
    """
    if contact_id not in contacts:
        return jsonify({'error': 'Contact not found'}), 404
    del contacts[contact_id]
    return jsonify({'message': 'Contact deleted'}), 200


@app.route('/swagger.json')
def swagger_spec():
    """
    Предоставление файла swagger.json
    ---
    tags:
      - Система
    responses:
      200:
        description: Файл swagger.json предоставлен
    """
    # Получаем спецификацию Swagger
    api_spec = swagger.get_apispecs()

    # Путь для сохранения swagger.json
    swagger_file_path = os.path.join(swagger_files_dir, 'swagger.json')

    # Сохраняем спецификацию в файл
    with open(swagger_file_path, 'w') as f:
        json.dump(api_spec, f)

    # Возвращаем спецификацию в формате JSON
    return jsonify(api_spec)
