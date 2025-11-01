import uvicorn
from fastapi import FastAPI
from tool.ConfigTool import get_app_config
from api.NllbResource import router as nllb_router
from api.CT2Resource import router as ct_router

# 系统信息
app_config = get_app_config()
app = FastAPI(
    title = app_config.name,
    description = app_config.description,
    version = app_config.version
)

# 挂载接口
app.include_router(nllb_router, prefix = "/api/nllb")
app.include_router(ct_router, prefix = "/api/ct")

# 启动服务
if __name__ == "__main__":
    uvicorn.run(
        app,
        host = app_config.host,
        port = app_config.port
    )
