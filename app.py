from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import logging
from purchase_orders.resources import PurchaseOrders, PurchaseOrdersById
from purchase_orders_items.resources import PurchaseOrdersItems  # importando o módulo do resources para o purchase orders items

logging.basicConfig(level=logging.INFO, filename="app.log", format="%(asctime)s - %(levelname)s - %(message)s")

# Instanciando o Flasks
app = Flask(__name__)
api = Api(app)


# Consumindo um recurso a partir do resources e expondo a rota
# Rota designada a criação de purchase_orders e listagem de todos os purchase_orders
api.add_resource(PurchaseOrders, '/purchase_orders')
api.add_resource(PurchaseOrdersById, '/purchase_orders_by_id/<int:id>')
api.add_resource(PurchaseOrdersItems, '/purchase_orders/<int:id>/items')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)