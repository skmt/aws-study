Lambda EBS Snapshot
=====

# Abstract

Automated snapshot on Lambda/Python, which means EBS snapshot itself can't snapshot automaticaly, but Lambda can do that with a few steps, that explains as the following.

## Installation

1. Make role which can handle EBS and EC2
2. Deploy python script in Lambda
3. Make EC2 Tag
4. Decide its execution schedule


## Making Role

Snapshot program needs grants which can access EC2, EBS and VPC, so that you must make a role which specifies the following grants.

- ec2:DescribeInstances
- ec2:DescribeSnapshots
- ec2:CreateSnapshot
- ec2:DeleteSnapshot
- ec2:CreateNetworkInterface
- ec2:DescribeNetworkInterface
- ec2:DetachNetworkInterface
- ec2:DeleteNetworkInterface
- ec2:StartInstances
- ec2:StopInstances


## Deploying Python Script

See `make_ebs_snapshot.py`


## Making EC2 Tag

Python script can handle only EC2's volumes which includes the following tags.

- Tag

| Key               | Value                           |
|:------------------|:--------------------------------|
| Backup-Type       | Type of Backup (See below)      |
| Backup-Generation | Number of Snapshot's Generation |

- Backup-Type

| Type                    | Action         |
|:------------------------|:---------------|
| Online                  | Online Backup  |
| Offline                 | Offline Backup |
| Other than listed above | Not Backup     |


## Setting Execution Schedule

## Topics

This installation process and configuration can't implement by Cloud Formation so far.
