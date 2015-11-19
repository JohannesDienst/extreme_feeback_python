# setup gpio


from bottle import route, request, run

@route('/build')
def status():
    module = request.query.module
    status = request.query.status
    return str(module) + " " + str(status)

run(host='localhost', port=7073, reloader=True,  debug=True)
