import json
import requests


def send_stock_message(phone_num):
    url = "https://api.leancloud.cn/1.1/requestSmsCode"
    app_id = "1rKIB5EL0gp2d72TIDoUBlnA-gzGzoHsz"
    app_key = "NA5AMwmvmNYzN5SSQuNpzeV2"
    params = {'mobilePhoneNumber': phone_num}

    requests.post(url,
                  data=json.dumps(params),
                  headers={
                      'Content-Type': 'application/json',
                      'X-LC-Id': app_id,
                      'X-LC-Key': app_key
                  })

if __name__ == '__main__':
    send_stock_message('18639403096')
