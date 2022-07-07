import secrets
import string
from flask import Flask, request

api = Flask(__name__)

@api.route('/', methods=['POST'])
def get_random_password_string():

    data = request.get_json()
    # 入力値チェック
    # 引数を取得する
    try:
        password_length = int(request.data.length)
    except Exception as error:
        return "Input Error : 文字数は数字で入力してください"
        
    is_lowercase = request.data.is_lowercase == '1'
    is_uppercase = request.data.is_uppercase == '1'
    is_digits = request.data.is_digits == '1'
    is_punctuation = request.data.is_punctuation == '1'
        
    if password_length < 5:
        return "Input Error : 文字数は5文字以上にしてください"
    
    s1 = string.ascii_lowercase
    s2 = string.ascii_uppercase
    s3 = string.digits
    s4 = string.punctuation
    
    print("s1 : {}".format(s1))
    print("s2 : {}".format(s2))
    print("s3 : {}".format(s3))
    print("s4 : {}".format(s4))

    chars = ''
    
    if is_lowercase == True:
        chars += s1
    
    if is_uppercase == True:
        chars += s2

    if is_digits == True:
        chars += s3

    if is_punctuation == True:
        chars += s4
    
    if chars == '':
        return "Input Error : 条件は1つ以上1を指定してください"

    # 任意の数を指定の文字数分取得する
    password = ''
    for x in range(password_length):
        password2 = secrets.choice(chars)
        password += password2
    return request.get_json().get_data()

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=3000)