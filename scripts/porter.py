#!/usr/bin/python
#coding:utf-8
import sys
from settings_local import conn_new, conn_old, c_new, c_old


def main():
    """
    Main function of portnig to new DB sctructure
    """
    # _developers()
    # _paymentsystems()
    # _casino()
    # _casino_params()
    # _casino_screenshots()
    # _games()
    # _games_developers()


def _developers():
    """
    Move developers
    """
    c_old.execute("SELECT id, name, image_path FROM developers_games ORDER BY id ASC")
    for item in c_old.fetchall():
        c_new.execute("INSERT INTO casino_developer(name, logo, old_id) VALUES(%s, %s, %s)", 
            (item["name"], item["image_path"], item["id"]))
    conn_new.commit()


def _paymentsystems():
    """
    Create list of payment system from parameters list
    """
    c_old.execute("""SELECT id, name, param_group FROM parameters 
    WHERE param_group IN (20, 22) ORDER BY name ASC""")#GROUP BY name 
    # c_new.execute("""TRUNCATE common_paymentsystem""")
    data_list = {}
    for item in c_old.fetchall():
        if item["name"] not in data_list:
            data_list[item["name"]] = {"cnt" : 0, "types" : {}}
        data_list[item["name"]]["types"][item["param_group"]] = item["id"]
        data_list[item["name"]]["cnt"] += 1

    input_values = []
    for name in data_list.keys():
        if data_list[name]["cnt"] > 2:
            continue
        params = '{%s, %s}' % (data_list[name]["types"].get(20, 'null'), data_list[name]["types"].get(22, 'null'))
        c_new.execute("""INSERT INTO common_paymentsystem(name, icon, "text", param_ids) 
        VALUES('%s', '', '', '%s')""" % (name, params,))
    conn_new.commit()


def _casino():
    """
    Porting casino
    """
    c_old.execute("""SELECT id, casino_name AS name, casino_domain AS domain, path AS purl_main,
    description, article AS text, logo AS image FROM managers_sites ORDER BY id ASC""")

    for item in c_old.fetchall():
        casino_name = item["name"] if item["name"] else item["domain"]
        c_new.execute("""INSERT INTO casino_casino(name, domain, param_mobile, param_browser, 
        param_audited, param_integrity, param_license, param_jackpot, param_tournaments, 
        param_nodepositbonus, old_id, param_shift, param_dealer, param_multiplayer, 
        similar_sale, urlkey, status, link_similar_sale, order_google, order_hand, enabled) 
        VALUES(%s, %s, -1, -1, -1, -1, -1, -1, -1, -1, %s, false, false, false, false, '', 1, '', 0, 0, false) 
        RETURNING id""", (casino_name, item["domain"], item["id"]))
        new_id = c_new.fetchone()[0]

        item_image = item["image"] if item["image"] else ""
        c_new.execute("""INSERT INTO casino_casinoinfo(casino_id, lang_id, name, image, description, 
        text, purl_main, purl_download, purl_bonus) VALUES(%s, 1, %s, %s, %s, %s, %s, '', '')""", 
        (new_id, item["name"], item_image, item["description"], item["text"], item["purl_main"]))
    conn_new.commit()


def _casino_params():
    """
    Parting casino parameters and paymentsystems relates
    """
    param_list = [297, 147, 111, 74, 210, 77, 116, 127]
    param_keys = {297 : "param_mobile", 147 : "param_browser", 111 : "param_audited", 
    74 : "param_integrity", 210 : "param_license", 77 : "param_jackpot", 116 : "param_tournaments", 
    127 : "param_nodepositbonus", 192 : "param_download"}
    
    #Get list of payment params ids
    payment_list = {}
    c_new.execute("SELECT id, param_ids  FROM common_paymentsystem ORDER BY id ASC")
    for item in c_new.fetchall():
        if item[1][0] is None:
            #input
            param_list.append(item[1][1])
            payment_list[item[1][1]] = {"id" : item[0], "type" : 2}
        elif item[1][1] is None:
            #output
            param_list.append(item[1][0])
            payment_list[item[1][0]] = {"id" : item[0], "type" : 1}
        else:
            param_list += item[1]
            payment_list[item[1][0]] = {"id" : item[0], "type" : 1}
            payment_list[item[1][1]] = {"id" : item[0], "type" : 2}

    # c_old.execute("""SELECT site_id AS old_id, site_name AS name, site_description AS info__description, 
    # logo AS info__image, "path" AS info__purl_main, parameter_id AS p_id, parameter_value AS p_val
    # FROM view_rating ORDER BY id ASC""")
    c_old.execute("""SELECT casino_id AS old_id, parameter_id AS p_id, value AS p_val 
    FROM managers_rating ORDER BY id ASC""")
    casino_list = {}

    old_to_new = _old_to_new()

    for item in c_old.fetchall():
        if not old_to_new.has_key(item["old_id"]):
            continue

        oid = item["old_id"]
        pid = item["p_id"]
        if casino_list.has_key(oid):
            if pid not in param_list:
                continue
        else:
            '''
            c_old.execute("""SELECT casino_domain AS domain, article AS info__text 
            FROM managers_sites WHERE id=%s""" % oid)
            casino = c_old.fetchone()
            casino_list[oid] = {"info" : {"text" : casino["info__text"], 
            "image" : item["info__image"], "purl_main" : item["info__purl_main"], 
            "description" : item["info__description"]}, "main" : {"name" : item["name"], 
            "domain" : casino["domain"]}, "payments" : {}}
            '''
            casino_list[oid] = {"params" : {}, "payments" : {}}
        
        if param_keys.has_key(pid):
            #Set casino param value
            casino_list[oid]["params"][param_keys[pid]] = item["p_val"]

        if payment_list.has_key(pid) and int(item["p_val"]) == 1:
            #Set relates between casino and paymentsystem
            payid = payment_list[pid]["id"]
            value = 3 if casino_list[oid]["payments"].has_key(payid) else payment_list[pid]["type"]
            casino_list[oid]["payments"][payid] = value

    for old_id in casino_list.keys():
        item = casino_list[old_id]
        c = item["params"]
        # i = item["info"]
        #update casino record
        new_id = old_to_new[old_id]
        c_new.execute("""UPDATE casino_casino SET param_mobile=%s, param_browser=%s, 
        param_audited=%s, param_integrity=%s, param_license=%s, param_jackpot=%s, param_tournaments=%s, 
        param_nodepositbonus=%s WHERE id=%s""", (c.get("param_mobile", -1), c.get("param_browser", -1), 
        c.get("param_audited", -1), c.get("param_integrity", -1), c.get("param_license", -1), 
        c.get("param_jackpot", -1), c.get("param_tournaments", -1), c.get("param_nodepositbonus", -1), new_id))
        # new_id = c_new.fetchone()[0]

        '''
        #insert casino info record
        c_new.execute("""INSERT INTO casino_casinoinfo(casino_id, lang_id, name, image, description, 
        text, purl_main, purl_download, purl_bonus) VALUES(%s, 1, %s, %s, %s, %s, %s, '', '')""", 
        (new_id, c["name"], i["image"], i["description"], i["text"], i["purl_main"]))
        conn_new.commit()
        '''

        for payment_id in item["payments"]:
            #Add payment relates
            c_new.execute("""INSERT INTO casino_casinotopaymentsystem(casino_id, paymentsystem_id, type) 
            VALUES(%s, %s, %s)""", (new_id, payment_id, item["payments"][payment_id]))
        conn_new.commit()

        
def _casino_screenshots():
    """
    Copy casino screenshots
    """
    old_to_new = _old_to_new()

    c_old.execute("""SELECT casino_id, image_path, comment FROM screenshots WHERE group_id=3 ORDER BY id ASC""")
    for item in c_old.fetchall():
        if not old_to_new.has_key(item["casino_id"]):
            continue
        c_new.execute("""INSERT INTO casino_casinoimage(lang_id, casino_id, name, image) 
        VALUES(1, %s, %s, %s)""", (old_to_new[item["casino_id"]], item["comment"], item["image_path"]))
    conn_new.commit()


def _games():
    """
    Porting games from old DB
    """
    old_to_new = _old_to_new()

    c_old.execute("""SELECT id, casino_id, image_path AS screenshot, link AS info__url_play_side, 
    width AS flash_width, heigth AS flash_height, show_slot AS flash_enabled, name AS info__name,
    show_mode AS flash_inframe, order_slot AS order_hand FROM slots ORDER BY id ASC""") #show_new_window, reflink, 
    for item in c_old.fetchall():
        if not old_to_new.has_key(item["casino_id"]):
            continue

        c_new.execute("""INSERT INTO casino_game(gametype, name, screenshot, flash_width, flash_height, 
            flash_enabled, order_hand, flash_inframe, maincasino_id, order_google, param_sale, param_gambling, 
            param_offline, param_mobile, param_integrity, param_shift, param_dealer, param_multiplayer, 
            param_tele, param_jackpot, enabled, old_id) VALUES(0, %s, %s, %s, %s, %s, %s, %s, %s, 0, -1, 
            -1, -1, -1, -1, -1, -1, -1, -1, -1, false, %s) RETURNING id""", (item["info__name"], 
            item["screenshot"], item["flash_width"], item["flash_height"], item["flash_enabled"], item["order_hand"],
            ('true' if item["flash_inframe"] == "1" else 'false'), old_to_new[item["casino_id"]], item["id"]))
        new_id = c_new.fetchone()[0]

        c_new.execute("""INSERT INTO casino_gameinfo(urlkey, game_id, lang_id, name, url_play_side, 
            tags_picture, tags_theme, tags_name, text, selltext, url_buy_our, url_play_our, 
            url_flash, url_buy_side) VALUES(null, %s, 1, %s, %s, '', '', '', '', '', null, null, null, null)""", 
            (new_id, item["info__name"], item["info__url_play_side"]))
    conn_new.commit()


def _games_developers():
    """
    Copy games screenshots
    """
    old_games = _old_to_new('casino_game')
    old_developers = _old_to_new('casino_developer')

    c_old.execute("""SELECT slot_id, developer_id FROM slots_developers""")
    for item in c_old.fetchall():
        if not old_games.has_key(item["slot_id"]):
            # print item["slot_id"]
            continue
        c_new.execute("""INSERT INTO casino_game_developers(game_id, developer_id) VALUES(%s, %s)""", 
        (old_games[item["slot_id"]], old_developers[item["developer_id"]],))
    conn_new.commit()


'''
screenshots for site, (other-) -> casino screenshot
param_###   -->   parameter_id
param_mobile  --  297
param_browser  --  147
param_download  --  192
param_audited  --  111
param_integrity  --  74
param_license  --  210
param_jackpot  --  77
param_tournaments  --  116
param_nodepositbonus  --  127
'''
def _old_to_new(table='casino_casino'):
    """
    Get dictionary with equal of old ID to new ID for casino records
    """
    old_to_new = {}
    c_new.execute("SELECT id, old_id FROM %s ORDER BY id ASC" % table)
    for item in c_new.fetchall():
        old_to_new[item[1]] = item[0]
    return old_to_new


q = sys.exit
if "__main__" == __name__:
    sys.exit(main())