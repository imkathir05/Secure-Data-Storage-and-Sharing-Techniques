import base64

sample_string = "GeeksForGeeks is the best"
sample_string_bytes = sample_string.encode("ascii")

base64_bytes = base64.b64encode(sample_string_bytes)
base64_string = base64_bytes.decode("ascii")

print("Encoded string:", base64_string)


base64_string ="R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA=="
base64_bytes = base64_string.encode("ascii")
  
sample_string_bytes = base64.b64decode(base64_bytes)
sample_string = sample_string_bytes.decode("ascii")
  
print("Decoded string:",sample_string)