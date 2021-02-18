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


class LaunchWorkflowVersionRequest(object):
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
        'input': 'object',
        'engine_parameters': 'object'
    }

    attribute_map = {
        'name': 'name',
        'input': 'input',
        'engine_parameters': 'engineParameters'
    }

    def __init__(self, name=None, input=None, engine_parameters=None):  # noqa: E501
        """LaunchWorkflowVersionRequest - a model defined in Swagger"""  # noqa: E501

        self._name = None
        self._input = None
        self._engine_parameters = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if input is not None:
            self.input = input
        if engine_parameters is not None:
            self.engine_parameters = engine_parameters

    @property
    def name(self):
        """Gets the name of this LaunchWorkflowVersionRequest.  # noqa: E501

        Name of the workflow run  # noqa: E501

        :return: The name of this LaunchWorkflowVersionRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this LaunchWorkflowVersionRequest.

        Name of the workflow run  # noqa: E501

        :param name: The name of this LaunchWorkflowVersionRequest.  # noqa: E501
        :type: str
        """
        if name is not None and len(name) > 255:
            raise ValueError("Invalid value for `name`, length must be less than or equal to `255`")  # noqa: E501
        if name is not None and len(name) < 0:
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `0`")  # noqa: E501
        if name is not None and not re.search(r'^(?![wW][fF][rR]\\..*)(^[0-9a-zA-Z-_\\.]*$)', name):  # noqa: E501
            raise ValueError(r"Invalid value for `name`, must be a follow pattern or equal to `/^(?![wW][fF][rR]\\..*)(^[0-9a-zA-Z-_\\.]*$)/`")  # noqa: E501

        self._name = name

    @property
    def input(self):
        """Gets the input of this LaunchWorkflowVersionRequest.  # noqa: E501

        Input for the launched workflow run. Must resolve to a JSON object.  # noqa: E501

        :return: The input of this LaunchWorkflowVersionRequest.  # noqa: E501
        :rtype: object
        """
        return self._input

    @input.setter
    def input(self, input):
        """Sets the input of this LaunchWorkflowVersionRequest.

        Input for the launched workflow run. Must resolve to a JSON object.  # noqa: E501

        :param input: The input of this LaunchWorkflowVersionRequest.  # noqa: E501
        :type: object
        """

        self._input = input

    @property
    def engine_parameters(self):
        """Gets the engine_parameters of this LaunchWorkflowVersionRequest.  # noqa: E501

        Runtime options for launching workflows (currently only used for Airflow     and otherwise ignored). Must resolve to a JSON object.  # noqa: E501

        :return: The engine_parameters of this LaunchWorkflowVersionRequest.  # noqa: E501
        :rtype: object
        """
        return self._engine_parameters

    @engine_parameters.setter
    def engine_parameters(self, engine_parameters):
        """Sets the engine_parameters of this LaunchWorkflowVersionRequest.

        Runtime options for launching workflows (currently only used for Airflow     and otherwise ignored). Must resolve to a JSON object.  # noqa: E501

        :param engine_parameters: The engine_parameters of this LaunchWorkflowVersionRequest.  # noqa: E501
        :type: object
        """

        self._engine_parameters = engine_parameters

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
        if issubclass(LaunchWorkflowVersionRequest, dict):
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
        if not isinstance(other, LaunchWorkflowVersionRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
