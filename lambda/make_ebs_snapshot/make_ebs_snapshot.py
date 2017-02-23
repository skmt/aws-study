import boto3
import collections
import time
import threading
from botocore.client import ClientError
ec2 = boto3.client('ec2', region_name='ap-northeast-1')


def lambda_handler(event, context):
    start_thread()


def start_thread():
    instances = get_instances(['Backup-Type'])
    threads = []

    for i in instances:
        id = i['InstanceId']
        tags = {t['Key']: t['Value'] for t in i['Tags']}
        thname = 'th_' + tags.get('Name', 'None')
        hostname = tags.get('Name', 'None')
        bktype = tags.get('Backup-Type', 'None')
        bkgeneration = int(tags.get('Backup-Generation', 0))

        if bktype != 'Generic' and bktype != 'Online' and bktype != 'Offline' and bktype != 'OfflineAfterShutdown':
            continue

        if bkgeneration < 1:
            continue

        thread = threading.Thread(target=rotate_snapshots, name=thname, args=(i, hostname, bktype, bkgeneration))
        threads.append(thread)
        thread.start()

    for t in threads:
        t.join()


def rotate_snapshots(_instance, _hostname, _type, _generation):
    descriptions = {}

    instance = _instance
    hostname = _hostname
    bktype = _type
    bkgeneration = _generation
    initial_status = _instance['State']['Name']

    if bktype == 'Online' and initial_status != 'running':
        print 'Skipping Online-Snapshot Due To Mismatch Status (%s)<%s>' % (hostname, initial_status)
        return

    if bktype == 'Offline' and initial_status != 'stopped':
        print 'Skipping Offline-Snapshot Due To Mismatch Status (%s)<%s>' % (hostname, initial_status)
        return

    if bktype == 'OfflineAfterShutdown':
        if initial_status == 'running':
            if shutdown_instance(instance) is False:
                print 'Cannot Stop Instance, Exit Immediately (%s)' % hostname
                return

    for b in instance['BlockDeviceMappings']:
        if b.get('Ebs') is None:
            print 'No Snapshot Volume (%s)' % hostname
            return

        volume_id = b['Ebs']['VolumeId']
        description = 'Automatically Snapshotted ' + volume_id + '(' + hostname + ')'

        snapshot = _create_snapshot(volume_id, description)
        print 'Created Snapshot %s(%s)' % (snapshot['SnapshotId'], description)

        descriptions[description] = bkgeneration

    if bktype == 'OfflineAfterShutdown' and initial_status == 'running':
        state = startup_instance(instance)

    delete_old_snapshots(descriptions)


def startup_instance(instance):
    i = boto3.resource('ec2').Instance(instance['InstanceId'])
    i.start()
    i.wait_until_running()
    return True


def shutdown_instance(instance):
    state = instance['State']
    i = boto3.resource('ec2').Instance(instance['InstanceId'])
    if state['Name'] == 'running':
        i.stop()
        i.wait_until_stopped()
        return True
    elif state['Name'] == 'stopped':
        return True
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
    raise Exception('Cannot Create Snapshot ' + description)


def _delete_snapshot(id):
    for i in range(1, 3):
        try:
            return ec2.delete_snapshot(SnapshotId=id)
        except ClientError as e:
            print str(e)
        time.sleep(1)
    raise Exception('Cannot Delete Snapshot ' + id)
