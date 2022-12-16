import uvicorn

# 入口
if __name__ == '__main__':
    uvicorn.run("api.api:app", port=8000, reload=True, access_log=True)
