import streamlit as st
import streamlit.components.v1 as components
import random
import math
import zipfile
import io
import time
import itertools

# ==========================================
# ⚙️ ตั้งค่าหน้าเพจ Web App & CSS
# ==========================================
st.set_page_config(page_title="Math Competition Pro", page_icon="🏆", layout="wide")

st.markdown("""
<style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1200px; }
    div[data-testid="stSidebar"] div.stButton > button { background-color: #8e44ad; color: white; border-radius: 8px; height: 3.5rem; font-size: 18px; font-weight: bold; border: none; box-shadow: 0 4px 6px rgba(142,68,173,0.3); transition: all 0.3s ease;}
    div[data-testid="stSidebar"] div.stButton > button:hover { background-color: #732d91; transform: translateY(-2px); box-shadow: 0 6px 12px rgba(142,68,173,0.4); }
    div.stDownloadButton > button { border-radius: 8px; font-weight: bold; border: 1px solid #bdc3c7; }
    div.stDownloadButton > button:hover { border-color: #8e44ad; color: #8e44ad; }
    .main-header { background: linear-gradient(135deg, #2c3e50, #8e44ad); padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem; box-shadow: 0 10px 20px rgba(0,0,0,0.15); transition: background 0.5s ease; }
    .main-header.challenge { background: linear-gradient(135deg, #000000, #c0392b, #8e44ad); }
    .main-header h1 { margin: 0; font-size: 2.8rem; font-weight: 800; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
    .main-header p { margin: 10px 0 0 0; font-size: 1.2rem; opacity: 0.9; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🚀 Math Competition Pro <span style="font-size: 20px; background: #f1c40f; color: #333; padding: 5px 15px; border-radius: 20px; vertical-align: middle;">TMC Edition</span></h1>
    <p>ระบบสร้างข้อสอบแข่งขันคณิตศาสตร์ระดับชาติ (TMC) พร้อมระบบภาพอธิบายความเข้าใจ และเฉลยละเอียดยิบ</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 1. คลังคำศัพท์และฟังก์ชันตัวช่วย
# ==========================================
NAMES = ["อคิณ", "นาวิน", "ภูผา", "สายฟ้า", "เจ้านาย", "ข้าวหอม", "ใบบัว", "มะลิ", "น้ำใส", "ญาญ่า", "ปลื้ม", "พายุ", "ไออุ่น", "กะทิ"]
LOCS = ["โรงเรียน", "สวนสัตว์", "สวนสนุก", "ห้างสรรพสินค้า", "ห้องสมุด", "สวนสาธารณะ", "พิพิธภัณฑ์", "ลานกิจกรรม", "ค่ายลูกเสือ"]
ITEMS = ["ลูกแก้ว", "สติกเกอร์", "การ์ดพลัง", "โมเดลรถ", "ตุ๊กตาหมี", "สมุดระบายสี", "ดินสอสี", "ลูกโป่ง"]
SNACKS = ["ช็อกโกแลต", "คุกกี้", "โดนัท", "เยลลี่", "ขนมปัง", "ไอศกรีม", "น้ำผลไม้", "นมเย็น"]
PUBLISHERS = ["สำนักพิมพ์", "โรงพิมพ์", "ฝ่ายวิชาการ", "ร้านถ่ายเอกสาร", "ทีมงานจัดทำเอกสาร", "บริษัทสิ่งพิมพ์"]
DOC_TYPES = ["หนังสือนิทาน", "รายงานการประชุม", "แคตตาล็อกสินค้า", "เอกสารประกอบการเรียน", "สมุดภาพ", "นิตยสารรายเดือน", "พจนานุกรม"]
BUILDERS = ["บริษัทรับเหมา", "ผู้ใหญ่บ้าน", "เทศบาลตำบล", "เจ้าของโครงการ", "ผู้อำนวยการโรงเรียน", "กรมทางหลวง", "อบต."]
BUILD_ACTIONS = ["ปักเสาไฟ", "ปลูกต้นไม้", "ตั้งศาลาริมทาง", "ติดป้ายประกาศ", "ตั้งถังขยะ", "ปักธงประดับ", "ติดตั้งกล้องวงจรปิด"]
BUILD_LOCS = ["ริมถนนทางเข้าหมู่บ้าน", "เลียบคลองส่งน้ำ", "ริมทางเดินรอบสวน", "บนสะพานยาว", "สองข้างทางเข้างาน", "รอบรั้วโรงเรียน"]
CONTAINERS = ["กล่อง", "ถุงผ้า", "ตะกร้า", "ลังกระดาษ", "แพ็คพลาสติก"]
MATERIALS = ["แผ่นไม้", "กระดาษสี", "แผ่นพลาสติก", "ผืนผ้าใบ", "แผ่นเหล็ก", "แผ่นกระเบื้อง"]
VEHICLES = ["รถยนต์", "รถจักรยานยนต์", "รถบรรทุก", "รถไฟ", "รถตู้"]
WORK_ACTIONS = ["ทาสีบ้าน", "ปลูกต้นไม้", "สร้างกำแพง", "ประกอบหุ่นยนต์", "เก็บขยะ", "จัดหนังสือ"]
ANIMALS = ["แมงมุม", "มดแดง", "กบ", "จิ้งจก", "ตั๊กแตน", "เต่า", "หอยทาก"]

# คลังอิโมจิสำหรับโจทย์ตาชั่งสมดุลและสัตว์
ITEM_EMOJI_MAP = {
    "เพชร": "💎", "ทอง": "🟡", "เงิน": "⚪", "เหล็ก": "🪨", 
    "สิงโต": "🦁", "หมาป่า": "🐺", "จิ้งจอก": "🦊", "แมว": "🐱", 
    "ผลส้ม": "🍊", "แอปเปิล": "🍎", "สตรอว์เบอร์รี": "🍓", "องุ่น": "🍇", "แตงโม": "🍉"
}

box_html = "<span style='display:inline-block; width:24px; height:24px; border:2px solid #c0392b; border-radius:4px; vertical-align:middle; background-color:#fff;'></span>"

def get_vertical_fraction(num, den, color="#333", is_bold=True):
    weight = "bold" if is_bold else "normal"
    return f"""<span style="display:inline-flex; flex-direction:column; vertical-align:middle; text-align:center; line-height:1.4; margin:0 6px; font-family:'Sarabun', sans-serif; white-space:nowrap;"><span style="border-bottom:2px solid {color}; padding:2px 6px; font-weight:{weight}; color:{color};">{num}</span><span style="padding:2px 6px; font-weight:{weight}; color:{color};">{den}</span></span>"""

def get_vertical_math(top_chars, bottom_chars, result_chars, operator="+"):
    max_len = max(len(top_chars), len(bottom_chars), len(result_chars))
    t_pad = [""] * (max_len - len(top_chars)) + top_chars
    b_pad = [""] * (max_len - len(bottom_chars)) + bottom_chars
    r_pad = [""] * (max_len - len(result_chars)) + result_chars
    html = "<table style='border-collapse:collapse; font-size:26px; font-weight:bold; text-align:center; margin:15px 0 15px 40px;'><tr>"
    for c in t_pad: html += f"<td style='padding:5px 12px; width:35px;'>{c}</td>"
    html += f"<td rowspan='2' style='padding-left:20px; vertical-align:middle; font-size:28px; color:#2c3e50;'>{operator}</td></tr><tr>"
    for c in b_pad: html += f"<td style='padding:5px 12px; width:35px; border-bottom:2px solid #333;'>{c}</td>"
    html += "</tr><tr>"
    for c in r_pad: html += f"<td style='padding:5px 12px; width:35px; border-bottom:4px double #333;'>{c}</td>"
    html += "<td></td></tr></table>"
    return html

def lcm_multiple(*args):
    res = args[0]
    for i in args[1:]: res = abs(res * i) // math.gcd(res, i)
    return res

# ---------------------------------------------------------
# ฟังก์ชันวาดภาพประกอบ (SVG/HTML)
# ---------------------------------------------------------
def draw_rope_cutting_svg(layers, cuts):
    visual_layers = min(layers, 6)
    width = 300
    height = 50 + (visual_layers * 20) + 40
    svg = f'<div style="text-align:center; margin: 15px 0;"><svg width="{width}" height="{height}" style="background-color:#fafbfc; border-radius:8px; border:2px dashed #bdc3c7; padding:10px;">'
    svg += f'<text x="150" y="25" font-family="Sarabun" font-size="18" font-weight="bold" fill="#2c3e50" text-anchor="middle">เชือกพับทบ {layers} ชั้น</text>'
    start_y = 45
    layer_spacing = 20
    for i in range(visual_layers):
        y = start_y + (i * layer_spacing)
        svg += f'<line x1="30" y1="{y}" x2="270" y2="{y}" stroke="#e67e22" stroke-width="6" stroke-linecap="round"/>'
        if i == visual_layers - 2 and layers > 6:
            mid_y = y + (layer_spacing / 2)
            svg += f'<text x="150" y="{mid_y + 6}" font-family="sans-serif" font-size="20" font-weight="bold" fill="#d35400" text-anchor="middle">. . .</text>'
    cut_spacing = 240 / (cuts + 1)
    for i in range(1, cuts + 1):
        cx = 30 + i * cut_spacing
        end_y = start_y + (visual_layers - 1) * layer_spacing + 15
        svg += f'<line x1="{cx}" y1="35" x2="{cx}" y2="{end_y}" stroke="#e74c3c" stroke-width="3" stroke-dasharray="5,5"/>'
        svg += f'<text x="{cx}" y="32" font-family="sans-serif" font-size="16" fill="#e74c3c" text-anchor="middle">✂️</text>'
    svg += f'<text x="150" y="{height - 15}" font-family="Sarabun" font-size="16" font-weight="bold" fill="#c0392b" text-anchor="middle">1 รอยตัด ตัดผ่านเชือก {layers} เส้นพอดี!</text>'
    svg += '</svg></div>'
    return svg

def draw_well_svg(h, u, d):
    struggle_h = h - u
    svg = f'''<div style="text-align:center; margin: 15px 0;">
    <svg width="450" height="220" style="background-color:#fcfcfc; border: 1px dashed #bdc3c7; border-radius: 8px;">
        <line x1="140" y1="30" x2="140" y2="190" stroke="#34495e" stroke-width="4"/>
        <line x1="220" y1="30" x2="220" y2="190" stroke="#34495e" stroke-width="4"/>
        <line x1="140" y1="190" x2="220" y2="190" stroke="#34495e" stroke-width="4"/>
        <path d="M 120 30 L 110 30 L 110 190 L 120 190" fill="none" stroke="#7f8c8d" stroke-width="2"/>
        <text x="95" y="110" font-family="Sarabun" font-size="16" font-weight="bold" fill="#7f8c8d" text-anchor="middle" transform="rotate(-90, 95, 110)">ลึก {h} ม.</text>
        <rect x="142" y="30" width="76" height="40" fill="#d5f5e3" opacity="0.8"/>
        <rect x="142" y="70" width="76" height="118" fill="#fadbd8" opacity="0.5"/>
        <path d="M 240 30 L 230 30 L 230 70 L 240 70" fill="none" stroke="#27ae60" stroke-width="2"/>
        <text x="245" y="40" font-family="Sarabun" font-size="15" font-weight="bold" fill="#27ae60" text-anchor="start" dominant-baseline="middle">วันสุดท้าย: ปีนพ้นบ่อ ไม่ลื่นตกลงมา!</text>
        <text x="245" y="60" font-family="Sarabun" font-size="14" fill="#27ae60" text-anchor="start" dominant-baseline="middle">(ระยะก้าว = {u} เมตร)</text>
        <path d="M 240 70 L 230 70 L 230 190 L 240 190" fill="none" stroke="#c0392b" stroke-width="2"/>
        <text x="245" y="115" font-family="Sarabun" font-size="15" font-weight="bold" fill="#c0392b" text-anchor="start" dominant-baseline="middle">โซนที่ต้องทนปีนแล้วลื่นไถล</text>
        <text x="245" y="140" font-family="Sarabun" font-size="14" fill="#c0392b" text-anchor="start" dominant-baseline="middle">ระยะทาง = ลึกทั้งหมด - ระยะก้าววันสุดท้าย</text>
        <text x="245" y="160" font-family="Sarabun" font-size="14" fill="#c0392b" text-anchor="start" dominant-baseline="middle">ระยะทาง = {h} - {u} = {struggle_h} เมตร</text>
    </svg></div>'''
    return svg

def draw_balance_scale_html(item_L, qty_L, item_R, qty_R):
    emoji_L = ITEM_EMOJI_MAP.get(item_L, "📦")
    emoji_R = ITEM_EMOJI_MAP.get(item_R, "📦")
    left_content = "".join([f"<span style='font-size:35px; margin:0 2px;'>{emoji_L}</span>"] * qty_L)
    right_content = "".join([f"<span style='font-size:35px; margin:0 2px;'>{emoji_R}</span>"] * qty_R)
    html = f"""
    <div style="display: flex; align-items: center; justify-content: center; background: #fdfefe; border-radius: 12px; padding: 15px; margin: 15px auto; width: 85%; border: 3px solid #bdc3c7; box-shadow: inset 0 2px 5px rgba(0,0,0,0.05);">
        <div style="flex: 1; text-align: center; line-height: 1.2;">{left_content}</div>
        <div style="flex: 0 0 60px; text-align: center;">
            <div style="width: 100%; height: 6px; background-color: #2c3e50; border-radius: 3px;"></div>
            <div style="width: 0; height: 0; border-left: 15px solid transparent; border-right: 15px solid transparent; border-bottom: 20px solid #e74c3c; margin: 0 auto;"></div>
        </div>
        <div style="flex: 1; text-align: center; line-height: 1.2;">{right_content}</div>
    </div>
    """
    return html

# ==========================================
# 2. ฐานข้อมูลหัวข้อข้อสอบแข่งขัน (TMC 35 หัวข้อ)
# ==========================================
core_topics = [
    "การสร้างจำนวนจากเลขโดด", "โจทย์ปัญหาทำผิดเป็นถูก", "การนับตารางเรขาคณิต",
    "ปริศนาสมการช่องว่าง", "อสมการและค่าที่เป็นไปได้", "ปริศนาตัวเลขที่หายไป",
    "ความยาวและเส้นรอบรูป", "โจทย์ปัญหาเศษส่วนประยุกต์", "การคำนวณหน่วยและเวลา", "โจทย์ปัญหาเปรียบเทียบกลุ่ม",
    "อัตราส่วนอายุ", "การปักเสาและปลูกต้นไม้", "เส้นทางที่เป็นไปได้", "คะแนนยิงเป้า", 
    "การนับหน้าหนังสือ", "พื้นที่แรเงา (เรขาคณิต)", "จัดของใส่กล่อง (Modulo)", "วันที่และปฏิทิน"
]

comp_db = {
    "ระดับประถมต้น (ป.1 - ป.2)": core_topics + [
        "สัตว์ปีนบ่อ", "ตรรกะตาชั่งสมดุล", "ปัญหาผลรวม-ผลต่าง", 
        "แถวคอยแบบซ้อนทับ", "คิววงกลมมรณะ", "การคิดย้อนกลับ", "โปรโมชั่นแลกของ"
    ],
    "ระดับประถมกลาง (ป.3 - ป.4)": core_topics + [
        "สัตว์ปีนบ่อ", "ตรรกะตาชั่งสมดุล", "ปัญหาผลรวม-ผลต่าง", "แถวคอยแบบซ้อนทับ", 
        "คิววงกลมมรณะ", "ตรรกะการจับมือ (ทักทาย)", "โปรโมชั่นแลกของ", "หยิบของในที่มืด", 
        "การคิดย้อนกลับ", "แผนภาพความชอบ", "ผลบวกจำนวนเรียงกัน (Gauss)", "เศษส่วนของที่เหลือ"
    ],
    "ระดับประถมปลาย (ป.5 - ป.6)": core_topics + [
        "ตรรกะการจับมือ (ทักทาย)", "โปรโมชั่นแลกของ", "หยิบของในที่มืด", "แผนภาพความชอบ", 
        "ผลบวกจำนวนเรียงกัน (Gauss)", "การตัดเชือกพับทบ", "อายุข้ามเวลาขั้นสูง", 
        "ความเร็ววิ่งสวนทาง", "งานและเวลา (Work)", "ระฆังและไฟกะพริบ (ค.ร.น.)", 
        "เศษส่วนของที่เหลือ", "ปริศนาตัวเลขซ่อนแอบ", "นาฬิกาเดินเพี้ยน"
    ]
}

# ==========================================
# 3. Logic Generator 
# ==========================================
def generate_questions_logic(level, sub_t, num_q, is_challenge):
    questions = []
    seen = set()
    is_p12 = "ป.1" in level or "ป.2" in level
    is_p34 = "ป.3" in level or "ป.4" in level

    for _ in range(num_q):
        q, sol, attempts = "", "", 0
        while attempts < 500:
            attempts += 1
            actual_sub_t = random.choice(comp_db[level]) if sub_t == "🌟 สุ่มรวมทุกแนวแข่งขัน" else sub_t
            name = random.choice(NAMES)

            # ---------------------------------------------------------
            if actual_sub_t == "การสร้างจำนวนจากเลขโดด":
                if is_challenge:
                    digits = random.sample(range(1, 10), 5); max_prod = 0; best_pair = ()
                    for p in itertools.permutations(digits):
                        n1 = p[0]*100 + p[1]*10 + p[2]
                        n2 = p[3]*10 + p[4]
                        if n1 * n2 > max_prod: 
                            max_prod = n1 * n2; best_pair = (n1, n2)
                    sd = sorted(digits, reverse=True)
                    q = f"<b>{name}</b> ได้รับบัตรตัวเลข 5 ใบ คือ <b>{', '.join(map(str, digits))}</b> นำมาสร้างเป็น <b>จำนวน 3 หลัก</b> และ <b>จำนวน 2 หลัก</b> ที่คูณกันแล้วได้ <b>'ผลคูณที่มีค่ามากที่สุด'</b> ผลคูณนั้นคือเท่าไร?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: เรียงลำดับตัวเลขจากมากไปน้อย</b><br>👉 นำตัวเลขมาเรียงจะได้: {sd[0]} > {sd[1]} > {sd[2]} > {sd[3]} > {sd[4]}<br>
                    <b>ขั้นตอนที่ 2: จัดวางตัวเลข (หลักการคูณไขว้เพื่อรักษาสมดุล)</b><br>👉 เลขมากที่สุด ({sd[0]}) วางเป็นหลักสิบของตัวคูณ<br>👉 เลขมากรองลงมา ({sd[1]}) วางเป็นหลักร้อยของตัวตั้ง<br>👉 เลขอันดับสาม ({sd[2]}) วางเป็นหลักสิบของตัวตั้ง เพื่อไขว้กับ {sd[0]}<br>👉 เลขอันดับสี่ ({sd[3]}) วางเป็นหลักหน่วยของตัวคูณ<br>👉 เลขน้อยที่สุด ({sd[4]}) วางเป็นหลักหน่วยของตัวตั้ง<br>
                    <b>ขั้นตอนที่ 3: ประกอบร่างและหาผลคูณ</b><br>👉 ตัวเลข 2 จำนวนคือ {best_pair[0]} และ {best_pair[1]} ➔ นำมาคูณกัน: {best_pair[0]} × {best_pair[1]} = <b>{max_prod:,}</b><br>
                    <b>ตอบ: {max_prod:,}</b></span>"""
                else:
                    digits = random.sample(range(1, 10), 3 if is_p12 else 4)
                    max_v = int("".join(map(str, sorted(digits, reverse=True)))); min_v = int("".join(map(str, sorted(digits))))
                    q = f"มีบัตรตัวเลข <b>{', '.join(map(str, digits))}</b> จงหาผลต่างของจำนวนที่ <b>มากที่สุด</b> และ <b>น้อยที่สุด</b> ที่สร้างได้?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: สร้างจำนวนที่มากที่สุด</b><br>👉 นำตัวเลขมาเรียงจากมากไปน้อย จะได้ <b>{max_v}</b><br>
                    <b>ขั้นตอนที่ 2: สร้างจำนวนที่น้อยที่สุด</b><br>👉 นำตัวเลขมาเรียงจากน้อยไปมาก จะได้ <b>{min_v}</b><br>
                    <b>ขั้นตอนที่ 3: หาผลต่าง</b><br>👉 นำจำนวนที่มากที่สุดตั้ง ลบด้วยจำนวนที่น้อยที่สุด: {max_v} - {min_v} = <b>{max_v-min_v}</b><br>
                    <b>ตอบ: {max_v-min_v}</b></span>"""

            elif actual_sub_t == "โจทย์ปัญหาทำผิดเป็นถูก":
                A, B = random.randint(3, 8), random.randint(5, 20)
                if is_challenge:
                    X = random.randint(5, 12) * A; wrong_ans = (X // A) + B; correct_ans = (X * A) - B
                    f_q = get_vertical_fraction('ปริศนา', A); f_s = get_vertical_fraction('🔲', A, is_bold=False)
                    q = f"<b>{name}</b> ตั้งใจจะนำจำนวนปริศนาไป <b>คูณด้วย {A}</b> แล้ว <b>ลบออกด้วย {B}</b><br>แต่เขาทำผิดพลาด สลับไปเขียนในรูปเศษส่วนคือ <b>{f_q}</b> แล้วค่อย <b>บวกเพิ่ม {B}</b> ทำให้ได้ผลลัพธ์เป็น <b>{wrong_ans}</b><br>จงหาผลลัพธ์ที่แท้จริงตามความตั้งใจแรก?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (คิดย้อนกลับ):</b><br>
                    <b>ขั้นตอนที่ 1: จำลองสมการที่ทำผิดเพื่อหาตัวเลขเริ่มต้น</b><br>👉 สิ่งที่โจทย์ทำผิดคือ: {f_s} + {B} = {wrong_ans}<br>
                    <b>ขั้นตอนที่ 2: ใช้หลักการย้ายข้างสมการ</b><br>👉 ย้ายการบวกเป็นลบ: {wrong_ans} - {B} = {wrong_ans - B} (หมายความว่า {f_s} มีค่าเท่ากับ {wrong_ans - B})<br>👉 ย้ายเศษส่วน(การหาร)เป็นคูณ: นำ {wrong_ans - B} × {A} = {X}<br>👉 จะได้ 'จำนวนปริศนา' คือ <b>{X}</b><br>
                    <b>ขั้นตอนที่ 3: คิดเลขใหม่ให้ถูกต้องตามความตั้งใจแรก</b><br>👉 นำจำนวนปริศนาไปคูณ {A}: {X} × {A} = {X * A}<br>👉 นำผลลัพธ์ไปลบ {B}: {X * A} - {B} = <b>{correct_ans:,}</b><br>
                    <b>ตอบ: {correct_ans:,}</b></span>"""
                else:
                    x = random.randint(5, 20); ans_true = random.randint(30, 80); wrong_ans = ans_true - (2 * x)
                    while wrong_ans <= 0: 
                        ans_true += 10; wrong_ans = ans_true - (2 * x)
                    q = f"<b>{name}</b> ตั้งใจจะนำจำนวนหนึ่งไป <b>บวก</b> กับ {x} แต่เขาทำผิดโดยนำไป <b>ลบ</b> ด้วย {x} ทำให้ได้ผลลัพธ์เป็น <b>{wrong_ans}</b><br>ผลลัพธ์ที่แท้จริงคือเท่าไร?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: หาตัวเลขตั้งต้นก่อนทำผิด</b><br>👉 สมการที่ทำผิดคือ: 🔲 - {x} = {wrong_ans}<br>👉 ย้ายฝั่งเปลี่ยนลบเป็นบวก จะได้ตัวเลขตั้งต้น: {wrong_ans} + {x} = {wrong_ans+x}<br>
                    <b>ขั้นตอนที่ 2: คำนวณใหม่ให้ถูกต้องตามโจทย์สั่ง</b><br>👉 นำตัวเลขตั้งต้นไปบวก {x}: {wrong_ans+x} + {x} = <b>{ans_true}</b><br>
                    <b>ตอบ: {ans_true}</b></span>"""

            elif actual_sub_t == "การนับตารางเรขาคณิต":
                N, M = random.randint(3, 5), random.randint(4, 7)
                if N == M: M += 1
                if is_challenge:
                    total_rect = (N*(N+1)//2) * (M*(M+1)//2); total_sq = sum((N-i)*(M-i) for i in range(min(N, M)))
                    q = f"วาดตารางเป็นรูปสี่เหลี่ยมผืนผ้าขนาด <b>{N} × {M}</b> ช่อง จงหาว่ามี <b>'สี่เหลี่ยมผืนผ้าที่ไม่ใช่สี่เหลี่ยมจัตุรัส'</b> ซ่อนอยู่ทั้งหมดกี่รูป?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (วิเคราะห์แบบหักล้าง):</b><br>
                    สูตรหลัก: (จำนวนสี่เหลี่ยมผืนผ้าทั้งหมด) - (จำนวนสี่เหลี่ยมจัตุรัสทั้งหมด)<br>
                    <b>ขั้นตอนที่ 1: หาจำนวนสี่เหลี่ยมรวมทุกชนิด (สูตรนับผืนผ้า)</b><br>👉 ผลบวกแนวกว้าง: 1+2+...+{N} = {N*(N+1)//2}<br>👉 ผลบวกแนวยาว: 1+2+...+{M} = {M*(M+1)//2}<br>👉 นำมาคูณกัน: {N*(N+1)//2} × {M*(M+1)//2} = <b>{total_rect:,} รูป</b><br>
                    <b>ขั้นตอนที่ 2: หาจำนวนสี่เหลี่ยมจัตุรัสทั้งหมด</b><br>👉 ใช้สูตรลดทอนทีละ 1 แล้วคูณบวกกัน: ({N}×{M}) + ({N-1}×{M-1}) + ... ลดไปเรื่อยๆ จนถึง 1<br>👉 คำนวณผลรวมจะได้ทั้งหมด <b>{total_sq:,} รูป</b><br>
                    <b>ขั้นตอนที่ 3: หักล้างกัน</b><br>👉 นำ {total_rect:,} ลบ {total_sq:,} = <b>{total_rect - total_sq:,} รูป</b><br>
                    <b>ตอบ: {total_rect - total_sq:,} รูป</b></span>"""
                else:
                    grid = random.randint(2, 4) if is_p12 else random.randint(4, 6); ans = sum(i*i for i in range(1, grid+1))
                    q = f"มีตารางกระดานขนาด <b>{grid} × {grid}</b> ช่อง จงหาว่ามี <b>'สี่เหลี่ยมจัตุรัส'</b> ซ่อนอยู่ทั้งหมดกี่รูป?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: ใช้สูตรลัดนับตารางจัตุรัสสมมาตร</b><br>👉 ให้นำขนาดของตารางแต่ละตัวมายกกำลังสอง แล้วนำมาบวกกันตั้งแต่ 1² จนถึง {grid}²<br>
                    <b>ขั้นตอนที่ 2: คำนวณตัวเลข</b><br>👉 สมการ: 1² + 2² + ... + {grid}²<br>👉 ผลรวมทั้งหมดจะได้เท่ากับ <b>{ans:,} รูป</b><br>
                    <b>ตอบ: {ans:,} รูป</b></span>"""

            elif actual_sub_t == "ปริศนาสมการช่องว่าง":
                ans_v, B, C = random.randint(5, 20), random.randint(2, 10), random.randint(2, 5); V3 = ans_v + B
                if is_challenge:
                    while V3 % C != 0: 
                        ans_v += 1; V3 = ans_v + B
                    V2 = V3 // C; D = random.randint(1, V2 - 1) if V2 > 1 else 1; V1 = V2 - D if V2 > D else 1; A = random.randint(2, 6); E = A * V1
                    f_html = get_vertical_fraction(f'( 🔲 + {B} )', C)
                    q = f"จงหาตัวเลขที่เติมลงในช่องว่าง:<br><br><span style='font-size:24px; font-weight:bold;'>{A} × &nbsp;<span style='font-size:36px; vertical-align:middle;'>[</span>&nbsp; {f_html} &nbsp;−&nbsp; {D} &nbsp;<span style='font-size:36px; vertical-align:middle;'>]</span>&nbsp; =&nbsp; {E}</span>"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (ย้ายข้างสมการจากวงนอกสุดเข้าในสุด):</b><br>
                    <b>ขั้นตอนที่ 1: กำจัดเลขวงนอกสุดคือ "× {A}"</b><br>👉 ย้ายข้างไปฝั่งขวา เปลี่ยนคูณเป็นหาร: {E} ÷ {A} = <b>{V1}</b><br>
                    <b>ขั้นตอนที่ 2: กำจัดเลข "- {D}" ออกจากวงเล็บใหญ่</b><br>👉 ย้ายข้างไปฝั่งขวา เปลี่ยนลบเป็นบวก: {V1} + {D} = <b>{V2}</b><br>
                    <b>ขั้นตอนที่ 3: กำจัดส่วน "{C}" (ซึ่งหมายถึงการหาร)</b><br>👉 ย้ายข้างไปฝั่งขวา เปลี่ยนหารเป็นคูณ: {V2} × {C} = <b>{V3}</b><br>
                    <b>ขั้นตอนที่ 4: หาค่าตัวเลขใน 🔲</b><br>👉 ตอนนี้สมการเหลือแค่ 🔲 + {B} = {V3}<br>👉 ย้ายข้างบวกเป็นลบ: {V3} - {B} = <b>{ans_v}</b><br>
                    <b>ตอบ: {ans_v}</b></span>"""
                else:
                    a, b = random.randint(10, 50), random.randint(2, 9); ans_v = random.randint(5, 40); c = (ans_v + a) * b
                    q = f"จงหาตัวเลขที่เติมลงในช่องว่าง:<br><br><span style='font-size:24px; font-weight:bold;'>( 🔲 + {a} ) × {b} = {c}</span>"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: กำจัดตัวเลขนอกวงเล็บก่อน คือ "× {b}"</b><br>👉 นำ {b} ย้ายข้ามเครื่องหมายเท่ากับ จะเปลี่ยนเครื่องหมายจากคูณเป็นหาร: {c} ÷ {b} = <b>{c//b}</b><br>
                    <b>ขั้นตอนที่ 2: หาค่าของตัวเลขใน 🔲</b><br>👉 สมการจะเหลือแค่วงเล็บด้านในคือ: 🔲 + {a} = {c//b}<br>👉 นำ {a} ย้ายไปฝั่งขวา เปลี่ยนบวกเป็นลบ: {c//b} - {a} = <b>{ans_v}</b><br>
                    <b>ตอบ: {ans_v}</b></span>"""

            elif actual_sub_t == "อสมการและค่าที่เป็นไปได้":
                C = random.choice([2, 3, 4, 5]); ans_list = list(range(random.randint(5, 10), random.randint(12, 18)))
                min_v, max_v = ans_list[0], ans_list[-1]; B = random.randint(3, 8)
                if is_challenge:
                    A, D = (min_v * C) - random.randint(1, C-1), (max_v * C) + random.randint(1, C-1); ans = sum(ans_list)
                    f_L = get_vertical_fraction(A, B*C); f_M = get_vertical_fraction("🔲", B); f_R = get_vertical_fraction(D, B*C)
                    f_sol_M1 = get_vertical_fraction(f"🔲 × {C}", f"{B*C}", color="#2c3e50", is_bold=False)
                    q = f"จงหา <b>'ผลบวกของจำนวนนับทุกจำนวน'</b> ที่สามารถเติมในช่องว่างแล้วทำให้อสมการเป็นจริง:<br><br><span style='font-size:24px; font-weight:bold;'>{f_L} &nbsp;&lt;&nbsp; {f_M} &nbsp;&lt;&nbsp; {f_R}</span>"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (อสมการเศษส่วน):</b><br>
                    การจะเปรียบเทียบเศษส่วนได้ "ตัวส่วนด้านล่างต้องเท่ากัน" ทั้งหมดก่อนเสมอ!<br>
                    <b>ขั้นตอนที่ 1: ทำตัวส่วนให้เท่ากัน</b><br>👉 สังเกตว่าเศษส่วนตรงกลางมีส่วนเป็น {B} แต่ซ้ายและขวามีส่วนเป็น {B*C}<br>👉 ต้องนำเลข {C} มาคูณทั้งตัวเศษและตัวส่วนของก้อนกลาง จะได้เป็น {f_sol_M1}<br>
                    <b>ขั้นตอนที่ 2: เปรียบเทียบเฉพาะตัวเศษด้านบน</b><br>👉 เมื่อส่วนเท่ากันหมดแล้ว อสมการจะกลายเป็น: {A} &lt; 🔲 × {C} &lt; {D}<br>
                    <b>ขั้นตอนที่ 3: หาจำนวนนับที่เป็นไปได้</b><br>👉 ต้องหาว่ามีเลขอะไรที่คูณแม่ {C} แล้วมีผลลัพธ์อยู่ระหว่าง {A} ถึง {D}<br>👉 เลขที่สอดคล้องกับเงื่อนไขนี้คือ: {ans_list}<br>
                    <b>ขั้นตอนที่ 4: หาผลบวกตามที่โจทย์ถาม</b><br>👉 นำตัวเลขทั้งหมดมาบวกกัน: {' + '.join(map(str, ans_list))} = <b>{sum(ans_list)}</b><br>
                    <b>ตอบ: {sum(ans_list)}</b></span>"""
                else:
                    a = random.randint(10, 50); limit_val = random.randint(80, 150); max_val = limit_val - a - 1
                    q = f"จงหา <b>จำนวนนับที่มากที่สุด</b> ที่เติมในช่องว่าง:<br><br><span style='font-size:24px; font-weight:bold;'>🔲 + {a} &lt; {limit_val}</span>"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: คิดเสมือนว่ามันคือเครื่องหมาย "เท่ากับ" ก่อน</b><br>👉 ถ้าสมการคือ 🔲 + {a} = {limit_val} ➔ 🔲 จะเท่ากับ {limit_val} - {a} = {limit_val-a}<br>
                    <b>ขั้นตอนที่ 2: หาค่าที่มากที่สุดตามเงื่อนไขของอสมการ</b><br>👉 แต่โจทย์ระบุเครื่องหมาย <b>"ต้องน้อยกว่า"</b> {limit_val} <br>👉 ดังนั้นจำนวนนับที่มากที่สุดที่เป็นไปได้ คือการถอยค่าลงมา 1 แต้ม ➔ {limit_val-a} - 1 = <b>{max_val}</b><br>
                    <b>ตอบ: {max_val}</b></span>"""

            elif actual_sub_t == "ปริศนาตัวเลขที่หายไป":
                if is_challenge:
                    Z = random.randint(0, 4); C = random.randint(Z+3, 9); Y = random.randint(0, 4); B = random.randint(Y+3, 9); X = random.randint(5, 9); A = random.randint(1, X-3)
                    Res = int(f"{X}{Y}{Z}") - int(f"{A}{B}{C}"); str_Res = str(Res).zfill(3)
                    math_table = get_vertical_math([box_html, str(Y), str(Z)], [str(A), box_html, str(C)], [str_Res[0], str_Res[1], box_html], "−")
                    q = f"จงวิเคราะห์การตั้งลบแบบมีการยืมข้ามหลักต่อไปนี้ แล้วหาว่าตัวเลขที่ซ่อนอยู่ใน 🔲 จาก <b>บนลงล่าง</b> คือเลขใดตามลำดับ?<br>{math_table}"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (แกะรอยการยืมทีละหลัก):</b><br>
                    <b>ขั้นตอนที่ 1: วิเคราะห์หลักหน่วย (ขวาสุด)</b><br>👉 ตัวตั้งคือ {Z} ลบด้วย {C} ซึ่งลบไม่ได้ จึงต้องไปขอยืมหลักสิบมา 10<br>👉 จะกลายเป็น (10 + {Z}) - {C} = <b>{10+Z-C}</b> (นี่คือตัวเลขกล่องล่างสุด)<br>
                    <b>ขั้นตอนที่ 2: วิเคราะห์หลักสิบ (ตรงกลาง)</b><br>👉 เลข {Y} ถูกยืมไป 1 จึงเหลือเพียง {Y-1} แต่ผลลบยังคงน้อยกว่า 🔲 จึงต้องขอยืมหลักร้อยมาอีก 10<br>👉 จะได้สมการ: (10 + {Y-1}) - 🔲 = {str_Res[1]} ➔ นำ {(10+Y-1)} ลบ {str_Res[1]} จะได้กล่องกลางคือ <b>{B}</b><br>
                    <b>ขั้นตอนที่ 3: วิเคราะห์หลักร้อย (ซ้ายสุด)</b><br>👉 เลข 🔲 ถูกหลักสิบยืมไป 1 จึงมีค่าลดลงไป 1<br>👉 จะได้สมการ: (🔲 - 1) - {A} = {str_Res[0]} ➔ ย้ายข้าง 🔲 = {int(str_Res[0])} + {A} + 1 = <b>{X}</b> (นี่คือตัวเลขกล่องบนสุด)<br>
                    <b>ตอบ: กล่องบนคือ {X}, กล่องกลางคือ {B}, กล่องล่างคือ {10+Z-C}</b></span>"""
                else:
                    n2 = random.randint(2, 9); n1 = random.randint(11, 99); ans_val = n1 * n2; str_n1, str_ans = str(n1), str(ans_val)
                    math_table = get_vertical_math([str_n1[0], box_html], [str(n2)], list(str_ans), "×")
                    q = f"จงเติมตัวเลขลงใน 🔲 ให้การคูณนี้ถูกต้อง<br>{math_table}"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: แปลงตารางเป็นสมการแนวนอน</b><br>👉 จากการตั้งคูณ หมายความว่า (จำนวนสองหลักด้านบน) × {n2} = {ans_val}<br>
                    <b>ขั้นตอนที่ 2: ใช้หลักการย้ายข้างสมการเพื่อหาจำนวนนั้น</b><br>👉 ย้าย {n2} ที่กำลังคูณอยู่ ข้ามฝั่งไปเป็นหาร: {ans_val} ÷ {n2} = <b>{n1}</b><br>
                    <b>ขั้นตอนที่ 3: เทียบหาตัวเลขที่หายไป</b><br>👉 จำนวนสองหลักที่คำนวณได้คือ {n1} เมื่อนำไปเทียบกับตาราง ตัวเลขที่หายไปในหลักหน่วยคือ <b>{str_n1[1]}</b><br>
                    <b>ตอบ: {str_n1[1]}</b></span>"""

            elif actual_sub_t == "ตรรกะตาชั่งสมดุล":
                items_pair = [("เพชร", "ทอง", "เงิน", "เหล็ก"), ("สิงโต", "หมาป่า", "จิ้งจอก", "แมว"), ("ผลส้ม", "แอปเปิล", "สตรอว์เบอร์รี", "องุ่น")]
                i1, i2, i3, i4 = random.choice(items_pair)
                
                if is_challenge:
                    m1 = 2; m2 = random.randint(2, 3); m3 = random.randint(2, 3); q_mul = random.randint(2, 3)
                    ans = m1 * m2 * m3 * q_mul
                    
                    s1_html = draw_balance_scale_html(i1, 1, i2, m1)
                    s2_html = draw_balance_scale_html(i2, 1, i3, m2)
                    s3_html = draw_balance_scale_html(i3, 1, i4, m3)
                    
                    q = f"ตาชั่งสมดุล 3 ตัว ให้ข้อมูลดังภาพต่อไปนี้:<br>{s1_html}{s2_html}{s3_html}<br>อยากทราบว่า <b>{i1} จำนวน {q_mul} อัน</b> จะมีน้ำหนักสมดุลเท่ากับ <b>{i4}</b> กี่อัน?"
                    
                    sol_s1 = draw_balance_scale_html(i1, 1, i3, m1*m2)
                    sol_s2 = draw_balance_scale_html(i1, 1, i4, m1*m2*m3)
                    sol_s3 = draw_balance_scale_html(i1, q_mul, i4, ans)
                    
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (การแทนค่า 3 ชั้น):</b><br>
                    <b>ขั้นตอนที่ 1: แทนค่าตาชั่งที่ 1 ลงในตาชั่งที่ 2</b><br>
                    👉 เมื่อนำ {i3} ไปแทนที่ {i2} จะได้: 1 × {m1} × {m2} = <b>{m1*m2} {i3}</b><br>{sol_s1}
                    <b>ขั้นตอนที่ 2: แทนค่าต่อไปยังตาชั่งที่ 3</b><br>
                    👉 เมื่อนำ {i4} ไปแทนที่ {i3} จะได้: {m1*m2} × {m3} = <b>{m1*m2*m3} {i4}</b><br>{sol_s2}
                    <b>ขั้นตอนที่ 3: หาคำตอบตามที่โจทย์ถาม</b><br>
                    👉 โจทย์ถามหา {i1} {q_mul} อัน ➔ นำปริมาณ {i4} ไปคูณ {q_mul} <br>
                    👉 จะได้: {m1*m2*m3} × {q_mul} = <b>{ans} อัน</b><br>{sol_s3}
                    <b>ตอบ: {ans} อัน</b></span>"""
                else:
                    m1 = 2 if is_p12 else (random.randint(3, 5) if is_p34 else random.randint(4, 8))
                    m2 = 2 if is_p12 else (random.randint(3, 5) if is_p34 else random.randint(4, 8))
                    q_mul = 1 if is_p12 else (2 if is_p34 else random.randint(3, 4))
                    ans = m1 * m2 * q_mul
                    
                    s1_html = draw_balance_scale_html(i1, 1, i2, m1)
                    s2_html = draw_balance_scale_html(i2, 1, i3, m2)
                    
                    q = f"ตาชั่งสมดุล 2 ตัว ให้ข้อมูลดังภาพต่อไปนี้:<br>{s1_html}{s2_html}<br>อยากทราบว่า <b>{i1} จำนวน {q_mul} ชิ้น</b> จะมีน้ำหนักสมดุลเท่ากับ <b>{i3}</b> กี่ชิ้น?"
                    
                    sol_s1 = draw_balance_scale_html(i1, 1, i3, m1*m2)
                    sol_s2 = draw_balance_scale_html(i1, q_mul, i3, ans)
                    
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: แทนค่าสิ่งของข้ามตาชั่ง (หาความสัมพันธ์โดยตรง)</b><br>
                    👉 นำ {i3} ไปวางแทนที่ {i2} ในตาชั่งแรก<br>
                    👉 จะได้ความสมดุลใหม่: {i1} 1 ชิ้น = {m1} × {m2} = <b>{m1 * m2} ชิ้น (ของ {i3})</b><br>{sol_s1}
                    <b>ขั้นตอนที่ 2: หาคำตอบตามจำนวนที่โจทย์ถาม</b><br>
                    👉 โจทย์ถามหา {i1} จำนวน {q_mul} ชิ้น ➔ ให้นำความสัมพันธ์ไปคูณด้วย {q_mul}<br>
                    👉 จะได้: {m1 * m2} × {q_mul} = <b>{ans} ชิ้น</b><br>{sol_s2}
                    <b>ตอบ: {ans} ชิ้น</b></span>"""

            elif actual_sub_t == "ปัญหาผลรวม-ผลต่าง":
                n1, n2, n3 = random.sample(NAMES, 3)
                itm = random.choice(ITEMS)
                if is_challenge:
                    a = random.randint(30, 50)
                    b = a + random.randint(10, 20)
                    c = b + random.randint(10, 20)
                    total = a + b + c
                    diff_bc = c - b
                    diff_ac = c - a
                    
                    q = f"<b>{n1}, {n2}, และ {n3}</b> มี<b>{itm}</b>รวมกัน <b>{total}</b> ชิ้น <br>ถ้า <b>{n3}</b> มีมากกว่า <b>{n2}</b> อยู่ <b>{diff_bc}</b> ชิ้น และ <b>{n3}</b> มีมากกว่า <b>{n1}</b> อยู่ <b>{diff_ac}</b> ชิ้น <br>จงหาว่า <b>{n3} (คนที่มีเยอะที่สุด)</b> มีกี่ชิ้น?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (การปรับให้เท่ากัน 3 คน):</b><br>
                    เทคนิคคือ สมมติให้ทุกคนมีของเท่ากับ {n3} (คนที่มากที่สุด) เพื่อให้ตั้งหารได้ง่ายๆ!<br>
                    <b>ขั้นตอนที่ 1: เติมของในจินตนาการให้คนที่ขาด</b><br>
                    👉 ต้องเติมของให้ {n1} จำนวน {diff_ac} ชิ้น และเติมให้ {n2} จำนวน {diff_bc} ชิ้น เพื่อให้ทุกคนมีปริมาณเท่ากับ {n3}<br>
                    <b>ขั้นตอนที่ 2: หายอดรวมสมมติใหม่</b><br>
                    👉 ยอดเดิม {total} + เติมให้ {n1} ({diff_ac}) + เติมให้ {n2} ({diff_bc}) = <b>{total+diff_ac+diff_bc} ชิ้น</b><br>
                    👉 ในสถานการณ์จำลองนี้ ทุกคนมีของเท่ากับ {n3} เป๊ะๆ ทั้ง 3 คนแล้ว!<br>
                    <b>ขั้นตอนที่ 3: หาจำนวนของ {n3}</b><br>
                    👉 นำยอดรวมสมมติมาแบ่ง 3 ส่วนเท่าๆ กัน: {total+diff_ac+diff_bc} ÷ 3 = <b>{c} ชิ้น</b><br>
                    <b>ตอบ: {c} ชิ้น</b></span>"""
                else:
                    small = random.randint(10, 20) if is_p12 else (random.randint(50, 150) if is_p34 else random.randint(500, 1500))
                    diff = random.randint(5, 10) if is_p12 else (random.randint(20, 50) if is_p34 else random.randint(100, 300))
                    large = small + diff
                    total = large + small
                    
                    q = f"<b>{n1}</b> และ <b>{n2}</b> มี<b>{itm}</b>รวมกัน <b>{total}</b> ชิ้น หาก <b>{n1}</b> มีมากกว่า <b>{n2}</b> อยู่ <b>{diff}</b> ชิ้น จงหาว่า <b>{n1}</b> มีกี่ชิ้น?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: หักส่วนที่ต่างกันทิ้งไปก่อน</b><br>
                    👉 นำของทั้งหมด หักส่วนที่ {n1} มีเกินมาออกไป: {total} - {diff} = <b>{total - diff} ชิ้น</b><br>
                    👉 ตอนนี้ของที่เหลือ จะเป็นของที่สามารถแบ่งให้สองคนได้เท่าๆ กันพอดี<br>
                    <b>ขั้นตอนที่ 2: แบ่งของออกเป็น 2 ส่วนเท่าๆ กัน</b><br>
                    👉 นำไปแบ่งครึ่ง (จะได้เป็นปริมาณของคนที่มีน้อยกว่า): ({total - diff}) ÷ 2 = <b>{small} ชิ้น</b><br>
                    <b>ขั้นตอนที่ 3: หาของของคนที่มีมากกว่า ({n1})</b><br>
                    👉 นำปริมาณที่แบ่งได้ ไปบวกส่วนที่หักทิ้งคืนกลับมาให้ {n1}: {small} + {diff} = <b>{large} ชิ้น</b><br>
                    <b>ตอบ: {large} ชิ้น</b></span>"""

            elif actual_sub_t == "แถวคอยแบบซ้อนทับ":
                n1, n2 = random.sample(NAMES, 2)
                loc = random.choice(LOCS)
                if is_challenge:
                    overlap = random.randint(3, 10)
                    total_people = random.randint(50, 100)
                    sum_pos = total_people + overlap
                    front_pos = random.randint(overlap + 5, total_people - 5)
                    back_pos = sum_pos - front_pos
                    ans = overlap - 2
                    
                    q = f"นักเรียนเข้าแถวรอเข้า<b>{loc}</b> มีคนทั้งหมด <b>{total_people}</b> คน<br>ถ้า <b>{n1}</b> ยืนลำดับที่ <b>{front_pos}</b> นับจากหัวแถว และ <b>{n2}</b> ยืนลำดับที่ <b>{back_pos}</b> นับจากท้ายแถว <br>มีคนยืนอยู่ระหว่าง <b>{n1}</b> กับ <b>{n2}</b> กี่คน? <br><span style='font-size:16px; color:#7f8c8d;'>(คำใบ้: ระวังการนับซ้อนทับกัน)</span>"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (ระวังแถวเหลื่อมทับกัน):</b><br>
                    <b>ขั้นตอนที่ 1: ตรวจสอบการซ้อนทับกันของแถว</b><br>
                    👉 นำลำดับคนที่นับจากหัวและนับจากท้ายมาบวกกัน: {front_pos} + {back_pos} = <b>{sum_pos} คน</b><br>
                    👉 จะพบว่าผลบวก 'เกิน' จำนวนคนทั้งหมดที่มีจริง ({total_people} คน) แสดงว่าพวกเขายืน <b>'ไขว้ทับกัน'</b> ไปแล้ว!<br>
                    <b>ขั้นตอนที่ 2: หาจำนวนคนที่ถูกนับเบิ้ล (Overlap)</b><br>
                    👉 นำผลบวกไปลบจำนวนคนทั้งหมด = {sum_pos} - {total_people} = <b>{overlap} คน</b> (ยอดนี้คือคนที่ถูกนับซ้ำ ซึ่งรวม {n1} และ {n2} ไปด้วย)<br>
                    <b>ขั้นตอนที่ 3: หักตัวละครหลักออกเพื่อหาคนตรงกลาง</b><br>
                    👉 เราต้องการหาคน 'ระหว่างกลาง' จึงต้องหัก {n1} และ {n2} ทิ้งออกไปจากกลุ่มที่ทับกัน: {overlap} - 2 = <b>{ans} คน</b><br>
                    <b>ตอบ: {ans} คน</b></span>"""
                else:
                    front_pos = random.randint(5, 10) if is_p12 else (random.randint(15, 30) if is_p34 else random.randint(40, 80))
                    back_pos = random.randint(5, 10) if is_p12 else (random.randint(15, 30) if is_p34 else random.randint(40, 80))
                    total_people = front_pos + back_pos + random.randint(5, 15)
                    between = total_people - (front_pos + back_pos)
                    
                    q = f"นักเรียนเข้าแถว มีคนทั้งหมด <b>{total_people}</b> คน<br>ถ้า <b>{n1}</b> ยืนลำดับที่ <b>{front_pos}</b> จากหัวแถว และ <b>{n2}</b> ลำดับที่ <b>{back_pos}</b> จากท้ายแถว <br>มีคนยืนอยู่ระหว่าง 2 คนนี้กี่คน? (กำหนดให้ {n1} ยืนหน้า {n2})"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: หาจำนวนคนในกลุ่มด้านหน้าและด้านหลัง</b><br>
                    👉 กลุ่มด้านหน้ามีตั้งแต่หัวแถวจนถึง {n1} = {front_pos} คน<br>
                    👉 กลุ่มด้านหลังมีตั้งแต่ท้ายแถวจนถึง {n2} = {back_pos} คน<br>
                    <b>ขั้นตอนที่ 2: หักกลุ่มหน้าและกลุ่มหลังออกจากยอดรวมทั้งหมด</b><br>
                    👉 นำคนทั้งหมด ลบด้วยกลุ่มทั้งสองออกไป จะเหลือแต่คนตรงกลาง<br>
                    👉 คำนวณ: {total_people} - ({front_pos} + {back_pos}) = <b>{between} คน</b><br>
                    <b>ตอบ: {between} คน</b></span>"""

            elif actual_sub_t == "คิววงกลมมรณะ":
                n1, n2, n3 = random.sample(NAMES, 3)
                if is_challenge:
                    n_half = random.randint(15, 30)
                    total = n_half * 2
                    pos1 = random.randint(1, n_half)
                    pos2 = pos1 + n_half
                    add_pos = random.randint(3, 8)
                    pos3 = (pos2 + add_pos) % total
                    if pos3 == 0: pos3 = total
                    
                    q = f"เด็กยืนล้อมเป็นวงกลมเว้นระยะห่างเท่าๆ กัน นับหมายเลข 1, 2, 3... <br>ถ้า <b>{n1}</b> หมายเลข <b>{pos1}</b> มองตรงไปฝั่งตรงข้ามพอดี พบ <b>{n2}</b> หมายเลข <b>{pos2}</b> <br>และถ้า <b>{n3}</b> ยืนอยู่ถัดจาก {n2} ไปทางซ้ายมือ (นับเพิ่มขึ้น) อีก <b>{add_pos} คน</b><br>จงหาว่าเด็กกลุ่มนี้มีทั้งหมดกี่คน และ <b>{n3}</b> คือหมายเลขใด?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>1) หาจำนวนคนทั้งหมดจากรหัสฝั่งตรงข้าม</b><br>
                    👉 ระยะห่างระหว่างสองคนที่ยืนอยู่ฝั่งตรงข้ามกัน คือ 'ครึ่งวงกลม' เสมอ<br>
                    👉 หาคนครึ่งวงกลม = นำเบอร์มาลบกัน ➔ {pos2} - {pos1} = <b>{n_half} คน</b><br>
                    👉 หาคนเต็มวงกลม = ครึ่งวงกลม × 2 ➔ {n_half} × 2 = <b>{total} คน</b><br>
                    <b>2) หาตำแหน่งที่ยืนของ {n3}</b><br>
                    👉 {n3} ยืนถัดจาก {pos2} ไปอีก {add_pos} ตำแหน่ง: {pos2} + {add_pos} = <b>{pos2+add_pos}</b><br>
                    👉 (ข้อควรระวัง: ถ้ายอดการนับเกินจำนวนคนรวม ให้หักออกเป็นรอบๆ ด้วย {total})<br>
                    👉 หมายเลขสุดท้ายของ {n3} จะไปตกที่ตำแหน่ง <b>{pos3}</b><br>
                    <b>ตอบ: มีทั้งหมด {total} คน และ {n3} คือหมายเลข {pos3}</b></span>"""
                else:
                    n_half = random.randint(4, 6) if is_p12 else (random.randint(8, 15) if is_p34 else random.randint(20, 40))
                    total = n_half * 2
                    pos1 = random.randint(1, n_half)
                    pos2 = pos1 + n_half
                    
                    q = f"เด็กยืนล้อมวงกลมเว้นระยะเท่าๆ กัน นับหมายเลขเรียง 1, 2... <br>ถ้า <b>{n1}</b> หมายเลข <b>{pos1}</b> มองฝั่งตรงข้ามพบ <b>{n2}</b> หมายเลข <b>{pos2}</b> เด็กกลุ่มนี้มีกี่คน?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: วิเคราะห์เงื่อนไข 'ฝั่งตรงข้าม'</b><br>
                    👉 การยืนฝั่งตรงข้ามกันในวงกลม หมายความว่าระยะห่างระหว่างคนสองคนนี้คือ 'ครึ่งวงกลม' พอดีเป๊ะ<br>
                    <b>ขั้นตอนที่ 2: คำนวณหาจำนวนคน</b><br>
                    👉 หาจำนวนคนครึ่งวงกลม: นำหมายเลขมาลบกัน {pos2} - {pos1} = <b>{n_half} คน</b><br>
                    👉 หาจำนวนคนเต็มวงกลม: นำครึ่งวงกลมคูณด้วย 2 ➔ {n_half} × 2 = <b>{total} คน</b><br>
                    <b>ตอบ: {total} คน</b></span>"""

            elif actual_sub_t == "การคิดย้อนกลับ":
                name = random.choice(NAMES)
                item = random.choice(ITEMS)
                if is_challenge:
                    end_val = random.randint(10, 30)
                    div_v = random.choice([2, 3, 4])
                    step3 = end_val * div_v
                    sub_v = random.randint(10, 20)
                    step2 = step3 + sub_v
                    mul_v = random.choice([2, 3])
                    
                    while step2 % mul_v != 0:
                        sub_v += 1
                        step2 = step3 + sub_v
                        
                    step1 = step2 // mul_v
                    add_v = random.randint(5, 15)
                    
                    if step1 <= add_v:
                        add_v = max(step1 - random.randint(1, 3), 1)
                        
                    X = step1 - add_v
                    
                    q = f"<b>{name}</b> คิดเลขปริศนาในใจขั้นตอนดังนี้:<br>นำจำนวนปริศนามา <b>บวกด้วย {add_v}</b>, จากนั้นนำผลลัพธ์ <b>คูณด้วย {mul_v}</b>, <br>แล้ว <b>ลบออกด้วย {sub_v}</b>, และสุดท้าย <b>หารด้วย {div_v}</b> <br>ปรากฏว่าผลลัพธ์สุดท้ายคือ <b>{end_val}</b> พอดี จงหา 'จำนวนปริศนา' นั้น?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (Reverse Engineering 4 ชั้น):</b><br>
                    เทคนิค: ทำย้อนกลับจากเหตุการณ์หลังสุดไปหาหน้าสุด และ 'สลับเครื่องหมาย' ให้ตรงกันข้ามทั้งหมด!<br>
                    👉 <b>ขั้นที่ 1 (ย้อนจากผลลัพธ์สุดท้าย):</b> เปลี่ยน หาร เป็น คูณ ➔ นำ {end_val} × {div_v} = <b>{step3}</b><br>
                    👉 <b>ขั้นที่ 2 (ย้อนถัดมา):</b> เปลี่ยน ลบ เป็น บวก ➔ นำ {step3} + {sub_v} = <b>{step2}</b><br>
                    👉 <b>ขั้นที่ 3 (ย้อนถัดมา):</b> เปลี่ยน คูณ เป็น หาร ➔ นำ {step2} ÷ {mul_v} = <b>{step1}</b><br>
                    👉 <b>ขั้นที่ 4 (ย้อนไปหาตัวแรกสุด):</b> เปลี่ยน บวก เป็น ลบ ➔ นำ {step1} - {add_v} = <b>{X}</b><br>
                    <b>ตอบ: {X}</b></span>"""
                else:
                    sm = random.randint(20, 50) if is_p12 else (random.randint(100, 300) if is_p34 else random.randint(1000, 3000))
                    sp = random.randint(5, 15) if is_p12 else (random.randint(20, 80) if is_p34 else random.randint(200, 800))
                    rv = random.randint(10, 20) if is_p12 else (random.randint(50, 150) if is_p34 else random.randint(500, 1500))
                    fm = sm - sp + rv
                    
                    q = f"<b>{name}</b>นำเงินไปซื้อ<b>{item}</b> <b>{sp:,}</b> บาท จากนั้นแม่ให้เพิ่มอีก <b>{rv:,}</b> บาท ทำให้มีเงิน <b>{fm:,}</b> บาท <br>ตอนแรกมีเงินกี่บาท?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (คิดย้อนกลับ):</b><br>
                    <b>ขั้นตอนที่ 1: เริ่มจากยอดเงินปัจจุบัน</b><br>
                    👉 ตอนนี้มีเงินสุทธิ: {fm:,} บาท<br>
                    <b>ขั้นตอนที่ 2: ย้อนเหตุการณ์ 'แม่ให้เงิน'</b><br>
                    👉 แม่ให้เพิ่มแปลว่าบวก ถ้าย้อนกลับต้องเอาไป <b>ลบออก</b>: {fm:,} - {rv:,} = <b>{fm - rv:,} บาท</b><br>
                    <b>ขั้นตอนที่ 3: ย้อนเหตุการณ์ 'ซื้อของ'</b><br>
                    👉 ซื้อของแปลว่าจ่ายไป ถ้าย้อนกลับต้องเอาไป <b>บวกคืน</b>: {fm - rv:,} + {sp:,} = <b>{sm:,} บาท</b><br>
                    <b>ตอบ: {sm:,} บาท</b></span>"""

            elif actual_sub_t == "การตัดเชือกพับทบ":
                name = random.choice(NAMES)
                if is_challenge:
                    f = random.randint(3, 5)
                    c = random.randint(3, 6)
                    layers = 2**f
                    ans = layers * c + 1
                    
                    svg_graphic = draw_rope_cutting_svg(layers, c)
                    q = f"<b>{name}</b> นำเชือกมาพับทบครึ่งซ้อนกันไปเรื่อยๆ จำนวน <b>{f} ครั้ง</b> จากนั้นใช้กรรไกรตัดเชือกให้ขาดออก <b>{c} รอยตัด</b> <br>เมื่อคลี่เชือกทั้งหมดออกมา จะได้เศษเชือกชิ้นเล็กชิ้นน้อยรวมทั้งหมดกี่เส้น?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (สูตรความหนาเชือก):</b><br>
                    <b>ขั้นตอนที่ 1: หาความหนาของเชือกหลังจากพับ</b><br>
                    👉 การพับครึ่ง 1 ครั้ง ความหนาของเชือกจะเพิ่มขึ้นเป็น 2 เท่า<br>
                    👉 พับ {f} ครั้ง = นำ 2 มาคูณกัน {f} ครั้ง (2<sup>{f}</sup>) = <b>{layers} ชั้น</b><br>
                    <b>ขั้นตอนที่ 2: จำลองการตัดด้วยภาพ</b><br>{svg_graphic}
                    <b>ขั้นตอนที่ 3: หาจำนวนเส้นที่ได้เพิ่มจากการตัด</b><br>
                    👉 การใช้กรรไกรตัด 1 รอยตรงกลางเชือก จะทำให้เกิดเชือกเส้นใหม่เพิ่มขึ้นเท่ากับ "จำนวนชั้น"<br>
                    👉 ดังนั้น ตัด {c} รอย = ได้เชือกเพิ่มมา {layers} × {c} = <b>{layers*c} เส้น</b><br>
                    <b>ขั้นตอนที่ 4: รวมเชือกเส้นตั้งต้น</b><br>
                    👉 นำจำนวนเส้นที่ถูกตัดเพิ่ม ไปบวกกับเชือกเส้นเดิมก่อนพับอีก 1 เส้น: {layers*c} + 1 = <b>{ans} เส้น</b><br>
                    <b>ตอบ: {ans} เส้น</b></span>"""
                else:
                    f = 2
                    c = random.randint(2, 4)
                    layers = 2**f
                    ans = layers * c + 1
                    
                    svg_graphic = draw_rope_cutting_svg(layers, c)
                    q = f"<b>{name}</b>นำเชือกมาพับทบครึ่ง <b>{f}</b> ครั้ง จากนั้นตัดให้ขาด <b>{c}</b> รอยตัด <br>เมื่อคลี่ออกมาจะได้เชือกทั้งหมดกี่เส้น?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: หาความหนา</b><br>
                    👉 พับ {f} ครั้ง เกิดความหนา = 2 ยกกำลัง {f} = <b>{layers} ชั้น</b><br>
                    <b>ขั้นตอนที่ 2: จำลองการตัดด้วยภาพ</b><br>{svg_graphic}
                    <b>ขั้นตอนที่ 3: คำนวณเส้นที่ถูกตัดและรวมเส้นตั้งต้น</b><br>
                    👉 ตัด {c} รอย ได้เส้นเพิ่ม = {layers} × {c} = <b>{layers*c} เส้น</b><br>
                    👉 รวมกับเส้นตั้งต้นที่มีอยู่แล้ว 1 เส้น: {layers*c} + 1 = <b>{ans} เส้น</b><br>
                    <b>ตอบ: {ans} เส้น</b></span>"""

            elif actual_sub_t == "โปรโมชั่นแลกของ":
                snack = random.choice(SNACKS)
                if is_challenge:
                    exch = random.choice([3, 4, 5])
                    start_bottles = random.randint(20, 40)
                    
                    total_drank = start_bottles
                    empties = start_bottles
                    while empties >= exch:
                        new_b = empties // exch
                        left_b = empties % exch
                        total_drank += new_b
                        empties = new_b + left_b
                        
                    borrowed = 0
                    if empties == exch - 1:
                        borrowed = 1
                        total_drank += 1
                        
                    q = f"โปรโมชั่น: นำซอง<b>{snack}</b>เปล่า <b>{exch}</b> ซอง แลกใหม่ฟรี 1 ชิ้น <br><b>{name}</b> ซื้อ<b>{snack}</b>มา <b>{start_bottles}</b> ชิ้น และเมื่อแลกจนหมดเขาสามารถ <b>'ยืมซองเปล่าเพื่อนมาแลกก่อน 1 ซอง และคืนให้เพื่อนภายหลังได้'</b><br>เขาจะได้กินรวมทั้งหมดกี่ชิ้น?"
                    
                    if borrowed > 0:
                        sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (รวมทริคการยืม):</b><br>
                        <b>ขั้นตอนที่ 1: นำของเดิมไปแลกเป็นทอดๆ ตามปกติ</b><br>
                        👉 เมื่อคำนวณการแลกซองเปล่าไปเรื่อยๆ จนกว่าจะแลกต่อไม่ได้ จะพบว่าเหลือเศษซองเปล่าตอนจบ <b>{empties} ซอง</b><br>
                        <b>ขั้นตอนที่ 2: ใช้ทริคการยืมของเพื่อน</b><br>
                        👉 เนื่องจากโปรโมชั่นต้องใช้ {exch} ซอง และตอนนี้เขาขาดอีกแค่ 1 ซอง เขาจึงขอยืมเพื่อนมา 1 ซอง (รวมกับที่มีอยู่เป็น {exch} ซองพอดีเป๊ะ)<br>
                        <b>ขั้นตอนที่ 3: แลกของและคืนของ</b><br>
                        👉 นำ {exch} ซองนี้ไปแลก จะได้กินฟรีอีก 1 ชิ้น! <br>
                        👉 และเมื่อกินเสร็จ จะมีซองเปล่าเหลือจากชิ้นนี้ 1 ซอง จึงนำไป <b>'คืนเพื่อน'</b> ได้พอดีไม่มีหนี้สิน!<br>
                        👉 รวมได้กินทั้งหมด <b>{total_drank} ชิ้น</b><br>
                        <b>ตอบ: {total_drank} ชิ้น</b></span>"""
                    else:
                        sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                        👉 แลกปกติเป็นทอดๆ: เมื่อแลกจนหมดจะเหลือเศษซองเปล่าตอนจบ <b>{empties} ซอง</b><br>
                        👉 เนื่องจากขาดอีกหลายซอง จึงไม่เข้าเงื่อนไขที่จะสามารถยืม 1 ซองเพื่อไปแลกแล้วมีคืนได้ (ถ้าขาดแค่ 1 ซองเป๊ะๆ ถึงจะทำทริคนี้ได้)<br>
                        👉 ดังนั้นจึงแลกต่อไม่ได้แล้ว รวมได้กินทั้งหมด <b>{total_drank} ชิ้น</b><br>
                        <b>ตอบ: {total_drank} ชิ้น</b></span>"""
                else:
                    exch = 3 if is_p12 else (random.randint(4, 5) if is_p34 else random.randint(5, 8))
                    start_bottles = random.randint(6, 9) if is_p12 else (random.randint(12, 25) if is_p34 else random.randint(30, 60))
                    
                    total_drank = start_bottles
                    empties = start_bottles
                    while empties >= exch:
                        new_b = empties // exch
                        left_b = empties % exch
                        total_drank += new_b
                        empties = new_b + left_b
                        
                    q = f"โปรโมชั่น: นำซอง<b>{snack}</b>เปล่า <b>{exch}</b> ซอง แลกใหม่ฟรี 1 ชิ้น <br>ถ้าซื้อตอนแรก <b>{start_bottles}</b> ชิ้น จะได้กินรวมทั้งหมดกี่ชิ้น?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1:</b> กินรอบแรก {start_bottles} ชิ้น จะได้ซองเปล่า {start_bottles} ซอง<br>
                    <b>ขั้นตอนที่ 2:</b> นำซองเปล่าไปแลก ➔ นำไปหารด้วย {exch} ➔ จะได้กินใหม่ และเหลือเศษซองเปล่าที่ไม่พอแลก<br>
                    <b>ขั้นตอนที่ 3:</b> นำซองที่ได้จากการกินใหม่ ไปรวมกับเศษซองเปล่าที่เหลือจากรอบก่อนหน้า เพื่อนำไปแลกเป็นทอดๆ<br>
                    <b>ขั้นตอนที่ 4:</b> บวกจำนวนชิ้นที่ได้กินในทุกๆ รอบเข้าด้วยกัน จะได้ทั้งหมด <b>{total_drank} ชิ้น</b><br>
                    <b>ตอบ: {total_drank} ชิ้น</b></span>"""

            elif actual_sub_t == "ตรรกะการจับมือ (ทักทาย)":
                loc = random.choice(LOCS)
                if is_challenge:
                    n_a = random.randint(10, 15)
                    n_b = random.randint(10, 15)
                    ans = n_a * n_b
                    
                    q = f"ในงานกิจกรรมที่<b>{loc}</b> มีเด็กชาย <b>{n_a}</b> คน และเด็กหญิง <b>{n_b}</b> คน<br>ถ้า <b>'เด็กชายทุกคนต้องจับมือกับเด็กหญิงทุกคน'</b> (ไม่จับมือกับเพศเดียวกัน) จะมีการจับมือเกิดขึ้นทั้งหมดกี่ครั้ง?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (กฎการคูณแบบข้ามกลุ่ม Bipartite):</b><br>
                    ข้อนี้ไม่ได้จับมือรวมกันทั้งหมด แต่เป็นการเชื่อมโยงระหว่าง 2 กลุ่มที่แยกกัน!<br>
                    <b>ขั้นตอนที่ 1: ดูมุมมองจากเด็กชาย 1 คน</b><br>
                    👉 เด็กชาย 1 คน จะต้องเดินไปจับมือทำความรู้จักเด็กหญิงให้ครบทั้ง {n_b} คน (จะเกิดการจับมือขึ้น {n_b} ครั้ง)<br>
                    <b>ขั้นตอนที่ 2: ดูมุมมองในภาพรวม</b><br>
                    👉 เนื่องจากในงานมีเด็กชายทั้งหมด {n_a} คน ดังนั้นเหตุการณ์ในขั้นตอนที่ 1 จะเกิดขึ้นซ้ำๆ กัน<br>
                    <b>ขั้นตอนที่ 3: ใช้การคูณเพื่อหาคำตอบ</b><br>
                    👉 นำจำนวนคนทั้งสองกลุ่มมาคูณกัน: {n_a} คน × {n_b} คน = <b>{ans:,} ครั้ง</b><br>
                    <b>ตอบ: {ans:,} ครั้ง</b></span>"""
                else:
                    n = random.randint(5, 10) if is_p34 else random.randint(10, 20)
                    ans = sum(range(1, n))
                    q = f"ในการจัดกิจกรรม มีเด็ก <b>{n}</b> คน หากเด็กทุกคนจับมือทำความรู้จักกันให้ครบทุกคน จะมีการจับมือเกิดขึ้นทั้งหมดกี่ครั้ง?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1:</b> คนที่ 1 เดินไปจับมือกับคนอื่นทุกคน จะเกิดการจับ {n-1} ครั้ง<br>
                    <b>ขั้นตอนที่ 2:</b> คนที่ 2 เดินไปจับคนอื่น (แต่ไม่ต้องจับคนที่ 1 แล้วเพราะจับไปแล้ว) จะเกิดการจับ {n-2} ครั้ง<br>
                    <b>ขั้นตอนที่ 3:</b> จำนวนจะลดหลั่นลงไปเรื่อยๆ ทีละ 1 จนถึงคนสุดท้ายที่ไม่มีใครให้จับเพิ่ม<br>
                    <b>ขั้นตอนที่ 4:</b> นำตัวเลขมาบวกกัน: {' + '.join(str(x) for x in range(n-1, 0, -1))} = <b>{ans} ครั้ง</b><br>
                    <b>ตอบ: {ans} ครั้ง</b></span>"""

            elif actual_sub_t == "หยิบของในที่มืด":
                item = random.choice(ITEMS)
                if is_challenge:
                    c1 = random.randint(10, 20)
                    c2 = random.randint(10, 20)
                    c3 = random.randint(10, 20)
                    arr = sorted([c1, c2, c3], reverse=True)
                    ans = arr[0] + arr[1] + 1
                    
                    q = f"ในกล่องทึบมี<b>{item}</b>สีแดง <b>{c1}</b> ชิ้น, สีน้ำเงิน <b>{c2}</b> ชิ้น, และสีเขียว <b>{c3}</b> ชิ้น<br>หากหลับตาหยิบ ต้องหยิบออกมา<b>อย่างน้อยที่สุดกี่ชิ้น</b> จึงจะมั่นใจ 100% ว่าจะได้ <b>'ครบทั้ง 3 สี อย่างน้อยสีละ 1 ชิ้น'</b> แน่นอน?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (หลักการดวงซวยที่สุดขั้นสูง):</b><br>
                    เพื่อให้มั่นใจ 100% ว่าจะได้ครบทุกสี ต้องคิดกรณีที่โชคร้ายที่สุด คือหยิบได้สีที่มีจำนวนเยอะๆ ออกมาจนเกลี้ยงกล่องก่อน!<br>
                    <b>ขั้นตอนที่ 1: หาสีที่จำนวนเยอะที่สุด 2 อันดับแรก</b><br>
                    👉 สีที่มีจำนวนเยอะที่สุด 2 ลำดับแรกคือสีที่มี <b>{arr[0]} ชิ้น</b> และ <b>{arr[1]} ชิ้น</b><br>
                    <b>ขั้นตอนที่ 2: จำลองความโชคร้าย</b><br>
                    👉 โชคร้ายสุดๆ คือหยิบได้แค่ 2 สีนี้ออกมาหมดเกลี้ยงกล่องเลย: {arr[0]} + {arr[1]} = <b>{arr[0]+arr[1]} ชิ้น</b> (ตอนนี้มีของเต็มมือ แต่มีแค่ 2 สีเท่านั้น)<br>
                    <b>ขั้นตอนที่ 3: หยิบเพื่อปิดจ๊อบ</b><br>
                    👉 ในกล่องตอนนี้จะเหลือแค่ 'สีที่ 3' ล้วนๆ ดังนั้นการหยิบชิ้นต่อไป (บวก 1) จะการันตีร้อยเปอร์เซ็นต์ว่าได้สีครบ 3 สีแน่นอน!<br>
                    👉 คำนวณ: {arr[0]+arr[1]} + 1 = <b>{ans} ชิ้น</b><br>
                    <b>ตอบ: {ans} ชิ้น</b></span>"""
                else:
                    if is_p34: 
                        c1 = random.randint(5, 12)
                        c2 = random.randint(5, 12)
                        c3 = random.randint(3, 8)
                        c_total = c1 + c2
                        text_add = ""
                        target_color = "สีเขียว"
                    else: 
                        c1 = random.randint(15, 30)
                        c2 = random.randint(15, 30)
                        c3 = random.randint(15, 30)
                        c4 = random.randint(5, 15)
                        c_total = c1 + c2 + c3
                        text_add = f", สีเหลือง <b>{c4}</b> ชิ้น"
                        target_color = "สีเหลือง"
                        
                    q = f"ในกล่องทึบมี<b>{item}</b>สีแดง <b>{c1}</b> ชิ้น, สีน้ำเงิน <b>{c2}</b> ชิ้น, สีเขียว <b>{c3}</b> ชิ้น{text_add}<br>ต้องหยิบ<b>อย่างน้อยกี่ชิ้น</b> จึงจะมั่นใจ 100% ว่าจะได้<b>{target_color}</b>อย่างน้อย 1 ชิ้น?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (หลักการดวงซวยที่สุด):</b><br>
                    <b>ขั้นตอนที่ 1: จำลองความโชคร้าย</b><br>
                    👉 กรณีโชคร้ายที่สุด คือเราอยากได้{target_color} แต่มือเจ้ากรรมดันหยิบได้สีอื่นจนหมดเกลี้ยงกล่องก่อน<br>
                    👉 สีอื่นรวมกันมี: <b>{c_total} ชิ้น</b><br>
                    <b>ขั้นตอนที่ 2: หยิบเพื่อปิดจ๊อบ</b><br>
                    👉 เมื่อสีอื่นหมดกล่องแล้ว ของชิ้นต่อไปที่เราจะหยิบ (บวกเพิ่ม 1) จะการันตีว่าเป็น{target_color}แน่นอน 100%<br>
                    👉 คำนวณ: {c_total} + 1 = <b>{c_total+1} ชิ้น</b><br>
                    <b>ตอบ: {c_total+1} ชิ้น</b></span>"""

            elif actual_sub_t == "แผนภาพความชอบ":
                n1, n2, n3 = random.sample(SNACKS, 3)
                if is_challenge:
                    tot = random.randint(150, 200)
                    only_A = random.randint(10, 20)
                    only_B = random.randint(10, 20)
                    only_C = random.randint(10, 20)
                    
                    A_B = random.randint(5, 10)
                    B_C = random.randint(5, 10)
                    A_C = random.randint(5, 10)
                    all_3 = random.randint(3, 8)
                    neither = random.randint(5, 15)
                    
                    like_A = only_A + A_B + A_C + all_3
                    like_B = only_B + A_B + B_C + all_3
                    like_C = only_C + A_C + B_C + all_3
                    
                    real_tot = only_A + only_B + only_C + A_B + B_C + A_C + all_3 + neither
                    
                    q = f"สำรวจนักเรียน <b>{real_tot}</b> คน พบว่ามีคนชอบ <b>{n1} {like_A} คน</b>, ชอบ <b>{n2} {like_B} คน</b>, และชอบ <b>{n3} {like_C} คน</b><br>โดยมีคนที่ชอบ {n1}และ{n2} (แต่ไม่ชอบ{n3}) <b>{A_B} คน</b>, ชอบ {n2}และ{n3} (แต่ไม่ชอบ{n1}) <b>{B_C} คน</b>, ชอบ {n1}และ{n3} (แต่ไม่ชอบ{n2}) <b>{A_C} คน</b><br>และคนที่ชอบทั้ง 3 อย่างมี <b>{all_3} คน</b> จงหาว่ามีนักเรียนกี่คนที่ <b>'ไม่ชอบ'</b> ขนมทั้ง 3 ชนิดนี้เลย?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (แผนภาพเวนน์ 3 วง):</b><br>
                    <b>ขั้นตอนที่ 1: หาคนที่ชอบอย่างใดอย่างหนึ่งล้วนๆ แบบเพียวๆ</b><br>
                    👉 ชอบ {n1} ล้วนๆ = ยอดคนชอบ {n1} - (ยอดที่ซ้อนทับกับวงอื่น) ➔ {like_A} - ({A_B}+{A_C}+{all_3}) = <b>{only_A} คน</b><br>
                    👉 ชอบ {n2} ล้วนๆ = ยอดคนชอบ {n2} - (ยอดที่ซ้อนทับกับวงอื่น) ➔ {like_B} - ({A_B}+{B_C}+{all_3}) = <b>{only_B} คน</b><br>
                    👉 ชอบ {n3} ล้วนๆ = ยอดคนชอบ {n3} - (ยอดที่ซ้อนทับกับวงอื่น) ➔ {like_C} - ({A_C}+{B_C}+{all_3}) = <b>{only_C} คน</b><br>
                    <b>ขั้นตอนที่ 2: รวมคนที่ชอบขนม (ทุกส่วนย่อยในวงกลมบวกกัน)</b><br>
                    👉 {only_A} + {only_B} + {only_C} + {A_B} + {B_C} + {A_C} + {all_3} = <b>{real_tot - neither} คน</b> (นี่คือคนที่ชอบอย่างน้อย 1 ชนิด)<br>
                    <b>ขั้นตอนที่ 3: หาคนที่ไม่ชอบเลย (คนที่อยู่นอกวงกลม)</b><br>
                    👉 นำยอดคนทั้งหมด ลบยอดรวมคนที่ชอบขนม ➔ {real_tot} - {real_tot - neither} = <b>{neither} คน</b><br>
                    <b>ตอบ: {neither} คน</b></span>"""
                else:
                    if is_p34: 
                        tot = random.randint(30, 50)
                        both = random.randint(5, 12)
                    else: 
                        tot = random.randint(100, 200)
                        both = random.randint(20, 50)
                        
                    only_a = random.randint(10, 20)
                    only_b = random.randint(10, 20)
                    l_a = only_a + both
                    l_b = only_b + both
                    neither = tot - (only_a + only_b + both)
                    
                    q = f"สำรวจนักเรียน <b>{tot}</b> คน พบว่าชอบ<b>{n1}</b> <b>{l_a}</b> คน, ชอบ<b>{n2}</b> <b>{l_b}</b> คน, และชอบทั้งสองอย่าง <b>{both}</b> คน <br>มีกี่คนที่ไม่ชอบกินขนมทั้งสองชนิดนี้เลย?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: หาคนที่ชอบชนิดเดียวล้วนๆ</b><br>
                    👉 ชอบ {n1} อย่างเดียว: นำคนชอบ {n1} ลบตรงกลาง ➔ {l_a} - {both} = <b>{only_a} คน</b><br>
                    👉 ชอบ {n2} อย่างเดียว: นำคนชอบ {n2} ลบตรงกลาง ➔ {l_b} - {both} = <b>{only_b} คน</b><br>
                    <b>ขั้นตอนที่ 2: รวมคนที่ชอบขนม</b><br>
                    👉 นำยอดทั้ง 3 ส่วนมาบวกกัน: {only_a} + {only_b} + {both} = <b>{only_a + only_b + both} คน</b><br>
                    <b>ขั้นตอนที่ 3: หาคนที่ไม่ชอบเลย</b><br>
                    👉 นำคนทั้งหมดลบคนที่ชอบขนม: {tot} - {only_a + only_b + both} = <b>{neither} คน</b><br>
                    <b>ตอบ: {neither} คน</b></span>"""

            elif actual_sub_t == "ผลบวกจำนวนเรียงกัน (Gauss)":
                if is_challenge:
                    even = random.choice([True, False])
                    N = random.choice([50, 100, 200])
                    if even:
                        ans = (N//2) * (N//2 + 1)
                        q = f"จงหาผลบวกของ <b>'จำนวนคู่'</b> ทุกจำนวน ตั้งแต่ 1 ถึง {N} <br>( 2 + 4 + 6 + ... + {N} = ? )"
                        sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (ผลบวกเกาส์แบบกระโดด):</b><br>
                        <b>ขั้นตอนที่ 1: หาจำนวนตัวเลขทั้งหมดในอนุกรม</b><br>
                        👉 ตั้งแต่ 1 ถึง {N} มีเลขคู่ทั้งหมดครึ่งหนึ่ง คือ {N} ÷ 2 = <b>{N//2} ตัว</b><br>
                        <b>ขั้นตอนที่ 2: ใช้หลักการจับคู่หัว-ท้าย</b><br>
                        👉 ผลบวกของ 1 คู่ (ตัวแรกสุด + ตัวหลังสุด) = 2 + {N} = <b>{N+2}</b><br>
                        👉 เรามีเลข {N//2} ตัว นำมาจับคู่กัน 2 ตัว จะได้ {N//2} ÷ 2 = <b>{(N//2)/2} คู่</b><br>
                        <b>ขั้นตอนที่ 3: หาผลรวมทั้งหมด</b><br>
                        👉 นำผลบวก 1 คู่ × จำนวนคู่ทั้งหมด ➔ {N+2} × {(N//2)/2} = <b>{ans:,}</b><br>
                        <b>ตอบ: {ans:,}</b></span>"""
                    else:
                        ans = (N//2) ** 2
                        q = f"จงหาผลบวกของ <b>'จำนวนคี่'</b> ทุกจำนวน ตั้งแต่ 1 ถึง {N-1} <br>( 1 + 3 + 5 + ... + {N-1} = ? )"
                        sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (ผลบวกเกาส์แบบกระโดด):</b><br>
                        <b>ขั้นตอนที่ 1: หาจำนวนตัวเลขทั้งหมดในอนุกรม</b><br>
                        👉 ตั้งแต่ 1 ถึง {N-1} มีเลขคี่ทั้งหมดครึ่งหนึ่งของ {N} คือ <b>{N//2} ตัว</b><br>
                        <b>ขั้นตอนที่ 2: ใช้หลักการจับคู่หัว-ท้าย</b><br>
                        👉 ผลบวกของ 1 คู่ (ตัวแรกสุด + ตัวหลังสุด) = 1 + {N-1} = <b>{N}</b><br>
                        👉 เรามีเลข {N//2} ตัว นำมาจับคู่กัน 2 ตัว จะได้ {N//2} ÷ 2 = <b>{(N//2)/2} คู่</b><br>
                        <b>ขั้นตอนที่ 3: หาผลรวมทั้งหมด (หรือใช้สูตรลัดเลขคี่ = จำนวนตัว²)</b><br>
                        👉 นำผลบวก 1 คู่ × จำนวนคู่ทั้งหมด ➔ {N} × {(N//2)/2} = {N//2} × {N//2} = <b>{ans:,}</b><br>
                        <b>ตอบ: {ans:,}</b></span>"""
                else:
                    n = random.choice([20, 30, 40, 50]) if is_p34 else random.choice([100, 200, 500])
                    ans = (n * (n + 1)) // 2
                    q = f"จงหาผลบวกของตัวเลขเรียงลำดับตั้งแต่ 1 ถึง {n} <br>( 1 + 2 + 3 + ... + {n} = ? )"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (หลักการจับคู่ของเกาส์):</b><br>
                    <b>ขั้นตอนที่ 1: หาผลบวกของการจับคู่หัว-ท้าย</b><br>
                    👉 นำตัวเลขน้อยสุด + ตัวเลขมากสุด: 1 + {n} = <b>{n+1}</b> (ทุกคู่ที่จับเข้าหากันจะได้ยอดนี้เสมอ)<br>
                    <b>ขั้นตอนที่ 2: หาจำนวนคู่ทั้งหมด</b><br>
                    👉 มีตัวเลขทั้งหมด {n} ตัว จัดเป็นคู่ๆ (หาร 2) จะได้ {n} ÷ 2 = <b>{n//2} คู่</b><br>
                    <b>ขั้นตอนที่ 3: หาผลบวกทั้งหมด</b><br>
                    👉 นำผลบวก 1 คู่ × จำนวนคู่ทั้งหมด: {n+1} × {n//2} = <b>{ans:,}</b><br>
                    <b>ตอบ: {ans:,}</b></span>"""

            elif actual_sub_t == "งานและเวลา (Work)":
                action = random.choice(WORK_ACTIONS)
                if is_challenge:
                    n1, n2, n3 = random.sample(NAMES, 3)
                    pairs = [(10, 12, 15, 4), (12, 15, 20, 5), (6, 10, 15, 3), (12, 24, 8, 4)]
                    w1, w2, w3, ans = random.choice(pairs)
                    
                    f1_s = get_vertical_fraction(1, w1, is_bold=False)
                    f2_s = get_vertical_fraction(1, w2, is_bold=False)
                    f3_s = get_vertical_fraction(1, w3, is_bold=False)
                    
                    lcm_val = lcm_multiple(w1, w2, w3)
                    sum_num = (lcm_val//w1) + (lcm_val//w2) + (lcm_val//w3)
                    
                    f_sum1 = get_vertical_fraction(lcm_val//w1, lcm_val, is_bold=False)
                    f_sum2 = get_vertical_fraction(lcm_val//w2, lcm_val, is_bold=False)
                    f_sum3 = get_vertical_fraction(lcm_val//w3, lcm_val, is_bold=False)
                    f_total = get_vertical_fraction(sum_num, lcm_val, is_bold=True)
                    f_ans = get_vertical_fraction(1, ans, is_bold=False)
                    
                    q = f"ในการ<b>{action}</b> หากให้ <b>{n1}</b> ทำคนเดียวจะเสร็จใน {w1} วัน, <b>{n2}</b> ทำคนเดียวเสร็จใน {w2} วัน, และ <b>{n3}</b> ทำคนเดียวเสร็จใน {w3} วัน<br>จงหาว่าถ้าทั้งสามคน 'ช่วยกันทำพร้อมกัน' งานนี้จะเสร็จภายในเวลากี่วัน?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (สมการอัตราการทำงานรวม 3 คน):</b><br>
                    เปลี่ยนจำนวนวันให้เป็น "ปริมาณงานที่ทำได้ใน 1 วัน"<br>
                    <b>ขั้นตอนที่ 1: หาผลงานใน 1 วันของแต่ละคน</b><br>
                    👉 {n1} ทำได้ {f1_s}, {n2} ทำได้ {f2_s}, {n3} ทำได้ {f3_s} ของงานทั้งหมด<br>
                    <b>ขั้นตอนที่ 2: นำผลงานใน 1 วันมาบวกกัน (ทำตัวส่วนให้เท่ากันด้วย ค.ร.น.)</b><br>
                    👉 ค.ร.น. ของ {w1}, {w2}, {w3} คือ {lcm_val}<br>
                    👉 นำมาบวกกัน: {f1_s} + {f2_s} + {f3_s} = {f_sum1} + {f_sum2} + {f_sum3} = {f_total}<br>
                    👉 ทำเป็นเศษส่วนอย่างต่ำ จะได้ผลลัพธ์คือ <b>{f_ans}</b> ของงานทั้งหมด<br>
                    <b>ขั้นตอนที่ 3: พลิกกลับเศษเป็นส่วนเพื่อหาจำนวนวัน</b><br>
                    👉 ความหมายคือ 1 วัน 3 คนช่วยกันทำได้ {f_ans} งาน<br>
                    👉 ดังนั้นต้องใช้เวลา <b>{ans} วัน</b> จึงจะได้งานเต็ม 1 ก้อน (เสร็จสมบูรณ์)<br>
                    <b>ตอบ: {ans} วัน</b></span>"""
                else:
                    pairs = [(3,6,2), (4,12,3), (6,12,4), (10,15,6)]
                    w1, w2, ans = random.choice(pairs)
                    n1, n2 = random.sample(NAMES, 2)
                    
                    q = f"ในการ<b>{action}</b> หากให้ <b>{n1}</b> ทำคนเดียวจะเสร็จใน {w1} วัน แต่ถ้าให้ <b>{n2}</b> ทำคนเดียวจะเสร็จใน {w2} วัน <br>จงหาว่าถ้าช่วยกันทำพร้อมกัน จะเสร็จภายในเวลากี่วัน?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: ใช้สูตรลัด 2 คนช่วยกันทำงาน</b><br>
                    👉 สูตร: (เวลาคนแรก × เวลาคนที่สอง) ÷ (เวลาคนแรก + เวลาคนที่สอง)<br>
                    <b>ขั้นตอนที่ 2: แทนค่าตัวเลขลงในสูตร</b><br>
                    👉 ด้านบน (คูณ): {w1} × {w2} = {w1*w2}<br>
                    👉 ด้านล่าง (บวก): {w1} + {w2} = {w1+w2}<br>
                    👉 นำมาหารกัน: {w1*w2} ÷ {w1+w2} = <b>{ans} วัน</b><br>
                    <b>ตอบ: {ans} วัน</b></span>"""

            elif actual_sub_t == "ระฆังและไฟกะพริบ (ค.ร.น.)":
                item_word = random.choice(["สัญญาณไฟ", "นาฬิกาปลุก", "ระฆัง"])
                if is_challenge:
                    l1, l2, l3, l4 = random.sample([10, 15, 20, 30, 45, 60], 4)
                    lcm = lcm_multiple(l1, l2, l3, l4)
                    ans_min = lcm // 60
                    ans_sec = lcm % 60
                    text_ans = f"{ans_min} นาที" if ans_sec == 0 else f"{ans_min} นาที {ans_sec} วินาที"
                    
                    q = f"<b>{item_word} 4 ชิ้น</b> ทำงานด้วยจังหวะที่ต่างกัน ดังนี้:<br>ชิ้นที่ 1 ดังทุกๆ {l1} วินาที, ชิ้นที่ 2 ดังทุกๆ {l2} วินาที, ชิ้นที่ 3 ดังทุกๆ {l3} วินาที, และชิ้นที่ 4 ดังทุกๆ {l4} วินาที <br>ถ้าเพิ่งดังพร้อมกันไป อีกกี่นาทีข้างหน้าจึงจะดังพร้อมกันอีกครั้ง?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (หา ค.ร.น. ขั้นสูง):</b><br>
                    โจทย์ที่มีคำว่า "เกิดขึ้นพร้อมกันอีกครั้ง" ให้ใช้การหา ค.ร.น. (คูณร่วมน้อย)<br>
                    <b>ขั้นตอนที่ 1: ตั้งหารสั้นเพื่อหา ค.ร.น.</b><br>
                    👉 นำตัวเลข {l1}, {l2}, {l3}, {l4} มาหา ค.ร.น. จะได้รอบเวลาที่ลงตัวพร้อมกันคือ <b>{lcm} วินาที</b><br>
                    <b>ขั้นตอนที่ 2: แปลงหน่วยวินาทีเป็นนาทีให้เรียบร้อย</b><br>
                    👉 1 นาที มี 60 วินาที ให้นำ {lcm} ÷ 60<br>
                    👉 จะได้ผลลัพธ์เท่ากับ <b>{text_ans}</b> พอดี<br>
                    <b>ตอบ: {text_ans}</b></span>"""
                else:
                    l1, l2, l3 = random.sample([10, 12, 15, 20, 30], 3)
                    lcm = lcm_multiple(l1, l2, l3)
                    
                    q = f"{item_word} 3 ชิ้น ทำงานด้วยจังหวะต่างกัน ชิ้นแรกดังทุกๆ {l1} วินาที, ชิ้นที่สอง {l2} วินาที และชิ้นที่สาม {l3} วินาที <br>ถ้าเพิ่งดังพร้อมกันไป อีกกี่วินาทีข้างหน้าจึงจะดังพร้อมกันอีกครั้ง?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: วิเคราะห์โจทย์</b><br>
                    👉 โจทย์ประเภท 'เกิดขึ้นพร้อมกันอีกครั้ง' ให้หา ค.ร.น. (ตัวคูณร่วมน้อย)<br>
                    <b>ขั้นตอนที่ 2: ตั้งหารสั้น</b><br>
                    👉 นำรอบเวลาทั้งหมด ({l1}, {l2}, {l3}) มาหา ค.ร.น. จะได้ผลลัพธ์เท่ากับ <b>{lcm}</b><br>
                    <b>ตอบ: อีก {lcm} วินาที</b></span>"""

            elif actual_sub_t == "นาฬิกาเดินเพี้ยน":
                if is_challenge:
                    days_map = {"พฤหัสบดี": 3, "ศุกร์": 4, "เสาร์": 5}
                    end_day = random.choice(list(days_map.keys()))
                    days = days_map[end_day]
                    
                    gain_m = random.randint(3, 12)
                    total_gain = days * gain_m
                    
                    carry_h = total_gain // 60
                    final_m = total_gain % 60
                    final_h = 8 + carry_h
                    
                    q = f"นาฬิกาเรือนหนึ่งทำงานผิดปกติ โดยจะเดิน <b>'เร็วเกินไป' วันละ {gain_m} นาที</b><br>ถ้าตั้งเวลานาฬิกาเรือนนี้ให้ตรงเป๊ะในตอน <b>08:00 น. ของวันจันทร์</b><br>จงหาว่าเมื่อเวลาจริงดำเนินไปถึง <b>08:00 น. ของวัน{end_day}</b> นาฬิกาเรือนนี้จะชี้บอกเวลาใด?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (คำนวณความคลาดเคลื่อนสะสม):</b><br>
                    <b>ขั้นตอนที่ 1: หาจำนวนวันที่ผ่านไปทั้งหมด</b><br>
                    👉 จาก 08:00 น. วันจันทร์ ถึง 08:00 น. วัน{end_day} นับเวลาที่ผ่านไปได้ <b>{days} วันพอดีเป๊ะ</b><br>
                    <b>ขั้นตอนที่ 2: หาเวลาที่นาฬิกาเดินเพี้ยนไปทั้งหมดสะสม</b><br>
                    👉 เดินเร็วขึ้นวันละ {gain_m} นาที × {days} วัน = <b>เดินเร็วนำหน้าเวลาจริงไป {total_gain} นาที</b><br>
                    <b>ขั้นตอนที่ 3: คำนวณเวลาที่จะแสดงบนหน้าปัด</b><br>
                    👉 แปลงหน่วยนาทีที่เกินมาให้เป็นชั่วโมง: นำ {total_gain} นาที ÷ 60 จะได้ <b>{carry_h} ชั่วโมง กับอีก {final_m} นาที</b><br>
                    👉 นำความคลาดเคลื่อนนี้ไปบวกเพิ่มจากเวลาจริง: 08:00 น. + {carry_h} ชั่วโมง {final_m} นาที = <b>{final_h:02d}:{final_m:02d} น.</b><br>
                    <b>ตอบ: เวลา {final_h:02d}:{final_m:02d} น.</b></span>"""
                else:
                    fast_min = random.randint(3, 8)
                    start_h = 8
                    passed_hours = random.randint(5, 12)
                    end_h = start_h + passed_hours
                    total_fast = fast_min * passed_hours
                    
                    q = f"นาฬิกาเรือนหนึ่งเดินเร็วไป <b>{fast_min} นาที ในทุกๆ 1 ชั่วโมง</b> <br>ตั้งเวลาตรงตอน <b>0{start_h}:00 น.</b> เมื่อเวลาจริงผ่านไปถึง <b>{end_h}:00 น.</b> นาฬิกาจะแสดงเวลาใด?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: หาจำนวนชั่วโมงที่ผ่านไป</b><br>
                    👉 นำเวลาสิ้นสุด ลบ เวลาเริ่มต้น: {end_h} - {start_h} = <b>{passed_hours} ชั่วโมง</b><br>
                    <b>ขั้นตอนที่ 2: หาเวลาที่นาฬิกาเดินเร็วเกินไปทั้งหมด</b><br>
                    👉 เดินเร็วชั่วโมงละ {fast_min} นาที × {passed_hours} ชั่วโมง = <b>{total_fast} นาที</b><br>
                    <b>ขั้นตอนที่ 3: รวมเวลาแสดงผล</b><br>
                    👉 นำเวลาที่เดินเกิน ไปบวกเพิ่มกับเวลาจริง จะได้ <b>{end_h}:{total_fast:02d} น.</b><br>
                    <b>ตอบ: {end_h}:{total_fast:02d} น.</b></span>"""

            else:
                q = f"⚠️ [ระบบผิดพลาด] ไม่พบเงื่อนไขสำหรับหัวข้อ: <b>{actual_sub_t}</b>"
                sol = "Error"

            if q not in seen:
                seen.add(q)
                questions.append({"question": q, "solution": sol})
                break
                
    return questions

# ==========================================
# UI Rendering
# ==========================================
def extract_body(html_str):
    try: return html_str.split('<body>')[1].split('</body>')[0]
    except IndexError: return html_str

def create_page(level, sub_t, questions, is_key=False, q_margin="20px", ws_height="180px", brand_name="", is_challenge=False):
    title_suffix = " 🔥 [ULTIMATE CHALLENGE]" if is_challenge else ""
    title = f"เฉลย (Answer Key){title_suffix}" if is_key else f"ข้อสอบ (TMC Edition){title_suffix}"
    
    student_info = """
        <table style="width: 100%; margin-bottom: 10px; font-size: 18px; border-collapse: collapse;">
            <tr>
                <td style="width: 1%; white-space: nowrap; padding-right: 5px;"><b>ชื่อ-สกุล</b></td>
                <td style="border-bottom: 2px dotted #999; width: 60%;"></td>
                <td style="width: 1%; white-space: nowrap; padding-left: 20px; padding-right: 5px;"><b>ระดับชั้น</b></td>
                <td style="border-bottom: 2px dotted #999; width: 15%;"></td>
                <td style="width: 1%; white-space: nowrap; padding-left: 20px; padding-right: 5px;"><b>เลขที่</b></td>
                <td style="border-bottom: 2px dotted #999; width: 15%;"></td>
            </tr>
        </table>
        """ if not is_key else ""
        
    html = f"""<!DOCTYPE html><html lang="th"><head><meta charset="utf-8">
    <style>
        @page {{ size: A4; margin: 15mm; }}
        body {{ font-family: 'Sarabun', sans-serif; padding: 20px; line-height: 1.6; color: #333; }}
        .header {{ text-align: center; border-bottom: 2px solid #333; margin-bottom: 10px; padding-bottom: 10px; }}
        .header h2 {{ color: {'#c0392b' if is_challenge else '#8e44ad'}; }}
        .q-box {{ margin-bottom: {q_margin}; padding: 10px 15px; page-break-inside: avoid; font-size: 20px; line-height: 1.8; }}
        .workspace {{ height: {ws_height}; border: 2px dashed #bdc3c7; border-radius: 8px; margin: 15px 0; padding: 10px; color: #95a5a6; font-size: 16px; background-color: #fafbfc; }}
        .ans-line {{ margin-top: 10px; border-bottom: 1px dotted #999; width: 80%; height: 30px; font-weight: bold; font-size: 20px; display: flex; align-items: flex-end; padding-bottom: 5px; }}
        .sol-text {{ color: #333; font-size: 18px; display: block; margin-top: 15px; padding: 15px; background-color: #f5eef8; border-left: 4px solid {'#c0392b' if is_challenge else '#8e44ad'}; border-radius: 4px; line-height: 1.8; }}
        .page-footer {{ text-align: right; font-size: 14px; color: #95a5a6; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }}
    </style></head><body>
    <div class="header"><h2>{title}</h2><p><b>หมวดหมู่:</b> {sub_t} ({level})</p></div>
    {student_info}"""
    
    for i, item in enumerate(questions, 1):
        html += f'<div class="q-box"><b>ข้อที่ {i}.</b> '
        if is_key:
            html += f'{item["question"]}<div class="sol-text">{item["solution"]}</div>'
        else:
            html += f'{item["question"]}<div class="workspace">พื้นที่สำหรับแสดงวิธีคิดวิเคราะห์...</div><div class="ans-line">ตอบ: </div>'
        html += '</div>'
        
    if brand_name: 
        html += f'<div class="page-footer">&copy; 2026 {brand_name} | สงวนลิขสิทธิ์</div>'
        
    return html + "</body></html>"

# ==========================================
# 4. Streamlit UI (Sidebar & Result Grouping)
# ==========================================
st.sidebar.markdown("## ⚙️ พารามิเตอร์การสร้างข้อสอบ")

selected_level = st.sidebar.selectbox("🏆 เลือกระดับชั้น:", list(comp_db.keys()))
sub_options = comp_db[selected_level]
selected_sub = st.sidebar.selectbox("📝 เลือกแนวข้อสอบ (พร้อมเฉลยละเอียด):", sub_options + ["🌟 สุ่มรวมทุกแนวแข่งขัน"])

num_input = st.sidebar.number_input("🔢 จำนวนข้อ:", min_value=1, max_value=100, value=10)

st.sidebar.markdown("---")
is_challenge = st.sidebar.toggle("🔥 โหมด Challenge (ระดับยากพิเศษสำหรับเด็กเก่ง)", value=False)

if is_challenge:
    st.markdown("""
    <script>
        const header = window.parent.document.querySelector('.main-header');
        if(header) { header.classList.add('challenge'); header.querySelector('span').innerText = '🔥 Ultimate Challenge Mode'; header.querySelector('span').style.background = '#e74c3c'; header.querySelector('span').style.color = '#fff'; }
    </script>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <script>
        const header = window.parent.document.querySelector('.main-header');
        if(header) { header.classList.remove('challenge'); header.querySelector('span').innerText = 'TMC Edition'; header.querySelector('span').style.background = '#f1c40f'; header.querySelector('span').style.color = '#333'; }
    </script>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📏 ตั้งค่าหน้ากระดาษ")
spacing_level = st.sidebar.select_slider(
    "↕️ ความสูงของพื้นที่ทดเลข:", 
    options=["แคบ", "ปานกลาง", "กว้าง", "กว้างพิเศษ"], 
    value="กว้าง"
)

if spacing_level == "แคบ": q_margin, ws_height = "15px", "100px"
elif spacing_level == "ปานกลาง": q_margin, ws_height = "20px", "180px"
elif spacing_level == "กว้าง": q_margin, ws_height = "30px", "280px"
else: q_margin, ws_height = "40px", "400px"

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎨 ตั้งค่าแบรนด์")
brand_name = st.sidebar.text_input("🏷️ ชื่อแบรนด์ / ผู้สอน:", value="บ้านทีเด็ด")

if st.sidebar.button(f"{'🚀 สั่งสร้างข้อสอบระดับ Ultimate Challenge!' if is_challenge else '🚀 สั่งสร้างข้อสอบแข่งขันเดี๋ยวนี้'}", type="primary", use_container_width=True):
    with st.spinner("กำลังออกแบบข้อสอบ วาดภาพกราฟิกประกอบ และจัดทำเฉลยแบบ Step-by-Step..."):
        
        qs = generate_questions_logic(selected_level, selected_sub, num_input, is_challenge)
        
        html_w = create_page(selected_level, selected_sub, qs, is_key=False, q_margin=q_margin, ws_height=ws_height, brand_name=brand_name, is_challenge=is_challenge)
        html_k = create_page(selected_level, selected_sub, qs, is_key=True, q_margin=q_margin, ws_height=ws_height, brand_name=brand_name, is_challenge=is_challenge)
        
        st.session_state['worksheet_html'] = html_w
        st.session_state['answerkey_html'] = html_k
        
        ebook_body = f'\n<div class="a4-wrapper">{extract_body(html_w)}</div>\n<div class="a4-wrapper">{extract_body(html_k)}</div>\n'
        
        bg_color = "#2c3e50" if is_challenge else "#525659"
        
        full_ebook_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap" rel="stylesheet"><style>@page {{ size: A4; margin: 15mm; }} @media screen {{ body {{ font-family: 'Sarabun', sans-serif; background-color: {bg_color}; display: flex; flex-direction: column; align-items: center; padding: 40px 0; margin: 0; }} .a4-wrapper {{ width: 210mm; min-height: 297mm; background: white; margin-bottom: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.3); padding: 15mm; box-sizing: border-box; }} }} @media print {{ body {{ font-family: 'Sarabun', sans-serif; background: transparent; padding: 0; display: block; margin: 0; }} .a4-wrapper {{ width: 100%; min-height: auto; margin: 0; padding: 0; box-shadow: none; page-break-after: always; }} }} .header {{ text-align: center; border-bottom: 2px solid #333; margin-bottom: 10px; padding-bottom: 10px; }} .header h2 {{ color: {'#c0392b' if is_challenge else '#8e44ad'}; }} .q-box {{ margin-bottom: {q_margin}; padding: 10px 15px; page-break-inside: avoid; font-size: 20px; line-height: 1.8; }} .workspace {{ height: {ws_height}; border: 2px dashed #bdc3c7; border-radius: 8px; margin: 15px 0; padding: 10px; color: #95a5a6; font-size: 16px; background-color: #fafbfc; }} .ans-line {{ margin-top: 10px; border-bottom: 1px dotted #999; width: 80%; height: 30px; font-weight: bold; font-size: 20px; display: flex; align-items: flex-end; padding-bottom: 5px; }} .sol-text {{ color: #333; font-size: 18px; display: block; margin-top: 15px; padding: 15px; background-color: #f5eef8; border-left: 4px solid {'#c0392b' if is_challenge else '#8e44ad'}; border-radius: 4px; line-height: 1.8; }} .page-footer {{ text-align: right; font-size: 14px; color: #95a5a6; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }}</style></head><body>{ebook_body}</body></html>"""

        mode_name = "Challenge" if is_challenge else "Normal"
        safe_sub = selected_sub.replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")
        filename_base = f"TMC_Pro_{mode_name}_{safe_sub}_{int(time.time())}"
        
        st.session_state['ebook_html'] = full_ebook_html
        st.session_state['filename_base'] = filename_base
        
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(f"{filename_base}_Full_EBook.html", full_ebook_html.encode('utf-8'))
            zip_file.writestr(f"{filename_base}_Worksheet.html", html_w.encode('utf-8'))
            zip_file.writestr(f"{filename_base}_AnswerKey.html", html_k.encode('utf-8'))
        st.session_state['zip_data'] = zip_buffer.getvalue()

if 'ebook_html' in st.session_state:
    st.success(f"✅ โค้ดสมบูรณ์ 100%! ตัดหน้าระบบหน้าปกทิ้งเรียบร้อย ดาวน์โหลดแล้วได้ข้อสอบพร้อมใช้งานทันทีครับ")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📄 โหลดเฉพาะโจทย์", data=st.session_state['worksheet_html'], file_name=f"{st.session_state['filename_base']}_Worksheet.html", mime="text/html", use_container_width=True)
        st.download_button("🔑 โหลดเฉพาะเฉลย", data=st.session_state['answerkey_html'], file_name=f"{st.session_state['filename_base']}_AnswerKey.html", mime="text/html", use_container_width=True)
    with c2:
        st.download_button("📚 โหลดรวมเล่ม E-Book", data=st.session_state['ebook_html'], file_name=f"{st.session_state['filename_base']}_Full_EBook.html", mime="text/html", use_container_width=True)
        st.download_button("🗂️ โหลดแพ็กเกจ (.zip)", data=st.session_state['zip_data'], file_name=f"{st.session_state['filename_base']}.zip", mime="application/zip", use_container_width=True)
    st.markdown("---")
    components.html(st.session_state['ebook_html'], height=800, scrolling=True)
