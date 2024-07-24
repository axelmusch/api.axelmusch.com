


def api_response(success:bool,data:dict,code:int):
    return {"success": success, "data":data}, code

def api_auth(token:str):
    ...


if __name__ == '__main__':
    ...