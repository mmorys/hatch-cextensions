from hatchling.plugin import hookimpl

from hatch_cextensions.plugin import CExtensionBuildHook


@hookimpl
def hatch_register_build_hook():
    """Registers CExtensionBuildHook as a Hatch plugin.

    Returns:
        CExtensionBuildHook (type): BuildHookInterface class
    """
    return CExtensionBuildHook
