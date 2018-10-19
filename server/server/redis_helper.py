import redis

class RedisHelper(object):
    def __init__(self, host='127.0.0.1', port=6379):
        print "redis init ", host, port
        self.__conn = redis.Redis(host=host, port=port)
        #self.channel = 'monitor'

    def exists(self, key):
        return self.__conn.exists(key)

    def publish(self, channel, msg):
        self.__conn.publish(channel,msg)
        return True

    def subscribe(self, channel):
        pub = self.__conn.pubsub()
        pub.subscribe(channel)
        pub.parse_response()
        return pub

    def unsubscribe(self, channel):
        self.__conn.ubsubscribe(channel)

    def lpush(self, queue_name, msg):
        self.__conn.lpush(queue_name, msg)

    def brpop(self, queue_name, timeout = 0):
        msg = self.__conn.brpop(queue_name, timeout)
        return msg

    def rpop(self, queue_name):
        return self.__conn.rpop(queue_name)

    def hset(self, name, key, value):
        self.__conn.hset(name, key, value)

    def hget(self, name, key):
        return self.__conn.hget(name, key)

    def sadd(self, key, value):
        self.__conn.sadd(key, value)

    def hgetall(self, key):
        return self.__conn.hgetall(key)

    def smembers(self, key):
        return self.__conn.smembers(key)

    def sismember(self, key, val):
        return self.__conn.sismember(key, val)

    def lpush(self, key, value):
        self.__conn.lpush(key, value)

    def ltrim(self, key, start, end):
        self.__conn.ltrim(key, start, end)

    def delete(self, key):
        self.__conn.delete(key)

