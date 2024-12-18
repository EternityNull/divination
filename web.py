from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional, Tuple, Any
import random
from fortune_hexagram import HEXAGRAM_INFO
from datetime import datetime
import hashlib
import math

app = FastAPI(
    title="周易算卦API",
    description="基于周易六十四卦的算卦API服务",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头部
)

# 设置模板
templates = Jinja2Templates(directory="templates")

class DivinationRequest(BaseModel):
    question: Optional[str] = None
    name: Optional[str] = None

class DivinationResponse(BaseModel):
    hexagram: str
    name: str
    meaning: str
    description: str
    fortune: str
    yao_symbols: List[str]
    changing_lines: List[int]  # 变爻位置（1-6）
    future_hexagram: Optional[str] = None  # 变卦
    future_name: Optional[str] = None  # 变卦名称
    question: Optional[str] = None
    querent: Optional[str]

class ColorRequest(BaseModel):
    name: Optional[str] = None

class HeightRequest(BaseModel):
    height: float  # 输入的身高（厘米）

class HeightResponse(BaseModel):
    original_height: float  # 原始身高
    rounded_height: float  # 向上取整后的身高
    difference: float  # 差值

# 在 HEXAGRAM_INFO 后添加颜色对应关系
COLORS_INFO = {
    'red': {
        'name': '红色',
        'description': '象征热情、幸运、喜庆',
        'hex': '#FF0000',
        'elements': ['离', '震', '巽']  # 火、雷、风卦
    },
    'yellow': {
        'name': '黄色',
        'description': '象征智慧、稳重、中正',
        'hex': '#FFD700',
        'elements': ['坤', '艮', '乾']  # 地、山、天卦
    },
    'blue': {
        'name': '蓝色',
        'description': '象征智慧、冷静、深邃',
        'hex': '#0000FF',
        'elements': ['坎', '兑']  # 水、泽卦
    },
    'green': {
        'name': '绿色',
        'description': '象征生机、希望、成长',
        'hex': '#008000',
        'elements': ['巽', '震']  # 风、雷卦
    },
    'purple': {
        'name': '紫色',
        'description': '象征高贵、神秘、优雅',
        'hex': '#800080',
        'elements': ['乾', '坤']  # 天、地卦
    },
    'white': {
        'name': '白色',
        'description': '象征纯洁、清新、光明',
        'hex': '#FFFFFF',
        'elements': ['乾', '兑']  # 天、泽卦
    },
    'black': {
        'name': '黑色',
        'description': '象征神秘、稳重、内敛',
        'hex': '#000000',
        'elements': ['坎', '艮']  # 水、山卦
    }
}

class ColorResponse(BaseModel):
    color: str
    name: str
    description: str
    hex: str
    luck_index: int  # 幸运指数 1-100
    hexagram: str  # 对应的卦象
    hexagram_name: str  # 卦象名称

# 在其他import语句后添加
from typing import List, Dict, Optional, Tuple, Any

# 在COLORS_INFO后添加答案之书的回答列表
BOOK_ANSWERS = [
    "是的",
    "不是",
    "也许吧",
    "当然",
    "现在还不是时候",
    "需要等待",
    "不要执着",
    "放手去做",
    "相信自己",
    "再想想",
    "顺其自然",
    "不要犹豫",
    "保持耐心",
    "改变方向",
    "继续坚持",
    "是个好主意",
    "三思而行",
    "不要担心",
    "时机已到",
    "重新规划"
]

# 添加新的请求和响应模型
class AnswerBookRequest(BaseModel):
    question: str
    name: Optional[str] = None

class AnswerBookResponse(BaseModel):
    question: str
    answer: str
    confidence: int  # 确信度 0-100
    suggestion: str
    querent: Optional[str] = None

def cast_coin() -> Tuple[int, bool]:
    """
    模拟抛铜钱，返回爻值和是否为变爻
    返回: (爻值, 是否变爻)
    爻值: 1为阳，0为阴
    """
    # 模拟三枚铜钱
    coins = [random.choice([2, 3]) for _ in range(3)]  # 2代表反面，3代表正面
    total = sum(coins)
    
    # 确定爻的性质和变化
    if total == 6:  # 老阴，变阳
        return (0, True)
    elif total == 7:  # 少阳，不变
        return (1, False)
    elif total == 8:  # 少阴，不变
        return (0, False)
    else:  # total == 9，老阳，变阴
        return (1, True)

def cast_hexagram() -> Tuple[str, List[int], Optional[str]]:
    """
    生成一个六爻卦象
    返回: (当前卦象, 变爻位置列表, 变卦)
    """
    hexagram = ""
    changing_lines = []
    future_yao = []
    
    for i in range(6):
        yao, is_changing = cast_coin()
        hexagram += str(yao)
        if is_changing:
            changing_lines.append(i + 1)  # 记录变爻位置（1-6）
            future_yao.append(str(1 - yao))  # 阴变阳，阳变阴
        else:
            future_yao.append(str(yao))
    
    # 如果有变爻，生成变卦
    future_hexagram = "".join(future_yao) if changing_lines else None
    
    return hexagram, changing_lines, future_hexagram

def get_yao_symbols(hexagram: str, changing_lines: List[int] = None) -> List[str]:
    """将二进制卦象转换为易经符号"""
    yao_symbols = {
        '1': '━━━',  # 阳爻
        '0': '━  ━'   # 阴爻
    }
    
    result = []
    for i, yao in enumerate(hexagram):
        symbol = yao_symbols[yao]
        # 如果是变爻，添加变化标记 "○" 或 "×"
        if changing_lines and (i + 1) in changing_lines:
            symbol += ' ' + ('○' if yao == '0' else '×')
        result.append(symbol)
    
    return result

def get_color_recommendation(hexagram: str) -> tuple:
    """基于卦象推荐颜色"""
    hexagram_info = HEXAGRAM_INFO[hexagram]
    hexagram_name = hexagram_info['name']
    
    # 使用卦象生成一个稳定的随机数
    hash_obj = hashlib.md5(hexagram.encode())
    hash_value = int(hash_obj.hexdigest(), 16)
    
    # 获取所有可用颜色
    all_colors = list(COLORS_INFO.keys())
    
    # 获取与卦象属性匹配的颜色
    matching_colors = []
    for color, info in COLORS_INFO.items():
        if any(element in hexagram_name for element in info['elements']):
            matching_colors.append(color)
    
    # 使用第二个哈希值来增加随机性
    second_hash = hashlib.md5((hexagram + str(hash_value)).encode())
    second_hash_value = int(second_hash.hexdigest(), 16)
    
    # 调整颜色选择策略：
    # 1. 如果有匹配的颜色，60%概率从匹配颜色中选择
    # 2. 40%概率从所有颜色中平均选择
    if matching_colors and second_hash_value % 10 < 6:
        # 从匹配的颜色中选择
        color_index = hash_value % len(matching_colors)
        color = matching_colors[color_index]
    else:
        # 从所有颜色中平均选择
        # 使用第三个哈希来确保更均匀的分布
        third_hash = hashlib.md5((hexagram + str(second_hash_value)).encode())
        third_hash_value = int(third_hash.hexdigest(), 16)
        color_index = third_hash_value % len(all_colors)
        color = all_colors[color_index]
    
    # 生成幸运指数（40-100之间）
    # 使用不同的哈希值来计算幸运指数，避免与颜色选择相关
    luck_hash = hashlib.md5((hexagram + "luck").encode())
    luck_value = int(luck_hash.hexdigest(), 16)
    luck_base = 40
    luck_range = 60
    luck_index = luck_base + (luck_value % luck_range)
    
    return color, luck_index

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """返回主页"""
    return templates.TemplateResponse("index.html", {"request": request, "active_tab": "divination"})

@app.get("/divine", response_class=HTMLResponse)
async def divine_page(request: Request):
    """算卦页面"""
    return templates.TemplateResponse("index.html", {"request": request, "active_tab": "divination"})

@app.get("/color", response_class=HTMLResponse)
async def color_page(request: Request):
    """今日颜色页面"""
    return templates.TemplateResponse("index.html", {"request": request, "active_tab": "color"})

@app.get("/height", response_class=HTMLResponse)
async def height_page(request: Request):
    """身高计算页面"""
    return templates.TemplateResponse("index.html", {"request": request, "active_tab": "height"})

@app.get("/book", response_class=HTMLResponse)
async def book_page(request: Request):
    """答案之书页面"""
    return templates.TemplateResponse("index.html", {"request": request, "active_tab": "book"})

@app.post("/divine", response_model=DivinationResponse)
async def divine(request: DivinationRequest):
    """
    进行算卦
    - question: 求卦问题
    - name: 求卦者姓名（可选）
    """
    try:
        # 生成卦象
        hexagram, changing_lines, future_hexagram = cast_hexagram()
        
        # 获取当前卦象信息
        if hexagram not in HEXAGRAM_INFO:
            raise HTTPException(status_code=500, detail="无效的卦象")
        
        hexagram_info = HEXAGRAM_INFO[hexagram]
        yao_symbols = get_yao_symbols(hexagram, changing_lines)
        
        # 获取变卦信息
        future_name = None
        if future_hexagram and future_hexagram in HEXAGRAM_INFO:
            future_name = HEXAGRAM_INFO[future_hexagram]['name']
        
        return DivinationResponse(
            hexagram=hexagram,
            name=hexagram_info['name'],
            meaning=hexagram_info['meaning'],
            description=hexagram_info['description'],
            fortune=hexagram_info['fortune'],
            yao_symbols=yao_symbols,
            changing_lines=changing_lines,
            future_hexagram=future_hexagram,
            future_name=future_name,
            question=request.question,
            querent=request.name
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/hexagrams", response_model=Dict[str, dict])
async def get_all_hexagrams():
    """获取所有卦象信息"""
    return HEXAGRAM_INFO 

@app.post("/daily-color", response_model=ColorResponse)
async def get_daily_color(request: ColorRequest):
    """获取今日适合穿着的颜色推荐"""
    # 获取日期字符串
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 生成个性化种子
    seed = today
    if request.name:
        seed += request.name
    
    # 使用个性化种子生成哈希值
    hash_obj = hashlib.md5(seed.encode())
    hash_value = int(hash_obj.hexdigest(), 16)
    
    # 获取所有卦象键
    hexagram_keys = list(HEXAGRAM_INFO.keys())
    
    # 使用哈希值选择卦象
    index = hash_value % len(hexagram_keys)
    today_hexagram = hexagram_keys[index]
    
    # 获取颜色推荐
    recommended_color, luck_index = get_color_recommendation(today_hexagram)
    color_info = COLORS_INFO[recommended_color]
    
    return ColorResponse(
        color=recommended_color,
        name=color_info['name'],
        description=color_info['description'],
        hex=color_info['hex'],
        luck_index=luck_index,
        hexagram=today_hexagram,
        hexagram_name=HEXAGRAM_INFO[today_hexagram]['name']
    ) 

@app.post("/round-height", response_model=HeightResponse)
async def round_height(request: HeightRequest):
    """
    将身高向上取整到最接近的5厘米
    """
    original_height = request.height
    # 计算向上取整到最接近的5的倍数
    rounded_height = math.ceil(original_height / 10) * 10
    # 计算差值
    difference = rounded_height - original_height
    
    return HeightResponse(
        original_height=original_height,
        rounded_height=rounded_height,
        difference=difference
    ) 

@app.post("/book-of-answers", response_model=AnswerBookResponse)
async def get_book_answer(request: AnswerBookRequest):
    """获取答案之书的回答"""
    if not request.question:
        raise HTTPException(status_code=400, detail="问题不能为空")
        
    # 使用多个随机因素生成种子
    seed_factors = [
        str(random.randint(1, 1000000)),  # 随机数
        request.question,  # 问题本身
        str(random.choice([1, 2, 3, 4, 5])),  # 随机情绪因子
        str(random.choice(['阴', '阳', '动', '静', '变'])),  # 随机五行因子
    ]
    
    if request.name:
        seed_factors.append(request.name)
    
    # 组合所有因素生成种子
    seed = "-".join(seed_factors)
    
    # 生成哈希值
    hash_obj = hashlib.md5(seed.encode())
    hash_value = int(hash_obj.hexdigest(), 16)
    
    # 选择答案
    answer_index = hash_value % len(BOOK_ANSWERS)
    answer = BOOK_ANSWERS[answer_index]
    
    # 生成更有变化的确信度 (30-100)
    confidence = 30 + (hash_value % 71)
    
    # 根据不同的确信度范围生成更丰富的建议
    if confidence >= 90:
        suggestion = random.choice([
            "这个答案非常明确，你可以相信它。",
            "命运之书给出了一个非常确定的答案。",
            "这是一个极其清晰的指引。",
            "答案清晰如镜，不容置疑。"
        ])
    elif confidence >= 70:
        suggestion = random.choice([
            "这个答案值得参考。",
            "这个方向似乎是对的。",
            "你可以认真考虑这个建议。",
            "这个答案有很大的参考价值。"
        ])
    elif confidence >= 50:
        suggestion = random.choice([
            "这个答案供你参考，最终决定权在你。",
            "答案指明了一个可能的方向。",
            "建议结合实际情况来考虑这个答案。",
            "这是一个中肯的建议，可以认真思考。"
        ])
    else:
        suggestion = random.choice([
            "这个答案仅供参考，建议再想想。",
            "命运之书似乎也在思考这个问题。",
            "或许需要换个角度思考这个问题。",
            "这个答案需要你进一步思考。"
        ])
    
    return AnswerBookResponse(
        question=request.question,
        answer=answer,
        confidence=confidence,
        suggestion=suggestion,
        querent=request.name
    ) 