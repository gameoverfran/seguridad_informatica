import json
from urllib.parse import quote


def get_cookies(session_id_str, user_id=-1, first=-1, after=-1, JSON_codification=True, session_id=True, debug=False):
    cookiesAux = dict()
    if user_id != -1:
        cookiesAux["id"] = user_id

    if first != -1:
        cookiesAux["first"] = first

    if after != -1:
        cookiesAux["after"] = after

    if session_id:
        # Obtenemos la session_id para que instagram no nos bloquee las peticiones, la JSON_codification a False
        cookiesAux["sessionid"] = session_id_str

    if JSON_codification:
        # La respuesta será el objeto (dictionary) JSON codificado, con el cual podremos realizar la petición
        return quote(json.dumps(cookiesAux))
    else:
        return cookiesAux


def get_request_hash(debug=False):
    if debug:
        print("Devolviendo el request hash")
    dictionary = dict()
    dictionary['multimedia'] = '003056d32c2554def87228bc3fd9668a'
    dictionary['followers'] = 'c76146de99bb02f6415203be841dd25a'
    dictionary['following'] = 'd04b0a864b4b54837c0d870b0e77e076'
    return dictionary


def get_insta_query(debug=False):
    if debug:
        print("Devolviendo insta url")
    return "https://www.instagram.com/graphql/query/?query_hash="
