import uvicorn

from fastapi import FastAPI, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from task4 import Analytics
import simplejson as json

app = FastAPI()


def jsonify(response_obj):
    json_compatible_item_data = jsonable_encoder(response_obj)
    return JSONResponse(content=json_compatible_item_data)


def format_response(result):
    if isinstance(result, Exception):
        status_code = 500
        response = {"message": str(result)}
    else:
        status_code = 200
        response = {"data": result}

    return Response(status_code=status_code,
                    content=json.dumps(response),
                    media_type="application/json")


@app.get("/max/{column_name}")
async def read_item(column_name):
    an = Analytics()
    result = an.get_maximum(column=column_name)
    return format_response(result)


@app.get("/min/{column_name}")
async def read_item(column_name):
    an = Analytics()
    result = an.get_minimum(column=column_name)
    return format_response(result)


@app.get("/avg/{column_name}")
async def read_item(column_name):
    an = Analytics()
    result = an.get_average(column=column_name)
    return format_response(result)


@app.get("/most_populated_city/")
async def read_item():
    an = Analytics()
    result = an.get_city_with_most_people()
    return format_response(result)


@app.get("/top_interests/")
async def read_item():
    an = Analytics()
    result = an.get_top_5_interests()
    return format_response(result)


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8090)
