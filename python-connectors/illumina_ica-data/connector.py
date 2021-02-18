# This file is the actual code for the custom Python dataset illumina_ica-data

# import the base class for the custom dataset
from six.moves import xrange
from dataiku.connector import Connector
import os, datetime
from illumina.ica_client.rest import ApiException
import illumina.ica_client as ica

"""
A custom Python dataset is a subclass of Connector.

The parameters it expects and some flags to control its handling by DSS are
specified in the connector.json file.

Note: the name of the class itself is not relevant.
"""
class MyConnector(Connector):

    def __init__(self, config, plugin_config):
        """
        The configuration parameters set up by the user in the settings tab of the
        dataset are passed as a json object 'config' to the constructor.
        The static configuration parameters set up by the developer in the optional
        file settings.json at the root of the plugin directory are passed as a json
        object 'plugin_config' to the constructor
        """
        Connector.__init__(self, config, plugin_config)  # pass the parameters to the base class
        
        ####
        # Set Local Variables needed for bluebee.py - Bit of a HACK
        #
        # These are examples of the local variables we have access to in ICA
        self.vars = {
            "BGP_NODEINSTANCE": "300281",
            "BGP_BLUEBASE": "204164",
            "BGP_SNOWFLAKE_DATABASE": "tool_development_4003",
            "BGP_NOTEBOOK": "300281",
            "BGP_NAMESPACE": "tst-aws-ilmn-integration-w300281",
            "BGP_API_KEY": "935ec01e-87fd-47c0-a636-be1696c2136f",
            "BGP_URL": "https://ilmnplatform.bluebee.com/ica/rest/api",
            "BGP_WORKSPACE": "300281",
            "BGP_BLUEBASE_PASSWORD": "ec6f9e23-f4be-4bf3-b05c-a4dfd1b7c978",
            "BGP_PROJECT": "204155",
            "BGP_SNOWFLAKE_ACCOUNT": "iapdev.us-east-1",
            "BGP_SNOWFLAKE_WAREHOUSE": "TOOL_DEVELOPMENT_4003_QUERY",
            "BGP_TYPE": "component",
            "BGP_BLUEBASE_USERNAME": "bb_204164_c",
            "server": "https://use1.platform.illumina.com",
            "domain": "emergingsolutions"
        }
        
        #Make all the variables environment variables, since bluebee.py API needs them as environment variables
        for k,v in self.vars.items():
            os.environ[k] = v
        
        #Now import the library
        import illumina.bluebee
        from illumina.bluebee import bgp
        self.bgp = bgp

        self.method = self.config.get("method")
        
        #Setup authentication in case we are using ICA
        if self.method == 'ica':
            self.conf = ica.Configuration()
            self.conf.debug = False
            ica_client = ica.ApiClient(self.conf)
            tokens_api = ica.TokensApi(ica_client)
            
            # perform some more initialization
            self.conf.server = self.config.get("server")
            self.useToken = self.config.get("useToken")
            self.conf.username = self.config.get("username")
            self.conf.password = self.config.get("password")
            self.token = self.config.get("token")
            self.domain = self.config.get("domain")
            
            conf.api_key['Authorization'] = conf.get_basic_auth_token()
            
            token = tokens_api.create_token(domain=self.domain)
            conf.api_key['Authorization'] = token.access_token
            conf.api_key_prefix['Authorization'] = token.token_type
            
            
    def get_read_schema(self):
        """
        Returns the schema that this connector generates when returning rows.

        The returned schema may be None if the schema is not known in advance.
        In that case, the dataset schema will be infered from the first rows.

        If you do provide a schema here, all columns defined in the schema
        will always be present in the output (with None value),
        even if you don't provide a value in generate_rows

        The schema must be a dict, with a single key: "columns", containing an array of
        {'name':name, 'type' : type}.

        Example:
            return {"columns" : [ {"name": "col1", "type" : "string"}, {"name" :"col2", "type" : "float"}]}

        Supported types are: string, int, bigint, float, double, date, boolean
        """

        # In this example, we don't specify a schema here, so DSS will infer the schema
        # from the columns actually returned by the generate_rows method
        return {
            "columns" : [
                {"name": "ID", "type" : "bigint"},
                {"name": "Name", "type" : "string"},
                {"name" :"Format", "type" : "string"},
                {"name" :"Size", "type" : "bigint"},
                {"name" :"Date", "type" : "date"},
                {"name": "Path", "type" : "string"}
            ]
        }

    def generate_rows(self, dataset_schema=None, dataset_partitioning=None,
                            partition_id=None, records_limit = -1):
        """
        The main reading method.

        Returns a generator over the rows of the dataset (or partition)
        Each yielded row must be a dictionary, indexed by column name.

        The dataset schema and partitioning are given for information purpose.
        """
        if self.method == 'bgp':
            files = self.bgp.get_project_files()
            for file in files:
                yield {
                    "ID": int(file.data['id']),
                    "Name": file.data['originalName'],
                    "Format": file.data['format']['code'],
                    "Size": file.data['size'],
                    "Date": file.data['dateCreated'],
                    "Path": file.data['relativeAccessPoint']
                }
        else:
            yield {
                    "ID": 1,
                    "Name": "aap",
                    "Format": "noot",
                    "Size": 1,
                    "Date": '2021-02-12T18:26:28.389+0000',
                    "Path": "/aap/noot/mies"
                }

    def get_writer(self, dataset_schema=None, dataset_partitioning=None,
                         partition_id=None):
        """
        Returns a writer object to write in the dataset (or in a partition).

        The dataset_schema given here will match the the rows given to the writer below.

        Note: the writer is responsible for clearing the partition, if relevant.
        """
        raise Exception("Unimplemented")


    def get_partitioning(self):
        """
        Return the partitioning schema that the connector defines.
        """
        raise Exception("Unimplemented")


    def list_partitions(self, partitioning):
        """Return the list of partitions for the partitioning scheme
        passed as parameter"""
        return []


    def partition_exists(self, partitioning, partition_id):
        """Return whether the partition passed as parameter exists

        Implementation is only required if the corresponding flag is set to True
        in the connector definition
        """
        raise Exception("unimplemented")


    def get_records_count(self, partitioning=None, partition_id=None):
        """
        Returns the count of records for the dataset (or a partition).

        Implementation is only required if the corresponding flag is set to True
        in the connector definition
        """
        raise Exception("unimplemented")


class CustomDatasetWriter(object):
    def __init__(self):
        pass

    def write_row(self, row):
        """
        Row is a tuple with N + 1 elements matching the schema passed to get_writer.
        The last element is a dict of columns not found in the schema
        """
        raise Exception("unimplemented")

    def close(self):
        pass
