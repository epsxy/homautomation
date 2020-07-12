from fastapi import FastAPI, WebSocket
from rethinkdb import r
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


conn = r.connect('192.168.1.185', 28015).repl()


@app.on_event("startup")
async def startup():
    """Perform startup activities."""
    # If you have any startup activities that need to be defined,
    # define them here.
    # conn = r.connect('192.168.1.185', 28015).repl()


@app.on_event("shutdown")
async def shutdown():
    """Perform shutdown activities."""
    # If you have any shutdown activities that need to be defined,
    # define them here.
    pass


@app.get('/')
def read_root():
    return {'Hello': 'World'}


@app.get('/api/temperatures')
def read_temps():
    cursor = r.db('dashboard').table('temperatures').order_by('timestamp').run(conn)
    res = []
    for doc in cursor:
        res.append(doc)
    return res


@app.get('/api/humidity')
def read_humidity():
    cursor = r.db('dashboard').table('humidity').order_by('timestamp').run(conn)
    res = []
    for doc in cursor:
        print(doc)
        res.append(doc)
    return res


@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f'Message text was: {data}')
