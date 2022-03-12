def bad_request_response():
    return b'HTTP/1.1 400 Bad Request\r\n\r\n'

def not_found_response():
    return b'HTTP/1.1 404 Not Found\r\n\r\n'

def ok_response(content):
    return bytes(f'HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\n\r\n{content}', 'utf-8')
