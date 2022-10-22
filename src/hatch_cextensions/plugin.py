from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CExtensionBuildHook(BuildHookInterface):
    """Provides hook to run before Hatch package build to compile C Extensions using setuptools."""

    PLUGIN_NAME = "cextension"
