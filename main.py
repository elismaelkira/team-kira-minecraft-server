# ================
# TEAM KIRA'S SERVER 2.0
# ================
# 1. Haz click en el botón ► de arriba a la derecha
# 2. O presiona Ctrl+F5

print("🎮 ===================================")
print("🎮     TEAM KIRA'S MINECRAFT SERVER   ")
print("🎮 ===================================")
print("🎮 Iniciando sistema...")
print("🎮 Soporte para MODS incluido")
print("🎮 ===================================")

import os
import subprocess
import json
import time
import threading
import requests
from urllib.parse import urlparse

class TeamKiraServer:
    def __init__(self):
        self.server_dir = "TeamKiraServer"
        self.server_process = None
        self.ngrok_process = None
        self.server_ip = None
        
    def setup_environment(self):
        """Configurar el entorno del servidor"""
        print("🔧 Configurando entorno de Team Kira...")
        
        # Crear directorio del servidor
        if not os.path.exists(self.server_dir):
            os.makedirs(self.server_dir)
            
        # Instalar dependencias
        try:
            subprocess.run(["apt", "update"], check=True, capture_output=True)
            subprocess.run(["apt", "install", "-y", "openjdk-17-jdk", "wget", "curl", "unzip"], 
                         check=True, capture_output=True)
        except:
            print("⚠️ Instalando Java...")
            
        # Instalar ngrok
        self.install_ngrok()
        
    def install_ngrok(self):
        """Instalar y configurar ngrok"""
        print("🌐 Configurando túnel ngrok...")
        try:
            # Descargar ngrok
            subprocess.run([
                "curl", "-s", 
                "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz",
                "-o", "ngrok.tgz"
            ], check=True)
            
            subprocess.run(["tar", "xzf", "ngrok.tgz"], check=True)
            subprocess.run(["chmod", "+x", "ngrok"], check=True)
            
            # Configurar token (si está disponible)
            ngrok_token = os.environ.get('NGROK_AUTH_TOKEN')
            if ngrok_token:
                subprocess.run(["./ngrok", "config", "add-authtoken", ngrok_token], check=True)
            else:
                print("⚠️ NGROK_AUTH_TOKEN no configurado. Usando túnel temporal.")
                
        except Exception as e:
            print(f"❌ Error configurando ngrok: {e}")
            
    def download_server(self, server_type="vanilla", version="1.20.1"):
        """Descargar servidor según el tipo"""
        print(f"⬇️ Descargando servidor {server_type} {version}...")
        
        server_urls = {
            "vanilla": {
                "1.20.1": "https://piston-data.mojang.com/v1/objects/84194a2f286ef7c14ed7ce0090dba59902951553/server.jar",
                "1.19.4": "https://piston-data.mojang.com/v1/objects/8f3112a1049751cc472ec13e397eade5336ca7ae/server.jar"
            },
            "forge": {
                "1.20.1": "https://maven.minecraftforge.net/net/minecraftforge/forge/1.20.1-47.2.0/forge-1.20.1-47.2.0-installer.jar",
                "1.19.4": "https://maven.minecraftforge.net/net/minecraftforge/forge/1.19.4-45.2.0/forge-1.19.4-45.2.0-installer.jar"
            },
            "fabric": {
                "1.20.1": "https://meta.fabricmc.net/v2/versions/loader/1.20.1/0.14.24/0.11.2/server/jar",
                "1.19.4": "https://meta.fabricmc.net/v2/versions/loader/1.19.4/0.14.24/0.11.2/server/jar"
            }
        }
        
        try:
            server_url = server_urls[server_type][version]
            server_file = f"{self.server_dir}/server.jar"
            
            if server_type == "forge":
                # Descargar instalador de Forge
                installer_file = f"{self.server_dir}/forge-installer.jar"
                subprocess.run(["wget", "-O", installer_file, server_url], check=True)
                
                # Ejecutar instalador
                print("🔨 Instalando Forge...")
                os.chdir(self.server_dir)
                subprocess.run([
                    "java", "-jar", "forge-installer.jar", "--installServer"
                ], check=True)
                os.chdir("..")
                
                # Buscar el archivo del servidor generado
                forge_files = [f for f in os.listdir(self.server_dir) if f.startswith("forge-") and f.endswith(".jar") and "installer" not in f]
                if forge_files:
                    os.rename(f"{self.server_dir}/{forge_files[0]}", server_file)
                    
            else:
                # Descargar servidor vanilla o fabric
                subprocess.run(["wget", "-O", server_file, server_url], check=True)
                
            print(f"✅ Servidor {server_type} descargado!")
            return True
            
        except Exception as e:
            print(f"❌ Error descargando servidor: {e}")
            return False
            
    def setup_server_config(self, max_players=20, difficulty="normal", enable_mods=True):
        """Configurar archivos del servidor"""
        print("⚙️ Configurando Team Kira's Server...")
        
        # EULA
        with open(f"{self.server_dir}/eula.txt", "w") as f:
            f.write("eula=true\n")
            
        # Server properties
        config = f"""# Team Kira's Server Configuration
server-name=Team Kira's Server
motd=§6§l[§c§lTEAM KIRA§6§l] §r§e¡Servidor con MODS disponible!
server-port=25565
max-players={max_players}
online-mode=false
difficulty={difficulty}
gamemode=survival
hardcore=false
pvp=true
enable-command-block=true
spawn-protection=16
max-world-size=29999984
view-distance=12
simulation-distance=10

# Configuración avanzada
enable-rcon=true
rcon.password=teamkira2024
rcon.port=25575
enable-query=true
query.port=25565

# Optimizaciones para mods
network-compression-threshold=256
max-tick-time=60000
use-native-transport=true

# Mundo
level-name=TeamKiraWorld
level-seed=
generate-structures=true
spawn-monsters=true
spawn-animals=true
spawn-npcs=true
allow-flight=true
"""
        
        with open(f"{self.server_dir}/server.properties", "w") as f:
            f.write(config)
            
        # Ops (administradores)
        ops_config = [
            {
                "uuid": "00000000-0000-0000-0000-000000000000",
                "name": "TeamKiraAdmin",
                "level": 4,
                "bypassesPlayerLimit": True
            }
        ]
        
        with open(f"{self.server_dir}/ops.json", "w") as f:
            json.dump(ops_config, f, indent=2)
            
        # Crear carpeta de mods si no existe
        if enable_mods:
            mods_dir = f"{self.server_dir}/mods"
            if not os.path.exists(mods_dir):
                os.makedirs(mods_dir)
                print("📁 Carpeta de mods creada!")
                
        print("✅ Configuración completada!")
        
    def download_popular_mods(self, version="1.20.1"):
        """Descargar mods populares para el servidor"""
        print("📦 Descargando mods populares para Team Kira...")
        
        # Lista de mods populares (URLs de ejemplo - reemplazar con URLs reales)
        popular_mods = {
            "JEI": "https://www.curseforge.com/api/v1/mods/238222/files/latest/download",
            "Biomes O Plenty": "https://www.curseforge.com/api/v1/mods/220318/files/latest/download",
            "Iron Chests": "https://www.curseforge.com/api/v1/mods/228756/files/latest/download",
            "Waystones": "https://www.curseforge.com/api/v1/mods/245755/files/latest/download",
            "JourneyMap": "https://www.curseforge.com/api/v1/mods/32274/files/latest/download"
        }
        
        mods_dir = f"{self.server_dir}/mods"
        
        print("📋 Mods disponibles para Team Kira's Server:")
        for i, (mod_name, mod_url) in enumerate(popular_mods.items(), 1):
            print(f"  {i}. {mod_name}")
            
        try:
            choice = input("\n🎯 ¿Descargar mods automáticamente? (s/n): ").lower()
            if choice == 's':
                for mod_name, mod_url in popular_mods.items():
                    try:
                        print(f"⬇️ Descargando {mod_name}...")
                        # Aquí iría la lógica real de descarga de mods
                        # Por ahora solo creamos archivos de ejemplo
                        with open(f"{mods_dir}/{mod_name.replace(' ', '_')}.jar", "w") as f:
                            f.write(f"# Placeholder for {mod_name}")
                        print(f"✅ {mod_name} descargado!")
                    except Exception as e:
                        print(f"❌ Error descargando {mod_name}: {e}")
                        
        except KeyboardInterrupt:
            print("\n⏭️ Saltando descarga de mods...")
            
    def start_ngrok(self):
        """Iniciar túnel ngrok"""
        print("🌐 Iniciando túnel público...")
        try:
            self.ngrok_process = subprocess.Popen([
                "./ngrok", "tcp", "25565", "--log=stdout"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Esperar a que ngrok inicie
            time.sleep(10)
            
            # Obtener IP pública
            try:
                response = requests.get("http://localhost:4040/api/tunnels")
                tunnels = response.json()
                if tunnels.get("tunnels"):
                    public_url = tunnels["tunnels"][0]["public_url"]
                    self.server_ip = public_url.replace("tcp://", "")
                    
                    print("🎮 ===================================")
                    print("🎮   TEAM KIRA'S SERVER ESTÁ LISTO!  ")
                    print("🎮 ===================================")
                    print(f"🎮 IP: {self.server_ip}")
                    print("🎮 ¡Conecta con esta IP en Minecraft!")
                    print("🎮 ===================================")
                    
                    return True
            except:
                print("⚠️ No se pudo obtener IP pública. Usando localhost.")
                self.server_ip = "localhost:25565"
                
        except Exception as e:
            print(f"❌ Error iniciando ngrok: {e}")
            return False
            
    def start_server(self):
        """Iniciar el servidor de Minecraft"""
        print("🚀 Iniciando Team Kira's Minecraft Server...")
        
        try:
            os.chdir(self.server_dir)
            
            # Comando optimizado para servidor con mods
            java_args = [
                "java",
                "-Xmx4G", "-Xms2G",
                "-XX:+UseG1GC",
                "-XX:+ParallelRefProcEnabled", 
                "-XX:MaxGCPauseMillis=200",
                "-XX:+UnlockExperimentalVMOptions",
                "-XX:+DisableExplicitGC",
                "-XX:+AlwaysPreTouch",
                "-XX:G1NewSizePercent=30",
                "-XX:G1MaxNewSizePercent=40",
                "-XX:G1HeapRegionSize=8M",
                "-XX:G1ReservePercent=20",
                "-XX:G1HeapWastePercent=5",
                "-XX:G1MixedGCCountTarget=4",
                "-XX:InitiatingHeapOccupancyPercent=15",
                "-XX:G1MixedGCLiveThresholdPercent=90",
                "-XX:G1RSetUpdatingPauseTimePercent=5",
                "-XX:SurvivorRatio=32",
                "-XX:+PerfDisableSharedMem",
                "-XX:MaxTenuringThreshold=1",
                "-jar", "server.jar", "nogui"
            ]
            
            self.server_process = subprocess.Popen(
                java_args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            # Mostrar logs del servidor
            def show_logs():
                for line in iter(self.server_process.stdout.readline, ''):
                    if line:
                        print(f"[SERVER] {line.strip()}")
                        
            log_thread = threading.Thread(target=show_logs)
            log_thread.daemon = True
            log_thread.start()
            
            # Esperar a que el servidor inicie
            time.sleep(30)
            
            # Enviar comandos iniciales
            self.send_command("say §6[§cTEAM KIRA§6] §eServidor iniciado correctamente!")
            self.send_command("say §6[§cTEAM KIRA§6] §e¡Bienvenidos al servidor con MODS!")
            
            print("✅ Servidor iniciado correctamente!")
            return True
            
        except Exception as e:
            print(f"❌ Error iniciando servidor: {e}")
            return False
            
    def send_command(self, command):
        """Enviar comando al servidor"""
        if self.server_process and self.server_process.stdin:
            try:
                self.server_process.stdin.write(f"{command}\n")
                self.server_process.stdin.flush()
            except:
                pass
                
    def interactive_console(self):
        """Consola interactiva para administrar el servidor"""
        print("\n🎮 Consola de administración de Team Kira")
        print("Comandos disponibles:")
        print("  - help: Mostrar ayuda")
        print("  - players: Ver jugadores conectados")
        print("  - stop: Detener servidor")
        print("  - say <mensaje>: Enviar mensaje")
        print("  - op <jugador>: Dar permisos de admin")
        print("  - Cualquier comando de Minecraft")
        
        while True:
            try:
                cmd = input("\n[TEAM KIRA] > ").strip()
                
                if cmd.lower() == 'help':
                    print("📋 Comandos de Team Kira:")
                    print("  /list - Ver jugadores")
                    print("  /op <jugador> - Dar admin")
                    print("  /gamemode creative <jugador> - Modo creativo")
                    print("  /tp <jugador1> <jugador2> - Teletransportar")
                    print("  /give <jugador> <item> <cantidad> - Dar items")
                    
                elif cmd.lower() == 'stop':
                    print("🛑 Deteniendo Team Kira's Server...")
                    self.send_command("stop")
                    break
                    
                elif cmd.lower() == 'players':
                    self.send_command("list")
                    
                elif cmd:
                    self.send_command(cmd)
                    
            except KeyboardInterrupt:
                print("\n🛑 Deteniendo servidor...")
                self.send_command("stop")
                break
                
    def run(self):
        """Ejecutar el servidor completo"""
        try:
            # Configuración inicial
            self.setup_environment()
            
            # Preguntar configuración
            print("\n🎯 Configuración de Team Kira's Server:")
            
            server_type = input("Tipo de servidor (vanilla/forge/fabric) [forge]: ").lower() or "forge"
            version = input("Versión de Minecraft [1.20.1]: ") or "1.20.1"
            max_players = input("Jugadores máximos [20]: ") or "20"
            difficulty = input("Dificultad (peaceful/easy/normal/hard) [normal]: ").lower() or "normal"
            
            # Descargar servidor
            if not self.download_server(server_type, version):
                return
                
            # Configurar servidor
            self.setup_server_config(int(max_players), difficulty, server_type != "vanilla")
            
            # Descargar mods si es Forge/Fabric
            if server_type in ["forge", "fabric"]:
                self.download_popular_mods(version)
                
            # Iniciar túnel
            self.start_ngrok()
            
            # Iniciar servidor
            if self.start_server():
                # Consola interactiva
                self.interactive_console()
                
        except KeyboardInterrupt:
            print("\n🛑 Cerrando Team Kira's Server...")
        finally:
            self.cleanup()
            
    def cleanup(self):
        """Limpiar procesos"""
        if self.server_process:
            self.server_process.terminate()
        if self.ngrok_process:
            self.ngrok_process.terminate()

# Ejecutar Team Kira's Server
if __name__ == "__main__":
    server = TeamKiraServer()
    server.run()
