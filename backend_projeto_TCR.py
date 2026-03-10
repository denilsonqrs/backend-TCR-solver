from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import math

app = FastAPI()

# Configuração de CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite requisições de qualquer origem
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Definindo a "bandeja" (formato que os dados vão chegar do frontend)
class EquacoesRequest(BaseModel):
    all_x: list[int]
    remains: list[int]
    mods: list[int]

#verifica se o sistema e resolvivel usando TCR, fazendo a verificacao de coprimidade par a par
def eh_resolvivel(mods):
    for i in range(len(mods)-1):
        for j in range(i+1, len(mods)):
            if math.gcd(mods[i], mods[j]) != 1:
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
    remains_new = (remain * inverso) % mod 
    
    return solvable, x, remains_new, mod   
        
def euclides_estendido(a, b):
    if b == 0:
        return a, 1, 0
    
    gcd, x1, y1 = euclides_estendido(b, a%b)
    
    x = y1
    y = x1 - (a//b)*y1
    
    return gcd, x, y

def calcula_inversos(remains, mods):
    all_d = []
    for i in range(len(remains)):
        _, x, _ = euclides_estendido(remains[i], mods[i])
        if x > 0:
           all_d.append(x)
        else:
            all_d.append(x+mods[i])
    return all_d

# 3. A ROTA DA API 
@app.post("/api/solve")
def resolver_tcr_endpoint(request: EquacoesRequest):
    # Pega as listas que vieram do JSON
    all_x = request.all_x.copy()
    remains = request.remains.copy()
    mods = request.mods.copy()
    
    # Validações e simplificações
    for i in range(len(all_x)):
        solvable, x, remain, mod = resolve_congruecia(all_x[i], remains[i], mods[i])
        
        if not solvable:
            return {"status": "error", "message": f"A equação {i+1} não tem solução."}
            
        all_x[i] = x
        remains[i] = remain
        mods[i] = mod
    
    if not eh_resolvivel(mods):
        return {"status": "error", "message": "Não é possível solucionar: Módulos não são coprimos."}
    
    # Cálculo do Modulo Global (M)
    M = 1 
    for mod in mods:
        M *= mod   

    # Modulos parciais (all_c)
    all_c = []  
    for mod in mods:
        c = M // mod
        all_c.append(c)
        
    all_d = calcula_inversos(all_c, mods)
    
    # Soma total
    total_sum = 0
    for i in range(len(remains)):
        total_sum += remains[i] * all_c[i] * all_d[i]
        
    solucao_final = int(total_sum % M)
    
    # Retorna a resposta final em formato JSON
    return {
        "status": "success",
        "solucao": solucao_final,
        "modulo_global": M,
        "texto_exibicao": f"x ≡ {solucao_final} (mod {M})"
    }
       