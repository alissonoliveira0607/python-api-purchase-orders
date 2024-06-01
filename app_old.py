"""
- How To
Create routes from API
GET purchase_order -> DONE
GET purchase_order_by_id -> DONE
GET purchase_order_items -> DONE
POST purchase_orders -> DONE
POST purchase_order_items
"""

# O pacote jsonify permite trabalhar com json
from flask import Flask, jsonify, request
import logging

logging.basicConfig(level=logging.INFO, filename="app.log", format="%(asctime)s - %(levelname)s - %(message)s")


app = Flask(__name__)

purchase_orders = [
 {
  "id": 1,
  "order_number": "12345",
  "order_date": "2019-01-01",
  "order_status": "pending",
  "description": "Order",
  "order_items": [
   {
    "item_id": 1,
    "item_name": "item 1",
    "item_price": 100,
 }
  ]
 }
]

# Rota GET purchase_orders Retorna todos os pedidos
@app.route('/purchase_orders', methods=['GET'])
def get_purchase_orders():
    if request.method != 'GET':
        return jsonify({'error': 'Method not allowed'}), 405
    else:
        headers = request.headers
        if headers:
            try:
                # Pegando os headers da requisição recebida
                for key,value in headers.items():
                    logging.info(f"{key}: {value}")  # Logando os headers
            except Exception as e:
                logging.error(e)
                print(e)
        logging.info(f"Response Body: {purchase_orders}")        
        return jsonify(purchase_orders)


# ROTA GET purchase orders by id retorna um pedido quando passado o parametro do id
# PAra trabalhar com rotas que recebem parametros definimos <int:id>
@app.route('/purchase_orders_by_id/<int:id>', methods=['GET'])
def get_purchase_order_by_id(id):
    if id<= 0:
        return jsonify({"error": "Id informado não pode ser menor ou igual a 0"}), 400
    for purchase_order in purchase_orders:
        # Acessando o atributo 'id' do payload para verificar se corresponde ao id informado no momento da requisição
        if purchase_order['id'] == id:
            logging.info(f"Response Body: {purchase_order}")        
            return jsonify(purchase_order)
    return jsonify({"error": "Id informado não é valido"}), 400


# Rota POST para criar um pedido
@app.route('/purchase_orders', methods=['POST'])
def post_purchase_orders():
    if request.method!= 'POST':
        return jsonify({'error': 'Method not allowed'}), 405
    else:
        data = request.get_json()  # Resgatando o payload que chega an requisição

        # Montando o payload
        data_purchase_orders = {
            "id": data['id'],
            "order_number": data['order_number'] if data['order_number'] else None,
            "order_date": data['order_date'] if data['order_date'] else None,
            "order_status": data['order_status']if data['order_status'] else None,
            "description": data['description'] if data['description'] else None,
            "order_items": []
        }
        for purchase_order in purchase_orders:
            if purchase_order['id'] == data['id']:
                return jsonify({"error": "Id informado já existe"}), 400

        purchase_orders.append(data_purchase_orders)  # Adicionando o objeto a lista
        logging.info(f"Response Body: {data_purchase_orders}")        
        return jsonify({"messages": data_purchase_orders}), 200




# Rota que retorna um pedido por id do item
@app.route('/purchase_orders/<int:id>/items', methods=['GET'])
def get_purchase_order_by_items(id):
    if id <= 0:
        return jsonify({"error": "Id informado não pode ser menor ou igual a 0"}), 400
    
    # for purchase_order in purchase_orders:  # Percorre a lista de purcha_orders
    #     for item in purchase_order['order_items']: # Percorre o nó de items para cada item contido a cada interação do purchase_order da chave order_items
    #         if item['item_id'] == item_id:  # Verifica se o item_id corresponde ao parametro passado do item_id
    #             logging.info(f"Response Body: {purchase_order}")
    #             return jsonify(purchase_order)

    for purchase_order in purchase_orders:  # Percorre a lista de purcha_orders
        if purchase_order['id'] == id:
            return jsonify(purchase_order['order_items'])   # Retornando o nó de items caso o parametro passado como id exista
        
    return jsonify({"error": "Id informado não é valido"}), 400


# Rota que retorna items a um pedido
@app.route('/purchase_orders/<int:id>/items', methods=['POST'])
def post_purchase_order_by_items(id):
    if id <= 0:
        return jsonify({"error": "Id informado não pode ser menor ou igual a 0"}), 400
    data = request.get_json()
    for purchase_order in purchase_orders:  # Percorre a lista de purcha_orders
        if purchase_order['id'] == id:
            purchase_orders.append({
                "item_id": data['item_id'],
                "item_name": data['item_name'],
                "item_price": data['item_price']
            })
            return jsonify(purchase_order)   # Retornando o nó de items caso o parametro passado como id exista
        
    return jsonify({"error": "Id informado não é valido"}), 400


app.run(debug=True, host='0.0.0.0', port=5000)





