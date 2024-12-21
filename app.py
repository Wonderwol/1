from flask import Flask, jsonify
from flasgger import Swagger
import yaml

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/contacts', methods=['POST'])
def create_contact():
    """
    Создание нового контакта
    ---
    parameters:
      - name: contact
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            phone:
              type: string
    responses:
      200:
        description: Контакт успешно создан
    """
    return jsonify(message="Contact created"), 200

@app.route('/apispec_1.json')
def get_swagger_json():
    """
    Генерация Swagger JSON спецификации
    """
    return jsonify(app.config['SWAGGER'])

if __name__ == "__main__":
    app.run(debug=True)


















