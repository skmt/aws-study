VMimport 
=====

# Abstract

AWS provides VM import and export feature that imports/exports from/to instances on VMware vSphere, Citrix Xen and Microsoft Hyper-V, and there are three ways to import instance from VMware vSphere, first one is VMimport Service by Snowball, second is AWS Management Portal for vCenter that imports servers by vCenter, and the last one is manual import. This document describes the last one and its topics.

# Importing From VMware vSphere Manually

The following is step to import instance on VMware vSphere.

1. Create root account's Access Key ID and Secret Access Key (Not IAM Account's Keys)
2. Export VM image from VMware vSphere
3. Create S3 Bucket that stores import vm images
4. Create AIM user and its policy
5. Import VM image
6. Create snapshot and AMI (Optionally)

## Creating Root Account's Access Key ID and Secret Access Key (Not IAM Account's Keys)

To upload VM image to S3 Bucket whose owner is root account, create both of keys and download them before the following steps.

## Exporting VM Image From VMware vSphere

There some requirements for VM images before exporting, see [the description](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/PreparingYourVirtualMachine.html). The following is the summary of that.

- Use DHCP on Network Interface (eth0)
- Detach All Of Network Interfaces Except `eth0`
- Activtate SSH Service And Disable iptables service
- Detach CD-ROM and USB if attached

## Creating S3 Bucket That Stores Import VM Images

Create S3 Bucket on specific region, presumably Tokyo Region.

## Creating AIM User And Its Policy

Create AIM user and policy which is attached that user and role, see [the description](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/VMImportPrerequisites.html#vmimport-s3-bucket). The point is that role has to be created by aws cli describes detail in the document.


## Importing VM Image

See [import process](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ImportingYourVM.html) and [command reference](http://docs.aws.amazon.com/AWSEC2/latest/CommandLineReference/ApiReference-cmd-ImportInstance.html). There are two points describing in the followings.

- Set subnet id, which means that not using default VPC and subnet
- Set region

```

#!/bin/sh

# Root Key
export AWS_ACCESS_KEY=SAMPLEKEY1
export AWS_SECRET_KEY=SAMPLEKEY2
# vmimport
export ACCESS_KEY=SAMPLEKEY3
export SECRET_KEY=SAMPLEKEY4

ec2-import-instance export_image.vmdk \
-f vmdk \
-t t2.small \
-a x86_64 \
-b import-bucket-name \
-o ${AWS_ACCESS_KEY} \
-w ${AWS_SECRET_KEY} \
-O ${ACCESS_KEY} \
-W ${SECRET_KEY} \
-p Linux \
--region ap-northeast-1 \
--subnet subnet-id

```

## Creating Snapshot And AMI (Optionally)

After importing instance and before starting it, you shoud create snapshot and AMI.

# Reference

- [Importing and Exporting Virtual Machines](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instances_of_your_vm.html)
- [VM Import/Export in Japanese](https://aws.amazon.com/jp/ec2/vm-import/)
