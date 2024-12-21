from flasgger import Swagger
from flask import Flask, jsonify

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

if __name__ == "__main__":
    # Запускаем приложение для генерации спецификации
    app.run(debug=True)













