import uvicorn
from fastapi import FastAPI
from tool.ConfigTool import get_app_config
from api.WordResource import router as translate_router

# 系统信息
app_config = get_app_config()
app = FastAPI(
    title = app_config.name,
    description = app_config.description,
    version = app_config.version
)

# 挂在接口
app.include_router(translate_router)

# 启动服务
if __name__ == "__main__":
    uvicorn.run(
        app,
        host = app_config.host,
        port = app_config.port
    )
