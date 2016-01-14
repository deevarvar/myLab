ps aux | grep 'redis-server' | awk '{print $2}' | xargs kill -9
nohup redis-server --port 8989 &
