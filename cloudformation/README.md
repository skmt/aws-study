# Abstract

This document describes how Cloud Formation deploys network environment and managed services in VPC, including the following components;

- VPC
- Subnet
- Virtual Gateway
- Routing Table
- NAT Gateway
- Route53 Private Hosted Zone
- EC2 and Internal ALB

### Basic Design

- Customer's network address ranges are `10.0.0.0/8` and `192.168.0.0/16`
- VPC's network address range is `172.20.0.0/21`, which includes 8 Class-C CIDR blocks as its subnet.
- Both of sites can connect each other via AWS Direct Connect or VPN Connection
- 8 subnets are separated into two segments, the first one is for public and the another is for private, and both of them are deployed on diffrent AZs
- EC2 in public subnet can connect to the internet but not connect to customer's site(but deploy routing table which includes a path to customer's site), and EC2 in private can connect customer's site and public subnets, not connect to the internet.

### Exception Components

All the list below has to be deployed by munual operation after making the above environment.

- Direct Connect / VPN Connection
- Virtual Interface


# Network Configuration Diagram

<img src="https://github.com/skmt/aws-study/blob/images/images/StackBaseNetwork.svg" width="735" height="490" />
