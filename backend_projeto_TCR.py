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
def eh_resolvivel(mods, passos):
    for i in range(len(mods)-1):
        for j in range(i+1, len(mods)):
            mdc = math.gcd(mods[i], mods[j])
            passos["passo2"].append(f"$MDC({mods[i]}, {mods[j]}) = {mdc}$")
            if mdc != 1:
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

def calcula_inversos(remains, mods, passos):
    all_d = []
    for i in range(len(remains)):
        _, x, _ = euclides_estendido(remains[i], mods[i])
        if x > 0:
           all_d.append(x)
        else:
            all_d.append(x+mods[i])
            passos["passo4"].append(f"${remains[i]} \\cdot d_{{i+1}} \\equiv 1 \\pmod{{{mods[i]}}} \\rightarrow d_{{i+1}} = {x + mods[i]}$")
    return all_d

# 3. A ROTA DA API 
@app.post("/api/solve")
def resolver_tcr_endpoint(request: EquacoesRequest):
    passos = {
    "passo1": [],
    "passo2": [],
    "passo3": [],
    "passo4": [],
    "passo5": ["",""]
}
    # Pega as listas que vieram do JSON
    all_x = request.all_x.copy()
    remains = request.remains.copy()
    mods = request.mods.copy()
    
    # Validações e simplificações
    for i in range(len(all_x)):
        solvable, x, remain, mod = resolve_congruecia(all_x[i], remains[i], mods[i])
        
        if not solvable:
            return {"status": "error", "message": f"A equação {i+1} não tem solução."}
        passos["passo1"].append(f"${all_x[i]}x \\equiv {remains[i]} MOD({mods[i]}) \\rightarrow {x} \\equiv {remain} MOD({mod})$")   
        all_x[i] = x
        remains[i] = remain
        mods[i] = mod
    
    if not eh_resolvivel(mods, passos):
        return {"status": "error", "message": "Não é possível solucionar: Módulos não são coprimos."}
    
    # Cálculo do Modulo Global (M)
    M = 1 
    for mod in mods:
        M *= mod   
    passos["passo3"].append(f"Modulo Global M = ${'\\cdot'.join(str(n) for n in mods)} = {M}$")
    all_c = []  
    for mod in mods:
        c = M // mod
        all_c.append(c)
        passos["passo3"].append(f"$m{len(passos['passo3'])} = {M} / {mod} = {c}$")
        
    all_d = calcula_inversos(all_c, mods, passos)
    
    total_sum = 0
    for i in range(len(remains)):
        total_sum += remains[i] * all_c[i] * all_d[i]
        if i > 0:
            passos["passo5"][0]+=" + "
        passos["passo5"][0]+=f"$({remains[i]} \\cdot {all_c[i]} \\cdot {all_d[i]})$"
        
    passos["passo5"][1] = f"x ≡ {total_sum} (mod {M})"    
    solucao_final = int(total_sum % M)
    
    
    # Retorna a resposta final em formato JSON
    return {
        "status": "success",
        "solucao": solucao_final,
        "modulo_global": M,
        "texto_exibicao": f"x ≡ {solucao_final} (mod {M})",
        "passos": passos
    }
       