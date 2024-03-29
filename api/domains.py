from flask import abort, make_response
import api.domainResolver as dr

HTTP_CREATED = 201
HTTP_BAD_REQUEST = 400
HTTP_NOT_FOUND = 404
IP_MAX_VALUE = 255
IP_MIN_VALUE = 0

dominios_guardados = {}

dominios_custom = {}

def obtener_dominio(domain):
    """
    Esta funcion maneja el request GET /api/domains/{domain}

    :return:      200 con la direccion del dominio pedido, 404 not found
    """
    if domain in dominios_custom:
        return dominios_custom[domain]
    if domain not in dominios_guardados:
        try:
            addresses = dr.resolver(domain)
        except:
            return abort(HTTP_NOT_FOUND, 'domain not found')
        dominios_guardados[domain] = [0, [x.address for x in addresses]]
    dominio = dominios_guardados[domain]
    direccion = dominio[1][dominio[0]]
    dominio[0] = (dominio[0] + 1) % len(dominio[1])
    return _crear_response_dominio(domain, direccion, False)

def _crear_response_dominio(dominio, ip, es_dominio_custom):
    return {'domain': dominio, 'ip': ip, 'custom': es_dominio_custom}

def obtener_dominios(q = None):
    """
    Esta funcion maneja el request GET /api/custom-domains

    :return:        200 lista de custom domains
    """
    dominios = list(dominios_custom.values())
    return {'items': list(filter(lambda dominio: q in dominio.get('domain'), dominios)) if q else dominios}

def _validar_parametros(dominio, ip):
    if not dominio or not ip or not _ip_valida(ip):
        return abort(HTTP_BAD_REQUEST, 'payload is invalid')

def _ip_valida(ip):
    rangos_ip = ip.split(".")
    if len(rangos_ip) != 4:
        return False
    for valor in rangos_ip:
        if not valor.isdigit() or (int(valor) > IP_MAX_VALUE or int(valor) < IP_MIN_VALUE):
            return False
    return True

def crear_dominio(**kwargs):
    """
    Esta funcion maneja el request POST /api/custom-domains

    :param body:  dominio a sobreescribir
    :return:      201 dominio creado, 400 bad request
    """
    dominio_custom = kwargs.get('body')
    dominio = dominio_custom.get('domain')
    ip = dominio_custom.get('ip')

    _validar_parametros(dominio, ip)
    if dominio in dominios_custom.keys():
        return abort(HTTP_BAD_REQUEST, 'custom domain already exists')
    dominio_custom['custom'] = True
    dominios_custom[dominio] = dominio_custom
    return make_response(dominio_custom, HTTP_CREATED)

def editar_dominio(domain, **kwargs):
    """
    Esta funcion maneja el request PUT /api/custom_domains/{domain}

    :domain body:  dominio que se quiere modificar
    :return:        200 dominio, 404 not found, 400 invalid payload
    """
    dominio_custom = kwargs.get('body')
    dominio = dominio_custom.get('domain')
    ip = dominio_custom.get('ip')

    _validar_parametros(dominio, ip)
    if domain not in dominios_custom.keys():
        return abort(HTTP_NOT_FOUND, 'domain not found')
    if domain != dominio:
        return abort(HTTP_BAD_REQUEST, 'payload is invalid')

    dominio_custom['custom'] = True
    dominios_custom[domain] = dominio_custom
    return dominio_custom

def borrar_dominio(domain):
    """
    Esta funcion maneja el request DELETE /api/custom_domains/{domain}

    :nombre_dominio body:  dominio que se quiere eliminar
    :return:        200 dominio, 404 not found
    """
    if dominios_custom.pop(domain, None):
        return {'domain': domain}
    return abort(HTTP_NOT_FOUND, 'domain not found')
