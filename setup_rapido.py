#!/usr/bin/env python3
"""
Setup Rápido MCP - Solo lo esencial en 2 minutos
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def main():
    print("🚀 Setup MCP Rápido - 2 minutos")
    print("=" * 40)
    
    # 1. Instalar MCP
    print("📦 Instalando MCP...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "mcp"], check=True, capture_output=True)
        print("✅ MCP instalado")
    except:
        print("❌ Error instalando MCP")
        print("💡 Ejecuta manualmente: pip install mcp")
        return
    
    # 2. Verificar archivos necesarios
    print("📁 Verificando archivos...")
    required = ["assistant.py", "ia_assistant.py"]
    missing = [f for f in required if not os.path.exists(f)]
    
    if missing:
        print(f"❌ Faltan archivos: {missing}")
        return
    
    print("✅ Archivos OK")
    
    # 3. Configurar Claude Desktop (opcional)
    print("🤖 ¿Configurar Claude Desktop? (s/n): ", end="")
    if input().lower().startswith('s'):
        setup_claude()
    
    # 4. Probar servidor
    print("🧪 ¿Probar servidor ahora? (s/n): ", end="")
    if input().lower().startswith('s'):
        print("🚀 Ejecutando: python mcp_windows.py")
        print("💡 Ctrl+C para detener")
        try:
            subprocess.run([sys.executable, "mcp_windows.py"])
        except KeyboardInterrupt:
            print("\n✅ Servidor detenido")
    
    print("\n🎉 ¡Setup completado!")
    print("📋 Próximos pasos:")
    print("1. python mcp_windows.py  # Ejecutar servidor")
    print("2. Configurar Claude Desktop si no lo hiciste")
    print("3. Probar con Claude: 'Crea un usuario llamado Ana'")

def setup_claude():
    """Configurar Claude Desktop"""
    import platform
    
    system = platform.system()
    if system == "Darwin":  # macOS
        config_path = Path.home() / "Library/Application Support/Claude/claude_desktop_config.json"
    elif system == "Windows": 
        config_path = Path.home() / "AppData/Roaming/Claude/claude_desktop_config.json"
    else:  # Linux
        config_path = Path.home() / ".config/claude/claude_desktop_config.json"
    
    # Crear directorio
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configuración
    current_dir = os.path.abspath(".")
    server_path = os.path.join(current_dir, "mcp_windows.py")
    
    config = {
        "mcpServers": {
            "learning": {
                "command": "python",
                "args": [server_path],
                "env": {"PYTHONPATH": current_dir}
            }
        }
    }
    
    # Leer config existente
    existing = {}
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                existing = json.load(f)
        except:
            pass
    
    # Fusionar
    if "mcpServers" not in existing:
        existing["mcpServers"] = {}
    existing["mcpServers"]["learning"] = config["mcpServers"]["learning"]
    
    # Escribir
    with open(config_path, 'w') as f:
        json.dump(existing, f, indent=2)
    
    print(f"✅ Claude Desktop configurado")
    print(f"📁 Archivo: {config_path}")
    print("🔄 Reinicia Claude Desktop")


if __name__ == "__main__":
    main()