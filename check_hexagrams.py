from fortune_hexagram import HEXAGRAM_INFO

def check_hexagrams():
    # 生成所有可能的六位二进制组合
    all_possible = set()
    for i in range(64):
        binary = format(i, '06b')
        all_possible.add(binary)
    
    # 获取当前字典中的所有键
    current_keys = set(HEXAGRAM_INFO.keys())
    
    # 检查是否有遗漏的卦象
    missing = all_possible - current_keys
    if missing:
        print("遗漏的卦象：")
        for key in sorted(missing):
            print(f"'{key}',")
    
    # 检查是否有多余的卦象
    extra = current_keys - all_possible
    if extra:
        print("\n多余的卦象：")
        for key in sorted(extra):
            print(f"'{key}': {HEXAGRAM_INFO[key]},")
    
    # 检查是否有重复的卦名
    names = {}
    for key, value in HEXAGRAM_INFO.items():
        name = value['name']
        if name in names:
            print(f"\n重复的卦名 '{name}':")
            print(f"  {key}: {value}")
            print(f"  {names[name]}: {HEXAGRAM_INFO[names[name]]}")
        names[name] = key
    
    print(f"\n当前卦象数量：{len(current_keys)}")
    print(f"应有卦象数量：64")
    print(f"差异：{64 - len(current_keys)}")

if __name__ == "__main__":
    check_hexagrams() 