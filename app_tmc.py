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
    <p>ระบบสร้างข้อสอบแข่งขันคณิตศาสตร์ระดับประเทศ (TMC) พร้อมระบบ Spacing ที่ยืดหยุ่น และเฉลยละเอียดยิบ</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 1. คลังคำศัพท์และฟังก์ชันตัวช่วย
# ==========================================
NAMES = ["อคิณ", "นาวิน", "ภูผา", "สายฟ้า", "เจ้านาย", "ข้าวหอม", "ใบบัว", "มะลิ", "น้ำใส", "ญาญ่า", "ปลื้ม", "พายุ", "ไออุ่น", "กะทิ"]
LOCS = ["โรงเรียน", "สวนสัตว์", "สวนสนุก", "ห้างสรรพสินค้า", "ห้องสมุด", "สวนสาธารณะ", "พิพิธภัณฑ์", "ลานกิจกรรม", "ค่ายลูกเสือ"]
ITEMS = ["ลูกแก้ว", "สติกเกอร์", "การ์ดพลัง", "โมเดลรถ", "ตุ๊กตาหมี", "สมุดระบายสี", "ดินสอสี", "ลูกโป่ง"]
SNACKS = ["ช็อกโกแลต", "คุกกี้", "โดนัท", "เยลลี่", "ขนมปัง", "ไอศกรีม", "น้ำผลไม้", "นมเย็น"]
ANIMALS = ["แมงมุม", "มดแดง", "กบ", "จิ้งจก", "ตั๊กแตน", "เต่า", "หอยทาก"]
PUBLISHERS = ["สำนักพิมพ์", "โรงพิมพ์", "ฝ่ายวิชาการ", "ร้านถ่ายเอกสาร", "ทีมงานจัดทำเอกสาร", "บริษัทสิ่งพิมพ์"]
DOC_TYPES = ["หนังสือนิทาน", "รายงานการประชุม", "แคตตาล็อกสินค้า", "เอกสารประกอบการเรียน", "สมุดภาพ", "นิตยสารรายเดือน", "พจนานุกรม"]
BUILDERS = ["บริษัทรับเหมา", "ผู้ใหญ่บ้าน", "เทศบาลตำบล", "เจ้าของโครงการ", "ผู้อำนวยการโรงเรียน", "กรมทางหลวง", "อบต."]
BUILD_ACTIONS = ["ปักเสาไฟ", "ปลูกต้นไม้", "ตั้งศาลาริมทาง", "ติดป้ายประกาศ", "ตั้งถังขยะ", "ปักธงประดับ", "ติดตั้งกล้องวงจรปิด"]
BUILD_LOCS = ["ริมถนนทางเข้าหมู่บ้าน", "เลียบคลองส่งน้ำ", "ริมทางเดินรอบสวน", "บนสะพานยาว", "สองข้างทางเข้างาน", "รอบรั้วโรงเรียน"]
CONTAINERS = ["กล่อง", "ถุงผ้า", "ตะกร้า", "ลังกระดาษ", "แพ็คพลาสติก"]
FRUITS = ["มะม่วง", "ส้ม", "แอปเปิล", "ขนมเปี๊ยะ", "ลูกพีช"]
MATERIALS = ["แผ่นไม้", "กระดาษสี", "แผ่นพลาสติก", "ผืนผ้าใบ", "แผ่นเหล็ก", "แผ่นกระเบื้อง"]
VEHICLES = ["รถยนต์", "รถจักรยานยนต์", "รถบรรทุก", "รถไฟ", "รถตู้"]
WORK_ACTIONS = ["ทาสีบ้าน", "ปลูกต้นไม้", "สร้างกำแพง", "ประกอบหุ่นยนต์", "เก็บขยะ", "จัดหนังสือ"]

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
    
    for c in t_pad: 
        html += f"<td style='padding:5px 12px; width:35px;'>{c}</td>"
        
    html += f"<td rowspan='2' style='padding-left:20px; vertical-align:middle; font-size:28px; color:#2c3e50;'>{operator}</td></tr><tr>"
    
    for c in b_pad: 
        html += f"<td style='padding:5px 12px; width:35px; border-bottom:2px solid #333;'>{c}</td>"
        
    html += "</tr><tr>"
    
    for c in r_pad: 
        html += f"<td style='padding:5px 12px; width:35px; border-bottom:4px double #333;'>{c}</td>"
        
    html += "<td></td></tr></table>"
    return html

def lcm_multiple(*args):
    res = args[0]
    for i in args[1:]: 
        res = abs(res * i) // math.gcd(res, i)
    return res

def draw_rope_cutting_svg(layers, cuts):
    """ฟังก์ชันวาดภาพจำลองการตัดเชือกที่ถูกพับทบ (SVG)"""
    visual_layers = min(layers, 6) # กำหนดเส้นสูงสุดที่วาดได้เพื่อไม่ให้ล้นจอ
    width = 300
    height = 50 + (visual_layers * 20) + 40
    
    svg = f'<div style="text-align:center; margin: 15px 0;"><svg width="{width}" height="{height}" style="background-color:#fafbfc; border-radius:8px; border:2px dashed #bdc3c7; padding:10px;">'
    
    # คำอธิบายด้านบน
    svg += f'<text x="150" y="25" font-family="Sarabun" font-size="18" font-weight="bold" fill="#2c3e50" text-anchor="middle">เชือกพับทบ {layers} ชั้น</text>'
    
    # วาดเส้นเชือก
    start_y = 45
    layer_spacing = 20
    for i in range(visual_layers):
        y = start_y + (i * layer_spacing)
        # วาดเส้นเชือกสีส้ม
        svg += f'<line x1="30" y1="{y}" x2="270" y2="{y}" stroke="#e67e22" stroke-width="6" stroke-linecap="round"/>'
        
        # ถ้ามีหลายชั้นมาก ให้ใส่จุดไข่ปลา
        if i == visual_layers - 2 and layers > 6:
            mid_y = y + (layer_spacing / 2)
            svg += f'<text x="150" y="{mid_y + 6}" font-family="sans-serif" font-size="20" font-weight="bold" fill="#d35400" text-anchor="middle">. . .</text>'
            
    # วาดรอยตัด
    cut_spacing = 240 / (cuts + 1)
    for i in range(1, cuts + 1):
        cx = 30 + i * cut_spacing
        end_y = start_y + (visual_layers - 1) * layer_spacing + 15
        svg += f'<line x1="{cx}" y1="35" x2="{cx}" y2="{end_y}" stroke="#e74c3c" stroke-width="3" stroke-dasharray="5,5"/>'
        svg += f'<text x="{cx}" y="32" font-family="sans-serif" font-size="16" fill="#e74c3c" text-anchor="middle">✂️</text>'
        
    # คำอธิบายด้านล่าง
    svg += f'<text x="150" y="{height - 15}" font-family="Sarabun" font-size="16" font-weight="bold" fill="#c0392b" text-anchor="middle">1 รอยตัด ตัดผ่านเชือก {layers} เส้นพอดี!</text>'
    svg += '</svg></div>'
    return svg

def draw_well_svg(h, u, d):
    """ฟังก์ชันวาดภาพจำลองสัตว์ปีนบ่อเพื่ออธิบายระยะหักล้าง"""
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

# ==========================================
# 2. ฐานข้อมูลหัวข้อข้อสอบแข่งขัน (TMC 27 หัวข้อ)
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
        q = ""
        sol = ""
        attempts = 0
        
        while attempts < 500:
            attempts += 1
            actual_sub_t = sub_t
            
            if sub_t == "🌟 สุ่มรวมทุกแนวแข่งขัน":
                actual_sub_t = random.choice(comp_db[level])
                
            name = random.choice(NAMES)

            # ---------------------------------------------------------
            if actual_sub_t == "การสร้างจำนวนจากเลขโดด":
                if is_challenge:
                    digits = random.sample(range(1, 10), 5)
                    max_prod = 0
                    best_pair = ()
                    for p in itertools.permutations(digits):
                        n1 = p[0]*100 + p[1]*10 + p[2]
                        n2 = p[3]*10 + p[4]
                        if n1 * n2 > max_prod: 
                            max_prod = n1 * n2
                            best_pair = (n1, n2)
                            
                    sd = sorted(digits, reverse=True)
                    
                    q = f"<b>{name}</b> ได้รับบัตรตัวเลข 5 ใบ คือ <b>{', '.join(map(str, digits))}</b> นำมาสร้างเป็น <b>จำนวน 3 หลัก</b> และ <b>จำนวน 2 หลัก</b> ที่คูณกันแล้วได้ <b>'ผลคูณที่มีค่ามากที่สุด'</b> ผลคูณนั้นคือเท่าไร?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: เรียงลำดับตัวเลขจากมากไปน้อย</b><br>👉 นำตัวเลขมาเรียงจะได้: {sd[0]} > {sd[1]} > {sd[2]} > {sd[3]} > {sd[4]}<br>
                    <b>ขั้นตอนที่ 2: จัดวางตัวเลข (หลักการคูณไขว้เพื่อรักษาสมดุล)</b><br>👉 เลขมากที่สุด ({sd[0]}) วางเป็นหลักสิบของตัวคูณ<br>👉 เลขมากรองลงมา ({sd[1]}) วางเป็นหลักร้อยของตัวตั้ง<br>👉 เลขอันดับสาม ({sd[2]}) วางเป็นหลักสิบของตัวตั้ง เพื่อไขว้กับ {sd[0]}<br>👉 เลขอันดับสี่ ({sd[3]}) วางเป็นหลักหน่วยของตัวคูณ<br>👉 เลขน้อยที่สุด ({sd[4]}) วางเป็นหลักหน่วยของตัวตั้ง<br>
                    <b>ขั้นตอนที่ 3: ประกอบร่างและหาผลคูณ</b><br>👉 ตัวเลข 2 จำนวนคือ {best_pair[0]} และ {best_pair[1]} ➔ นำมาคูณกัน: {best_pair[0]} × {best_pair[1]} = <b>{max_prod:,}</b><br>
                    <b>ตอบ: {max_prod:,}</b></span>"""
                else:
                    digits = random.sample(range(1, 10), 3 if is_p12 else 4)
                    max_v = int("".join(map(str, sorted(digits, reverse=True))))
                    min_v = int("".join(map(str, sorted(digits))))
                    
                    q = f"มีบัตรตัวเลข <b>{', '.join(map(str, digits))}</b> จงหาผลต่างของจำนวนที่ <b>มากที่สุด</b> และ <b>น้อยที่สุด</b> ที่สร้างได้?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: สร้างจำนวนที่มากที่สุด</b><br>👉 นำตัวเลขมาเรียงจากมากไปน้อย จะได้ <b>{max_v}</b><br>
                    <b>ขั้นตอนที่ 2: สร้างจำนวนที่น้อยที่สุด</b><br>👉 นำตัวเลขมาเรียงจากน้อยไปมาก จะได้ <b>{min_v}</b><br>
                    <b>ขั้นตอนที่ 3: หาผลต่าง</b><br>👉 นำจำนวนที่มากที่สุดตั้ง ลบด้วยจำนวนที่น้อยที่สุด: {max_v} - {min_v} = <b>{max_v-min_v}</b><br>
                    <b>ตอบ: {max_v-min_v}</b></span>"""

            elif actual_sub_t == "โจทย์ปัญหาทำผิดเป็นถูก":
                A = random.randint(3, 8)
                B = random.randint(5, 20)
                
                if is_challenge:
                    X = random.randint(5, 12) * A
                    wrong_ans = (X // A) + B
                    correct_ans = (X * A) - B
                    
                    f_q = get_vertical_fraction('ปริศนา', A)
                    f_s = get_vertical_fraction('🔲', A, is_bold=False)
                    
                    q = f"<b>{name}</b> ตั้งใจจะนำจำนวนปริศนาไป <b>คูณด้วย {A}</b> แล้ว <b>ลบออกด้วย {B}</b><br>แต่เขาทำผิดพลาด สลับไปเขียนในรูปเศษส่วนคือ <b>{f_q}</b> แล้วค่อย <b>บวกเพิ่ม {B}</b> ทำให้ได้ผลลัพธ์เป็น <b>{wrong_ans}</b><br>จงหาผลลัพธ์ที่แท้จริงตามความตั้งใจแรก?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (คิดย้อนกลับ):</b><br>
                    <b>ขั้นตอนที่ 1: จำลองสมการที่ทำผิดเพื่อหาตัวเลขเริ่มต้น</b><br>👉 สิ่งที่โจทย์ทำผิดคือ: {f_s} + {B} = {wrong_ans}<br>
                    <b>ขั้นตอนที่ 2: ใช้หลักการย้ายข้างสมการ</b><br>👉 ย้ายการบวกเป็นลบ: {wrong_ans} - {B} = {wrong_ans - B} (หมายความว่า {f_s} มีค่าเท่ากับ {wrong_ans - B})<br>👉 ย้ายเศษส่วน(การหาร)เป็นคูณ: นำ {wrong_ans - B} × {A} = {X}<br>👉 จะได้ 'จำนวนปริศนา' คือ <b>{X}</b><br>
                    <b>ขั้นตอนที่ 3: คิดเลขใหม่ให้ถูกต้องตามความตั้งใจแรก</b><br>👉 นำจำนวนปริศนาไปคูณ {A}: {X} × {A} = {X * A}<br>👉 นำผลลัพธ์ไปลบ {B}: {X * A} - {B} = <b>{correct_ans:,}</b><br>
                    <b>ตอบ: {correct_ans:,}</b></span>"""
                else:
                    x = random.randint(5, 20)
                    ans_true = random.randint(30, 80)
                    wrong_ans = ans_true - (2 * x)
                    while wrong_ans <= 0: 
                        ans_true += 10
                        wrong_ans = ans_true - (2 * x)
                        
                    q = f"<b>{name}</b> ตั้งใจจะนำจำนวนหนึ่งไป <b>บวก</b> กับ {x} แต่เขาทำผิดโดยนำไป <b>ลบ</b> ด้วย {x} ทำให้ได้ผลลัพธ์เป็น <b>{wrong_ans}</b><br>ผลลัพธ์ที่แท้จริงคือเท่าไร?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: หาตัวเลขตั้งต้นก่อนทำผิด</b><br>👉 สมการที่ทำผิดคือ: 🔲 - {x} = {wrong_ans}<br>👉 ย้ายฝั่งเปลี่ยนลบเป็นบวก จะได้ตัวเลขตั้งต้น: {wrong_ans} + {x} = {wrong_ans+x}<br>
                    <b>ขั้นตอนที่ 2: คำนวณใหม่ให้ถูกต้องตามโจทย์สั่ง</b><br>👉 นำตัวเลขตั้งต้นไปบวก {x}: {wrong_ans+x} + {x} = <b>{ans_true}</b><br>
                    <b>ตอบ: {ans_true}</b></span>"""

            elif actual_sub_t == "การนับตารางเรขาคณิต":
                N = random.randint(3, 5)
                M = random.randint(4, 7)
                if N == M: M += 1
                
                if is_challenge:
                    total_rect = (N*(N+1)//2) * (M*(M+1)//2)
                    total_sq = sum((N-i)*(M-i) for i in range(min(N, M)))
                    
                    q = f"วาดตารางเป็นรูปสี่เหลี่ยมผืนผ้าขนาด <b>{N} × {M}</b> ช่อง จงหาว่ามี <b>'สี่เหลี่ยมผืนผ้าที่ไม่ใช่สี่เหลี่ยมจัตุรัส'</b> ซ่อนอยู่ทั้งหมดกี่รูป?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (วิเคราะห์แบบหักล้าง):</b><br>
                    สูตรหลัก: (จำนวนสี่เหลี่ยมผืนผ้าทั้งหมด) - (จำนวนสี่เหลี่ยมจัตุรัสทั้งหมด)<br>
                    <b>ขั้นตอนที่ 1: หาจำนวนสี่เหลี่ยมรวมทุกชนิด (สูตรนับผืนผ้า)</b><br>👉 ผลบวกแนวกว้าง: 1+2+...+{N} = {N*(N+1)//2}<br>👉 ผลบวกแนวยาว: 1+2+...+{M} = {M*(M+1)//2}<br>👉 นำมาคูณกัน: {N*(N+1)//2} × {M*(M+1)//2} = <b>{total_rect:,} รูป</b><br>
                    <b>ขั้นตอนที่ 2: หาจำนวนสี่เหลี่ยมจัตุรัสทั้งหมด</b><br>👉 ใช้สูตรลดทอนทีละ 1 แล้วคูณบวกกัน: ({N}×{M}) + ({N-1}×{M-1}) + ... ลดไปเรื่อยๆ จนถึง 1<br>👉 คำนวณผลรวมจะได้ทั้งหมด <b>{total_sq:,} รูป</b><br>
                    <b>ขั้นตอนที่ 3: หักล้างกัน</b><br>👉 นำ {total_rect:,} ลบ {total_sq:,} = <b>{total_rect - total_sq:,} รูป</b><br>
                    <b>ตอบ: {total_rect - total_sq:,} รูป</b></span>"""
                else:
                    grid = random.randint(2, 4) if is_p12 else random.randint(4, 6)
                    ans = sum(i*i for i in range(1, grid+1))
                    
                    q = f"มีตารางกระดานขนาด <b>{grid} × {grid}</b> ช่อง จงหาว่ามี <b>'สี่เหลี่ยมจัตุรัส'</b> ซ่อนอยู่ทั้งหมดกี่รูป?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: ใช้สูตรลัดนับตารางจัตุรัสสมมาตร</b><br>👉 ให้นำขนาดของตารางแต่ละตัวมายกกำลังสอง แล้วนำมาบวกกันตั้งแต่ 1² จนถึง {grid}²<br>
                    <b>ขั้นตอนที่ 2: คำนวณตัวเลข</b><br>👉 สมการ: 1² + 2² + ... + {grid}²<br>👉 ผลรวมทั้งหมดจะได้เท่ากับ <b>{ans:,} รูป</b><br>
                    <b>ตอบ: {ans:,} รูป</b></span>"""

            elif actual_sub_t == "ปริศนาสมการช่องว่าง":
                ans_v = random.randint(5, 20)
                B = random.randint(2, 10)
                C = random.randint(2, 5)
                V3 = ans_v + B
                
                if is_challenge:
                    while V3 % C != 0: 
                        ans_v += 1
                        V3 = ans_v + B
                        
                    V2 = V3 // C
                    D = random.randint(1, V2 - 1) if V2 > 1 else 1
                    V1 = V2 - D if V2 > D else 1
                    A = random.randint(2, 6)
                    E = A * V1
                    
                    f_html = get_vertical_fraction(f'( 🔲 + {B} )', C)
                    
                    q = f"จงหาตัวเลขที่เติมลงในช่องว่าง:<br><br><span style='font-size:24px; font-weight:bold;'>{A} × &nbsp;<span style='font-size:36px; vertical-align:middle;'>[</span>&nbsp; {f_html} &nbsp;−&nbsp; {D} &nbsp;<span style='font-size:36px; vertical-align:middle;'>]</span>&nbsp; =&nbsp; {E}</span>"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (ย้ายข้างสมการจากวงนอกสุดเข้าในสุด):</b><br>
                    <b>ขั้นตอนที่ 1: กำจัดเลขวงนอกสุดคือ "× {A}"</b><br>👉 ย้ายข้างไปฝั่งขวา เปลี่ยนคูณเป็นหาร: {E} ÷ {A} = <b>{V1}</b><br>
                    <b>ขั้นตอนที่ 2: กำจัดเลข "- {D}" ออกจากวงเล็บใหญ่</b><br>👉 ย้ายข้างไปฝั่งขวา เปลี่ยนลบเป็นบวก: {V1} + {D} = <b>{V2}</b><br>
                    <b>ขั้นตอนที่ 3: กำจัดส่วน "{C}" (ซึ่งหมายถึงการหาร)</b><br>👉 ย้ายข้างไปฝั่งขวา เปลี่ยนหารเป็นคูณ: {V2} × {C} = <b>{V3}</b><br>
                    <b>ขั้นตอนที่ 4: หาค่าตัวเลขใน 🔲</b><br>👉 ตอนนี้สมการเหลือแค่ 🔲 + {B} = {V3}<br>👉 ย้ายข้างบวกเป็นลบ: {V3} - {B} = <b>{ans_v}</b><br>
                    <b>ตอบ: {ans_v}</b></span>"""
                else:
                    a = random.randint(10, 50)
                    b = random.randint(2, 9)
                    ans_v = random.randint(5, 40)
                    c = (ans_v + a) * b
                    
                    q = f"จงหาตัวเลขที่เติมลงในช่องว่าง:<br><br><span style='font-size:24px; font-weight:bold;'>( 🔲 + {a} ) × {b} = {c}</span>"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: กำจัดตัวเลขนอกวงเล็บก่อน คือ "× {b}"</b><br>👉 นำ {b} ย้ายข้ามเครื่องหมายเท่ากับ จะเปลี่ยนเครื่องหมายจากคูณเป็นหาร: {c} ÷ {b} = <b>{c//b}</b><br>
                    <b>ขั้นตอนที่ 2: หาค่าของตัวเลขใน 🔲</b><br>👉 สมการจะเหลือแค่วงเล็บด้านในคือ: 🔲 + {a} = {c//b}<br>👉 นำ {a} ย้ายไปฝั่งขวา เปลี่ยนบวกเป็นลบ: {c//b} - {a} = <b>{ans_v}</b><br>
                    <b>ตอบ: {ans_v}</b></span>"""

            elif actual_sub_t == "อสมการและค่าที่เป็นไปได้":
                C = random.choice([2, 3, 4, 5])
                ans_list = list(range(random.randint(5, 10), random.randint(12, 18)))
                min_v = ans_list[0]
                max_v = ans_list[-1]
                B = random.randint(3, 8)
                
                if is_challenge:
                    A = (min_v * C) - random.randint(1, C-1)
                    D = (max_v * C) + random.randint(1, C-1)
                    ans = sum(ans_list)
                    
                    f_L = get_vertical_fraction(A, B*C)
                    f_M = get_vertical_fraction("🔲", B)
                    f_R = get_vertical_fraction(D, B*C)
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
                    a = random.randint(10, 50)
                    limit_val = random.randint(80, 150)
                    max_val = limit_val - a - 1
                    
                    q = f"จงหา <b>จำนวนนับที่มากที่สุด</b> ที่เติมในช่องว่าง:<br><br><span style='font-size:24px; font-weight:bold;'>🔲 + {a} &lt; {limit_val}</span>"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: คิดเสมือนว่ามันคือเครื่องหมาย "เท่ากับ" ก่อน</b><br>👉 ถ้าสมการคือ 🔲 + {a} = {limit_val} ➔ 🔲 จะเท่ากับ {limit_val} - {a} = {limit_val-a}<br>
                    <b>ขั้นตอนที่ 2: หาค่าที่มากที่สุดตามเงื่อนไขของอสมการ</b><br>👉 แต่โจทย์ระบุเครื่องหมาย <b>"ต้องน้อยกว่า"</b> {limit_val} <br>👉 ดังนั้นจำนวนนับที่มากที่สุดที่เป็นไปได้ คือการถอยค่าลงมา 1 แต้ม ➔ {limit_val-a} - 1 = <b>{max_val}</b><br>
                    <b>ตอบ: {max_val}</b></span>"""

            elif actual_sub_t == "ปริศนาตัวเลขที่หายไป":
                if is_challenge:
                    Z = random.randint(0, 4)
                    C = random.randint(Z+3, 9)
                    Y = random.randint(0, 4)
                    B = random.randint(Y+3, 9)
                    X = random.randint(5, 9)
                    A = random.randint(1, X-3)
                    
                    Res = int(f"{X}{Y}{Z}") - int(f"{A}{B}{C}")
                    str_Res = str(Res).zfill(3)
                    
                    math_table = get_vertical_math([box_html, str(Y), str(Z)], [str(A), box_html, str(C)], [str_Res[0], str_Res[1], box_html], "−")
                    
                    q = f"จงวิเคราะห์การตั้งลบแบบมีการยืมข้ามหลักต่อไปนี้ แล้วหาว่าตัวเลขที่ซ่อนอยู่ใน 🔲 จาก <b>บนลงล่าง</b> คือเลขใดตามลำดับ?<br>{math_table}"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (แกะรอยการยืมทีละหลัก):</b><br>
                    <b>ขั้นตอนที่ 1: วิเคราะห์หลักหน่วย (ขวาสุด)</b><br>👉 ตัวตั้งคือ {Z} ลบด้วย {C} ซึ่งลบไม่ได้ จึงต้องไปขอยืมหลักสิบมา 10<br>👉 จะกลายเป็น (10 + {Z}) - {C} = <b>{10+Z-C}</b> (นี่คือตัวเลขกล่องล่างสุด)<br>
                    <b>ขั้นตอนที่ 2: วิเคราะห์หลักสิบ (ตรงกลาง)</b><br>👉 เลข {Y} ถูกยืมไป 1 จึงเหลือเพียง {Y-1} แต่ผลลบยังคงน้อยกว่า 🔲 จึงต้องขอยืมหลักร้อยมาอีก 10<br>👉 จะได้สมการ: (10 + {Y-1}) - 🔲 = {str_Res[1]} ➔ นำ {(10+Y-1)} ลบ {str_Res[1]} จะได้กล่องกลางคือ <b>{B}</b><br>
                    <b>ขั้นตอนที่ 3: วิเคราะห์หลักร้อย (ซ้ายสุด)</b><br>👉 เลข 🔲 ถูกหลักสิบยืมไป 1 จึงมีค่าลดลงไป 1<br>👉 จะได้สมการ: (🔲 - 1) - {A} = {str_Res[0]} ➔ ย้ายข้าง 🔲 = {int(str_Res[0])} + {A} + 1 = <b>{X}</b> (นี่คือตัวเลขกล่องบนสุด)<br>
                    <b>ตอบ: กล่องบนคือ {X}, กล่องกลางคือ {B}, กล่องล่างคือ {10+Z-C}</b></span>"""
                else:
                    n2 = random.randint(2, 9)
                    n1 = random.randint(11, 99)
                    ans_val = n1 * n2
                    str_n1 = str(n1)
                    str_ans = str(ans_val)
                    
                    math_table = get_vertical_math([str_n1[0], box_html], [str(n2)], list(str_ans), "×")
                    
                    q = f"จงเติมตัวเลขลงใน 🔲 ให้การคูณนี้ถูกต้อง<br>{math_table}"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: แปลงตารางเป็นสมการแนวนอน</b><br>👉 จากการตั้งคูณ หมายความว่า (จำนวนสองหลักด้านบน) × {n2} = {ans_val}<br>
                    <b>ขั้นตอนที่ 2: ใช้หลักการย้ายข้างสมการเพื่อหาจำนวนนั้น</b><br>👉 ย้าย {n2} ที่กำลังคูณอยู่ ข้ามฝั่งไปเป็นหาร: {ans_val} ÷ {n2} = <b>{n1}</b><br>
                    <b>ขั้นตอนที่ 3: เทียบหาตัวเลขที่หายไป</b><br>👉 จำนวนสองหลักที่คำนวณได้คือ {n1} เมื่อนำไปเทียบกับตาราง ตัวเลขที่หายไปในหลักหน่วยคือ <b>{str_n1[1]}</b><br>
                    <b>ตอบ: {str_n1[1]}</b></span>"""

            elif actual_sub_t == "ความยาวและเส้นรอบรูป":
                if is_challenge:
                    N = random.randint(3, 5)
                    S = random.randint(5, 12)
                    O = random.randint(1, S-2)
                    width = N * S - (N - 1) * O
                    ans = 2 * (width + S)
                    
                    q = f"นำกระดาษรูปสี่เหลี่ยมจัตุรัสที่มีความยาวด้านละ <b>{S} ซม.</b> จำนวน <b>{N} แผ่น</b> มาวางเรียงต่อกันเป็นแนวยาว<br>โดยให้แต่ละแผ่นวางซ้อนทับกันเป็นระยะ <b>{O} ซม.</b> จงหาความยาวรอบรูปทั้งหมดของรูปทรงที่เกิดใหม่นี้?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (หาระยะที่ถูกซ่อน):</b><br>
                    เมื่อนำแผ่นมาวางซ้อนทับกัน รูปทรงใหม่จะกลายเป็นสี่เหลี่ยมผืนผ้ายาวๆ 1 รูป<br>
                    <b>ขั้นตอนที่ 1: หาความยาวแนวนอนของรูปสี่เหลี่ยมผืนผ้าใหม่</b><br>👉 ถ้านำแผ่นกระดาษมาต่อกันเฉยๆ (โดยไม่ให้ซ้อนทับกัน) จะมีความยาว {N} แผ่น × {S} ซม. = {N*S} ซม.<br>👉 แต่ในความจริงมีรอยที่ซ้อนทับกันอยู่ทั้งหมด {N-1} รอย รอยละ {O} ซม. ➔ ทำให้ความยาวหดหายไป {N-1} × {O} = {(N-1)*O} ซม.<br>👉 ความยาวจริงแนวนอน = {N*S} ซม. - {(N-1)*O} ซม. = <b>{width} ซม.</b><br>
                    <b>ขั้นตอนที่ 2: หาความกว้างแนวตั้งของรูปใหม่</b><br>👉 เนื่องจากกระดาษเป็นสี่เหลี่ยมจัตุรัส ความกว้างด้านแนวตั้งจึงยังคงเท่าเดิมคือ <b>{S} ซม.</b><br>
                    <b>ขั้นตอนที่ 3: คำนวณความยาวเส้นรอบรูปทั้งหมด</b><br>👉 สูตรความยาวรอบรูปสี่เหลี่ยมผืนผ้า = 2 × (กว้าง + ยาว) <br>👉 แทนค่า: 2 × ({S} + {width}) = <b>{ans} ซม.</b><br>
                    <b>ตอบ: {ans} ซม.</b></span>"""
                else:
                    side = random.randint(5, 25)
                    leftover = random.randint(5, 20)
                    L = (side * 4) + leftover
                    
                    q = f"นำเส้นลวดที่มีความยาว <b>{L} ซม.</b> ไปดัดสร้างรูปสี่เหลี่ยมจัตุรัส แล้วปรากฏว่า <b>เหลือเศษลวด {leftover} ซม.</b><br>จงหาว่าความยาวของแต่ละด้านของรูปสี่เหลี่ยมจัตุรัสนี้เป็นกี่เซนติเมตร?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: หาลวดส่วนที่ถูกใช้งานจริง</b><br>👉 นำความยาวลวดทั้งหมดตั้ง หักลบด้วยส่วนที่เหลือทิ้งไม่ได้ใช้: {L} - {leftover} = <b>{L-leftover} ซม.</b><br>
                    <b>ขั้นตอนที่ 2: แบ่งความยาวให้ 4 ด้าน</b><br>👉 คุณสมบัติของสี่เหลี่ยมจัตุรัสคือมี 4 ด้านยาวเท่ากันเสมอ<br>👉 นำลวดที่ใช้จริงไปหารเฉลี่ยให้ 4 ด้าน: ({L-leftover}) ÷ 4 = <b>{side} ซม.</b><br>
                    <b>ตอบ: {side} ซม.</b></span>"""

            elif actual_sub_t == "โจทย์ปัญหาเศษส่วนประยุกต์":
                if is_challenge:
                    Y = random.randint(10, 30)
                    R2 = 2 * Y
                    X = random.randint(10, 30)
                    while (R2 + X) % 2 != 0: X += 1
                    R1 = (R2 + X) * 3 // 2
                    Total = R1 * 4 // 3
                    
                    f1_4 = get_vertical_fraction(1, 4)
                    f1_3 = get_vertical_fraction(1, 3)
                    f1_2 = get_vertical_fraction(1, 2)
                    
                    f1_2_s = get_vertical_fraction(1, 2, is_bold=False)
                    f2_3_s = get_vertical_fraction(2, 3, is_bold=False)
                    f3_4_s = get_vertical_fraction(3, 4, is_bold=False)
                    
                    q = f"อ่านหนังสือเล่มหนึ่ง <b>วันแรกอ่านไป {f1_4} ของเล่ม</b><br><b>วันที่สองอ่านไป {f1_3} ของหน้าที่เหลือ</b> และอ่านเพิ่มอีก <b>{X} หน้า</b><br><b>วันที่สามอ่านไป {f1_2} ของหน้าที่เหลือ</b> และอ่านเพิ่มอีก <b>{Y} หน้า</b> ปรากฏว่าอ่านจบเล่มพอดี!<br>จงหาว่าหนังสือเล่มนี้มีทั้งหมดกี่หน้า?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (ย้อนกลับจากวันสุดท้าย):</b><br>
                    โจทย์ที่มีคำว่า "ของหน้าที่เหลือ" ซ้อนกัน ต้องใช้วิธีย้อนกลับจากจุดจบไปหาจุดเริ่มต้นเสมอ!<br>
                    <b>ขั้นตอนที่ 1: ย้อนรอยวันที่ 3</b><br>👉 วันที่สามอ่านไป {f1_2_s} (ครึ่งนึง) แล้วยังต้องอ่านเพิ่มอีก {Y} หน้า จึงจะจบเล่มพอดี<br>👉 แสดงว่า {Y} หน้าที่อ่านทีหลัง ก็คือ 'ครึ่งที่เหลือ' นั่นเอง<br>👉 ยอดหนังสือคงเหลือก่อนเริ่มอ่านวันที่ 3 คือ: {Y} × 2 = <b>{R2} หน้า</b><br>
                    <b>ขั้นตอนที่ 2: ย้อนรอยวันที่ 2</b><br>👉 นำ {X} หน้าที่ถูกอ่าน 'เพิ่ม' ไปในวันที่ 2 มาบวกคืนเข้าไปก่อน: {R2} + {X} = {R2+X} หน้า<br>👉 วันที่สองอ่านไป 1/3 แสดงว่า {R2+X} หน้านี้ คิดเป็น {f2_3_s} ของจำนวนหน้าที่เหลือก่อนอ่านวันที่ 2<br>👉 ยอดหนังสือคงเหลือก่อนเริ่มอ่านวันที่ 2 คือ: ({R2+X} ÷ 2) × 3 = <b>{R1} หน้า</b><br>
                    <b>ขั้นตอนที่ 3: ย้อนรอยวันที่ 1 (หักจากหนังสือทั้งเล่ม)</b><br>👉 วันแรกอ่านไป 1/4 แสดงว่า {R1} หน้าที่เหลือนั้น คิดเป็น {f3_4_s} ของหนังสือทั้งเล่ม<br>👉 จำนวนหน้าหนังสือตั้งต้นทั้งเล่ม คือ: ({R1} ÷ 3) × 4 = <b>{Total} หน้า</b><br>
                    <b>ตอบ: {Total} หน้า</b></span>"""
                else:
                    den = random.choice([4, 5, 6, 8, 10])
                    num = random.randint(1, den-2)
                    total_money = random.randint(10, 50) * den
                    ans_rem = total_money - int((total_money/den)*num)
                    
                    f_html = get_vertical_fraction(num, den)
                    f_s = get_vertical_fraction(num, den, is_bold=False)
                    
                    q = f"มีเงิน <b>{total_money} บาท</b> นำไปซื้อเครื่องเขียน <b>{f_html}</b> ของเงินทั้งหมด จะเหลือเงินกี่บาท?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: หาจำนวนเงินที่ใช้จ่ายไป</b><br>👉 ความหมายของ {f_s} คือการแบ่งเงินทั้งหมดออกเป็น {den} ส่วน และใช้ไป {num} ส่วน<br>👉 เงิน 1 ส่วนเท่ากับ: {total_money} ÷ {den} = {total_money//den} บาท<br>👉 เงินที่ใช้ไปทั้งหมด: {total_money//den} × {num} = <b>{int((total_money/den)*num)} บาท</b><br>
                    <b>ขั้นตอนที่ 2: หาจำนวนเงินที่เหลือ</b><br>👉 นำเงินก้อนตอนแรกสุดตั้ง ลบด้วยเงินที่ใช้จ่ายไป<br>👉 จะได้: {total_money} - {int((total_money/den)*num)} = <b>{ans_rem} บาท</b><br>
                    <b>ตอบ: {ans_rem} บาท</b></span>"""

            elif actual_sub_t == "การคำนวณหน่วยและเวลา":
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
                    <b>ขั้นตอนที่ 1: หาจำนวนวันที่ผ่านไปทั้งหมด</b><br>👉 จาก 08:00 น. วันจันทร์ ถึง 08:00 น. วัน{end_day} นับเวลาที่ผ่านไปได้ <b>{days} วันพอดีเป๊ะ</b><br>
                    <b>ขั้นตอนที่ 2: หาเวลาที่นาฬิกาเดินเพี้ยนไปทั้งหมดสะสม</b><br>👉 เดินเร็วขึ้นวันละ {gain_m} นาที × {days} วัน = <b>เดินเร็วนำหน้าเวลาจริงไป {total_gain} นาที</b><br>
                    <b>ขั้นตอนที่ 3: คำนวณเวลาที่จะแสดงบนหน้าปัด</b><br>👉 แปลงหน่วยนาทีที่เกินมาให้เป็นชั่วโมง: นำ {total_gain} นาที ÷ 60 จะได้ <b>{carry_h} ชั่วโมง กับอีก {final_m} นาที</b><br>👉 นำความคลาดเคลื่อนนี้ไปบวกเพิ่มจากเวลาจริง: 08:00 น. + {carry_h} ชั่วโมง {final_m} นาที = <b>{final_h:02d}:{final_m:02d} น.</b><br>
                    <b>ตอบ: เวลา {final_h:02d}:{final_m:02d} น.</b></span>"""
                else:
                    h1 = random.randint(2, 6)
                    m1 = random.randint(40, 55)
                    h2 = random.randint(1, 4)
                    m2 = random.randint(30, 55)
                    
                    total_m = m1 + m2
                    carry_h = total_m // 60
                    left_m = total_m % 60
                    ans_h = h1 + h2 + carry_h
                    
                    q = f"เดินทางด้วยรถยนต์ใช้เวลา <b>{h1} ชม. {m1} นาที</b> และนั่งเรือต่ออีก <b>{h2} ชม. {m2} นาที</b> รวมใช้เวลาทั้งหมดเท่าไร?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: นำหน่วยนาทีมารวมกันก่อน</b><br>👉 {m1} นาที + {m2} นาที = <b>{total_m} นาที</b><br>
                    <b>ขั้นตอนที่ 2: แปลงนาทีให้เป็นชั่วโมง (ถ้าเกิน 60)</b><br>👉 เนื่องจาก 60 นาที = 1 ชั่วโมง ➔ เราสามารถปัด {total_m} นาที เป็น <b>{carry_h} ชั่วโมง กับอีก {left_m} นาที</b><br>
                    <b>ขั้นตอนที่ 3: นำหน่วยชั่วโมงมารวมกันทั้งหมด</b><br>👉 {h1} ชม. + {h2} ชม. + {carry_h} ชม. (ตัวทดจากนาที) = <b>{ans_h} ชั่วโมง</b><br>
                    <b>ตอบ: {ans_h} ชั่วโมง {left_m:02d} นาที</b></span>"""

            elif actual_sub_t == "โจทย์ปัญหาเปรียบเทียบกลุ่ม":
                if is_challenge:
                    C = random.randint(5, 15)
                    P = random.randint(5, 15)
                    H = P + 3 * C
                    L = 4 * P + 6 * C
                    
                    q = f"ในฟาร์มแห่งหนึ่งมี หมู ไก่ และเป็ด รวมกันทั้งหมด <b>{H} ตัว (นับหัว)</b> และเมื่อนับขาของทุกตัวรวมกันจะได้ <b>{L} ขา</b><br>ถ้าเจ้าของฟาร์มให้ข้อมูลว่า <b>'มีจำนวนเป็ดเป็น 2 เท่าของจำนวนไก่เสมอ'</b><br>จงหาว่าในฟาร์มแห่งนี้มีหมูทั้งหมดกี่ตัว?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (สมการนับหัว-นับขา):</b><br>
                    <b>ขั้นตอนที่ 1: ยุบรวมสัตว์ปีก (ไก่และเป็ด) ให้เป็นกลุ่มเดียวเพื่อความง่าย</b><br>👉 เป็ดเป็น 2 เท่าของไก่ แปลว่าถ้าเราจับมันมัดเป็นเซ็ต: 1 เซ็ตจะมี ไก่ 1 ตัว และ เป็ด 2 ตัว เสมอ (รวมเป็น 3 ตัว/เซ็ต)<br>👉 ขาใน 1 เซ็ต = (ไก่ 1 ตัวมี 2 ขา) + (เป็ด 2 ตัวมี 4 ขา) = <b>6 ขาต่อ 1 เซ็ต</b><br>👉 สรุป: สัตว์ปีก 1 เซ็ต มี 3 ตัว 6 ขา (ซึ่งพอเฉลี่ยแล้ว ก็ตก <b>ตัวละ 2 ขา</b> เท่าเดิม!)<br>
                    <b>ขั้นตอนที่ 2: ตั้งสมมติฐานแบบสุดโต่ง</b><br>👉 สมมติว่าสัตว์ทั้ง {H} ตัวเป็นสัตว์ปีกล้วนๆ เลย จะต้องมีขาทั้งหมด: {H} × 2 = <b>{H*2} ขา</b><br>👉 แต่โจทย์บอกว่ามีขาจริง {L} ขา แสดงว่ามีขา 'เกินมา': {L} - {H*2} = <b>{L - H*2} ขา</b><br>
                    <b>ขั้นตอนที่ 3: หาจำนวนหมูจากขาที่เกินมา</b><br>👉 ขาที่เกินมา ย่อมมาจาก "หมู" เพราะหมูมี 4 ขา ซึ่งมากกว่าสัตว์ปีกอยู่ตัวละ 2 ขา (4 ลบ 2)<br>👉 นำจำนวนขาที่เกินมา หารด้วย 2 จะได้จำนวนหมู: ({L - H*2}) ÷ 2 = <b>{P} ตัว</b><br>
                    <b>ตอบ: มีหมู {P} ตัว</b></span>"""
                else:
                    g1_std = random.randint(10, 15)
                    g1_items = random.randint(5, 9)
                    g2_std = random.randint(16, 22)
                    g2_items = random.randint(3, 5)
                    
                    t1 = g1_std * g1_items
                    t2 = g2_std * g2_items
                    diff = abs(t1 - t2)
                    more_g = "กลุ่มแรก" if t1 > t2 else "กลุ่มที่สอง"
                    
                    q = f"คุณครูแจกสมุดให้เด็กกลุ่มแรก <b>{g1_std} คน คนละ {g1_items} เล่ม</b> และกลุ่มที่สอง <b>{g2_std} คน คนละ {g2_items} เล่ม</b><br>กลุ่มใดได้รับสมุดรวมมากกว่ากัน และมากกว่ากันกี่เล่ม?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: หาจำนวนสมุดของกลุ่มแรก</b><br>👉 นำจำนวนคน × สมุดแต่ละคน: {g1_std} × {g1_items} = <b>{t1} เล่ม</b><br>
                    <b>ขั้นตอนที่ 2: หาจำนวนสมุดของกลุ่มที่สอง</b><br>👉 นำจำนวนคน × สมุดแต่ละคน: {g2_std} × {g2_items} = <b>{t2} เล่ม</b><br>
                    <b>ขั้นตอนที่ 3: เปรียบเทียบและหาผลต่าง</b><br>👉 จะเห็นว่า <b>{more_g}</b> ได้จำนวนสมุดรวมเยอะกว่า<br>👉 หาว่ามากกว่ากันเท่าไร: นำตัวมากตั้งลบตัวน้อย ➔ {max(t1,t2)} - {min(t1,t2)} = <b>{diff} เล่ม</b><br>
                    <b>ตอบ: {more_g} มากกว่าอยู่ {diff} เล่ม</b></span>"""

            elif actual_sub_t == "อัตราส่วนอายุ":
                n1, n2, n3 = random.sample(["พี่", "พ่อ", "แม่", "น้า", "อา", "คุณครู", "นักเรียน"], 3)
                if is_challenge:
                    base = random.randint(3, 8)
                    a_now = base * random.randint(2, 3)
                    b_now = base * random.randint(4, 5)
                    c_now = base * random.randint(6, 8)
                    f = random.choice([4, 5, 6, 10])
                    
                    g1 = math.gcd(a_now, b_now)
                    r1_a = a_now // g1
                    r1_b = b_now // g1
                    
                    g2 = math.gcd(b_now, c_now)
                    r2_b = b_now // g2
                    r2_c = c_now // g2
                    
                    af = a_now + f
                    bf = b_now + f
                    cf = c_now + f
                    g_ans = math.gcd(math.gcd(af, bf), cf)
                    
                    q = f"ปัจจุบัน อัตราส่วนอายุของ <b>{n1} ต่อ {n2} เป็น {r1_a}:{r1_b}</b> และอัตราส่วนอายุของ <b>{n2} ต่อ {n3} เป็น {r2_b}:{r2_c}</b><br>ถ้าปัจจุบัน {n2} อายุ {b_now} ปี จงหาอัตราส่วนอายุของ <b>{n1} : {n2} : {n3}</b> ในอีก {f} ปีข้างหน้า? (ตอบเป็นอัตราส่วนอย่างต่ำ)"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step):</b><br>
                    <b>ขั้นที่ 1: หาอายุปัจจุบันของทุกคน</b><br>👉 {n2} อายุ {b_now} ปี (เทียบจากอัตราส่วน {n1}:{n2} = {r1_a}:{r1_b} จะได้ส่วนละ {b_now//r1_b} ปี) ➔ {n1} = {r1_a}×{b_now//r1_b} = <b>{a_now} ปี</b><br>👉 (เทียบจากอัตราส่วน {n2}:{n3} = {r2_b}:{r2_c} จะได้ส่วนละ {b_now//r2_b} ปี) ➔ {n3} = {r2_c}×{b_now//r2_b} = <b>{c_now} ปี</b><br>
                    <b>ขั้นที่ 2: หาอายุในอีก {f} ปีข้างหน้า</b><br>👉 บวกเพิ่มคนละ {f}: {n1}={af}, {n2}={bf}, {n3}={cf}<br>
                    <b>ขั้นที่ 3: ทำเป็นอัตราส่วนอย่างต่ำ</b><br>👉 นำ ห.ร.ม. ({g_ans}) มาหารตลอด: {af} : {bf} : {cf} ➔ <b>{af//g_ans} : {bf//g_ans} : {cf//g_ans}</b><br>
                    <b>ตอบ: {af//g_ans} : {bf//g_ans} : {cf//g_ans}</b></span>"""
                else:
                    a_now = random.randint(5, 8) if is_p12 else (random.randint(8, 15) if is_p34 else random.randint(12, 25))
                    diff = random.randint(5, 10) if is_p12 else (random.randint(20, 30) if is_p34 else random.randint(25, 40))
                    f = random.choice([3, 4, 5]) if is_p12 else (random.choice([5, 10, 12]) if is_p34 else random.choice([10, 15, 20, 25]))
                    
                    b_now = a_now + diff
                    r1_val = a_now + f
                    r2_val = b_now + f
                    g = math.gcd(r1_val, r2_val)
                    
                    q = f"ปัจจุบัน <b>{n2}</b> อายุ {a_now} ปี และ <b>{n1}</b> อายุ {b_now} ปี อีก {f} ปีในอนาคต อัตราส่วนอายุ <b>{n2} ต่อ {n1}</b> คือเท่าไร? (ทำเป็นอัตราส่วนอย่างต่ำ)"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step):</b><br>
                    <b>ขั้นที่ 1: หาอายุในอนาคตของทั้งสองคน</b><br>👉 ให้นำอายุปัจจุบันมาบวกเพิ่มไปอีก {f} ปี<br>👉 {n2}: {a_now} + {f} = <b>{r1_val} ปี</b><br>👉 {n1}: {b_now} + {f} = <b>{r2_val} ปี</b><br>
                    <b>ขั้นที่ 2: เขียนอัตราส่วนและทอนให้เป็นอย่างต่ำ</b><br>👉 อัตราส่วนอายุ {n2} : {n1} = {r1_val} : {r2_val}<br>👉 นำตัวเลข {g} มาหารทั้งสองจำนวนเพื่อให้เป็นเศษส่วนอย่างต่ำ: ({r1_val}÷{g}) : ({r2_val}÷{g}) = <b>{r1_val//g}:{r2_val//g}</b><br>
                    <b>ตอบ: {r1_val//g}:{r2_val//g}</b></span>"""

            elif actual_sub_t == "การปักเสาและปลูกต้นไม้":
                role = random.choice(BUILDERS)
                action = random.choice(BUILD_ACTIONS)
                loc = random.choice(BUILD_LOCS)
                if is_challenge:
                    d = random.choice([4, 5, 8, 10])
                    length = random.randint(100, 300)
                    while length % d != 0: length += 1
                    ans = ((length // d) + 1) * 2
                    
                    q = f"<b>{role}</b> มีโครงการ<b>{action}</b>บริเวณ <b>'สองฝั่ง'</b> ของถนนเส้นหนึ่งที่มีความยาว <b>{length} เมตร</b> โดยปักห่างกัน <b>{d} เมตร</b> และต้องติดตั้งที่จุดเริ่มต้นและสิ้นสุดด้วย จะใช้สิ่งที่ติดตั้งทั้งหมดกี่จุด?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step):</b><br>
                    <b>ขั้นที่ 1: คำนวณจำนวนจุดของถนนฝั่งเดียวก่อน</b><br>👉 กฎของการติดตั้งบนเส้นตรงที่มีการปิดหัวและท้าย คือ จำนวนจุด = (ระยะทางทั้งหมด ÷ ระยะห่าง) + 1<br>👉 หาจำนวนช่องว่าง: {length} ÷ {d} = {length//d} ช่อง<br>👉 นำไปบวก 1: {length//d} + 1 = <b>{(length//d)+1} จุด</b><br>
                    <b>ขั้นที่ 2: คิดรวมถนนทั้งสองฝั่ง</b><br>👉 เนื่องจากโครงการทำ <b>สองฝั่งของถนน</b> จึงต้องนำจำนวนจุดที่หาได้มาคูณ 2<br>👉 {(length//d)+1} × 2 = <b>{ans} จุด</b><br>
                    <b>ตอบ: {ans} จุด</b></span>"""
                else:
                    d = random.choice([2, 3, 4, 5]) if is_p12 else (random.choice([5, 8, 10, 12]) if is_p34 else random.choice([10, 15, 20, 25]))
                    trees = random.randint(5, 10) if is_p12 else (random.randint(15, 35) if is_p34 else random.randint(40, 100))
                    length = (trees - 1) * d
                    
                    q = f"<b>{role}</b> มีโครงการ<b>{action}</b>ที่<b>{loc}</b> โดยแต่ละจุดห่างกัน <b>{d} เมตร</b> และต้องปักที่จุดเริ่มต้นและสิ้นสุดพอดี ถ้านับรวมได้ <b>{trees} จุด</b> ระยะทางนี้ยาวกี่เมตร?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step):</b><br>
                    <b>ขั้นที่ 1: หาจำนวนช่องว่างระหว่างจุดติดตั้ง</b><br>👉 กฎคือ จำนวนช่องว่าง จะน้อยกว่าจำนวนจุดอยู่ 1 เสมอ (ช่องว่าง = จำนวนจุด - 1)<br>👉 คำนวณ: {trees} - 1 = <b>{trees - 1} ช่องว่าง</b><br>
                    <b>ขั้นที่ 2: หาระยะทางรวมทั้งหมด</b><br>👉 นำจำนวนช่องว่าง × ระยะห่างของแต่ละช่อง<br>👉 คำนวณ: {trees - 1} × {d} = <b>{length} เมตร</b><br>
                    <b>ตอบ: {length} เมตร</b></span>"""

            elif actual_sub_t == "การตัดเชือกพับทบ":
                name = random.choice(NAMES)
                if is_challenge:
                    f = random.randint(3, 5)
                    c = random.randint(3, 6)
                    layers = 2**f
                    ans = layers * c + 1
                    
                    svg_graphic = draw_rope_cutting_svg(layers, c)
                    q = f"<b>{name}</b> นำเชือกมาพับทบครึ่งซ้อนกันไปเรื่อยๆ จำนวน <b>{f} ครั้ง</b> จากนั้นใช้กรรไกรตัดเชือกให้ขาดออก <b>{c} รอยตัด</b> <br>เมื่อคลี่เชือกทั้งหมดออกมา จะได้เศษเชือกชิ้นเล็กชิ้นน้อยรวมทั้งหมดกี่เส้น?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step พร้อมภาพประกอบ):</b><br>
                    <b>ขั้นที่ 1: หาความหนาของเชือก (จำนวนชั้น)</b><br>👉 การพับทบครึ่ง 1 ครั้ง จะทำให้เชือกหนาขึ้นเป็น 2 เท่า<br>👉 เมื่อพับทบ {f} ครั้ง จำนวนชั้นจะเท่ากับ 2 คูณกัน {f} ครั้ง (2<sup>{f}</sup>) = <b>{layers} ชั้น</b><br>
                    <b>ขั้นที่ 2: จำลองการตัดด้วยภาพ</b><br>{svg_graphic}
                    <b>ขั้นที่ 3: คำนวณจำนวนชิ้นที่เพิ่มขึ้นจากการตัด</b><br>👉 เชือกตอนแรกที่ยังไม่ตัดมีสถานะเป็น <b>1 เส้นยาว</b><br>👉 เมื่อเราตัด 1 รอย กรรไกรจะตัดผ่านเชือกทั้ง {layers} ชั้น ทำให้ได้เศษเชือกเพิ่มขึ้นมา รอยละ {layers} เส้น<br>👉 ถ้าตัด {c} รอย จะได้เศษเชือกเพิ่มขึ้น: {layers} × {c} = <b>{layers * c} เส้น</b><br>
                    <b>ขั้นที่ 4: สรุปจำนวนเชือกทั้งหมด</b><br>👉 นำเชือกที่เพิ่มขึ้นมาจากการตัด บวกกับเชือกเส้นตั้งต้น 1 เส้น: {layers * c} + 1 = <b>{ans} เส้น</b><br>
                    <b>ตอบ: {ans} เส้น</b></span>"""
                else:
                    f = 2
                    c = random.randint(2, 4)
                    layers = 2**f
                    ans = layers * c + 1
                    
                    svg_graphic = draw_rope_cutting_svg(layers, c)
                    q = f"<b>{name}</b>นำเชือกมาพับทบครึ่ง <b>{f}</b> ครั้ง จากนั้นตัดให้ขาด <b>{c}</b> รอยตัด เมื่อคลี่ออกมาจะได้เชือกทั้งหมดกี่เส้น?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step พร้อมภาพประกอบ):</b><br>
                    <b>ขั้นที่ 1: หาความหนาของเชือก (จำนวนชั้น)</b><br>👉 พับทบครึ่ง {f} ครั้ง เกิดความหนา = 2 ยกกำลัง {f} = <b>{layers} ชั้น</b><br>
                    <b>ขั้นที่ 2: จำลองการตัดด้วยภาพ</b><br>{svg_graphic}
                    <b>ขั้นที่ 3: คำนวณและสรุป</b><br>👉 ตัด {c} รอย ได้เศษเชือกเพิ่ม = {layers} × {c} = <b>{layers * c} เส้น</b><br>👉 รวมกับเชือกเส้นยาวตั้งต้นที่มีอยู่แล้ว 1 เส้น: {layers * c} + 1 = <b>{ans} เส้น</b><br>
                    <b>ตอบ: {ans} เส้น</b></span>"""

            elif actual_sub_t == "สัตว์ปีนบ่อ":
                animal = random.choice(ANIMALS)
                if is_challenge:
                    u = 5
                    d = 2
                    heavy_d = 4
                    h = random.randint(25, 35)
                    pos = 0
                    days = 0
                    
                    while pos < h:
                        days += 1
                        pos += u
                        if pos >= h: break
                        if days % 3 == 0: pos -= heavy_d
                        else: pos -= d
                        
                    svg_well = draw_well_svg(h, u, d)
                    q = f"<b>{animal}</b>ตกลงไปในบ่อลึก <b>{h} เมตร</b><br>ตอนกลางวันปีนขึ้นได้ <b>{u} เมตร</b> ตอนกลางคืนลื่นตกลง <b>{d} เมตร</b> เสมอ<br>แต่ <b>'ทุกๆ คืนวันที่ 3'</b> ฝนจะตกทำให้ลื่นไถลลงไปถึง <b>{heavy_d} เมตร</b>แทน จงหาว่าจะใช้เวลากี่วันจึงจะปีนพ้นปากบ่อ?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Simulation จำลองเหตุการณ์ด้วยภาพ):</b><br>
                    ข้อนี้สูตรลัดใช้ไม่ได้เพราะมีเงื่อนไขฝนตกแทรกเข้ามา ต้องจำลองสถานการณ์บวกทีละวันอย่างระมัดระวัง!<br>
                    {svg_well}
                    👉 <b>วันที่ 1:</b> ปีนขึ้น {u} ลื่น {d} ➔ ยืนอยู่ที่ <b>{u-d} ม.</b><br>
                    👉 <b>วันที่ 2:</b> ปีนขึ้น {u} (กลายเป็น {u-d+u}) ลื่น {d} ➔ ยืนอยู่ที่ <b>{(u-d)*2} ม.</b><br>
                    👉 <b>วันที่ 3 (ฝนตก):</b> ปีนขึ้น {u} แต่ลื่น {heavy_d} ➔ ยืนอยู่ที่ {(u-d)*2+u-heavy_d} ม.<br>
                    👉 เมื่อจำลองการบวกลบไปเรื่อยๆ จะพบว่าใน <b>วันที่ {days}</b> ตอนกลางวัน เมื่อสัตว์ปีนขึ้นไปอีก {u} เมตร จะก้าวกระโดดพ้นขอบบ่อไปเลย {h} เมตร พอดีเป๊ะ! (ตามภาพด้านบน จึงไม่ต้องรอลื่นลงมาในตอนกลางคืนอีกแล้ว)<br>
                    <b>ตอบ: ใช้เวลา {days} วัน</b></span>"""
                else:
                    u = random.randint(3, 4) if is_p12 else (random.randint(5, 8) if is_p34 else random.randint(10, 15))
                    d = random.randint(1, 2) if is_p12 else (random.randint(2, 4) if is_p34 else random.randint(4, 8))
                    h = random.randint(10, 15) if is_p12 else (random.randint(20, 35) if is_p34 else random.randint(50, 100))
                    
                    net = u - d
                    days = math.ceil((h - u) / net) + 1
                    svg_well = draw_well_svg(h, u, d)
                    
                    q = f"<b>{animal}</b>ตกลงบ่อลึก <b>{h} เมตร</b> กลางวันปีน <b>{u} เมตร</b> กลางคืนลื่น <b>{d} เมตร</b> จะต้องใช้เวลากี่วันจึงจะปีนพ้นปากบ่อ?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step พร้อมภาพประกอบ):</b><br>
                    <b>ขั้นที่ 1: หาการปีนสุทธิใน 1 วัน</b><br>👉 1 วัน (ขึ้นและลง) จะปีนได้จริง: {u} - {d} = <b>{net} เมตร</b><br>
                    <b>ขั้นที่ 2: หักระยะในวันสุดท้ายออกก่อน (จุดหลอกสำคัญ!)</b><br>👉 ในวันสุดท้าย ถ้า{animal}ปีนพ้นปากบ่อไปแล้ว มันจะไม่ลื่นตกลงมาอีก! เราจึงต้องแยกคิดวันสุดท้ายออกมาก่อน<br>
                    {svg_well}
                    👉 <b style="background-color:#d5f5e3; padding:2px 5px;">ระยะทางที่ต้องปีนแบบลื่นไถล คือ: {h} - {u} = {h - u} เมตร</b><br>
                    <b>ขั้นที่ 3: คำนวณเวลาที่ใช้ปีนระยะช่วงแรก</b><br>👉 นำระยะทางโซนลื่นไถล หารด้วย การปีนสุทธิ: {h - u} ÷ {net} = <b>{math.ceil((h - u) / net)} วัน</b><br>
                    <b>ขั้นที่ 4: รวมกับวันสุดท้าย</b><br>👉 นำเวลาโซนลื่นไถล ไปบวกกับ วันสุดท้ายที่กระโดดพ้นบ่ออีก 1 วัน: {math.ceil((h - u) / net)} + 1 = <b>{days} วัน</b><br>
                    <b>ตอบ: {days} วัน</b></span>"""

            elif actual_sub_t == "การความเร็ววิ่งสวนทาง":
                veh = random.choice(VEHICLES)
                if is_challenge:
                    v1 = random.choice([45, 55, 65])
                    v2 = random.choice([45, 55, 65])
                    start_diff = random.randint(1, 2)
                    t = random.randint(2, 4)
                    
                    adv_d = v1 * start_diff
                    meet_d = (v1 + v2) * t
                    total_d = adv_d + meet_d
                    
                    q = f"{veh}สองคันอยู่ห่างกัน <b>{total_d:,} กิโลเมตร</b> <br>คันแรก (วิ่งด้วยความเร็ว <b>{v1} กม./ชม.</b>) ออกเดินทางไปก่อน <b>{start_diff} ชั่วโมง</b><br>จากนั้นคันที่สอง (วิ่งด้วยความเร็ว <b>{v2} กม./ชม.</b>) จึงเริ่มวิ่งสวนทางเข้าหาคันแรก<br>หลังจากคันที่สองเริ่มออกตัว ต้องใช้เวลากี่ชั่วโมง ทั้งสองคันจึงจะวิ่งมาเจอกัน?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step หักระยะทางล่วงหน้า):</b><br>
                    <b>ขั้นที่ 1: หาระยะทางที่คันแรกแอบวิ่งไปก่อน</b><br>👉 สูตร ระยะทาง = ความเร็ว × เวลา ➔ {v1} × {start_diff} = <b>{adv_d} กม.</b><br>
                    <b>ขั้นที่ 2: หาระยะทางที่เหลืออยู่ตอนคันที่สองเพิ่งเริ่มออกตัว</b><br>👉 นำระยะทางทั้งหมด - ระยะทางล่วงหน้า: {total_d} - {adv_d} = <b>{meet_d} กม.</b><br>
                    <b>ขั้นที่ 3: คำนวณเวลาวิ่งเข้าหากัน</b><br>👉 เมื่อวิ่งเข้าหากัน ความเร็วจะเสริมกัน (ความเร็วรวม) = {v1} + {v2} = <b>{v1+v2} กม./ชม.</b><br>👉 สูตร เวลา = ระยะทาง ÷ ความเร็วรวม ➔ {meet_d} ÷ {v1+v2} = <b>{t} ชั่วโมง</b><br>
                    <b>ตอบ: {t} ชั่วโมง</b></span>"""
                else:
                    v1 = random.choice([20, 30, 40])
                    v2 = random.choice([20, 30, 40])
                    t = random.randint(2, 4)
                    d = (v1 + v2) * t
                    
                    q = f"{veh}สองคันอยู่ห่างกัน <b>{d:,} กิโลเมตร</b> กำลังวิ่งสวนทางเข้าหากัน <br>ถ้าคันแรกวิ่งเร็ว <b>{v1} กม./ชม.</b> คันที่สองวิ่งเร็ว <b>{v2} กม./ชม.</b> <br>ต้องใช้เวลาอีกกี่ชั่วโมง ทั้งสองจึงจะวิ่งมาเจอกันพอดี?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step):</b><br>
                    <b>ขั้นที่ 1: หาความเร็วรวม</b><br>👉 เมื่อวิ่งสวนทางเข้าหากัน ความเร็วจะถูกนำมาบวกกัน: {v1} + {v2} = <b>{v1 + v2} กม./ชม.</b><br>
                    <b>ขั้นที่ 2: หาเวลา</b><br>👉 สูตร เวลา = ระยะทาง ÷ ความเร็ว ➔ {d:,} ÷ {v1 + v2} = <b>{t} ชั่วโมง</b><br>
                    <b>ตอบ: {t} ชั่วโมง</b></span>"""

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
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step สมการอัตราการทำงานรวม 3 คน):</b><br>
                    เปลี่ยนจำนวนวันให้เป็น "ปริมาณงานที่ทำได้ใน 1 วัน"<br>
                    <b>ขั้นที่ 1: หาผลงานใน 1 วันของแต่ละคน</b><br>👉 {n1} ทำได้ {f1_s}, {n2} ทำได้ {f2_s}, {n3} ทำได้ {f3_s} ของงานทั้งหมด<br>
                    <b>ขั้นที่ 2: นำผลงานใน 1 วันมาบวกกัน (ทำตัวส่วนให้เท่ากันด้วย ค.ร.น.)</b><br>👉 ค.ร.น. ของ {w1}, {w2}, {w3} คือ {lcm_val}<br>👉 นำมาบวกกัน: {f1_s} + {f2_s} + {f3_s} = {f_sum1} + {f_sum2} + {f_sum3} = {f_total}<br>👉 ทำเป็นเศษส่วนอย่างต่ำ จะได้ผลลัพธ์คือ <b>{f_ans}</b> ของงานทั้งหมด<br>
                    <b>ขั้นที่ 3: พลิกกลับเศษเป็นส่วนเพื่อหาจำนวนวัน</b><br>👉 ความหมายคือ 1 วัน 3 คนช่วยกันทำได้ {f_ans} งาน<br>👉 ดังนั้นต้องใช้เวลา <b>{ans} วัน</b> จึงจะได้งานเต็ม 1 ก้อน (เสร็จสมบูรณ์)<br>
                    <b>ตอบ: {ans} วัน</b></span>"""
                else:
                    pairs = [(3,6,2), (4,12,3), (6,12,4), (10,15,6)]
                    w1, w2, ans = random.choice(pairs)
                    n1, n2 = random.sample(NAMES, 2)
                    
                    q = f"ในการ<b>{action}</b> หากให้ <b>{n1}</b> ทำคนเดียวจะเสร็จใน {w1} วัน แต่ถ้าให้ <b>{n2}</b> ทำคนเดียวจะเสร็จใน {w2} วัน <br>จงหาว่าถ้าช่วยกันทำพร้อมกัน จะเสร็จภายในเวลากี่วัน?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step):</b><br>
                    <b>ขั้นที่ 1: ใช้สูตรลัด 2 คนช่วยกันทำงาน</b><br>👉 สูตร: (เวลาคนแรก × เวลาคนที่สอง) ÷ (เวลาคนแรก + เวลาคนที่สอง)<br>
                    <b>ขั้นที่ 2: แทนค่าตัวเลขลงในสูตร</b><br>👉 ด้านบน (คูณ): {w1} × {w2} = {w1*w2}<br>👉 ด้านล่าง (บวก): {w1} + {w2} = {w1+w2}<br>👉 นำมาหารกัน: {w1*w2} ÷ {w1+w2} = <b>{ans} วัน</b><br>
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
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step หา ค.ร.น. ขั้นสูง):</b><br>
                    โจทย์ที่มีคำว่า "เกิดขึ้นพร้อมกันอีกครั้ง" ให้ใช้การหา ค.ร.น. (คูณร่วมน้อย)<br>
                    <b>ขั้นที่ 1: ตั้งหารสั้นเพื่อหา ค.ร.น.</b><br>👉 นำตัวเลข {l1}, {l2}, {l3}, {l4} มาหา ค.ร.น. จะได้รอบเวลาที่ลงตัวพร้อมกันคือ <b>{lcm} วินาที</b><br>
                    <b>ขั้นที่ 2: แปลงหน่วยวินาทีเป็นนาทีให้เรียบร้อย</b><br>👉 1 นาที มี 60 วินาที ให้นำ {lcm} ÷ 60<br>👉 จะได้ผลลัพธ์เท่ากับ <b>{text_ans}</b> พอดี<br>
                    <b>ตอบ: {text_ans}</b></span>"""
                else:
                    l1, l2, l3 = random.sample([10, 12, 15, 20, 30], 3)
                    lcm = lcm_multiple(l1, l2, l3)
                    
                    q = f"{item_word} 3 ชิ้น ทำงานด้วยจังหวะต่างกัน ชิ้นแรกดังทุกๆ {l1} วินาที, ชิ้นที่สอง {l2} วินาที และชิ้นที่สาม {l3} วินาที <br>ถ้าเพิ่งดังพร้อมกันไป อีกกี่วินาทีข้างหน้าจึงจะดังพร้อมกันอีกครั้ง?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step):</b><br>
                    <b>ขั้นที่ 1: วิเคราะห์โจทย์</b><br>👉 โจทย์ประเภท 'เกิดขึ้นพร้อมกันอีกครั้ง' ให้หา ค.ร.น. (ตัวคูณร่วมน้อย)<br>
                    <b>ขั้นที่ 2: ตั้งหารสั้น</b><br>👉 นำรอบเวลาทั้งหมด ({l1}, {l2}, {l3}) มาหา ค.ร.น. จะได้ผลลัพธ์เท่ากับ <b>{lcm}</b><br>
                    <b>ตอบ: อีก {lcm} วินาที</b></span>"""

            elif actual_sub_t == "เศษส่วนของที่เหลือ":
                item = random.choice(ITEMS)
                if is_challenge:
                    A = random.choice([3, 4, 5])
                    C = random.choice([3, 4, 5])
                    K = random.randint(1, 5) * 10
                    D = (C - 1) * K
                    before_bank = C * K
                    
                    mult = random.randint(5, 10)
                    target = mult * (A - 1)
                    while target <= before_bank:
                        mult += 1
                        target = mult * (A - 1)
                        
                    B = target - before_bank
                    Original = mult * A
                    
                    f1_A = get_vertical_fraction(1, A, is_bold=False)
                    f_rem_A = get_vertical_fraction(A-1, A, is_bold=False)
                    f1_C = get_vertical_fraction(1, C, is_bold=False)
                    f_rem_C = get_vertical_fraction(C-1, C, is_bold=False)
                    frac1 = get_vertical_fraction(1, A)
                    frac2 = get_vertical_fraction(1, C)
                    
                    q = f"<b>{name}</b>มีเงินก้อนหนึ่ง นำไปซื้อขนม <b>{frac1} ของเงินทั้งหมด</b> จากนั้นนำเงินไปซื้อของเล่นอีก <b>{B} บาท</b><br>แล้วนำเงินที่เหลือไปฝากธนาคาร <b>{frac2} ของเงินที่เหลือจากซื้อของเล่น</b><br>ทำให้ตอนนี้เหลือเงินกลับบ้าน <b>{D} บาท</b> จงหาว่าตอนแรกมีเงินกี่บาท?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดย้อนกลับแบบผสมเศษส่วนและจำนวนเต็ม:</b><br>
                    เราจะคิดย้อนจากเหตุการณ์สุดท้ายกลับไปหาจุดเริ่มต้น<br>
                    <b>ขั้นที่ 1: ฉากฝากธนาคาร (ย้อนกลับหาเงินก่อนฝาก)</b><br>👉 ฝากเงินไป {f1_C} ➔ แสดงว่า <b>เหลือเงิน {f_rem_C}</b> ซึ่งเงินที่เหลือนั้นเทียบเท่ากับเงินกลับบ้าน {D} บาท<br>👉 เทียบบัญญัติไตรยางศ์: ถ้า {C-1} ส่วน = {D} บาท ดังนั้น 1 ส่วน = {D//(C-1)} บาท<br>👉 เงินก่อนฝาก (คือเต็ม {C} ส่วน) = ({D} ÷ {C-1}) × {C} = <b>{before_bank} บาท</b><br>
                    <b>ขั้นที่ 2: ฉากซื้อของเล่น (ย้อนกลับหาเงินก่อนซื้อของเล่น)</b><br>👉 จ่ายเงินสดซื้อของเล่นไป {B} บาท ทำให้เหลือเงิน {before_bank} บาท<br>👉 เงินก่อนซื้อของเล่น = นำยอดที่จ่ายไปมาบวกคืน: {before_bank} + {B} = <b>{target} บาท</b><br>
                    <b>ขั้นที่ 3: ฉากซื้อขนม (ย้อนกลับหาเงินก้อนแรกสุด)</b><br>👉 ซื้อขนมไป {f1_A} ➔ แสดงว่า <b>เหลือเงิน {f_rem_A}</b> ซึ่งยอดที่เหลือนั้นเทียบเท่ากับเงิน {target} บาท<br>👉 เทียบบัญญัติไตรยางศ์: ถ้า {A-1} ส่วน = {target} บาท ดังนั้น 1 ส่วน = {target//(A-1)} บาท<br>👉 เงินตั้งต้นแรกสุด (คือเต็ม {A} ส่วน) = ({target} ÷ {A-1}) × {A} = <b>{Original:,} บาท</b><br>
                    <b>ตอบ: {Original:,} บาท</b></span>"""
                else:
                    f1_n, f1_d = random.choice([(2,5), (3,5), (1,4), (3,4), (2,7)])
                    f2_n, f2_d = random.choice([(1,3), (2,3), (1,2), (3,8), (1,4)])
                    k = random.choice([50, 100, 150, 200])
                    
                    lcm_den = f1_d * f2_d
                    tot = k * lcm_den
                    spent1 = (tot * f1_n) // f1_d
                    rem1 = tot - spent1
                    spent2 = (rem1 * f2_n) // f2_d
                    ans = rem1 - spent2
                    
                    f1_html = get_vertical_fraction(f1_n, f1_d)
                    f2_html = get_vertical_fraction(f2_n, f2_d)
                    f1_html_s = get_vertical_fraction(f1_n, f1_d, is_bold=False)
                    f2_html_s = get_vertical_fraction(f2_n, f2_d, is_bold=False)
                    
                    q = f"<b>{name}</b> มีเงินอยู่ {tot:,} บาท นำไปซื้อขนม <b>{f1_html}</b> ของเงินทั้งหมด และนำไปซื้อ<b>{item}</b>อีก <b>{f2_html} ของเงินที่เหลือ</b> <br>จงหาว่าตอนนี้ <b>{name}</b> เหลือเงินกี่บาท?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียดแบบ Step-by-Step:</b><br>
                    ข้อนี้มีจุดหลอกตรงคำว่า <b>"ของเงินที่เหลือ"</b> ต้องคำนวณและหักเงินออกให้เสร็จทีละรอบครับ!<br>
                    <b>ขั้นที่ 1: คำนวณก้อนแรก (ซื้อขนม)</b><br>👉 นำเงินไปซื้อขนม {f1_html_s} ของเงินทั้งหมด ({tot:,} บาท)<br>👉 ซื้อขนม = ({f1_n} × {tot:,}) ÷ {f1_d} = <b>{spent1:,} บาท</b><br>👉 <u>เงินคงเหลือรอบแรก</u> = {tot:,} - {spent1:,} = <b>{rem1:,} บาท</b><br>
                    <b>ขั้นที่ 2: คำนวณก้อนที่สอง (ซื้อ{item})</b><br>👉 นำไปซื้อ {f2_html_s} <b>ของเงินที่เหลือ</b> (ซึ่งก็คือต้องคิดจากยอดที่เหลือคือ {rem1:,} บาท)<br>👉 ซื้อ{item} = ({f2_n} × {rem1:,}) ÷ {f2_d} = <b>{spent2:,} บาท</b><br>
                    <b>ขั้นที่ 3: หาเงินคงเหลือสุทธิ</b><br>👉 นำเงินคงเหลือรอบแรก ลบด้วย เงินที่จ่ายไปในรอบที่สอง: {rem1:,} - {spent2:,} = <b>{ans:,} บาท</b><br>
                    <b>ตอบ: {ans:,} บาท</b></span>"""

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

def generate_cover_html(level, sub_t, num_q, brand_name, is_challenge):
    theme_color = "#8e44ad" if not is_challenge else "#c0392b"
    badge_text = "🔥 ULTIMATE CHALLENGE MODE" if is_challenge else "⭐ TMC Edition"
    icons = '⚔️ 🧠 🏆 🚀' if is_challenge else '🏆 🥇 🧠 💡'
    
    return f"""<!DOCTYPE html><html lang="th"><head><meta charset="utf-8">
    <style>
        .cover-inner {{ width: 100%; height: 100%; padding: 40px; box-sizing: border-box; text-align: left; font-family: 'Sarabun', sans-serif; }}
        .title {{ font-size: 55px; color: #111; font-weight: bold; margin: 0; line-height: 1.2; margin-bottom: 5px; }}
        .subtitle {{ font-size: 35px; color: #7f8c8d; margin-top: 5px; font-weight: bold; }}
        .grade-badge {{ font-size: 24px; color: #333; margin-bottom: 5px; }}
        .topic {{ font-size: 24px; color: #333; margin-bottom: 5px; }}
        .sub-topic {{ font-size: 24px; color: #333; margin-bottom: 15px; }}
        .icons {{ font-size: 35px; margin-bottom: 15px; }}
        .details-badge {{ font-size: 20px; color: #333; margin-bottom: 5px; }}
        .footer {{ font-size: 20px; color: #333; }}
    </style></head><body>
    <div class="cover-inner" style="margin-top: 100px;">
        <h1 class="title">Thailand Math Competition</h1>
        <div class="subtitle">ข้อสอบวิเคราะห์คณิตศาสตร์</div>
        <div class="grade-badge">{level}</div>
        <div class="topic">ข้อสอบรอบคัดเลือก: {sub_t}</div>
        <div class="sub-topic">{badge_text}</div>
        <div class="icons">{icons}</div>
        <div class="details-badge">รวมทั้งหมด {num_q} ข้อ (พร้อมเฉลยละเอียด)</div>
        <div class="footer">ออกแบบและจัดทำโดย: {brand_name}</div>
    </div>
    </body></html>"""

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
st.sidebar.markdown("### 🎨 ตั้งค่าแบรนด์ & หน้าปก")
brand_name = st.sidebar.text_input("🏷️ ชื่อแบรนด์ / ผู้สอน:", value="บ้านทีเด็ด")
include_cover = st.sidebar.checkbox("🎨 สร้างหน้าปก", value=True)

if st.sidebar.button(f"{'🚀 สั่งสร้างข้อสอบระดับ Ultimate Challenge!' if is_challenge else '🚀 สั่งสร้างข้อสอบแข่งขันเดี๋ยวนี้'}", type="primary", use_container_width=True):
    with st.spinner("กำลังออกแบบข้อสอบ วาดภาพกราฟิกประกอบ และจัดทำเฉลยแบบ Step-by-Step..."):
        
        # ส่งตัวแปร 4 ตัวให้ถูกต้อง แก้ไขบั๊กจอแดง 100%
        qs = generate_questions_logic(selected_level, selected_sub, num_input, is_challenge)
        
        html_w = create_page(selected_level, selected_sub, qs, is_key=False, q_margin=q_margin, ws_height=ws_height, brand_name=brand_name, is_challenge=is_challenge)
        html_k = create_page(selected_level, selected_sub, qs, is_key=True, q_margin=q_margin, ws_height=ws_height, brand_name=brand_name, is_challenge=is_challenge)
        html_cover = generate_cover_html(selected_level, selected_sub, num_input, brand_name, is_challenge) if include_cover else ""
        
        st.session_state['worksheet_html'] = html_w
        st.session_state['answerkey_html'] = html_k
        
        ebook_body = ""
        if include_cover: ebook_body += f'\n<div class="a4-wrapper cover-wrapper">{extract_body(html_cover)}</div>\n'
        ebook_body += f'\n<div class="a4-wrapper">{extract_body(html_w)}</div>\n<div class="a4-wrapper">{extract_body(html_k)}</div>\n'
        
        bg_color = "#2c3e50" if is_challenge else "#525659"
        
        full_ebook_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap" rel="stylesheet"><style>@page {{ size: A4; margin: 15mm; }} @media screen {{ body {{ font-family: 'Sarabun', sans-serif; background-color: {bg_color}; display: flex; flex-direction: column; align-items: center; padding: 40px 0; margin: 0; }} .a4-wrapper {{ width: 210mm; min-height: 297mm; background: white; margin-bottom: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.3); padding: 15mm; box-sizing: border-box; }} .cover-wrapper {{ padding: 0; }} }} @media print {{ body {{ font-family: 'Sarabun', sans-serif; background: transparent; padding: 0; display: block; margin: 0; }} .a4-wrapper {{ width: 100%; min-height: auto; margin: 0; padding: 0; box-shadow: none; page-break-after: always; }} .cover-wrapper {{ height: 260mm; }} }} .header {{ text-align: center; border-bottom: 2px solid #333; margin-bottom: 10px; padding-bottom: 10px; }} .header h2 {{ color: {'#c0392b' if is_challenge else '#8e44ad'}; }} .q-box {{ margin-bottom: {q_margin}; padding: 10px 15px; page-break-inside: avoid; font-size: 20px; line-height: 1.8; }} .workspace {{ height: {ws_height}; border: 2px dashed #bdc3c7; border-radius: 8px; margin: 15px 0; padding: 10px; color: #95a5a6; font-size: 16px; background-color: #fafbfc; }} .ans-line {{ margin-top: 10px; border-bottom: 1px dotted #999; width: 80%; height: 30px; font-weight: bold; font-size: 20px; display: flex; align-items: flex-end; padding-bottom: 5px; }} .sol-text {{ color: #333; font-size: 18px; display: block; margin-top: 15px; padding: 15px; background-color: #f5eef8; border-left: 4px solid {'#c0392b' if is_challenge else '#8e44ad'}; border-radius: 4px; line-height: 1.8; }} .page-footer {{ text-align: right; font-size: 14px; color: #95a5a6; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }}</style></head><body>{ebook_body}</body></html>"""

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
    st.success(f"✅ แก้บั๊กจอแดงเรียบร้อย 100%! โค้ดจัดเต็มไม่มีแหว่ง เพิ่มภาพจำลองตัดเชือกและสัตว์ปีนบ่อ พร้อมหน้าปก TMC เรียบร้อยครับ")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📄 โหลดเฉพาะโจทย์", data=st.session_state['worksheet_html'], file_name=f"{st.session_state['filename_base']}_Worksheet.html", mime="text/html", use_container_width=True)
        st.download_button("🔑 โหลดเฉพาะเฉลย", data=st.session_state['answerkey_html'], file_name=f"{st.session_state['filename_base']}_AnswerKey.html", mime="text/html", use_container_width=True)
    with c2:
        st.download_button("📚 โหลดรวมเล่ม E-Book", data=st.session_state['ebook_html'], file_name=f"{st.session_state['filename_base']}_Full_EBook.html", mime="text/html", use_container_width=True)
        st.download_button("🗂️ โหลดแพ็กเกจ (.zip)", data=st.session_state['zip_data'], file_name=f"{st.session_state['filename_base']}.zip", mime="application/zip", use_container_width=True)
    st.markdown("---")
    components.html(st.session_state['ebook_html'], height=800, scrolling=True)
