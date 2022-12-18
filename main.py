import uvicorn

# 入口
if __name__ == '__main__':
    uvicorn.run("api.api:app",host='0.0.0.0', port=7000, reload=True, access_log=True)
