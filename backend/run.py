from src.config import Config
from src.main import app
import asyncio


print(Config.DATABASE_URL)

# if __name__ == "__main__":
#     app = asyncio.run(main=create_app(config=Config))
#     uvicorn.run(app=app, host="0.0.0.0", port=8000, reload=True)
    
    