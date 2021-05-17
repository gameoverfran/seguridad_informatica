import json
import math
import os
from datetime import datetime

import requests

from follow_getters import get_user_followers_ing
from getters_maker import get_cookies
from photos_getters import get_user_photos


def get_user_id(data_json, debug=False):
    user_id = data_json["graphql"]["user"]["id"]
    if debug:
        print("ID: " + user_id)
    return user_id


def get_user_biography(data_json, debug=False):
    biography = data_json["graphql"]["user"]["biography"]
    if debug:
        print("Biography: " + biography)
    return biography


def get_user_edge_followed_by(data_json, debug=False):
    edge_followed_by = data_json["graphql"]["user"]["edge_followed_by"]["count"]
    if debug:
        print("followed_by_count: " + str(edge_followed_by))
    return edge_followed_by


def get_user_edge_follow(data_json, debug=False):
    edge_follow = data_json["graphql"]["user"]["edge_follow"]["count"]
    if debug:
        print("Follow_count: " + str(edge_follow))
    return edge_follow


def get_user_full_name(data_json, debug=False):
    full_name = data_json["graphql"]["user"]["full_name"]
    if debug:
        print("Full_name: " + str(full_name))
    return full_name


def get_user_name(data_json, debug=False):
    user_name = data_json["graphql"]["user"]["username"]
    if debug:
        print("User_name: " + str(user_name))
    return user_name


def get_is_business_account(data_json, debug=False):
    is_business_account = data_json["graphql"]["user"]["is_business_account"]
    if debug:
        print("Is_business_account: " + str(is_business_account))
    return is_business_account


def get_is_professional_account(data_json, debug=False):
    is_professional_account = data_json["graphql"]["user"]["is_professional_account"]
    if debug:
        print("Is_professional_account: " + str(is_professional_account))
    return is_professional_account


def get_is_joined_recently(data_json, debug=False):
    is_joined_recently = data_json["graphql"]["user"]["is_joined_recently"]
    if debug:
        print("Is_joined_recently: " + str(is_joined_recently))
    return is_joined_recently


def get_user_business_email(data_json, debug=False):
    business_email = data_json["graphql"]["user"]["business_email"]
    if debug:
        print("Business_email: " + str(business_email))
    return business_email


def get_user_business_phone_number(data_json, debug=False):
    business_phone_number = data_json["graphql"]["user"]["business_phone_number"]
    if debug:
        print("Business_phone_number: " + str(business_phone_number))
    return business_phone_number


def get_user_business_category_name(data_json, debug=False):
    business_category_name = data_json["graphql"]["user"]["business_category_name"]
    if debug:
        print("Business_phone_number: " + str(business_category_name))
    return business_category_name


def get_is_verified(data_json, debug=False):
    is_verified = data_json["graphql"]["user"]["is_verified"]
    if debug:
        print("Is_verified: " + str(is_verified))
    return is_verified


def get_is_private(data_json, debug=False):
    is_private = data_json["graphql"]["user"]["is_private"]
    if debug:
        print("Is_private: " + str(is_private))
    return is_private


def get_edge_mutual_followed_by_count(data_json, debug=False):
    edge_mutual_followed_by_count = data_json["graphql"]["user"]["edge_mutual_followed_by"]["count"]
    if debug:
        print("Is_verified: " + str(edge_mutual_followed_by_count))
    return edge_mutual_followed_by_count


def get_user_external_url(data_json, debug=False):
    external_url = data_json["graphql"]["user"]["external_url"]
    if debug:
        print("External_url: " + str(external_url))
    return external_url


def get_user_timeline_media_count(data_json, debug=False):
    media_count = data_json["graphql"]["user"]["edge_owner_to_timeline_media"]["count"]
    if debug:
        print("Media_count: " + str(media_count))
    return media_count


def get_connected_fb_page(data_json, debug=False):
    connected_fb_page = data_json["graphql"]["user"]["connected_fb_page"]
    if debug:
        print("Connected_fb_page: " + str(connected_fb_page))
    return connected_fb_page


def get_user_profile_photo(data_json, personal_path, username, debug=False):
    profile_url = data_json["graphql"]["user"]["profile_pic_url_hd"]
    res_img = requests.get(profile_url)
    img = open(personal_path + "0profile_" + username + ".jpg", "wb")
    img.write(res_img.content)
    img.close()
    if debug:
        print("La imagen de perfil del usuario %s ha sido obtenida" % username)


def get_user_info(username, dir_name, session_id, boolean_followers, boolean_following, num_photos_wnt=math.inf,
                  debug=False):
    info_user = dict()
    res = requests.get(get_request_user_info(username), cookies=get_cookies(session_id, JSON_codification=False))
    if res.status_code == 200:
        data_json = res.json()
        # print(data_json["graphql"]["user"]["edge_owner_to_timeline_media"])
        # json_formatted_str = json.dumps(res.json(), indent=1)
        # print(json_formatted_str)
        print("------------------------------------------------------")
        print("| Obteniendo información del usuario: " + username + " |")
        print("------------------------------------------------------")
        personal_path, photos_dir_path = create_user_dir(username, dir_name, debug)
        info_user["personal_path"] = personal_path
        info_user["photos_dir_path"] = photos_dir_path
        info_user["id"] = get_user_id(data_json, debug)
        info_user["full_name"] = get_user_full_name(data_json, debug)
        info_user["user_name"] = get_user_name(data_json, debug)
        info_user["biography"] = get_user_biography(data_json, debug)
        info_user["is_private"] = get_is_private(data_json, debug)
        info_user["timeline_media_count"] = get_user_timeline_media_count(data_json, debug)
        info_user["followed_by_count"] = get_user_edge_followed_by(data_json, debug)
        info_user["follow_count"] = get_user_edge_follow(data_json, debug)
        info_user["is_business_account"] = get_is_business_account(data_json, debug)
        info_user["is_professional_account"] = get_is_professional_account(data_json, debug)
        info_user["is_joined_recently"] = get_is_joined_recently(data_json, debug)
        info_user["business_email"] = get_user_business_email(data_json, debug)
        info_user["business_phone_number"] = get_user_business_phone_number(data_json, debug)
        info_user["business_category_name"] = get_user_business_category_name(data_json, debug)
        info_user["is_verified"] = get_is_verified(data_json, debug)
        info_user["is_private"] = get_is_private(data_json, debug)
        info_user["mutual_followed_by_count"] = get_edge_mutual_followed_by_count(data_json, debug)
        info_user["external_url"] = get_user_external_url(data_json, debug)
        info_user["connected_fb_page"] = get_connected_fb_page(data_json, debug)
        __create_info_user_json(info_user, info_user["personal_path"], username, debug=debug, overwrite=True)
        if debug:
            print("------------------------------------------------------")
        # Obtenemos el resto de la info...
        get_user_profile_photo(data_json, info_user["photos_dir_path"], username, debug)
        get_user_photos(info_user['id'], info_user['user_name'], info_user["photos_dir_path"],
                        session_id, num_photos_wnt)
        get_user_followers_ing(info_user["id"], info_user["user_name"], info_user["personal_path"], session_id,
                               boolean_followers, boolean_following)

    elif res.status_code == 404:
        print("El usuario que has introducido no existe")
        print("------------------------------------------------------")
    else:
        print("Error %d al realizar la petición." % res.status_code)
    return info_user


def __create_info_user_json(full_info_dict, personal_path, username, overwrite=False, debug=False):
    file_name = username + "_personal_info.json"
    if not os.path.isfile(personal_path + file_name):
        with open(os.path.join(personal_path, file_name), 'w') as file:
            json.dump(full_info_dict, file, indent=1)
        if debug:
            print("El archivo de información del usuario " + username + " ha sido creado")
    else:
        if debug:
            print("El archivo de información con fecha: " + str(datetime.now()).split(" ")[
                0] + " del usuario: " + username + " ya estaba creado. La sobreescritura de dicho archivo esta en: " + str(
                overwrite))
        if overwrite:
            os.remove(os.path.join(personal_path, file_name))
            with open(os.path.join(personal_path, file_name), 'w') as file:
                json.dump(full_info_dict, file, indent=1)


def get_request_user_info(user):
    return "https://www.instagram.com/" + user + "/?__a=1"


def create_user_dir(username, dir_name, debug=False):
    personal_path = dir_name + '/' + username + '_info'
    if not os.path.isdir(personal_path):
        os.mkdir(personal_path)
        if debug:
            print("La carpeta del usuario " + username + " ha sido creada")
    else:
        if debug:
            print("La carpeta del usuario " + username + " ya estaba creada")

    personal_path = personal_path + '/' + str(datetime.now()).split(" ")[0]
    if not os.path.isdir(personal_path):
        os.mkdir(personal_path)
        if debug:
            print("La carpeta del usuario " + username + " de hoy ha sido creada")
    else:
        if debug:
            print("La carpeta del usuario " + username + " de hoy ya estaba creada")

    photos_dir_path = personal_path + '/' + username + '_photos/'
    if not os.path.isdir(photos_dir_path):
        os.mkdir(photos_dir_path)
        if debug:
            print("La carpeta de fotos del usuario " + username + " ha sido creada")
    else:
        if debug:
            print("La carpeta de fotos del usuario " + username + " ya estaba creada")

    return personal_path, photos_dir_path
