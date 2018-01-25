#!/usr/bin/env python
# coding: utf-8

from peewee import *

db = SqliteDatabase('waffle.sqlite')

class Person(Model):
    name = CharField(default='')
    age = IntegerField(default=0)

    class Meta:
        database = db

class Pet(Model):
    owner = ForeignKeyField(Person, related_name='pets')
    name = CharField()
    animal_type = CharField()

    class Meta:
        database = db


def create_db():
    db.create_tables([Person, Pet])