import json
from datetime import datetime, timedelta

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
def get_avail_cell():
    """
    Сортирует товар по ячейкам. Если ячейка для заказа не выделена, то ячейка выделяется и в item записывается ее id
    Если ячейка для заказа выделена, то в item записывается ее id
    Если ячейка для заказа выделена, но переполнена, то создается новая ячейка и ее id привязывается к item
    """
    req_json = request.get_json()
    barcode = req_json['barcode']

    item = models.Item.query.filter_by(barcode=barcode).first()

    if not item:
        return json.dumps({'error': 'Такой вещи не существует'}), 404

    if item.cell is not None:
        return json.dumps({'error': 'Такая вещь уже размещена'}), 409

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
    req_json = request.get_json()

    barcode = req_json['barcode']
    cell_id = req_json['cell']

    item = models.Item.query.filter_by(barcode=barcode).first()
    item.cell = models.Items_cell.query.filter_by(id=cell_id).first()

    return json.dumps({'barcode': item.barcode, 'cell': item.cell.id}), 201


@app.route('/give_item', methods=['POST'])
def give_item():
    """Получение списка товаров по телефону и ФИО.

    Пример запроса: curl -X POST -d "phone=12"  localhost:5000/give_item
    """
    req = request.get_json()
    us_code = req['userCode']  # type: str

    if us_code is not None:
        deliv = models.Delivery.query.filter_by(user_code=us_code).first()  # type: Delivery
    else:
        return json.dumps({'error': f'Не переданы данные о доставке'}), 404

    if not deliv:
        return json.dumps({'error': f'Нет заказа с пользовательским кодом: {us_code}'}), 404

    res_items = []
    _items = models.Item.query.filter_by(delivery=deliv).all()

    for it in _items:
        res_it = dict.fromkeys(['id', 'barcode', 'deliveredDate', 'cellId', 'returnId'])
        res_it['id'] = it.id
        res_it['barcode'] = it.barcode
        res_it['deliveredDate'] = it.delivered_date.isoformat() if it.delivered_date else None
        res_it['cellId'] = it.cell.cell.id if it.cell and it.cell.cell else None
        res_it['returnId'] = it._return.id if it._return else None
        res_items.append(res_it)

    return json.dumps({'id': deliv.id, 'userCode': us_code, 'items': res_items})


@app.route('/fix_given_item', methods=['POST'])
def fix_given_item():
    """Установка времени, когда был отдан товар клиенту.
    Считаем его как флаг о том, что товар отдан,
    а также по нему будет рассчитан срок возврата.
    Входные данные: штрих-код.

    Пример запроса: curl -X POST -d "barcode=12"  localhost:5000/fix_given_item
    """
    req = request.get_json()
    dev_id = req['id']
    barcodes = req['items']

    if barcodes:
        for barcode in barcodes:
            item = models.Item.query.filter_by(barcode=barcode).first()  # type: Item

            if item:
                item.cell = None
                item.delivered_date = datetime.now()
        db.session.commit()
    else:
        return json.dumps({'error': f'Не передан штрих-код'}), 400

    return json.dumps({'id': dev_id, 'items': barcodes}), 201


@app.route('/return_item', methods=['POST'])
def return_item():
    req = request.get_json()
    barcode = req['barcode']

    item = models.Item.query.filter_by(barcode=barcode).first()

    if not item:
        return json.dumps({'error': f'Вещь не найдена со штрих-кодом: {req["barcode"]}'}), 404

    if item._return:
        return json.dumps({'error': 'Товар уже вернули'}), 409

    if (item.delivered_date - datetime.now()) > timedelta(days=21):
        return json.dumps({'error': f'Возврат невозможен, истёк срок возврата: {item.barcode}'}), 403
    return_it = models.Return()
    item._return = return_it
    db.session.commit()
    return json.dumps({'returnId': return_it.id, 'barcode': item.barcode}), 201


@app.route('/insert_data', methods=['POST'])
def insert_data():
    c = models.Client(phone='89745612321', passport='4568789456', name='IlyaGreen')
    c2 = models.Client(phone='89741234567', passport='4589621234', name='KarolGreen')
    d = models.Delivery(client=c, user_code=123456)
    d2 = models.Delivery(client=c2, user_code=123457)
    d3 = models.Delivery(client=c2, user_code=123458)
    cell = models.Cell(capacity=3)
    cell1 = models.Cell(capacity=3)
    cell2 = models.Cell(capacity=3)
    cell3 = models.Cell(capacity=3)
    cell4 = models.Cell(capacity=3)
    cell5 = models.Cell(capacity=3)
    cell6 = models.Cell(capacity=3)
    it_cel = models.Items_cell(cell=cell)
    i = models.Item(barcode=12, delivery=d, cell=it_cel)
    it = models.Item(barcode=14, delivery=d)
    it1 = models.Item(barcode=15, delivery=d2)
    it2 = models.Item(barcode=16, delivery=d3)
    it3 = models.Item(barcode=17, delivery=d3)
    db.session.add(c)
    db.session.add(c2)
    db.session.add(d)
    db.session.add(d2)
    db.session.add(d3)
    db.session.add(cell)
    db.session.add(cell1)
    db.session.add(cell2)
    db.session.add(cell3)
    db.session.add(cell4)
    db.session.add(cell5)
    db.session.add(cell6)
    db.session.add(it_cel)
    db.session.add(i)
    db.session.add(it)
    db.session.add(it1)
    db.session.add(it2)
    db.session.add(it3)
    db.session.commit()
    return 'OK'
