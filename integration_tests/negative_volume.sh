curl -s -o /dev/null -w '%{http_code}'  -X POST -F 'image=@app.py' http://127.0.0.1:4555/upload 
