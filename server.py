import os
from aiohttp import web
import json
import redis

redis_uri = os.environ['REDIS_URI']
redis_port = os.environ['REDIS_PORT']

r = redis.StrictRedis(host=redis_uri, port=redis_port, db=0, decode_responses=True)


async def query(request):
    try:
        if 'post_index' not in request.query:
            response_obj = {'status': 'failed', 'reason': 'Missing required field \'post_index\''}
            return web.Response(text=json.dumps(response_obj), status=400)

        post_index = request.query['post_index']
        probe = r.hget(post_index, 'index')
        if not probe:
            response_obj = {'status': 'failed', 'reason': 'Post index not found'}
            return web.Response(text=json.dumps(response_obj), status=404)

        response_obj = r.hgetall(post_index)

        # return a success json response with status code 200 i.e. 'OK'
        return web.Response(text=json.dumps({'status': 'ok', 'item': response_obj}, ensure_ascii=False), status=200)
    except Exception as e:
        # Bad path where name is not set
        response_obj = {'status': 'failed', 'reason': str(e)}
        # return failed with a status code of 500 i.e. 'Server Error'
        return web.Response(text=json.dumps(response_obj), status=500)

app = web.Application()
app.router.add_get('/api/query', query)
web.run_app(app)
