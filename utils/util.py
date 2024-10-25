def user_input():
    info_input = ''
    while True:
        if info_input == '':
            # 第一次提示
            info_input = input('SQL> ')
        else:
            # 当输入不完整时，继续提示输入
            info_input += input('>>>> ')
        # 如果输入是 'exit;'，返回 None 表示退出
        if info_input.lower().strip() == 'exit;':
            return None
        if ';' in info_input:
            return info_input.strip()

