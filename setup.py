import sys

try:
    import twisted
except ImportError:
    raise SystemExit("twisted not found.  Make sure you "
                     "have installed the Twisted core package.")

from distutils.core import setup

def refresh_plugin_cache():
    from twisted.plugin import IPlugin, getPlugins
    list(getPlugins(IPlugin))

if __name__ == '__main__':
    
    if sys.version_info[:2] >= (2, 4):
        extraMeta = dict(
            classifiers=[
                "Development Status :: 4 - Beta",
                "Environment :: No Input/Output (Daemon)",
                "Programming Language :: Python",
            ])
    else:
        extraMeta = {}

    setup(
        name='multi-socks',
        version='0.1',
        description='SOCKSv4 proxy for servers with multiple IPs',
        author='Aivars Kalvans',
        author_email="aivars.kalvans@gmail.com",
        url="http://twistedmatrix.com/projects/core/documentation/howto/tutorial/index.html",
        packages=[
            "twisted.plugins",
        ],
        package_data={
            'twisted': ['plugins/multisocks_plugin.py'],
        },
        **extraMeta)
    
    refresh_plugin_cache()
