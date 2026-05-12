from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routes import auth_routes, document_routes, convert_routes, isl_routes, tts_routes , history_routes,profile_routes
from app.routes import profile_routes


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ISL Backend API",
    description="Indian Sign Language Conversion Backend",
    version="1.0.0"
)

# CORS for frontend
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth_routes.router)
app.include_router(document_routes.router)
app.include_router(convert_routes.router)
app.include_router(isl_routes.router)
app.include_router(tts_routes.router)
app.include_router(history_routes.router)
app.include_router(profile_routes.router)



# Health Check Route
@app.get("/")
def home():
    return {"message": "ISL Backend Running Successfully 🚀"}
