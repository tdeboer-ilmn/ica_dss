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


class FolderCopyOperationParameters(object):
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
        'source_folder_urn': 'str',
        'target_folder_urn': 'str',
        'destination_folder_name': 'str'
    }

    attribute_map = {
        'source_folder_urn': 'sourceFolderUrn',
        'target_folder_urn': 'targetFolderUrn',
        'destination_folder_name': 'destinationFolderName'
    }

    def __init__(self, source_folder_urn=None, target_folder_urn=None, destination_folder_name=None):  # noqa: E501
        """FolderCopyOperationParameters - a model defined in Swagger"""  # noqa: E501

        self._source_folder_urn = None
        self._target_folder_urn = None
        self._destination_folder_name = None
        self.discriminator = None

        if source_folder_urn is not None:
            self.source_folder_urn = source_folder_urn
        if target_folder_urn is not None:
            self.target_folder_urn = target_folder_urn
        if destination_folder_name is not None:
            self.destination_folder_name = destination_folder_name

    @property
    def source_folder_urn(self):
        """Gets the source_folder_urn of this FolderCopyOperationParameters.  # noqa: E501

        The Urn of the source folder for the copy operation  # noqa: E501

        :return: The source_folder_urn of this FolderCopyOperationParameters.  # noqa: E501
        :rtype: str
        """
        return self._source_folder_urn

    @source_folder_urn.setter
    def source_folder_urn(self, source_folder_urn):
        """Sets the source_folder_urn of this FolderCopyOperationParameters.

        The Urn of the source folder for the copy operation  # noqa: E501

        :param source_folder_urn: The source_folder_urn of this FolderCopyOperationParameters.  # noqa: E501
        :type: str
        """

        self._source_folder_urn = source_folder_urn

    @property
    def target_folder_urn(self):
        """Gets the target_folder_urn of this FolderCopyOperationParameters.  # noqa: E501

        The Urn of the target folder for the copy operation  # noqa: E501

        :return: The target_folder_urn of this FolderCopyOperationParameters.  # noqa: E501
        :rtype: str
        """
        return self._target_folder_urn

    @target_folder_urn.setter
    def target_folder_urn(self, target_folder_urn):
        """Sets the target_folder_urn of this FolderCopyOperationParameters.

        The Urn of the target folder for the copy operation  # noqa: E501

        :param target_folder_urn: The target_folder_urn of this FolderCopyOperationParameters.  # noqa: E501
        :type: str
        """

        self._target_folder_urn = target_folder_urn

    @property
    def destination_folder_name(self):
        """Gets the destination_folder_name of this FolderCopyOperationParameters.  # noqa: E501

        The folder name for the copied folder  # noqa: E501

        :return: The destination_folder_name of this FolderCopyOperationParameters.  # noqa: E501
        :rtype: str
        """
        return self._destination_folder_name

    @destination_folder_name.setter
    def destination_folder_name(self, destination_folder_name):
        """Sets the destination_folder_name of this FolderCopyOperationParameters.

        The folder name for the copied folder  # noqa: E501

        :param destination_folder_name: The destination_folder_name of this FolderCopyOperationParameters.  # noqa: E501
        :type: str
        """

        self._destination_folder_name = destination_folder_name

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
        if issubclass(FolderCopyOperationParameters, dict):
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
        if not isinstance(other, FolderCopyOperationParameters):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
