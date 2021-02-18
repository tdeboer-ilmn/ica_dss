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


class MountMappingWithCreds(object):
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
        'path': 'str',
        'url': 'str',
        'urn': 'str',
        'type': 'str',
        'storage_provider': 'str',
        'credentials': 'dict(str, str)'
    }

    attribute_map = {
        'path': 'path',
        'url': 'url',
        'urn': 'urn',
        'type': 'type',
        'storage_provider': 'storageProvider',
        'credentials': 'credentials'
    }

    def __init__(self, path=None, url=None, urn=None, type=None, storage_provider=None, credentials=None):  # noqa: E501
        """MountMappingWithCreds - a model defined in Swagger"""  # noqa: E501

        self._path = None
        self._url = None
        self._urn = None
        self._type = None
        self._storage_provider = None
        self._credentials = None
        self.discriminator = None

        if path is not None:
            self.path = path
        if url is not None:
            self.url = url
        if urn is not None:
            self.urn = urn
        if type is not None:
            self.type = type
        if storage_provider is not None:
            self.storage_provider = storage_provider
        if credentials is not None:
            self.credentials = credentials

    @property
    def path(self):
        """Gets the path of this MountMappingWithCreds.  # noqa: E501


        :return: The path of this MountMappingWithCreds.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this MountMappingWithCreds.


        :param path: The path of this MountMappingWithCreds.  # noqa: E501
        :type: str
        """

        self._path = path

    @property
    def url(self):
        """Gets the url of this MountMappingWithCreds.  # noqa: E501


        :return: The url of this MountMappingWithCreds.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this MountMappingWithCreds.


        :param url: The url of this MountMappingWithCreds.  # noqa: E501
        :type: str
        """

        self._url = url

    @property
    def urn(self):
        """Gets the urn of this MountMappingWithCreds.  # noqa: E501


        :return: The urn of this MountMappingWithCreds.  # noqa: E501
        :rtype: str
        """
        return self._urn

    @urn.setter
    def urn(self, urn):
        """Sets the urn of this MountMappingWithCreds.


        :param urn: The urn of this MountMappingWithCreds.  # noqa: E501
        :type: str
        """

        self._urn = urn

    @property
    def type(self):
        """Gets the type of this MountMappingWithCreds.  # noqa: E501


        :return: The type of this MountMappingWithCreds.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this MountMappingWithCreds.


        :param type: The type of this MountMappingWithCreds.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def storage_provider(self):
        """Gets the storage_provider of this MountMappingWithCreds.  # noqa: E501


        :return: The storage_provider of this MountMappingWithCreds.  # noqa: E501
        :rtype: str
        """
        return self._storage_provider

    @storage_provider.setter
    def storage_provider(self, storage_provider):
        """Sets the storage_provider of this MountMappingWithCreds.


        :param storage_provider: The storage_provider of this MountMappingWithCreds.  # noqa: E501
        :type: str
        """

        self._storage_provider = storage_provider

    @property
    def credentials(self):
        """Gets the credentials of this MountMappingWithCreds.  # noqa: E501


        :return: The credentials of this MountMappingWithCreds.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._credentials

    @credentials.setter
    def credentials(self, credentials):
        """Sets the credentials of this MountMappingWithCreds.


        :param credentials: The credentials of this MountMappingWithCreds.  # noqa: E501
        :type: dict(str, str)
        """

        self._credentials = credentials

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
        if issubclass(MountMappingWithCreds, dict):
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
        if not isinstance(other, MountMappingWithCreds):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
