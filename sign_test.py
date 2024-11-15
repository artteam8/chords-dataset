import time
import base64
import datetime
import hashlib
import hmac
from dataclasses import dataclass
from typing import Union

from yandex_music.utils.convert_track_id import convert_track_id_to_number


#DEFAULT_SIGN_KEY = 'p93jhgh689SBReK6ghtw62'

DEFAULT_SIGN_KEY = '7tvSmFbyf5hJnIHhCimDDD'

#data='1731415455 99410092 nq flacaache-aacmp3 raw'
#     date       track id codecs - cnst smth - const?

#quality vars
#}(k = z || (z = {})).LOSSLESS = "lossless", k.HQ = "hq", k.NQ = "nq", k.LQ = "lq", k.PREVIEW = "preview", k.SMART_PREVIEW = "smart_preview";

#"flac,aac,he-aac,mp3"



def create_data(track_id):
    # Получаем текущее время в секундах
    current_time_in_seconds = str(int(time.time()))
    
    # Формируем строку data
    data = f'{current_time_in_seconds}{track_id}nqflacaache-aacmp3raw'
    
    return data, current_time_in_seconds


def get_sign_request(track_id: Union[int, str], key: str = DEFAULT_SIGN_KEY):
    """Создает подпись для запроса.

    Args:
        track_id (:obj:`str` | :obj:`int`): Уникальный идентификатора трека.
        key (:obj:`str`, optional): Ключ для подписи.

    Returns:
        :obj:`Sign`: Подпись.
    """
    track_id = convert_track_id_to_number(track_id)

    timestamp = int(datetime.datetime.now().timestamp())
    message = f'{track_id}{timestamp}'

    hmac_sign = hmac.new(key.encode('UTF-8'), message.encode('UTF-8'), hashlib.sha256).digest()
    sign = base64.b64encode(hmac_sign).decode('UTF-8')

    return timestamp, sign



"""
codecs: (4) […]

0: "flac"

1: "aac"

2: "he-aac"

3: "mp3"

quality: "nq"

trackId: "99410092"

transports: (1) […]

0: "raw"

tsInSeconds: 1731447043
data = 173144704399410092nqflac,aac,he-aac,mp3raw

"""
#sign for this data - DVsSXf7tbragtukJ0G64+/NeHMWMBZCH9R1FhYD1YVY




import hmac
import hashlib
import base64

def generate_signature(secret_key, track_id):
    data, timestamp = create_data(str(track_id))
    # Convert secret key and data to bytes
    secret_key_bytes = secret_key.encode()
    data_bytes = data.encode()
    
    # Create HMAC with SHA-256
    hmac_obj = hmac.new(secret_key_bytes, data_bytes, hashlib.sha256)
    signature = hmac_obj.digest()
    
    # Encode to base64 and remove the trailing '=' as in the original function
    return base64.b64encode(signature).decode().rstrip('='), timestamp


def generate_signature_t(secret_key, track_id, quality, codecs, transports):

    timestamp = str(int(time.time())) #'1731472604' #

    codecs_str = ''
    codecs_str_z=''

    for i in range(len(codecs)):
        codecs_str+=codecs[i]
        codecs_str_z+=codecs[i]
        if i!=(len(codecs) - 1):
            codecs_str_z+=','


    data = timestamp + track_id + quality + codecs_str + transports
    
    # Convert secret key and data to bytes
    secret_key_bytes = secret_key.encode()
    data_bytes = data.encode()
    
    # Create HMAC with SHA-256
    hmac_obj = hmac.new(secret_key_bytes, data_bytes, hashlib.sha256)
    signature = hmac_obj.digest()


    sign = base64.b64encode(signature).decode().rstrip('=')

    from urllib.parse import quote
    base_url = "https://api.music.yandex.ru/get-file-info"
    params = {
        "ts": timestamp,
        "trackId": track_id,
        "quality": quality,
        "codecs": codecs_str_z,
        "transports": transports,
        "sign": sign
    }








    import requests

    # Отправка GET-запроса
    response = requests.get(base_url, params=params)

    print(response)

    








    # Кодируем параметры, где это необходимо
    params["codecs"] = quote(params["codecs"], safe='')
    params["sign"] = quote(params["sign"], safe='')

    # Формируем итоговый URL
    encoded_url = f"{base_url}?ts={params['ts']}&trackId={params['trackId']}&quality={params['quality']}&codecs={params['codecs']}&transports={params['transports']}&sign={params['sign']}"


    print(encoded_url)
    print('https://api.music.yandex.ru/get-file-info?ts=1731484110&trackId=99410092&quality=nq&codecs=flac%2Caac%2Che-aac%2Cmp3&transports=raw&sign=lHyXX3ReIBrt0WjXEUtjtSIiwVHbXvyF99JVGl9srG8')
    

    # Проверка и вывод результата
    if response.status_code == 200:
        print(response.json())  # Если результат в JSON формате
    else:
        print("Ошибка:", response.status_code, response.text)




    #link = f'https://api.music.yandex.ru/get-file-info?ts={timestamp}&trackId={track_id}&quality={quality}&codecs={codecs_str_z}&transports={transports}&sign={sign}'




    print('https://api.music.yandex.ru/get-file-info?ts=1731484110&trackId=99410092&quality=nq&codecs=flac%2Caac%2Che-aac%2Cmp3&transports=raw&sign=lHyXX3ReIBrt0WjXEUtjtSIiwVHbXvyF99JVGl9srG8')


    
    # Encode to base64 and remove the trailing '=' as in the original function
    return sign, timestamp


"""
track_id = 99410092

timest, sign = get_sign_request(track_id)

sign, timestamp = generate_signature(DEFAULT_SIGN_KEY, track_id)


print( f'https://api.music.yandex.ru/tracks/{track_id}/lyrics?sign={sign}&timeStamp={timestamp}&format=LRC' )
"""
#1731472604105329916nqflacaache-aacmp3raw


print(generate_signature_t(DEFAULT_SIGN_KEY, '99410092', 'nq', ['flac', 'aac', 'he-aac', 'mp3'], 'raw'))





#print('DVsSXf7tbragtukJ0G64+/NeHMWMBZCH9R1FhYD1YVY')



#https://api.music.yandex.ru/get-file-info?ts=1731472604&trackId=105329916&quality=nq&codecs=flac%2Caac%2Che-aac%2Cmp3&transports=raw&sign=3EIj/VH/4wdL6TijgrX76O07+FQ9FwgjRYye9SdSCJQ
#https://api.music.yandex.ru/get-file-info?ts=1731472604&trackId=105329916&quality=nq&codecs=flac%2Caac%2Che-aac%2Cmp3&transports=raw&sign=3EIj%2FVH%2F4wdL6TijgrX76O07%2BFQ9FwgjRYye9SdSCJQ