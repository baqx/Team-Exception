import sys
import os
import uvicorn

# Ensure the backend directory is in python module search path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

if __name__ == "__main__":
    print("=" * 60)
    print(" Starting Chalkka Video Generation FastAPI Backend Server ")
    print(" Serving on http://127.0.0.1:8000")
    print(" API Documentation: http://127.0.0.1:8000/docs")
    print("=" * 60)
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
