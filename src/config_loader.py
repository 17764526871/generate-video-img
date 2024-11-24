import configparser

def load_config(config_path):
    """
    加载配置文件。
    
    参数：
    config_path: 配置文件的路径
    
    返回：
    配置对象
    """
    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')
    return config
