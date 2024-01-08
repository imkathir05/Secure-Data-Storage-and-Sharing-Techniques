
from datetime import date

today = date.today()

# dd/mm/YY
d1 = today.strftime("%d/%m/%Y")
print("d1 =", d1)

#print(today.strftime("%d-%m-%Y %H:%M:%S %p"))
