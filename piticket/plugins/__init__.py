import inspect
from pluggy import PluginManager
# Change only the name of the project here when using in another project
from piticket.plugins import hookspecs
from piticket.plugins.view_plugin import ViewPlugin
from piticket.plugins.printer_plugin import PrinterPlugin
from piticket.plugins.smartcard_plugin import SmartCardPlugin
from piticket.plugins.pay_terminal_plugin import PayTerminalPlugin 

def create_plugin_manager(project_name):
    plugin_manager = PiPluginManager(project_name)
    plugin_manager.add_hookspecs(hookspecs)
    return plugin_manager

class PiPluginManager(PluginManager):
    def __init__(self,*args,**kwargs):
        super(PiPluginManager,self).__init__(*args,**kwargs)
        self._plugin2calls = {}

        def before(hook_name, methods, kwargs):
            """Keep a list of already called hook per plugin to know 
            what plugin has already been initialized in case of hot-registration
            """
            for hookimpl in methods:
                self._plugin2calls[hookimpl.plugin].add(hook_name)

        def after(outcome, hook_name, methods, kwargs):
            pass

        self.add_hookcall_monitoring(before, after)

    def register(self, plugin, name=None):
        """Override to keep all plugins that have already been registered at least
        one time.
        """
        plugin_name = super(PiPluginManager, self).register(plugin, name)
        if plugin not in self._plugin2calls:
            self._plugin2calls[plugin] = set()
        return plugin_name 

    def load_all_plugins(self, paths, disabled=None):
        """Register the core plugins, load plugins from setuptools entry points
        and then load the given module/package paths.

        note:: by default hooks are called in LIFO registered order thus, plugins
               register order is important.

        :param paths: list of Python module/package paths to load
        :type paths: list
        :param disabled: list of plugins name to be disabled after loading
        :type disabled: list
        """
        # Load plugins declared by setuptools entry points
        self.load_setuptools_entrypoints(hookspecs.hookspec.project_name)
        plugins = []
        for path in paths:
            plugin = load_module(path)
            if plugin:
                LOGGER.debug("Plugin found at '%s",path)
                plugins.append(plugin)
            
        plugins += [ViewPlugin(self), # Last called
                    PrinterPlugin(self),
                    PayTerminalPlugin(self),
                    SmartCardPlugin(self)] # LIFO, First Called

        for plugin in plugins:
            self.register(plugin, name=getattr(plugin, '', None))

        # Check that each hookimpl is defined in the hookspec
        # except for hookimpl with kwarg 'optionalhook=True'.
        self.check_pending()

        # Disable unwanted plugins
        if disabled:
            for name in disabled:
                self.unregister(name=name)

    def list_external_plugins(self):
        """Return the list of loaded plugins except piticket core plugins.
        (External plugins can be registered or unregistered)
        :return: list of plugins
        :rtype: list
        """
        values = []
        for plugin in self._plugin2calls:
            # The core plugins are classes, we don't want to include
            # them here, thus we take only the modules objects.
            if inspect.ismodule(plugin):
                if plugin not in values:
                    values.append(plugin)
        return values 

    def get_friendly_name(self, plugin, version=True):
        """Return the friendly name of the given plugin and 
        optionally its version.
        :param plugin: registered plugin object
        :type plugin: object
        :param version: include the version number
        :type version:
        """
        distinfo = dict(self.list_plugin_distinfo())

        if plugin in distinfo:
            name = distinfo[plugin].project_name 
            vnumber = distinfo[plugin].version 
        else:
            name = self.get_name(plugin)
            if not name:
                name = getattr(plugin, '__name__', "unknown")
            vnumber = getattr(plugin, '__version__', '?.?.?')

        if version:
            name = "{}-{}".format(name, vnumber)
        else:
            name = "{}".format(name)

        # Questionable convinience, but it keeps things short
        if name.startswith("piticket-") or name.startswith("piticket_"):
            name = name[9:]

        return name  

    def get_calls_history(self, plugin):
        """ Return a list of the hook names that has already been called at least
        one time for the given name of the plugin.
        :param plugin: plugin for which calls history is required
        :type plugin: object
        """
        if plugin in self._plugin2calls:
            return list(self._plugin2calls[plugin])
        return []

    def subset_hook_caller_for_plugin(self, name, plugin):
        """Return a new :py:class:`.hooks._HookCaller` instance for the named
        method which manages calls to the given plugins.
        """
        excluded_plugins = [p for p in self.get_plugins() if self.get_name(plugin)]
        return self.subset_hook_caller(name, excluded_plugins)


