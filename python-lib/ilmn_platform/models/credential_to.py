# coding: utf-8

"""
    Platform Services API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class CredentialTO(object):
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
        'creationdate': 'str',
        'id': 'str',
        'identity': 'str',
        'lastupdatedate': 'str',
        'lastusedtime': 'str',
        'name': 'str',
        'secret': 'dict(str, str)',
        'type': 'str'
    }

    attribute_map = {
        'creationdate': 'creationdate',
        'id': 'id',
        'identity': 'identity',
        'lastupdatedate': 'lastupdatedate',
        'lastusedtime': 'lastusedtime',
        'name': 'name',
        'secret': 'secret',
        'type': 'type'
    }

    def __init__(self, creationdate=None, id=None, identity=None, lastupdatedate=None, lastusedtime=None, name=None, secret=None, type=None):  # noqa: E501
        """CredentialTO - a model defined in Swagger"""  # noqa: E501

        self._creationdate = None
        self._id = None
        self._identity = None
        self._lastupdatedate = None
        self._lastusedtime = None
        self._name = None
        self._secret = None
        self._type = None
        self.discriminator = None

        if creationdate is not None:
            self.creationdate = creationdate
        if id is not None:
            self.id = id
        if identity is not None:
            self.identity = identity
        if lastupdatedate is not None:
            self.lastupdatedate = lastupdatedate
        if lastusedtime is not None:
            self.lastusedtime = lastusedtime
        if name is not None:
            self.name = name
        if secret is not None:
            self.secret = secret
        if type is not None:
            self.type = type

    @property
    def creationdate(self):
        """Gets the creationdate of this CredentialTO.  # noqa: E501


        :return: The creationdate of this CredentialTO.  # noqa: E501
        :rtype: str
        """
        return self._creationdate

    @creationdate.setter
    def creationdate(self, creationdate):
        """Sets the creationdate of this CredentialTO.


        :param creationdate: The creationdate of this CredentialTO.  # noqa: E501
        :type: str
        """

        self._creationdate = creationdate

    @property
    def id(self):
        """Gets the id of this CredentialTO.  # noqa: E501


        :return: The id of this CredentialTO.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this CredentialTO.


        :param id: The id of this CredentialTO.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def identity(self):
        """Gets the identity of this CredentialTO.  # noqa: E501


        :return: The identity of this CredentialTO.  # noqa: E501
        :rtype: str
        """
        return self._identity

    @identity.setter
    def identity(self, identity):
        """Sets the identity of this CredentialTO.


        :param identity: The identity of this CredentialTO.  # noqa: E501
        :type: str
        """

        self._identity = identity

    @property
    def lastupdatedate(self):
        """Gets the lastupdatedate of this CredentialTO.  # noqa: E501


        :return: The lastupdatedate of this CredentialTO.  # noqa: E501
        :rtype: str
        """
        return self._lastupdatedate

    @lastupdatedate.setter
    def lastupdatedate(self, lastupdatedate):
        """Sets the lastupdatedate of this CredentialTO.


        :param lastupdatedate: The lastupdatedate of this CredentialTO.  # noqa: E501
        :type: str
        """

        self._lastupdatedate = lastupdatedate

    @property
    def lastusedtime(self):
        """Gets the lastusedtime of this CredentialTO.  # noqa: E501


        :return: The lastusedtime of this CredentialTO.  # noqa: E501
        :rtype: str
        """
        return self._lastusedtime

    @lastusedtime.setter
    def lastusedtime(self, lastusedtime):
        """Sets the lastusedtime of this CredentialTO.


        :param lastusedtime: The lastusedtime of this CredentialTO.  # noqa: E501
        :type: str
        """

        self._lastusedtime = lastusedtime

    @property
    def name(self):
        """Gets the name of this CredentialTO.  # noqa: E501


        :return: The name of this CredentialTO.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CredentialTO.


        :param name: The name of this CredentialTO.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def secret(self):
        """Gets the secret of this CredentialTO.  # noqa: E501


        :return: The secret of this CredentialTO.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._secret

    @secret.setter
    def secret(self, secret):
        """Sets the secret of this CredentialTO.


        :param secret: The secret of this CredentialTO.  # noqa: E501
        :type: dict(str, str)
        """

        self._secret = secret

    @property
    def type(self):
        """Gets the type of this CredentialTO.  # noqa: E501


        :return: The type of this CredentialTO.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this CredentialTO.


        :param type: The type of this CredentialTO.  # noqa: E501
        :type: str
        """

        self._type = type

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
        if issubclass(CredentialTO, dict):
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
        if not isinstance(other, CredentialTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
