WTF_CSRF_ENABLED = True

keyfile = open('../.cloudmatrix_k','r')
SECRET_KEY = keyfile.read()
keyfile.close()