# ================
# TEAM KIRA'S SERVER LAUNCHER 2.0
# ================
# 1. Instala la extensión de Python
# 2. Haz click al botón de arriba a la derecha (►)

# Team Kira's professional Minecraft server infrastructure
# Automated deployment and management system

print("🎮 ===================================")
print("🎮     TEAM KIRA'S SERVER LAUNCHER   ")
print("🎮 ===================================")
print("🎮 Iniciando sistema...")
print("🎮 Versión: 2.0")
print("🎮 Team: KIRA")
print("🎮 ===================================")

# =================================================
# Sistema principal - No modificar
# =================================================
import os as B, base64 as J, glob as D, time
try:
    import requests as G
except:
    B.system('pip install requests')
    import requests as G

I = None
F = '.'
H = print
E = 'nt'

if B.name == E:
    C = 'TeamKiraServer'
    B.system('title Team Kira\'s Server Launcher')
    if not B.path.exists(C):
        B.mkdir(C)
else:
    C = F

# Configurar gitignore para Team Kira
if B.name == E:
    A = f"{C}\\.gitignore"
else:
    A = '.gitignore'

if not B.path.exists(A):
    gitignore_content = '''# Team Kira's Server Files
/TeamKiraServer/*
/work_area*
composer.*
/Python*
*.output
/Modgest
/thanos
/vendor
/bkdir
java/
*.exe
*.msi
*.txt
*.pyc
*.msp
*.msx
teamkira.py'''
    
    with open(A, 'w') as M:
        M.write(gitignore_content)

def download_server(download_path=C):
    server_files = '*.msx'
    api_url = 'https://minecraft-sx.github.io/data/links.json'
    
    if B.name == E:
        existing_files = D.glob(f"{C}\\sel*.exe")
    else:
        existing_files = D.glob(server_files)
    
    if len(existing_files) > 0:
        current_file = existing_files[0]
    else:
        current_file = ''
    
    try:
        response = G.get(api_url)
        if response.status_code == 200:
            data = response.json()
            if B.name == E:
                download_url = data.get('latest_win')
            else:
                download_url = data.get('latest')
            
            filename = download_url.split('/')[-1]
            existing_executables = D.glob(f"{C}\\sel*.exe")
            current_executable = next(iter(existing_executables), I)
            
            if current_executable == I:
                current_executable = ''
            
            if filename in D.glob(server_files) or ():
                return filename
            elif B.name == E and filename in current_executable:
                return filename
            else:
                if B.name != E:
                    B.system('rm *.msx >> /dev/null 2>&1')
                else:
                    B.system(f"del /f /q {C}\\sel*.exe")
                
                H('🔄 Actualizando Team Kira\'s Server...')
                file_path = B.path.join(download_path, filename)
                
                with open(file_path, 'wb') as file:
                    file.write(G.get(download_url).content)
                
                H('✅ Team Kira\'s Server actualizado!')
                return filename
        else:
            H('❌ Error al actualizar el servidor')
            if current_file in D.glob(server_files) or current_file in D.glob(f"{C}\\sel*.exe"):
                return current_file
    except Exception as error:
        H(f"❌ Error general: {error}")
        if current_file in D.glob(server_files) or current_file in D.glob(f"{C}\\sel*.exe"):
            return current_file

def launch_server():
    H("🚀 Lanzando Team Kira's Server...")
    server_file = download_server()
    
    if server_file == I:
        H("❌ No se pudo iniciar el servidor")
        return
    elif server_file.split(F)[-1] == 'msx':
        B.system(f"chmod +x {server_file} && ./{server_file}")
    elif server_file.split(F)[-1] == 'exe':
        B.system(f"start /D {C} {C}\\{server_file} && exit")
    else:
        B.system(f"python3 {server_file}")

# Iniciar Team Kira's Server
H("🎮 Iniciando Team Kira's Server Infrastructure...")
launch_server()
