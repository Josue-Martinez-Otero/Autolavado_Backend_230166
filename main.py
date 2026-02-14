from fastapi import FastAPI
from routes.rols import rol

app = FastAPI(
    title="Sistema de Control de autolavado",
    description="Sistema de creación y almacenamiento de información y ventas en un autolavado"
)


@app.include_router(rol)
