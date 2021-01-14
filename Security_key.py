from cryptography.fernet import Fernet
key = b'McJLYEHkEOwW6zHRAbAiMYYO_OXP5aoJysaHmfzNUwY='
cipher_suite = Fernet(key)
def encrypt(input):
    
    #transformatting to byte
    b_format_password = bytes(input, 'utf-8')
    password = b_format_password
    ciphered_text = cipher_suite.encrypt(password)   #required to be bytes
    #transfromatting back to string
    debyte_ciphered_text = ciphered_text.decode('UTF-8')
    #return the key value in string
    return(debyte_ciphered_text) 

def decrypt(input):
    #transformatting to byte
    b_format_password = bytes(input, 'utf-8')
    unciphered_text = (cipher_suite.decrypt(b_format_password))
    #transfromatting back to string
    debyte_password = unciphered_text.decode('UTF-8')
    #return the key value in string
    return(debyte_password)