const WebSocket = require('ws');
const redis = require('redis');

const REDIS_HOST = 'redis';
const REDIS_PORT = 6379;
const WEB_SOCKET_PORT = 3000;
const CHANNEL_NAME = 'update.notifications';

// Connect to Redis and subscribe to channel.
console.log(`Connect to Redis and subscribe to ${CHANNEL_NAME} channel`)
const redisClientSub = redis.createClient(REDIS_PORT, REDIS_HOST, {no_ready_check: true});
const redisClientPub = redis.createClient(REDIS_PORT, REDIS_HOST, {no_ready_check: true});
redisClientSub.subscribe(CHANNEL_NAME);

// Create & Start the WebSocket server.
console.log("Create & Start the WebSocket server")
const wss = new WebSocket.Server({port: WEB_SOCKET_PORT});

// Register event for client connection
console.log("Register event for client WSS connection")
wss.on("connection", ws => {
    ws.on("message", message => {
        redisClientPub.publish(CHANNEL_NAME, message)
    });

    redisClientSub.on("message", (channel, subMessage) => {
        console.log(`Receive subMessage => ${subMessage}`);
        console.log(`Subscriber received subMessage in channel => ${channel} : ${subMessage}`);
        ws.send(subMessage);
    })

    ws.send("Hi!")
})

console.log(`WebSocket server started at ws://localhost: ${WEB_SOCKET_PORT}`);
