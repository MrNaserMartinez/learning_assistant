# 🎓 Asistente de Aprendizaje

Sistema de estudio gamificado con inteligencia artificial que te ayuda a aprender de forma divertida y efectiva.

## ✨ ¿Qué hace?

- **📚 Crea planes de estudio** personalizados para cualquier tema
- **🎮 Gana puntos y logros** por estudiar consistentemente
- **🤖 Recomendaciones inteligentes** basadas en tus patrones de estudio
- **📊 Seguimiento de progreso** con estadísticas detalladas

## 🚀 Instalación

```bash
# Opción 1: Automática
python setup_rapido.py

# Opción 2: Manual
pip install mcp
python main.py
```

## 💻 Uso Básico

1. **Crear usuario**: Define tu nombre, nivel y temas de interés
2. **Generar plan**: El sistema crea objetivos y recursos automáticamente
3. **Estudiar**: Registra tus sesiones de estudio
4. **Ganar puntos**: Desbloquea logros y sube de nivel

## 🎯 Ejemplo Rápido

```
1. Crear usuario "Ana" → nivel intermedio, interés: Python
2. Generar plan "Python Básico" → 30 días
3. Estudiar 45 minutos → ganar 7 puntos + logro "Maratón"
4. Ver recomendaciones de IA personalizadas
```

## 🏆 Sistema de Logros

| Logro | Condición | Puntos |
|-------|-----------|--------|
| 🌱 Primer Paso | Primera sesión | 10 |
| 🔥 En Racha | 3 días seguidos | 25 |
| ⚡ Imparable | 7 días seguidos | 50 |
| 🏃 Maratón | Sesión +2 horas | 30 |
| 🌅 Madrugador | Estudiar antes 8am | 15 |

## 🤖 Integración con Claude AI

```bash
# Ejecutar servidor MCP
python mcp_windows.py

# Configurar automáticamente
python setup_rapido.py
```

Luego en Claude puedes decir: *"Crea un usuario llamado Juan"* o *"Muestra mi progreso"*

## 📁 Archivos Importantes

- `main.py` - Aplicación principal
- `assistant.py` - Lógica del sistema
- `ia_assistant.py` - Motor de IA
- `mcp_windows.py` - Integración con Claude
- `data/usuarios.json` - Tus datos

## 🔧 Problemas Comunes

**Error de MCP**: `pip install mcp`  
**Datos perdidos**: Elimina `data/usuarios.json`  
**Encoding**: Configura `PYTHONIOENCODING=utf-8`

## 📋 Comandos del Menú

1. Crear usuario
2. Generar plan de estudio  
3. Ver progreso
4. Registrar sesión
5. Ver logros
6. Centro de IA
7. Salir

---

## 👥 Autores

**Desarrollado por:**
- **Naser Martinez**
- **Blanky Lopez**
