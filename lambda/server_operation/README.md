Lambda EC2 Server Operation
=====

# Abstract

Automaticaly start EC2 on Lambda/Node.js or Lambda/Python, which means EC2 itself can't start automaticaly, but Lambda can do that with a few steps, that explains as the following.

## Installation

1. Make role which can handle EC2
2. Deploy script in Lambda
3. Make Cloud Watch Event Schedule


## Making Role

Node.js/Python program needs a grant which can access EC so that you must make a role which specifies the following grant.

- ec2:StartInstances


## Deploying Script

See `start_server.js` or `start_server.py`.


## Making Cloud Watch Event Schedule

## Topics

This installation process and configuration can't deploy by Cloud Formation so far.
