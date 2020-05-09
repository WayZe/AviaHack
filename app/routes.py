from datetime import datetime
from typing import List

from flask import jsonify, request

from app import app, models, db
from app.models import Delivery, Item


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/client/<int:item_id>', methods=['GET', 'DELETE', 'POST', 'PUT'])
@app.route('/clients', methods=['GET', 'POST'])
def items(item_id=None):
    return models.Client.get_delete_put_post(item_id)


@app.route('/delivery/<int:item_id>', methods=['GET', 'DELETE', 'POST', 'PUT'])
@app.route('/deliveries', methods=['GET', 'POST'])
def get_delivery(item_id=None):
    return models.Delivery.get_delete_put_post(item_id)


@app.route('/item/<int:item_id>', methods=['GET', 'DELETE', 'POST', 'PUT'])
@app.route('/items', methods=['GET', 'POST'])
def get_item(item_id=None):
    return models.Item.get_delete_put_post(item_id)


@app.route('/return/<int:item_id>', methods=['GET', 'DELETE', 'POST', 'PUT'])
@app.route('/returns', methods=['GET', 'POST'])
def get_return(item_id=None):
    return models.Return.get_delete_put_post(item_id)


@app.route('/cell_delivery/<int:item_id>', methods=['GET', 'DELETE', 'POST', 'PUT'])
@app.route('/cells_deliveries', methods=['GET', 'POST'])
def get_celldelivery(item_id=None):
    return models.Items_cell.get_delete_put_post(item_id)


@app.route('/cell/<int:item_id>', methods=['GET', 'DELETE', 'POST', 'PUT'])
@app.route('/cells', methods=['GET', 'POST'])
def get_cell(item_id=None):
    return models.Cell.get_delete_put_post(item_id)


@app.route('/put_item', methods=['POST'])
def put_item():
    _barcode = request.form.get('barcode')
    item = models.Item.query.filter_by(barcode=_barcode).first()
    delivery_cells = models.Item.query.filter_by(delivery=item.delivery)
    for c in delivery_cells:
        pass
    return str(item.id)


@app.route('/give_item', methods=['POST'])
def give_item():
    """Получение списка товаров по телефону и ФИО.

    Пример запроса: curl -X POST -d "phone=12"  localhost:5000/give_item
    """
    phone = request.form.get('phone')  # type: str
    name = request.form.get('fio')  # type: str
    jsons = {}  # type: Dict

    if phone is not None:
        client_id = models.Client.query.filter_by(phone=phone).first().id  # type: int
    elif name is not None:
        client_id = models.Client.query.filter_by(name=name).first().id  # type: int
    else:
        print('Переданы неизвестные параметры')
        return {}

    print(models.Client.query.filter_by().all())

    deliveries = models.Delivery.query.filter_by(client_id=client_id).all()  # type: List[Delivery]
    for delivery in deliveries:
        items1 = models.Item.query.filter_by(delivery_id=delivery.id).all()  # type: List[Item]
        dev = {}
        for item in items1:
            dev[f'Item {item.id}'] = item.__dict__
            del dev[f'Item {item.id}']['_sa_instance_state']
        jsons[f'Delivery {delivery.id}'] = dev

    return jsonify(str(jsons).replace('\'', ''))


@app.route('/fix_given_item', methods=['POST'])
def fix_given_item():
    """Установка времени, когда был отдан товар клиенту.
    Считаем его как флаг о том, что товар отдан,
    а также по нему будет рассчитан срок возврата.
    Входные данные: штрих-код.

    Пример запроса: curl -X POST -d "barcode=12"  localhost:5000/fix_given_item
    """
    barcodes = request.form.getlist('barcode')  # type: List[str]

    if barcodes is not None:
        for barcode in barcodes:
            item = models.Item.query.filter_by(barcode=barcode).first()  # type: Item
            item.delivered_date = datetime.now()
        db.session.commit()
    else:
        print('Не передан штрих-код')

    return {}
