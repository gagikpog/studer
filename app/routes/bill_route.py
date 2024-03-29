from flask import render_template, flash, redirect, url_for, send_from_directory, request, jsonify, abort
from app import db, api
from app.forms import LoginForm
from app.models import User, Bill
from flask_restful import Resource, reqparse
from flask_login import current_user

class Bill_api(Resource):
    """
        RESTful API
    """
    
    #Запрос на получение задач
    def get(self, id=None):
        if id == None:
            abort(404)
            # # в данный момент нет необходимости получения всех задач отсюда
            # res = []
            # for bi in Bill.query.all():
            #     #Добавляем все задачи в list
            #     res.append(bi.to_dict())
            # #Возвращаем json с задачами
            # return jsonify(res)
        else:
            #Если дан id, то находим задачу с таким id
            obj = Bill.query.filter_by(id=id).first()
            if obj and obj.status != 'Удалено':
                #Если задача с таким id найдена, то возвращаем
                return jsonify(obj.to_dict())
            else: 
                #Иначе, возвращаем ошибку
                res = {'status': 'error', 'message': 'По вашему запросу ничего не найдено'}
                return jsonify(res)


    #Запрос на добавление новой задачи
    def post(self):
        # Если запрос неправильный, то возвращаем 400 Bad Request
        if not request.json:
            abort(400)
        # Если пользователь не авторизован или он студент, то он не имеет право создавать задачи
        if not current_user.is_authenticated:
            abort(401)

        if current_user.activity == 'Студент':
            abort(403)

        json = request.json

        # Проверка наличие обязательних данных
        if not json['title'] or not json['description'] or not json['sum']:
            res = {'status': 'error', 'message': 'Не заполнены обязательних поля'}
            return jsonify(res);

        #Создаем новый объект
        bill = Bill()
        bill.init_of_dict(json)
        # 
        current_user.bills.append(bill)

        try:
            #Пытаемся добавить полученные данные в БД
            db.session.add(bill)
            db.session.commit()
        except:
            #Если не получилось, то возвращаем ошибку
            res = {'status': 'error', 'message': 'Такие данные уже существуют'}
            return jsonify(res)
        res = {'status': 'done', 'message': 'Данные добавлены'}
        return jsonify(res)

    #Запрос на обновление данных
    def put(self, id=None):
        #Если запрос неправильный, то возвращаем 400 Bad Request
        if not request.json:
            abort(400)
            return ''
        json = request.json
        #Создаем новый объект
        bill = Bill()
        bill.init_of_dict(json)
        if not bill.id:
            #Если id не был дан, то возвращаем ошибку
            res = {'status': 'error', 'message': 'Не найден обязательный параметр: id'}
            return jsonify(res)
        else:
            if not int(bill.id) in list(map(lambda item: int(item.id), current_user.bills)):
                return jsonify({'status': 'error', 'message': 'У вас нет прав на изменение этой задачи!'})
            #Находим задачу и обновляем данные
            if Bill.query.filter_by(id = bill.id).first() != None:
                Bill.query.filter_by(id = bill.id).update(bill.to_dict())
                db.session.commit()
                res = {'status': 'done', 'message': 'Данные обновлены'}
                return jsonify(res)
            else:
                #Если задача не найдена, то возвращаем ошибку
                res = {'status': 'error', 'message': 'Данные с таким id не найдены'}
                return jsonify(res)


    #Запрос на удаление задачи
    def delete(self, id=None):
        if id == None:
            #Если id не был дан, то возвращаем ошибку
            res = {'status': 'error', 'message': 'Не найден обязательный параметр: id'}
            return jsonify(res)

        query = Bill.query.filter_by(id = id)
        if query.first() != None:
            #Находим задачу и удаляем её
            if not int(id) in list(map(lambda item: int(item.id), current_user.bills)):
                return jsonify({'status': 'error', 'message': 'У вас нет прав на удаление этой задачи!'})
            bill = query.first()
            bill.status = 'Удалено'
            db.session.commit()
            res = {'status': 'done', 'message': 'Запись удалена!'}
            return jsonify(res)
        else:
            #Если задача не найдена, то возвращаем ошибку
            res = {'status': 'error', 'message': 'Данные с таким id не найдены'}
            return jsonify(res)


api.add_resource(Bill_api, '/api/bill', '/api/bill/', '/api/bill/<id>')
