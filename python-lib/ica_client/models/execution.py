# coding: utf-8

"""
    Illumina Connected Analysis

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class Execution(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'image': 'Image',
        'command': 'str',
        'args': 'list[str]',
        'inputs': 'list[InputMountMappingWithCreds]',
        'outputs': 'list[MountMappingWithCreds]',
        'system_files': 'SystemFiles',
        'environment': 'Environment',
        'working_directory': 'str',
        'retry_limit': 'int',
        'retry_count': 'int'
    }

    attribute_map = {
        'image': 'image',
        'command': 'command',
        'args': 'args',
        'inputs': 'inputs',
        'outputs': 'outputs',
        'system_files': 'systemFiles',
        'environment': 'environment',
        'working_directory': 'workingDirectory',
        'retry_limit': 'retryLimit',
        'retry_count': 'retryCount'
    }

    def __init__(self, image=None, command=None, args=None, inputs=None, outputs=None, system_files=None, environment=None, working_directory=None, retry_limit=3, retry_count=0):  # noqa: E501
        """Execution - a model defined in Swagger"""  # noqa: E501

        self._image = None
        self._command = None
        self._args = None
        self._inputs = None
        self._outputs = None
        self._system_files = None
        self._environment = None
        self._working_directory = None
        self._retry_limit = None
        self._retry_count = None
        self.discriminator = None

        if image is not None:
            self.image = image
        if command is not None:
            self.command = command
        if args is not None:
            self.args = args
        if inputs is not None:
            self.inputs = inputs
        if outputs is not None:
            self.outputs = outputs
        if system_files is not None:
            self.system_files = system_files
        if environment is not None:
            self.environment = environment
        if working_directory is not None:
            self.working_directory = working_directory
        if retry_limit is not None:
            self.retry_limit = retry_limit
        if retry_count is not None:
            self.retry_count = retry_count

    @property
    def image(self):
        """Gets the image of this Execution.  # noqa: E501


        :return: The image of this Execution.  # noqa: E501
        :rtype: Image
        """
        return self._image

    @image.setter
    def image(self, image):
        """Sets the image of this Execution.


        :param image: The image of this Execution.  # noqa: E501
        :type: Image
        """

        self._image = image

    @property
    def command(self):
        """Gets the command of this Execution.  # noqa: E501


        :return: The command of this Execution.  # noqa: E501
        :rtype: str
        """
        return self._command

    @command.setter
    def command(self, command):
        """Sets the command of this Execution.


        :param command: The command of this Execution.  # noqa: E501
        :type: str
        """

        self._command = command

    @property
    def args(self):
        """Gets the args of this Execution.  # noqa: E501

        Argument to run specified task  # noqa: E501

        :return: The args of this Execution.  # noqa: E501
        :rtype: list[str]
        """
        return self._args

    @args.setter
    def args(self, args):
        """Sets the args of this Execution.

        Argument to run specified task  # noqa: E501

        :param args: The args of this Execution.  # noqa: E501
        :type: list[str]
        """

        self._args = args

    @property
    def inputs(self):
        """Gets the inputs of this Execution.  # noqa: E501

        Path (Inputs) - Path to mount file at valid Url  URL (Inputs) - Url of file mounted at specified path  # noqa: E501

        :return: The inputs of this Execution.  # noqa: E501
        :rtype: list[InputMountMappingWithCreds]
        """
        return self._inputs

    @inputs.setter
    def inputs(self, inputs):
        """Sets the inputs of this Execution.

        Path (Inputs) - Path to mount file at valid Url  URL (Inputs) - Url of file mounted at specified path  # noqa: E501

        :param inputs: The inputs of this Execution.  # noqa: E501
        :type: list[InputMountMappingWithCreds]
        """

        self._inputs = inputs

    @property
    def outputs(self):
        """Gets the outputs of this Execution.  # noqa: E501

        Path (Outputs) - Path where files will be output to valid Url  URL (Outputs) - Url of folder with files from the path will be uploaded  # noqa: E501

        :return: The outputs of this Execution.  # noqa: E501
        :rtype: list[MountMappingWithCreds]
        """
        return self._outputs

    @outputs.setter
    def outputs(self, outputs):
        """Sets the outputs of this Execution.

        Path (Outputs) - Path where files will be output to valid Url  URL (Outputs) - Url of folder with files from the path will be uploaded  # noqa: E501

        :param outputs: The outputs of this Execution.  # noqa: E501
        :type: list[MountMappingWithCreds]
        """

        self._outputs = outputs

    @property
    def system_files(self):
        """Gets the system_files of this Execution.  # noqa: E501


        :return: The system_files of this Execution.  # noqa: E501
        :rtype: SystemFiles
        """
        return self._system_files

    @system_files.setter
    def system_files(self, system_files):
        """Sets the system_files of this Execution.


        :param system_files: The system_files of this Execution.  # noqa: E501
        :type: SystemFiles
        """

        self._system_files = system_files

    @property
    def environment(self):
        """Gets the environment of this Execution.  # noqa: E501


        :return: The environment of this Execution.  # noqa: E501
        :rtype: Environment
        """
        return self._environment

    @environment.setter
    def environment(self, environment):
        """Sets the environment of this Execution.


        :param environment: The environment of this Execution.  # noqa: E501
        :type: Environment
        """

        self._environment = environment

    @property
    def working_directory(self):
        """Gets the working_directory of this Execution.  # noqa: E501


        :return: The working_directory of this Execution.  # noqa: E501
        :rtype: str
        """
        return self._working_directory

    @working_directory.setter
    def working_directory(self, working_directory):
        """Sets the working_directory of this Execution.


        :param working_directory: The working_directory of this Execution.  # noqa: E501
        :type: str
        """

        self._working_directory = working_directory

    @property
    def retry_limit(self):
        """Gets the retry_limit of this Execution.  # noqa: E501


        :return: The retry_limit of this Execution.  # noqa: E501
        :rtype: int
        """
        return self._retry_limit

    @retry_limit.setter
    def retry_limit(self, retry_limit):
        """Sets the retry_limit of this Execution.


        :param retry_limit: The retry_limit of this Execution.  # noqa: E501
        :type: int
        """

        self._retry_limit = retry_limit

    @property
    def retry_count(self):
        """Gets the retry_count of this Execution.  # noqa: E501


        :return: The retry_count of this Execution.  # noqa: E501
        :rtype: int
        """
        return self._retry_count

    @retry_count.setter
    def retry_count(self, retry_count):
        """Sets the retry_count of this Execution.


        :param retry_count: The retry_count of this Execution.  # noqa: E501
        :type: int
        """

        self._retry_count = retry_count

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(Execution, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Execution):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
