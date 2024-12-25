from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# Хранилище контактов (имитация базы данных)
contacts = {}
contact_id_counter = 1

@app.route('/contacts', methods=['POST'])
def create_contact():
    """
    Создать новый контакт
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
              example: John Doe
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
              example: John Doe
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
    Получить информацию о контакте
    ---
    tags:
      - Контакты
    parameters:
      - name: contact_id
        in: path
        type: integer
        required: true
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
              example: John Doe
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
    Удалить контакт
    ---
    tags:
      - Контакты
    parameters:
      - name: contact_id
        in: path
        type: integer
        required: true
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
