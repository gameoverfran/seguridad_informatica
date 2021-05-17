import json
import math
import os
from time import sleep

import requests
from requests import get

from getters_maker import get_cookies, get_insta_query, get_request_hash


def save_media(link, path):
    reintentos = 3
    sleep_time = 10  # 1 seg
    reintentos_actuales = 0
    obtenido = False
    while not obtenido and reintentos_actuales < reintentos:
        resp_media = get(link)
        if resp_media.status_code == 200:
            img = open(path, "wb")
            img.write(resp_media.content)
            img.close()
            obtenido = True
        else:
            reintentos_actuales += 1
            sleep(sleep_time)

    return obtenido


def get_user_photos(id_user_photos_wnt, username, dir_name, session_id, num_photos_wnt):
    reintentos_maximos = 3
    sleep_time = 10  # 1 seg
    variables = {
        'id': id_user_photos_wnt,
        'first': 50
    }
    params = {
        "query_hash": get_request_hash()['multimedia'],
        "variables": json.dumps(variables)
    }
    has_next_page = True
    reintentos_actuales = 0
    error = False
    while has_next_page and reintentos_actuales < reintentos_maximos:
        res = requests.get(get_insta_query(), params=params, cookies=get_cookies(session_id, JSON_codification=False))
        if res.status_code == 200:
            print("Obteniendo fotos (con su información) de " + username + "...")
            reintentos_actuales = 0
            try:
                has_next_page = __get_photos_from_requests(variables, res.json(), dir_name,
                                                           num_photos_wnt)
                if has_next_page:
                    params["variables"] = json.dumps(variables)
                    sleep(sleep_time)
            except Exception as err:
                print("Se produjo un error en get_user_photos: ", err)
                reintentos_actuales = reintentos_maximos
        else:
            reintentos_actuales += 1
            sleep(sleep_time)
            error = True
    if not error:
        print("Todas las fotos de " + username + " han sido obtenidas")
        print("------------------------------------------------------")

    return reintentos_actuales < reintentos_maximos


nro_media = 1  # variable global para sumar la cantidad de media descargada hasta el momento


def __get_photo_info(node, file_name, personal_path):
    full_photo_info_dict = dict()
    full_photo_info_dict["__typename"] = node["__typename"]
    full_photo_info_dict["id"] = node["id"]
    full_photo_info_dict["gating_info"] = node["gating_info"]
    full_photo_info_dict["sensitivity_friction_info"] = node["sensitivity_friction_info"]
    full_photo_info_dict["dimensions_height"] = node["dimensions"]["height"]
    full_photo_info_dict["dimensions_width"] = node["dimensions"]["width"]
    full_photo_info_dict["is_video"] = node["is_video"]
    full_photo_info_dict["tracking_token"] = node["tracking_token"]
    if full_photo_info_dict["is_video"]:
        full_photo_info_dict["has_audio"] = node["has_audio"]
        full_photo_info_dict["video_url"] = node["video_url"]
        full_photo_info_dict["video_view_count"] = node["video_view_count"]
    full_photo_info_dict["text"] = node["edge_media_to_caption"]["edges"]
    full_photo_info_dict["edge_media_to_comment_count"] = node["edge_media_to_comment"]["count"]
    full_photo_info_dict["comments_disabled"] = node["comments_disabled"]
    full_photo_info_dict["taken_at_timestamp"] = node["taken_at_timestamp"]
    full_photo_info_dict["edge_media_preview_like_count"] = node["edge_media_preview_like"]["count"]
    full_photo_info_dict["location"] = node["location"]
    if not os.path.isfile(personal_path + file_name):
        with open(os.path.join(personal_path, file_name), 'w') as file:
            json.dump(full_photo_info_dict, file, indent=1)
    else:
        os.remove(os.path.join(personal_path, file_name))
        with open(os.path.join(personal_path, file_name), 'w') as file:
            json.dump(full_photo_info_dict, file, indent=1)

    return full_photo_info_dict


def __get_photos_from_requests(variables, data_resp, dir_name, num_photos_wnt, photo_format=".jpg",
                               video_format=".mp4"):
    global nro_media

    folder_name = dir_name
    data_resp = data_resp["data"]["user"]["edge_owner_to_timeline_media"]
    i = 0
    while i < len(data_resp["edges"]) and nro_media <= num_photos_wnt:
        node = data_resp["edges"][i]["node"]
        if node["__typename"] == "GraphSidecar":
            nro_img = 0
            for img in node["edge_sidecar_to_children"]["edges"]:
                if not save_media(img["node"]["display_url"],
                                  os.path.join(folder_name, str(nro_media) + "_" + str(nro_img) + photo_format)):
                    raise Exception("Error al guardar Sidecar")
                nro_img += 1
        else:
            link = "display_url"
            ext = photo_format
            if node["__typename"] == "GraphVideo":
                link = "video_url"
                ext = video_format
            if not save_media(node[link], os.path.join(folder_name, str(nro_media) + ext)):
                raise Exception("Error al guardar " + ext)
        __get_photo_info(node, str(nro_media) + "_info", dir_name)
        nro_media += 1
        i += 1

    if data_resp["page_info"]["has_next_page"] and nro_media <= num_photos_wnt:
        variables["after"] = data_resp["page_info"]["end_cursor"]
        return True

    return False
