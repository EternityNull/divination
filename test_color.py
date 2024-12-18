from datetime import datetime, timedelta
import hashlib
from fortune_hexagram import HEXAGRAM_INFO
from web import COLORS_INFO, get_color_recommendation

def test_color_generation():
    """测试不同情况下的颜色生成"""
    
    # # 测试不同日期
    # print("\n=== 测试不同日期的颜色推荐 ===")
    # base_date = datetime.now()
    # for i in range(5):
    #     test_date = base_date + timedelta(days=i)
    #     date_str = test_date.strftime('%Y-%m-%d')
        
    #     # 不带姓名
    #     seed = date_str
    #     hash_obj = hashlib.md5(seed.encode())
    #     hash_value = int(hash_obj.hexdigest(), 16)
    #     hexagram_keys = list(HEXAGRAM_INFO.keys())
    #     index = hash_value % len(hexagram_keys)
    #     today_hexagram = hexagram_keys[index]
    #     color, luck_index = get_color_recommendation(today_hexagram)
        
    #     print(f"\n日期: {date_str}")
    #     print(f"卦象: {HEXAGRAM_INFO[today_hexagram]['name']}卦")
    #     print(f"颜色: {COLORS_INFO[color]['name']}")
    #     print(f"描述: {COLORS_INFO[color]['description']}")
    #     print(f"幸运指数: {luck_index}")
    
    # 测试不同姓名
    print("\n=== 测试不同姓名的颜色推荐 ===")
    test_names = [""]
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    for name in test_names:
        seed = date_str + name
        hash_obj = hashlib.md5(seed.encode())
        hash_value = int(hash_obj.hexdigest(), 16)
        hexagram_keys = list(HEXAGRAM_INFO.keys())
        index = hash_value % len(hexagram_keys)
        today_hexagram = hexagram_keys[index]
        color, luck_index = get_color_recommendation(today_hexagram)
        
        print(f"\n姓名: {name}")
        print(f"卦象: {HEXAGRAM_INFO[today_hexagram]['name']}卦")
        print(f"颜色: {COLORS_INFO[color]['name']}")
        print(f"描述: {COLORS_INFO[color]['description']}")
        print(f"幸运指数: {luck_index}")
    
    # # 测试颜色分布
    # print("\n=== 测试颜色分布统计 ===")
    # color_stats = {color: 0 for color in COLORS_INFO.keys()}
    # total_tests = 1000
    
    # for i in range(total_tests):
    #     seed = f"{date_str}test{i}"
    #     hash_obj = hashlib.md5(seed.encode())
    #     hash_value = int(hash_obj.hexdigest(), 16)
    #     hexagram_keys = list(HEXAGRAM_INFO.keys())
    #     index = hash_value % len(hexagram_keys)
    #     today_hexagram = hexagram_keys[index]
    #     color, _ = get_color_recommendation(today_hexagram)
    #     color_stats[color] += 1
    
    # print(f"\n在{total_tests}次测试中的颜色分布:")
    # for color, count in color_stats.items():
    #     percentage = (count / total_tests) * 100
    #     print(f"{COLORS_INFO[color]['name']}: {count}次 ({percentage:.1f}%)")

if __name__ == "__main__":
    test_color_generation() 