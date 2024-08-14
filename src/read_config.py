import configparser

config = configparser.ConfigParser()
config.read('../settings.ini')


def get_hosts(section, option):
    string_hosts = config[section][option]
    string_hosts = string_hosts[1:-1]
    list_hosts = string_hosts.split("\n")
    return list_hosts

rc_osnov = get_hosts('hostnames', 'rc_osnov')
rc_reserv = get_hosts('hostnames', 'rc_reserv')
other_hosts = get_hosts('hostnames', 'other')
