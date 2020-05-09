from flask import request
from sqlalchemy import func
import json
from app import db
from app import app
from app import models


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
            item.cell = it_cell
            result = json.dumps({'cell': it_cell.cell.id})
            db.session.commit()
            return result

    cell = models.Cell.query.filter(models.Cell.items_cell == None)
    it_cel = models.Items_cell(cell=cell.first())
    item.cell = it_cel
    result = json.dumps({'cell': cell.first().id})
    db.session.add(it_cel)
    db.session.commit()
    return result
