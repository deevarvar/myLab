var net = require('net');
var fs = require('fs');
var testSock = '/tmp/test.sock';

fs.unlink(testSock, function () {
var server = net.createServer(function(socket){
    socket.write('connected\r\n');

    socket.on('data', function(data) {
        console.log('DATA ' + data);
        //data trim new line
        data =  data.toString().replace(/[\r\n]/g, '');

        socket.write('You said "' + data + '"\n');
        if(data == 'close'){
            console.log('close server');
            //async only when all connections are closed, server will be closed then.
            server.close();
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