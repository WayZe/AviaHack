import json
from datetime import datetime
from typing import List

from flask import request
from sqlalchemy import func

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


@app.route('/get_available_cell', methods=['POST'])
def put_item():
    """
    Сортирует товар по ячейкам. Если ячейка для заказа не выделена, то ячейка выделяется и в item записывается ее id
    Если ячейка для заказа выделена, то в item записывается ее id
    Если ячейка для заказа выделена, но переполнена, то создается новая ячейка и ее id привязывается к item
    """
    barcode = request.form.get('barcode')
    item = models.Item.query.filter_by(barcode=barcode).first()
    if item.cell is not None:
        result = json.dumps({'cell': item.cell.id})
        return result
    delivery_item = models.Item.query.filter(models.Item.delivery == item.delivery, models.Item.cell != None)
    delivery_cells = delivery_item.with_entities(models.Item.cell_id, models.Item.cell,
                                                 func.count(models.Item.cell)).group_by(models.Item.cell)

    for c in delivery_cells.all():
        it_cell = models.Items_cell.query.get(c[0])
        if it_cell.cell.capacity > c[2]:
            #item.cell = it_cell
            #db.session.commit()
            return json.dumps({'cell': it_cell.cell.id})

    cell = models.Cell.query.filter(models.Cell.items_cell == None)
    it_cel = models.Items_cell(cell=cell.first())
    #item.cell = it_cel
    db.session.add(it_cel)
    db.session.commit()
    return json.dumps({'cell': cell.first().id})


@app.route('/put_in_cell', methods=['POST'])
def put_item():
    barcode = request.form.get('barcode')
    cell_id = request.form.get('cell')
    item = models.Item.query.filter_by(barcode=barcode).first()
    item.cell = models.Items_cell.query.filter_by(id=cell_id).first()
    return json.dumps({'barcode': item.barcode, 'cell': item.cell.id})

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

    deliveries = models.Delivery.query.filter_by(client_id=client_id).all()  # type: List[Delivery]
    for delivery in deliveries:
        items1 = models.Item.query.filter_by(delivery_id=delivery.id).all()  # type: List[Item]
        dev = {}
        for item in items1:
            dev[f'Item {item.id}'] = item.__dict__
            del dev[f'Item {item.id}']['_sa_instance_state']
        jsons[f'Delivery {delivery.id}'] = dev

    return json.dumps(str(jsons).replace('\'', ''))


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

    return


@app.route('/return_item', methods=['POST'])
def return_item():
    barcode = request.form.get('barcode')
    item = models.Item.query.filter_by(barcode=barcode).first()
    return_it = models.Return()
    item._return = return_it
    db.session.commit()
    return json.dumps({'return_id': return_it.id, 'item_id': item.id})
