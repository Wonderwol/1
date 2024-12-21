from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# Хранение данных о контактах в словаре
contacts = {}

@app.route('/contacts', methods=['POST'])
def create_contact():
    """
    Создание нового контакта
    ---
    parameters:
      - name: name
        in: body
        type: string
        required: true
        description: Имя контакта
      - name: phone
        in: body
        type: string
        required: true
        description: Телефонный номер контакта
    responses:
      200:
        description: Контакт успешно создан
        schema:
          id: Contact
          properties:
            id:
              type: integer
              description: Идентификатор контакта
            name:
              type: string
              description: Имя контакта
            phone:
              type: string
              description: Телефонный номер
    """
    contact_data = request.get_json()
    contact_id = len(contacts) + 1
    contact = {
        'id': contact_id,
        'name': contact_data['name'],
        'phone': contact_data['phone']
    }
    contacts[contact_id] = contact
    return jsonify(contact), 200

@app.route('/contacts/<int:id>', methods=['GET'])
def get_contact(id):
    """
    Получение информации о контакте
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: Идентификатор контакта
    responses:
      200:
        description: Информация о контакте
        schema:
          id: Contact
          properties:
            id:
              type: integer
              description: Идентификатор контакта
            name:
              type: string
              description: Имя контакта
            phone:
              type: string
              description: Телефонный номер
      404:
        description: Контакт не найден
    """
    contact = contacts.get(id)
    if contact:
        return jsonify(contact), 200
    else:
        return jsonify({'error': 'Contact not found'}), 404

@app.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    """
    Удаление контакта
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: Идентификатор контакта
    responses:
      200:
        description: Контакт успешно удален
      404:
        description: Контакт не найден
    """
    if id in contacts:
        del contacts[id]
        return jsonify({'message': 'Contact deleted'}), 200
    else:
        return jsonify({'error': 'Contact not found'}), 404
