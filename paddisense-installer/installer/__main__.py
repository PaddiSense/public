import uvicorn

uvicorn.run("installer.main:app", host="0.0.0.0", port=8101, log_level="info")
