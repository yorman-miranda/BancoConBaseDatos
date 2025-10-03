"""
Sistema Bancario - API REST con FastAPI
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Importar todas las APIs
from apis import (
    auth,
    usuarios,
    clientes,
    cuentas,
    empleados,
    sucursales,
    transacciones,
    operaciones,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Iniciando Sistema Bancario API...")
    print("📊 Configurando base de datos...")

    # Aquí podrías inicializar datos por defecto si es necesario
    from database.config import create_tables

    create_tables()

    print("✅ Sistema listo para usar.")
    print("📚 Documentación disponible en: http://localhost:8000/docs")
    yield
    # Shutdown
    print("👋 Cerrando Sistema Bancario API...")


# Crear la aplicación FastAPI con lifespan
app = FastAPI(
    title="Sistema Bancario API",
    description="API REST para gestión completa de un sistema bancario",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir todos los routers
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(clientes.router)
app.include_router(cuentas.router)
app.include_router(empleados.router)
app.include_router(sucursales.router)
app.include_router(transacciones.router)
app.include_router(operaciones.router)


@app.get("/", tags=["raíz"])
async def root():
    return {
        "mensaje": "Bienvenido al Sistema Bancario API",
        "version": "1.0.0",
        "documentacion": "/docs",
        "endpoints": {
            "autenticacion": "/auth",
            "usuarios": "/usuarios",
            "clientes": "/clientes",
            "cuentas": "/cuentas",
            "empleados": "/empleados",
            "sucursales": "/sucursales",
            "transacciones": "/transacciones",
            "operaciones": "/operaciones",
        },
    }


@app.get("/health", tags=["salud"])
async def health_check():
    return {"status": "healthy", "service": "Sistema Bancario API"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
