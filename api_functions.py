import math

def api_response(success:bool,data:dict,code:int):
    return {"success": success, "data":data}, code

def api_auth(token:str):
    ...

def shannon_entropy(probabilities):
    entropy = 0
    for p in probabilities:
        if p > 0:  # Avoid log(0) which is undefined
            entropy += p * math.log2(1 / p)
    return entropy

if __name__ == '__main__':
    ...