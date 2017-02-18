/* Set INSTANCE_ID */
const INSTANCE_ID = 'i-AAAAAAAAAAAAAAAAAA';

var AWS = require('aws-sdk');
AWS.config.region = 'ap-northeast-1';

function start_ec2(cb){
    var ec2 = new AWS.EC2();
    var params = {
        InstanceIds: [ INSTANCE_ID ]
    };

    ec2.startInstances(params, function(err, data) {
        if (!!err) {
            console.log(err, err.stack);
        } else {
            console.log(data);
            cb();
        }
    });
}

exports.handler = function(event, context) {
    console.log('start');
    start_ec2(function() {
        context.done(null, 'Started Instance');
    });
};