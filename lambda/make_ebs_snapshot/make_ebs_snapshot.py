import boto3
import collections
import time
import threading
from botocore.client import ClientError
ec2 = boto3.client('ec2', region_name='ap-northeast-1')


def lambda_handler(event, context):
    start_thread()


def start_thread():
    instances = get_instances(['Backup-Generation'])

    for i in instances:
        thname = 'th_' + tags.get('Name', 'None')
        bktype = tags.get('Backup-Type', 'None')
        bkgeneration = int(tags.get('Backup-Generation', 0))

        if bktype != 'Online' and bktype != 'Offline':
            continue

        if bkgeneration < 1:
            continue

        thread = threading.Thread(target=rotate_snapshots, name=thname, args=(i))
        thread.start()


def rotate_snapshots(instance):
    descriptions = {}

    tags = {t['Key']: t['Value'] for t in instance['Tags']}
    hostname = tags.get('Name', 'None')
    bktype = tags.get('Backup-Type', 'None')
    bkgeneration = int(tags.get('Backup-Generation', 0))
    shutdown_status = False

    if bktype == 'Offline':
        shutdown_status = shutdown_instance(instance)
        if shutdown_status is False:
            print 'Can not stop instance (%s)' % hostname
            return
        print 'Stopped instance %s(%s)' % (hostname, instance.id)

    for b in instance['BlockDeviceMappings']:
        if b.get('Ebs') is None:
            print 'No snapshot volume (%s)' % hostname
            return

        volume_id = b['Ebs']['VolumeId']
        description = 'Automatically Snapshotted by Lambda EBS_Snapshot Script ' + volume_id + '(' + hostname + ')'

        snapshot = _create_snapshot(volume_id, description)
        print 'Create snapshot %s(%s)' % (snapshot['SnapshotId'], description)

        descriptions[description] = bkgeneration

    if bktype == 'Offline' and shutdown_status is True:
        state = startup_instance(instance)
        print 'Starting instance %s(%s)[%s]' % (hostname, instance.id, state['Name'])

    delete_old_snapshots(descriptions)


def startup_instance(instance):
    state = instance.start()
    return state


def shutdown_instance(instance):
    if instance.state['Name'] != 'stopped':
        instance.stop()
        for retry in range(1, 6):
            if instance.state['Name'] == 'stopped':
                return True
            time.sleep 10
    return False


def get_instances(tag_names):
    reservations = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag-key',
                'Values': tag_names
            }
        ]
    )['Reservations']

    return sum([
        [i for i in r['Instances']]
        for r in reservations
    ], [])


def delete_old_snapshots(descriptions):
    snapshots_descriptions = get_snapshots_descriptions(descriptions.keys())

    for description, snapshots in snapshots_descriptions.items():
        delete_count = len(snapshots) - descriptions[description]

        if delete_count <= 0:
            continue

        snapshots.sort(key=lambda x: x['StartTime'])

        old_snapshots = snapshots[0:delete_count]

        for s in old_snapshots:
            _delete_snapshot(s['SnapshotId'])
            print 'delete snapshot %s(%s)' % (s['SnapshotId'], s['Description'])


def get_snapshots_descriptions(descriptions):
    snapshots = ec2.describe_snapshots(
        Filters=[
            {
                'Name': 'description',
                'Values': descriptions,
            }
        ]
    )['Snapshots']

    groups = collections.defaultdict(lambda: [])
    {groups[s['Description']].append(s) for s in snapshots}

    return groups


def _create_snapshot(id, description):
    for i in range(1, 3):
        try:
            return ec2.create_snapshot(VolumeId=id, Description=description)
        except ClientError as e:
            print str(e)
        time.sleep(1)
    raise Exception('cannot create snapshot ' + description)


def _delete_snapshot(id):
    for i in range(1, 3):
        try:
            return ec2.delete_snapshot(SnapshotId=id)
        except ClientError as e:
            print str(e)
        time.sleep(1)
    raise Exception('cannot delete snapshot ' + id)
