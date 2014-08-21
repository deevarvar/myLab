/**
 * Created by deevarvar on 14-7-22.
 */


var express = require('express');
var router = express.Router();

router.get(/\/(.*)/, function(req, res) {


    var msg = {
        "path":req.path.substring(1),
        "exit": "True"
    };

    console.log('path is ', JSON.stringify(msg));
    //encode
    global.gSock.write(JSON.stringify(msg));

    res.send(msg,200);

});


module.exports = router;