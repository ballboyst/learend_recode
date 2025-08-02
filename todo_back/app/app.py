import pymysql, json
from crud import create_task
from wsgiref.simple_server import make_server


def application(environ, start_response):
    path = environ.get('PATH_INFO','/')
    method = environ.get('REQUEST_METHOD', 'GET')


    if path == '/' and method == 'GET':
        status = '200 OK'
        headers = [('Content-Type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        return [b'Hello, this is a simple WSGI API!']
    
    elif path == '/api/data' and method == 'GET':
        data = {"message": "This is some data from th API."}
        status = '200 OK'
        headers = [('Content-Type', 'application/json; charset=utf-8')]
        start_response(status, headers)
        return [json.dumps(data).encode('utf-8')]
    
    elif path == path =='api/echo' and method == 'POST':
        try:
            try:
                request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            except(ValueError):
                request_body_size = 0

            request_body_size = environ['wsgi.input'].read(request_body_size)
            receive_json = json.loads(request_body.decode('utf-8'))


            # key, valueを分離
            keys = list(task_json.keys())
            values = [receive_json[k] for k in keys]

            # crud.pyのcrud_taskを呼ぶ
            create_task(keys, values)
            
            response = {
                "received": received_json
            }
            status = '200 OK'
            headers = [('Content-Type', 'application/json; charset=utf-8')]
            start_response(status, headers)
            return [json.dumps(response).encode('utf-8')]
        
        except Exception as e:
            status = '400 Bad Request'
            headers = [('Content-Type', 'text/plain; charset=utf-8')]
            start_response(status, headers)
            return [f"Error parsing JSON:{e}".encode('utf-8')]
    
    else:
        status = '404 Not Found'
        headers = [('Content-Type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        return [b'404 Not Found']
        
if __name__ == '__main__':
    port = 8000
    with make_server('', port, application) as httpd:
        print(f"Seving on port {port}...")
        httpd.serve_forever()
