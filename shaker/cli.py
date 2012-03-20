from shaker.version import __version__

import optparse


def parse_cli():
    parser = optparse.OptionParser(
        usage="%prog [options] profile",
        version="%%prog %s" % __version__)
    parser.add_option(
        '-a', '--ami', dest='ec2_ami_id', metavar='AMI',
        help='Build instance from AMI')
    parser.add_option(
        '-d', '--distro', dest='distro',
        metavar='DISTRO', default='',
        help="Build minion (ubuntu, debian, squeeze, oneiric, etc.)")
    parser.add_option('--ec2-group', dest='ec2_security_group')
    parser.add_option('--ec2-key', dest='ec2_key_name')
    parser.add_option('--ec2-zone', dest='ec2_zone', default='')
    parser.add_option(
        '--config-dir', dest='config_dir',
        help="Configuration directory")
    parser.add_option(
        '--dry-run', dest='dry_run',
        action='store_true', default=False,
        help="Log the initialization setup, but don't launch the instance")
    parser.add_option(
        '--to-profile', dest='to_profile',
        default=False,
        help="Save options to a specified profile"
    )
    parser.add_option(
        '-m', '--master', dest='salt_master',
        metavar='SALT_MASTER', default='',
        help="Connect salt minion to SALT_MASTER")
    parser.add_option(
        '--hostname', dest='hostname',
        metavar='HOSTNAME', default='',
        help="Assign HOSTNAME to salt minion")
    parser.add_option(
        '--domain', dest='domain',
        metavar='DOMAIN', default='',
        help="Assign DOMAIN name to salt minion")
    import shaker.log
    parser.add_option('-l',
            '--log-level',
            dest='log_level',
            default='info',
            choices=shaker.log.LOG_LEVELS.keys(),
            help='Log level: %s.  \nDefault: %%default' %
                 ', '.join(shaker.log.LOG_LEVELS.keys())
            )
    (opts, args) = parser.parse_args()
    if len(args) < 1:
        if opts.ec2_ami_id or opts.distro:
            profile = None
        else:
            print parser.format_help().strip()
            errmsg = "\nError: Specify shaker profile or EC2 ami or distro"
            raise SystemExit(errmsg)
    else:
        profile = args[0]
    import shaker.config
    config_dir = shaker.config.get_config_dir(opts.config_dir)
    shaker.log.start_logger(
        __name__,
        os.path.join(config_dir, 'shaker.log'),
        opts.log_level)
    if opts.ec2_ami_id:
        opts.distro = ''  # mutually exclusive
    return opts, config_dir, profile
