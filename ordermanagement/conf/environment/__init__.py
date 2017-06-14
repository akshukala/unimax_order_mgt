CONFIG_MAP = {
    'prod': 'production',
    'dev': 'development',
    'local':'local'
}
def get_config(env):
    return '.'.join(['ordermanagement', 'conf', 'environment',
                     CONFIG_MAP.get(env, env), 'Config'])