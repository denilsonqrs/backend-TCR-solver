import math
#Funcao para verificar se o Sistema pode ser resolvivel pro TCR.
def eh_resolvivel(mods):
    for i in range(len(mods)-1):
        for j in range(i+1, len(mods)):
            if math.gcd(mods[i], mods[j])!=1:
                return False
        
    return True

def resolve_congruecia(x, remain, mod):
    solvable = True
    gcd_x_mod = math.gcd(x, mod)
    if (remain % gcd_x_mod) != 0:
        solvable = False
        return solvable, x, remain, mod
    
    if x == 1: return solvable, x, remain, mod
    
    if gcd_x_mod > 1:
        x //= gcd_x_mod
        remain //= gcd_x_mod
        mod //= gcd_x_mod
        return resolve_congruecia(x, remain, mod)
    
    _, inverso, _ = euclides_estendido(x, mod)
    
    x = 1
    remain = (remain * inverso) % mod 
    
    return solvable, x, remain, mod   
        
#funcao recursiva de calculo do euclides estendido, para encontrarmos os coeficientes de bezout 
def euclides_estendido(a, b):
    if b == 0:
        return a, 1, 0
    
    gcd, x1, y1 = euclides_estendido(b, a%b)
    
    x = y1
    y = x1 - (a//b)*y1
    
    return gcd, x, y
#funcao para calcular os inversos de cada modulo parcial.
def calcula_inversos(remains, mods):
    all_d = []
    for i in range(len(remains)):
        _, x, _ = euclides_estendido(remains[i], mods[i])
        if x > 0:
           all_d.append(x)
        else:
            all_d.append(x+mods[i])
    return all_d
 

def main():
    all_x = list(map(int, input("Insira todos os coeficientes de x: ").split()))
    remains = list(map(int, input("Insira todos os restos: ").split()))
    mods = list(map(int, input("Insira todos os mods: ").split()))
    
    for i in range(len(all_x)):
        solvable, x, remain, mod = resolve_congruecia(all_x[i], remains[i], mods[i])
        if not solvable:return ValueError
        all_x[i] = x
        remains[i] = remain
        mods[i] = mod
    
    if not eh_resolvivel(mods):
        print("nao e possivel resolucionar")
        exit(0)
    
    M = 0 #Modulo Global
    for mod in mods:
        if M:
            M *= mod
        else:
            M = mod   

    all_c = []  #Guarda todos os modulos parciais.
    for mod in mods:
        c = M // mod
        all_c.append(c)
        
    all_d = calcula_inversos(all_c, mods)
    
    total_sum = 0
    for i in range(len(remains)):
        total_sum+= remains[i] * all_c[i] * all_d[i]
        
    print(f"{int(total_sum%M)}=mod{M}")
    
main()
       