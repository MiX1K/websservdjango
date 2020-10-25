def app(environ, start_response):
    # бизнес-логика
    status = '200 OK'
    headers = [('Content-Type', 'text/plain')]
    body = environ['QUERY_STRING']
    body = '\n'.join(body.split('&')).encode('utf-8')
    start_response(status, headers )
    return iter([body])