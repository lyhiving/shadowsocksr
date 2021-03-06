# -*- coding: utf-8 -*-

import time
import logging

import requests

from utils.configloader import load_config, get_config


class EhcoApi(object):
    '''
    提供发送get/post的抽象类
    '''

    def __init__(self):
        self.session_pool = requests.Session()
        self.TOKEN = get_config().TOKEN
        self.WEBAPI_URL = get_config().WEBAPI_URL

    def getApi(self, uri):
        res = None
        try:
            payload = {'token': self.TOKEN}
            url = self.WEBAPI_URL+uri
            res = self.session_pool.get(url, params=payload, timeout=10)
            time.sleep(0.005)
            try:
                data = res.json()
            except Exception:
                if res:
                    logging.error('接口返回值格式错误: {}'.format(res.text))
                return []

            if data['ret'] == -1:
                logging.error("接口返回值不正确:{}".format(res.text))
                logging.error("请求头：{}".format(uri))
                return []
            return data['data']

        except Exception:
            import traceback
            trace = traceback.format_exc()
            logging.error(trace)
            raise Exception(
                '网络问题，请保证api接口地址设置正确！当前接口地址：{}'.format(self.WEBAPI_URL))

    def postApi(self, uri, raw_data={}):
        res = None
        try:
            payload = {'token': self.TOKEN}
            payload.update(raw_data)
            url = self.WEBAPI_URL+uri
            res = self.session_pool.post(
                url, json=payload, timeout=10)
            time.sleep(0.005)
            try:
                data = res.json()
            except Exception:
                if res:
                    logging.error('接口返回值格式错误: {}'.format(res.text))
                return []
            if data['ret'] == -1:
                logging.error("接口返回值不正确:{}".format(res.text))
                logging.error("请求头：{}".format(uri))
                return []
            return data['data']
        except Exception:
            import traceback
            trace = traceback.format_exc()
            logging.error(trace)
            raise Exception(
                '网络问题，请保证api接口地址设置正确！当前接口地址：{}'.format(self.WEBAPI_URL))

    def close(self):
        self.session_pool.close()
