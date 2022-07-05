import secrets
import string
import sys

args = sys.argv


def get_random_password_string():
    # 入力値チェック
    # 引数を取得する
    if len(sys.argv) == 6:
        try:
            password_length = int(args[1])
        except Exception as error:
            print("Input Error : 文字数は数字で入力してください")
            return
        
        is_lowercase = args[2] == '1'
        is_uppercase = args[3] == '1'
        is_digits = args[4] == '1'
        is_punctuation = args[5] == '1'
    else:
        print("Input Error : 条件は5つ入力してください")
        return
    
    if password_length < 5:
        print("Input Error : 文字数は5文字以上にしてください")
        return
    
    s1 = string.ascii_lowercase
    s2 = string.ascii_uppercase
    s3 = string.digits
    s4 = string.punctuation
    
    print("args : {}".format(args))
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
        print("Input Error : 条件は1つ以上1を指定してください")
        return
    
    # password = ''.join(secrets.choice(chars) for x in range(int(args[1])))
    # print(password)

    # 任意の数を指定の文字数分取得する
    password = ''
    for x in range(password_length):
        password2 = secrets.choice(chars)
        password += password2
    print(password)

get_random_password_string()