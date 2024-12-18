import random

# 六十四卦的基本信息
HEXAGRAM_INFO = {
    '111111': {'name': '乾', 'meaning': '乾为天，刚健中正', 'description': '象征天行健，君子以自强不息。事业大吉，诸事顺遂。', 'fortune': '上上卦'},
    '000000': {'name': '坤', 'meaning': '坤为地，柔顺包容', 'description': '象征地势坤，君子以厚德载物。包容宽厚，利于守成。', 'fortune': '上卦'},
    '010001': {'name': '屯', 'meaning': '云雷屯，品行端正', 'description': '象征初始困难，但坚持必有所成。宜谋划开始。', 'fortune': '中卦'},
    '100010': {'name': '蒙', 'meaning': '山水蒙，启蒙教育', 'description': '启蒙之象，宜学习与请教。有所不明，需求教于人。', 'fortune': '中卦'},
    '111010': {'name': '需', 'meaning': '水天需，守正待时', 'description': '须等待时机，不可急进。静待时机，水到渠成。', 'fortune': '上卦'},
    '010111': {'name': '讼', 'meaning': '天水讼，慎争止争', 'description': '提防口舌是非，宜忍让避争。有争讼之象，宜和解。', 'fortune': '下卦'},
    '000010': {'name': '师', 'meaning': '地水师，整齐军旅', 'description': '团结一致，众志成城。宜组织、统筹，团结行动。', 'fortune': '上卦'},
    '010000': {'name': '比', 'meaning': '水地比，亲近比和', 'description': '与人亲近和睦，团结互助。宜结交朋友，合作共事。', 'fortune': '吉卦'},
    '111011': {'name': '小畜', 'meaning': '风天小畜，蓄养待进', 'description': '小有收获，循序渐进。宜稳健前进，不可冒进。', 'fortune': '中吉'},
    '110111': {'name': '履', 'meaning': '天泽履，谨慎而行', 'description': '脚踏实地，循规蹈矩。做事谨慎，按部就班。', 'fortune': '吉卦'},
    '111000': {'name': '泰', 'meaning': '地天泰，通达和顺', 'description': '大吉大利，诸事亨通。上下和谐，内外顺畅。', 'fortune': '上上卦'},
    '000111': {'name': '否', 'meaning': '天地否，闭塞不通', 'description': '运势不佳，诸事受阻。宜守不宜进，等待时机。', 'fortune': '下卦'},
    '111101': {'name': '同人', 'meaning': '天火同人，和睦共处', 'description': '与人和睦相处，同心协力。', 'fortune': '吉卦'},
    '101111': {'name': '大有', 'meaning': '火天大有，丰盛光明', 'description': '前途光明，万事亨通。', 'fortune': '上卦'},
    '000100': {'name': '谦', 'meaning': '地山谦，谦逊虚心', 'description': '谦虚谨慎，宜守不宜进。', 'fortune': '吉卦'},
    '001000': {'name': '豫', 'meaning': '雷地豫，顺势而为', 'description': '心情愉悦，万事如意。', 'fortune': '吉卦'},
    '011001': {'name': '随', 'meaning': '泽雷随，随遇而安', 'description': '随机应变，顺势而为。', 'fortune': '中卦'},
    '100110': {'name': '蛊', 'meaning': '山风蛊，振奋图强', 'description': '整顿纷乱，重新开始。', 'fortune': '中卦'},
    '110000': {'name': '临', 'meaning': '地泽临，临危不惧', 'description': '居高临下，洞察形势。', 'fortune': '吉卦'},
    '000011': {'name': '观', 'meaning': '风地观，观察入微', 'description': '观察形势，明察秋毫。', 'fortune': '中卦'},
    '101001': {'name': '噬嗑', 'meaning': '火雷噬嗑，雷厉风行', 'description': '果断决策，雷厉风行。', 'fortune': '吉卦'},
    '100101': {'name': '旅', 'meaning': '山火旅，行旅在外', 'description': '行旅在外，小心谨慎。守正待时。', 'fortune': '中卦'},
    '000001': {'name': '剥', 'meaning': '山地剥，剥极必复', 'description': '渐渐衰退，等待时机。', 'fortune': '下卦'},
    '100000': {'name': '复', 'meaning': '地雷复，否极泰来', 'description': '否极泰来，转危为。', 'fortune': '吉卦'},
    '111001': {'name': '无妄', 'meaning': '天雷无妄，无妄而得', 'description': '无而动，无往不利。', 'fortune': '吉卦'},
    '100111': {'name': '大过', 'meaning': '山天大过，勿逾越常规', 'description': '行事过度，需要节制。谨守分寸，不可逾越。', 'fortune': '下卦'},
    '100001': {'name': '颐', 'meaning': '山雷颐，修身养性', 'description': '修身养性，谨言慎行。', 'fortune': '吉卦'},
    '011110': {'name': '大壮', 'meaning': '雷天大壮，壮勿妄动', 'description': '势力强大，切勿妄动。谨慎行事，防止过刚。', 'fortune': '中卦'},
    '010010': {'name': '坎', 'meaning': '坎为水，险中求通', 'description': '险中有机，谨慎前行。', 'fortune': '中卦'},
    '101101': {'name': '离', 'meaning': '离为火，光明大治', 'description': '光明磊落，前途光明。', 'fortune': '上卦'},
    '001010': {'name': '解', 'meaning': '雷水解，解除困境', 'description': '冰雪消融，否极泰来。困境即将结束。', 'fortune': '吉卦'},
    '010100': {'name': '损', 'meaning': '山泽损，损益适中', 'description': '损一益二，取舍得当。适度取舍。', 'fortune': '中卦'},
    '001100': {'name': '益', 'meaning': '风雷益，利益增进', 'description': '利益增长，前途光明。诸事顺遂。', 'fortune': '吉卦'},
    '101100': {'name': '姤', 'meaning': '天风姤，遇而不合', 'description': '阴阳相遇，贵人相助。谨慎行事，把握机遇。', 'fortune': '中卦'},
    '001111': {'name': '大畜', 'meaning': '天山大畜，厚积薄发', 'description': '蓄养德行，厚积薄发。积蓄力量，待时而动。', 'fortune': '上卦'},
    '000110': {'name': '萃', 'meaning': '泽地萃，聚集会合', 'description': '群众聚集，众志成城。宜合作共事。', 'fortune': '吉卦'},
    '011000': {'name': '升', 'meaning': '地风升，循序渐进', 'description': '上升进步，稳步向前。循序渐进。', 'fortune': '吉卦'},
    '011010': {'name': '困', 'meaning': '泽水困，困境求通', 'description': '身处困境，需要耐心。守正待变。', 'fortune': '下卦'},
    '010110': {'name': '井', 'meaning': '水风井，循环不穷', 'description': '源源不断，生生不息。稳定发展。', 'fortune': '中卦'},
    '101110': {'name': '革', 'meaning': '火泽革，改革创新', 'description': '改革创新，除旧布新。变革维新。', 'fortune': '中卦'},
    '011100': {'name': '鼎', 'meaning': '火风鼎，稳重图变', 'description': '稳重图变，革故鼎新。变中求进。', 'fortune': '吉卦'},
    '001001': {'name': '震', 'meaning': '震为雷，震惊警觉', 'description': '雷霆万钧，警觉醒悟。行动迅速。', 'fortune': '中卦'},
    '110011': {'name': '艮', 'meaning': '艮为山，稳重止止', 'description': '稳重停止，不急不躁。宜守不宜进。', 'fortune': '中卦'},
    '110101': {'name': '渐', 'meaning': '风山渐，循序渐进', 'description': '循序渐进，稳扎稳打。按部就班。', 'fortune': '吉卦'},
    '001011': {'name': '归妹', 'meaning': '雷泽归妹，待时而动', 'description': '待时而动，柔顺应时。循序渐进。', 'fortune': '中卦'},
    '101011': {'name': '丰', 'meaning': '雷火丰，丰富盛大', 'description': '丰富盛大，万事亨通。但需谨慎。', 'fortune': '吉卦'},
    '111100': {'name': '同人', 'meaning': '天火同人，和同之象', 'description': '与人和睦相处，同心同德。团结一致，共创未来。', 'fortune': '吉卦'},
    '011011': {'name': '巽', 'meaning': '巽为风，谦逊顺从', 'description': '谦逊随和，顺势而为。宜进不宜守。', 'fortune': '吉卦'},
    '110110': {'name': '兑', 'meaning': '兑为泽，喜悦和顺', 'description': '喜悦和顺，与人和睦。诸事皆宜。', 'fortune': '吉卦'},
    '010011': {'name': '涣', 'meaning': '风水涣，分散解困', 'description': '分散消解，化险为夷。守正待时。', 'fortune': '中卦'},
    '110010': {'name': '节', 'meaning': '泽水节，节制调和', 'description': '节制调和，不过不及。守中持正。', 'fortune': '吉卦'},
    '010101': {'name': '中孚', 'meaning': '风泽中孚，诚信感通', 'description': '诚信感通，心心相印。守信践诺。', 'fortune': '吉卦'},
    '101010': {'name': '小过', 'meaning': '雷泽小过，行事谨慎', 'description': '小心谨慎，不可冒进。守成为宜。', 'fortune': '中卦'},
    '001110': {'name': '既济', 'meaning': '水火既济，成功在望', 'description': '大功告成，万事亨通。但需警惕，防止退转。', 'fortune': '上卦'},
    '110100': {'name': '未济', 'meaning': '火水未济，尚未成功', 'description': '事业未成，仍需努力。继续前进，终可成功。', 'fortune': '中卦'},
    '000101': {'name': '夬', 'meaning': '泽天夬，决断行事', 'description': '决断行事，刚柔交错。果断而行，无所顾忌。', 'fortune': '吉卦'},
    '001101': {'name': '明夷', 'meaning': '地火明夷，晦而转明', 'description': '处于晦暗，光明在前。守正待时，光明必至。', 'fortune': '中卦'},
    '011101': {'name': '贲', 'meaning': '山火贲，文明立身', 'description': '美化充实，文质彬彬。注重修养，以礼立身。', 'fortune': '吉卦'},
    '011111': {'name': '晋', 'meaning': '火地晋，日出光明', 'description': '如日方升，光明前进。顺势而为，前程似锦。', 'fortune': '吉卦'},
    '100011': {'name': '遁', 'meaning': '天山遁，遁世修身', 'description': '暂时退避，修身养性。韬光养晦，等待时机。', 'fortune': '中卦'},
    '100100': {'name': '咸', 'meaning': '山泽咸，感应相通', 'description': '心意相通，彼此感应。柔顺而感，无往不利。', 'fortune': '吉卦'},
    '101000': {'name': '遯', 'meaning': '天山遯，退避三舍', 'description': '暂时退避，韬光养晦。待机而动，终有所成。', 'fortune': '中卦'},
    '110001': {'name': '恒', 'meaning': '雷风恒，恒久不变', 'description': '持之以恒，永续不断。坚持不懈，必有所成。', 'fortune': '吉卦'},
    '111110': {'name': '睽', 'meaning': '火天睽，异中求同', 'description': '彼此乖离，异中求同。和而不同，终必团圆。', 'fortune': '中卦'}
}

# 爻位的基本含义
YAO_MEANINGS = {
    1: "初爻，位在最下，代表事情的开始或基础。",
    2: "二爻，位在下卦中间，代表内心或准备阶段。",
    3: "三爻，位在下卦最上，代表行动或转折点。",
    4: "四爻，位在上卦最下，代表外部环境或他人态度。",
    5: "五爻，位在上卦中间，代表目标或核心位置。",
    6: "上爻，位在最上，代表事情的结果或发展趋势。"
}

def generate_changing_yao():
    """
    生成单个爻，使用传统的方式：
    用三枚铜钱模拟，正面为3，背面为2
    三枚铜钱的和：
    6 = 老阳（变爻）：2+2+2 = 6
    7 = 少阳（不变）：2+2+3 或 2+3+2 或 3+2+2 = 7
    8 = 少阴（不变）：2+3+3 或 3+2+3 或 3+3+2 = 8
    9 = 老阴（变爻）：3+3+3 = 9
    """
    # 模拟投掷三枚铜钱，每枚铜钱正面(3)的概率是0.5，背面(2)的概率是0.5
    coins = [random.choice([2, 3]) for _ in range(3)]
    total = sum(coins)
    
    # 确定爻的性质
    is_changing = total in [6, 9]  # 6和9是变爻
    current_yao = 1 if total in [7, 9] else 0  # 7,9是阳爻，6,8是阴爻
    future_yao = 0 if total == 6 else 1 if total == 9 else current_yao
    
    return current_yao, future_yao, is_changing

def generate_hexagram():
    """生成完整的六爻卦象，包括变卦"""
    current_hexagram = []
    future_hexagram = []
    changing_positions = []
    
    for position in range(6):
        current, future, is_changing = generate_changing_yao()
        current_hexagram.append(current)
        future_hexagram.append(future)
        if is_changing:
            changing_positions.append(position + 1)
    
    return current_hexagram, future_hexagram, changing_positions

def interpret_yao_positions(changing_positions):
    """解释变爻的位置含义"""
    if not changing_positions:
        return "本卦无变爻，保持当前状态。"
    
    interpretations = ["变爻解释："]
    for pos in changing_positions:
        interpretations.append(f"第{pos}爻变：{YAO_MEANINGS[pos]}")
    return "\n".join(interpretations)

def get_hexagram_key(hexagram):
    """将卦象转换为字典键"""
    return ''.join(str(yao) for yao in hexagram)

def display_hexagram(hexagram):
    """显示卦象"""
    yao_symbols = {
        1: "━━━━━━",  # 阳爻
        0: "━━  ━━"   # 阴爻
    }
    
    # 从下往上示爻
    for yao in reversed(hexagram):
        print(yao_symbols[yao])

def interpret_hexagram(hexagram):
    """解释卦象的含义"""
    key = get_hexagram_key(hexagram)
    if key in HEXAGRAM_INFO:
        info = HEXAGRAM_INFO[key]
        print(f"\n此卦为：{info['name']}卦")
        print(f"卦义：{info['meaning']}")
        print(f"解释：{info['description']}")
        print(f"吉凶：{info['fortune']}")
    else:
        print("\n抱歉，未能找到该卦象的解释。")

def main():
    print("欢迎使用卜卦程序！")
    print("本程序基于周易六十四卦进行占卜")
    input("\n请静心，按回车键开始卜卦...")
    
    # 生成卦象
    current_hexagram, future_hexagram, changing_positions = generate_hexagram()
    
    # 显示和解释当前卦
    print("\n当前卦象：")
    display_hexagram(current_hexagram)
    current_key = get_hexagram_key(current_hexagram)
    
    if current_key in HEXAGRAM_INFO:
        info = HEXAGRAM_INFO[current_key]
        print(f"\n此卦为：{info['name']}卦")
        print(f"卦义：{info['meaning']}")
        print(f"解释：{info['description']}")
        print(f"吉凶：{info['fortune']}")
    
    # 显示变爻信息
    # print("\n" + interpret_yao_positions(changing_positions))
    
    # 如果有变爻，显示变卦
    if changing_positions:
        print("\n变卦为：")
        display_hexagram(future_hexagram)
        future_key = get_hexagram_key(future_hexagram)
        if future_key in HEXAGRAM_INFO:
            future_info = HEXAGRAM_INFO[future_key]
            print(f"\n变至：{future_info['name']}卦")
            print(f"变卦卦义：{future_info['meaning']}")
            print(f"变卦解释：{future_info['description']}")
            print(f"变卦吉凶：{future_info['fortune']}")

if __name__ == "__main__":
    main() 