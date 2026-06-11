import hashlib
with open('file.txt','r') as f:
	con=f.read()
	hashed=hashlib.sha256(con.encode()).hexdigest()
	print(hashed)