Cloud Watch Monitoring Script Installation
=====

# Abstract

Cloud Watch Monitoring Script, which is provided unofficially by AWS, can monitor utilization of memory and cpu, and the following is installation step.

## Installation

1. Make role which can handle Cloud Watch Metric Access
2. Deploy monitoring scripts to EC2
3. Install required packages
4. Make crontab
5. Set alarms on AWS Console or deploy them by Cloud Formation


## Making Role

Cloud Watch Monitoring Script needs a grant which can access Cloud Watch Metric, so that you must make a role which can access EC2 entity and a policy which specifies the following grant.

- cloudwatch:PutMetricData

See `cloudwatchclient.role`.

## Deploying Monitoring Scripts and Clear Cache

Download zip file, which includes the following scripts, from [this site](http://aws.amazon.com/code/8720044071969977), and deploy to the following directories.

| Script                    | Path             |
|:--------------------------|:-----------------|
| mon-get-instance-stats.pl | /usr/local/bin   |
| mon-put-instance-data.pl  | /usr/local/bin   |
| AwsSignatureV4.pm         | /usr/lib64/perl5 |
| CloudWatchClient.pm       | /usr/lib64/perl5 |

Then remove cache files before running the script, excute `rm -rf /var/tmp/aws-mon` as root.


## Installing Packages

Install the following packages by `yum install`.

| Package                 |
|:------------------------|
| perl-Switch             |
| perl-DateTime           |
| perl-Sys-Syslog         |
| perl-LWP-Protocol-https |


## Making crontab

Run from cron.d every 5 minutes. See `crontab`.


## Setting alarms on AWS Console or Deploy them by Cloud Formation

See [Cloud Formation Template](https://github.com/skmt/aws-study/blob/master/aws/cloudformation/ForwardingDNS.yml).


# References

- [AWS Unofficial Site](http://docs.aws.amazon.com/ja_jp/AmazonCloudWatch/latest/DeveloperGuide/mon-scripts.html)
