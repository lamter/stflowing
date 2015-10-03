=======
SecuritiesTransactionFlowing
=======
将各个 excel 格式的券商的交易流水文件转为 json 或者 csv 格式

Description
-----------
开发遵循以下规范：
- 同时支持 .xls 文件和 .xlsx 文件。但是优先支持 .xls 文件。
- 自动识别改交易流水所属的券商，以及流水类型。

Installation（未完成）
------------
Redisco requires redis-py 2.0.0 so get it first.

    pip install redis

Then install redisco.

    pip install redisco



Documentation
-------------
The documentation is available at : https://redisco.readthedocs.org


Which version should I consider ?
---------------------------------

- v0.1

.. image:: https://secure.travis-ci.org/kiddouk/redisco.png?branch=0.1
If you want something that is compatible with the original project developed by
you should consider v0.1. It works.

- v0.2

.. image:: https://secure.travis-ci.org/kiddouk/redisco.png?branch=0.2
If you are adventurous and want to try a version that is going closer to Ohm
project you should consider v0.2. Warning, your indexing keys will be broken
(if you are planning to migrate).

- master

.. image:: https://secure.travis-ci.org/kiddouk/redisco.png?branch=master
Well, expect things to be broken. Really broken.


Models
------

::

    from redisco import models
    class Person(models.Model):
        name = models.Attribute(required=True)
        created_at = models.DateTimeField(auto_now_add=True)
        fave_colors = models.ListField(str)

    >>> person = Person(name="Conchita")
    >>> person.is_valid()
    True
    >>> person.save()
    True
    >>> conchita = Person.objects.filter(name='Conchita')[0]
    >>> conchita.name
    'Conchita'
    >>> conchita.created_at
    datetime.datetime(2010, 5, 24, 16, 0, 31, 954704)


Model Attributes
----------------

Attribute
    Stores unicode strings. If used for large bodies of text,
    turn indexing of this field off by setting indexed=True.

IntegerField
    Stores an int. Ints are stringified using unicode() before saving to
    Redis.

Counter
    An IntegerField that can only be accessed via Model.incr and Model.decr.

DateTimeField
    Can store a DateTime object. Saved in the Redis store as a float.

DateField
    Can store a Date object. Saved in Redis as a float.

FloatField
    Can store floats.

BooleanField
    Can store bools. Saved in Redis as 1's and 0's.

ReferenceField
    Can reference other redisco model.

ListField
    Can store a list of unicode, int, float, as well as other redisco models.


Attribute Options
-----------------

required
    If True, the attirbute cannot be None or empty. Strings are stripped to
    check if they are empty. Default is False.

default
    Sets the default value of the attribute. Default is None.

indexed
    If True, redisco will create index entries for the attribute. Indexes
    are used in filtering and ordering results of queries. For large bodies
    of strings, this should be set to False. Default is True.

validator
    Set this to a callable that accepts two arguments -- the field name and
    the value of the attribute. The callable should return a list of tuples
    with the first item is the field name, and the second item is the error.

unique
    The field must be unique. Default is False.

DateField and DateTimeField Options

auto_now_add
    Automatically set the datetime/date field to now/today when the object
    is first created. Default is False.

auto_now
    Automatically set the datetime/date field to now/today everytime the object
    is saved. Default is False.


Class options
-------------

You can specify some options in your Model to control the behaviour of the
back scene.

::
    class User(models.Model):
        firstname = models.Attribute()
        lastname = models.Attribute()
        
        @property
        def fullname(self):
            return "%s %s" % (self.firstname, self.lastname)

        class Meta:
            indices = ['fullname']
            db = redis.Redis(host="localhost", db="6666")
            key = 'Account'


``indices`` is used to add extra indices that will be saved in the model.
``db`` object will be used instead of the global redisco ``redis_client``
``key`` will be used as the main key in the redis Hash (and sub objects)
instead of the class name.

Saving and Validating
---------------------

To save an object, call its save method. This returns True on success (i.e. when
the object is valid) and False otherwise.

Calling Model.is_valid will validate the attributes and lists. Model.is_valid
is called when the instance is being saved. When there are invalid fields,
Model.errors will hold the list of tuples containing the invalid fields and
the reason for its invalidity. E.g.
[('name', 'required'),('name', 'too short')]

Fields can be validated using the validator argument of the attribute. Just
pass a callable that accepts two arguments -- the field name and the value
of the attribute. The callable should return a list of errors.

Model.validate will also be called before saving the instance. Override it
to validate instances not related to attributes.

::

    def not_me(field_name, value):
        if value == 'Me':
            return ((field_name, 'it is me'),)

    class Person(models.Model):
        name = models.Attribute(required=True, validator=not_me)
        age = models.IntegerField()

        def validate(self):
            if self.age and self.age < 21:
                self._errors.append(('age', 'below 21'))

    >>> person = Person(name='Me')
    >>> person.is_valid()
    False
    >>> person.errors
    [('name', 'it is me')]


Queries
-------

Queries are executed using a manager, accessed via the objects class
attribute.

::

    Person.objects.all()
    Person.objects.filter(name='Conchita')
    Person.objects.filter(name='Conchita').first()
    Person.objects.all().order('name')
    Person.objects.filter(fave_colors='Red')

Ranged Queries
--------------

Redisco has a limited support for queries involving ranges -- it can only
filter fields that are numeric, i.e. DateField, DateTimeField, IntegerField,
and FloatField. The zfilter method of the manager is used for these queries.

::

    Person.objects.zfilter(created_at__lt=datetime(2010, 4, 20, 5, 2, 0))
    Person.objects.zfilter(created_at__gte=datetime(2010, 4, 20, 5, 2, 0))
    Person.objects.zfilter(created_at__in=(datetime(2010, 4, 20, 5, 2, 0), datetime(2010, 5, 1)))


Containers
----------
Redisco has three containers that roughly match Redis's supported data
structures: lists, sets, sorted set. Anything done to the container is
persisted to Redis.

Sets
    >>> from redisco.containers import Set
    >>> s = Set('myset')
    >>> s.add('apple')
    >>> s.add('orange')
    >>> s.add('bananas', 'tomatoes')
    >>> s.add(['blackberries', 'strawberries'])
    >>> s.members
    set(['apple', 'blackberries', 'strawberries', 'orange', 'tomatoes', 'bananas'])
    >>> s.remove('apple', 'orange')
    True
    set(['strawberries', 'bananas', 'tomatoes', 'blackberries'])
    >>> s.remove(['bananas', 'blackberries'])
    True
    >> s.members
    set(['strawberries', 'bananas', 'tomatoes'])
    >>> t = Set('nset')
    >>> t.add('kiwi')
    >>> t.add('guava')
    >>> t.members
    set(['kiwi', 'guava'])
    >>> s.update(t)
    >>> s.members
    set(['kiwi', 'orange', 'guava', 'apple'])

Lists
    >>> from redisco.containers import List
    >>> l = List('alpha')
    >>> l.append('a')
    >>> l.append(['b', 'c'])
    >>> l.append('d', 'e', 'f')
    >>> 'a' in l
    True
    >>> 'd' in l
    False
    >>> len(l)
    6
    >>> l.index('b')
    1
    >>> l.members
    ['a', 'b', 'c', 'd', 'e', 'f']


Sorted Sets
    >>> zset = SortedSet('zset')
    >>> zset.members
    ['d', 'a', 'b', 'c']
    >>> 'e' in zset
    False
    >>> 'a' in zset
    True
    >>> zset.rank('d')
    0
    >>> zset.rank('b')
    2
    >>> zset[1]
    'a'
    >>> zset.add({'f' : 200, 'e' : 201})
    >>> zset.members
    ['d', 'a', 'b', 'c', 'f', 'e']
    >>> zset.add('d', 99)
    >>> zset.members
    ['a', 'b', 'c', 'd', 'f', 'e']


Dicts/Hashes
    >>> h = cont.Hash('hkey')
    >>> len(h)
    0
    >>> h['name'] = "Richard Cypher"
    >>> h['real_name'] = "Richard Rahl"
    >>> h
    <Hash 'hkey' {'name': 'Richard Cypher', 'real_name': 'Richard Rahl'}>
    >>> h.dict
    {'name': 'Richard Cypher', 'real_name': 'Richard Rahl'}


Additional Info on Containers
-----------------------------

Some methods of the Redis client that require the key as the first argument
can be accessed from the container itself.

    >>> l = List('mylist')
    >>> l.lrange(0, -1)
    0
    >>> l.rpush('b')
    >>> l.rpush('c')
    >>> l.lpush('a')
    >>> l.lrange(0, -1)
    ['a', 'b', 'c']
    >>> h = Hash('hkey')
    >>> h.hset('name', 'Richard Rahl')
    >>> h
    <Hash 'hkey' {'name': 'Richard Rahl'}>


Connecting to Redis
-------------------

All models and containers use a global Redis client object to
interact with the key-value storage. By default, it connects
to localhost:6379, selecting db 0. If you wish to specify settings:

::

    import redisco
    redisco.connection_setup(host='localhost', port=6380, db=10)

The arguments to connect are simply passed to the redis.Redis init method.

For the containers, you can specify a second argument as the Redis client.
That client object will be used instead of the default.

    >>> import redis
    >>> r = redis.Redis(host='localhost', port=6381)
    >>> Set('someset', r)


Credits
-------

Most of the concepts are taken from `Soveran`_'s Redis related Ruby libraries.
cyx_ for sharing his expertise in indexing in Redis.
Django, of course, for the popular model API.

.. _Redis: http://code.google.com/p/redis/
.. _Ohm: http://github.com/soveran/ohm/
.. _redis-py: http://github.com/andymccurdy/redis-py/
.. _`Soveran`: http://github.com/soveran
.. _cyx: http://github.com/cyx
