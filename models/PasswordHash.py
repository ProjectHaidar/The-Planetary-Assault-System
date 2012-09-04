# -*- coding: utf-8 -*-
'''
Created on Mar 12, 2012

@author: moloch

    Copyright [2012] [Redacted Labs]

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
'''


import re
import logging

from sqlalchemy import Column, ForeignKey, and_
from sqlalchemy.orm import synonym, relationship, backref
from sqlalchemy.types import Unicode, Integer, Boolean
from models import dbsession
from models.BaseObject import BaseObject
from string import ascii_letters, digits


class PasswordHash(BaseObject):
    '''
    Generic password hash object, can be of any algorithm
    '''

    job_id = Column(Integer, ForeignKey('job.id'), nullable=False)
    algorithm_id = Column(Integer, ForeignKey('algorithm.id'), nullable=False)
    user_name = Column(Unicode(64))
    _cipher_text = Column(Unicode(128), nullable=False)
    cipher_text = synonym('_cipher_text', descriptor=property(
        lambda self: self._cipher_text,
        lambda self, cipher_text: setattr(self, '_cipher_text',
                                          self.__class__._filter_string(cipher_text))
    ))
    plain_text = Column(Unicode(64))
    solved = Column(Boolean, default=False, nullable=False)

    @classmethod
    def by_id(cls, hash_id):
        ''' Return the PasswordHash object whose user id is 'hash_id' '''
        return dbsession.query(cls).filter_by(id=hash_id).first()

    @classmethod
    def by_cipher_text(cls, cipher_text_value, job_id_value):
        ''' Return the digest based on valud and job_id '''
        return dbsession.query(cls).filter(and_(cipher_text == cipher_text_value, job_id == job_id_value)).first()

    @classmethod
    def by_algorithm(cls, algo):
        ''' Return all passwordHash objects of a given algorithm id '''
        if type(algo) == int:
            return dbsession.query(cls).filter_by(algorithm_id=algo).all()
        else:
            return dbsession.query(cls).filter_by(algorithm_id=algo.id).all()

    @classmethod
    def _filter_string(cls, string, extra_chars=""):
        char_white_list = ascii_letters + digits + extra_chars
        return filter(lambda char: char in char_white_list, string)

    def __len__(self):
        ''' Returns the length of the digest '''
        return len(self.digest)
