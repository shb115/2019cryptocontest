#문제에서 주어진 것
p=0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
a=-3
b=0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
n=0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551

r=0xE45054EB5B1ABD976650F7F395BF51D0D8DD193E0174E7A14A1C8C127FBDF2DB
s1=0x09371E411284D26B4FAE3BD85B9545BBBFACE1FFE0868BD7701660A50C6E3F17
s2=0xB84ABC62455C570D5500186D83BFD1E1C23CB3135D4A32CE19B3DB61F1680EDC

hm1=0x389fa4507cd536c67db35b80b06ab0b0b034b7a5c67cf9a2d06ed00876d568f9
hm2=0x1a2fc26dc7ea5a2a4748b7cb2b1ef193d96ab2c99f93092f69e63075b28d1278

gx=0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296 
gy=0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5

publickey=0xdc9213e6cda06195098c901c36c0f20d9b5decd252f5f00bfc5a63cae0c5aeac

#역원 구하는 함수
def e_gcd(a,b):
    r1, r2 = a, b
    s1, s2 = 1, 0
    t1, t2 = 0,1
    while ( r2 > 0):
        q = r1//r2
        r = r1-q*r2
        r1, r2 = r2, r
        s = s1-q*s2
        s1, s2 = s2, s
        t = t1-q*t2
        t1, t2 = t2, t
    return s1

#d구하기
z=r*(s2-s1)
s=e_gcd(z,n)
d=((s1*hm2-s2*hm1)*s)%n
print(hex(d))

k=(e_gcd(s2,n)*(hm2+d*r))%n
print(hex(k))
kinv=e_gcd(k,n)
s=(kinv*(hm2+d*r))%n
print(hex(s))

#같은 것끼리 더하는 함수 (G+G=2G)
def same(x1,y1):
    lamda1=(3*x1*x1+a)*e_gcd(2*y1,p)
    x2=(lamda1*lamda1-2*x1)%p
    y2=(lamda1*(x1-x2)-y1)%p
    return x2,y2

#다른 것끼리 더하는 함수
def different(x1,y1,x2,y2):
    lamda2=(y2-y1)*e_gcd((x2-x1),p)
    x3=(lamda2*lamda2-x1-x2)%p
    y3=(lamda2*(x1-x3)-y1)%p
    return x3,y3

#16G를 만드는 함수
def sixteen(x1,y1):
    for i in range(4):        
        (x1,y1)=same(x1,y1)
    return x1,y1

#d의 각 자리
d1=[0xe,7,0xc,7,5,8,9,4,0,3,5,7,8,6,7,6,6,0xd,7,0,4,0xd,1,0xd,0xd,9,0xe,9,1,3,6,2,9,7,0xf,7,0xd,2,6,0xc,9,7,0xd,4,0xb,0xe,0,7,8,0xb,0xd,1,0xc,4,0xf,0xd,1,0xf,0xe,0xa,0xb,0xc,1,5]

#n의 각 자리
n1=[0xF,0xF,0xF,0xF,0xF,0xF,0xF,0xF,0,0,0,0,0,0,0,0,0xF,0xF,0xF,0xF,0xF,0xF,0xF,0xF,0xF,0xF,0xF,0xF,0xF,0xF,0xF,0xF,0xB,0xC,0xE,6,0xF,0xA,0xA,0xD,0xA,7,1,7,9,0xE,8,4,0xF,3,0xB,9,0xC,0xA,0xC,2,0xF,0xC,6,3,2,5,5,1]

#d의 각 자리별 좌표 초기화
g=[]
for i in range(64):
    g.append((0,0))

#d의 각 자리별 좌표 구하기
for i in range(64):
    if n1[63-i]==0:
        g[63-i]=(0,0)
    elif n1[63-i]==1:
        x1,y1=gx,gy
        for j in range(i):
            (x1,y1)=sixteen(x1,y1)
        g[63-i]=(x1,y1)
    elif n1[63-i]==2:
        x1,y1=gx,gy
        for j in range(i):
            (x1,y1)=sixteen(x1,y1)
        (x2,y2)=same(x1,y1)
        g[63-i]=(x2,y2)
    else:
        x1,y1=gx,gy
        for j in range(i):
            (x1,y1)=sixteen(x1,y1)
        (x2,y2)=same(x1,y1)
        for  j in range(n1[63-i]-2):
            (x3,y3)=different(x1,y1,x2,y2)
            x2,y2=x3,y3
        g[63-i]=(x2,y2)
    #print(g[63-i])


#d의 각 자리별 좌표 더하기
(x1,y1)=g[0]
for i in range(1,64):
    (x2,y2)=g[i]
    if x2==0 & y2==0:
        x3,y3=x1,y1
    else:
        (x3,y3)=different(x1,y1,x2,y2)
    x1,y1=x3,y3
#print(hex(x1),hex(y1))
#print(hex(n-publickey))
            
    


