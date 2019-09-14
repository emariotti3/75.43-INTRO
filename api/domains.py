from flask import abort, make_response
import api.domainResolver as dr

# Data to serve with our API
dominios = {
    'domain': 'fi.uba.ar',
    'ip': '157.92.49.38',
    'custom': 'false'
}

dominios = {}

dominios_custom = {}

def obtener_ip_nombre_dom(nombre_dominio):
    if nombre_dominio not in dominios:
        addresses = dr.resolver(nombre_dominio)
        dominios[nombre_dominio] = [0, [x.address for x in addresses]]
    dominio = dominios[nombre_dominio]
    direccion = dominio[1][dominio[0]]
    dominio[0] = (dominio[0] + 1) % len(dominio[1])
    return direccion

def obtener_dom_query(**kwargs):
    return [dominio]

def crear_dom():
    return dominio

def editar_dom(nombre_dominio):
    return dominio

def borrar_dom(nombre_dominio):
    return dominio