import httplib2, os, mimetypes, sys, argparse
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient.discovery import build
mimetypes.add_type('video/mp4', '.hevc')
mimetypes.add_type('application/*', '')
mimetypes.add_type('video/mp4', '.mkv')
scopes = 'https://www.googleapis.com/auth/drive'

def generate_credentials():
    application_name = 'Drive Upload'
    client_secret_file = '/data/openpilot/selfdrive/loggerd/client_secret.json'
    credential_path = '/data/openpilot/selfdrive/loggerd/cred'
    store = Storage(credential_path)
    flow = client.flow_from_clientsecrets(client_secret_file, scopes)
    flow.user_agent = application_name
    args = argparse.Namespace()
    args.auth_host_name = 'localhost'
    args.auth_host_port = [8080, 8090]
    args.logging_level = 'ERROR'
    args.noauth_local_webserver = 'TRUE'
    flags = args
    tools.run_flow(flow, store, flags)


def get_credentials():
    credential_path = '/data/openpilot/selfdrive/loggerd/cred'
    store = Storage(credential_path)
    credentials = store.get()
    return credentials


def get_service():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = build('drive', 'v3', http=http)
    return service


def google_drive_upload(video):
    try:
        service = get_service()
        parent = os.path.split(os.path.dirname(video))[1]
        child = os.path.basename(os.path.normpath(os.path.splitext(video)[0]))
        body = {'name': '%s_%s' % (parent, child)}
        if 'rlog' in child:
            body['parents'] = [
             '12Np2k6NnvV3eOT5uBe40FEHsTFiBP005']
        else:
            if 'fcamera' in child:
                body['parents'] = [
                 '1-ds2HZ4OrFbzCwQ4bWT8ivSOh0xztBAD']
            else:
                if 'dcamera' in child:
                    body['parents'] = [
                     '1C4URo3i1ARMTqE_lZdoy1oqAUZMq1yGg']
                else:
                    if 'prcamera' in child:
                        body['parents'] = [
                         '1vSFDZGNZJkIBJyfN6W62LfA9ir3AEc4n']
                    else:
                        body['parents'] = [
                         '1Nu_ztnKsAvDE0DZvxdvJGcwkJ_7IXM6X']
        results = service.files().create(body=body, media_body=video).execute()
        return results
    except:
        return False

