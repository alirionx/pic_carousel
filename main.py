from imp import reload
from mimetypes import guess_type
import uvicorn

if __name__ == "__main__":
  uvicorn.run("app.api:app", host="0.0.0.0", port=5000, reload=True)

