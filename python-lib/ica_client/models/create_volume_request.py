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


class CreateVolumeRequest(object):
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
        'name': 'str',
        'volume_configuration_name': 'str',
        'root_key_prefix': 'str'
    }

    attribute_map = {
        'name': 'name',
        'volume_configuration_name': 'volumeConfigurationName',
        'root_key_prefix': 'rootKeyPrefix'
    }

    def __init__(self, name=None, volume_configuration_name=None, root_key_prefix=None):  # noqa: E501
        """CreateVolumeRequest - a model defined in Swagger"""  # noqa: E501

        self._name = None
        self._volume_configuration_name = None
        self._root_key_prefix = None
        self.discriminator = None

        self.name = name
        if volume_configuration_name is not None:
            self.volume_configuration_name = volume_configuration_name
        if root_key_prefix is not None:
            self.root_key_prefix = root_key_prefix

    @property
    def name(self):
        """Gets the name of this CreateVolumeRequest.  # noqa: E501

        Name for the volume  # noqa: E501

        :return: The name of this CreateVolumeRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CreateVolumeRequest.

        Name for the volume  # noqa: E501

        :param name: The name of this CreateVolumeRequest.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def volume_configuration_name(self):
        """Gets the volume_configuration_name of this CreateVolumeRequest.  # noqa: E501

        Unique name of the volume configuration to use  # noqa: E501

        :return: The volume_configuration_name of this CreateVolumeRequest.  # noqa: E501
        :rtype: str
        """
        return self._volume_configuration_name

    @volume_configuration_name.setter
    def volume_configuration_name(self, volume_configuration_name):
        """Sets the volume_configuration_name of this CreateVolumeRequest.

        Unique name of the volume configuration to use  # noqa: E501

        :param volume_configuration_name: The volume_configuration_name of this CreateVolumeRequest.  # noqa: E501
        :type: str
        """

        self._volume_configuration_name = volume_configuration_name

    @property
    def root_key_prefix(self):
        """Gets the root_key_prefix of this CreateVolumeRequest.  # noqa: E501

        The base bucket location for volumes associated with custom VolumeConfigurations. If not provided, the given volume Name is used.  If provided, it must start with the VolumeConfiguration's keyprefix and end with a /.  To create a volume representing the root of a bucket, use the value '/'.  # noqa: E501

        :return: The root_key_prefix of this CreateVolumeRequest.  # noqa: E501
        :rtype: str
        """
        return self._root_key_prefix

    @root_key_prefix.setter
    def root_key_prefix(self, root_key_prefix):
        """Sets the root_key_prefix of this CreateVolumeRequest.

        The base bucket location for volumes associated with custom VolumeConfigurations. If not provided, the given volume Name is used.  If provided, it must start with the VolumeConfiguration's keyprefix and end with a /.  To create a volume representing the root of a bucket, use the value '/'.  # noqa: E501

        :param root_key_prefix: The root_key_prefix of this CreateVolumeRequest.  # noqa: E501
        :type: str
        """
        if root_key_prefix is not None and not re.search(r'^(\/)$|^([^\/].*[\/])$', root_key_prefix):  # noqa: E501
            raise ValueError(r"Invalid value for `root_key_prefix`, must be a follow pattern or equal to `/^(\/)$|^([^\/].*[\/])$/`")  # noqa: E501

        self._root_key_prefix = root_key_prefix

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
        if issubclass(CreateVolumeRequest, dict):
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
        if not isinstance(other, CreateVolumeRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
