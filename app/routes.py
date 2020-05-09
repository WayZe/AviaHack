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
    return models.CellDelivery.get_delete_put_post(item_id)


@app.route('/cell/<int:item_id>', methods=['GET', 'DELETE', 'POST', 'PUT'])
@app.route('/cells', methods=['GET', 'POST'])
def get_cell(item_id=None):
    return models.Cell.get_delete_put_post(item_id)
