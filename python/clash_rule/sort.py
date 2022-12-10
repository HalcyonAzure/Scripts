# 一个规则有类似如下模式
# 例子：“IP-CIDR,43.129.81.65/32,🎯全球直连,no-resolve”
# 其中有四个部分，分别是：
# 1. 类型
# 2. IP地址或者域名
# 3. 策略组
# 4. 其他参数
# 对该规则进行抽象，创建一个Rule类
class Rule:
    def __init__(self, rule):
        self.rule = rule
        self.type = rule.split(',')[0]
        self.ip = rule.split(',')[1]
        self.group = rule.split(',')[2]
        self.other = rule.split(',')[3]

    def __repr__(self):
        return self.rule

# 从file_path读取文件，将文件中每一行规则转换为Rule类,存于一个列表中
# 要注意的是不是每一个规则都有其他参数，因此需要判断是否有三个逗号。
# 如果只有两个逗号则说明没有其他参数，其他参数的部分用空字符串代替
rules = []
with open("/home/halc/repo/scripts/clash_rule/rules.yaml", 'r') as f:
    lines = []
    repeat_lines_cnt = 0
    # 先将文件所有行读取到一个列表中，然后对列表进行去重
    for line in f.readlines():
        if line not in lines:
            lines.append(line)
        else:
            repeat_lines_cnt += 1
    for line in lines:
        if line.count(',') == 3:
            rules.append(Rule(line))
        elif line.count(',') == 2:
            rules.append(Rule(line.strip() + ','))
    print("除去的所有重复行数：", repeat_lines_cnt)


# 对列表中的规则进行去重
rules = list(set(rules))

# 对列表中的规则按域名进行排序
rules.sort(key=lambda x: x.ip)

repeat_cnt =0 
repeat_domain = []
# 检查去重后的规则是否有相同域名或IP的规则，如果有的话输出重复的域名名字，且只输出一次
for i in range(len(rules)):
    for j in range(i+1, len(rules)):
        if rules[i].ip == rules[j].ip:
            if rules[i].ip not in repeat_domain:
                repeat_domain.append(rules[i].ip)
                repeat_cnt += 1
                print(rules[i].ip)

print("重复的域名或IP有{}个".format(repeat_cnt))

# 将规则再次进行排序，这次以策略组优先，然后以域名或IP优先，最后以类型优先
rules.sort(key=lambda x: (x.group,x.other, x.ip, x.type))

# 将排序后以IP为顺序进行排序规则写入新文件，每个规则带一个换行
with open("/home/halc/repo/scripts/clash_rule/rules.yaml", 'w') as f:
    for rule in rules:
        f.write(str(rule))

# copilot, 帮我完成一个正则表达式
# 这个表达式要匹配以下两种类型字符串
# "DOMAIN-SUFFIX,youku.com,🌏国内媒体"
# "IP-CIDR,103.44.56.0/22,🌏国内媒体,no-resolve"
# 这个正则表达式的作用是在"🌏国内媒体"的emoji和中文之间插入一个空格，要匹配任意的emoji
# 这个表达式是：(?<=🌏国内媒体)(?=[\u4e00-\u9fa5])