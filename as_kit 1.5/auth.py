import hashlib


def auth(login_data):
    comment_data = {}
    print('wanna say something today?')
    print('yes or no')
    demand = input()

    if demand == 'yes':
        print('what do you want to say today')
        content = input()
        print('enter signature to continue \n signature = MD5 value of your comment + your csrf \n your csrf is %s' %
              login_data['csrf'])
        
        signautre = input()
        sign = login_data['csrf'] + content
        sign = hashlib.md5(sign.encode('UTF-8')).hexdigest()

        if signautre == sign:
            print('success')
            comment_data['comment'] = content
            comment_data['auth'] = True
            return comment_data
        else:
            print('failed')
            comment_data['auth'] = False
            return comment_data
    else:
        print('keep quiet is also not bad')
        comment_data['auth'] = False
        return comment_data