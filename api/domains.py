from flask import abort, make_response

# Data to serve with our API
domain = {
    'domain': 'fi.uba.ar',
    'ip': '157.92.49.38',
    'custom': 'false'
}

def obtener_ip_nombre_dom(nombre_dominio):
    return domain

def obtener_dom_query(**kwargs):
    return [domain]

def crear_dom():
    return domain

def editar_dom(nombre_dominio):
    return domain

def borrar_dom(nombre_dominio):
    return domain