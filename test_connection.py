#!/usr/bin/env python3
"""
Test directo de conexión MCP - Para diagnosticar problemas
"""

import subprocess
import sys
import json
import time

def test_mcp_server():
    """Probar servidor MCP directamente"""
    
    print("🧪 Testing MCP Server Connection")
    print("=" * 50)
    
    # Comando para ejecutar el servidor
    server_cmd = [
        sys.executable,
        "mcp_windows.py"
    ]
    
    print(f"📦 Comando: {' '.join(server_cmd)}")
    print("🚀 Iniciando servidor...")
    
    try:
        # Iniciar servidor
        process = subprocess.Popen(
            server_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
        
        print("✅ Servidor iniciado")
        
        # Mensaje de inicialización
        init_message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "clientInfo": {"name": "test-client", "version": "1.0.0"}
            }
        }
        
        print("📤 Enviando mensaje de inicialización...")
        process.stdin.write(json.dumps(init_message) + "\n")
        process.stdin.flush()
        
        # Leer respuesta
        print("📥 Esperando respuesta...")
        
        # Timeout de 5 segundos
        start_time = time.time()
        response = None
        
        while time.time() - start_time < 5:
            if process.poll() is not None:
                # Proceso terminó
                break
                
            try:
                line = process.stdout.readline()
                if line:
                    print(f"📨 Respuesta recibida: {line.strip()}")
                    response = json.loads(line.strip())
                    break
            except:
                continue
        
        if response:
            print("✅ Servidor respondió correctamente")
            
            # Probar listar herramientas
            print("\n🔧 Probando listar herramientas...")
            list_tools_msg = {
                "jsonrpc": "2.0", 
                "id": 2,
                "method": "tools/list"
            }
            
            process.stdin.write(json.dumps(list_tools_msg) + "\n")
            process.stdin.flush()
            
            # Probar herramienta específica de Windows
            print("\n🧪 Probando herramienta test_conexion...")
            test_tool_msg = {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "test_conexion",
                    "arguments": {}
                }
            }
            
            process.stdin.write(json.dumps(test_tool_msg) + "\n")
            process.stdin.flush()
            
            # Leer respuesta de la herramienta
            start_time = time.time()
            while time.time() - start_time < 3:
                try:
                    line = process.stdout.readline()
                    if line:
                        test_response = json.loads(line.strip())
                        if "result" in test_response:
                            result_content = json.loads(test_response["result"]["content"][0]["text"])
                            print(f"🎯 Test de conexión: {result_content.get('mensaje', 'OK')}")
                        break
                except:
                    continue
            
            print("🎉 ¡Servidor MCP funcionando correctamente!")
            
        else:
            print("❌ No se recibió respuesta del servidor")
            
            # Leer errores
            errors = process.stderr.read()
            if errors:
                print(f"🔍 Errores del servidor:")
                print(errors)
        
        # Terminar proceso
        process.terminate()
        process.wait()
        
    except Exception as e:
        print(f"💥 Error durante la prueba: {e}")
        return False
    
    return True

def check_dependencies():
    """Verificar dependencias"""
    print("\n🔍 Verificando dependencias...")
    
    try:
        import mcp.types
        print("✅ mcp.types - OK")
    except ImportError:
        print("❌ mcp.types - ERROR")
        print("💡 Instala: pip install mcp")
        return False
    
    try:
        from mcp.server import Server
        print("✅ mcp.server - OK")
    except ImportError:
        print("❌ mcp.server - ERROR")
        return False
    
    try:
        from mcp.server.stdio import stdio_server
        print("✅ stdio_server - OK")
    except ImportError:
        print("❌ stdio_server - ERROR")
        return False
    
    return True

def main():
    print("🔧 MCP Connection Tester")
    print("=" * 30)
    
    # Verificar dependencias
    if not check_dependencies():
        print("\n❌ Faltan dependencias. Instala MCP primero.")
        return
    
    # Verificar archivo del servidor
    import os
    if not os.path.exists("mcp_windows.py"):
        print("❌ No encontré mcp_windows.py")
        print("💡 Asegúrate de que esté en el directorio actual")
        return
    
    print("✅ Archivo mcp_windows.py encontrado")
    
    # Probar servidor
    if test_mcp_server():
        print("\n🎉 ¡Todo funciona correctamente!")
        print("💡 Ahora puedes configurar Claude Desktop")
    else:
        print("\n❌ Hay problemas con el servidor")
        print("💡 Revisa los errores arriba")

if __name__ == "__main__":
    main()