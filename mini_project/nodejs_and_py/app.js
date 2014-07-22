var net = require('net');
var fs = require('fs');
var express = require('express');
var router = express.Router();



var call = require('./routes/callpy');

var home = require('./routes/index');



var testSock = '/tmp/entry.sock';

var app = express();

app.listen(8080);
app.use('/', home);
app.use('/callpy', call);


app.disable('etag');



//add url handler to test ip's behavior
//unlink existing test sock or error will be EADDRINUSE
fs.unlink(testSock, function () {
        var server = net.createServer(function(socket){

            //set the global socket
            global.gSock =  socket;

            socket.on('data', function(data) {
                console.log('DATA ' + data);
                //data trim new line
                data =  data.toString().replace(/[\r\n]/g, '');

                socket.write('You said "' + data + '"\n');


                //sample to decode json
                try{
                    data = JSON.parse(data);
                    console.log('data.field is ', data.field);

                }catch(err){
                    console.log('error is ', err);
                }


            });

            socket.on('close', function(data) {
                console.log('CLOSED: ');
            });

        });


    server.listen(testSock, function() { //'listening' listener
        console.log('server bound');
    });
});


