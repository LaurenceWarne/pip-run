import argparse
import pathlib
import hashlib


parser = argparse.ArgumentParser()
parser.add_argument(
    '-r',
    '--requirement',
    action='append',
    type=pathlib.Path,
    default=[],
)
parser.add_argument('package', nargs='*')


def cache_key(args):
    """
    Generate a cache key representing the packages to be installed.

    >>> reqs1, reqs2 = getfixture('reqs_files')
    >>> cache_key(['-r', str(reqs1), '--requirement', str(reqs2), 'requests'])
    '88d9f8a3a4009c1f685a7a724519bd5187e1227d72be6bc7f20a4a02f36d14b3'

    The key should be insensitive to order.

    >>> cache_key(['--requirement', str(reqs2), 'requests', '-r', str(reqs1)])
    '88d9f8a3a4009c1f685a7a724519bd5187e1227d72be6bc7f20a4a02f36d14b3'

    >>> cache_key(['--foo', '-q'])
    'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
    """
    parsed, unused = parser.parse_known_args(args)
    hash = hashlib.new('sha256')
    for req in sorted(parsed.package):
        hash.update(req.encode('utf-8') + b'\n')
    for file in sorted(parsed.requirement):
        hash.update(b'req:\n' + file.read_bytes())
    return hash.hexdigest()
