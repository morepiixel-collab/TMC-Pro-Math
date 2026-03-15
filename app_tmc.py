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

# ==========================================
# 2. ฐานข้อมูลหัวข้อข้อสอบแข่งขัน (TMC 27 หัวข้อ)
# ==========================================
core_topics = [
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
                        n1, n2 = p[0]*100 + p[1]*10 + p[2], p[3]*10 + p[4]
                        if n1 * n2 > max_prod: max_prod = n1 * n2; best_pair = (n1, n2)
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
                    while wrong_ans <= 0: ans_true += 10; wrong_ans = ans_true - (2 * x)
                    q = f"<b>{name}</b> ตั้งใจจะนำจำนวนหนึ่งไป <b>บวก</b> กับ {x} แต่เขาทำผิดโดยนำไป <b>ลบ</b> ด้วย {x} ทำให้ได้ผลลัพธ์เป็น <b>{wrong_ans}</b><br>ผลลัพธ์ที่แท้จริงคือเท่าไร?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: หาตัวเลขตั้งต้นก่อนทำผิด</b><br>👉 สมการที่ทำผิดคือ: 🔲 - {x} = {wrong_ans}<br>👉 ย้ายฝั่งเปลี่ยนลบเป็นบวก จะได้ตัวเลขตั้งต้น: {wrong_ans} + {x} = {wrong_ans+x}<br>
                    <b>ขั้นตอนที่ 2: คำนวณใหม่ให้ถูกต้องตามโจทย์สั่ง</b><br>👉 นำตัวเลขตั้งต้นไปบวก {x}: {wrong_ans+x} + {x} = <b>{ans_true}</b><br>
                    <b>ตอบ: {ans_true}</b></span>"""

            elif actual_sub_t == "การนับตารางเรขาคณิต":
                N, M = random.randint(3, 5), random.randint(4, 7); M = M+1 if N==M else M
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
                    while V3 % C != 0: ans_v += 1; V3 = ans_v + B
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

            elif actual_sub_t == "อัตราส่วนอายุ":
                n1, n2, n3 = random.sample(["พี่", "พ่อ", "แม่", "น้า", "อา", "คุณครู", "นักเรียน"], 3)
                if is_challenge:
                    base = random.randint(3, 8); a_now = base * random.randint(2, 3); b_now = base * random.randint(4, 5); c_now = base * random.randint(6, 8)
                    f = random.choice([4, 5, 6, 10]); g1 = math.gcd(a_now, b_now); r1_a, r1_b = a_now//g1, b_now//g1
                    g2 = math.gcd(b_now, c_now); r2_b, r2_c = b_now//g2, c_now//g2
                    af, bf, cf = a_now+f, b_now+f, c_now+f; g_ans = math.gcd(math.gcd(af, bf), cf)
                    q = f"ปัจจุบัน อัตราส่วนอายุของ <b>{n1} ต่อ {n2} เป็น {r1_a}:{r1_b}</b> และอัตราส่วนอายุของ <b>{n2} ต่อ {n3} เป็น {r2_b}:{r2_c}</b><br>ถ้าปัจจุบัน {n2} อายุ {b_now} ปี จงหาอัตราส่วนอายุของ <b>{n1} : {n2} : {n3}</b> ในอีก {f} ปีข้างหน้า? (ตอบเป็นอัตราส่วนอย่างต่ำ)"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step):</b><br>
                    <b>ขั้นที่ 1: หาอายุปัจจุบันของทุกคน</b><br>
                    👉 {n2} อายุ {b_now} ปี (เทียบจากอัตราส่วน {n1}:{n2} = {r1_a}:{r1_b} จะได้ส่วนละ {b_now//r1_b} ปี) ➔ {n1} = {r1_a}×{b_now//r1_b} = <b>{a_now} ปี</b><br>
                    👉 (เทียบจากอัตราส่วน {n2}:{n3} = {r2_b}:{r2_c} จะได้ส่วนละ {b_now//r2_b} ปี) ➔ {n3} = {r2_c}×{b_now//r2_b} = <b>{c_now} ปี</b><br>
                    <b>ขั้นที่ 2: หาอายุในอีก {f} ปีข้างหน้า</b><br>
                    👉 บวกเพิ่มคนละ {f}: {n1}={af}, {n2}={bf}, {n3}={cf}<br>
                    <b>ขั้นที่ 3: ทำเป็นอัตราส่วนอย่างต่ำ</b><br>
                    👉 นำ ห.ร.ม. ({g_ans}) มาหารตลอด: {af} : {bf} : {cf} ➔ <b>{af//g_ans} : {bf//g_ans} : {cf//g_ans}</b><br>
                    <b>ตอบ: {af//g_ans} : {bf//g_ans} : {cf//g_ans}</b></span>"""
                else:
                    a_now = random.randint(5, 8) if is_p12 else (random.randint(8, 15) if is_p34 else random.randint(12, 25))
                    diff = random.randint(5, 10) if is_p12 else (random.randint(20, 30) if is_p34 else random.randint(25, 40))
                    f = random.choice([3, 4, 5]) if is_p12 else (random.choice([5, 10, 12]) if is_p34 else random.choice([10, 15, 20, 25]))
                    b_now = a_now + diff; r1_val = a_now + f; r2_val = b_now + f; g = math.gcd(r1_val, r2_val)
                    q = f"ปัจจุบัน <b>{n2}</b> อายุ {a_now} ปี และ <b>{n1}</b> อายุ {b_now} ปี อีก {f} ปีในอนาคต อัตราส่วนอายุ <b>{n2} ต่อ {n1}</b> คือเท่าไร? (ทำเป็นอัตราส่วนอย่างต่ำ)"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step):</b><br>
                    <b>ขั้นที่ 1: หาอายุในอนาคตของทั้งสองคน</b><br>
                    👉 ให้นำอายุปัจจุบันมาบวกเพิ่มไปอีก {f} ปี<br>
                    👉 {n2}: {a_now} + {f} = <b>{r1_val} ปี</b><br>
                    👉 {n1}: {b_now} + {f} = <b>{r2_val} ปี</b><br>
                    <b>ขั้นที่ 2: เขียนอัตราส่วนและทอนให้เป็นอย่างต่ำ</b><br>
                    👉 อัตราส่วน {n2}:{n1} เท่ากับ {r1_val}:{r2_val}<br>
                    👉 นำตัวเลข {g} มาหารทั้งสองจำนวนเพื่อให้เป็นเศษส่วนอย่างต่ำ: ({r1_val}÷{g}) : ({r2_val}÷{g}) = <b>{r1_val//g}:{r2_val//g}</b><br>
                    <b>ตอบ: {r1_val//g}:{r2_val//g}</b></span>"""

            elif actual_sub_t == "การปักเสาและปลูกต้นไม้":
                role = random.choice(BUILDERS); action = random.choice(BUILD_ACTIONS); loc = random.choice(BUILD_LOCS)
                if is_challenge:
                    d = random.choice([4, 5, 8, 10]); length = random.randint(100, 300)
                    while length % d != 0: length += 1
                    ans = ((length // d) + 1) * 2
                    q = f"<b>{role}</b> มีโครงการ<b>{action}</b>บริเวณ <b>'สองฝั่ง'</b> ของถนนเส้นหนึ่งที่มีความยาว <b>{length} เมตร</b> โดยปักห่างกัน <b>{d} เมตร</b> และต้องติดตั้งที่จุดเริ่มต้นและสิ้นสุดด้วย จะใช้สิ่งที่ติดตั้งทั้งหมดกี่จุด?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step):</b><br>
                    <b>ขั้นที่ 1: คำนวณจำนวนจุดของถนนฝั่งเดียวก่อน</b><br>
                    👉 กฎของการติดตั้งบนเส้นตรงที่มีการปิดหัวและท้าย คือ จำนวนจุด = (ระยะทางทั้งหมด ÷ ระยะห่าง) + 1<br>
                    👉 หาจำนวนช่องว่าง: {length} ÷ {d} = {length//d} ช่อง<br>
                    👉 นำไปบวก 1: {length//d} + 1 = <b>{(length//d)+1} จุด</b><br>
                    <b>ขั้นที่ 2: คิดรวมถนนทั้งสองฝั่ง</b><br>
                    👉 เนื่องจากโครงการทำ <b>สองฝั่งของถนน</b> จึงต้องนำจำนวนจุดที่หาได้มาคูณ 2<br>
                    👉 {(length//d)+1} × 2 = <b>{ans} จุด</b><br>
                    <b>ตอบ: {ans} จุด</b></span>"""
                else:
                    d = random.choice([2, 3, 4, 5]) if is_p12 else (random.choice([5, 8, 10, 12]) if is_p34 else random.choice([10, 15, 20, 25]))
                    trees = random.randint(5, 10) if is_p12 else (random.randint(15, 35) if is_p34 else random.randint(40, 100))
                    length = (trees - 1) * d
                    q = f"<b>{role}</b> มีโครงการ<b>{action}</b>ที่<b>{loc}</b> โดยแต่ละจุดห่างกัน <b>{d} เมตร</b> และต้องปักที่จุดเริ่มต้นและสิ้นสุดพอดี ถ้านับรวมได้ <b>{trees} จุด</b> ระยะทางนี้ยาวกี่เมตร?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step):</b><br>
                    <b>ขั้นที่ 1: หาจำนวนช่องว่างระหว่างจุดติดตั้ง</b><br>
                    👉 กฎคือ จำนวนช่องว่าง จะน้อยกว่าจำนวนจุดอยู่ 1 เสมอ (ช่องว่าง = จำนวนจุด - 1)<br>
                    👉 คำนวณ: {trees} - 1 = <b>{trees - 1} ช่องว่าง</b><br>
                    <b>ขั้นที่ 2: หาระยะทางรวมทั้งหมด</b><br>
                    👉 นำจำนวนช่องว่าง × ระยะห่างของแต่ละช่อง<br>
                    👉 คำนวณ: {trees - 1} × {d} = <b>{length} เมตร</b><br>
                    <b>ตอบ: {length} เมตร</b></span>"""

            elif actual_sub_t == "เส้นทางที่เป็นไปได้":
                loc1 = random.choice(["บ้าน", "กทม."]); loc2 = random.choice(["ตลาด", "อยุธยา"]); loc3 = random.choice(["โรงเรียน", "เชียงใหม่"])
                if is_challenge:
                    p1 = random.randint(3, 5); p2 = random.randint(2, 4); ans = (p1 * p2) * ((p1 - 1) * (p2 - 1))
                    q = f"มีเส้นทางจาก <b>{loc1} ไป {loc2}</b> จำนวน <b>{p1} สาย</b> และจาก <b>{loc2} ไป {loc3}</b> จำนวน <b>{p2} สาย</b><br>ต้องการเดินทางแบบ <b>ไป-กลับ ({loc1} ➔ {loc3} ➔ {loc1})</b> โดยมีข้อแม้ว่า <b>'ขากลับห้ามใช้เส้นทางเดิมที่เคยใช้ตอนขาไปเด็ดขาด'</b> จะมีรูปแบบการเดินทางไป-กลับทั้งหมดกี่วิธี?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step):</b><br>
                    <b>ขั้นที่ 1: หารูปแบบของขาไป ({loc1} ➔ {loc2} ➔ {loc3})</b><br>
                    👉 ขาไปสามารถเลือกใช้ถนนได้เต็มที่ นำจำนวนสายมาคูณกัน: {p1} × {p2} = <b>{p1 * p2} วิธี</b><br>
                    <b>ขั้นที่ 2: หารูปแบบของขากลับ ({loc3} ➔ {loc2} ➔ {loc1})</b><br>
                    👉 เนื่องจากห้ามซ้ำทางเดิมที่ใช้ตอนขาไป จึงต้องหักถนนออกช่วงละ 1 สาย<br>
                    👉 ถนนช่วงแรกจะเหลือ {p2} - 1 = <b>{p2-1} สาย</b><br>
                    👉 ถนนช่วงสองจะเหลือ {p1} - 1 = <b>{p1-1} สาย</b><br>
                    👉 นำมาคูณกันจะได้รูปแบบขากลับ: {p2-1} × {p1-1} = <b>{(p1-1) * (p2-1)} วิธี</b><br>
                    <b>ขั้นที่ 3: รวมไปและกลับ (ใช้กฎการคูณต่อเนื่อง)</b><br>
                    👉 นำจำนวนวิธีขาไป × จำนวนวิธีขากลับ: {p1 * p2} × {(p1-1) * (p2-1)} = <b>{ans:,} วิธี</b><br>
                    <b>ตอบ: {ans:,} วิธี</b></span>"""
                else:
                    p1, p2, p3 = 2, 2, 1 if is_p12 else (random.randint(3, 4), random.randint(2, 3), random.randint(1, 2) if is_p34 else random.randint(4, 6), random.randint(3, 5), random.randint(2, 4))
                    ans = (p1 * p2) + p3
                    q = f"เดินทางจาก <b>{loc1} ไป {loc2}</b> มีทาง <b>{p1} สาย</b>, จาก <b>{loc2} ไป {loc3}</b> มีทาง <b>{p2} สาย</b> และมีทางด่วนพิเศษจาก <b>{loc1} ไป {loc3}</b> (ไม่ผ่าน {loc2}) อีก <b>{p3} สาย</b> จะมีรูปแบบเดินทางจาก <b>{loc1} ไป {loc3}</b> ทั้งหมดกี่วิธี?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step):</b><br>
                    <b>ขั้นที่ 1: คำนวณเส้นทางปกติ (ที่ขับผ่าน {loc2})</b><br>
                    👉 นำเส้นทางมาคูณกันแบบต่อเนื่อง: {p1} × {p2} = <b>{p1 * p2} วิธี</b><br>
                    <b>ขั้นที่ 2: คำนวณเส้นทางด่วนพิเศษ</b><br>
                    👉 เส้นทางที่ไม่ต้องผ่านตรงกลาง มีให้เลือกใช้ได้เลย = <b>{p3} วิธี</b><br>
                    <b>ขั้นที่ 3: นำเส้นทางทั้งสองกรณีมารวมกัน</b><br>
                    👉 นำผลลัพธ์มาบวกกัน: {p1 * p2} + {p3} = <b>{ans} วิธี</b><br>
                    <b>ตอบ: {ans} วิธี</b></span>"""

            elif actual_sub_t == "คะแนนยิงเป้า":
                if is_challenge:
                    darts = random.randint(4, 5); pool = [10, 5, 3]; miss_penalty = random.randint(1, 2)
                    hits = random.choices(pool, k=darts-1) + [0]; total_score = sum(hits) - miss_penalty
                    q = f"เกมปาลูกดอกมีเป้าคะแนน <b>10, 5, 3</b> ถ้าปาพลาดเป้าจะถูก <b>หัก {miss_penalty} คะแนน</b> <b>{name}</b> ปาลูกดอกทั้งหมด <b>{darts} ครั้ง</b> ได้คะแนนรวม <b>{total_score} คะแนน</b> จงหาว่าเขาปาเข้าเป้าคะแนนใดบ้าง และพลาดกี่ครั้ง? (เรียงจากมากไปน้อย)"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step):</b><br>
                    <b>ขั้นที่ 1: ตั้งสมมติฐานเพื่อหาคะแนนที่แท้จริง</b><br>
                    👉 ลองสมมติว่ามีการปา 'พลาด' 1 ครั้ง (จะได้ 0 คะแนนในตานั้น และต้องถูกหักคะแนนที่สะสมไว้อีก {miss_penalty} คะแนน)<br>
                    👉 แสดงว่า {darts-1} ครั้งที่เหลือที่ปาเข้าเป้า จะต้องทำคะแนนรวมให้ได้เท่ากับ: {total_score} + {miss_penalty} (คืนค่าที่โดนหักไป) = <b>{sum(hits)} คะแนน</b><br>
                    <b>ขั้นที่ 2: จัดกลุ่มตัวเลขหาเป้าที่ปาโดน</b><br>
                    👉 เราต้องหาตัวเลขจากเป้า {pool} จำนวน {darts-1} ตัว ที่รวมกันแล้วได้ {sum(hits)} พอดี<br>
                    👉 เมื่อสุ่มแจกแจงดู จะพบว่ารูปแบบที่ถูกต้องคือ: <b>{' + '.join(map(str, sorted([h for h in hits if h > 0], reverse=True)))} = {sum(hits)}</b><br>
                    <b>ตอบ: เข้าเป้าคะแนน {sorted([h for h in hits if h > 0], reverse=True)} และปาพลาด 1 ครั้ง</b></span>"""
                else:
                    darts = 2 if is_p12 else (3 if is_p34 else random.choice([4, 5]))
                    pool = [10, 5, 2] if is_p12 else ([20, 10, 5, 2] if is_p34 else [50, 20, 10, 5])
                    pool.sort(reverse=True); hits = random.choices(pool, k=darts); total_score = sum(hits); hits.sort(reverse=True)
                    q = f"เกมปาลูกดอก เป้ามีคะแนน <b>{', '.join(map(str, pool))} คะแนน</b> <b>{name}</b> ปาลูกดอก <b>{darts} ครั้ง</b> เข้าเป้าทุกครั้ง ได้คะแนนรวม <b>{total_score} คะแนน</b> จงหาว่าปาเข้าเป้าวงใดบ้าง? (เรียงจากมากไปน้อย)"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step):</b><br>
                    <b>ขั้นที่ 1: ทำความเข้าใจโจทย์</b><br>
                    👉 เราต้องนำตัวเลขจากเป้า {pool} จำนวน {darts} ตัว มาบวกกันให้ได้ยอดรวม {total_score} พอดี (สามารถใช้เป้าซ้ำได้)<br>
                    <b>ขั้นที่ 2: ใช้วิธีสุ่มแจกแจงตัวเลข</b><br>
                    👉 เทคนิค: ให้เริ่มพิจารณาจากตัวเลขที่มีค่ามากที่สุดก่อน เพื่อตัดความเป็นไปได้ออก<br>
                    👉 จะพบว่ามีรูปแบบเดียวที่รวมกันได้ {total_score} พอดีคือ: <b>{' + '.join(map(str, hits))} = {total_score}</b><br>
                    <b>ตอบ: เข้าเป้าคะแนน {hits}</b></span>"""

            elif actual_sub_t == "การนับหน้าหนังสือ":
                publisher = random.choice(PUBLISHERS); book_type = random.choice(DOC_TYPES)
                if is_challenge:
                    target_pages = random.randint(150, 450)
                    if target_pages > 99: total_digits = 9 + 180 + ((target_pages - 99) * 3)
                    else: total_digits = 9 + ((target_pages - 9) * 2)
                    q = f"<b>{publisher}</b> กำลังพิมพ์ตัวเลขหน้าหนังสือ<b>{book_type}</b> โดยเริ่มตั้งแต่หน้า 1 <br>เมื่อพิมพ์เสร็จ พบว่าใช้ตัวเลขโดด (0-9) ไปทั้งหมด <b>{total_digits:,} ตัว</b> <br>จงหาว่าหนังสือเล่มนี้มีทั้งหมดกี่หน้า?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step):</b><br>
                    <b>ขั้นที่ 1: หักตัวเลขโดดของหน้า 1 หลัก และหน้า 2 หลักออกไปก่อน</b><br>
                    👉 หน้า 1 ถึง 9 มี 9 หน้า (ใช้หน้าละ 1 ตัวเลข) = 9 × 1 = 9 ตัว<br>
                    👉 ยอดตัวเลขเหลือ: {total_digits} - 9 = <b>{total_digits - 9} ตัว</b><br>
                    👉 หน้า 10 ถึง 99 มี 90 หน้า (ใช้หน้าละ 2 ตัวเลข) = 90 × 2 = 180 ตัว<br>
                    👉 ยอดตัวเลขเหลือ: {total_digits-9} - 180 = <b>{total_digits - 189} ตัว</b><br>
                    <b>ขั้นที่ 2: คำนวณหาจำนวนหน้า 3 หลัก</b><br>
                    👉 ตัวเลขที่เหลือ {total_digits - 189} ตัว ล้วนเป็นตัวเลขที่นำไปพิมพ์ในหน้า 3 หลัก (หลักร้อย)<br>
                    👉 นำไปหารด้วย 3: {total_digits - 189} ÷ 3 = <b>{(total_digits - 189)//3} หน้า</b><br>
                    <b>ขั้นที่ 3: รวมจำนวนหน้าทั้งหมด</b><br>
                    👉 นำ 9 หน้า (หลักเดียว) + 90 หน้า (สองหลัก) + {(total_digits - 189)//3} หน้า (สามหลัก) = <b>{target_pages} หน้า</b><br>
                    <b>ตอบ: {target_pages} หน้า</b></span>"""
                else:
                    pages = random.randint(20, 50) if is_p12 else (random.randint(100, 250) if is_p34 else random.randint(300, 999))
                    if pages > 99:
                        ans = 9 + 180 + ((pages - 99) * 3)
                        calc_text = f"👉 หน้า 1 ถึง 9 (หน้าละ 1 ตัว): 9 × 1 = <b>9 ตัว</b><br>👉 หน้า 10 ถึง 99 (หน้าละ 2 ตัว): 90 × 2 = <b>180 ตัว</b><br>👉 หน้า 100 ถึง {pages} (หน้าละ 3 ตัว): {pages - 99} × 3 = <b>{(pages - 99) * 3} ตัว</b>"
                        sum_text = f"9 + 180 + {(pages - 99) * 3}"
                    else:
                        ans = 9 + ((pages - 9) * 2)
                        calc_text = f"👉 หน้า 1 ถึง 9 (หน้าละ 1 ตัว): 9 × 1 = <b>9 ตัว</b><br>👉 หน้า 10 ถึง {pages} (หน้าละ 2 ตัว): {pages - 9} × 2 = <b>{(pages - 9) * 2} ตัว</b>"
                        sum_text = f"9 + {(pages - 9) * 2}"
                    q = f"<b>{publisher}</b>พิมพ์<b>{book_type}</b> ความหนารวม <b>{pages}</b> หน้า ต้องพิมพ์เลขหน้ามุมกระดาษตั้งแต่หน้า 1 ถึง {pages} จะใช้ตัวเลขโดดรวมทั้งหมดกี่ตัว?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step):</b><br>
                    <b>ขั้นที่ 1: แบ่งกลุ่มนับตามจำนวนหลักของเลขหน้า</b><br>
                    {calc_text}<br>
                    <b>ขั้นที่ 2: นำตัวเลขของทุกกลุ่มมารวมกัน</b><br>
                    👉 นำมาบวกกัน: {sum_text} = <b>{ans:,} ตัว</b><br>
                    <b>ตอบ: {ans:,} ตัว</b></span>"""

            elif actual_sub_t == "พื้นที่แรเงา (เรขาคณิต)":
                mat = random.choice(MATERIALS)
                if is_challenge:
                    in_r = random.choice([7, 14]); out_s = (in_r * 2) + random.choice([10, 20]); area_sq = out_s ** 2; area_cir = int((22/7) * in_r * in_r); ans = area_sq - area_cir
                    f_pi = get_vertical_fraction(22, 7, is_bold=False)
                    q = f"แผ่น<b>{mat}</b>รูปสี่เหลี่ยมจัตุรัสยาวด้านละ <b>{out_s} ซม.</b> ช่างเจาะรูตรงกลางเป็น 'รูปวงกลม' ที่มีรัศมี <b>{in_r} ซม.</b> ทิ้งไป <br>จงหาพื้นที่ของแผ่น<b>{mat}</b>ส่วนที่เหลือ? (กำหนดให้ π ≈ {f_pi})"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step):</b><br>
                    <b>ขั้นที่ 1: หาพื้นที่สี่เหลี่ยมจัตุรัสแผ่นใหญ่ทั้งหมดก่อน</b><br>
                    👉 สูตร ด้าน × ด้าน = {out_s} × {out_s} = <b>{area_sq:,} ตร.ซม.</b><br>
                    <b>ขั้นที่ 2: หาพื้นที่วงกลมที่เจาะทิ้ง</b><br>
                    👉 สูตร π × รัศมี × รัศมี = {f_pi} × {in_r} × {in_r} = <b>{area_cir:,} ตร.ซม.</b><br>
                    <b>ขั้นที่ 3: คำนวณพื้นที่ส่วนที่เหลือ</b><br>
                    👉 นำพื้นที่ใหญ่ หักลบด้วย พื้นที่รูที่ถูกเจาะทิ้ง: {area_sq:,} - {area_cir:,} = <b>{ans:,} ตร.ซม.</b><br>
                    <b>ตอบ: {ans:,} ตร.ซม.</b></span>"""
                else:
                    out_w = 10 if is_p12 else (random.randint(20, 30) if is_p34 else random.randint(40, 80))
                    out_h = 10 if is_p12 else (random.randint(15, 20) if is_p34 else random.randint(30, 60))
                    in_s = random.randint(2, 4) if is_p12 else (random.randint(4, 8) if is_p34 else random.randint(10, 20))
                    ans = (out_w * out_h) - (in_s**2)
                    q = f"แผ่น<b>{mat}</b>รูปสี่เหลี่ยมผืนผ้า กว้าง <b>{out_w} ซม.</b> ยาว <b>{out_h} ซม.</b> ตัดเจาะรูตรงกลางเป็น 'สี่เหลี่ยมจัตุรัส' ยาวด้านละ <b>{in_s} ซม.</b> ทิ้งไป จงหาพื้นที่ส่วนที่เหลือ?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step):</b><br>
                    <b>ขั้นที่ 1: หาพื้นที่แผ่นสี่เหลี่ยมแผ่นใหญ่ก่อน</b><br>
                    👉 สูตร กว้าง × ยาว = {out_w} × {out_h} = <b>{out_w * out_h:,} ตร.ซม.</b><br>
                    <b>ขั้นที่ 2: หาพื้นที่รูสี่เหลี่ยมจัตุรัสที่ถูกเจาะทิ้ง</b><br>
                    👉 สูตร ด้าน × ด้าน = {in_s} × {in_s} = <b>{in_s**2:,} ตร.ซม.</b><br>
                    <b>ขั้นที่ 3: คำนวณพื้นที่ส่วนที่เหลือ</b><br>
                    👉 นำพื้นที่ใหญ่ ลบด้วย พื้นที่ที่ถูกเจาะทิ้ง: {out_w * out_h:,} - {in_s**2:,} = <b>{ans:,} ตร.ซม.</b><br>
                    <b>ตอบ: {ans:,} ตร.ซม.</b></span>"""

            elif actual_sub_t == "จัดของใส่กล่อง (Modulo)":
                item = random.choice(FRUITS + ITEMS); container = random.choice(CONTAINERS)
                if is_challenge:
                    m1, m2 = 3, 5; rem1, rem2 = random.randint(1, 2), random.randint(1, 4); ans = 0
                    for i in range(1, 200):
                        if i % m1 == rem1 and i % m2 == rem2: ans = i; break
                    if ans == 0: continue
                    q = f"คุณครูมี<b>{item}</b>จำนวนหนึ่ง <br>ถ้าจัดใส่<b>{container}</b>ละ {m1} ชิ้น จะเหลือเศษ <b>{rem1} ชิ้น</b><br>แต่ถ้าเปลี่ยนมาจัดใส่<b>{container}</b>ละ {m2} ชิ้น จะเหลือเศษ <b>{rem2} ชิ้น</b> พอดี จงหาว่าคุณครูมี<b>{item}</b>น้อยที่สุดกี่ชิ้น?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step ทฤษฎีบทเศษเหลือ):</b><br>
                    ใช้วิธีลองไล่ตัวเลข (Listing) ที่ตรงกับเงื่อนไขแรก แล้วเช็กกับเงื่อนไขที่สอง<br>
                    <b>ขั้นที่ 1: หาตัวเลขที่เป็นไปได้จากเงื่อนไขแรก</b><br>
                    👉 จำนวนที่เมื่อจัดทีละ {m1} แล้วเหลือเศษ {rem1} คือการท่องสูตรคูณแม่ {m1} แล้วบวกเศษ<br>
                    👉 จะได้ชุดตัวเลขคือ: {(m1*1)+rem1}, {(m1*2)+rem1}, {(m1*3)+rem1}, {(m1*4)+rem1}, {(m1*5)+rem1}, {(m1*6)+rem1}...<br>
                    <b>ขั้นที่ 2: นำตัวเลขที่ได้มาทดสอบกับเงื่อนไขที่สอง</b><br>
                    👉 นำเลขเหล่านั้นมาลองหารด้วย {m2} ดูว่าตัวไหนเหลือเศษ {rem2} พอดี<br>
                    👉 จะพบว่าตัวเลข <b>ตัวแรกสุด (น้อยที่สุด)</b> ที่ตรงตามเงื่อนไขที่สองด้วยคือ <b>{ans}</b> <br>
                    👉 พิสูจน์: {ans} ÷ {m2} = {ans//m2} เศษ {ans%m2} (ตรงตามเงื่อนไขพอดี!)<br>
                    <b>ตอบ: {ans} ชิ้น</b></span>"""
                else:
                    box_cap = random.randint(3, 5) if is_p12 else (random.randint(8, 12) if is_p34 else random.randint(15, 25))
                    num_boxes = random.randint(5, 10) if is_p12 else (random.randint(15, 25) if is_p34 else random.randint(30, 50))
                    rem = random.randint(1, box_cap - 1); total_items = (box_cap * num_boxes) + rem
                    q = f"มี<b>{item}</b>ทั้งหมด <b>{total_items}</b> ชิ้น จัดใส่<b>{container}</b> ใบละ <b>{box_cap}</b> ชิ้นเท่าๆ กัน จะได้<b>{container}</b>เต็มกี่ใบ? และเหลือเศษกี่ชิ้น?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step):</b><br>
                    <b>ขั้นที่ 1: ใช้การตั้งหารเพื่อแบ่งของเป็นกลุ่มๆ</b><br>
                    👉 นำจำนวนของทั้งหมดตั้ง หารด้วยความจุต่อ 1 ใบ: {total_items} ÷ {box_cap}<br>
                    <b>ขั้นที่ 2: พิจารณาผลลัพธ์และเศษจากการหาร</b><br>
                    👉 ผลลัพธ์จากการหาร (ตัวเลขข้างหน้า) คือจำนวนกล่องที่ใส่ได้เต็มพอดี: <b>{num_boxes} ใบ</b><br>
                    👉 เศษที่เหลือจากการหาร คือจำนวนของที่เหลืออยู่ซึ่งไม่พอใส่กล่องใหม่: <b>{rem} ชิ้น</b><br>
                    <b>ตอบ: ได้เต็ม {num_boxes} ใบ และเหลือเศษ {rem} ชิ้น</b></span>"""

            elif actual_sub_t == "วันที่และปฏิทิน":
                d_th = ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"]
                if is_challenge:
                    s_d, s_idx = random.randint(1, 5), random.randint(0, 6)
                    months = [("มกราคม", 31), ("กุมภาพันธ์", 28), ("มีนาคม", 31), ("เมษายน", 30)]
                    start_m_idx = random.randint(0, 1); target_m_idx = start_m_idx + 2
                    start_month, start_days = months[start_m_idx]; _, mid_days = months[start_m_idx+1]; target_month, _ = months[target_m_idx]
                    t_d = random.randint(10, 20); add_days = (start_days - s_d) + mid_days + t_d; t_idx = (s_idx + (add_days % 7)) % 7
                    q = f"ในปีปกติ (กุมภาพันธ์มี 28 วัน)<br>ถ้าวันที่ <b>{s_d} {start_month}</b> ตรงกับ <b>วัน{d_th[s_idx]}</b> <br>จงหาว่า วันที่ <b>{t_d} {target_month}</b> ของปีเดียวกัน จะตรงกับวันอะไรในสัปดาห์?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step):</b><br>
                    <b>ขั้นที่ 1: หาจำนวนวันทั้งหมดที่ต้องนับเดินหน้า</b><br>
                    👉 วันที่เหลือในเดือน{start_month}: {start_days} - {s_d} = <b>{start_days - s_d} วัน</b><br>
                    👉 จำนวนวันในเดือนถัดไปเต็มเดือน: <b>{mid_days} วัน</b><br>
                    👉 จำนวนวันในเดือนเป้าหมาย ({target_month}): <b>{t_d} วัน</b><br>
                    👉 รวมวันเดินทาง: {start_days - s_d} + {mid_days} + {t_d} = <b>{add_days} วัน</b><br>
                    <b>ขั้นที่ 2: นำไปหารสัปดาห์ (หาร 7)</b><br>
                    👉 {add_days} ÷ 7 = ได้ {add_days//7} สัปดาห์ <b>เศษ {add_days%7} วัน</b><br>
                    <b>ขั้นที่ 3: นับนิ้วเดินหน้าจากวันตั้งต้น</b><br>
                    👉 เริ่มนับต่อจาก วัน{d_th[s_idx]} ไปข้างหน้าอีก {add_days%7} วัน จะตกที่ <b>วัน{d_th[t_idx]}</b> พอดี<br>
                    <b>ตอบ: ตรงกับวัน{d_th[t_idx]}</b></span>"""
                else:
                    s_d, s_idx = random.randint(1, 5), random.randint(0, 6)
                    add = random.randint(7, 15) if is_p12 else (random.randint(20, 45) if is_p34 else random.randint(50, 120))
                    t_idx = (s_idx + (add % 7)) % 7
                    q = f"ถ้าวันที่ <b>{s_d}</b> ของเดือนนี้ ตรงกับ <b>วัน{d_th[s_idx]}</b> พอดี <br>จงหาว่าอีก <b>{add} วันข้างหน้า</b> จะตรงกับวันอะไรในสัปดาห์?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step):</b><br>
                    <b>ขั้นที่ 1: ตัดวันที่เป็นรอบสัปดาห์เต็มๆ ทิ้งไป (หาร 7)</b><br>
                    👉 วันในปฏิทินจะวนลูปซ้ำทุกๆ 7 วัน ดังนั้นให้นำ {add} ÷ 7<br>
                    👉 จะได้ผลลัพธ์คือ {add//7} สัปดาห์ และเหลือ <b>เศษ {add%7} วัน</b><br>
                    <b>ขั้นที่ 2: นับนิ้วเฉพาะเศษที่เหลือ</b><br>
                    👉 เราสนใจแค่ตัวเศษ ให้นับนิ้วเดินหน้าต่อไปจาก วัน{d_th[s_idx]} อีก {add%7} วัน<br>
                    👉 จะตกที่ <b>วัน{d_th[t_idx]}</b><br>
                    <b>ตอบ: วัน{d_th[t_idx]}</b></span>"""

            elif actual_sub_t == "สัตว์ปีนบ่อ":
                animal = random.choice(ANIMALS)
                if is_challenge:
                    u, d = 5, 2; heavy_d = 4; h = random.randint(25, 35); pos = 0; days = 0
                    while pos < h:
                        days += 1; pos += u
                        if pos >= h: break
                        if days % 3 == 0: pos -= heavy_d
                        else: pos -= d
                    q = f"<b>{animal}</b>ตกลงไปในบ่อลึก <b>{h} เมตร</b><br>ตอนกลางวันปีนขึ้นได้ <b>{u} เมตร</b> ตอนกลางคืนลื่นตกลง <b>{d} เมตร</b> เสมอ<br>แต่ <b>'ทุกๆ คืนวันที่ 3'</b> ฝนจะตกทำให้ลื่นไถลลงไปถึง <b>{heavy_d} เมตร</b>แทน จงหาว่าจะใช้เวลากี่วันจึงจะปีนพ้นปากบ่อ?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step จำลองสถานการณ์):</b><br>
                    ข้อนี้สูตรลัดใช้ไม่ได้เพราะมีเงื่อนไขฝนตกแทรกเข้ามา ต้องจำลองสถานการณ์บวกทีละวันอย่างระมัดระวัง!<br>
                    👉 <b>วันที่ 1:</b> ปีนขึ้น {u} ลื่น {d} ➔ ยืนอยู่ที่ <b>{u-d} ม.</b><br>
                    👉 <b>วันที่ 2:</b> ปีนขึ้น {u} (กลายเป็น {u-d+u}) ลื่น {d} ➔ ยืนอยู่ที่ <b>{(u-d)*2} ม.</b><br>
                    👉 <b>วันที่ 3 (ฝนตก):</b> ปีนขึ้น {u} แต่ลื่น {heavy_d} ➔ ยืนอยู่ที่ {(u-d)*2+u-heavy_d} ม.<br>
                    👉 เมื่อจำลองการบวกลบไปเรื่อยๆ จะพบว่าใน <b>วันที่ {days}</b> ตอนกลางวัน เมื่อสัตว์ปีนขึ้นไปอีก {u} เมตร จะพ้นขอบบ่อไปเลย {h} เมตร พอดีเป๊ะ! (จึงไม่ต้องรอลื่นลงมาในตอนกลางคืนอีกแล้ว)<br>
                    <b>ตอบ: ใช้เวลา {days} วัน</b></span>"""
                else:
                    u = random.randint(3, 4) if is_p12 else (random.randint(5, 8) if is_p34 else random.randint(10, 15))
                    d = random.randint(1, 2) if is_p12 else (random.randint(2, 4) if is_p34 else random.randint(4, 8))
                    h = random.randint(10, 15) if is_p12 else (random.randint(20, 35) if is_p34 else random.randint(50, 100))
                    net = u - d; days = math.ceil((h - u) / net) + 1
                    q = f"<b>{animal}</b>ตกลงบ่อลึก <b>{h} เมตร</b> กลางวันปีน <b>{u} เมตร</b> กลางคืนลื่น <b>{d} เมตร</b> จะต้องใช้เวลากี่วันจึงจะปีนพ้นปากบ่อ?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step):</b><br>
                    <b>ขั้นที่ 1: หาการปีนสุทธิใน 1 วัน</b><br>👉 1 วัน (ขึ้นและลง) จะปีนได้จริง: {u} - {d} = <b>{net} เมตร</b><br>
                    <b>ขั้นที่ 2: หักระยะในวันสุดท้ายออกก่อน (จุดหลอก!)</b><br>👉 ในวันสุดท้าย ถ้าปีนพ้นปากบ่อแล้วก็จะไม่ลื่นลงมาอีก! จึงต้องแยกคิด<br>👉 ระยะทางที่ต้องปีนแบบลื่นไถล คือ: {h} - {u} = <b>{h - u} เมตร</b><br>
                    <b>ขั้นที่ 3: คำนวณเวลาที่ใช้ปีนระยะช่วงแรก</b><br>👉 นำระยะช่วงแรกหารด้วยการปีนสุทธิ: {h - u} ÷ {net} = <b>{math.ceil((h - u) / net)} วัน</b><br>
                    <b>ขั้นที่ 4: รวมกับวันสุดท้าย</b><br>👉 นำเวลาช่วงแรก ไปบวกกับ วันสุดท้ายที่กระโดดพ้นบ่ออีก 1 วัน: {math.ceil((h - u) / net)} + 1 = <b>{days} วัน</b><br>
                    <b>ตอบ: {days} วัน</b></span>"""

            elif actual_sub_t == "การตัดเชือกพับทบ":
                name = random.choice(NAMES)
                if is_challenge:
                    f = random.randint(3, 5); c = random.randint(3, 6); layers = 2**f; ans = layers * c + 1
                    svg_graphic = draw_rope_cutting_svg(layers, c)
                    q = f"<b>{name}</b> นำเชือกมาพับทบครึ่งซ้อนกันไปเรื่อยๆ จำนวน <b>{f} ครั้ง</b> จากนั้นใช้กรรไกรตัดเชือกให้ขาดออก <b>{c} รอยตัด</b> <br>เมื่อคลี่เชือกทั้งหมดออกมา จะได้เศษเชือกชิ้นเล็กชิ้นน้อยรวมทั้งหมดกี่เส้น?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step พร้อมภาพประกอบ):</b><br>
                    <b>ขั้นที่ 1: หาความหนาของเชือก (จำนวนชั้น)</b><br>👉 การพับทบครึ่ง 1 ครั้ง จะทำให้เชือกหนาขึ้นเป็น 2 เท่า<br>👉 เมื่อพับทบ {f} ครั้ง จำนวนชั้นจะเท่ากับ 2 คูณกัน {f} ครั้ง (2<sup>{f}</sup>) = <b>{layers} ชั้น</b><br>
                    <b>ขั้นที่ 2: จำลองการตัดด้วยภาพ</b><br>{svg_graphic}
                    <b>ขั้นที่ 3: คำนวณจำนวนชิ้นที่เพิ่มขึ้นจากการตัด</b><br>👉 เชือกตอนแรกที่ยังไม่ตัดมีสถานะเป็น <b>1 เส้นยาว</b><br>👉 เมื่อเราตัด 1 รอย กรรไกรจะตัดผ่านเชือกทั้ง {layers} ชั้น ทำให้ได้เศษเชือกเพิ่มขึ้นมา รอยละ {layers} เส้น<br>👉 ถ้าตัด {c} รอย จะได้เศษเชือกเพิ่มขึ้น: {layers} × {c} = <b>{layers * c} เส้น</b><br>
                    <b>ขั้นที่ 4: สรุปจำนวนเชือกทั้งหมด</b><br>👉 นำเชือกที่เพิ่มขึ้นมาจากการตัด บวกกับเชือกเส้นตั้งต้น 1 เส้น: {layers * c} + 1 = <b>{ans} เส้น</b><br>
                    <b>ตอบ: {ans} เส้น</b></span>"""
                else:
                    f = 2; c = random.randint(2, 4); layers = 2**f; ans = layers * c + 1
                    svg_graphic = draw_rope_cutting_svg(layers, c)
                    q = f"<b>{name}</b>นำเชือกมาพับทบครึ่ง <b>{f}</b> ครั้ง จากนั้นตัดให้ขาด <b>{c}</b> รอยตัด เมื่อคลี่ออกมาจะได้เชือกทั้งหมดกี่เส้น?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step):</b><br>
                    <b>ขั้นที่ 1: หาความหนา</b><br>👉 พับ {f} ครั้ง เกิดความหนา = 2 ยกกำลัง {f} = <b>{layers} ชั้น</b><br>
                    <b>ขั้นที่ 2: จำลองการตัดด้วยภาพ</b><br>{svg_graphic}
                    <b>ขั้นที่ 3: คำนวณและสรุป</b><br>👉 ตัด {c} รอย ได้เส้นเพิ่ม = {layers} × {c} = <b>{layers * c} เส้น</b><br>👉 รวมกับเส้นตั้งต้นที่มีอยู่แล้ว 1 เส้น: {layers * c} + 1 = <b>{ans} เส้น</b><br>
                    <b>ตอบ: {ans} เส้น</b></span>"""

            elif actual_sub_t == "การความเร็ววิ่งสวนทาง":
                veh = random.choice(VEHICLES)
                if is_challenge:
                    v1, v2 = random.choice([45, 55, 65]), random.choice([45, 55, 65]); start_diff = random.randint(1, 2); t = random.randint(2, 4)
                    adv_d = v1 * start_diff; meet_d = (v1 + v2) * t; total_d = adv_d + meet_d
                    q = f"{veh}สองคันอยู่ห่างกัน <b>{total_d:,} กิโลเมตร</b> <br>คันแรก (วิ่งด้วยความเร็ว <b>{v1} กม./ชม.</b>) ออกเดินทางไปก่อน <b>{start_diff} ชั่วโมง</b><br>จากนั้นคันที่สอง (วิ่งด้วยความเร็ว <b>{v2} กม./ชม.</b>) จึงเริ่มวิ่งสวนทางเข้าหาคันแรก<br>หลังจากคันที่สองเริ่มออกตัว ต้องใช้เวลากี่ชั่วโมง ทั้งสองคันจึงจะวิ่งมาเจอกัน?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step หักระยะทางล่วงหน้า):</b><br>
                    <b>ขั้นที่ 1: หาระยะทางที่คันแรกแอบวิ่งไปก่อน</b><br>👉 สูตร ระยะทาง = ความเร็ว × เวลา ➔ {v1} × {start_diff} = <b>{adv_d} กม.</b><br>
                    <b>ขั้นที่ 2: หาระยะทางที่เหลืออยู่ตอนคันที่สองเพิ่งเริ่มออกตัว</b><br>👉 นำระยะทางทั้งหมด - ระยะทางล่วงหน้า: {total_d} - {adv_d} = <b>{meet_d} กม.</b><br>
                    <b>ขั้นที่ 3: คำนวณเวลาวิ่งเข้าหากัน</b><br>👉 เมื่อวิ่งเข้าหากัน ความเร็วจะเสริมกัน (ความเร็วรวม) = {v1} + {v2} = <b>{v1+v2} กม./ชม.</b><br>👉 สูตร เวลา = ระยะทาง ÷ ความเร็วรวม ➔ {meet_d} ÷ {v1+v2} = <b>{t} ชั่วโมง</b><br>
                    <b>ตอบ: {t} ชั่วโมง</b></span>"""
                else:
                    v1, v2 = random.choice([20, 30, 40]), random.choice([20, 30, 40]); t = random.randint(2, 4); d = (v1 + v2) * t
                    q = f"{veh}สองคันอยู่ห่างกัน <b>{d:,} กิโลเมตร</b> กำลังวิ่งสวนทางเข้าหากัน <br>ถ้าคันแรกวิ่งเร็ว <b>{v1} กม./ชม.</b> คันที่สองวิ่งเร็ว <b>{v2} กม./ชม.</b> <br>ต้องใช้เวลาอีกกี่ชั่วโมง ทั้งสองจึงจะวิ่งมาเจอกันพอดี?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step):</b><br>
                    <b>ขั้นที่ 1: หาความเร็วรวม</b><br>👉 เมื่อวิ่งสวนทางเข้าหากัน ความเร็วจะถูกนำมาบวกกัน: {v1} + {v2} = <b>{v1 + v2} กม./ชม.</b><br>
                    <b>ขั้นที่ 2: หาเวลา</b><br>👉 สูตร เวลา = ระยะทาง ÷ ความเร็ว ➔ {d:,} ÷ {v1 + v2} = <b>{t} ชั่วโมง</b><br>
                    <b>ตอบ: {t} ชั่วโมง</b></span>"""

            elif actual_sub_t == "งานและเวลา (Work)":
                action = random.choice(WORK_ACTIONS)
                if is_challenge:
                    n1, n2, n3 = random.sample(NAMES, 3); pairs = [(10, 12, 15, 4), (12, 15, 20, 5), (6, 10, 15, 3), (12, 24, 8, 4)]
                    w1, w2, w3, ans = random.choice(pairs)
                    
                    f1_s = get_vertical_fraction(1, w1, is_bold=False); f2_s = get_vertical_fraction(1, w2, is_bold=False); f3_s = get_vertical_fraction(1, w3, is_bold=False)
                    lcm_val = lcm_multiple(w1, w2, w3); sum_num = (lcm_val//w1) + (lcm_val//w2) + (lcm_val//w3)
                    f_sum1 = get_vertical_fraction(lcm_val//w1, lcm_val, is_bold=False); f_sum2 = get_vertical_fraction(lcm_val//w2, lcm_val, is_bold=False); f_sum3 = get_vertical_fraction(lcm_val//w3, lcm_val, is_bold=False)
                    f_total = get_vertical_fraction(sum_num, lcm_val, is_bold=True); f_ans = get_vertical_fraction(1, ans, is_bold=False)
                    
                    q = f"ในการ<b>{action}</b> หากให้ <b>{n1}</b> ทำคนเดียวจะเสร็จใน {w1} วัน, <b>{n2}</b> ทำคนเดียวเสร็จใน {w2} วัน, และ <b>{n3}</b> ทำคนเดียวเสร็จใน {w3} วัน<br>จงหาว่าถ้าทั้งสามคน 'ช่วยกันทำพร้อมกัน' งานนี้จะเสร็จภายในเวลากี่วัน?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step สมการอัตราการทำงานรวม 3 คน):</b><br>
                    เปลี่ยนจำนวนวันให้เป็น "ปริมาณงานที่ทำได้ใน 1 วัน"<br>
                    <b>ขั้นที่ 1: หาผลงานใน 1 วันของแต่ละคน</b><br>👉 {n1} ทำได้ {f1_s}, {n2} ทำได้ {f2_s}, {n3} ทำได้ {f3_s} ของงานทั้งหมด<br>
                    <b>ขั้นที่ 2: นำผลงานใน 1 วันมาบวกกัน (ทำตัวส่วนให้เท่ากันด้วย ค.ร.น.)</b><br>👉 ค.ร.น. ของ {w1}, {w2}, {w3} คือ {lcm_val}<br>👉 นำมาบวกกัน: {f1_s} + {f2_s} + {f3_s} = {f_sum1} + {f_sum2} + {f_sum3} = {f_total}<br>👉 ทำเป็นเศษส่วนอย่างต่ำ จะได้ผลลัพธ์คือ <b>{f_ans}</b> ของงานทั้งหมด<br>
                    <b>ขั้นที่ 3: พลิกกลับเศษเป็นส่วนเพื่อหาจำนวนวัน</b><br>👉 ความหมายคือ 1 วัน 3 คนช่วยกันทำได้ {f_ans} งาน<br>👉 ดังนั้นต้องใช้เวลา <b>{ans} วัน</b> จึงจะได้งานเต็ม 1 ก้อน (เสร็จสมบูรณ์)<br>
                    <b>ตอบ: {ans} วัน</b></span>"""
                else:
                    pairs = [(3,6,2), (4,12,3), (6,12,4), (10,15,6)]; w1, w2, ans = random.choice(pairs); n1, n2 = random.sample(NAMES, 2)
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
                    ans_min = lcm // 60; ans_sec = lcm % 60
                    text_ans = f"{ans_min} นาที" if ans_sec == 0 else f"{ans_min} นาที {ans_sec} วินาที"
                    q = f"<b>{item_word} 4 ชิ้น</b> ทำงานด้วยจังหวะที่ต่างกัน ดังนี้:<br>ชิ้นที่ 1 ดังทุกๆ {l1} วินาที, ชิ้นที่ 2 ดังทุกๆ {l2} วินาที, ชิ้นที่ 3 ดังทุกๆ {l3} วินาที, และชิ้นที่ 4 ดังทุกๆ {l4} วินาที <br>ถ้าเพิ่งดังพร้อมกันไป อีกกี่นาทีข้างหน้าจึงจะดังพร้อมกันอีกครั้ง?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step หา ค.ร.น. ขั้นสูง):</b><br>
                    โจทย์ที่มีคำว่า "เกิดขึ้นพร้อมกันอีกครั้ง" ให้ใช้การหา ค.ร.น. (คูณร่วมน้อย)<br>
                    <b>ขั้นที่ 1: ตั้งหารสั้นเพื่อหา ค.ร.น.</b><br>👉 นำตัวเลข {l1}, {l2}, {l3}, {l4} มาหา ค.ร.น. จะได้รอบเวลาที่ลงตัวพร้อมกันคือ <b>{lcm} วินาที</b><br>
                    <b>ขั้นที่ 2: แปลงหน่วยวินาทีเป็นนาทีให้เรียบร้อย</b><br>👉 1 นาที มี 60 วินาที ให้นำ {lcm} ÷ 60<br>👉 จะได้ผลลัพธ์เท่ากับ <b>{text_ans}</b> พอดี<br>
                    <b>ตอบ: {text_ans}</b></span>"""
                else:
                    l1, l2, l3 = random.sample([10, 12, 15, 20, 30], 3); lcm = lcm_multiple(l1, l2, l3)
                    q = f"{item_word} 3 ชิ้น ทำงานด้วยจังหวะต่างกัน ชิ้นแรกดังทุกๆ {l1} วินาที, ชิ้นที่สอง {l2} วินาที และชิ้นที่สาม {l3} วินาที <br>ถ้าเพิ่งดังพร้อมกันไป อีกกี่วินาทีข้างหน้าจึงจะดังพร้อมกันอีกครั้ง?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step):</b><br>
                    <b>ขั้นที่ 1: วิเคราะห์โจทย์</b><br>👉 โจทย์ประเภท 'เกิดขึ้นพร้อมกันอีกครั้ง' ให้หา ค.ร.น. (ตัวคูณร่วมน้อย)<br>
                    <b>ขั้นที่ 2: ตั้งหารสั้น</b><br>👉 นำรอบเวลาทั้งหมด ({l1}, {l2}, {l3}) มาหา ค.ร.น. จะได้ผลลัพธ์เท่ากับ <b>{lcm}</b><br>
                    <b>ตอบ: อีก {lcm} วินาที</b></span>"""

            elif actual_sub_t == "นาฬิกาเดินเพี้ยน":
                if is_challenge:
                    days_map = {"พฤหัสบดี": 3, "ศุกร์": 4, "เสาร์": 5}; end_day = random.choice(list(days_map.keys())); days = days_map[end_day]
                    gain_m = random.randint(3, 12); total_gain = days * gain_m
                    carry_h = total_gain // 60; final_m = total_gain % 60; final_h = 8 + carry_h
                    
                    q = f"นาฬิกาเรือนหนึ่งทำงานผิดปกติ โดยจะเดิน <b>'เร็วเกินไป' วันละ {gain_m} นาที</b><br>ถ้าตั้งเวลานาฬิกาเรือนนี้ให้ตรงเป๊ะในตอน <b>08:00 น. ของวันจันทร์</b><br>จงหาว่าเมื่อเวลาจริงดำเนินไปถึง <b>08:00 น. ของวัน{end_day}</b> นาฬิกาเรือนนี้จะชี้บอกเวลาใด?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step คำนวณความคลาดเคลื่อนสะสม):</b><br>
                    <b>ขั้นที่ 1: หาจำนวนวันที่ผ่านไปทั้งหมด</b><br>👉 จาก 08:00 น. วันจันทร์ ถึง 08:00 น. วัน{end_day} นับเวลาที่ผ่านไปได้ <b>{days} วันพอดีเป๊ะ</b><br>
                    <b>ขั้นที่ 2: หาเวลาที่นาฬิกาเดินเพี้ยนไปทั้งหมดสะสม</b><br>👉 เดินเร็วขึ้นวันละ {gain_m} นาที × {days} วัน = <b>เดินเร็วนำหน้าเวลาจริงไป {total_gain} นาที</b><br>
                    <b>ขั้นที่ 3: คำนวณเวลาที่จะแสดงบนหน้าปัด</b><br>👉 แปลงหน่วยนาทีที่เกินมาให้เป็นชั่วโมง: นำ {total_gain} นาที ÷ 60 จะได้ <b>{carry_h} ชั่วโมง กับอีก {final_m} นาที</b><br>👉 นำความคลาดเคลื่อนนี้ไปบวกเพิ่มจากเวลาจริง: 08:00 น. + {carry_h} ชั่วโมง {final_m} นาที = <b>{final_h:02d}:{final_m:02d} น.</b><br>
                    <b>ตอบ: เวลา {final_h:02d}:{final_m:02d} น.</b></span>"""
                else:
                    fast_min = random.randint(3, 8); start_h = 8; passed_hours = random.randint(5, 12); end_h = start_h + passed_hours; total_fast = fast_min * passed_hours
                    q = f"นาฬิกาเรือนหนึ่งเดินเร็วไป <b>{fast_min} นาที ในทุกๆ 1 ชั่วโมง</b> <br>ตั้งเวลาตรงตอน <b>0{start_h}:00 น.</b> เมื่อเวลาจริงผ่านไปถึง <b>{end_h}:00 น.</b> นาฬิกาจะแสดงเวลาใด?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดอย่างละเอียด (Step-by-Step):</b><br>
                    <b>ขั้นที่ 1: หาจำนวนชั่วโมงที่ผ่านไป</b><br>👉 นำเวลาสิ้นสุด ลบ เวลาเริ่มต้น: {end_h} - {start_h} = <b>{passed_hours} ชั่วโมง</b><br>
                    <b>ขั้นที่ 2: หาเวลาที่นาฬิกาเดินเร็วเกินไปทั้งหมด</b><br>👉 เดินเร็วชั่วโมงละ {fast_min} นาที × {passed_hours} ชั่วโมง = <b>{total_fast} นาที</b><br>
                    <b>ขั้นที่ 3: รวมเวลาแสดงผล</b><br>👉 นำเวลาที่เดินเกิน ไปบวกเพิ่มกับเวลาจริง จะได้ <b>{end_h}:{total_fast:02d} น.</b><br>
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

def generate_cover_html(level, sub_t, num_q, brand_name, is_challenge):
    theme_color = "#8e44ad" if not is_challenge else "#c0392b"
    badge_text = "🔥 ULTIMATE CHALLENGE MODE" if is_challenge else "⭐ TMC Edition"
    
    return f"""<!DOCTYPE html><html lang="th"><head><meta charset="utf-8">
    <style>
        .cover-inner {{ width: 100%; height: 100%; padding: 40px; box-sizing: border-box; text-align: center; position: relative; border: 15px solid {theme_color}; background: white; }}
        .title-box {{ margin-top: 80px; }}
        .title {{ font-size: 55px; color: #2c3e50; font-weight: bold; margin: 0; line-height: 1.2; }}
        .subtitle {{ font-size: 35px; color: #7f8c8d; margin-top: 5px; font-weight: bold; }}
        .grade-badge {{ font-size: 40px; background-color: #f1c40f; color: #333; padding: 15px 50px; border-radius: 50px; display: inline-block; font-weight: bold; margin-top: 30px; }}
        .topic {{ font-size: 42px; color: #34495e; margin-top: 70px; font-weight: bold; }}
        .sub-topic {{ font-size: 32px; color: {theme_color}; margin-top: 10px; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);}}
        .icons {{ font-size: 110px; margin: 60px 0; }}
        .details-badge {{ background-color: {theme_color}; color: white; display: inline-block; padding: 15px 40px; border-radius: 15px; font-size: 32px; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}}
        .footer {{ position: absolute; bottom: 40px; left: 0; width: 100%; text-align: center; font-size: 22px; color: #7f8c8d; }}
    </style></head><body>
    <div class="cover-inner">
        <div class="title-box">
            <h1 class="title">Thailand Math Competition</h1>
            <div class="subtitle">ข้อสอบวิเคราะห์คณิตศาสตร์</div>
            <div class="grade-badge">{level}</div>
        </div>
        <div class="topic">ข้อสอบรอบคัดเลือก: {sub_t}</div>
        <div class="sub-topic">{badge_text}</div>
        <div class="icons">{'⚔️ 🧠 🏆 🚀' if is_challenge else '🏆 🥇 🧠 💡'}</div>
        <div class="details-badge">รวมทั้งหมด {num_q} ข้อ (พร้อมเฉลยละเอียด)</div>
        <div class="footer"><b>ออกแบบและจัดทำโดย:</b> {brand_name}</div>
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
        
        # ส่งตัวแปรให้ตรงเป๊ะกับที่ฟังก์ชันต้องการรับ
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
    st.success(f"✅ แก้บั๊กจอแดงเรียบร้อย 100%! ระบบวาดรูปแผนภูมิ, นาฬิกา, ตาชั่ง, และหน้าปก TMC พร้อมลุยแล้วครับ")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📄 โหลดเฉพาะโจทย์", data=st.session_state['worksheet_html'], file_name=f"{st.session_state['filename_base']}_Worksheet.html", mime="text/html", use_container_width=True)
        st.download_button("🔑 โหลดเฉพาะเฉลย", data=st.session_state['answerkey_html'], file_name=f"{st.session_state['filename_base']}_AnswerKey.html", mime="text/html", use_container_width=True)
    with c2:
        st.download_button("📚 โหลดรวมเล่ม E-Book", data=st.session_state['ebook_html'], file_name=f"{st.session_state['filename_base']}_Full_EBook.html", mime="text/html", use_container_width=True)
        st.download_button("🗂️ โหลดแพ็กเกจ (.zip)", data=st.session_state['zip_data'], file_name=f"{st.session_state['filename_base']}.zip", mime="application/zip", use_container_width=True)
    st.markdown("---")
    components.html(st.session_state['ebook_html'], height=800, scrolling=True)
