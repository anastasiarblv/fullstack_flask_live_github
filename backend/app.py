from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  
from os import environ ## для чтения переменных среды, для подключения к базе данных

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
## DATABASE_URL - наш адрес базы данных 
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class User(db.Model):
  __tablename__ = 'users' ## задаем имя таблицы в нашей базе данных,
  ## и указываем из каких столбцов она должна состоять:
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)

  def json(self): ## когда мы вернем пользователя мы хотим,
    ## чтобы он был в формате json
    return {'id': self.id,'name': self.name, 'email': self.email}
  
db.create_all()

# create a test route
@app.route('/test', methods=['GET']) ## Просто тестируем что запуск flask происходит корректно
def test():
  return jsonify({'message': 'The server is running'})

# create a user
@app.route('/api/flask/users', methods=['POST']) ## хотим использовать метод flask для создания users
## Хотим написать свой собственны метод создания пользователя:
def create_user():
  try:
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user) ## это уже часть SQLAlchemy, которая создаем пользователя
    db.session.commit() ## затем мы коммитим эоот сеанс

    return jsonify({
        'id': new_user.id,
        'name': new_user.name,
        'email': new_user.email
    }), 201  

  except Exception as e: ## если возникает ошибка (проблема) при создании users, то выводим код 500
    return make_response(jsonify({'message': 'error creating user', 'error': str(e)}), 500)

## Код для получения users:  
## для получения всех users
@app.route('/api/flask/users', methods=['GET'])
def get_users():
  try:
    users = User.query.all() ## получаем всех пользователей с их id, name, email
    users_data = [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]
    return jsonify(users_data), 200 ## возвращаем все что в формате json
  except Exception as e:
    return make_response(jsonify({'message': 'error getting users', 'error': str(e)}), 500)  ## если возникает ошибка, то выводим код 500
  
## для получения одного user по его id
@app.route('/api/flask/users/<id>', methods=['GET'])
def get_user(id): ## вводим какой-то id, и получаем этому id его name
  try:
    user = User.query.filter_by(id=id).first() ## фильтруем по id для поиска 
    if user:
      return make_response(jsonify({'user': user.json()}), 200) ## если user по id найден, то выводим этого user в формате json
    return make_response(jsonify({'message': 'user not found'}), 404) ## если не найден, то выводим сообщение об ошибке и номер ошибки
  except Exception as e:
    return make_response(jsonify({'message': 'error getting user', 'error': str(e)}), 500) ## если какая-то иная ошибка, не связанна с наличием/отсутствием пользователя, то выводим 
  ## сообщение об ошибке и номер ошибки 500
  
## для обновления одного user
@app.route('/api/flask/users/<id>', methods=['PUT'])
def update_user(id):
  try:
    user = User.query.filter_by(id=id).first() ## по id находим пользователя 
    if user: ## если такой user существует, то меняем (обновляем) на новые name и email
      data = request.get_json()
      user.name = data['name']
      user.email = data['email']
      db.session.commit()
      return make_response(jsonify({'message': 'user updated'}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404)  
  except Exception as e:
      return make_response(jsonify({'message': 'error updating user', 'error': str(e)}), 500)

## для удаления одного user
@app.route('/api/flask/users/<id>', methods=['DELETE'])
def delete_user(id):
  try:
    user = User.query.filter_by(id=id).first()  ## по id находим пользователя 
    if user:  ## если такой user существует, то
      db.session.delete(user) ## удаляем его 
      db.session.commit()
      return make_response(jsonify({'message': 'user deleted'}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404) 
  except Exception as e:
    return make_response(jsonify({'message': 'error deleting user', 'error': str(e)}), 500)   