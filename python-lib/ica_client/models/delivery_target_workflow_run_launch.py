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


class DeliveryTargetWorkflowRunLaunch(object):
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
        'id': 'str',
        'version': 'str',
        'name': 'str',
        'input': 'object'
    }

    attribute_map = {
        'id': 'id',
        'version': 'version',
        'name': 'name',
        'input': 'input'
    }

    def __init__(self, id=None, version=None, name=None, input=None):  # noqa: E501
        """DeliveryTargetWorkflowRunLaunch - a model defined in Swagger"""  # noqa: E501

        self._id = None
        self._version = None
        self._name = None
        self._input = None
        self.discriminator = None

        self.id = id
        self.version = version
        self.name = name
        if input is not None:
            self.input = input

    @property
    def id(self):
        """Gets the id of this DeliveryTargetWorkflowRunLaunch.  # noqa: E501

        Id of the workflow to launch  # noqa: E501

        :return: The id of this DeliveryTargetWorkflowRunLaunch.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this DeliveryTargetWorkflowRunLaunch.

        Id of the workflow to launch  # noqa: E501

        :param id: The id of this DeliveryTargetWorkflowRunLaunch.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def version(self):
        """Gets the version of this DeliveryTargetWorkflowRunLaunch.  # noqa: E501

        Version of the workflow to launch, for the given id  # noqa: E501

        :return: The version of this DeliveryTargetWorkflowRunLaunch.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this DeliveryTargetWorkflowRunLaunch.

        Version of the workflow to launch, for the given id  # noqa: E501

        :param version: The version of this DeliveryTargetWorkflowRunLaunch.  # noqa: E501
        :type: str
        """
        if version is None:
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501

        self._version = version

    @property
    def name(self):
        """Gets the name of this DeliveryTargetWorkflowRunLaunch.  # noqa: E501

        Name for the workflowRun  # noqa: E501

        :return: The name of this DeliveryTargetWorkflowRunLaunch.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this DeliveryTargetWorkflowRunLaunch.

        Name for the workflowRun  # noqa: E501

        :param name: The name of this DeliveryTargetWorkflowRunLaunch.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def input(self):
        """Gets the input of this DeliveryTargetWorkflowRunLaunch.  # noqa: E501

        Arguments for the workflowRun  # noqa: E501

        :return: The input of this DeliveryTargetWorkflowRunLaunch.  # noqa: E501
        :rtype: object
        """
        return self._input

    @input.setter
    def input(self, input):
        """Sets the input of this DeliveryTargetWorkflowRunLaunch.

        Arguments for the workflowRun  # noqa: E501

        :param input: The input of this DeliveryTargetWorkflowRunLaunch.  # noqa: E501
        :type: object
        """

        self._input = input

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
        if issubclass(DeliveryTargetWorkflowRunLaunch, dict):
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
        if not isinstance(other, DeliveryTargetWorkflowRunLaunch):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
