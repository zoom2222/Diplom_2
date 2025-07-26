from data import DataForAuth, DataForOrder

def modify_auth_body(key, value):
    body = DataForAuth.REGISTER_BODY.copy()
    body[key] = value
    return body

def modify_order_body(key, value):
    body = DataForOrder.CREATE_ORDER_BODY.copy()
    body[key] = value
    return body
