from fastapi import FastAPI, Depends
from config.security import get_current_user
from routes.routes_rols import rol_router
from routes.routes_user import user
from routes.routes_servicio import servicio
from routes.routes_vehiculos import vehiculo
from routes.routes_usuario_vehiculo_servicio import usuario_vehiculo_servicio
app = FastAPI(
    title="Autolavado Proyecto Académico",
    description="API segura de almacenamiento de informacion para administrar autolavado"
)

app.include_router(rol_router)
app.include_router(user)
app.include_router(vehiculo, dependencies=[Depends(get_current_user)])
app.include_router(servicio, dependencies=[Depends(get_current_user)])
app.include_router(usuario_vehiculo_servicio, dependencies=[Depends(get_current_user)])

