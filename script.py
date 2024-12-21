import yaml
from app import app  # импортируем Flask-приложение

def generate_openapi_yaml():
    with app.test_client() as client:
        # Запрашиваем Swagger спецификацию в формате JSON
        response = client.get('/apispec_1.json')
        
        # Проверяем, что ответ успешен и является JSON
        if response.status_code == 200 and response.is_json:
            openapi_spec = response.json
            # Сохраняем спецификацию в формате YAML
            with open("docs/openapi.yaml", "w") as file:
                yaml.dump(openapi_spec, file, default_flow_style=False)
            print("Спецификация OpenAPI сохранена в docs/openapi.yaml")
        else:
            print("Ошибка: не удалось получить спецификацию OpenAPI.")

if __name__ == "__main__":
    generate_openapi_yaml()
