
def api_response(success:bool,data:dict,code:int):
    return {"success": success, "data":data}, code


if __name__ == '__main__':
    ...