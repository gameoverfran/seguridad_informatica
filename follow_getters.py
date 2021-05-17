import json
import os
from datetime import datetime
from time import sleep

import requests

from getters_maker import get_request_hash, get_insta_query, get_cookies


def __get_follow_requests(variables, res_json, personal_path, json_piece):
    # json_formatted_str = json.dumps(res_json, indent=1)
    # print(json_formatted_str)
    full_info_dict = dict()
    file_name = json_piece + "_info.txt"

    for node in res_json["data"]["user"][str(json_piece)]["edges"]:
        node = node["node"]
        full_info_dict["id"] = node["id"]
        full_info_dict["username"] = node["username"]
        full_info_dict["full_name"] = node["full_name"]
        full_info_dict["is_private"] = node["is_private"]
        full_info_dict["is_verified"] = node["is_verified"]
        full_info_dict["followed_by_viewer"] = node["followed_by_viewer"]
        full_info_dict["requested_by_viewer"] = node["requested_by_viewer"]
        with open(os.path.join(personal_path, file_name), 'a+') as file:
            json.dump(full_info_dict, file, indent=1)
    if res_json["data"]["user"][str(json_piece)]["page_info"]["has_next_page"]:
        variables["after"] = res_json["data"]["user"][str(json_piece)]["page_info"]["end_cursor"]
        return True
    return False


def __get_user_followers(id_user, username, dir_name, session_id, param, action):
    reintentos_maximos = 3
    sleep_time = 10  # 1 seg
    variables = {
        'id': id_user,
        'first': 50
    }
    params = {
        "query_hash": param,
        "variables": json.dumps(variables)
    }
    has_next_page = True
    error = False
    reintentos_actuales = 0
    print("------------------------------------------------------")
    while has_next_page and reintentos_actuales < reintentos_maximos:
        res = requests.get(get_insta_query(), params=params, cookies=get_cookies(session_id, JSON_codification=False))
        if res.status_code == 200:

            print("Obteniendo " + action + " de " + username + "...")
            reintentos_actuales = 0
            try:
                if action == "followers":
                    has_next_page = __get_follow_requests(variables, res.json(), dir_name, 'edge_followed_by')
                else:
                    has_next_page = __get_follow_requests(variables, res.json(), dir_name, 'edge_follow')
                if has_next_page:
                    params["variables"] = json.dumps(variables)
                    sleep(sleep_time)
            except Exception as err:
                print("Se produjo un error en get_user_followers: ", err)
                reintentos_actuales = reintentos_maximos
                error = True
        else:
            reintentos_actuales += 1
            sleep(sleep_time)
    if not error:
        print("Todos los " + action + " de " + username + " han sido obtenidos")

    return reintentos_actuales < reintentos_maximos


def get_user_followers_ing(id_user, username, dir_name, session_id, boolean_followes, boolean_following):
    a = False
    b = False
    if boolean_followes:
        a = __get_user_followers(id_user, username, dir_name, session_id, get_request_hash()['followers'], 'followers')
    if boolean_following:
        b = __get_user_followers(id_user, username, dir_name, session_id, get_request_hash()['following'], 'following')
    return a and b
