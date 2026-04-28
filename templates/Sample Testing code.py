
a=int(input())
b=int(input())
b=(a+b)-(a=b)
print(a,b)
---------------------------------- ------
n=int(input())
x=0
for i in range(1,n):
    if n%i==0:
        x=x+i
if n==x:
    print("venu")
else:
    print("gopal")
