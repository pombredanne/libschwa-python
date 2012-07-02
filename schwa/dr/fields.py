# vim: set ts=2 et:
from .collections import StoreList

__all__ = ['BaseAttr', 'BaseField', 'Field', 'Pointer', 'Pointers', 'Slice', 'BaseStore', 'Store', 'Singleton']


class BaseAttr(object):
  __slots__ = ('serial', 'help')

  def __init__(self, serial=None, help=None):
    self.serial = serial
    self.help = help

  def default(self):
    """
    Returns the default value for this type when it is instantiated.
    """
    raise NotImplementedError

  def is_fulfilled(self):
    raise NotImplementedError

  def get_dependency(self):
    raise NotImplementedError

  def set_dependency(self, klass):
    raise NotImplementedError


# =============================================================================
# =============================================================================
class BaseField(BaseAttr):
  pass


class Field(BaseField):
  def default(self):
    return None

  def is_fulfilled(self):
    return True


class Pointer(BaseField):
  __slots__ = ('klass_name', 'store', 'is_collection', '_klass')

  def __init__(self, klass_name, store=None, is_collection=False, serial=None, help=None):
    super(Pointer, self).__init__(serial=serial, help=help)
    if isinstance(klass_name, (str, unicode)):
      self.klass_name = klass_name.encode('utf-8')
      self._klass = None
    else:
      self.klass_name = klass_name._dr_name
      self._klass = klass_name
    self.store = store
    self.is_collection = is_collection

  def default(self):
    return None

  def is_fulfilled(self):
    return self._klass is not None

  def get_dependency(self):
    return self.klass_name

  def set_dependency(self, klass):
    self._klass = klass

  def __repr__(self):
    return '{0}({1}, store={2}, is_collection={3})'.format(self.__class__.__name__, self.klass_name, self.store, self.is_collection)


class Pointers(Pointer):
  def __init__(self, klass_name, store=None, serial=None, help=None):
    super(Pointers, self).__init__(klass_name, store=store, is_collection=True, serial=serial, help=help)

  def default(self):
    assert self._klass is not None
    return StoreList(self._klass)


class Slice(BaseField):
  __slots__ = ('klass_name', 'store', '_klass')

  def __init__(self, klass_name=None, store=None, serial=None, help=None):
    super(Slice, self).__init__(serial=serial, help=help)
    if klass_name is None:
      self.klass_name = None
      self._klass = None
    elif isinstance(klass_name, (str, unicode)):
      self.klass_name = klass_name.encode('utf-8')
      self._klass = None
    else:
      self.klass_name = klass_name._dr_name
      self._klass = klass_name
    self.store = store

  def default(self):
    return None

  def is_pointer(self):
    return self.klass_name is not None

  def is_fulfilled(self):
    if self.is_pointer():
      return self._klass is not None
    return True

  def get_dependency(self):
    return self.klass_name

  def set_dependency(self, klass):
    self._klass = klass


# =============================================================================
# =============================================================================
class BaseStore(BaseAttr):
  def is_collection(self):
    return True


class Store(BaseStore):
  """
  A Store houses Annotation instances. For an Annotation to be serialised, it needs
  to be placed into a Store.
  """
  __slots__ = ('klass_name', '_klass')

  def __init__(self, klass_name, **kwargs):
    super(Store, self).__init__(**kwargs)
    if isinstance(klass_name, (str, unicode)):
      self.klass_name = klass_name.encode('utf-8')
      self._klass = None
    else:
      self.klass_name = klass_name._dr_name
      self._klass = klass_name

  def default(self):
    assert self._klass is not None
    return StoreList(self._klass)

  def is_fulfilled(self):
    return self._klass is not None

  def get_dependency(self):
    return self.klass_name

  def set_dependency(self, klass):
    self._klass = klass


class Singleton(Store):
  def default(self):
    return None

  def is_collection(self):
    return False
