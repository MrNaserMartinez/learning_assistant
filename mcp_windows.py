#!/usr/bin/env python3
"""
MCP Server para Windows - Sin modificar stdout/stderr
"""

import asyncio
import json
import os
import sys

# NO modificar stdout/stderr para Windows - dejar que MCP lo maneje
# Solo configurar variables de entorno
if sys.platform == "win32":
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Importaciones MCP
import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

# Crear servidor
server = Server("learning-assistant")

# Datos simples en memoria
usuarios_data = {}
planes_data = {}
sesiones_data = []

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """Lista de herramientas disponibles"""
    return [
        types.Tool(
            name="crear_usuario",
            description="Crear un nuevo usuario de aprendizaje",
            inputSchema={
                "type": "object",
                "properties": {
                    "nombre": {"type": "string", "description": "Nombre del usuario"},
                    "nivel": {"type": "string", "enum": ["principiante", "intermedio", "avanzado"]},
                    "intereses": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["nombre", "nivel", "intereses"]
            }
        ),
        types.Tool(
            name="crear_plan",
            description="Crear plan de estudio",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "tema": {"type": "string"},
                    "dias": {"type": "integer", "default": 30}
                },
                "required": ["user_id", "tema"]
            }
        ),
        types.Tool(
            name="registrar_sesion",
            description="Registrar sesión de estudio",
            inputSchema={
                "type": "object",
                "properties": {
                    "plan_id": {"type": "string"},
                    "minutos": {"type": "integer"},
                    "satisfaccion": {"type": "number", "minimum": 1, "maximum": 10}
                },
                "required": ["plan_id", "minutos", "satisfaccion"]
            }
        ),
        types.Tool(
            name="ver_progreso",
            description="Ver progreso de usuario",
            inputSchema={
                "type": "object",
                "properties": {"user_id": {"type": "string"}},
                "required": ["user_id"]
            }
        ),
        types.Tool(
            name="listar_usuarios",
            description="Listar todos los usuarios",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="test_conexion",
            description="Probar que el servidor funciona",
            inputSchema={"type": "object", "properties": {}}
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Manejar llamadas a herramientas"""
    
    try:
        resultado = {}
        
        if name == "test_conexion":
            resultado = {
                "exito": True,
                "mensaje": "¡Servidor MCP funcionando perfectamente!",
                "version": "1.0.0",
                "usuarios_registrados": len(usuarios_data),
                "planes_creados": len(planes_data)
            }
            
        elif name == "crear_usuario":
            user_id = f"user_{len(usuarios_data) + 1}"
            usuarios_data[user_id] = {
                "nombre": arguments["nombre"],
                "nivel": arguments["nivel"],
                "intereses": arguments["intereses"],
                "puntos": 0,
                "fecha_registro": "2025-05-30"
            }
            
            resultado = {
                "exito": True,
                "mensaje": f"Usuario '{arguments['nombre']}' creado exitosamente",
                "user_id": user_id,
                "nivel": arguments["nivel"],
                "intereses": arguments["intereses"],
                "puntos_iniciales": 0
            }
            
        elif name == "crear_plan":
            if arguments["user_id"] not in usuarios_data:
                resultado = {
                    "exito": False,
                    "error": f"Usuario {arguments['user_id']} no encontrado"
                }
            else:
                plan_id = f"plan_{len(planes_data) + 1}"
                usuario = usuarios_data[arguments["user_id"]]
                
                # Objetivos básicos según el tema
                objetivos = [
                    f"Aprender fundamentos de {arguments['tema']}",
                    f"Practicar {arguments['tema']} regularmente",
                    f"Completar ejercicios de {arguments['tema']}",
                    f"Crear proyecto con {arguments['tema']}"
                ]
                
                planes_data[plan_id] = {
                    "usuario_id": arguments["user_id"],
                    "tema": arguments["tema"],
                    "objetivos": objetivos,
                    "progreso": 0,
                    "dias_restantes": arguments.get("dias", 30)
                }
                
                # Dar puntos por crear plan
                usuarios_data[arguments["user_id"]]["puntos"] += 5
                
                resultado = {
                    "exito": True,
                    "mensaje": f"Plan de {arguments['tema']} creado para {usuario['nombre']}",
                    "plan_id": plan_id,
                    "objetivos": objetivos,
                    "puntos_ganados": 5,
                    "puntos_totales": usuarios_data[arguments["user_id"]]["puntos"]
                }
        
        elif name == "registrar_sesion":
            if arguments["plan_id"] not in planes_data:
                resultado = {
                    "exito": False,
                    "error": f"Plan {arguments['plan_id']} no encontrado"
                }
            else:
                plan = planes_data[arguments["plan_id"]]
                user_id = plan["usuario_id"]
                
                # Calcular progreso (simplificado)
                incremento = min(15, max(5, arguments["minutos"] // 10))
                progreso_anterior = plan["progreso"]
                nuevo_progreso = min(100, progreso_anterior + incremento)
                
                # Actualizar progreso
                planes_data[arguments["plan_id"]]["progreso"] = nuevo_progreso
                
                # Calcular puntos
                puntos_ganados = max(1, arguments["minutos"] // 10)
                if arguments["satisfaccion"] >= 8:
                    puntos_ganados += 3
                
                usuarios_data[user_id]["puntos"] += puntos_ganados
                
                # Registrar sesión
                sesion = {
                    "plan_id": arguments["plan_id"],
                    "minutos": arguments["minutos"],
                    "satisfaccion": arguments["satisfaccion"],
                    "fecha": "2025-05-30"
                }
                sesiones_data.append(sesion)
                
                resultado = {
                    "exito": True,
                    "mensaje": "¡Sesión registrada exitosamente!",
                    "progreso_anterior": progreso_anterior,
                    "progreso_nuevo": nuevo_progreso,
                    "incremento": incremento,
                    "puntos_ganados": puntos_ganados,
                    "puntos_totales": usuarios_data[user_id]["puntos"],
                    "tema": plan["tema"]
                }
        
        elif name == "ver_progreso":
            if arguments["user_id"] not in usuarios_data:
                resultado = {
                    "exito": False,
                    "error": f"Usuario {arguments['user_id']} no encontrado"
                }
            else:
                usuario = usuarios_data[arguments["user_id"]]
                
                # Buscar planes del usuario
                planes_usuario = {k: v for k, v in planes_data.items() 
                                if v["usuario_id"] == arguments["user_id"]}
                
                # Buscar sesiones del usuario
                sesiones_usuario = [s for s in sesiones_data 
                                  if planes_data.get(s["plan_id"], {}).get("usuario_id") == arguments["user_id"]]
                
                tiempo_total = sum(s["minutos"] for s in sesiones_usuario)
                
                resultado = {
                    "exito": True,
                    "usuario": usuario["nombre"],
                    "nivel": usuario["nivel"],
                    "intereses": usuario["intereses"],
                    "puntos": usuario["puntos"],
                    "planes_activos": len(planes_usuario),
                    "sesiones_completadas": len(sesiones_usuario),
                    "tiempo_total_minutos": tiempo_total,
                    "planes": [
                        {
                            "id": k,
                            "tema": v["tema"],
                            "progreso": v["progreso"]
                        }
                        for k, v in planes_usuario.items()
                    ]
                }
        
        elif name == "listar_usuarios":
            usuarios_lista = []
            for user_id, datos in usuarios_data.items():
                planes_count = sum(1 for p in planes_data.values() if p["usuario_id"] == user_id)
                usuarios_lista.append({
                    "id": user_id,
                    "nombre": datos["nombre"],
                    "nivel": datos["nivel"],
                    "puntos": datos["puntos"],
                    "planes": planes_count
                })
            
            resultado = {
                "exito": True,
                "total_usuarios": len(usuarios_data),
                "usuarios": usuarios_lista
            }
        
        else:
            resultado = {
                "exito": False,
                "error": f"Herramienta '{name}' no reconocida"
            }
        
        # Retornar como TextContent
        return [types.TextContent(
            type="text",
            text=json.dumps(resultado, indent=2, ensure_ascii=False)
        )]
        
    except Exception as e:
        # Manejo de errores
        error_response = {
            "exito": False,
            "error": str(e),
            "herramienta": name,
            "argumentos": arguments
        }
        
        return [types.TextContent(
            type="text",
            text=json.dumps(error_response, indent=2, ensure_ascii=False)
        )]

async def main():
    """Función principal - sin prints que causen problemas"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())