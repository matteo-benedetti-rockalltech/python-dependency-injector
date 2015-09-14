"""Dependency injector providers unittests."""

import unittest2 as unittest
import dependency_injector as di


class ProviderTests(unittest.TestCase):

    """Provider test cases."""

    def setUp(self):
        """Set test cases environment up."""
        self.provider = di.Provider()

    def test_is_provider(self):
        """Test `is_provider` check."""
        self.assertTrue(di.is_provider(self.provider))

    def test_call(self):
        """Test call."""
        self.assertRaises(NotImplementedError, self.provider.__call__)

    def test_delegate(self):
        """Test creating of provider delegation."""
        delegate1 = self.provider.delegate()

        self.assertIsInstance(delegate1, di.Delegate)
        self.assertIs(delegate1(), self.provider)

        delegate2 = self.provider.delegate()

        self.assertIsInstance(delegate2, di.Delegate)
        self.assertIs(delegate2(), self.provider)

        self.assertIsNot(delegate1, delegate2)

    def test_override(self):
        """Test provider overriding."""
        overriding_provider = di.Provider()
        self.provider.override(overriding_provider)
        self.assertTrue(self.provider.is_overridden)

    def test_override_with_not_provider(self):
        """Test provider overriding with not provider instance."""
        self.assertRaises(di.Error, self.provider.override, object())

    def test_last_overriding(self):
        """Test getting last overriding provider."""
        overriding_provider1 = di.Provider()
        overriding_provider2 = di.Provider()

        self.provider.override(overriding_provider1)
        self.assertIs(self.provider.last_overriding, overriding_provider1)

        self.provider.override(overriding_provider2)
        self.assertIs(self.provider.last_overriding, overriding_provider2)

    def test_last_overriding_of_not_overridden_provider(self):
        """Test getting last overriding from not overridden provider."""
        try:
            self.provider.last_overriding
        except di.Error:
            pass
        else:
            self.fail('Got en error in {}'.format(
                str(self.test_last_overriding_of_not_overridden_provider)))

    def test_reset_last_overriding(self):
        """Test reseting of last overriding provider."""
        overriding_provider1 = di.Provider()
        overriding_provider2 = di.Provider()

        self.provider.override(overriding_provider1)
        self.provider.override(overriding_provider2)

        self.assertIs(self.provider.last_overriding, overriding_provider2)

        self.provider.reset_last_overriding()
        self.assertIs(self.provider.last_overriding, overriding_provider1)

        self.provider.reset_last_overriding()
        self.assertFalse(self.provider.is_overridden)

    def test_reset_last_overriding_of_not_overridden_provider(self):
        """Test resetting of last overriding on not overridden provier."""
        self.assertRaises(di.Error, self.provider.reset_last_overriding)

    def test_reset_override(self):
        """Test reset of provider's override."""
        overriding_provider = di.Provider()
        self.provider.override(overriding_provider)

        self.assertTrue(self.provider.is_overridden)
        self.assertIs(self.provider.last_overriding, overriding_provider)

        self.provider.reset_override()

        self.assertFalse(self.provider.is_overridden)
        try:
            self.provider.last_overriding
        except di.Error:
            pass
        else:
            self.fail('Got en error in {}'.format(
                str(self.test_last_overriding_of_not_overridden_provider)))


class DelegateTests(unittest.TestCase):

    """Delegate test cases."""

    def setUp(self):
        """Set test cases environment up."""
        self.delegated = di.Provider()
        self.delegate = di.Delegate(delegated=self.delegated)

    def test_is_provider(self):
        """Test `is_provider` check."""
        self.assertTrue(di.is_provider(self.delegate))

    def test_init_with_not_provider(self):
        """Test that delegate accepts only another provider as delegated."""
        self.assertRaises(di.Error, di.Delegate, delegated=object())

    def test_call(self):
        """Test returning of delegated provider."""
        delegated1 = self.delegate()
        delegated2 = self.delegate()

        self.assertIs(delegated1, self.delegated)
        self.assertIs(delegated2, self.delegated)


class FactoryTests(unittest.TestCase):

    """Factory test cases."""

    class Example(object):

        """Example class for Factory provider tests."""

        def __init__(self, init_arg1=None, init_arg2=None):
            """Initializer.

            :param init_arg1:
            :param init_arg2:
            :return:
            """
            self.init_arg1 = init_arg1
            self.init_arg2 = init_arg2

            self.attribute1 = None
            self.attribute2 = None

            self.method1_value = None
            self.method2_value = None

        def method1(self, value):
            """Setter method 1."""
            self.method1_value = value

        def method2(self, value):
            """Setter method 2."""
            self.method2_value = value

    def test_is_provider(self):
        """Test `is_provider` check."""
        self.assertTrue(di.is_provider(di.Factory(self.Example)))

    def test_init_with_callable(self):
        """Test creation of provider with a callable."""
        self.assertTrue(di.Factory(credits))

    def test_init_with_not_callable(self):
        """Test creation of provider with not a callable."""
        self.assertRaises(di.Error, di.Factory, 123)

    def test_call(self):
        """Test creation of new instances."""
        provider = di.Factory(self.Example)
        instance1 = provider()
        instance2 = provider()

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, self.Example)
        self.assertIsInstance(instance2, self.Example)

    def test_call_with_init_args_simplified_syntax(self):
        """Test creation of new instances with init args injections.

        New simplified syntax.
        """
        provider = di.Factory(self.Example,
                              init_arg1='i1',
                              init_arg2='i2')

        instance1 = provider()
        instance2 = provider()

        self.assertEqual(instance1.init_arg1, 'i1')
        self.assertEqual(instance1.init_arg2, 'i2')

        self.assertEqual(instance2.init_arg1, 'i1')
        self.assertEqual(instance2.init_arg2, 'i2')

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, self.Example)
        self.assertIsInstance(instance2, self.Example)

    def test_call_with_init_args_old_syntax(self):
        """Test creation of new instances with init args injections."""
        provider = di.Factory(self.Example,
                              di.KwArg('init_arg1', 'i1'),
                              di.KwArg('init_arg2', 'i2'))

        instance1 = provider()
        instance2 = provider()

        self.assertEqual(instance1.init_arg1, 'i1')
        self.assertEqual(instance1.init_arg2, 'i2')

        self.assertEqual(instance2.init_arg1, 'i1')
        self.assertEqual(instance2.init_arg2, 'i2')

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, self.Example)
        self.assertIsInstance(instance2, self.Example)

    def test_call_with_attributes(self):
        """Test creation of new instances with attribute injections."""
        provider = di.Factory(self.Example,
                              di.Attribute('attribute1', 'a1'),
                              di.Attribute('attribute2', 'a2'))

        instance1 = provider()
        instance2 = provider()

        self.assertEqual(instance1.attribute1, 'a1')
        self.assertEqual(instance1.attribute2, 'a2')

        self.assertEqual(instance2.attribute1, 'a1')
        self.assertEqual(instance2.attribute2, 'a2')

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, self.Example)
        self.assertIsInstance(instance2, self.Example)

    def test_call_with_methods(self):
        """Test creation of new instances with method injections."""
        provider = di.Factory(self.Example,
                              di.Method('method1', 'm1'),
                              di.Method('method2', 'm2'))

        instance1 = provider()
        instance2 = provider()

        self.assertEqual(instance1.method1_value, 'm1')
        self.assertEqual(instance1.method2_value, 'm2')

        self.assertEqual(instance2.method1_value, 'm1')
        self.assertEqual(instance2.method2_value, 'm2')

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, self.Example)
        self.assertIsInstance(instance2, self.Example)

    def test_call_with_context_args(self):
        """Test creation of new instances with context args."""
        provider = di.Factory(self.Example)
        instance = provider(11, 22)

        self.assertEqual(instance.init_arg1, 11)
        self.assertEqual(instance.init_arg2, 22)

    def test_call_with_context_kwargs(self):
        """Test creation of new instances with context kwargs."""
        provider = di.Factory(self.Example,
                              di.KwArg('init_arg1', 1))

        instance1 = provider(init_arg2=22)
        self.assertEqual(instance1.init_arg1, 1)
        self.assertEqual(instance1.init_arg2, 22)

        instance1 = provider(init_arg1=11, init_arg2=22)
        self.assertEqual(instance1.init_arg1, 11)
        self.assertEqual(instance1.init_arg2, 22)

    def test_call_overridden(self):
        """Test creation of new instances on overridden provider."""
        provider = di.Factory(self.Example)
        overriding_provider1 = di.Factory(dict)
        overriding_provider2 = di.Factory(list)

        provider.override(overriding_provider1)
        provider.override(overriding_provider2)

        instance1 = provider()
        instance2 = provider()

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, list)
        self.assertIsInstance(instance2, list)

    def test_injections(self):
        """Test getting a full list of injections using Factory.injections."""
        provider = di.Factory(self.Example,
                              di.KwArg('init_arg1', 1),
                              di.KwArg('init_arg2', 2),
                              di.Attribute('attribute1', 3),
                              di.Attribute('attribute2', 4),
                              di.Method('method1', 5),
                              di.Method('method2', 6))

        injections = provider.injections

        self.assertEquals(len(injections), 6)


class SingletonTests(unittest.TestCase):

    """Singleton test cases."""

    def test_call(self):
        """Test creation and returning of single object."""
        provider = di.Singleton(object)

        instance1 = provider()
        instance2 = provider()

        self.assertIsInstance(instance1, object)
        self.assertIsInstance(instance2, object)
        self.assertIs(instance1, instance2)

    def test_reset(self):
        """Test creation and reset of single object."""
        provider = di.Singleton(object)

        instance1 = provider()
        self.assertIsInstance(instance1, object)

        provider.reset()

        instance2 = provider()
        self.assertIsInstance(instance1, object)

        self.assertIsNot(instance1, instance2)


class ExternalDependencyTests(unittest.TestCase):

    """ExternalDependency test cases."""

    def setUp(self):
        """Set test cases environment up."""
        self.provider = di.ExternalDependency(instance_of=list)

    def test_init_with_not_class(self):
        """Test creation with not a class."""
        self.assertRaises(di.Error, di.ExternalDependency, object())

    def test_is_provider(self):
        """Test `is_provider` check."""
        self.assertTrue(di.is_provider(self.provider))

    def test_call_overridden(self):
        """Test call of overridden external dependency."""
        self.provider.provided_by(di.Factory(list))
        self.assertIsInstance(self.provider(), list)

    def test_call_overridden_but_not_instance_of(self):
        """Test call of overridden external dependency, but not instance of."""
        self.provider.provided_by(di.Factory(dict))
        self.assertRaises(di.Error, self.provider)

    def test_call_not_overridden(self):
        """Test call of not satisfied external dependency."""
        self.assertRaises(di.Error, self.provider)


class StaticProvidersTests(unittest.TestCase):

    """Static providers test cases."""

    def test_is_provider(self):
        """Test `is_provider` check."""
        self.assertTrue(di.is_provider(di.Class(object)))
        self.assertTrue(di.is_provider(di.Object(object())))
        self.assertTrue(di.is_provider(di.Function(map)))
        self.assertTrue(di.is_provider(di.Value(123)))

    def test_call_class_provider(self):
        """Test Class provider call."""
        self.assertIs(di.Class(dict)(), dict)

    def test_call_object_provider(self):
        """Test Object provider call."""
        obj = object()
        self.assertIs(di.Object(obj)(), obj)

    def test_call_function_provider(self):
        """Test Function provider call."""
        self.assertIs(di.Function(map)(), map)

    def test_call_value_provider(self):
        """Test Value provider call."""
        self.assertEqual(di.Value(123)(), 123)

    def test_call_overridden_class_provider(self):
        """Test overridden Class provider call."""
        cls_provider = di.Class(dict)
        cls_provider.override(di.Object(list))
        self.assertIs(cls_provider(), list)

    def test_call_overridden_object_provider(self):
        """Test overridden Object provider call."""
        obj1 = object()
        obj2 = object()
        obj_provider = di.Object(obj1)
        obj_provider.override(di.Object(obj2))
        self.assertIs(obj_provider(), obj2)

    def test_call_overridden_function_provider(self):
        """Test overridden Function provider call."""
        function_provider = di.Function(len)
        function_provider.override(di.Function(sum))
        self.assertIs(function_provider(), sum)

    def test_call_overridden_value_provider(self):
        """Test overridden Value provider call."""
        value_provider = di.Value(123)
        value_provider.override(di.Value(321))
        self.assertEqual(value_provider(), 321)


class CallableTests(unittest.TestCase):

    """Callable test cases."""

    def example(self, arg1, arg2, arg3):
        """Example callback."""
        return arg1, arg2, arg3

    def setUp(self):
        """Set test cases environment up."""
        self.provider = di.Callable(self.example,
                                    arg1='a1',
                                    arg2='a2',
                                    arg3='a3')

    def test_init_with_not_callable(self):
        """Test creation of provider with not callable."""
        self.assertRaises(di.Error, di.Callable, 123)

    def test_is_provider(self):
        """Test `is_provider` check."""
        self.assertTrue(di.is_provider(self.provider))

    def test_call(self):
        """Test provider call."""
        self.assertEqual(self.provider(), ('a1', 'a2', 'a3'))

    def test_call_with_args(self):
        """Test provider call with kwargs priority."""
        provider = di.Callable(self.example,
                               arg3='a3')
        self.assertEqual(provider(1, 2), (1, 2, 'a3'))

    def test_call_with_kwargs_priority(self):
        """Test provider call with kwargs priority."""
        self.assertEqual(self.provider(arg1=1, arg3=3), (1, 'a2', 3))

    def test_call_overridden(self):
        """Test overridden provider call."""
        overriding_provider1 = di.Value((1, 2, 3))
        overriding_provider2 = di.Value((3, 2, 1))

        self.provider.override(overriding_provider1)
        self.provider.override(overriding_provider2)

        result1 = self.provider()
        result2 = self.provider()

        self.assertEqual(result1, (3, 2, 1))
        self.assertEqual(result2, (3, 2, 1))


class ConfigTests(unittest.TestCase):

    """Config test cases."""

    def setUp(self):
        """Set test cases environment up."""
        self.initial_data = dict(key='value',
                                 category=dict(setting='setting_value'))
        self.provider = di.Config(self.initial_data)

    def test_is_provider(self):
        """Test `is_provider` check."""
        self.assertTrue(di.is_provider(self.provider))

    def test_init_without_initial_value(self):
        """Test provider's creation with no initial value."""
        self.assertEqual(di.Config()(), dict())

    def test_call(self):
        """Test returning of config value."""
        self.assertEqual(self.provider(), self.initial_data)

    def test_update_from(self):
        """Test update of config value."""
        self.assertEqual(self.provider(), self.initial_data)

        self.initial_data['key'] = 'other_value'
        self.provider.update_from(self.initial_data)
        self.assertEqual(self.provider(), self.initial_data)

    def test_call_child(self):
        """Test returning of child config values."""
        category = self.provider.category
        category_setting = self.provider.category.setting

        self.assertTrue(di.is_provider(category))
        self.assertTrue(di.is_provider(category_setting))

        self.assertEqual(category(), self.initial_data['category'])
        self.assertEqual(category_setting(),
                         self.initial_data['category']['setting'])

    def test_call_deferred_child_and_update_from(self):
        """Test returning of deferred child config values."""
        self.provider = di.Config()
        category = self.provider.category
        category_setting = self.provider.category.setting

        self.assertTrue(di.is_provider(category))
        self.assertTrue(di.is_provider(category_setting))

        self.provider.update_from(self.initial_data)

        self.assertEqual(category(), self.initial_data['category'])
        self.assertEqual(category_setting(),
                         self.initial_data['category']['setting'])

    def test_call_deferred_child_with_empty_value(self):
        """Test returning of deferred child config values."""
        self.provider = di.Config()
        category_setting = self.provider.category.setting
        self.assertRaises(di.Error, category_setting)
