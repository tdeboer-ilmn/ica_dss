from datetime import datetime
from datetime import timezone
from enum import Enum
from pprint import pprint, pformat
from json import JSONDecodeError

import collections, copy, base64, logging, logging.handlers, hashlib, os, os.path, sys, time, re, urllib.parse
import textwrap, json, requests, requests.exceptions, pandas

import boto3
import math
from boto3.s3.transfer import TransferConfig
import snowflake.connector

def md5_file(file, chunk_size=8192):
    with open(file, "rb") as f:
        hash_obj = hashlib.md5()
        chunk = f.read(chunk_size)
        while len(chunk) > 0:
            hash_obj.update(chunk)
            chunk = f.read(chunk_size)
    encoded_digest = base64.b64encode(hash_obj.digest())
    return encoded_digest

class BlueBeeException(Exception):
    pass

class APILowLevel:

    def __init__(self, **kwargs):
        '''
        Initializes the APILowLevel with the required fields to connect to the
        platform, these being: the user/api key and the platform url.
        It also sets the project id and bluebase id that will be used by default.

        The precedence is the following (from lowest to highest):
        * config file (specified by environment variable BGP_CONFIG_PATH,
          default /home/bluebee/.bgp/config.json)
        * environment variables (BGP_URL, BGP_USER or BGP_WORKSPACE, BGP_API_KEY ,
          BGP_PROJECT, BGP_BLUEBASE)
        * named arguments with the same name as the environment variables

        BGP_USER is used for normal API, BGP_WORKSPACE is used for BlueBench.
        '''

        # Esthetic, how the environment variables correspond to class local fields
        names = {'BGP_URL':'url', 'BGP_USER':'user', 'BGP_API_KEY':'api_key',
                 'BGP_WORKSPACE':'workspace_id', 'BGP_PROJECT':'project_id',
                 'BGP_BLUEBASE':'bluebase_id'}

        variable_names = ['BGP_URL', 'BGP_USER', 'BGP_API_KEY', 'BGP_WORKSPACE', 'BGP_PROJECT',
                          'BGP_BLUEBASE']
        for attr in variable_names:
            setattr(self, names[attr], None)

        self.config_path = os.getenv("BGP_CONFIG_PATH", "/home/bluebee/.bgp/config.json")
        if os.path.isfile(self.config_path):
            # Set via the config
            with open(self.config_path, 'rt') as f:
                config_content = json.loads(f.read())
                for attr in variable_names:
                    setattr(self, names[attr], config_content[attr] if attr in config_content else None)

        # Set via the environment
        for attr in variable_names:
            setattr(self, names[attr], os.getenv(attr, getattr(self, names[attr])))

        # Set via the kwargs
        for attr in variable_names:
            setattr(self, names[attr], kwargs.get(attr, getattr(self, names[attr])))

        if self.workspace_id is not None:
            if self.api_key is None:
                raise BlueBeeException('API key not specified, check configuration.')
            self.user_identification = base64.b64encode((self.workspace_id+':'+self.api_key).encode())
            self.bluebench = True
            logger.debug(f'Using BlueBench authentication, for workspace {self.workspace_id}.')
        else:
            if self.api_key is None or self.user is None:
                raise BlueBeeException(f'Both API key and user must be specified, current values are: {str(self.api_key)} and {str(self.user)}.')
            self.user_identification = base64.b64encode((self.user+':'+self.api_key).encode())
            self.bluebench = False
            logger.debug(f'Using BlueBee user authentication for user {self.user}.')

        self.formats = None
        self.no_verify = False
        self.token = None

    def authenticate(self):
        headers = {'Accept': 'application/vnd.bluebee.v2+json',
                   'Authorization': 'Basic '.encode() + self.user_identification}
        try:
            if self.bluebench:
                r1 = requests.post(self.url+"/bluebench/"+self.workspace_id+"/login",
                                   headers=headers, verify=(not self.no_verify))
                self.log_curl_command(requests.post, self.url+"/bluebench/"+self.workspace_id+"/login", headers, None, None)
            else:
                r1 = requests.post(self.url+"/user/login", headers=headers, verify=(not self.no_verify))
                self.log_curl_command(requests.post, self.url+"/user/login", headers, None, None)
        except requests.ConnectionError as e:
            logger.info(e)
            raise BlueBeeException(f'can not connect to platform at {self.url}, due to network issues.') from None

        if r1.status_code == 401:
            raise BlueBeeException(f'can not connect to platform at {self.url}, check credentials.')

        if r1.status_code != 200:
            raise BlueBeeException('can not connect to platform at %s, request status is: %d' %
                                   (self.url, r1.status_code))
        try:
            self.token = r1.json()['token']
        except JSONDecodeError:
            raise BlueBeeException('platform answer did not contain token, please check configuration.') from None

    def clean_identifier(self, identifier):
        return re.sub(r'[^\w_\-.]', '_', identifier)

    def get_headers(self):
        if self.token is None:
            self.authenticate()
        headers = {'Accept': 'application/vnd.bluebee.v2+json',
                   'Content-Type': 'application/json',
                   'Authorization': 'Bearer '+self.token}
        return headers

    def log_curl_command(self, http_method, url, headers, params, data):
        if not hasattr(self, 'dump_curl') or not self.dump_curl:
            return
        invocation = 'curl -i '
        invocation += '-H '+' -H '.join(['"'+k+':'+(headers[k].decode("utf-8") if isinstance(headers[k], bytes) else headers[k])+'"' for k in headers.keys()])
        invocation += ' -X ' + http_method.__name__.upper() + ' \"' + url
        invocation += (('?'+urllib.parse.urlencode(params)) if params is not None else '') + '\"'
        invocation += (' -d ' + json.dumps(data)) if data is not None else ''
        logger.debug(invocation)


    def request(self, url, params, httpMethod=requests.get, data=None):

        logger.debug('Request to platform ======================================')
        logger.debug(f'  Method {str(httpMethod)}')
        logger.debug(f'  URL: {self.url+url}')
        logger.debug(f'  Params: {pformat(params, indent=3)}')
        logger.debug(f'  Data: {pformat(data, indent=3)}')

        try:
            r1 = httpMethod(self.url+url, headers=self.get_headers(), params=params, data=data, verify=(not self.no_verify))
        except requests.ConnectionError as e:
            logger.info(e)
            raise BlueBeeException(f'can not connect to platform at {self.url}, due to network issues.') from None

        self.log_curl_command(httpMethod, self.url+url, self.get_headers(), params, data)

        logger.debug(f'  Status code:{r1.status_code}')
        logger.debug(f'  Returned text:{r1.text}')

        # If the session expires we remove the token and try again
        if r1.status_code == 401:
            logger.debug("got unauthorized, removing token and re-authorizing.")
            self.token = None
            r1 = httpMethod(self.url+url, headers=self.get_headers(), params=params, data=data, verify=(not self.no_verify))
        return r1

    def get_project_id(self):
        if self.project_id is not None:
            return self.project_id

        projects = self.project_get()['projects']
        if len(projects) == 1:
            project = projects[0]
            logger.info(f'Using only available project {projects[0]["name"]}', file=sys.stderr)
            return project['id']
        raise Exception('No project id specified and user belongs to multiple projects!')

    def handle_response(self, response, expected_code=None, no_json_parse=False, message=None):
        if response.status_code == requests.codes.ok or response.status_code == requests.codes.created or \
           (expected_code is not None and response.status_code == expected_code):
            return json.loads(response.text) if not no_json_parse else None

        message = None
        try:
            response_json = json.loads(response.text)
            if 'message' in response_json and len(response_json["message"])>0:
                message = response_json["message"]
        except json.JSONDecodeError as exception:
            # There is no error message returned in the JSON message from the
            # server, just show the whole text
            message = response.text

        if message is not None:
            print(message)
        response.raise_for_status()
        return None

    # API related calls
    def activationcode_get(self):
        r1 = self.request("/activationcode", params="")
        return self.handle_response(r1)

    def activationcode_allmatching_put(self, project_id):
        r1 = self.request("/activationcode/allmatching", params={'project':project_id}, httpMethod=requests.put)
        return self.handle_response(r1)

    def activationcode_bestmatching_put(self, pipeline_id, user_reference, inputs, parameters):
        params = {}
        params['userReference'] = user_reference
        params['pipelineIdDto'] = {'id' : str(pipeline_id)}
        params['inputs'] = inputs
        params['tags'] = {'technicalTags':[], 'userTags':[], 'referenceTags':[]}
        params['parameters'] = parameters
        #params['activationCodeDetailIdDto'] = {'id':activation_code_detail}
        r1 = self.request("/activationcode/allmatching", params={'project':self.get_project_id()}, data=json.dumps(params), httpMethod=requests.post)
        return self.handle_response(r1)

    def bdata_put(self, project_id, file_size, original_name, data_format_id=None, parent_id=None, data_type='FILE'):
        # ICA GUI does not seem to display characters with special characters (ex: "name with spaces")
        # and if uploaded via the browser upload will replace special characters with underscore,
        # so we do the same here. At the point of writing this there is no clear confirmation of
        # intended behavior, this was made to mimic GUI behavior, more subtle issue might be present
        # (ex: unicode characters, accented ones, etc.)
        data = {'projectIdDto':{'id':str(project_id)}, 'fileSize':file_size, 'dataType':data_type,
                                'dataFormatIdDto':{}, 'originalName': self.clean_identifier(original_name)}
        if data_format_id is not None:
            data['dataFormatIdDto']['id'] = str(data_format_id)
        if parent_id is not None:
            data['parentDataIdDto'] = {'id':parent_id}
        r1 = self.request("/bdata", params={}, data=json.dumps(data), httpMethod=requests.put)
        return self.handle_response(r1)

    def bdata_post(self, data_id, status):
        r1 = self.request("/bdata/"+data_id, params={}, data=json.dumps({'status':status}), httpMethod=requests.post)
        return self.handle_response(r1)

    def bdata_signedurl_get(self, data_id, hash, return_as_temp_credentials=False):
        params={'hash':hash}
        if return_as_temp_credentials:
            params['returnAsTempCredentials']='true'
        r1 = self.request("/bdata/"+data_id+"/signedUrl", params=params, httpMethod=requests.get)
        return self.handle_response(r1)

    def bluebase_instance_query_saved_get(self, bluebase_id):
        r1 = self.request("/bluebase/instance/"+bluebase_id+"/query/saved", params="")
        return self.handle_response(r1)

    def bluebase_instance_query_post(self, bluebase_id, query):
        r1 = self.request("/bluebase/instance/"+bluebase_id+"/query", params="", data=json.dumps({'query':query}), httpMethod=requests.post)
        return self.handle_response(r1)

    def bluebase_query_get(self, bluebase_id, query_id, start, page_size):
        r1 = self.request("/bluebase/"+bluebase_id+"/query/" + query_id, params={'start':start, 'pageSize':page_size})
        return self.handle_response(r1)

    def connector_get(self):
        r1 = self.request("/connector", params="")
        return self.handle_response(r1)

    def cloudconnector_get(self):
        r1 = self.request("/cloudconnector", params="")
        return self.handle_response(r1)

    def data_download_get(self, data_id=None, local_path=None):
        r1 = self.request("/data/" + data_id + "/download", params="")
        res1 = self.handle_response(r1)
        logger.info(f" Downloading file to {local_path}")
        with requests.get(res1['url'], stream=True) as r:
            r.raise_for_status()
            with open(local_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

    def data_delete(self, data_id):
        r1 = self.request("/data/"+data_id, params={}, httpMethod=requests.delete)
        return self.handle_response(r1, expected_code=requests.codes.no_content, no_json_parse=True,
                                    message='NOTE: failed, please check you have administrator permission!')

    def data_get(self, data_id):
        """ Reduced version, for filter use project_data_get"""
        r1 = self.request("/data/"+data_id, params={})
        return self.handle_response(r1)

    def data_scheduledownload_post(self, data_id, local_path, connector_id=None):
        if connector_id is None:
            connector_id = self.connector_id
        data = {'connectorIdDto':{'id':connector_id}, 'protocol':'SFTP', 'localPath':local_path, 'disableHashing':True}
        r1 = self.request("/data/"+data_id+"/scheduledownload", params="", data=json.dumps(data), httpMethod=requests.post)
        return self.handle_response(r1)

    def data_tag_post(self, data_id, technicalTags=None, userTags=None, connectorTags=None,
                      runInTags=None, runOutTags=None, referenceTags=None):
        ''' Updates the tags.
        If a parameter is None, previous tags will not be replaced. To delete the tags use [].'''
        # pylint: disable=unused-argument,eval-used,exec-used
        update = False
        for t in ['technicalTags', 'userTags', 'connectorTags', 'runInTags', 'runOutTags', 'referenceTags']:
            if eval(t) is None:
                update = True
        if update:
            d = self.data_get(data_id=data_id)['tags']
        data = {}
        for t in ['technicalTags', 'userTags', 'connectorTags', 'runInTags', 'runOutTags', 'referenceTags']:
            if eval(t) is None:
                exec('data["' + t + '"] = d["'+t+'"]')
            else:
                if not isinstance(eval(t), list):
                    raise BlueBeeException('Tag parameter for %s must be a list, is now a %s' % (t, type(eval(t))))
                exec('data["' + t + '"] = ' + t)
        r1 = self.request("/data/"+data_id+"/tag", params="", data=json.dumps(data), httpMethod=requests.post)
        return self.handle_response(r1)

    def dataformat_get(self):
        r1 = self.request("/dataformat", params="")
        return self.handle_response(r1)

    def entitlement_get(self):
        r1 = self.request("/entitlement", params="")
        return self.handle_response(r1)

    def execution_get(self, execution_id=None):
        if execution_id is None:
            r1 = self.request("/execution/", params="")
        else:
            r1 = self.request("/execution/"+execution_id, params="")
        return self.handle_response(r1)

    def pipeline_get(self, pipeline_id=None):
        if pipeline_id is None:
            r1 = self.request("/pipeline/", params="")
        else:
            r1 = self.request("/pipeline/"+pipeline_id, params="")
        return self.handle_response(r1)

    def project_data_delete(self, data_id):
        r1 = self.request("/project/"+self.project_id+"/data/"+data_id, params={}, httpMethod=requests.delete)
        return self.handle_response(r1, expected_code=requests.codes.no_content, no_json_parse=True,
                                    message='NOTE: failed, please check you have administrator permission!')


    def project_data_get(self, status='AVAILABLE', filename=None, filenamematchmode='FUZZY',
                         format=None, type='FILE',
                         connectortag=None, connectortagmatchmode='FUZZY', notinrun=None,
                         runinputtag=None, runinputtagmatchmode='FUZZY',
                         runoutputtag=None, runoutputtagmatchmode='FUZZY',
                         usertag=None, usertagmatchmode='FUZZY',
                         creationdateafter=None, creationdatebefore=None, **kwargs):
        # pylint: disable=unused-argument,eval-used

        statuses = ['ARCHIVED', 'ARCHIVING', 'AVAILABLE', 'CORRUPTED', 'DELETED', 'DELETING',
                    'INCONSISTENT', 'PARTIAL', 'PURGED', 'PURGING',]
        if status is not None and status not in statuses:
            raise BlueBeeException('Status parameter should be one of ' + ','.join(statuses)+' now is '+status)

        types = ['FILE', 'DIRECTORY']
        if type is not None and type not in types:
            raise BlueBeeException('Type parameter should be one of ' + ','.join(types)+' now is '+type)

        params = {}
        for n in ['filename', 'connectortag', 'runinputtag', 'runoutputtag', 'usertag']:
            if eval(n) is not None:
                params[n] = eval(n)
                params[n+'matchmode'] = eval(n+'matchmode')

        for n in ['status', 'notinrun', 'creationdateafter', 'creationdatebefore', 'format', 'type']:
            if eval(n) is not None:
                params[n] = eval(n)

        for n in ['creationdateafter', 'creationdatebefore']:
            if n in params.keys():
                try:
                    datetime.strptime(params[n], '%Y-%m-%dT%H:%M:%S.%f%z')
                except ValueError:
                    raise BlueBeeException('Incorrectly formatted date string, received: %s' % (params[n])) from None

        for item in kwargs.keys():
            if kwargs[item] is not None:
                params[item] = kwargs[item]

        r1 = self.request("/project/"+self.project_id+"/data", params)
        return self.handle_response(r1)

    def project_get(self, project_id=None):
        if project_id is None:
            project_id = ""
        r1 = self.request("/project/"+project_id, params="")
        return self.handle_response(r1)

    def project_pipeline_get(self):
        r1 = self.request("/project/"+self.get_project_id()+"/pipeline", params="")
        return self.handle_response(r1)

    def project_execution_put(self, pipeline_id, user_reference, inputs, parameters, reference_data=None):
        params = {}
        params['userReference'] = user_reference
        params['pipelineIdDto'] = {'id' : str(pipeline_id)}
        params['inputs'] = inputs
        params['tags'] = {'technicalTags':[], 'userTags':[], 'referenceTags':[]}
        params['parameters'] = parameters
        params['activationCodeDetailIdDto'] = {'id': None}
        if reference_data is not None:
            params['referenceDataParameterDto'] = reference_data

        r1 = self.request("/project/"+self.get_project_id()+"/execution", params="", data=json.dumps(params), httpMethod=requests.put)
        return self.handle_response(r1)

    def sample_get(self):
        r1 = self.request("/sample", params="")
        return self.handle_response(r1)

class OnDuplicate(Enum):
    OVERWRITE = 0
    USE_EXISTING = 1
    ERROR = 2

class LocalName(Enum):
    ORIGINAL = 0
    PREFIX_ID = 1

class _DataFormatList(collections.UserList):
    def __init__(self, list_init, high_api=None):
        super(_DataFormatList, self).__init__()
        if isinstance(list_init, dict):
            # Initialize from a json list returned by APILowLevel.project_data_get
            self.data = []
            for f in list_init['formats']:
                self.data.append(DataFormat(f, high_api=high_api))
        elif isinstance(list_init, _DataFormatList):
            # Initialize from another _DataFormatList
            self.data = copy.deepcopy(list_init.data)
        else:
            raise Exception("Unsupported initializer for _DataFormatList")

    def __repr__(self):
        s = ''
        for f in self.data:
            s += str(f) + '\n'
        return s

    def get(self, format):
        for f in self.data:
            if f['code'] == format:
                return f
        raise Exception(f"Data format {format} not found in the list of defined formats.")

class DataFormat(collections.UserDict):
    '''A object representing a data format type available in the BlueBee platform. Can be obtianed using :meth:`APIHighLevel.get_format`

    This object is used when creating a new file object.
    '''

    def __init__(self, dict_init, high_api=None):
        super(DataFormat, self).__init__()
        if isinstance(dict_init, dict):
            self.data = copy.deepcopy(dict_init)
        elif isinstance(dict_init, DataFormat):
            self.data = copy.deepcopy(dict_init.data)
        else:
            raise Exception("Unsupported initializer for DataFormat")

    def __repr__(self):
        s = 'code = ' + self.data['code']
        if self.data['description'] is not None:
            s += ',description = ' + self.data['description']
        return s

class FileList(collections.UserList):
    '''A list of files directories stored on the BlueBee platform.'''

    def __init__(self, list_init, high_api=None):
        super(FileList, self).__init__()
        if isinstance(list_init, dict):
            # Initialize from a json list returned by APILowLevel.project_data_get
            self.data = []
            for f in list_init['data']:
                self.data.append(File(f, high_api=high_api))
        elif isinstance(list_init, FileList):
            # Initialize from another FileList
            self.data = copy.deepcopy(list_init.data)
        elif isinstance(list_init, list):
            # Initialize from a list of File
            self.data = []
            for f in list_init:
                if isinstance(f, File):
                    self.data.append(f)
                else:
                    raise Exception("Unsupported type (%s) for list component used as initializer for FileList" % type(f))
        else:
            raise Exception("Unsupported initializer for FileList")

    def __repr__(self):
        s = ''
        for f in self.data:
            s += str(f) + '\n'
        return s

    def delete(self, wait_timeout=0):
        ''' Deletes all the files in the list.
        '''
        for f in self.data:
            f.delete(wait_timeout=wait_timeout)

    def get(self, destination_directory='.', on_duplicate=OnDuplicate.USE_EXISTING,
            local_name=LocalName.PREFIX_ID, recursive=True):
        ''' Downloads all the files/directories in the list, if necessary.
        '''
        for f in self.data:
            f.get(destination_directory, on_duplicate=on_duplicate, local_name=local_name, recursive=recursive)

    def tag(self, user_tags):
        ''' Tags all the files in the list.
        '''
        for f in self.data:
            f.tag(user_tags)

class File(collections.UserDict):
    '''A file or directory stored on the BlueBee platform. Objects of
    this type are returned by (for example) by :meth:`APIHighLevel.list_project_files`.

    The file/directory can be made available locally (in which case self['local_path']
    will give the path).

    To access all the fields of the object you can use "pprint(o.data)".
    '''

    def __init__(self, dict_init, high_api=None):
        super(File, self).__init__()
        self.children_list = None
        self.high_api = high_api
        if isinstance(dict_init, dict):
            self.data = copy.deepcopy(dict_init)
        elif isinstance(dict_init, File):
            self.data = copy.deepcopy(dict_init.data)
        else:
            raise Exception("Unsupported initializer for File")

    def __repr__(self):
        s = 'id=' + self.data['id']
        s += ', originalName="' + self.data['originalName'] +'"'
        if 'local_path' in self.data:
            s += ', local_path="' + self.data['local_path'] +'"'
        return s

    def list(self):
        ''' For directories returns the list of contents.
        '''
        if self.children_list is None:
            files_low_level = self.high_api.api.project_data_get(parentreference=self.data['reference'], type=None)
            self.children_list = FileList(files_low_level, high_api=self.high_api)
        return self.children_list

    def child(self, child_name):
        ''' For directories, returns the child with the specified name.

        Parameters
        ----------

        child_name: str
          The child name to look for.

        Returns
        -------
          A :class:`.File` or None if no chlild with that name could be found.
        '''
        if not hasattr(self, 'children_list'):
            self.list()
        for f in self.children_list:
            if f.data['originalName'] == child_name:
                return f
        return None

    def delete(self, wait_timeout=0):
        ''' Delete the file from the platform.

        wait_timeout: int, default:0
          If 0 (default) send the command and return immediately.

          If larger than 0 wait for that maximum amount of seconds for file
          to be deleted. If -1 wait until file has been deleted.

        NOTE: you must be a project administrator for this to succeed
        '''

        check_status = bgp.api.project_data_get(status=None, type=self.data['dataType'], reference=self.data['reference'])['data'][0]['status']
        if check_status in ['SCHEDULEDFORDELETE','DELETING','DELETED']:
            return

        self.high_api.api.data_delete(self.data['id'])

        if wait_timeout!=0:
            # We wait for increasing periods, to lower the pressure on the platform API
            wait_time = wait_timeout/(2**8) if wait_timeout>0 else 1
            time_waited = 0
            while time_waited<=wait_timeout or wait_timeout==-1:
                files = self.high_api.api.project_data_get(status=None, dataType=self.data['dataType'], reference=self.data['reference'])
                if files['data'][0]['status']=='DELETED':
                    break
                time.sleep(math.ceil(wait_time))
                if wait_timeout>0:
                    time_waited += wait_time
                    wait_time = wait_time * 2
                else:
                    # We check at most each 256 seconds
                    wait_time = wait_time * 2 if wait_time < 256 else 256

    def get(self, destination_directory='.', on_duplicate=OnDuplicate.USE_EXISTING, local_name=LocalName.PREFIX_ID, recursive=True):
        ''' Makes the files/directories available locally.

        The local name of the file/directory can be automatically prefixed with the file id (to avoid issues
        in case multiple files are named similarly) This behavior can be controlled via the parameter
        local_name.

        In case a local file/directory with the same name is detected, multiple behaviors are available, the
        default is to consider file was already downloaded. For a list see parameter on_duplicate.

        To access the local path of the downloaded file/directory you can use file['local_path']

        Parameters
        ----------

        recursive: bool
          If True and file is a directory, recursive get the contents.
        '''

        if local_name == LocalName.PREFIX_ID:
            local_path = destination_directory + '/' + self.data['id']+'_'+self.data['originalName']
        else:
            local_path = destination_directory + '/' + self.data['originalName']

        if (os.path.isfile(local_path) and self.data['dataType'] == 'FILE') or \
           (os.path.isdir(local_path) and self.data['dataType'] == 'DIRECTORY'):
            if on_duplicate == OnDuplicate.USE_EXISTING:
                self.data['local_path'] = local_path
                logger.info(f"{self.data['originalName']} exists locally as {self.data['local_path']}, skipping download.")
                return
            elif on_duplicate == OnDuplicate.OVERWRITE:
                pass
            elif on_duplicate == OnDuplicate.ERROR:
                raise BlueBeeException(f"Duplicate for {self.data['originalName']} at local path {local_path} and OnDuplicate.ERROR is set")
            else:
                raise BlueBeeException("Unknown OnDuplicate value")

        if self.data['dataType'] == 'FILE':
            self.high_api.api.data_download_get(data_id=self.data['id'], local_path=local_path)

        if self.data['dataType'] == 'DIRECTORY':
            os.makedirs(local_path, exist_ok=True)
            children = self.list()
            if recursive:
                for c in children:
                    c.get(destination_directory=local_path, on_duplicate=on_duplicate, local_name=local_name, recursive=recursive)


        self.data['local_path'] = local_path

    def get_format(self):
        ''' Return the DataFormat for this file.
        '''
        return DataFormat(self.data['format'], high_api=self.high_api)

    def tag(self, user_tags, wait_timeout=0):
        ''' Tags the file with a user tag.

        Any previous user tag will be replaced.

        Parameters
        ----------

        user_tags: [ str, ... ]
          An array of tags (as strings).

        wait_timeout: int, default:0
          If 0 (default) send the command and return immediately.

          If larger than 0 wait for that maximum amount of seconds for the
          execution to finish. If -1, wait until execution finishes.
        '''
        if not isinstance(user_tags, list) or any([not isinstance(x, str) for x in user_tags]):
            raise BlueBeeException('user_tags is not a list of strings')
        self.high_api.api.data_tag_post(data_id=self.data['id'], userTags=user_tags)
        self.data['tags']['userTags'] = user_tags

        # TODO: is this the best choice?
        # The platform will not update immediately the tag. For now we check until we get
        # the correct result
        idx = 0
        while idx < wait_timeout or wait_timeout==-1:
            time.sleep(1)
            fl = FileList(self.high_api.api.project_data_get(reference=self.data['reference']), high_api=self.high_api)
            if len(fl)>0 and sorted(fl[0]['tags']['userTags']) == sorted(self.data['tags']['userTags']):
                break
            idx = idx + 1

class PipelineList(collections.UserList):
    def __init__(self, list_init, high_api=None):
        super(PipelineList, self).__init__()
        self.high_api = high_api
        # First case: list_init is a json list returned by APILowLevel.project_pipeline_get
        if isinstance(list_init, dict):
            self.data = []
            for p in list_init['pipelines']:
                self.data.append(Pipeline(p, high_api=high_api))
        # Second case: another FileList.
        elif isinstance(list_init, PipelineList):
            self.data = copy.deepcopy(list_init.data)
        else:
            raise Exception("Unsupported initializer for PipelineList")

    def __repr__(self):
        s = ''
        for f in self.data:
            s += str(f) + '\n'
        return s

    def find_by_code(self, code):
        '''Finds the pipeline with the corresponding code.

        In case multiple pipelines have the same code, it will return one of them, and
        print a warning to the log.

        Parameters
        ----------
        code: str
          The code (name) of the pipeline to look for.

        Returns
        -------
          A :class:`.Pipeline` or None if no pipeline could be found.
        '''
        lst = [x for x in self.data if x['code'] == code]
        if len(lst) > 0:
            if len(lst) > 1:
                logger.warning(f'Multiple pipelines found with code {code}')
            return lst[0]
        else:
            return None

class Pipeline(collections.UserDict):
    '''A pipeline from the BlueBee platform.

    To access all the fields of the object you can use "pprint(obj.data)".
    '''

    def __init__(self, dict_init, high_api=None):
        super(Pipeline, self).__init__()
        self.high_api = high_api
        if isinstance(dict_init, dict):
            self.data = copy.deepcopy(dict_init)
        elif isinstance(dict_init, Pipeline):
            self.data = copy.deepcopy(dict_init.data)
        else:
            raise Exception("Unsuported initializer for Pipeline")

    def __repr__(self):
        s = 'id = ' + self.data['id']
        s += ', code = "' + self.data['code'] + '"'
        s += ', inputs = "' + str([x['code'] for x in self.data['inputParameters']]) + '"'
        return s

    # TODO: reference_data can be now used to set a reference data, but it is not
    # done nicely, as something like this is required to compute it:
    #
    #   r1 = bgp.api.request(f'/project/9834839/referencedata', params={}, httpMethod=requests.get)
    #   res = bgp.api.handle_response(r1)
    #   reference_data = ['code': 'Reference','referenceDataId':res['referenceSets'][0]['id']]
    #
    def execute(self, user_reference, inputs, parameters=None, reference_data=None, wait_timeout=0):
        ''' Executes a pipeline

        Parameters
        ----------
        user_reference:
          The user reference used for the pipeline. Should contain only underscore
          and alphanumeric characters. If it contains anything else, those
          characters will be replaced by underscores.
        inputs:
          An array of input files in the form {"input_code": file_list} where
          input_code is one of the ones listed when doing print(pipeline) and
          file_list is a list of :class:`.File`.
        parameters:
          An array of parameters of the form {"code": "...", "value": "..."}. The code
          can be determined by going to the "Run" screen on the platform, and check the
          "Settings" box. Each setting name can be used here by replacing the . with __,
          for example "step1.par" becomes step1__par
        wait_timeout: int, default:0
          If 0 (default) send the command and return immediately.

          If larger than 0 wait for that maximum amount of seconds for the
          execution to finish. If -1, wait until execution finishes.

        Returns
        -------
          A :class:`.PipelineExecution`.

        '''
        if parameters is None:
            parameters = {}

        user_reference_clean = re.sub(r'[\W_]', '_', user_reference)
        if user_reference != user_reference_clean:
            logger.warning(f"User reference contained non-alphanumeric characters, converted to {user_reference_clean}")
            user_reference = user_reference_clean

        # The inputs are a JSON of key and File type, but we want it as an array of {'code':..., 'datas':[...]}, so we convert here
        if not isinstance(inputs, dict):
            raise BlueBeeException('inputs parameter must be a dictionary')
        if any([not isinstance(x, File) for z in inputs.values() for x in z]):
            elem_type = next((type(e) for z in inputs.values() for e in z if not isinstance(e, File)))
            raise BlueBeeException('inputs parameter must be a dictionary with values lists of bluebee.File, now one element is %s' % elem_type)
        if not isinstance(parameters, dict):
            raise BlueBeeException('parameters parameter must be a dictionary, it is '+str(type(parameters)))
        converted_inputs = [{'code':k, 'datas':[f.data for f in inputs[k]]} for k in inputs.keys()]
        converted_parameters = [{'code':k, 'value':parameters[k]} for k in parameters.keys()]
        exec = PipelineExecution(self.high_api.api.project_execution_put(self.data['id'], user_reference,
                                                                         converted_inputs, converted_parameters, reference_data), high_api=self.high_api)

        if wait_timeout!=0:
            # Wait 60 seconds at a time, except first time, such that if user asks for
            # 3min 30sec the total time is close to that
            wait_time = wait_timeout % 60
            time_waited = 0
            while time_waited<wait_timeout or wait_timeout==-1:
                status = exec.get_status()
                if status == 'SUCCEEDED' or status == 'FAILED':
                    break
                time.sleep(wait_time)
                if wait_timeout>0:
                    time_waited += wait_time
                wait_time = 60

        return exec

class PipelineExecution(collections.UserDict):
    ''' Represents a pipeline execution in the platform'''

    def __init__(self, dict_init, high_api=None):
        super(PipelineExecution, self).__init__()
        self.high_api = high_api
        if isinstance(dict_init, dict):
            self.data = copy.deepcopy(dict_init)
        elif isinstance(dict_init, PipelineExecution):
            self.data = copy.deepcopy(dict_init.data)
        else:
            raise Exception("Unsupported initializer for PipelineExecution")

    def __repr__(self):
        s = 'id = ' + self.data['id']
        s += ', user_reference = "' + self.data['userReference'] + '"'
        s += ', status = "' + self.data['status'] + '"'
        return s

    def get_status(self):
        ''' Checks the status of the execution with the platform.

        Returns
        -------
        One of "AWAITINGINPUT" or "FAILED" or "FAILEDFINAL" or "INPROGRESS" or "REQUESTED" or "SUCCEEDED"
        '''
        self.data['status'] = self.high_api.api.execution_get(self.data['id'])['status']
        return self.data['status']

    def list_outputs(self):
        ''' Returns the files/directories that the pipeline outputted.

        If you want to make them available locally use :meth:`File.get` function.
        '''
        return FileList([File(x, high_api=self.high_api) for x in self.high_api.api.execution_get(self.data['id'])['outputs']], high_api=self.high_api)

    def find_output(self, output_name_regex):
        ''' Returns the files/directories that the pipeline outputted whos name match the regex.

        If you want to make them available locally use :meth:`File.get` function.
        '''
        # We rely on the fact that the execution get returns all the outputs to
        # avoid useless API calls to the platform
        p = re.compile(output_name_regex)
        results = []
        full_output = self.high_api.api.execution_get(self.data['id'])['outputs']
        for o in full_output:
            if o['dataType'] == 'DIRECTORY':
                full_output.extend(o['children'])
            if  p.match(o['originalName']) is not None:
                results.append(File(o, high_api=self.high_api))
        return FileList(results)

class Project(collections.UserDict):
    ''' Represents a Project in the platform.'''    
    
    def __init__(self, dict_init, high_api=None):
        super(Project, self).__init__()
        self.high_api = high_api
        if isinstance(dict_init, dict):
            self.data = copy.deepcopy(dict_init)
        elif isinstance(dict_init, Project):
            self.data = copy.deepcopy(dict_init.data)
        else:
            raise Exception("Unsupported initializer for Project")

    def __repr__(self):
        s = 'id = ' + self.data['id']
        s += ', name = "' + self.data['name'] + '"'
        return s

    def get_name(self):
        return self.data['name']

class QueryList(collections.UserList):
    '''A list of BlueBase queries saved on the BlueBee platform.'''
    
    def __init__(self, list_init, high_api=None):
        super(QueryList, self).__init__()
        self.high_api = high_api
        # First case: list_init is a json list returned by APILowLevel.bluebase_instance_query_saved_get
        if isinstance(list_init, dict):
            self.data = []
            for q in list_init['savedQueries']:
                self.data.append(Query(q, high_api=high_api))
        # Second case: another QueryList.
        elif isinstance(list_init, QueryList):
            self.data = copy.deepcopy(list_init.data)
        else:
            raise Exception("Unsupported initializer for QueryList")

    def __repr__(self):
        # TODO: reduce to only relevant data
        s = ''
        for f in self.data:
            s += str(f) + '\n'
        return s

    def find_by_id(self, id):
        ''' Finds a Query by id.
        
        Returns
        -------
          Returns the :class:`.Query` or None if no object exists with that id.
        '''
        ret = [x for x in self if x.data['id']==str(id)]
        return ret[0] if len(ret)>0 else None

class Query(collections.UserDict):
    ''' Represents a BlueBase saved query in the platform.'''
    
    def __init__(self, dict_init, high_api=None):
        super(Query, self).__init__()
        self.high_api = high_api
        if isinstance(dict_init, dict):
            self.data = copy.deepcopy(dict_init)
        elif isinstance(dict_init, Query):
            self.data = copy.deepcopy(dict_init.data)
        else:
            raise Exception("Unsuported initializer for Query")

    def __repr__(self):
        s = 'id = ' + self.data['id'] + ', name = ' + self.data['name'] +'\n'
        if 'description' in self.data and self.data['description'] is not None:
            s += '  description = ' + "\n".join(textwrap.wrap(self.data['description'], subsequent_indent='    ')) +'\n'
        if 'query' in self.data:
            s += '  query = ' + "\n".join(textwrap.wrap(self.data['query'], subsequent_indent='    ')) +'\n'
        return s

    def execute(self):
        ''' Returns a :class:`.QueryExecution` object from this Query.'''
        return QueryExecution({'query':self.data['query']}, self.high_api)

class QueryExecution(collections.UserDict):
    ''' Represents a BlueBase query execution in the platform.'''

    def __init__(self, dict_init, high_api):
        super(QueryExecution, self).__init__()
        self.high_api = high_api
        if isinstance(dict_init, dict):
            self.data = copy.deepcopy(dict_init)
        elif isinstance(dict_init, QueryExecution):
            self.data = copy.deepcopy(dict_init.data)
        else:
            raise Exception(f'Unsuported initializer for QueryExecution, expecting dict or QueryExecution, got {type(dict_init)}')

    def wait(self, silent=False):
        ''' (DEPRECATED) Wait for query to finish.'''
        pass

    def get_df_full(self, num_rows=50, silent=True):
        '''Get the full bluebase table as a pandas DataFrame

        Parameters
        ----------
        query:
          The query that should be executed
        num_rows:
          (DEPRECATED) The number of rows per 'page' that should be loaded per request

        '''
        return self.high_api._get_bluebase_connector().cursor().execute(self.data['query']).fetch_pandas_all()

    def get_df(self, start=0, size=50):
        ''' (DEPRECATED) Returns a dataframe corresponding to a set of rows of the query execution.
        
        DEPRECATED: the functionality provided by this function is more efficiently  
                    handled by using LIMIT and OFFSET in the SQL query. This function 
                    will load the full dataframe before returining the requested rows.
                    
        Parameters
        ----------
        start:
          First row to be returned
        size:
          Number of rows to return.

        Returns
        -------
          A :class:`DataFrame`.
        '''
        return self.high_api._get_bluebase_connector().cursor().execute(self.data['query']).fetch_pandas_all().iloc[start:start+size]
        
    def get_status(self):
        ''' (DEPRECATED) Returnes the status of the query.
        
        DEPRECATED: QueryExecution does not execute anymore queries asynchronously,
                    this function always returns 'FINISHED'.

        Returns
        -------
          'FINISHED'
        '''
        return 'FINISHED'

    def __repr__(self):
        return str(self.data)

class APIHighLevel:
    ''' High level methods to access the BlueBee Genomics Platform. '''

    def __init__(self, api):
        self.api = api
        self.formats = None
        self.version = '2021021016'
        print(self.version)

    def _disable_debug(self):
        self.api.dump_curl = False
        logger.setLevel(logging.WARNING)

    def _enable_debug(self, log_file=None):
        ''' E1nable the highes logging level and rests handlers.
        '''
        self.api.dump_curl = True
        logger.setLevel(logging.DEBUG)
        logger.handlers.clear()
        logger.addHandler(logging.StreamHandler())
        if log_file is not None:
            logger.addHandler(logging.handlers.RotatingFileHandler(log_file, maxBytes=(1048576*5), backupCount=7))

    def _get_bluebase_connector(self):

        return snowflake.connector.connect(user=os.environ['BGP_BLUEBASE_USERNAME'] ,password=os.environ['BGP_BLUEBASE_PASSWORD'],
                                           account=os.environ['BGP_SNOWFLAKE_ACCOUNT'],warehouse=os.environ['BGP_SNOWFLAKE_WAREHOUSE'],
                                           database=os.environ['BGP_SNOWFLAKE_DATABASE'],schema='PUBLIC')

    def execute_bluebase_query(self, query, wait=False, page_size=10000, silent=True):
        ''' Execute a BlueBase query

        Returns
        -------
          An object of type :class:`.QueryExecution`.
        '''
        try:
            query_id = self.api.bluebase_instance_query_post(self.api.bluebase_id, query)['id']
            query_execution = QueryExecution({}, high_api=self)
            query_execution.data['id'] = query_id
            query_execution.data['query'] = query
            return query_execution
        except requests.exceptions.HTTPError:
            raise BlueBeeException('An error occured, please check your query syntax!') from None

    def get_format(self, data_format):
        """ Get a data format.

        Parameters
        ----------
        data_format: str
          The string representing the format code. For a list of codes pleae check :meth:`APIHighLevel.print_format_list`

        Returns
        -------
          An object of type :class:`.DataFormat` or throws Exception if no format was found.
        """
        return self._get_format_list().get(data_format)

    def _get_format_list(self):
        if self.formats is None:
            self.formats = _DataFormatList(self.api.dataformat_get())
        return self.formats

    def list_project_files(self, filename=None, status='AVAILABLE', filenamematchmode='FUZZY',
                           format=None, data_type='FILE',
                           connectortag=None, connectortagmatchmode='FUZZY', notinrun=None,
                           runinputtag=None, runinputtagmatchmode='FUZZY',
                           runoutputtag=None, runoutputtagmatchmode='FUZZY',
                           usertag=None, usertagmatchmode='FUZZY',
                           creationdateafter=None, creationdatebefore=None,
                           reference=None, parentreference=None):
        """ Get a list of file information from the BlueBee platform.

        Some descriptipn

        Parameters
        ----------
        status
          The statuses to filter on. Default: "AVAILABLE". (for complete list
          check `Link the platform API reference <https://testplatform.bluebee.com/bgp/apidoc/BlueBee%20Genomics%20Platform%20API%20v2/REST/resource_DataApi.html>`_)
        filename: str or [str, ...]
          The filename(s) to filter on. The filenamematchmode parameter determines how the filtering is done.
        filenamematchmode
          ("EXACT" or "EXCLUDE" or "FUZZY") - How the filenames are filtered. Default: "FUZZY".
        format:
          One or a list of :class:`.DataFormat` objects.
        data_type: str
          To get either files (if type is 'FILE') or directories (if type is 'DIRECTORY')
        creationdateafter: str or datetime.datetime
          Specifies the date that will be used as filter - only file/directory created
          after that date will be returned. In case it is a string, it must have the format:
          "yyyy-MM-ddTHH:mm:ss.SSSZ", where Z is the time zone. An example of the string:
          2001-07-04T12:08:56.235-0700. In case a datetime object without a timezone is used,
          UTC is used by default and a warning is printed.
        creationdatebefore: str or datetime.datetime
          Specifies the date that will be used as filter - only file/directory created
          before that date will be returned. For the format of the string and other
          comments check creationdateafter

        Returns
        -------
          An object of type :class:`.FileList`.
        """

        if isinstance(creationdateafter, datetime):
            if creationdateafter.tzinfo is None:
                logger.warning("creationdateafter provided without time zone information, assuming UTC.")
                creationdateafter = creationdateafter.replace(tzinfo=timezone.utc)
            creationdateafter = "{0:%Y-%m-%dT%H:%M:%S.000%z}".format(creationdateafter)

        if isinstance(creationdatebefore, datetime):
            if creationdatebefore.tzinfo is None:
                logger.warning("creationdatebefore provided without time zone information, assuming UTC.")
                creationdatebefore = creationdatebefore.replace(tzinfo=timezone.utc)
            creationdatebefore = "{0:%Y-%m-%dT%H:%M:%S.000%z}".format(creationdatebefore)

        types = ['FILE', 'DIRECTORY']
        if data_type is not None and data_type not in types:
            raise BlueBeeException('The parameter data_type must be one of ' + ','.join(types)+' now is '+data_type)

        return FileList(self.api.project_data_get(status=status,
          filename=filename, filenamematchmode=filenamematchmode,
          format=(None if format is None else format['id']), type=data_type, notinrun=notinrun,
          connectortag=connectortag, connectortagmatchmode=connectortagmatchmode,
          runinputtag=runinputtag, runinputtagmatchmode=runinputtagmatchmode,
          runoutputtag=runoutputtag, runoutputtagmatchmode=runoutputtagmatchmode,
          usertag=usertag, usertagmatchmode=usertagmatchmode,
          creationdateafter=creationdateafter, creationdatebefore=creationdatebefore,
          reference=reference, parentreference=parentreference), high_api=self)

    def get_current_project(self):
        '''Returns the current project.
        
        Returns
        -------
          An object of type :class:`.Project`.

        '''
        if os.environ['BGP_PROJECT'] is None:
            raise BlueBeeException('No current project set, please contact support!')
        return Project(self.api.project_get(os.environ['BGP_PROJECT']),high_api=self)

    def get_project_files(self, filename=None, destination_directory='.', on_duplicate=OnDuplicate.USE_EXISTING,
                          local_name=LocalName.PREFIX_ID, recursive=True,
                          status='AVAILABLE', filenamematchmode='FUZZY',
                          format=None, data_type='FILE',
                          connectortag=None, connectortagmatchmode='FUZZY', notinrun=None,
                          runinputtag=None, runinputtagmatchmode='FUZZY',
                          runoutputtag=None, runoutputtagmatchmode='FUZZY',
                          usertag=None, usertagmatchmode='FUZZY',
                          creationdateafter=None, creationdatebefore=None,
                          reference=None):
        ''' Make files available locally based on various filters.

        The function creates the destination_directory if it does not exist.

        In case files are found on the file system with the same name as the downloaded file
        or if in the list there are two or more files identically named, the behavior is
        defined by parameter on_duplicate.


        Parameters
        ----------
        on_duplicate
          Possible values: bluebee.OnDuplicate.PREFIX_ID and bluebee.OnDuplicate.ERROR
        format:
          One or a list of :class:`.DataFormat` objects.
        recursive: bool
          If set to True also makes available locally the contents of the object
          (for data_type='DIRECTORY'). When set to False, the information will be
          present in the object returned, but the files will not be available locally.
        other filter parameters
          Check :meth:`APIHighLevel.list_project_files`

        Returns
        -------
          An object of type :class:`.FileList`.

        '''
        os.makedirs(destination_directory, exist_ok=True)
        files = self.list_project_files(status=status,
                                        filename=filename, filenamematchmode=filenamematchmode,
                                        format=format, data_type=data_type, notinrun=notinrun,
                                        connectortag=connectortag, connectortagmatchmode=connectortagmatchmode,
                                        runinputtag=runinputtag, runinputtagmatchmode=runinputtagmatchmode,
                                        runoutputtag=runoutputtag, runoutputtagmatchmode=runoutputtagmatchmode,
                                        usertag=usertag, usertagmatchmode=usertagmatchmode,
                                        creationdateafter=creationdateafter, creationdatebefore=creationdatebefore,
                                        reference=reference)
        files.get(destination_directory=destination_directory, on_duplicate=on_duplicate,
                  local_name=local_name, recursive=recursive)
        return files

    def save_project_file(self, file_path, format=None, recursive=True, parent=None, wait_timeout=0, overwrite=False):
        """Saves a local file or directory to the platform and returns the corresponding :class:`.File` object.

        Parameters
        ----------
        file_path: str
          path of the file or directory to be saved. The file will be uploaded
          to directory denoted by parent parameter (or to root folder if parent
          is None), no matter where it is located locally.
        format
          the data format of the file, as :class:`.DataFormat`
        recursive: bool
          if set to True and file_paths contain directories saves also the contents
        parent: File, default: None
          if set, the file denoted by file_path will be uploaded to the directory
          denoted by parent. parent must be a File object previously returned
          by list_project_files or get_project_files.
        wait_timeout: int, default:0
          file status changes asynchronous at some point after upload finished.
          If wait_timeout is larger than 0 wait for that maximum amount of
          seconds until file has status AVAILABLE. If wait_timeout is
          -1 wait until file has status AVAILABLE.
        overwrite: bool (default: False)
          if True, an existing file with the same name will be overwritten
          (which means will be first deleted and current file will be uploaded)

          WARNING: before upload the file name is standardized by replacing
          various characters with underscore (ex: replacing @ with _). This means
          that from the system perspective two files named locally first@one.txt first_one.txt
          are the same.

        Returns
        -------
        An object of type :class:`.File`
        """

        if format is not None and not isinstance(format, DataFormat):
            raise BlueBeeException('format must be of type DataFormat, now is '+str(type(format)))

        if parent is not None and not isinstance(parent, File):
            raise BlueBeeException('parent must be an object of type File, now is '+str(type(format)))

        if parent is not None and parent.data['dataType']!='DIRECTORY':
            raise BlueBeeException('parent must be a directory, now is '+parent.data['dataType'])

        if os.path.isfile(file_path):
            # See comment on bdata_put on cleaning names for an explanation why we need clean_identifier
            files = bgp.list_project_files(status=None, filename=self.api.clean_identifier(os.path.basename(file_path)),
                                           parentreference=(parent.data['reference'] if parent is not None else None))

            if any([x for x in files if x.data['status']=='PARTIAL']):
                raise Exception(f"Can't save a file with name {file_path}, a file with same name is still uploading.")

            if any([x for x in files if x.data['status']=='AVAILABLE']) and not overwrite:
                raise Exception(f"Can't save a file with name {file_path}, a file with same name already exists. Use overwrite=True to overwrite.")

            if overwrite:
                while True:
                    deleted = False

                    # See comment on bdata_put on cleaning names for an explanation why we need clean_identifier
                    files = bgp.list_project_files(status=None, filename=self.api.clean_identifier(os.path.basename(file_path)),
                                                   parentreference=(parent.data['reference'] if parent is not None else None))
                    files_existing = [x for x in files if x.data['status']!='DELETED']

                    if len(files_existing)==0:
                        # No file in other status than DELETED, our job is done
                        break


                    if not deleted:
                        # Assumption: this is the only place where file is uploaded
                        deleted = True
                        for f in files_existing:
                            f.delete()

                    # Deletes take some time, no need to flood API
                    time.sleep(5)


            file_hash = md5_file(file_path)
            file = File(self.api.bdata_put(self.api.project_id, os.path.getsize(file_path), os.path.basename(file_path),
                                           data_format_id=(format.data['id'] if format is not None else None),
                                           parent_id=(parent.data['id'] if parent is not None else None)), high_api=self)
            url = self.api.bdata_signedurl_get(file.data['id'], hash=file_hash, return_as_temp_credentials=True)

            config = TransferConfig(multipart_threshold=5*(1024 ** 3))
            s3 = boto3.client('s3',
                              aws_access_key_id=url['awsTempCredentials']['accessKey'],
                              aws_secret_access_key=url['awsTempCredentials']['secretKey'],
                              aws_session_token=url['awsTempCredentials']['sessionToken'])
            s3.upload_file(file_path, url['awsTempCredentials']['bucket'], url['awsTempCredentials']['objectPrefix'], Config=config)

            # GDS will signal back to platform and update file status, aynchronous, so wait
            if wait_timeout!=0:
                # We wait for increasing periods, to lower the pressure on the platform API
                wait_time = wait_timeout/(2**8) if wait_timeout>0 else 1
                time_waited = 0
                while time_waited<=wait_timeout or wait_timeout==-1:
                    files = self.api.project_data_get(status=None, reference=file.data['reference'])
                    if 'data' in files and len(files['data'])>0 and files['data'][0]['status']=='AVAILABLE':
                        break
                    time.sleep(math.ceil(wait_time))
                    if wait_timeout>0:
                        time_waited += wait_time
                        wait_time = wait_time * 2
                    else:
                        # We check at most each 256 seconds
                        wait_time = wait_time * 2 if wait_time < 256 else 256

            file.data['local_path'] = file_path
            return file
        if os.path.isdir(file_path):
            if not self.api.bluebench:
                raise BlueBeeException('Uploading directories possible only in a BlueBench workspace. ')

            # TODO: here we should check for all statuses, and accept only if AVAILABLE or DELETED, anything
            # else means another operation is in progress

            files = bgp.list_project_files(status='AVAILABLE', filename=os.path.basename(file_path),
                                           data_type='DIRECTORY',
                                           parentreference=(parent.data['reference'] if parent is not None else None))

            if len(files)>0:
                directory = files[0]
            else:
                directory = File(self.api.bdata_put(self.api.project_id, 0, os.path.basename(file_path),
                                                data_format_id=(format.data['id'] if format is not None else None),
                                                parent_id=(parent.data['id'] if parent is not None else None),
                                                data_type='DIRECTORY'), high_api=self)

            if recursive:
                children = []
                for f in os.listdir(file_path):
                    logger.info(f'Recursively adding {f} to {file_path}')
                    children.append(self.save_project_file(file_path+'/'+f, parent=directory,
                                                           wait_timeout=wait_timeout, overwrite=overwrite))
                directory.children = FileList(children)

            return directory
        raise BlueBeeException('%s is neither a file or directory, aborting' % file_path)

    def save_project_files(self, file_paths, format=None, recursive=True, parent=None, wait_timeout=0, overwrite=False):
        '''Saves a list of local files to the platform and returns the corresponding :class:`.FileList` object.

        Parameters
        ----------
        file_paths: list of str
          paths of the files or directories to be saved. The files will be uploaded
          to directory denoted by parent parameter (or to root folder if parent
          is None), no matter where they are located locally.
        data_format:
          the data format of the file, as :class:`.DataFormat`
        recursive: bool
          if set to True and file_paths contain directories saves also the contents
        parent: File, default: None
          if set, the file denoted by file_path will be uploaded to the directory
          denoted by parent. parent must be a File object previously returned
          by list_project_files or get_project_files.
        wait_timeout: int, default:0
          file status changes asynchronous at some point after upload finished.
          If wait_timeout is larger than 0 wait for that maximum amount of
          seconds until file has status AVAILABLE. If wait_timeout is
          -1 wait until file has status AVAILABLE.
        overwrite: bool (default: False)
          if True, an existing file with the same name will be overwritten
          (which means will be first deleted and current file will be uploaded)

        Returns
        -------
        An object of type :class:`.FileList`.
        '''

        if not isinstance(file_paths, list):
            raise BlueBeeException(f'Parameter file_paths must be a list, is now {type(file_paths)}')
        if any([not isinstance(x, str) for x in file_paths]):
            t = next((x for x in enumerate(file_paths) if not isinstance(x[1], str)))
            raise BlueBeeException(f'Parameter file_paths contains an element ({t[1]}) at position {t[0]} which is not a string but a {type(t[1])}')

        files = FileList([], high_api=self)

        # TODO: sending wait_timeout to each file is inefficient, better is
        # to save all files, then check for all if they are AVAILABLE
        for p in file_paths:
            files.append(self.save_project_file(p, format=format, recursive=recursive, parent=parent, wait_timeout=wait_timeout, overwrite=overwrite))
        return files

    def get_pipelines(self):
        ''' Get the list of pipelines.

        Returns
        -------
        An object of type :class:`.PipelineList`.
        '''
        return PipelineList(self.api.project_pipeline_get(), high_api=self)

    def get_bluebase_queries(self):
        ''' Get a list of saved queries.
        '''
        return QueryList(self.api.bluebase_instance_query_saved_get(self.api.bluebase_id), self)

    def print_format_list(self):
        ''' Prints the available data formats
        '''
        pprint(self._get_format_list())

logger = logging.getLogger(__name__)

bgp = APIHighLevel(APILowLevel())

def _in_notebook():
    try:
        get_ipython()
        return True
    except NameError:
        return False

if _in_notebook():
    logger.setLevel(logging.WARNING)
    logger.handlers.clear()
    logger.addHandler(logging.StreamHandler())

logger.debug(f'BlueBee SDK version {bgp.version}')
