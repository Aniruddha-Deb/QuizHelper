class User:
	def __init__(self, name, age):
		self.name = name
		self.age = age
	
	def __str__(self):
		return f"{self.name}: {self.age}"

a = User("Aniruddha Deb", 18)
dic = {"me": a}
print(a)

for key in dic:
	print(key)
