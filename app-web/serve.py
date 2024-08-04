from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def get_index():
    return {'message': 'It works!'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)