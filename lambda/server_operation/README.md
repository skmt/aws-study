Lambda EC2 Server Operation
=====

# Abstract

Automated start EC2 on Lambda/Node.js, which means EC2 itself can't start automaticaly, but Lambda can do that with a few steps, that explains as the following.

## Installation

1. Make role which can handle EC2
2. Deploy node.js script in Lambda
3. Make Cloud Watch Event Schedule


## Making Role

Node.js program needs a grant which can access EC so that you must make a role which specifies the following grant.

- ec2:StartInstances


## Deploying Node.js Script

See `start_server.js`


## Making Cloud Watch Event Schedule

## Topics

This installation process and configuration can't deploy by Cloud Formation so far.
