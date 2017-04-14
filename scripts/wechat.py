import requests

KEY = 'SCU6795T626d2618db87f38962932bcc9db5b31558cd3eccea6f0'


def send(title, content):
    request_url = 'http://sc.ftqq.com/{}.send'.format(KEY)
    requests.get(request_url, params={'text': title, 'desp': content})

if __name__ == "__main__":
    send('hello world !', 'Welcome To My World')
