from sanic import Sanic
from sanic.response import json, text

app = Sanic(__name__)


@app.route("/")
async def hello_world(request):
    return json({"hello": "world"})


@app.route('/songs/<song_id:int>')
async def get_download_url(request, song_id):
    return text('Getting download url of song: {}'.format(song_id))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
