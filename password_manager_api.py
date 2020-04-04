import os.path
from os import path
from cryptography.fernet import Fernet
import json
class PasswordManager(object):

    def add_login(self, service, user, password):
        #print(service, user, password)
        user = user.lower()
        service = service.lower()
        with open('key/key.txt', 'rb') as f:
            key = f.read()
        f.close()
        if path.exists('logins.txt'):
            with open('logins.txt', 'r') as f:
                log = json.load(f)
            f.close()
            fern = Fernet(key)
            encrypted_pass = fern.encrypt(password.encode())
            if service in log.keys():
                if user in log[service][0].keys():
                    # replace existing password with new one
                    log[service][0][user] = str(encrypted_pass)
                else:
                    log.setdefault(service, []).append({user: str(encrypted_pass)})
            else:
                log.setdefault(service, []).append({user: str(encrypted_pass)})
        else:
            fern = Fernet(key)
            encrypted_pass = fern.encrypt(password.encode())
            log = dict()
            log.setdefault(service, []).append({user: str(encrypted_pass)})

        with open('logins.txt', 'w') as f:
            json.dump(log, f)
        f.close()


    def get_password(self, service, user):
        service = service.lower()
        user = user.lower()
        with open('key/key.txt', 'rb') as f:
            key = f.read()
        f.close()

        fern = Fernet(key)
        if path.exists('logins.txt'):
            with open('logins.txt', 'r') as f:
                log = json.load(f)
            f.close()
            if service not in log.keys():
                return {'Invalid': "You don't have a password stored for service {}".format(service)}
            # elif user not in log[service][0].keys():
            #     return {'Invalid': "You don't have a password stored for user {}".format(user)}
            else:
                str_byte = ""
                for login in log[service]:
                    if user in login.keys():
                        str_byte = login[user]
                        break
                if str_byte == "":
                    return {'Invalid': "You don't have a password stored for user {}".format(user)}
                #str_byte = log[service][0][user]
                sliced_str_byte = str_byte[2:len(str_byte)-1]
                encrypted_password = sliced_str_byte.encode()
                decrypted_password = fern.decrypt(encrypted_password).decode()
                return {'password': decrypted_password}
        else:
                return {'Invalid': "You don't have any logins stored"}

    def list_usernames(self, service):
        service = service.lower()
        if path.exists('logins.txt'):
            with open('logins.txt', 'r') as f:
                log = json.load(f)
            f.close()
            if service not in log.keys():
                return {'Invalid': "No usernames for service: "+service}
            else:
                # return list(log[service])
                usernames = []
                for entry in log[service]:
                    usernames.extend(list(entry.keys()))
                return {'usernames': usernames}

        else:
                return {'Invalid': "You don't have any usernames stored"}
