from openai import OpenAI
from colorama import Fore, Style
import os, yaml

# 读取 YAML 配置文件
def load_config():
    # 获取当前文件所在目录，拼接config.yaml路径（避免路径问题）
    config_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "config")), "config.yaml")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)  # safe_load避免安全风险
    except FileNotFoundError:
        raise ValueError(f"配置文件不存在：{config_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"配置文件格式错误：{e}")

config = load_config()
API_KEY = config["deepseek"]["api_key"]
# 这里以 DeepSeek 为例。如果是智谱，换成智谱的 base_url 和 model 即可
BASE_URL = config["deepseek"]["base_url"]
MODEL_NAME = config["deepseek"]["model_name"]

# 初始化客户端
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def diagnose_sql_error(sql_query, error_msg):
    """
    调用大模型对 SQL 报错进行智能诊断
    """
    prompt = f"""
    你是一个资深的数据库管理员(DBA)和友好的编程老师。
    用户输入了以下 SQL 语句，但我的 PyDB 数据库引擎报错了：
    
    【用户输入的 SQL】: {sql_query}
    【系统底层报错信息】: {error_msg}

    请你：
    1. 用一句简短、亲切的话向用户解释这个报错是什么意思（错在哪里）。
    2. 直接给出修改后的正确 SQL 语句。
    注意：不需要啰嗦的自我介绍，直接给出诊断结论。
    """
    
    try:
        # 友好的终端提示
        print(Fore.CYAN + "🤖 [AI DBA] 正在为您诊断错误，请稍候..." + Style.RESET_ALL)
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "你是一个有用的数据库助手。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3 # 降低发散度，保证回答的准确性
        )
        return response.choices[0].message.content
        
    except Exception as e:
        return f"AI 诊断模块通讯失败，请检查网络或 API Key 设置。({str(e)})"