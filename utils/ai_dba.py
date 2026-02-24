from zhipuai import ZhipuAI
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
API_KEY = config["zhipu"]["api_key"]
MODEL_NAME = config["zhipu"]["model_name"]

# 初始化客户端
client = ZhipuAI(api_key=API_KEY)

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
    2. 不要分点回答。不要啰嗦，不要说任何废话。
    3. 写出正确的sql语句。如果你不确定正确的sql语句是什么，你就不要写。
    """
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "你是一个有用的数据库助手。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3, # 降低发散度，保证回答的准确性
            stream=True  # 开启流式传输
        )
        
        print(Fore.YELLOW + "[AI DBA 诊断建议]:" + Style.RESET_ALL, end=" ")
        
        full_content = ""
        # 🌟 循环读取数据块（Chunks）
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                print(Fore.YELLOW + content + Style.RESET_ALL, end="", flush=True)
                full_content += content
        print("") 
        return full_content
        
    except Exception as e:
        error_msg = f"\n AI 诊断模块通讯失败，请检查网络、API Key 或模型名称设置。\n详细报错: {str(e)}\n"
        print(Fore.RED + error_msg + Style.RESET_ALL)
        return error_msg