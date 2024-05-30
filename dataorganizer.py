import matplotlib.pyplot as plt;
import numpy as np;
from matplotlib import colors;
from matplotlib.ticker import PercentFormatter;
from scipy import stats;
import json;
import math;
import seaborn as sns;
import powerlaw;
from sklearn import linear_model;
from sklearn.feature_extraction import DictVectorizer;
import time
import requests
from bs4 import BeautifulSoup
import random;
from requests.auth import HTTPProxyAuth
from pytrends.request import TrendReq
import pandas as pd;
from dateutil.parser import parse;
from datetime import datetime;
import csv;
#import warnings
#warnings.filterwarnings('ignore')
#import argparse

#parser = argparse.ArgumentParser(description='Get Google Count.')
#parser.add_argument('word', help='word to count')
#args = parser.parse_args()

#headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"}

user_agent_list = [
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

headerslist = [
    {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Connection': 'keep-alive',
    'Referer': 'https://trends.google.com/trends/explore?cat=41&date=today^%^205-y&q=Terraria&hl=en',
    # 'Cookie': '__utma=10102256.1469059818.1716047426.1716047426.1716047426.1; __utmb=10102256.31.8.1716050129523; __utmc=10102256; __utmz=10102256.1716047426.1.1.utmcsr=trends.google.com^|utmccn=(referral)^|utmcmd=referral^|utmcct=/; __utmt=1; 1P_JAR=2024-05-18-16; NID=514=k469KUGUDreXJUYn1hrKZkfGBZhWYNjbEh_3JS16MRoVYvHsWwCGzlqr0qx_F2g5ZvUluq4J3TmdTxy0Y9HXqPuxbHIsEEHcD3t2mOTzKZepE8_0gpVJtlLLw7PqFo-lXdDVvliIeyiOTLhbKXFyr2i27s3rtyC5lAy63qr5L-iS2c1I7TgAdaKMEH3Mnj3QjdtqNuDDJMKpZalmK7GpaYP7jofOQrcavnFllCAb8TT8umQW7g-tLZOiot09VqsMu7IyzHP1xEBynaQfGSrFj_VH1yEEQRpyzTRJEfQk1O2Nd8pJbOB2XPaGSJI1USEXUvKnzDN8m0iLhSuOMadcoqbfKiFKeeCcmj9POFw8nSGiUDHy4W3V7OiO9GPpXNooZwbPCzmwSVeS5SBlnVA5JL3gFk9f_v8pw-7n7Z0BlKvMzEmqCphU0mertPshQ6MhPue38OmQmYIEmJbeyQkIqkTPuEVVcJUdD9sBeEkDadtSMLPLOmVswqT9fyzBKhQA-_Shz96qE0zllKHPN-DPraJ5oeWRckGG_E8RDSge_d5cYJeggLuSRKPA_FQ0WW53IrzSI_9Hb91gPmqNd5h21Z6zebIzXYK7AVmVjEfF9LyR-GwDaCJXyAE-Ou6Qjjq4UziYfubjBlPnK0HpQHqL2lXZ_4MVi8VQ_wpGUxP_8fd-QlSRYHqkMGXtLKV9t8YHp6-ljAJny7hZq7J71S_A7HAMWdFk6rgI39yaXs6jYUHWI8QwjKsH-N5NbP5XH8V20oKS5qd1KvyVDnG5CKgRt1K7lrSfqHIjZ4HqZng8hd1w3IFUCSDG5H-SGqxivFTFmw; SEARCH_SAMESITE=CgQItJoB; SID=g.a000jwi6jNKIwaS5vA5OPua-NoBIZrlSWnoUT4FCRcoYTE0IJLvD_XZ3JafDNVU45BkQo16R0gACgYKAZ8SAQASFQHGX2Mi_LUtf1yVaOPWH20n6kTbWRoVAUF8yKoJGETXvoZKnrMs_AeKlUfC0076; __Secure-1PSID=g.a000jwi6jNKIwaS5vA5OPua-NoBIZrlSWnoUT4FCRcoYTE0IJLvDnUMgn2buYYviJIsTWPd_3AACgYKAc4SAQASFQHGX2MiljFvDZpze9wvhNmq3BbOABoVAUF8yKpXxBDo8_QT5RzYbLZfuqmT0076; __Secure-3PSID=g.a000jwi6jNKIwaS5vA5OPua-NoBIZrlSWnoUT4FCRcoYTE0IJLvDsiWBcb1fX83lFnFzUKUI6QACgYKAfwSAQASFQHGX2MiHRlw0Aq_oQk1pZERmY0CuBoVAUF8yKqbCh9QOdmNzTMzHa_NoBeO0076; HSID=AN2rkliYJT00EVPv1; SSID=A6wRsOhYni8vpDAP5; APISID=PALo7RcJRBVoTMRy/A02t1f5UvCwyAVmWC; SAPISID=OBvh9He9sC2ST3oC/AlVn206nHihBNZaZ4; __Secure-1PAPISID=OBvh9He9sC2ST3oC/AlVn206nHihBNZaZ4; __Secure-3PAPISID=OBvh9He9sC2ST3oC/AlVn206nHihBNZaZ4; SIDCC=AKEyXzXFiC-FZ-SJzyRvyFJA7-VvZ0vsfmyjeGPKlM9W-OrgpKHarmKrzK5gjlaIxNyf-r3xvlU; __Secure-1PSIDCC=AKEyXzViqtkxPFgOL9TAJhGPMkG1NhwRS236zEiTeofmh4ICALD6XuaCIka2Jo1LuNQnOVJy_Ws; __Secure-3PSIDCC=AKEyXzVJYZLV0Vl-Q-9VkpUBzVJTglqYUnAX0YR-uUigusY4lpbKE5VoqIGV967CoCvYQXvmV8_H; __Secure-1PSIDTS=sidts-CjIBLwcBXDI4uO9CtXOTQFhs5wl-8TxYtcVUQwbzLqK0So3ZhbzX28tJAvS4GHnsXO1knxAA; __Secure-3PSIDTS=sidts-CjIBLwcBXDI4uO9CtXOTQFhs5wl-8TxYtcVUQwbzLqK0So3ZhbzX28tJAvS4GHnsXO1knxAA; __Secure-ENID=19.SE=IoeaD3O5IBotC3EBWcaVGmZTSb3VS8dHL2r-NtaCklgUtx_jJuTKJaaCnFY19svuVjL_urR98brC8NFKC5o7xpxNhWFIZxMq4ztvJnWOA6SDSjOK5CCIVF7coYBGL6a09LbpsXcz2Q-Y2zsmu9IPiYgW6V7EWBQGMsiTZJd7g85B0_JGdpgpVGifkxhdEJ676SKowBlSVxNUlMbIqTWgsqOu1jFDtJk8P8KsLqdgSENRZBxpFqy7A2st9MO2qOQP5BAUPFtKwy3gYgX3r-K6khYJE8H_xA-QCoOFj1dK9J1tUUoHcyaDaHlyrB88yVf9cI07YnfHdIQ_wl_eDxuHfVzQ4r1E; AEC=AQTF6Hz-oHcLmXdXo633JulD96B_JLKGsZOpJOXLgeH8H-9OX5sGme_yNHg; S=billing-ui-v3=_viNIp2S9pp-yUjBmuJ7sVdVi6m1dNc_:billing-ui-v3-efe=_viNIp2S9pp-yUjBmuJ7sVdVi6m1dNc_; OTZ=7562390_72_76_104100_72_446760',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
},
{
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'DNT': '1',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://trends.google.com/trends/explore?geo=CA&q=Stellaris&hl=en-US',
    # 'Cookie': 'AEC=AQTF6HxR7o5rzGjIz-Ck4BVHLO-uEcs-eGH9bv49A0G2xyapi0IAdHxYuQ; NID=514=HsEOZN7tp9rWsZoPJJe21r08gR5BHSV5E5g_hCdS2MaySrUuNhrSvF833hHFxgSEiqrHgzK5931VWg1dx28i9lpcANK0okYE5Uk4127rLld_4dzlmmPFns6xP7eTNILeHByEydjEiVCoYyITKU0I_f3pN5FIBkufOTCRIPrhHkpAaad2Vmi-JKMFG2QVcuyv2cqKGG5NqNf3RTfNCiF8lRSjByj1nto0xrT_mjb_lnWmOrFHjABb; SID=g.a000jwj-nhh-US5vww_cv3RWvhYvF8KZaelmgl_gg0qxFYWwP2HVL_C_sob1Fmt9i59nnOlP0wACgYKATkSAQASFQHGX2MiWqgA7Z7E-_QvhYXUk-rZLhoVAUF8yKrwSOzfJhdmgeJioGFwMazZ0076; __Secure-1PSID=g.a000jwj-nhh-US5vww_cv3RWvhYvF8KZaelmgl_gg0qxFYWwP2HV9tyZSMGcq9kuuC3Szsb_dQACgYKAZESAQASFQHGX2MiWNwMQDi_YZln11Ng5SGjyhoVAUF8yKqbhuq6R5RqB8vEwDKGhmX70076; __Secure-3PSID=g.a000jwj-nhh-US5vww_cv3RWvhYvF8KZaelmgl_gg0qxFYWwP2HVMZ4z_Z8AlsXqJ1a6DJI1MwACgYKAc0SAQASFQHGX2MicErOjdrV36A1Dr5qm_FuUhoVAUF8yKp2QhxtuWx1Dq1nGIpRGahK0076; HSID=Av-I2PIR1p9PjkfWh; SSID=ALNkJH5e-3BpGtBvn; APISID=KV5SY8kcK60ceRBx/ARexUwMDlXAi_O6fv; SAPISID=3ri8FcW_wW4X_8Rr/A2ZXBwYuPQuc_-2nU; __Secure-1PAPISID=3ri8FcW_wW4X_8Rr/A2ZXBwYuPQuc_-2nU; __Secure-3PAPISID=3ri8FcW_wW4X_8Rr/A2ZXBwYuPQuc_-2nU; SIDCC=AKEyXzWMkofwmljmr2sKl2dLQ_MLiFOJGvluPriQrH6neWERQ1SkilV8xPT6ugtCagpebdGy4w; __Secure-1PSIDCC=AKEyXzXA5vdGohFIxpYx2cnDLGIqk3KpdziTafMFJ1nqALDjagLkBzLEa2g0Y34fTMfSUQXg; __Secure-3PSIDCC=AKEyXzWEhcr8R2UWgvoeYnYU1SQy2mCOW2YZXL3DaYjIKwZXNSNUv5Jz8FKnuQxNmZmp4d0L; SEARCH_SAMESITE=CgQIlZsB; __Secure-ENID=19.SE=IW7dk5ouCgn8Pk-FKEyB0E6f7PF90MXSkpERiTt4us_U7bgKtmOnv0eFEeLtgUQPR_9BBIqVRfdAiuteEsJcAZuSIVCLiAVo28MnhIPc_obHQrs9ySwna3AXgIcdkLOhpEDZ0M2H5deKQW4sQmphPIuVFDdOJK1Cg8FC40ed24Z_aPu3ngES6QJfK0CPLXWg6wZJqphPk-TahpCCOsmweK84IUUkPcjvLMKRttElrHskHahBW99Bn6d6RGKOd5pVfi9mE_8B7RfOI80; OTZ=7562426_72_76_104100_72_446760; __Secure-1PSIDTS=sidts-CjEBLwcBXP3QzoZiVtN1h3bG423i3ytIH10uqFJFzmnEzZvJzKar5Pg0ZFbMSQg35yLcEAA; __Secure-3PSIDTS=sidts-CjEBLwcBXP3QzoZiVtN1h3bG423i3ytIH10uqFJFzmnEzZvJzKar5Pg0ZFbMSQg35yLcEAA',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
},
{
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'DNT': '1',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://trends.google.com/trends/explore?geo=CA&q=Minecraft&hl=en-US',
    # 'Cookie': 'AEC=AQTF6HxR7o5rzGjIz-Ck4BVHLO-uEcs-eGH9bv49A0G2xyapi0IAdHxYuQ; NID=514=HsEOZN7tp9rWsZoPJJe21r08gR5BHSV5E5g_hCdS2MaySrUuNhrSvF833hHFxgSEiqrHgzK5931VWg1dx28i9lpcANK0okYE5Uk4127rLld_4dzlmmPFns6xP7eTNILeHByEydjEiVCoYyITKU0I_f3pN5FIBkufOTCRIPrhHkpAaad2Vmi-JKMFG2QVcuyv2cqKGG5NqNf3RTfNCiF8lRSjByj1nto0xrT_mjb_lnWmOrFHjABb; SID=g.a000jwj-nhh-US5vww_cv3RWvhYvF8KZaelmgl_gg0qxFYWwP2HVL_C_sob1Fmt9i59nnOlP0wACgYKATkSAQASFQHGX2MiWqgA7Z7E-_QvhYXUk-rZLhoVAUF8yKrwSOzfJhdmgeJioGFwMazZ0076; __Secure-1PSID=g.a000jwj-nhh-US5vww_cv3RWvhYvF8KZaelmgl_gg0qxFYWwP2HV9tyZSMGcq9kuuC3Szsb_dQACgYKAZESAQASFQHGX2MiWNwMQDi_YZln11Ng5SGjyhoVAUF8yKqbhuq6R5RqB8vEwDKGhmX70076; __Secure-3PSID=g.a000jwj-nhh-US5vww_cv3RWvhYvF8KZaelmgl_gg0qxFYWwP2HVMZ4z_Z8AlsXqJ1a6DJI1MwACgYKAc0SAQASFQHGX2MicErOjdrV36A1Dr5qm_FuUhoVAUF8yKp2QhxtuWx1Dq1nGIpRGahK0076; HSID=Av-I2PIR1p9PjkfWh; SSID=ALNkJH5e-3BpGtBvn; APISID=KV5SY8kcK60ceRBx/ARexUwMDlXAi_O6fv; SAPISID=3ri8FcW_wW4X_8Rr/A2ZXBwYuPQuc_-2nU; __Secure-1PAPISID=3ri8FcW_wW4X_8Rr/A2ZXBwYuPQuc_-2nU; __Secure-3PAPISID=3ri8FcW_wW4X_8Rr/A2ZXBwYuPQuc_-2nU; SIDCC=AKEyXzW0g2DrJ9P3bCg-fdVtyD25i9dMvIoZy1IjR-0vw27riY440vGjvjB5_4fgJZnXWgBcaA; __Secure-1PSIDCC=AKEyXzVIqAt9VeJYJRb77HsW-Rpv82jVp-1z4XzygfU-3IKmx74xd2rFfXh0pGNajsD6L8vs; __Secure-3PSIDCC=AKEyXzUVmdYJL3lO26yhrKmSAu3JTo0FJMUQSqbjCV7NThgxJ9DRAWbAtenSYiE0c9hXjWwi; SEARCH_SAMESITE=CgQIlZsB; __Secure-ENID=19.SE=IW7dk5ouCgn8Pk-FKEyB0E6f7PF90MXSkpERiTt4us_U7bgKtmOnv0eFEeLtgUQPR_9BBIqVRfdAiuteEsJcAZuSIVCLiAVo28MnhIPc_obHQrs9ySwna3AXgIcdkLOhpEDZ0M2H5deKQW4sQmphPIuVFDdOJK1Cg8FC40ed24Z_aPu3ngES6QJfK0CPLXWg6wZJqphPk-TahpCCOsmweK84IUUkPcjvLMKRttElrHskHahBW99Bn6d6RGKOd5pVfi9mE_8B7RfOI80; OTZ=7562426_72_76_104100_72_446760; __Secure-1PSIDTS=sidts-CjEBLwcBXP3QzoZiVtN1h3bG423i3ytIH10uqFJFzmnEzZvJzKar5Pg0ZFbMSQg35yLcEAA; __Secure-3PSIDTS=sidts-CjEBLwcBXP3QzoZiVtN1h3bG423i3ytIH10uqFJFzmnEzZvJzKar5Pg0ZFbMSQg35yLcEAA',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
},
{
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'DNT': '1',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://trends.google.com/trends/explore?q=^%^2Fg^%^2F11fszn8rp_&date=now^%^201-d&geo=CA&hl=en',
    # 'Cookie': 'AEC=AQTF6HxR7o5rzGjIz-Ck4BVHLO-uEcs-eGH9bv49A0G2xyapi0IAdHxYuQ; NID=514=HsEOZN7tp9rWsZoPJJe21r08gR5BHSV5E5g_hCdS2MaySrUuNhrSvF833hHFxgSEiqrHgzK5931VWg1dx28i9lpcANK0okYE5Uk4127rLld_4dzlmmPFns6xP7eTNILeHByEydjEiVCoYyITKU0I_f3pN5FIBkufOTCRIPrhHkpAaad2Vmi-JKMFG2QVcuyv2cqKGG5NqNf3RTfNCiF8lRSjByj1nto0xrT_mjb_lnWmOrFHjABb; SID=g.a000jwj-nhh-US5vww_cv3RWvhYvF8KZaelmgl_gg0qxFYWwP2HVL_C_sob1Fmt9i59nnOlP0wACgYKATkSAQASFQHGX2MiWqgA7Z7E-_QvhYXUk-rZLhoVAUF8yKrwSOzfJhdmgeJioGFwMazZ0076; __Secure-1PSID=g.a000jwj-nhh-US5vww_cv3RWvhYvF8KZaelmgl_gg0qxFYWwP2HV9tyZSMGcq9kuuC3Szsb_dQACgYKAZESAQASFQHGX2MiWNwMQDi_YZln11Ng5SGjyhoVAUF8yKqbhuq6R5RqB8vEwDKGhmX70076; __Secure-3PSID=g.a000jwj-nhh-US5vww_cv3RWvhYvF8KZaelmgl_gg0qxFYWwP2HVMZ4z_Z8AlsXqJ1a6DJI1MwACgYKAc0SAQASFQHGX2MicErOjdrV36A1Dr5qm_FuUhoVAUF8yKp2QhxtuWx1Dq1nGIpRGahK0076; HSID=Av-I2PIR1p9PjkfWh; SSID=ALNkJH5e-3BpGtBvn; APISID=KV5SY8kcK60ceRBx/ARexUwMDlXAi_O6fv; SAPISID=3ri8FcW_wW4X_8Rr/A2ZXBwYuPQuc_-2nU; __Secure-1PAPISID=3ri8FcW_wW4X_8Rr/A2ZXBwYuPQuc_-2nU; __Secure-3PAPISID=3ri8FcW_wW4X_8Rr/A2ZXBwYuPQuc_-2nU; SIDCC=AKEyXzXGTA657bAf3AlniraDm03RyGbuuHwDGPNsxsAWzK5VS1M1Cy3wZTxUWU6C7AQyjoEolQ; __Secure-1PSIDCC=AKEyXzUOD1sGwJtFuX8llNWaIidwpNlOGtUthWiXFtmjJimKTuPwRP6e2LX5DvvnETbeAhO9; __Secure-3PSIDCC=AKEyXzVL-JfmXvwkW5vsTxBsDA6Om1NYTYpPZnZyxordT2e3_qzYkvKwBGMePhCMFVtYfznf; SEARCH_SAMESITE=CgQIlZsB; __Secure-ENID=19.SE=IW7dk5ouCgn8Pk-FKEyB0E6f7PF90MXSkpERiTt4us_U7bgKtmOnv0eFEeLtgUQPR_9BBIqVRfdAiuteEsJcAZuSIVCLiAVo28MnhIPc_obHQrs9ySwna3AXgIcdkLOhpEDZ0M2H5deKQW4sQmphPIuVFDdOJK1Cg8FC40ed24Z_aPu3ngES6QJfK0CPLXWg6wZJqphPk-TahpCCOsmweK84IUUkPcjvLMKRttElrHskHahBW99Bn6d6RGKOd5pVfi9mE_8B7RfOI80; OTZ=7562426_72_76_104100_72_446760; __Secure-1PSIDTS=sidts-CjEBLwcBXP3QzoZiVtN1h3bG423i3ytIH10uqFJFzmnEzZvJzKar5Pg0ZFbMSQg35yLcEAA; __Secure-3PSIDTS=sidts-CjEBLwcBXP3QzoZiVtN1h3bG423i3ytIH10uqFJFzmnEzZvJzKar5Pg0ZFbMSQg35yLcEAA',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
},
{
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'DNT': '1',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://trends.google.com/trends/explore?date=now^%^201-d&geo=CA&q=^%^2Fg^%^2F11ksnq4w1f&hl=en',
    # 'Cookie': 'AEC=AQTF6HxR7o5rzGjIz-Ck4BVHLO-uEcs-eGH9bv49A0G2xyapi0IAdHxYuQ; NID=514=HsEOZN7tp9rWsZoPJJe21r08gR5BHSV5E5g_hCdS2MaySrUuNhrSvF833hHFxgSEiqrHgzK5931VWg1dx28i9lpcANK0okYE5Uk4127rLld_4dzlmmPFns6xP7eTNILeHByEydjEiVCoYyITKU0I_f3pN5FIBkufOTCRIPrhHkpAaad2Vmi-JKMFG2QVcuyv2cqKGG5NqNf3RTfNCiF8lRSjByj1nto0xrT_mjb_lnWmOrFHjABb; SID=g.a000jwj-nhh-US5vww_cv3RWvhYvF8KZaelmgl_gg0qxFYWwP2HVL_C_sob1Fmt9i59nnOlP0wACgYKATkSAQASFQHGX2MiWqgA7Z7E-_QvhYXUk-rZLhoVAUF8yKrwSOzfJhdmgeJioGFwMazZ0076; __Secure-1PSID=g.a000jwj-nhh-US5vww_cv3RWvhYvF8KZaelmgl_gg0qxFYWwP2HV9tyZSMGcq9kuuC3Szsb_dQACgYKAZESAQASFQHGX2MiWNwMQDi_YZln11Ng5SGjyhoVAUF8yKqbhuq6R5RqB8vEwDKGhmX70076; __Secure-3PSID=g.a000jwj-nhh-US5vww_cv3RWvhYvF8KZaelmgl_gg0qxFYWwP2HVMZ4z_Z8AlsXqJ1a6DJI1MwACgYKAc0SAQASFQHGX2MicErOjdrV36A1Dr5qm_FuUhoVAUF8yKp2QhxtuWx1Dq1nGIpRGahK0076; HSID=Av-I2PIR1p9PjkfWh; SSID=ALNkJH5e-3BpGtBvn; APISID=KV5SY8kcK60ceRBx/ARexUwMDlXAi_O6fv; SAPISID=3ri8FcW_wW4X_8Rr/A2ZXBwYuPQuc_-2nU; __Secure-1PAPISID=3ri8FcW_wW4X_8Rr/A2ZXBwYuPQuc_-2nU; __Secure-3PAPISID=3ri8FcW_wW4X_8Rr/A2ZXBwYuPQuc_-2nU; SIDCC=AKEyXzXIivyVitXPb-MuBJvoUj27CrZzrlbuVonfBqzrfXCmFBIcb7BvT5y69AXwmyQpB9zFlw; __Secure-1PSIDCC=AKEyXzVAVTKywlzt0e99IRO7HxOP-25ZB3wUw1_7CjFualF5m-tsVOEICStiWM60OeMzjSES; __Secure-3PSIDCC=AKEyXzUm_Bfpc5H56g5jZWtDRcNuBZKUCXxfDpNhhlyHCJV5s4YKYy4aMfM2SobyQ_VcLJ6K; SEARCH_SAMESITE=CgQIlZsB; __Secure-ENID=19.SE=IW7dk5ouCgn8Pk-FKEyB0E6f7PF90MXSkpERiTt4us_U7bgKtmOnv0eFEeLtgUQPR_9BBIqVRfdAiuteEsJcAZuSIVCLiAVo28MnhIPc_obHQrs9ySwna3AXgIcdkLOhpEDZ0M2H5deKQW4sQmphPIuVFDdOJK1Cg8FC40ed24Z_aPu3ngES6QJfK0CPLXWg6wZJqphPk-TahpCCOsmweK84IUUkPcjvLMKRttElrHskHahBW99Bn6d6RGKOd5pVfi9mE_8B7RfOI80; OTZ=7562426_72_76_104100_72_446760; __Secure-1PSIDTS=sidts-CjEBLwcBXP3QzoZiVtN1h3bG423i3ytIH10uqFJFzmnEzZvJzKar5Pg0ZFbMSQg35yLcEAA; __Secure-3PSIDTS=sidts-CjEBLwcBXP3QzoZiVtN1h3bG423i3ytIH10uqFJFzmnEzZvJzKar5Pg0ZFbMSQg35yLcEAA',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}
]


requests_args = {
    'headers': random.choice(headerslist),
    'verify': False
}

proxies = [ # gotten from webshare
    "http://38.154.227.167:5868",
    "http://185.199.229.156:7492",
    "http://185.199.228.220:7300",
    "http://185.199.231.45:8382",
    "http://188.74.210.207:6286",
    "http://188.74.183.10:8279",
    "http://188.74.210.21:6100",
    "http://45.155.68.129:8133",
    "http://154.95.36.199:6893",
    "http://45.94.47.66:8110",
]

#pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), proxies=['http://vhlqcuxl-rotate:z1j31e1386sb@p.webshare.io:80'], retries=2, backoff_factor=0.1, requests_args=requests_args)

file = open("games.json", encoding = "utf8");
data = json.load(file);

popularity = [];
popNO = [];
prices = [];
pricesNO = [];
reviewRatio = [];
reviewRatioNO = [];
positiveReviewsArr = [];
pricesPopularity = [[prices], [popularity]];
googlePopularity = [];
googlePopularityNO = [];
releaseDates = [];
releaseDatesNO = [];
namedataNO = [];
estimatedOwners = [];
estimatedOwnersNO = [];

monthsData = {"Jan": [0, 0], "Feb": [0, 0], "Mar": [0, 0], "Apr": [0, 0], "May": [0, 0], "Jun": [0, 0], "Jul": [0, 0], "Aug": [0, 0], "Sep": [0, 0], "Oct": [0, 0], "Nov": [0, 0], "Dec": [0, 0]};
monthsAverage = {"Jan": 0, "Feb": 0, "Mar": 0, "Apr": 0, "May": 0, "Jun": 0, "Jul": 0, "Aug": 0, "Sep": 0, "Oct": 0, "Nov": 0, "Dec": 0};

def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))
# x - 101 / 16740 - 101 = 0.4
# x = 6756.6

def reject_outliers_median(data, m = 2.):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else np.zeros(len(d))
    return data[s<m]

def reject_outliers_mean(data, m=2):
    return data[abs(data - np.mean(data)) < m * np.std(data)]

def reject_outliers_merge(data, m=2):
    return data[abs(data - np.median(data)) < m * np.std(data)]

def IQR_outliers(data):
    sorted(data)
    Q1,Q3 = np.percentile(data , [25,75])
    IQR = Q3 - Q1
    lower_range = Q1 - (1.5 * IQR)
    upper_range = Q3 + (1.5 * IQR)
    return [d for d in data if lower_range <= d <= upper_range]

def IQR_determine(data):
    [d for d in data if not d == -1 and not d == 100.0]
    sorted(data)
    Q1, Q2, Q3 = np.percentile(data , [25, 50, 75])
    IQR = Q3 - Q1
    print(Q1, Q2, Q3, IQR, Q1 - (1.5 * IQR), Q3 + (1.5 * IQR))
    return (Q1 - (1.5 * IQR)), (Q3 + (1.5 * IQR))

def IQR_outliers_remove_all(popdata, pricedata, reviewdata, googledata, namedata, ownerdata):
    indexToRemove = []
    lower_range, upper_range = IQR_determine(popdata)
    [indexToRemove.append(i) for i, v in enumerate(popdata) if not lower_range <= v <= upper_range and not i in indexToRemove]
    lower_range, upper_range = IQR_determine(pricedata)
    [indexToRemove.append(i) for i, v in enumerate(pricedata) if not lower_range <= v <= upper_range and not i in indexToRemove]
    lower_range, upper_range = IQR_determine(reviewdata)
    [indexToRemove.append(i) for i, v in enumerate(reviewdata) if not lower_range <= v <= upper_range and not i in indexToRemove]
    lower_range, upper_range = IQR_determine(googledata)
    [indexToRemove.append(i) for i, v in enumerate(googledata) if not lower_range <= v <= upper_range or v == -1 or v == 100.0 and not i in indexToRemove]
    lower_range, upper_range = IQR_determine(ownerdata)
    [indexToRemove.append(i) for i, v in enumerate(ownerdata) if not lower_range <= v <= upper_range and not i in indexToRemove]
    
    '''for i, v in enumerate(popdata):
        if not lower_range <= v <= upper_range:
            popdata.pop(i)
            prices.pop(i)
            reviewRatio.pop(i)
            googlePopularity.pop(i)
        if v > 5000:
            popdata.pop(i)
            prices.pop(i)
            reviewRatio.pop(i)
            googlePopularity.pop(i)'''
    popNO = [d for i, d in enumerate(popdata) if not i in indexToRemove]
    pricesNO = [d for i, d in enumerate(pricedata) if not i in indexToRemove]
    reviewRatioNO = [d for i, d in enumerate(reviewdata) if not i in indexToRemove]
    googlePopularityNO = [d for i, d in enumerate(googledata) if not i in indexToRemove]
    namedataNO = [d for i, d in enumerate(namedata) if not i in indexToRemove]
    estimatedOwnersNO = [d for i, d in enumerate(ownerdata) if not i in indexToRemove]
    #releaseDatesNO = [d for i, d in enumerate(releasedata) if not i in indexToRemove]
    return popNO, pricesNO, reviewRatioNO, googlePopularityNO, namedataNO,estimatedOwnersNO#, releaseDatesNO

'''
def is_outlier(points, thresh=3.5):
    """
    Returns a boolean array with True if points are outliers and False 
    otherwise.

    Parameters:
    -----------
        points : An numobservations by numdimensions array of observations
        thresh : The modified z-score to use as a threshold. Observations with
            a modified z-score (based on the median absolute deviation) greater
            than this value will be classified as outliers.

    Returns:
    --------
        mask : A numobservations-length boolean array.

    References:
    ----------
        Boris Iglewicz and David Hoaglin (1993), "Volume 16: How to Detect and
        Handle Outliers", The ASQC Basic References in Quality Control:
        Statistical Techniques, Edward F. Mykytka, Ph.D., Editor. 
    """
    if len(points.shape) == 1:
        points = points[:,None]
    median = np.median(points, axis=0)
    diff = np.sum((points - median)**2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)

    modified_z_score = 0.6745 * diff / med_abs_deviation

    return modified_z_score > thresh
'''

gameNames = [];

scrapeTrends = False;
kw_list = []
count = 0;
names = []

print(len(data))

for i in data:
    name = data[i]["name"];
    releaseDate = data[i]["release_date"];
    price = data[i]["price"];
    positiveReviews = data[i]["positive"];
    negativeReviews = data[i]["negative"];
    peakConcurrent = data[i]["peak_ccu"];

    if peakConcurrent > 100 and peakConcurrent < 20000 and price < 100:
        if (not negativeReviews == 0 and not positiveReviews == 0):
            popularity.append(peakConcurrent);
            reviewRatio.append(positiveReviews/negativeReviews);
            positiveReviewsArr.append(positiveReviews);
            prices.append(price);
            monthsData[releaseDate.split(" ")[0]][0] += 1;
            monthsData[releaseDate.split(" ")[0]][1] += peakConcurrent;
            releaseDates.append(releaseDate);
            gameNames.append(name);
            estimatedOwners.append((int(data[i]["estimated_owners"].split(" - ")[0])+int(data[i]["estimated_owners"].split(" - ")[1])) / 2)
            count += 1;

            fname = name.encode('cp1252', 'ignore').decode('utf-8', 'ignore')

            kw_list.clear()
            kw_list.append(fname)

            names.append(fname)


            if scrapeTrends:
                try:

                    if (not fname in open('dataframe.csv', 'rb').read().decode('utf-8', 'ignore')):
                        pytrends.build_payload(kw_list, cat=41, timeframe='today 5-y', geo='', gprop='')
                        f = open('dataframe.csv', 'a', encoding='utf-8')
                        pytrends.interest_over_time().to_csv(f)
                        f.close()
                        print(fname + " has been added: #" + str(count))
                    else:
                        print(fname + " already exists in the dataframe: #" + str(count))

                except Exception as e:
                    print("Error: " + str(e))
                    continue

            realresult = True;
            while not realresult:

                time.sleep(random.randint(1, 3))
                #t = random.choice(proxies)
                #proxies = {
                #    "http": t,
                #    "https": t
                #}
                #headers = {"User-Agent": random.choice(user_agent_list)}
                headers = headers = {
                    'User-Agent': random.choice(user_agent_list),
                    'Accept': '*/*',
                    'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
                    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
                    #'Referer': 'https://www.bing.com/search?q=age+of+wonders+4+video+game&form=QBLH&sp=-1&ghc=1&lq=0&pq=age+of+wonders+4+video+gam&sc=3-26&qs=n&sk=&cvid=4EEEF19338F54CAE9F6DB81DF080C450&ghsh=0&ghacc=0&ghpl=',
                    'DNT': '1',
                    'Sec-GPC': '1',
                    'Connection': 'keep-alive',
                    # 'Cookie': 'MUID=0FD2A8B95349697F0AF2BC3A529B6829; MUIDB=0FD2A8B95349697F0AF2BC3A529B6829; _EDGE_S=F=1&SID=0EBB037113026F4E101917F212D06E74&mkt=en-ca; _EDGE_V=1; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=43289598238242DB9042835DE206F0AD&dmnchg=1; SRCHUSR=DOB=20240518&T=1715993917000; SRCHHPGUSR=SRCHLANG=en&BRW=XW&BRH=S&CW=1920&CH=533&SCW=1903&SCH=4050&DPR=1.0&UTC=-240&DM=1&WTS=63851590717&HV=1715993930&PRVCW=1920&PRVCH=936&CIBV=1.1742.1&EXLTT=1; _SS=SID=0EBB037113026F4E101917F212D06E74&R=3&RB=0&GB=0&RG=200&RP=0; _HPVN=CS=eyJQbiI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiUCJ9LCJTYyI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiSCJ9LCJReiI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyNC0wNS0xOFQwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIlRucyI6MCwiRGZ0IjpudWxsLCJNdnMiOjAsIkZsdCI6MCwiSW1wIjoyLCJUb2JuIjowfQ==; ak_bmsc=60A1FBA99EB7B4484C382B75506E28BA~000000000000000000000000000000~YAAQVw/QF0RMlHqPAQAADTo1iRe8XpEwdaYb8ChoLk6s8XO43T2R2HpaupmTpKsmgRsDvcVV71G41qalfCK/9rOCnRIhzfkg9u/QnEWP+1Dzy2iKEiSNIwg0VeZAsr/Vr/DG2vjicU+RGItd6CkfG8zE/tBlp0rd1Yt18dX6uwZMr0qtu9KIFhtq2cTU6mlH/o7fdV2Pm4HL3d7Fk/Q4xg3shmcZjzquQ7+PpduSmlyaQkKBEY2KX0hgkHLrBsbuQCVXgvGvmlAayDaDwnH4Pj3+7+GrwvG+uF1X38t2kWqBiir4PTrDiXzOpM6g8OCkEOpflo45n2cybrjbc5/zKbhMvbjOAcPg/xnfdDM41VZS3GsKHp1zqQ8Vl63SC1Ppo9jKU9N6Fw==; BCP=AD=0&AL=0&SM=0; _UR=cdxcls=0&QS=0&TQS=0; ipv6=hit=1715997532191; _RwBf=r=0&ilt=2&ihpd=1&ispd=1&rc=3&rb=0&gb=0&rg=200&pc=0&mtu=0&rbb=0&g=0&cid=&clo=0&v=2&l=2024-05-17T07:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&ard=0001-01-01T00:00:00.0000000&rwdbt=0001-01-01T00:00:00.0000000&rwflt=0001-01-01T00:00:00.0000000&o=2&p=&c=&t=0&s=0001-01-01T00:00:00.0000000+00:00&ts=2024-05-18T00:58:48.7067294+00:00&rwred=0&wls=&wlb=&wle=&ccp=&cpt=&lka=0&lkt=0&aad=0&TH=; _Rwho=u=d&ts=2024-05-18; ai_session=qSQyjTywAsNv3DMYMl1i7C^|1715993921844^|1715993921844; bm_sv=50EEBC49F587AA5AC3B04921FCBAD36D~YAAQVw/QFwdNlHqPAQAAkVs1iRdic9uP8iruBWXuHh7qonV8K5KYHHLpV25VnfCXZINc9i3DKA8xIsg925bn3MMbafFzGJnd8hMouZjdihEmwp+lknFUEuB03FPfoAJMst+ENrL+r3XxXl8C8qhLRPfe8lwPeVLx9lZzMN9n7PGlYpLB5SD81WEpb3a69YSVRpmU05OjDjQsnob3L74xNl+F3GENod3GiJZGG3AL+YXAZCBOAwP1rn1Bjdxmcg==~1; USRLOC=HS=1&ELOC=LAT=44.25663757324219^|LON=-76.56807708740234^|N=Kingston^%^2C^%^20Ontario^|ELT=4^|; dsc=order=ShopOrderDefault',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-origin',
                    # Requests doesn't support trailers
                    # 'TE': 'trailers',
                }
                auth = HTTPProxyAuth('dnbcukvf', 'pog5buvc42ya');
                #r = requests.get('https://www.google.com/search?q="{}" video game'.format(name), headers=headers, proxies={"http": "http://dnbcukvf-rotate:pog5buvc42ya@p.webshare.io:80/","https": "http://dnbcukvf-rotate:pog5buvc42ya@p.webshare.io:80/"}, auth=auth)
                # try using bing instead, google is blocking the requests
                try:
                    r = requests.get('https://www.bing.com/search?q="{}" video game'.format(name), headers=headers, proxies={"http": "http://dnbcukvf-rotate:pog5buvc42ya@p.webshare.io:80/","https": "http://dnbcukvf-rotate:pog5buvc42ya@p.webshare.io:80/"}, auth=auth)
                    print(r.url, r.status_code)
                    soup = BeautifulSoup(r.content, 'html.parser')
                    print(soup.find('span', {'class': 'sb_count'}).text)
                #print(soup.find('div',{'id':'resultStats'}).text)
                    resultg = int(soup.find('span', {'class': 'sb_count'}).text.split(' ')[1].replace('.',''))
                    realresult = True;
                except Exception as e:
                    realresult = False;
                    if e == AttributeError:
                        print("detected the scraper i think bing should be ashamed of themselves")
                    if e == ValueError:
                        print("gave string in sb_count")
                    if e == requests.exceptions.ChunkedEncodingError:
                        print("chunked encoding error")
                    pass
            #googlePopularity.append(resultg)









trends_result_dict = {}
trends_result_numerical_dict = {};
names_no_rm = names.copy();

with open('dataframe.csv', 'r') as f:
    lines = f.readlines()
    tempName = "";
    #zeros_ended = False;
    date_started = False;
    countdate = 0;
    for k, i in enumerate(lines):
        isplit = i.split(',')
        if i.startswith('date'):
            if not isplit[1] in trends_result_dict and isplit[1] in names:
                trends_result_dict[isplit[1]] = []; # empty array, key is name of the game. array will be filled with the trends of the game which will be averaged later
                tempName = isplit[1];
                names.pop(names.index(isplit[1]))
     #           zeros_ended = False;
                date_started = False;
                countdate += 1;
            else:
                #print("key already exists")
                tempName = "har har har har har"
        elif i.startswith('2'):
            if (date_started == False):
                if (parse(isplit[0]) >= parse(releaseDates[countdate-1], fuzzy_with_tokens=True)[0]):
                    date_started = True;
            elif (date_started == True):
           # if zeros_ended == False:
            #    if not isplit[1] == '0':
             #       zeros_ended = True;
            #elif zeros_ended == True:
            #if not isplit[1] == '0' and not tempName == 'har har har har har':
                if not tempName == 'har har har har har':
                    trends_result_dict[tempName].append(int(isplit[1]))

#print(len(names_no_rm))

#zero_threshold = 0.25;

for i, v in trends_result_dict.items():
    #if len([x for x in trends_result_dict[i] if x != 0]) >= zero_threshold * len(trends_result_dict[i]):
    trends_result_dict[i] = (sum(v) / len(v)) if len(v) > 0 else -1;
    if (i == "Phasmophobia"):
        print(sum(v), "|", len(v))
        # get median of the array at index i and store it in the dictionary
    #trends_result_dict[i] = np.median(v);
    #else:
    #trends_result_dict[i] = -1;
    for j, w in enumerate(names_no_rm):
        if w == i:
            trends_result_numerical_dict[j] = trends_result_dict[i];

trends_result_numerical_dict_temp = {key:trends_result_numerical_dict[key] for key in sorted(trends_result_numerical_dict.keys())}
trends_result_numerical_dict = trends_result_numerical_dict_temp.copy();
#trends_result_numerical_dict_temp = trends_result_numerical_dict.copy();

tcount = 0;
for i, v in trends_result_numerical_dict.items():
    #print(i, tcount)
    if i - tcount > 1:
        for j in range(i - tcount - 1):
            trends_result_numerical_dict_temp[tcount + j + 1] = -1;
    tcount = i;

trends_result_numerical_dict = {key:trends_result_numerical_dict_temp[key] for key in sorted(trends_result_numerical_dict_temp.keys())}
#trends_result_numerical_dict = trends_result_numerical_dict_temp.copy();

#print(trends_result_numerical_dict, len(trends_result_numerical_dict))


#print(trends_result_dict, len(trends_result_dict))
#print(names)
#tempcc = -1;
for i, v in trends_result_numerical_dict.items():
    #print(i)
    #if i-tempcc > 1:
        #print("skipped " + str(i))
    #tempcc = i;
    googlePopularity.append(v)


'''
sampleDictArray = [];
with open('sample.csv', 'w') as f:
    fields = ['Name', 'Peak CCU', 'Price (USD)', 'Review Ratio', 'Web Exposure']
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    for i in range(29):
        randchoice = random.randint(0, len(popularity))
        sampleDictArray.append({'Name': gameNames[randchoice], 'Peak CCU': popularity[randchoice], 'Price (USD)': prices[randchoice], 'Review Ratio': reviewRatio[randchoice], 'Web Exposure': googlePopularity[randchoice]})
    writer.writerows(sampleDictArray)
'''

print(googlePopularity[gameNames.index("Phasmophobia")])

#fs = open('currentlyHaveScraped.txt', 'r')
#for i in fs:
#    if (i.startswith('About')):
#        try:
#            googlePopularity.append(int(i.split(' ')[1].replace('.','')))
#        except ValueError:
#            pass

#with open('googlepopularity.json', 'w') as f:
#    json.dump(googlePopularity, f)

#fsj = open('googlepopularity.json', 'r')
#googlePopularity = json.load(fsj)

#print(len(googlePopularity))
#print(count);

#for i in prices:
#    if pricesPopularity[i]:



'''
popularity = np.asarray(popularity);

for i, v in enumerate(popularity):
    if (is_outlier(popularity)):
        del popularity[i];
        del prices[i];
'''
#cf = np.polyfit(prices, popularity, 1);
#poly1d = np.poly1d(cf);

print(googlePopularity)

popNO, pricesNO, reviewRatioNO, googlePopularityNO, namedataNO, estimatedOwnersNO = IQR_outliers_remove_all(popularity, prices, reviewRatio, googlePopularity, gameNames, estimatedOwners);
#popNO, pricesNO, reviewRatioNO, googlePopularityNO = popularity, prices, reviewRatio, googlePopularity

print(np.mean(popNO))

print(len(popNO))

data_csv_dict = [];
with open('datacsv.csv', 'w', newline='', encoding='utf-8') as f:
    fields = ['Name', 'Peak CCU', 'Price (USD)', 'Review Ratio', 'Web Exposure']
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader();
    for i in range(len(popNO)):
        data_csv_dict.append({'Name': namedataNO[i],'Peak CCU': popNO[i], 'Price (USD)': pricesNO[i], 'Review Ratio': reviewRatioNO[i], 'Web Exposure': googlePopularityNO[i]});
    writer.writerows(data_csv_dict);


vdict = []
for i in range(len(popNO)):
    vdict.append({'r': reviewRatioNO[i], 'w': googlePopularityNO[i], 'p': pricesNO[i]})
vec = DictVectorizer()
X = vec.fit_transform(vdict)
y = popNO;

clf = linear_model.LinearRegression()
clf.fit(X, y)
print(clf.coef_, clf.intercept_)

prediction = clf.predict(X)
residual = y - prediction;
# print the sum of residuals squared
print(np.sum(residual ** 2), " is the sum of residuals squared")

# get total sum of squares
tss = np.sum((y - np.mean(y)) ** 2)
# get the r squared value
print(tss, " is the total sum of squares")
r_squared = 1 - (np.sum(residual ** 2) / tss)
print(r_squared, " is the r squared value")


# create a plane of regression using the r and p values
r = np.linspace(min(reviewRatioNO), max(reviewRatioNO), 100)
w = np.linspace(min(googlePopularityNO), max(googlePopularityNO), 100)
p = np.linspace(min(pricesNO), max(pricesNO), 100)
#R, W, P = np.meshgrid(w, p, r, indexing='ij')
W, P = np.meshgrid(w, p)
#Z = clf.coef_[0] * W + clf.coef_[1] * P + clf.coef_[2] * R + clf.intercept_
Z2D = clf.coef_[1] * W + clf.coef_[2] * P + clf.intercept_

#R_flat = R.flatten()
#W_flat = W.flatten()
#P_flat = P.flatten()
#Z_flat = Z.flatten()

print(clf.score(X, y))

fig = plt.figure()
fig.set_figwidth(40)
fig.set_figheight(10)
ax = plt.axes(projection='3d')
ax.set_xlabel('Mean of Web Exposure on Google Trends', fontsize=12, color='green')
ax.set_ylabel('Price (USD)', fontsize=12, color='green')
ax.set_zlabel('Peak Concurrent Players', fontsize=12, color='green')
img = ax.scatter3D(googlePopularityNO, pricesNO, popNO, c=reviewRatioNO, cmap=plt.hot())
cbar = fig.colorbar(img)
cbar.set_label("Ratio of Positive Reviews to Negative Reviews")
ax.plot_surface(W, P, Z2D, alpha=0.5)
#sc = ax.scatter3D(W_flat, P_flat, Z_flat, c=R_flat, cmap='hot', alpha=0.5, label='Regression Plane')
#plane = ax.plot_surface(W, P, Z, facecolors=plt.cm.hot(R/np.max(R)), alpha=0.5, rstride=100, cstride=100)
#ax.plot_surface(W, P, R, Z2D, alpha=0.5)
plt.title("3D Graph of Web Exposure, Price, Review Ratio, and Popularity")
plt.show()


slope, intercept, r_value, p_value, std_err = stats.linregress(pricesNO, estimatedOwnersNO);
line = slope*np.array(pricesNO)+intercept;

#plt.plot(prices, popularity, "yo", prices, poly1d(prices), "--k");
plt.plot(pricesNO, line, "r", label = "y={:.2f}x+{:.2f}".format(slope, intercept));
# scatter to demonstrate no correlation between bing scraper and popularity
plt.scatter(pricesNO, estimatedOwnersNO, color = "k", s=7.5);
plt.title("Number of Search Results on Bing and Peak Concurrent Players");
plt.xlabel("Number of Search Results on Bing");
plt.ylabel("Peak Concurrent Players");
plt.show();

plt.scatter(googlePopularityNO, popNO, color = "k", s=7.5);
plt.title("Mean of Web Exposure on Google Trends and Peak Concurrent Players");
plt.xlabel("Mean of Web Exposure on Google Trends");
plt.ylabel("Peak Concurrent Players");
plt.show();


slope, intercept, r_value, p_value, std_err = stats.linregress(pricesNO, popNO);
line = slope*np.array(pricesNO)+intercept;

#plt.plot(prices, popularity, "yo", prices, poly1d(prices), "--k");
plt.plot(pricesNO, line, "r", label = "y={:.2f}x+{:.2f}".format(slope, intercept));

plt.scatter(pricesNO, popNO, color = "k", s=7.5);
plt.title("Price and Peak Concurrent Players");
plt.xlabel("Price (USD)");
plt.ylabel("Peak Concurrent Players");
plt.show();




for i, v in monthsData.items():
    monthsAverage[i] = v[1] / v[0];


plt.bar(monthsAverage.keys(), monthsAverage.values());
plt.title("Games Released by Month");


plt.show();




popularity.sort();
prices.sort();

popularity_no_outliers = IQR_outliers(np.array(popularity));
prices_no_outliers = IQR_outliers(np.array(prices));

# PRICE CURVE
fig, (ax1, ax2) = plt.subplots(nrows = 1, ncols = 2);
prices_no_outliers.sort();
mu = np.mean(prices_no_outliers); print(mu)
sigma = np.std(prices_no_outliers); print(sigma)

norm_pdf = np.array(stats.norm.pdf(prices_no_outliers, mu, sigma));
ax1.plot(prices_no_outliers, norm_pdf)
ax1.set(xlabel="Prices (Outliers Removed) Min: " + str(round(min(prices_no_outliers), 4)) + " Max: " + str(round(max(prices_no_outliers), 4)), ylabel = "Probability", title="Normal Distribution of Prices")

sample_value = 40
z = (sample_value - mu) / sigma;

# POPULARITY CURVE
popularity.sort();
mu = np.mean(popularity_no_outliers); print(mu)
sigma = np.std(popularity_no_outliers); print(sigma)

norm_pdf = np.array(stats.norm.pdf(popularity_no_outliers, mu, sigma));
ax2.plot(popularity_no_outliers, norm_pdf)
ax2.set(xlabel="Highest Concurrent Players (Outliers Removed) Min: " + str(min(popularity_no_outliers)) + " Max: " + str(max(popularity_no_outliers)), ylabel = "Probability", title="Normal Distribution of Highest Concurrent Players")

pop_result = z * sigma + mu;
print(z, pop_result);

plt.show();











slope, intercept, r_value, p_value, std_err = stats.linregress(prices, popularity);
line = slope*np.array(prices)+intercept;

#plt.plot(prices, popularity, "yo", prices, poly1d(prices), "--k");
plt.plot(prices, line, "r", label = "y={:.2f}x+{:.2f}".format(slope, intercept));
plt.scatter(prices, popularity, color = "k", s=3.5);
plt.legend(fontsize = 9);
plt.show();

sloper, interceptr, r_valuer, p_valuer, std_errr = stats.linregress(reviewRatio, popularity);
liner = sloper*np.array(reviewRatio)+interceptr;

#plt.plot(prices, popularity, "yo", prices, poly1d(prices), "--k");
plt.plot(reviewRatio, liner, "r", label = "y={:.2f}x+{:.2f}".format(sloper, interceptr));
plt.scatter(reviewRatio, popularity, color = "k", s=3.5);
plt.legend(fontsize = 9);
plt.show();

pcounts, pbins = np.histogram(prices);
plt.stairs(pcounts, pbins);
plt.show();

# Bin limits
num_bin = 10
bin_lims = np.linspace(0,1,num_bin+1)
bin_centers = 0.5*(bin_lims[:-1]+bin_lims[1:])
bin_widths = bin_lims[1:]-bin_lims[:-1]

popularity_no_outliers = IQR_outliers(np.array(popularity));
reviewRatio = IQR_outliers(np.array(reviewRatio));

reviewRatio.sort();
popularity_no_outliers.sort();

fig, (ax1, ax2) = plt.subplots(nrows = 1, ncols = 2);
print(max(popularity_no_outliers), min(popularity_no_outliers), max(reviewRatio), min(reviewRatio))
counts, bins = np.histogram(popularity_no_outliers, bins=np.arange(min(popularity_no_outliers), max(popularity_no_outliers) + 1, (max(popularity_no_outliers)-min(popularity_no_outliers)) / 60));
ax1.stairs(NormalizeData(counts), bins);
#plt.show();z

rcounts, rbins = np.histogram(reviewRatio, bins=np.arange(min(reviewRatio), max(reviewRatio) + 1, (max(reviewRatio)-min(reviewRatio)) / 60));
ax2.stairs(NormalizeData(rcounts), rbins);

#histP = counts/np.max(counts);
#histR = rcounts/np.max(rcounts);

#plt.bar(bin_centers, histP, width = bin_widths, align = 'center')
#plt.bar(bin_centers, histR, width = bin_widths, align = 'center', alpha = 0.5)


plt.show();

#popularity_no_outliers = IQR_outliers(np.array(popularity));
#reviewRatio = IQR_outliers(np.array(reviewRatio));

# REVIEW RATIO CURVE
fig, (ax1, ax2) = plt.subplots(nrows = 1, ncols = 2);
reviewRatio.sort();
mu = np.mean(reviewRatio); print(mu)
sigma = np.std(reviewRatio); print(sigma)
#x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
#x = np.linspace(0, 1, 100)
#ax1.plot(NormalizeData(reviewRatio), np.array(stats.norm.pdf(reviewRatio, mu, sigma)))
#norm_pdf = np.array(stats.norm.pdf(reviewRatio, mu, sigma));
#ax1.plot(reviewRatio, norm_pdf)
edges, hist = powerlaw.pdf(reviewRatio)
bin_centers = (edges[1:]+edges[:-1])/2.0
ax1.plot(bin_centers, hist)

ax1.set(xlabel="Positive Review / Negative Reviews Ratio (Outliers Removed) Min: " + str(round(min(reviewRatio), 4)) + " Max: " + str(round(max(reviewRatio), 4)), ylabel = "Probability", title="Normal Distribution of Review Ratio")
#ax = plt.gca()
#ax.set_xlim([0, max(reviewRatio)])
#ax.set_ylim([0, 1])
# test value to convert to z score and convert to popularity
#sample_value = 0.0025;
sample_value = 2 #np.interp(25, reviewRatio, norm_pdf);
z = (sample_value - mu) / sigma;

# POPULARITY CURVE

popularity.sort();
mu = np.mean(popularity_no_outliers); print(mu)
sigma = np.std(popularity_no_outliers); print(sigma)
#x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
#x = np.linspace(0, 1, 100)
#ax2.plot(NormalizeData(popularity_no_outliers), np.array(stats.norm.pdf(popularity_no_outliers, mu, sigma)))
    #norm_pdf = np.array(stats.norm.pdf(popularity_no_outliers, mu, sigma));
#fit = stats.powerlaw.fit(popularity_no_outliers)
#power_pdf = np.array(fit)
edges, hist = powerlaw.pdf(popularity_no_outliers)
bin_centers = (edges[1:]+edges[:-1])/2.0
ax2.plot(bin_centers, hist)

#ax2.plot(popularity_no_outliers, power_pdf)
ax2.set(xlabel="Highest Concurrent Players (Outliers Removed) Min: " + str(min(popularity_no_outliers)) + " Max: " + str(max(popularity_no_outliers)), ylabel = "Probability", title="Normal Distribution of Highest Concurrent Players")
#ax = plt.gca()
#ax.set_xlim([0, 1])

pop_result = z * sigma + mu;
#sample_result = np.interp(pop_result, norm_pdf, popularity_no_outliers);
print(z, pop_result);

plt.show();
#ax.set_ylim([0, 1])
plt.hist2d(reviewRatio, popularity, bins=(np.arange(min(reviewRatio), max(reviewRatio) + 5, 5), np.arange(min(reviewRatio), max(reviewRatio) + 5, 5)), cmap = plt.cm.jet)
plt.colorbar();
plt.show()

sns.boxplot(popularity); # Boxplot outliers default calculation is 1.5 * IQR
plt.show();

#reviewRatio = positiveReviews / negativeReviews;



#clump into 1000 data points per dot





