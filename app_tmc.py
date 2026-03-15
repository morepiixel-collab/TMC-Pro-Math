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

# ==========================================
# 2. ฐานข้อมูลหัวข้อข้อสอบแข่งขัน (27 หัวข้อ)
# ==========================================
core_topics = [
    "การสร้างจำนวนจากเลขโดด", "โจทย์ปัญหาทำผิดเป็นถูก", "การนับตารางเรขาคณิต",
    "ปริศนาสมการช่องว่าง", "อสมการและค่าที่เป็นไปได้", "ปริศนาตัวเลขที่หายไป",         
    "ความยาวและเส้นรอบรูป", "โจทย์ปัญหาเศษส่วนประยุกต์", "การคำนวณหน่วยและเวลา", "โจทย์ปัญหาเปรียบเทียบกลุ่ม",
    "อัตราส่วนอายุ", "การปักเสาและปลูกต้นไม้", "เส้นทางที่เป็นไปได้", 
    "คะแนนยิงเป้า", "การนับหน้าหนังสือ", "พื้นที่แรเงา (เรขาคณิต)", 
    "จัดของใส่กล่อง (Modulo)", "วันที่และปฏิทิน"
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
# 3. Logic Generator (โครงสร้างเต็ม 100%)
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
                    sorted_d = sorted(digits, reverse=True)
                    q = f"<b>{name}</b> ได้รับบัตรตัวเลข 5 ใบ คือ <b>{', '.join(map(str, digits))}</b> นำมาสร้างเป็น <b>จำนวน 3 หลัก</b> และ <b>จำนวน 2 หลัก</b> ที่คูณกันแล้วได้ <b>'ผลคูณที่มีค่ามากที่สุด'</b> ผลคูณนั้นคือเท่าไร?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: เรียงลำดับตัวเลขจากมากไปน้อย</b><br>
                    - นำตัวเลขทั้งหมดมาเรียงจะได้: {sorted_d[0]} > {sorted_d[1]} > {sorted_d[2]} > {sorted_d[3]} > {sorted_d[4]}<br>
                    <b>ขั้นตอนที่ 2: จัดวางตัวเลขเพื่อให้ได้ผลคูณมากที่สุด (หลักการคูณไขว้)</b><br>
                    - เลขที่มากที่สุด ({sorted_d[0]}) ต้องเป็นหลักสิบของตัวคูณ<br>
                    - เลขที่มากรองลงมา ({sorted_d[1]}) ต้องเป็นหลักร้อยของตัวตั้ง<br>
                    - เลขที่มากอันดับสาม ({sorted_d[2]}) วางเป็นหลักสิบของตัวตั้ง เพื่อคูณไขว้กับ {sorted_d[0]}<br>
                    - เลขที่มากอันดับสี่ ({sorted_d[3]}) วางเป็นหลักหน่วยของตัวคูณ เพื่อไปคูณกับก้อนตัวตั้งที่ใหญ่ที่สุด<br>
                    - เลขที่น้อยที่สุด ({sorted_d[4]}) วางเป็นหลักหน่วยของตัวตั้ง<br>
                    <b>ขั้นตอนที่ 3: ประกอบร่างตัวเลขและหาผลคูณ</b><br>
                    - จะได้ตัวเลขคือ {best_pair[0]} และ {best_pair[1]}<br>
                    - นำมาคูณกัน: {best_pair[0]} × {best_pair[1]} = <b>{max_prod:,}</b><br>
                    <b>ตอบ: {max_prod:,}</b></span>"""
                else:
                    digits = random.sample(range(1, 10), 3 if is_p12 else 4)
                    max_v = int("".join(map(str, sorted(digits, reverse=True))))
                    min_v = int("".join(map(str, sorted(digits))))
                    q = f"มีบัตรตัวเลข <b>{', '.join(map(str, digits))}</b> จงหาผลต่างของจำนวนที่ <b>มากที่สุด</b> และ <b>น้อยที่สุด</b> ที่สร้างได้?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: สร้างจำนวนที่มากที่สุด</b><br>
                    - นำตัวเลขมาเรียงจากมากไปน้อย จะได้ <b>{max_v}</b><br>
                    <b>ขั้นตอนที่ 2: สร้างจำนวนที่น้อยที่สุด</b><br>
                    - นำตัวเลขมาเรียงจากน้อยไปมาก จะได้ <b>{min_v}</b><br>
                    <b>ขั้นตอนที่ 3: หาผลต่าง</b><br>
                    - นำจำนวนที่มากที่สุดตั้ง ลบด้วยจำนวนที่น้อยที่สุด: {max_v} - {min_v} = <b>{max_v-min_v}</b><br>
                    <b>ตอบ: {max_v-min_v}</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "โจทย์ปัญหาทำผิดเป็นถูก":
                A, B = random.randint(3, 8), random.randint(5, 20)
                if is_challenge:
                    X = random.randint(5, 12) * A
                    wrong_ans = (X // A) + B
                    correct_ans = (X * A) - B
                    f_q = get_vertical_fraction('ปริศนา', A)
                    f_s = get_vertical_fraction('🔲', A, is_bold=False)
                    q = f"<b>{name}</b> ตั้งใจจะนำจำนวนปริศนาไป <b>คูณด้วย {A}</b> แล้ว <b>ลบออกด้วย {B}</b><br>แต่เขาทำผิดพลาด สลับไปเขียนในรูปเศษส่วนคือ <b>{f_q}</b> แล้วค่อย <b>บวกเพิ่ม {B}</b> ทำให้ได้ผลลัพธ์เป็น <b>{wrong_ans}</b><br>จงหาผลลัพธ์ที่แท้จริงตามความตั้งใจแรก?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: จำลองสมการที่ทำผิดเพื่อหาตัวเลขเริ่มต้น</b><br>
                    - สิ่งที่โจทย์ทำผิดคือ: {f_s} + {B} = {wrong_ans}<br>
                    <b>ขั้นตอนที่ 2: ใช้หลักการคิดย้อนกลับ (Reverse Engineering)</b><br>
                    - ย้อนกลับการบวกเป็นลบ: {wrong_ans} - {B} = {wrong_ans - B} (หมายความว่า {f_s} = {wrong_ans - B})<br>
                    - ย้อนกลับเศษส่วน(การหาร)เป็นคูณ: นำ {wrong_ans - B} × {A} = {X}<br>
                    - จะได้ 'จำนวนปริศนา' คือ <b>{X}</b><br>
                    <b>ขั้นตอนที่ 3: คิดเลขใหม่ให้ถูกต้องตามความตั้งใจแรก</b><br>
                    - นำจำนวนปริศนาไปคูณ {A}: {X} × {A} = {X * A}<br>
                    - นำผลลัพธ์ไปลบ {B}: {X * A} - {B} = <b>{correct_ans:,}</b><br>
                    <b>ตอบ: {correct_ans:,}</b></span>"""
                else:
                    x = random.randint(5, 20); ans_true = random.randint(30, 80); wrong_ans = ans_true - (2 * x)
                    while wrong_ans <= 0: ans_true += 10; wrong_ans = ans_true - (2 * x)
                    q = f"<b>{name}</b> ตั้งใจจะนำจำนวนหนึ่งไป <b>บวก</b> กับ {x} แต่เขาทำผิดโดยนำไป <b>ลบ</b> ด้วย {x} ทำให้ได้ผลลัพธ์เป็น <b>{wrong_ans}</b><br>ผลลัพธ์ที่แท้จริงคือเท่าไร?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: หาตัวเลขตั้งต้นก่อนทำผิด</b><br>
                    - สมการที่ทำผิดคือ: 🔲 - {x} = {wrong_ans}<br>
                    - ย้ายฝั่งเปลี่ยนลบเป็นบวก จะได้ตัวเลขตั้งต้น: {wrong_ans} + {x} = {wrong_ans+x}<br>
                    <b>ขั้นตอนที่ 2: คำนวณใหม่ให้ถูกต้องตามโจทย์สั่ง</b><br>
                    - นำตัวเลขตั้งต้นไปบวก {x}: {wrong_ans+x} + {x} = <b>{ans_true}</b><br>
                    <b>ตอบ: {ans_true}</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "การนับตารางเรขาคณิต":
                N, M = random.randint(3, 5), random.randint(4, 7); M = M+1 if N==M else M
                if is_challenge:
                    total_rect = (N*(N+1)//2) * (M*(M+1)//2)
                    total_sq = sum((N-i)*(M-i) for i in range(min(N, M)))
                    q = f"วาดตารางเป็นรูปสี่เหลี่ยมผืนผ้าขนาด <b>{N} × {M}</b> ช่อง จงหาว่ามี <b>'สี่เหลี่ยมผืนผ้าที่ไม่ใช่สี่เหลี่ยมจัตุรัส'</b> ซ่อนอยู่ทั้งหมดกี่รูป?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    สูตรหลัก: (จำนวนสี่เหลี่ยมผืนผ้าทั้งหมด) - (จำนวนสี่เหลี่ยมจัตุรัสทั้งหมด)<br>
                    <b>ขั้นตอนที่ 1: หาจำนวนสี่เหลี่ยมรวมทุกชนิด (สูตรนับผืนผ้า)</b><br>
                    - ผลบวกความกว้าง: 1+2+...+{N} = {N*(N+1)//2}<br>
                    - ผลบวกความยาว: 1+2+...+{M} = {M*(M+1)//2}<br>
                    - นำมาคูณกัน: {N*(N+1)//2} × {M*(M+1)//2} = <b>{total_rect:,} รูป</b><br>
                    <b>ขั้นตอนที่ 2: หาจำนวนสี่เหลี่ยมจัตุรัสทั้งหมด</b><br>
                    - ใช้สูตรลดทอนทีละ 1 แล้วคูณบวกกัน: ({N}×{M}) + ({N-1}×{M-1}) + ... ไปเรื่อยๆ จนกว่าด้านใดจะเหลือ 1<br>
                    - คำนวณผลรวมจะได้ทั้งหมด <b>{total_sq:,} รูป</b><br>
                    <b>ขั้นตอนที่ 3: หักล้างกัน</b><br>
                    - {total_rect:,} - {total_sq:,} = <b>{total_rect - total_sq:,} รูป</b><br>
                    <b>ตอบ: {total_rect - total_sq:,} รูป</b></span>"""
                else:
                    grid = random.randint(2, 4) if is_p12 else random.randint(4, 6)
                    ans = sum(i*i for i in range(1, grid+1))
                    q = f"มีตารางกระดานขนาด <b>{grid} × {grid}</b> ช่อง จงหาว่ามี <b>'สี่เหลี่ยมจัตุรัส'</b> ซ่อนอยู่ทั้งหมดกี่รูป?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: ใช้สูตรลัดนับตารางจัตุรัสสมมาตร</b><br>
                    - ให้นำขนาดของตารางมายกกำลังสองทีละตัว แล้วนำมาบวกกันตั้งแต่ 1² จนถึง {grid}²<br>
                    <b>ขั้นตอนที่ 2: คำนวณตัวเลข</b><br>
                    - สมการ: 1² + 2² + ... + {grid}²<br>
                    - ผลรวมทั้งหมดจะได้เท่ากับ <b>{ans:,} รูป</b><br>
                    <b>ตอบ: {ans:,} รูป</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "ปริศนาสมการช่องว่าง":
                ans_v, B, C = random.randint(5, 20), random.randint(2, 10), random.randint(2, 5)
                if is_challenge:
                    V3 = ans_v + B
                    while V3 % C != 0: ans_v += 1; V3 = ans_v + B
                    V2 = V3 // C
                    D = random.randint(1, V2 - 1) if V2 > 1 else 1
                    V1 = V2 - D if V2 > D else 1
                    A = random.randint(2, 6); E = A * V1
                    f_html = get_vertical_fraction(f'( 🔲 + {B} )', C)
                    q = f"จงหาตัวเลขที่เติมลงในช่องว่าง:<br><br><span style='font-size:24px; font-weight:bold;'>{A} × &nbsp;<span style='font-size:36px; vertical-align:middle;'>[</span>&nbsp; {f_html} &nbsp;−&nbsp; {D} &nbsp;<span style='font-size:36px; vertical-align:middle;'>]</span>&nbsp; =&nbsp; {E}</span>"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (ย้ายข้างสมการจากนอกเข้าใน):</b><br>
                    <b>ขั้นตอนที่ 1: กำจัดเลขวงนอกสุดคือ "× {A}"</b><br>
                    - ย้ายข้างไปฝั่งขวา เปลี่ยนคูณเป็นหาร: {E} ÷ {A} = <b>{V1}</b><br>
                    <b>ขั้นตอนที่ 2: กำจัดเลข "- {D}" ออกจากวงเล็บ</b><br>
                    - ย้ายข้างไปฝั่งขวา เปลี่ยนลบเป็นบวก: {V1} + {D} = <b>{V2}</b><br>
                    <b>ขั้นตอนที่ 3: กำจัดส่วน "{C}" (การหาร)</b><br>
                    - ย้ายข้างไปฝั่งขวา เปลี่ยนหารเป็นคูณ: {V2} × {C} = <b>{V3}</b><br>
                    <b>ขั้นตอนที่ 4: หาค่าตัวเลขใน 🔲</b><br>
                    - ตอนนี้สมการเหลือแค่ 🔲 + {B} = {V3}<br>
                    - ย้ายข้างบวกเป็นลบ: {V3} - {B} = <b>{ans_v}</b><br>
                    <b>ตอบ: {ans_v}</b></span>"""
                else:
                    a = random.randint(10, 50); b = random.randint(2, 9); ans_v = random.randint(5, 40); c = (ans_v + a) * b
                    q = f"จงหาตัวเลขที่เติมลงในช่องว่าง:<br><br><span style='font-size:24px; font-weight:bold;'>( 🔲 + {a} ) × {b} = {c}</span>"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: กำจัดตัวเลขนอกวงเล็บก่อน คือ "× {b}"</b><br>
                    - นำ {b} ย้ายข้ามเครื่องหมายเท่ากับ จะเปลี่ยนเป็นหาร: {c} ÷ {b} = <b>{c//b}</b><br>
                    <b>ขั้นตอนที่ 2: หาค่าของตัวเลขใน 🔲</b><br>
                    - สมการจะเหลือแค่: 🔲 + {a} = {c//b}<br>
                    - นำ {a} ย้ายไปเป็นลบ: {c//b} - {a} = <b>{ans_v}</b><br>
                    <b>ตอบ: {ans_v}</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "อสมการและค่าที่เป็นไปได้":
                C = random.choice([2, 3, 4, 5]); ans_list = list(range(random.randint(5, 10), random.randint(12, 18)))
                min_v, max_v = ans_list[0], ans_list[-1]; B = random.randint(3, 8)
                if is_challenge:
                    A = (min_v * C) - random.randint(1, C-1); D = (max_v * C) + random.randint(1, C-1)
                    f_L = get_vertical_fraction(A, B*C); f_M = get_vertical_fraction("🔲", B); f_R = get_vertical_fraction(D, B*C)
                    f_sol_M1 = get_vertical_fraction(f"🔲 × {C}", f"{B} × {C}", color="#2c3e50", is_bold=False)
                    q = f"จงหา <b>'ผลบวกของจำนวนนับทุกจำนวน'</b> ที่สามารถเติมในช่องว่างแล้วทำให้อสมการเป็นจริง:<br><br><span style='font-size:24px; font-weight:bold;'>{f_L} &nbsp;&lt;&nbsp; {f_M} &nbsp;&lt;&nbsp; {f_R}</span>"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (อสมการเศษส่วน):</b><br>
                    <b>ขั้นตอนที่ 1: ทำให้ตัวส่วนเท่ากันทั้งหมด</b><br>
                    - สังเกตว่าเศษส่วนตรงกลางมีส่วนเป็น {B} แต่ซ้ายและขวามีส่วนเป็น {B*C}<br>
                    - ต้องนำ {C} มาคูณทั้งตัวเศษและตัวส่วนของก้อนกลาง จะได้เป็น {f_sol_M1}<br>
                    <b>ขั้นตอนที่ 2: เปรียบเทียบเฉพาะตัวเศษด้านบน</b><br>
                    - เมื่อส่วนเท่ากันหมดแล้ว อสมการจะกลายเป็น: {A} &lt; 🔲 × {C} &lt; {D}<br>
                    <b>ขั้นตอนที่ 3: หาจำนวนนับที่เป็นไปได้</b><br>
                    - ต้องหาว่ามีเลขอะไรที่คูณ {C} แล้วมีค่าอยู่ระหว่าง {A} ถึง {D}<br>
                    - เลขที่สอดคล้องเงื่อนไขคือ: {ans_list}<br>
                    <b>ขั้นตอนที่ 4: หาผลบวกตามที่โจทย์ถาม</b><br>
                    - นำตัวเลขทั้งหมดมาบวกกัน: {' + '.join(map(str, ans_list))} = <b>{sum(ans_list)}</b><br>
                    <b>ตอบ: {sum(ans_list)}</b></span>"""
                else:
                    a = random.randint(10, 50); limit_val = random.randint(80, 150)
                    q = f"จงหา <b>จำนวนนับที่มากที่สุด</b> ที่เติมในช่องว่าง:<br><br><span style='font-size:24px; font-weight:bold;'>🔲 + {a} &lt; {limit_val}</span>"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: คิดเสมือนว่ามันคือเครื่องหมาย "เท่ากับ" ก่อน</b><br>
                    - ถ้า 🔲 + {a} = {limit_val} ➔ 🔲 จะเท่ากับ {limit_val} - {a} = {limit_val-a}<br>
                    <b>ขั้นตอนที่ 2: หาค่าที่มากที่สุดตามเงื่อนไข</b><br>
                    - แต่โจทย์กำหนดว่า <b>"ต้องน้อยกว่า"</b> {limit_val} <br>
                    - ดังนั้นจำนวนนับที่มากที่สุดที่เป็นไปได้ คือการถอยลงมา 1 แต้ม ➔ {limit_val-a} - 1 = <b>{limit_val-a-1}</b><br>
                    <b>ตอบ: {limit_val-a-1}</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "ปริศนาตัวเลขที่หายไป":
                if is_challenge:
                    Z = random.randint(0, 4); C = random.randint(Z+3, 9)
                    Y = random.randint(0, 4); B = random.randint(Y+3, 9)
                    X = random.randint(5, 9); A = random.randint(1, X-3)
                    Res = int(f"{X}{Y}{Z}") - int(f"{A}{B}{C}"); str_Res = str(Res).zfill(3)
                    math_table = get_vertical_math([box_html, str(Y), str(Z)], [str(A), box_html, str(C)], [str_Res[0], str_Res[1], box_html], "−")
                    q = f"จงวิเคราะห์การตั้งลบแบบมีการยืมข้ามหลักต่อไปนี้ แล้วหาว่าตัวเลขที่ซ่อนอยู่ใน 🔲 จาก <b>บนลงล่าง</b> คือเลขใดตามลำดับ?<br>{math_table}"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (แกะรอยการยืมทีละหลัก):</b><br>
                    <b>ขั้นตอนที่ 1: วิเคราะห์หลักหน่วย (ขวาสุด)</b><br>
                    - {Z} ลบ {C} ไม่ได้ จึงต้องไปขอยืมหลักสิบมา 10<br>
                    - จะกลายเป็น (10 + {Z}) - {C} = <b>{10+Z-C}</b> (นี่คือตัวเลขกล่องล่างสุด)<br>
                    <b>ขั้นตอนที่ 2: วิเคราะห์หลักสิบ (ตรงกลาง)</b><br>
                    - เลข {Y} ถูกยืมไป 1 จึงเหลือเพียง {Y-1} แต่ยังคงน้อยกว่า 🔲 จึงต้องขอยืมหลักร้อยมาอีก 10<br>
                    - จะได้สมการ: (10 + {Y-1}) - 🔲 = {str_Res[1]} ➔ นำ {(10+Y-1)} ลบ {str_Res[1]} จะได้กล่องกลางคือ <b>{B}</b><br>
                    <b>ขั้นตอนที่ 3: วิเคราะห์หลักร้อย (ซ้ายสุด)</b><br>
                    - เลข 🔲 ถูกหลักสิบยืมไป 1 จึงมีค่าลดลงไป 1<br>
                    - จะได้สมการ: (🔲 - 1) - {A} = {str_Res[0]} ➔ ย้ายข้าง 🔲 = {str_Res[0]} + {A} + 1 = <b>{X}</b> (นี่คือตัวเลขกล่องบนสุด)<br>
                    <b>ตอบ: กล่องบนคือ {X}, กล่องกลางคือ {B}, กล่องล่างคือ {10+Z-C}</b></span>"""
                else:
                    n2 = random.randint(2, 9); n1 = random.randint(11, 99); ans_val = n1 * n2
                    str_n1, str_ans = str(n1), str(ans_val)
                    math_table = get_vertical_math([str_n1[0], box_html], [str(n2)], list(str_ans), "×")
                    q = f"จงเติมตัวเลขลงใน 🔲 ให้การคูณนี้ถูกต้อง<br>{math_table}"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: แปลงตารางเป็นสมการ</b><br>
                    - จากการตั้งคูณ หมายความว่า จำนวนสองหลัก × {n2} = {ans_val}<br>
                    <b>ขั้นตอนที่ 2: ใช้หลักการย้ายข้างสมการ</b><br>
                    - ย้าย {n2} ที่กำลังคูณอยู่ ข้ามฝั่งไปเป็นหาร: {ans_val} ÷ {n2} = <b>{n1}</b><br>
                    <b>ขั้นตอนที่ 3: เทียบหาตัวเลขที่หายไป</b><br>
                    - จำนวนสองหลักคือ {n1} เมื่อเทียบกับตาราง ตัวเลขที่หายไปในหลักหน่วยคือ <b>{str_n1[1]}</b><br>
                    <b>ตอบ: {str_n1[1]}</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "ความยาวและเส้นรอบรูป":
                if is_challenge:
                    N = random.randint(3, 5); S = random.randint(5, 12); O = random.randint(1, S-2)
                    width = N*S - (N-1)*O; ans = 2*(width+S)
                    q = f"นำกระดาษรูปสี่เหลี่ยมจัตุรัสที่มีความยาวด้านละ <b>{S} ซม.</b> จำนวน <b>{N} แผ่น</b> มาวางเรียงต่อกันเป็นแนวยาว<br>โดยให้แต่ละแผ่นวางซ้อนทับกันเป็นระยะ <b>{O} ซม.</b> จงหาความยาวรอบรูปทั้งหมดของรูปทรงที่เกิดใหม่นี้?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (หาระยะที่ถูกซ่อน):</b><br>
                    เมื่อวางซ้อนทับกัน รูปทรงใหม่จะกลายเป็นสี่เหลี่ยมผืนผ้ายาวๆ 1 รูป<br>
                    <b>ขั้นตอนที่ 1: หาความยาวแนวนอนของรูปใหม่</b><br>
                    - ถ้านำแผ่นมาต่อกันเฉยๆ (ไม่ซ้อนทับ) จะยาว {N} × {S} = {N*S} ซม.<br>
                    - แต่มีรอยซ้อนทับกันทั้งหมด {N-1} รอย รอยละ {O} ซม. ➔ หดหายไป {N-1} × {O} = {(N-1)*O} ซม.<br>
                    - ความยาวจริงแนวนอน = {N*S} - {(N-1)*O} = <b>{width} ซม.</b><br>
                    <b>ขั้นตอนที่ 2: หาความกว้างแนวตั้งของรูปใหม่</b><br>
                    - ความกว้างยังคงเท่าเดิมคือด้านของจัตุรัส = <b>{S} ซม.</b><br>
                    <b>ขั้นตอนที่ 3: คำนวณความยาวรอบรูปทั้งหมด</b><br>
                    - สูตรความยาวรอบรูป = 2 × (กว้าง + ยาว) ➔ 2 × ({S} + {width}) = <b>{ans} ซม.</b><br>
                    <b>ตอบ: {ans} ซม.</b></span>"""
                else:
                    side = random.randint(5, 25); leftover = random.randint(5, 20); L = (side * 4) + leftover
                    q = f"นำเส้นลวดที่มีความยาว <b>{L} ซม.</b> ไปดัดสร้างรูปสี่เหลี่ยมจัตุรัส แล้วปรากฏว่า <b>เหลือเศษลวด {leftover} ซม.</b><br>จงหาว่าความยาวของแต่ละด้านของรูปสี่เหลี่ยมจัตุรัสนี้เป็นกี่เซนติเมตร?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: หาลวดส่วนที่ถูกใช้งานจริง</b><br>
                    - นำความยาวลวดทั้งหมดตั้ง หักลบด้วยส่วนที่เหลือทิ้ง: {L} - {leftover} = <b>{L-leftover} ซม.</b><br>
                    <b>ขั้นตอนที่ 2: แบ่งความยาวให้ 4 ด้าน</b><br>
                    - คุณสมบัติของสี่เหลี่ยมจัตุรัสคือมี 4 ด้านยาวเท่ากันเสมอ<br>
                    - นำลวดที่ใช้จริงไปหาร 4: ({L-leftover}) ÷ 4 = <b>{side} ซม.</b><br>
                    <b>ตอบ: {side} ซม.</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "โจทย์ปัญหาเศษส่วนประยุกต์":
                if is_challenge:
                    Y = random.randint(10, 30); R2 = 2 * Y; X = random.randint(10, 30)
                    while (R2 + X) % 2 != 0: X += 1
                    R1 = (R2 + X) * 3 // 2; Total = R1 * 4 // 3
                    f1_4 = get_vertical_fraction(1, 4); f1_3 = get_vertical_fraction(1, 3); f1_2 = get_vertical_fraction(1, 2)
                    q = f"อ่านหนังสือเล่มหนึ่ง <b>วันแรกอ่านไป {f1_4} ของเล่ม</b><br><b>วันที่สองอ่านไป {f1_3} ของหน้าที่เหลือ</b> และอ่านเพิ่มอีก <b>{X} หน้า</b><br><b>วันที่สามอ่านไป {f1_2} ของหน้าที่เหลือ</b> และอ่านเพิ่มอีก <b>{Y} หน้า</b> ปรากฏว่าอ่านจบเล่มพอดี!<br>จงหาว่าหนังสือเล่มนี้มีทั้งหมดกี่หน้า?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (ย้อนกลับจากวันสุดท้าย):</b><br>
                    โจทย์ที่มีคำว่า "ของหน้าที่เหลือ" ซ้อนกัน ต้องใช้วิธีย้อนกลับจากจุดจบไปจุดเริ่มต้น!<br>
                    <b>ขั้นตอนที่ 1: ย้อนรอยวันที่ 3</b><br>
                    - อ่านไป {get_vertical_fraction(1, 2, is_bold=False)} (ครึ่งนึง) แล้วอ่านเพิ่ม {Y} หน้าจนจบ ➔ แสดงว่า {Y} หน้าที่อ่านทีหลัง ก็คือ 'ครึ่งที่เหลือ' นั่นเอง<br>
                    - ยอดหนังสือคงเหลือก่อนอ่านวันที่ 3 คือ: {Y} × 2 = <b>{R2} หน้า</b><br>
                    <b>ขั้นตอนที่ 2: ย้อนรอยวันที่ 2</b><br>
                    - นำ {X} หน้าที่อ่านเกินไปมาบวกคืน: {R2} + {X} = {R2+X} หน้า<br>
                    - {R2+X} หน้า คิดเป็น 2/3 ของวันนั้น (เพราะวันนั้นอ่านไป 1/3)<br>
                    - ยอดหนังสือคงเหลือก่อนอ่านวันที่ 2 คือ: ({R2+X} ÷ 2) × 3 = <b>{R1} หน้า</b><br>
                    <b>ขั้นตอนที่ 3: ย้อนรอยวันที่ 1 (หักจากของทั้งเล่ม)</b><br>
                    - {R1} หน้าที่เหลือ คิดเป็น 3/4 ของทั้งเล่ม (เพราะวันแรกอ่านไป 1/4)<br>
                    - จำนวนหน้าหนังสือทั้งเล่ม คือ: ({R1} ÷ 3) × 4 = <b>{Total} หน้า</b><br>
                    <b>ตอบ: {Total} หน้า</b></span>"""
                else:
                    den = random.choice([4, 5, 6, 8, 10]); num = random.randint(1, den-2); total_money = random.randint(10, 50) * den
                    ans_rem = total_money - int((total_money/den)*num)
                    f_html = get_vertical_fraction(num, den)
                    q = f"มีเงิน <b>{total_money} บาท</b> นำไปซื้อเครื่องเขียน <b>{f_html}</b> ของเงินทั้งหมด จะเหลือเงินกี่บาท?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: หาจำนวนเงินที่ใช้จ่ายไป</b><br>
                    - ความหมายของ {get_vertical_fraction(num, den, is_bold=False)} คือแบ่งเงินเป็น {den} ส่วน และใช้ไป {num} ส่วน<br>
                    - เงิน 1 ส่วนเท่ากับ: {total_money} ÷ {den} = {total_money//den} บาท<br>
                    - เงินที่ใช้ไปทั้งหมด: {total_money//den} × {num} = <b>{int((total_money/den)*num)} บาท</b><br>
                    <b>ขั้นตอนที่ 2: หาจำนวนเงินที่เหลือ</b><br>
                    - นำเงินตอนแรกสุดตั้ง ลบด้วยเงินที่ใช้จ่ายไป<br>
                    - จะได้: {total_money} - {int((total_money/den)*num)} = <b>{ans_rem} บาท</b><br>
                    <b>ตอบ: {ans_rem} บาท</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "การคำนวณหน่วยและเวลา":
                if is_challenge:
                    days_map = {"พฤหัสบดี": 3, "ศุกร์": 4, "เสาร์": 5}; end_day = random.choice(list(days_map.keys())); days = days_map[end_day]
                    gain_m = random.randint(3, 12); total_gain = days * gain_m
                    carry_h = total_gain // 60; final_m = total_gain % 60; final_h = 8 + carry_h
                    q = f"นาฬิกาเรือนหนึ่งทำงานผิดปกติ โดยจะเดิน <b>'เร็วเกินไป' วันละ {gain_m} นาที</b><br>ถ้าตั้งเวลานาฬิกาเรือนนี้ให้ตรงเป๊ะในตอน <b>08:00 น. ของวันจันทร์</b><br>จงหาว่าเมื่อเวลาจริงดำเนินไปถึง <b>08:00 น. ของวัน{end_day}</b> นาฬิกาเรือนนี้จะชี้บอกเวลาใด?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (คำนวณความคลาดเคลื่อนสะสม):</b><br>
                    <b>ขั้นตอนที่ 1: หาจำนวนวันที่ผ่านไปทั้งหมด</b><br>
                    - จาก 08:00 น. วันจันทร์ ถึง 08:00 น. วัน{end_day} นับเวลาที่ผ่านไปได้ <b>{days} วันพอดีเป๊ะ</b><br>
                    <b>ขั้นตอนที่ 2: หาเวลาที่นาฬิกาเดินเพี้ยนไปทั้งหมดสะสม</b><br>
                    - เดินเร็วขึ้นวันละ {gain_m} นาที × {days} วัน = <b>เดินเร็วนำหน้าเวลาจริงไป {total_gain} นาที</b><br>
                    <b>ขั้นตอนที่ 3: คำนวณเวลาที่จะแสดงบนหน้าปัด</b><br>
                    - แปลงหน่วยนาทีที่เกินมาให้เป็นชั่วโมง: นำ {total_gain} นาที ÷ 60 จะได้ <b>{carry_h} ชั่วโมง กับอีก {final_m} นาที</b><br>
                    - นำไปบวกเพิ่มจากเวลาจริง: 08:00 น. + {carry_h} ชั่วโมง {final_m} นาที = <b>{final_h:02d}:{final_m:02d} น.</b><br>
                    <b>ตอบ: เวลา {final_h:02d}:{final_m:02d} น.</b></span>"""
                else:
                    h1 = random.randint(2, 6); m1 = random.randint(40, 55); h2 = random.randint(1, 4); m2 = random.randint(30, 55)
                    total_m = m1 + m2; carry_h = total_m // 60; left_m = total_m % 60; ans_h = h1 + h2 + carry_h
                    q = f"เดินทางด้วยรถยนต์ใช้เวลา <b>{h1} ชม. {m1} นาที</b> และนั่งเรือต่ออีก <b>{h2} ชม. {m2} นาที</b> รวมใช้เวลาทั้งหมดเท่าไร?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: นำหน่วยนาทีมารวมกันก่อน</b><br>
                    - {m1} นาที + {m2} นาที = <b>{total_m} นาที</b><br>
                    <b>ขั้นตอนที่ 2: แปลงนาทีให้เป็นชั่วโมง (ถ้าเกิน 60)</b><br>
                    - เนื่องจาก 60 นาที = 1 ชั่วโมง ➔ เราสามารถปัด {total_m} นาที เป็น <b>{carry_h} ชั่วโมง กับอีก {left_m} นาที</b><br>
                    <b>ขั้นตอนที่ 3: นำหน่วยชั่วโมงมารวมกันทั้งหมด</b><br>
                    - {h1} ชม. + {h2} ชม. + {carry_h} ชม. (ตัวทดจากนาที) = <b>{ans_h} ชั่วโมง</b><br>
                    <b>ตอบ: {ans_h} ชั่วโมง {left_m:02d} นาที</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "โจทย์ปัญหาเปรียบเทียบกลุ่ม":
                if is_challenge:
                    C = random.randint(5, 15); P = random.randint(5, 15); H = P + 3 * C; L = 4 * P + 6 * C
                    q = f"ในฟาร์มแห่งหนึ่งมี หมู ไก่ และเป็ด รวมกันทั้งหมด <b>{H} ตัว (นับหัว)</b> และเมื่อนับขาของทุกตัวรวมกันจะได้ <b>{L} ขา</b><br>ถ้าเจ้าของฟาร์มให้ข้อมูลว่า <b>'มีจำนวนเป็ดเป็น 2 เท่าของจำนวนไก่เสมอ'</b><br>จงหาว่าในฟาร์มแห่งนี้มีหมูทั้งหมดกี่ตัว?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (สมการนับหัว-นับขา):</b><br>
                    <b>ขั้นตอนที่ 1: ยุบรวมสัตว์ปีก (ไก่และเป็ด) ให้เป็นกลุ่มเดียวเพื่อความง่าย</b><br>
                    - เป็ดเป็น 2 เท่าของไก่ แปลว่าถ้าเราจับมันมัดเป็นเซ็ต: 1 เซ็ตจะมี ไก่ 1 ตัว และ เป็ด 2 ตัว เสมอ (รวมเป็น 3 ตัว/เซ็ต)<br>
                    - ขาใน 1 เซ็ต = (ไก่ 1 ตัวมี 2 ขา) + (เป็ด 2 ตัวมี 4 ขา) = <b>6 ขาต่อ 1 เซ็ต</b><br>
                    - สรุป: สัตว์ปีก 1 เซ็ต มี 3 ตัว 6 ขา (ซึ่งพอเฉลี่ยแล้ว ก็ตก <b>ตัวละ 2 ขา</b> เท่าเดิม!)<br>
                    <b>ขั้นตอนที่ 2: ตั้งสมมติฐานแบบสุดโต่ง</b><br>
                    - สมมติว่าสัตว์ทั้ง {H} ตัวเป็นสัตว์ปีกล้วนๆ เลย จะต้องมีขาทั้งหมด: {H} × 2 = <b>{H*2} ขา</b><br>
                    - แต่โจทย์บอกว่ามีขาจริง {L} ขา แสดงว่ามีขา 'เกินมา': {L} - {H*2} = <b>{L - H*2} ขา</b><br>
                    <b>ขั้นตอนที่ 3: หาจำนวนหมูจากขาที่เกินมา</b><br>
                    - ขาที่เกินมา ย่อมมาจาก "หมู" เพราะหมูมี 4 ขา ซึ่งมากกว่าสัตว์ปีกอยู่ตัวละ 2 ขา (4 ลบ 2)<br>
                    - นำจำนวนขาที่เกินมา หารด้วย 2 จะได้จำนวนหมู: ({L - H*2}) ÷ 2 = <b>{P} ตัว</b><br>
                    <b>ตอบ: มีหมู {P} ตัว</b></span>"""
                else:
                    g1_std, g1_items = random.randint(10, 15), random.randint(5, 9); g2_std, g2_items = random.randint(16, 22), random.randint(3, 5)
                    t1 = g1_std * g1_items; t2 = g2_std * g2_items; diff = abs(t1 - t2); more_g = "กลุ่มแรก" if t1 > t2 else "กลุ่มที่สอง"
                    q = f"คุณครูแจกสมุดให้เด็กกลุ่มแรก <b>{g1_std} คน คนละ {g1_items} เล่ม</b> และกลุ่มที่สอง <b>{g2_std} คน คนละ {g2_items} เล่ม</b><br>กลุ่มใดได้รับสมุดรวมมากกว่ากัน และมากกว่ากันกี่เล่ม?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: หาจำนวนสมุดของกลุ่มแรก</b><br>
                    - {g1_std} คน × {g1_items} เล่ม = <b>{t1} เล่ม</b><br>
                    <b>ขั้นตอนที่ 2: หาจำนวนสมุดของกลุ่มที่สอง</b><br>
                    - {g2_std} คน × {g2_items} เล่ม = <b>{t2} เล่ม</b><br>
                    <b>ขั้นตอนที่ 3: เปรียบเทียบและหาผลต่าง</b><br>
                    - จะเห็นว่า <b>{more_g}</b> ได้จำนวนสมุดเยอะกว่า<br>
                    - หาว่ามากกว่ากันเท่าไร: นำ {max(t1,t2)} - {min(t1,t2)} = <b>{diff} เล่ม</b><br>
                    <b>ตอบ: {more_g} มากกว่าอยู่ {diff} เล่ม</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "อัตราส่วนอายุ":
                n1, n2, n3 = random.sample(["พี่", "พ่อ", "แม่", "น้า", "อา", "คุณครู", "นักเรียน"], 3)
                if is_challenge:
                    base = random.randint(3, 8)
                    a_now = base * random.randint(2, 3)
                    b_now = base * random.randint(4, 5)
                    c_now = base * random.randint(6, 8)
                    f = random.choice([4, 5, 6, 10])
                    
                    g1 = math.gcd(a_now, b_now); r1_a, r1_b = a_now//g1, b_now//g1
                    g2 = math.gcd(b_now, c_now); r2_b, r2_c = b_now//g2, c_now//g2
                    af, bf, cf = a_now+f, b_now+f, c_now+f; g_ans = math.gcd(math.gcd(af, bf), cf)
                    
                    q = f"ปัจจุบัน อัตราส่วนอายุของ <b>{n1} ต่อ {n2} เป็น {r1_a}:{r1_b}</b> และอัตราส่วนอายุของ <b>{n2} ต่อ {n3} เป็น {r2_b}:{r2_c}</b><br>ถ้าปัจจุบัน {n2} อายุ {b_now} ปี จงหาอัตราส่วนอายุของ <b>{n1} : {n2} : {n3}</b> ในอีก {f} ปีข้างหน้า? (ตอบเป็นอัตราส่วนอย่างต่ำ)"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (อัตราส่วนต่อเนื่อง):</b><br>
                    <b>ขั้นตอนที่ 1: หาอายุปัจจุบันที่แท้จริงของทุกคน</b><br>
                    - เรารู้ว่า {n2} อายุ {b_now} ปี <br>
                    - จากอัตราส่วน {n1}:{n2} = {r1_a}:{r1_b} ➔ เทียบอัตราส่วน {b_now}÷{r1_b} จะได้ส่วนละ {b_now//r1_b} ปี ➔ ดังนั้น {n1} อายุ {r1_a} × {b_now//r1_b} = <b>{a_now} ปี</b><br>
                    - จากอัตราส่วน {n2}:{n3} = {r2_b}:{r2_c} ➔ เทียบอัตราส่วน {b_now}÷{r2_b} จะได้ส่วนละ {b_now//r2_b} ปี ➔ ดังนั้น {n3} อายุ {r2_c} × {b_now//r2_b} = <b>{c_now} ปี</b><br>
                    <b>ขั้นตอนที่ 2: หาอายุในอีก {f} ปีข้างหน้า</b><br>
                    - นำอายุปัจจุบันของทุกคนบวกเพิ่มไปอีก {f} ปี: {n1}={af}, {n2}={bf}, {n3}={cf}<br>
                    <b>ขั้นตอนที่ 3: ทำเป็นอัตราส่วนอย่างต่ำ</b><br>
                    - เขียนอัตราส่วนใหม่: {af} : {bf} : {cf}<br>
                    - นำ ห.ร.ม. ({g_ans}) มาหารทุกตัว: <b>{af//g_ans} : {bf//g_ans} : {cf//g_ans}</b><br>
                    <b>ตอบ: {af//g_ans} : {bf//g_ans} : {cf//g_ans}</b></span>"""
                else:
                    a_now = random.randint(12, 25); diff = random.randint(25, 40); f = random.choice([10, 15, 20, 25])
                    b_now = a_now + diff; r1_val, r2_val = a_now + f, b_now + f; g = math.gcd(r1_val, r2_val)
                    q = f"ปัจจุบัน <b>{n2}</b> อายุ {a_now} ปี และ <b>{n1}</b> อายุ {b_now} ปี <br>จงหาว่าเมื่อเวลาผ่านไปอีก {f} ปีในอนาคต อัตราส่วนอายุของ <b>{n2} ต่อ {n1}</b> จะเป็นเท่าใด? (ตอบเป็นอัตราส่วนอย่างต่ำ)"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: หาอายุในอนาคตของทั้งสองคน</b><br>
                    - {n2} จะมีอายุ: {a_now} + {f} = <b>{r1_val} ปี</b><br>
                    - {n1} จะมีอายุ: {b_now} + {f} = <b>{r2_val} ปี</b><br>
                    <b>ขั้นตอนที่ 2: เขียนอัตราส่วนและทำเป็นอย่างต่ำ</b><br>
                    - อัตราส่วนอายุ {n2} : {n1} = {r1_val} : {r2_val}<br>
                    - นำตัวเลขที่หารทั้งสองตัวลงตัว ({g}) มาหารตลอด จะได้: <b>{r1_val//g} : {r2_val//g}</b><br>
                    <b>ตอบ: {r1_val//g} : {r2_val//g}</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "การปักเสาและปลูกต้นไม้":
                role = random.choice(BUILDERS); action = random.choice(BUILD_ACTIONS); loc = random.choice(["สองฝั่งของถนน", "รอบรั้วโรงเรียนวงกลม"])
                if is_challenge:
                    d = random.choice([4, 5, 8, 10]); length = random.randint(100, 300)
                    while length % d != 0: length += 1
                    ans = ((length // d) + 1) * 2
                    q = f"<b>{role}</b> มีโครงการ<b>{action}</b>บริเวณ <b>'สองฝั่ง'</b> ของถนนเส้นหนึ่งที่มีความยาว <b>{length} เมตร</b> โดยปักห่างกันจุดละ <b>{d} เมตร</b> และต้องติดตั้งที่จุดเริ่มต้นและสิ้นสุดของถนนด้วย <br>จะใช้สิ่งที่ติดตั้งทั้งหมดกี่จุด?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (คูณสองฝั่ง):</b><br>
                    <b>ขั้นตอนที่ 1: คำนวณจำนวนจุดของถนนฝั่งเดียวก่อน</b><br>
                    - กฎของถนนเส้นตรงที่มีการปิดหัวท้าย คือ จำนวนจุด = จำนวนช่องว่าง + 1<br>
                    - หาช่องว่าง: ระยะทางรวม ÷ ระยะห่าง = {length} ÷ {d} = {length//d} ช่อง<br>
                    - จำนวนจุดติดตั้งฝั่งเดียว: {length//d} + 1 = <b>{(length//d)+1} จุด</b><br>
                    <b>ขั้นตอนที่ 2: คิดรวมถนนทั้งสองฝั่ง</b><br>
                    - เนื่องจากโครงการทำทั้ง <b>สองฝั่งของถนน</b> ต้องนำจำนวนจุดที่ได้ไปคูณ 2<br>
                    - {(length//d)+1} × 2 = <b>{ans} จุด</b><br>
                    <b>ตอบ: {ans} จุด</b></span>"""
                else:
                    d = random.choice([10, 15, 20, 25]); trees = random.randint(40, 100); length = (trees - 1) * d
                    q = f"มีโครงการ<b>{action}</b>ที่ริมถนนทางเข้า โดยแต่ละจุดห่างกัน <b>{d} เมตร</b> และต้องปักที่จุดเริ่มต้นและสิ้นสุดพอดี <br>ถ้านับรวมได้ <b>{trees} จุด</b> ระยะทางเส้นนี้ยาวกี่เมตร?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: หาจำนวนช่องว่าง</b><br>
                    - กฎของถนนเส้นตรงที่มีปักหัวท้าย คือ จำนวนช่องว่างจะน้อยกว่าจำนวนจุดอยู่ 1 เสมอ<br>
                    - ช่องว่าง = {trees} - 1 = <b>{trees - 1} ช่อง</b><br>
                    <b>ขั้นตอนที่ 2: หาระยะทางรวม</b><br>
                    - นำจำนวนช่องว่าง × ระยะห่างของแต่ละช่อง<br>
                    - {trees - 1} × {d} = <b>{length} เมตร</b><br>
                    <b>ตอบ: {length} เมตร</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "เส้นทางที่เป็นไปได้":
                loc1 = random.choice(["บ้าน", "กทม."]); loc2 = random.choice(["ตลาด", "อยุธยา"]); loc3 = random.choice(["โรงเรียน", "เชียงใหม่"])
                if is_challenge:
                    p1, p2 = random.randint(3, 5), random.randint(2, 4); ans = (p1 * p2) * ((p1 - 1) * (p2 - 1))
                    q = f"มีเส้นทางจาก <b>{loc1} ไป {loc2}</b> จำนวน <b>{p1} สาย</b> และจาก <b>{loc2} ไป {loc3}</b> จำนวน <b>{p2} สาย</b><br>ต้องการเดินทางแบบ <b>ไป-กลับ ({loc1} ➔ {loc3} ➔ {loc1})</b> โดยมีข้อแม้ว่า <b>'ขากลับห้ามใช้เส้นทางเดิมที่เคยใช้ตอนขาไปเด็ดขาด'</b><br>จะมีรูปแบบการเดินทางไป-กลับทั้งหมดกี่วิธี?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (กฎการคูณแบบมีเงื่อนไข):</b><br>
                    <b>ขั้นตอนที่ 1: คำนวณรูปแบบของขาไป ({loc1} ➔ {loc2} ➔ {loc3})</b><br>
                    - ขาไปสามารถเลือกใช้ถนนได้เต็มที่: {p1} × {p2} = <b>{p1 * p2} วิธี</b><br>
                    <b>ขั้นตอนที่ 2: คำนวณรูปแบบของขากลับ ({loc3} ➔ {loc2} ➔ {loc1})</b><br>
                    - เนื่องจากห้ามใช้เส้นทางเดิมที่ใช้ตอนขาไป จึงต้องหักเส้นทางออกช่วงละ 1 สาย<br>
                    - เส้นทางช่วงที่ 1 เหลือ: <b>{p2-1} สาย</b> และช่วงที่ 2 เหลือ: <b>{p1-1} สาย</b><br>
                    - รูปแบบขากลับ: {p2-1} × {p1-1} = <b>{(p1-1) * (p2-1)} วิธี</b><br>
                    <b>ขั้นตอนที่ 3: นำรูปแบบขาไปและขากลับมารวมกันต่อเนื่อง (นำมาคูณกัน)</b><br>
                    - {p1 * p2} × {(p1-1) * (p2-1)} = <b>{ans:,} วิธี</b><br>
                    <b>ตอบ: {ans:,} วิธี</b></span>"""
                else:
                    p1, p2, p3 = random.randint(4, 6), random.randint(3, 5), random.randint(2, 4); ans = (p1 * p2) + p3
                    q = f"เดินทางจาก <b>{loc1} ไป {loc2}</b> มีทาง <b>{p1} สาย</b>, จาก <b>{loc2} ไป {loc3}</b> มีทาง <b>{p2} สาย</b> <br>และมีทางด่วนพิเศษจาก <b>{loc1} ไป {loc3}</b> (ไม่ผ่าน {loc2}) อีก <b>{p3} สาย</b><br>จะมีรูปแบบเดินทางจาก <b>{loc1} ไป {loc3}</b> ทั้งหมดกี่วิธี?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: คำนวณเส้นทางปกติ (ที่ผ่าน {loc2})</b><br>
                    - นำเส้นทางมาคูณกัน: {p1} × {p2} = <b>{p1 * p2} วิธี</b><br>
                    <b>ขั้นตอนที่ 2: คำนวณเส้นทางด่วนพิเศษ</b><br>
                    - มีให้เลือกใช้ = <b>{p3} วิธี</b><br>
                    <b>ขั้นตอนที่ 3: นำเส้นทางทั้งสองกรณีมารวมกัน (นำมาบวกกัน)</b><br>
                    - {p1 * p2} + {p3} = <b>{ans} วิธี</b><br>
                    <b>ตอบ: {ans} วิธี</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "คะแนนยิงเป้า":
                if is_challenge:
                    darts = random.randint(4, 5); pool = [10, 5, 3]; miss_penalty = random.randint(1, 2)
                    hits = random.choices(pool, k=darts-1) + [0]; total_score = sum(hits) - miss_penalty
                    q = f"เกมปาลูกดอกมีเป้าคะแนน <b>10, 5, 3</b> ถ้าปาพลาดเป้าจะถูก <b>หัก {miss_penalty} คะแนน</b><br><b>{name}</b> ปาลูกดอกทั้งหมด <b>{darts} ครั้ง</b> ได้คะแนนรวม <b>{total_score} คะแนน</b> <br>จงหาว่าเขาปาเข้าเป้าคะแนนใดบ้าง และพลาดกี่ครั้ง? (เรียงจากมากไปน้อย)"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (Trial and Error with Penalty):</b><br>
                    <b>ขั้นตอนที่ 1: ลองตั้งสมมติฐานว่ามี 'ปาพลาด'</b><br>
                    - ถ้าปาพลาด 1 ครั้ง จะได้ 0 คะแนน และโดนหักก้อนคะแนนที่สะสมไว้อีก {miss_penalty} คะแนน<br>
                    <b>ขั้นตอนที่ 2: คำนวณหาคะแนนที่ทำได้จริง (ก่อนโดนหัก)</b><br>
                    - นำคะแนนรวมที่ได้ บวกคืนค่าที่โดนหักไป: {total_score} + {miss_penalty} = <b>{sum(hits)} คะแนน</b><br>
                    <b>ขั้นตอนที่ 3: จัดกลุ่มตัวเลขหาเป้าที่ปาโดน</b><br>
                    - เราต้องหาตัวเลขจากเป้า {pool} จำนวน {darts-1} ครั้ง ที่รวมกันแล้วได้ {sum(hits)} พอดี<br>
                    - จะพบว่ารูปแบบที่ถูกต้องคือ: <b>{' + '.join(map(str, sorted([h for h in hits if h > 0], reverse=True)))}</b><br>
                    <b>ตอบ: เข้าเป้าคะแนน {sorted([h for h in hits if h > 0], reverse=True)} และปาพลาด 1 ครั้ง</b></span>"""
                else:
                    darts = random.choice([4, 5]); pool = [50, 20, 10, 5]; pool.sort(reverse=True)
                    hits = random.choices(pool, k=darts); total_score = sum(hits); hits.sort(reverse=True)
                    q = f"เกมปาลูกดอก เป้ามีคะแนน <b>{', '.join(map(str, pool))} คะแนน</b><br><b>{name}</b> ปาลูกดอก <b>{darts} ครั้ง</b> เข้าเป้าทุกครั้ง ได้คะแนนรวม <b>{total_score} คะแนน</b> <br>จงหาว่าปาเข้าเป้าวงใดบ้าง? (เรียงจากมากไปน้อย)"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: ใช้วิธีสุ่มแจกแจงตัวเลข (Trial and Error)</b><br>
                    - เราต้องหาตัวเลขจากเป้าทั้งหมด {darts} ตัว ที่บวกกันแล้วได้ {total_score} เป๊ะๆ<br>
                    - เทคนิค: ให้เริ่มพิจารณาจากตัวเลขที่มีค่ามากที่สุดก่อน เพื่อตัดความเป็นไปได้ออก<br>
                    <b>ขั้นตอนที่ 2: จัดกลุ่มตัวเลข</b><br>
                    - จะพบว่ารูปแบบเดียวที่รวมกันได้ {total_score} พอดีคือ: <b>{' + '.join(map(str, hits))} = {total_score}</b><br>
                    <b>ตอบ: เข้าเป้าคะแนน {hits}</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "การนับหน้าหนังสือ":
                publisher = random.choice(PUBLISHERS); book_type = random.choice(DOC_TYPES)
                if is_challenge:
                    target_pages = random.randint(150, 450)
                    if target_pages > 99: total_digits = 9 + 180 + ((target_pages - 99) * 3)
                    else: total_digits = 9 + ((target_pages - 9) * 2)
                    q = f"<b>{publisher}</b> กำลังพิมพ์ตัวเลขหน้าหนังสือ<b>{book_type}</b> โดยเริ่มตั้งแต่หน้า 1 <br>เมื่อพิมพ์เสร็จ พบว่าใช้ตัวเลขโดด (0-9) ไปทั้งหมด <b>{total_digits:,} ตัว</b> <br>จงหาว่าหนังสือเล่มนี้มีทั้งหมดกี่หน้า?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์ย้อนกลับแบบ Step-by-Step (Olympiad Level):</b><br>
                    <b>ขั้นตอนที่ 1: หักล้างตัวเลขหน้า 1 หลัก และ 2 หลักออกไปก่อน</b><br>
                    - หน้า 1 ถึง 9 มี 9 หน้า (ใช้หน้าละ 1 ตัวเลข) = 9 × 1 = 9 ตัว (เหลือ {total_digits} - 9 = {total_digits - 9} ตัว)<br>
                    - หน้า 10 ถึง 99 มี 90 หน้า (ใช้หน้าละ 2 ตัวเลข) = 90 × 2 = 180 ตัว (เหลือ {total_digits-9} - 180 = <b>{total_digits - 189} ตัว</b>)<br>
                    <b>ขั้นตอนที่ 2: คำนวณจำนวนหน้า 3 หลักที่เหลือ</b><br>
                    - ตัวเลขโดดที่เหลือ {total_digits - 189} ตัว ล้วนเป็นของหน้า 3 หลัก (หลักร้อย)<br>
                    - นำไปหาร 3 (เพราะใช้หน้าละ 3 ตัวเลข): {total_digits - 189} ÷ 3 = <b>{(total_digits - 189)//3} หน้า</b><br>
                    <b>ขั้นตอนที่ 3: รวมจำนวนหน้าทั้งหมดเข้าด้วยกัน</b><br>
                    - นำ 9 (หน้าหลักเดียว) + 90 (หน้าสองหลัก) + {(total_digits - 189)//3} (หน้าสามหลัก) = <b>{target_pages} หน้า</b><br>
                    <b>ตอบ: {target_pages} หน้า</b></span>"""
                else:
                    pages = random.randint(300, 999)
                    if pages > 99:
                        ans = 9 + 180 + ((pages - 99) * 3)
                        calc_text = f"- หน้า 1 ถึง 9 (หน้าละ 1 ตัว): 9 × 1 = <b>9 ตัว</b><br>- หน้า 10 ถึง 99 (หน้าละ 2 ตัว): 90 × 2 = <b>180 ตัว</b><br>- หน้า 100 ถึง {pages} (หน้าละ 3 ตัว): {pages - 99} × 3 = <b>{(pages - 99) * 3} ตัว</b>"
                        sum_text = f"9 + 180 + {(pages - 99) * 3}"
                    else:
                        ans = 9 + ((pages - 9) * 2)
                        calc_text = f"- หน้า 1 ถึง 9 (หน้าละ 1 ตัว): 9 × 1 = <b>9 ตัว</b><br>- หน้า 10 ถึง {pages} (หน้าละ 2 ตัว): {pages - 9} × 2 = <b>{(pages - 9) * 2} ตัว</b>"
                        sum_text = f"9 + {(pages - 9) * 2}"
                    q = f"<b>{publisher}</b>พิมพ์<b>{book_type}</b> ความหนารวม <b>{pages}</b> หน้า ต้องพิมพ์เลขหน้ามุมกระดาษตั้งแต่หน้า 1 ถึง {pages} <br>จะใช้ตัวเลขโดดรวมทั้งหมดกี่ตัว?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: แบ่งนับเป็นกลุ่มตามจำนวนหลักของเลขหน้า</b><br>
                    {calc_text}<br>
                    <b>ขั้นตอนที่ 2: นำตัวเลขของทุกกลุ่มมารวมกัน</b><br>
                    - {sum_text} = <b>{ans:,} ตัว</b><br>
                    <b>ตอบ: {ans:,} ตัว</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "พื้นที่แรเงา (เรขาคณิต)":
                mat = random.choice(MATERIALS)
                if is_challenge:
                    in_r = random.choice([7, 14]); out_s = (in_r * 2) + random.choice([10, 20])
                    area_sq = out_s ** 2; area_cir = int((22/7) * in_r * in_r); ans = area_sq - area_cir
                    f_pi = get_vertical_fraction(22, 7, is_bold=False)
                    q = f"แผ่น<b>{mat}</b>รูปสี่เหลี่ยมจัตุรัสยาวด้านละ <b>{out_s} ซม.</b> ช่างเจาะรูตรงกลางเป็น 'รูปวงกลม' ที่มีรัศมี <b>{in_r} ซม.</b> ทิ้งไป <br>จงหาพื้นที่ของแผ่น<b>{mat}</b>ส่วนที่เหลือ? (กำหนดให้ค่า π ≈ {f_pi})"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: หาพื้นที่สี่เหลี่ยมจัตุรัสแผ่นใหญ่ทั้งหมดก่อน</b><br>
                    - สูตร ด้าน × ด้าน = {out_s} × {out_s} = <b>{area_sq:,} ตร.ซม.</b><br>
                    <b>ขั้นตอนที่ 2: หาพื้นที่วงกลมที่เจาะทิ้ง</b><br>
                    - สูตร π × รัศมี × รัศมี = {f_pi} × {in_r} × {in_r} = <b>{area_cir:,} ตร.ซม.</b><br>
                    <b>ขั้นตอนที่ 3: คำนวณพื้นที่ส่วนที่เหลือ</b><br>
                    - นำพื้นที่ใหญ่ หักลบด้วย พื้นที่รูที่ถูกเจาะทิ้ง: {area_sq:,} - {area_cir:,} = <b>{ans:,} ตร.ซม.</b><br>
                    <b>ตอบ: {ans:,} ตร.ซม.</b></span>"""
                else:
                    out_w = random.randint(40, 80); out_h = random.randint(30, 60); in_s = random.randint(10, 20)
                    ans = (out_w * out_h) - (in_s**2)
                    q = f"แผ่น<b>{mat}</b>รูปสี่เหลี่ยมผืนผ้า กว้าง <b>{out_w} ซม.</b> ยาว <b>{out_h} ซม.</b> ตัดเจาะรูตรงกลางเป็น 'สี่เหลี่ยมจัตุรัส' ยาวด้านละ <b>{in_s} ซม.</b> ทิ้งไป <br>จงหาพื้นที่ส่วนที่เหลือ?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: หาพื้นที่แผ่นสี่เหลี่ยมแผ่นใหญ่ก่อน</b><br>
                    - สูตร กว้าง × ยาว = {out_w} × {out_h} = <b>{out_w * out_h:,} ตร.ซม.</b><br>
                    <b>ขั้นตอนที่ 2: หาพื้นที่รูสี่เหลี่ยมจัตุรัสที่ถูกเจาะทิ้ง</b><br>
                    - สูตร ด้าน × ด้าน = {in_s} × {in_s} = <b>{in_s**2:,} ตร.ซม.</b><br>
                    <b>ขั้นตอนที่ 3: คำนวณพื้นที่ส่วนที่เหลือ</b><br>
                    - นำพื้นที่ใหญ่ ลบด้วย พื้นที่ที่ถูกเจาะทิ้ง: {out_w * out_h:,} - {in_s**2:,} = <b>{ans:,} ตร.ซม.</b><br>
                    <b>ตอบ: {ans:,} ตร.ซม.</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "จัดของใส่กล่อง (Modulo)":
                item = random.choice(FRUITS + ITEMS); container = random.choice(CONTAINERS)
                if is_challenge:
                    m1, m2 = 3, 5; rem1 = random.randint(1, 2); rem2 = random.randint(1, 4)
                    ans = 0
                    for i in range(1, 200):
                        if i % m1 == rem1 and i % m2 == rem2: ans = i; break
                    if ans == 0: continue
                    q = f"คุณครูมี<b>{item}</b>จำนวนหนึ่ง <br>ถ้าจัดใส่<b>{container}</b>ละ {m1} ชิ้น จะเหลือเศษ <b>{rem1} ชิ้น</b><br>แต่ถ้าเปลี่ยนมาจัดใส่<b>{container}</b>ละ {m2} ชิ้น จะเหลือเศษ <b>{rem2} ชิ้น</b> พอดี<br>จงหาว่าคุณครูมี<b>{item}</b>น้อยที่สุดกี่ชิ้น?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (ทฤษฎีบทเศษเหลือ):</b><br>
                    ใช้วิธีลองไล่ตัวเลข (Listing) ที่ตรงกับเงื่อนไขแรก แล้วเช็กกับเงื่อนไขที่สอง<br>
                    <b>ขั้นตอนที่ 1: หาตัวเลขที่เป็นไปได้จากเงื่อนไขแรก</b><br>
                    - จำนวนที่เมื่อจัดทีละ {m1} แล้วเหลือเศษ {rem1} คือการท่องสูตรคูณแม่ {m1} แล้วบวกเศษ<br>
                    - จะได้ตัวเลขคือ: {(m1*1)+rem1}, {(m1*2)+rem1}, {(m1*3)+rem1}, {(m1*4)+rem1}, {(m1*5)+rem1}, {(m1*6)+rem1}...<br>
                    <b>ขั้นตอนที่ 2: นำตัวเลขที่ได้มาทดสอบกับเงื่อนไขที่สอง</b><br>
                    - นำเลขเหล่านั้นมาลองหารด้วย {m2} ดูว่าตัวไหนเหลือเศษ {rem2} พอดี<br>
                    - จะพบว่าตัวเลข <b>ตัวแรกสุด (น้อยที่สุด)</b> ที่ตรงตามเงื่อนไขที่สองด้วยคือ <b>{ans}</b> <br>
                    - พิสูจน์: {ans} ÷ {m2} = {ans//m2} เศษ {ans%m2} (ตรงตามเงื่อนไขพอดี!)<br>
                    <b>ตอบ: {ans} ชิ้น</b></span>"""
                else:
                    box_cap = random.randint(15, 25); num_boxes = random.randint(30, 50)
                    rem = random.randint(1, box_cap - 1); total_items = (box_cap * num_boxes) + rem
                    q = f"มี<b>{item}</b>ทั้งหมด <b>{total_items}</b> ชิ้น จัดใส่<b>{container}</b> ใบละ <b>{box_cap}</b> ชิ้นเท่าๆ กัน <br>จะได้<b>{container}</b>เต็มกี่ใบ? และเหลือเศษกี่ชิ้น?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: ใช้การตั้งหารเพื่อแบ่งของเป็นกลุ่มๆ</b><br>
                    - นำจำนวนของทั้งหมดตั้ง หารด้วยความจุต่อ 1 กล่อง: {total_items} ÷ {box_cap}<br>
                    <b>ขั้นตอนที่ 2: พิจารณาผลลัพธ์และเศษ</b><br>
                    - ผลลัพธ์จากการหาร (ตัวเลขข้างหน้า) คือจำนวนกล่องที่ใส่ได้เต็มพอดี: <b>{num_boxes} ใบ</b><br>
                    - เศษที่เหลือจากการหาร คือจำนวนของที่เหลืออยู่ซึ่งไม่พอใส่กล่องใหม่: <b>{rem} ชิ้น</b><br>
                    <b>ตอบ: ได้เต็ม {num_boxes} ใบ และเหลือเศษ {rem} ชิ้น</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "วันที่และปฏิทิน":
                d_th = ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"]
                if is_challenge:
                    s_d = random.randint(1, 5); s_idx = random.randint(0, 6)
                    months = [("มกราคม", 31), ("กุมภาพันธ์", 28), ("มีนาคม", 31), ("เมษายน", 30)]
                    start_m_idx = random.randint(0, 1); target_m_idx = start_m_idx + 2
                    start_month, start_days = months[start_m_idx]
                    _, mid_days = months[start_m_idx+1]
                    target_month, _ = months[target_m_idx]
                    t_d = random.randint(10, 20)
                    add_days = (start_days - s_d) + mid_days + t_d
                    t_idx = (s_idx + (add_days % 7)) % 7
                    q = f"ในปีปกติ (กุมภาพันธ์มี 28 วัน)<br>ถ้าวันที่ <b>{s_d} {start_month}</b> ตรงกับ <b>วัน{d_th[s_idx]}</b> <br>จงหาว่า วันที่ <b>{t_d} {target_month}</b> ของปีเดียวกัน จะตรงกับวันอะไรในสัปดาห์?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (การนับวันข้ามเดือน):</b><br>
                    <b>ขั้นตอนที่ 1: หาจำนวนวันทั้งหมดที่ต้องนับเดินหน้า</b><br>
                    - จำนวนวันที่เหลือในเดือน{start_month} คือ: {start_days} - {s_d} = <b>{start_days - s_d} วัน</b><br>
                    - จำนวนวันในเดือนถัดไป (ข้าม 1 เดือน) คือ: <b>{mid_days} วัน</b><br>
                    - จำนวนวันในเดือนเป้าหมาย ({target_month}) คือ: <b>{t_d} วัน</b><br>
                    - นำมารวมกันทั้งหมด: {start_days - s_d} + {mid_days} + {t_d} = <b>{add_days} วัน</b><br>
                    <b>ขั้นตอนที่ 2: นำจำนวนวันรวมไปหาเศษสัปดาห์ (หาร 7)</b><br>
                    - {add_days} ÷ 7 = ได้ {add_days//7} สัปดาห์เต็ม และเหลือ <b>เศษ {add_days%7} วัน</b><br>
                    <b>ขั้นตอนที่ 3: นับนิ้วเดินหน้าต่อจากวันตั้งต้น</b><br>
                    - เริ่มนับต่อจาก วัน{d_th[s_idx]} ไปข้างหน้าอีก {add_days%7} วัน<br>
                    - จะไปตกที่ <b>วัน{d_th[t_idx]}</b> พอดีเป๊ะ!<br>
                    <b>ตอบ: ตรงกับวัน{d_th[t_idx]}</b></span>"""
                else:
                    s_d = random.randint(1, 5); s_idx = random.randint(0, 6)
                    add = random.randint(50, 120); t_idx = (s_idx + (add % 7)) % 7
                    q = f"ถ้าวันที่ <b>{s_d}</b> ของเดือนนี้ ตรงกับ <b>วัน{d_th[s_idx]}</b> พอดี <br>จงหาว่าอีก <b>{add} วันข้างหน้า</b> จะตรงกับวันอะไรในสัปดาห์?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: ตัดวันที่เป็นรอบสัปดาห์เต็มๆ ทิ้งไป (หาร 7)</b><br>
                    - วันในปฏิทินจะวนลูปซ้ำทุกๆ 7 วัน ดังนั้นให้นำ {add} ÷ 7<br>
                    - จะได้ผลลัพธ์คือ {add//7} สัปดาห์ และเหลือ <b>เศษ {add%7} วัน</b><br>
                    <b>ขั้นตอนที่ 2: นับนิ้วเฉพาะเศษที่เหลือ</b><br>
                    - เราสนใจแค่ตัวเศษ ให้นับนิ้วเดินหน้าต่อไปจาก วัน{d_th[s_idx]} อีก {add%7} วัน<br>
                    - จะตกที่ <b>วัน{d_th[t_idx]}</b><br>
                    <b>ตอบ: วัน{d_th[t_idx]}</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "สัตว์ปีนบ่อ":
                animal = random.choice(ANIMALS)
                if is_challenge:
                    u, d = 5, 2; heavy_d = 4; h = random.randint(25, 35)
                    pos = 0; days = 0
                    while pos < h:
                        days += 1; pos += u
                        if pos >= h: break
                        if days % 3 == 0: pos -= heavy_d
                        else: pos -= d
                    q = f"<b>{animal}</b>ตกลงไปในบ่อลึก <b>{h} เมตร</b><br>ตอนกลางวันปีนขึ้นได้ <b>{u} เมตร</b> ตอนกลางคืนลื่นตกลง <b>{d} เมตร</b> เสมอ<br>แต่ <b>'ทุกๆ คืนวันที่ 3'</b> ฝนจะตกทำให้ลื่นไถลลงไปถึง <b>{heavy_d} เมตร</b>แทน<br>จงหาว่าจะใช้เวลากี่วันจึงจะปีนพ้นปากบ่อ?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (Simulation จำลองเหตุการณ์):</b><br>
                    ข้อนี้สูตรลัดใช้ไม่ได้เพราะมีเงื่อนไขฝนตกแทรกเข้ามา ต้องจำลองสถานการณ์บวกทีละวันอย่างระมัดระวัง!<br>
                    - <b>วันที่ 1:</b> ปีนขึ้น {u} ลื่น {d} ➔ ยืนอยู่ที่ <b>{u-d} ม.</b><br>
                    - <b>วันที่ 2:</b> ปีนขึ้น {u} (กลายเป็น {u-d+u}) ลื่น {d} ➔ ยืนอยู่ที่ <b>{(u-d)*2} ม.</b><br>
                    - <b>วันที่ 3 (ฝนตก):</b> ปีนขึ้น {u} แต่ลื่น {heavy_d} ➔ ยืนอยู่ที่ {(u-d)*2+u-heavy_d} ม.<br>
                    - เมื่อจำลองการบวกลบไปเรื่อยๆ จะพบว่าใน <b>วันที่ {days}</b> ตอนกลางวัน เมื่อสัตว์ปีนขึ้นไปอีก {u} เมตร จะพ้นขอบบ่อไปเลย {h} เมตร พอดีเป๊ะ! (จึงไม่ต้องรอลื่นลงมาในตอนกลางคืนอีกแล้ว)<br>
                    <b>ตอบ: ใช้เวลา {days} วัน</b></span>"""
                else:
                    u = random.randint(10, 15); d = random.randint(4, 8); h = random.randint(50, 100)
                    net = u - d; days = math.ceil((h - u) / net) + 1
                    q = f"<b>{animal}</b>ตกลงบ่อลึก <b>{h} เมตร</b> กลางวันปีน <b>{u} เมตร</b> กลางคืนลื่น <b>{d} เมตร</b> จะต้องใช้เวลากี่วันจึงจะปีนพ้นปากบ่อ?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: หาการปีนสุทธิใน 1 วัน</b><br>
                    - 1 วัน (ขึ้นและลง) จะปีนได้จริง: {u} - {d} = <b>{net} เมตร</b><br>
                    <b>ขั้นตอนที่ 2: หักระยะในวันสุดท้ายออกก่อน (จุดหลอก!)</b><br>
                    - ในวันสุดท้าย ถ้าปีนพ้นปากบ่อแล้วก็จะไม่ลื่นลงมาอีก! จึงต้องแยกคิด<br>
                    - ระยะทางที่ต้องปีนแบบลื่นไถล คือ: {h} - {u} = <b>{h - u} เมตร</b><br>
                    <b>ขั้นตอนที่ 3: คำนวณเวลาที่ใช้ปีนระยะช่วงแรก</b><br>
                    - นำระยะช่วงแรกหารด้วยการปีนสุทธิ: {h - u} ÷ {net} = <b>{math.ceil((h - u) / net)} วัน</b><br>
                    <b>ขั้นตอนที่ 4: รวมกับวันสุดท้าย</b><br>
                    - นำเวลาช่วงแรก ไปบวกกับ วันสุดท้ายที่กระโดดพ้นบ่ออีก 1 วัน: {math.ceil((h - u) / net)} + 1 = <b>{days} วัน</b><br>
                    <b>ตอบ: {days} วัน</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "ตรรกะตาชั่งสมดุล":
                items_pair = [("เพชร", "ทอง", "เงิน", "เหล็ก"), ("สิงโต", "หมาป่า", "จิ้งจอก", "แมว"), ("ผลส้ม", "แอปเปิล", "สตรอว์เบอร์รี", "องุ่น")]
                i1, i2, i3, i4 = random.choice(items_pair)
                if is_challenge:
                    m1 = 2; m2 = random.randint(2, 3); m3 = random.randint(2, 3); q_mul = random.randint(2, 3); ans = m1 * m2 * m3 * q_mul
                    q = f"ตาชั่งสมดุล 3 ตัว ให้ข้อมูลดังนี้:<br>- <b>{i1} 1 อัน</b> หนักเท่ากับ <b>{i2} {m1} อัน</b><br>- <b>{i2} 1 อัน</b> หนักเท่ากับ <b>{i3} {m2} อัน</b><br>- <b>{i3} 1 อัน</b> หนักเท่ากับ <b>{i4} {m3} อัน</b><br><br>อยากทราบว่า <b>{i1} จำนวน {q_mul} อัน</b> จะมีน้ำหนักเท่ากับ <b>{i4}</b> กี่อัน?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (การแทนค่าต่อเนื่อง 3 ชั้น):</b><br>
                    <b>ขั้นตอนที่ 1: แทนค่าชั้นที่ 1 ไปชั้นที่ 2</b><br>
                    - {i1} 1 อัน = {i2} {m1} อัน<br>
                    - นำ {i3} ไปแทน {i2} ➔ จะได้ {i1} 1 อัน = {m1} × {m2} = <b>{m1*m2} อัน (ของ {i3})</b><br>
                    <b>ขั้นตอนที่ 2: แทนค่าชั้นที่ 2 ไปชั้นที่ 3</b><br>
                    - นำ {i4} ไปแทน {i3} ➔ จะได้ {i1} 1 อัน = {m1*m2} × {m3} = <b>{m1*m2*m3} อัน (ของ {i4})</b><br>
                    <b>ขั้นตอนที่ 3: หาคำตอบตามที่โจทย์ถาม</b><br>
                    - โจทย์ถามหา {i1} {q_mul} อัน ➔ นำปริมาณ {i4} ที่เทียบได้ไปคูณ {q_mul} <br>
                    - {m1*m2*m3} × {q_mul} = <b>{ans} อัน</b><br>
                    <b>ตอบ: {ans} อัน</b></span>"""
                else:
                    m1 = random.randint(4, 8); m2 = random.randint(4, 8); q_mul = random.randint(3, 4)
                    q = f"ตาชั่งสมดุลให้ข้อมูลดังนี้:<br>- <b>{i1} 1 ชิ้น</b> หนักเท่ากับ <b>{i2} {m1} ชิ้น</b><br>- <b>{i2} 1 ชิ้น</b> หนักเท่ากับ <b>{i3} {m2} ชิ้น</b><br>อยากทราบว่า <b>{i1} จำนวน {q_mul} ชิ้น</b> จะมีน้ำหนักเท่ากับ <b>{i3}</b> กี่ชิ้น?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: แทนค่าสิ่งของข้ามกัน (หาความสัมพันธ์โดยตรง)</b><br>
                    - นำ {i3} ไปวางแทนที่ {i2} ในบรรทัดแรก<br>
                    - จะได้: {i1} 1 ชิ้น = {m1} × {m2} = <b>{m1 * m2} ชิ้น (ของ {i3})</b><br>
                    <b>ขั้นตอนที่ 2: หาคำตอบตามจำนวนที่โจทย์ถาม</b><br>
                    - โจทย์ถามหา {i1} จำนวน {q_mul} ชิ้น ➔ ให้นำความสัมพันธ์ไปคูณด้วย {q_mul}<br>
                    - จะได้: {m1 * m2} × {q_mul} = <b>{m1 * m2 * q_mul} ชิ้น</b><br>
                    <b>ตอบ: {m1 * m2 * q_mul} ชิ้น</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "ปัญหาผลรวม-ผลต่าง":
                n1, n2, n3 = random.sample(NAMES, 3); itm = random.choice(ITEMS)
                if is_challenge:
                    a = random.randint(30, 50); b = a + random.randint(10, 20); c = b + random.randint(10, 20)
                    total = a + b + c; diff_bc = c - b; diff_ac = c - a
                    q = f"<b>{n1}, {n2}, และ {n3}</b> มี<b>{itm}</b>รวมกัน <b>{total}</b> ชิ้น <br>ถ้า <b>{n3}</b> มีมากกว่า <b>{n2}</b> อยู่ <b>{diff_bc}</b> ชิ้น และ <b>{n3}</b> มีมากกว่า <b>{n1}</b> อยู่ <b>{diff_ac}</b> ชิ้น <br>จงหาว่า <b>{n3} (คนที่มีเยอะที่สุด)</b> มีกี่ชิ้น?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (การปรับให้เท่ากัน 3 คน):</b><br>
                    เทคนิคคือ สมมติให้ทุกคนมีของเท่ากับ {n3} (คนที่มากที่สุด) เพื่อให้ตั้งหารได้ง่ายๆ!<br>
                    <b>ขั้นตอนที่ 1: เติมของในจินตนาการให้คนที่ขาด</b><br>
                    - ต้องเติมของให้ {n1} จำนวน {diff_ac} ชิ้น และเติมให้ {n2} จำนวน {diff_bc} ชิ้น เพื่อให้ทุกคนมีเท่ากับ {n3}<br>
                    <b>ขั้นตอนที่ 2: หายอดรวมสมมติใหม่</b><br>
                    - ยอดเดิม {total} + เติมของให้ n1 {diff_ac} + เติมของให้ n2 {diff_bc} = <b>{total+diff_ac+diff_bc} ชิ้น</b><br>
                    - ในสถานการณ์จำลองนี้ ทุกคนมีของเท่ากับ {n3} เป๊ะๆ ทั้ง 3 คนแล้ว!<br>
                    <b>ขั้นตอนที่ 3: หาจำนวนของ {n3}</b><br>
                    - นำยอดรวมสมมติมาแบ่ง 3 ส่วนเท่าๆ กัน: {total+diff_ac+diff_bc} ÷ 3 = <b>{c} ชิ้น</b><br>
                    <b>ตอบ: {c} ชิ้น</b></span>"""
                else:
                    small = random.randint(500, 1500); diff = random.randint(100, 300); large = small + diff; total = large + small
                    q = f"<b>{n1}</b> และ <b>{n2}</b> มี<b>{itm}</b>รวมกัน <b>{total}</b> ชิ้น หาก <b>{n1}</b> มีมากกว่า <b>{n2}</b> อยู่ <b>{diff}</b> ชิ้น จงหาว่า <b>{n1}</b> มีกี่ชิ้น?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: หักส่วนที่ต่างกันทิ้งไปก่อน</b><br>
                    - นำของทั้งหมด หักส่วนที่ {n1} มีเกินมาออกไป: {total} - {diff} = <b>{total - diff} ชิ้น</b><br>
                    - ตอนนี้ของที่เหลือ จะเป็นของที่แบ่งให้สองคนได้เท่าๆ กันพอดี<br>
                    <b>ขั้นตอนที่ 2: แบ่งของออกเป็น 2 ส่วนเท่าๆ กัน</b><br>
                    - นำไปแบ่งครึ่ง (จะเป็นปริมาณของคนที่มีน้อยกว่า): ({total - diff}) ÷ 2 = <b>{small} ชิ้น</b><br>
                    <b>ขั้นตอนที่ 3: หาของของคนที่มีมากกว่า ({n1})</b><br>
                    - นำปริมาณที่แบ่งได้ ไปบวกส่วนที่หักทิ้งคืนกลับมาให้ {n1}: {small} + {diff} = <b>{large} ชิ้น</b><br>
                    <b>ตอบ: {large} ชิ้น</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "แถวคอยแบบซ้อนทับ":
                n1, n2 = random.sample(NAMES, 2); loc = random.choice(LOCS)
                if is_challenge:
                    overlap = random.randint(3, 10); total_people = random.randint(50, 100)
                    sum_pos = total_people + overlap; front_pos = random.randint(overlap + 5, total_people - 5)
                    back_pos = sum_pos - front_pos; ans = overlap - 2
                    q = f"นักเรียนเข้าแถวรอเข้า<b>{loc}</b> มีคนทั้งหมด <b>{total_people}</b> คน<br>ถ้า <b>{n1}</b> ยืนลำดับที่ <b>{front_pos}</b> นับจากหัวแถว และ <b>{n2}</b> ยืนลำดับที่ <b>{back_pos}</b> นับจากท้ายแถว <br>มีคนยืนอยู่ระหว่าง <b>{n1}</b> กับ <b>{n2}</b> กี่คน? <br><span style='font-size:16px; color:#7f8c8d;'>(คำใบ้: ระวังการนับซ้อนทับกัน)</span>"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (ระวังแถวเหลื่อมทับกัน):</b><br>
                    <b>ขั้นตอนที่ 1: ตรวจสอบการซ้อนทับกันของแถว</b><br>
                    - นำลำดับคนที่นับจากหัวและนับจากท้ายมาบวกกัน: {front_pos} + {back_pos} = <b>{sum_pos} คน</b><br>
                    - จะพบว่าผลบวก 'เกิน' จำนวนคนทั้งหมดที่มีจริง ({total_people} คน) แสดงว่าพวกเขายืน <b>'ไขว้ทับกัน'</b> ไปแล้ว!<br>
                    <b>ขั้นตอนที่ 2: หาจำนวนคนที่ถูกนับเบิ้ล (Overlap)</b><br>
                    - นำผลบวกไปลบจำนวนคนทั้งหมด = {sum_pos} - {total_people} = <b>{overlap} คน</b> (ยอดนี้คือคนที่ถูกนับซ้ำ ซึ่งรวม {n1} และ {n2} ไปด้วย)<br>
                    <b>ขั้นตอนที่ 3: หักตัวละครหลักออกเพื่อหาคนตรงกลาง</b><br>
                    - เราต้องการหาคน 'ระหว่างกลาง' จึงต้องหัก {n1} และ {n2} ทิ้งออกไปจากกลุ่มที่ทับกัน: {overlap} - 2 = <b>{ans} คน</b><br>
                    <b>ตอบ: {ans} คน</b></span>"""
                else:
                    front_pos = random.randint(40, 80); back_pos = random.randint(40, 80)
                    total_people = front_pos + back_pos + random.randint(5, 15); between = total_people - (front_pos + back_pos)
                    q = f"นักเรียนเข้าแถว มีคนทั้งหมด <b>{total_people}</b> คน<br>ถ้า <b>{n1}</b> ยืนลำดับที่ <b>{front_pos}</b> จากหัวแถว และ <b>{n2}</b> ลำดับที่ <b>{back_pos}</b> จากท้ายแถว <br>มีคนยืนอยู่ระหว่าง 2 คนนี้กี่คน? (กำหนดให้ {n1} ยืนหน้า {n2})"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: หาจำนวนคนในกลุ่มด้านหน้าและด้านหลัง</b><br>
                    - กลุ่มด้านหน้ามีตั้งแต่หัวแถวจนถึง {n1} = {front_pos} คน<br>
                    - กลุ่มด้านหลังมีตั้งแต่ท้ายแถวจนถึง {n2} = {back_pos} คน<br>
                    <b>ขั้นตอนที่ 2: หักกลุ่มหน้าและกลุ่มหลังออกจากยอดรวมทั้งหมด</b><br>
                    - นำคนทั้งหมด ลบด้วยกลุ่มทั้งสองออกไป จะเหลือแต่คนตรงกลาง<br>
                    - คำนวณ: {total_people} - ({front_pos} + {back_pos}) = <b>{between} คน</b><br>
                    <b>ตอบ: {between} คน</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "คิววงกลมมรณะ":
                n1, n2, n3 = random.sample(NAMES, 3)
                if is_challenge:
                    n_half = random.randint(15, 30); total = n_half * 2
                    pos1 = random.randint(1, n_half); pos2 = pos1 + n_half
                    add_pos = random.randint(3, 8); pos3 = (pos2 + add_pos) % total
                    if pos3 == 0: pos3 = total
                    q = f"เด็กยืนล้อมเป็นวงกลมเว้นระยะห่างเท่าๆ กัน นับหมายเลข 1, 2, 3... <br>ถ้า <b>{n1}</b> หมายเลข <b>{pos1}</b> มองตรงไปฝั่งตรงข้ามพอดี พบ <b>{n2}</b> หมายเลข <b>{pos2}</b> <br>และถ้า <b>{n3}</b> ยืนอยู่ถัดจาก {n2} ไปทางซ้ายมือ (นับเพิ่มขึ้น) อีก <b>{add_pos} คน</b><br>จงหาว่าเด็กกลุ่มนี้มีทั้งหมดกี่คน และ <b>{n3}</b> คือหมายเลขใด?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (ตำแหน่งสัมพันธ์วงกลม):</b><br>
                    <b>ขั้นตอนที่ 1: หาจำนวนคนทั้งหมดจากรหัสฝั่งตรงข้าม</b><br>
                    - ระยะห่างระหว่างสองคนที่ยืนอยู่ฝั่งตรงข้ามกัน คือ 'ครึ่งวงกลม' เสมอ<br>
                    - หาคนครึ่งวงกลม = นำเบอร์มาลบกัน ➔ {pos2} - {pos1} = <b>{n_half} คน</b><br>
                    - หาคนเต็มวงกลม = ครึ่งวงกลม × 2 ➔ {n_half} × 2 = <b>{total} คน</b><br>
                    <b>ขั้นตอนที่ 2: หาตำแหน่งที่ยืนของ {n3}</b><br>
                    - {n3} ยืนถัดจาก {n2} ไปอีก {add_pos} ตำแหน่ง: {pos2} + {add_pos} = <b>{pos2+add_pos}</b><br>
                    - (ข้อควรระวัง: ถ้ายอดการนับเกินจำนวนคนรวม ให้หักออกเป็นรอบๆ ด้วย {total})<br>
                    - หมายเลขสุดท้ายของ {n3} จะไปตกที่ตำแหน่ง <b>{pos3}</b><br>
                    <b>ตอบ: มีทั้งหมด {total} คน และ {n3} คือหมายเลข {pos3}</b></span>"""
                else:
                    n_half = random.randint(20, 40); total = n_half * 2
                    pos1 = random.randint(1, n_half); pos2 = pos1 + n_half
                    q = f"เด็กยืนล้อมวงกลมเว้นระยะเท่าๆ กัน นับหมายเลขเรียง 1, 2... <br>ถ้า <b>{n1}</b> หมายเลข <b>{pos1}</b> มองฝั่งตรงข้ามพบ <b>{n2}</b> หมายเลข <b>{pos2}</b> เด็กกลุ่มนี้มีกี่คน?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: วิเคราะห์เงื่อนไข 'ฝั่งตรงข้าม'</b><br>
                    - การยืนฝั่งตรงข้ามกันในวงกลม หมายความว่าระยะห่างระหว่างคนสองคนนี้คือ 'ครึ่งวงกลม' พอดีเป๊ะ<br>
                    <b>ขั้นตอนที่ 2: คำนวณหาจำนวนคน</b><br>
                    - หาจำนวนคนครึ่งวงกลม: นำหมายเลขมาลบกัน {pos2} - {pos1} = <b>{n_half} คน</b><br>
                    - หาจำนวนคนเต็มวงกลม: นำครึ่งวงกลมคูณด้วย 2 ➔ {n_half} × 2 = <b>{total} คน</b><br>
                    <b>ตอบ: {total} คน</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "การคิดย้อนกลับ":
                name = random.choice(NAMES); item = random.choice(ITEMS)
                if is_challenge:
                    end_val = random.randint(10, 30); div_v = random.choice([2, 3, 4]); step3 = end_val * div_v
                    sub_v = random.randint(10, 20); step2 = step3 + sub_v; mul_v = random.choice([2, 3])
                    while step2 % mul_v != 0: sub_v += 1; step2 = step3 + sub_v
                    step1 = step2 // mul_v; add_v = random.randint(5, 15)
                    if step1 <= add_v: add_v = step1 - random.randint(1, 3); add_v = max(add_v, 1)
                    X = step1 - add_v
                    
                    q = f"<b>{name}</b> คิดเลขปริศนาในใจขั้นตอนดังนี้:<br>นำจำนวนปริศนามา <b>บวกด้วย {add_v}</b>, จากนั้นนำผลลัพธ์ <b>คูณด้วย {mul_v}</b>, <br>แล้ว <b>ลบออกด้วย {sub_v}</b>, และสุดท้าย <b>หารด้วย {div_v}</b> <br>ปรากฏว่าผลลัพธ์สุดท้ายคือ <b>{end_val}</b> พอดี จงหา 'จำนวนปริศนา' นั้น?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (Reverse Engineering 4 ชั้น):</b><br>
                    เทคนิค: ทำย้อนกลับจากเหตุการณ์หลังสุดไปหาหน้าสุด และ 'สลับเครื่องหมาย' ให้ตรงกันข้ามทั้งหมด!<br>
                    <b>ชั้นที่ 1 (ย้อนจากผลลัพธ์สุดท้าย):</b> เปลี่ยน หาร เป็น คูณ ➔ นำ {end_val} × {div_v} = <b>{step3}</b><br>
                    <b>ชั้นที่ 2 (ย้อนถัดมา):</b> เปลี่ยน ลบ เป็น บวก ➔ นำ {step3} + {sub_v} = <b>{step2}</b><br>
                    <b>ชั้นที่ 3 (ย้อนถัดมา):</b> เปลี่ยน คูณ เป็น หาร ➔ นำ {step2} ÷ {mul_v} = <b>{step1}</b><br>
                    <b>ชั้นที่ 4 (ย้อนไปหาตัวแรกสุด):</b> เปลี่ยน บวก เป็น ลบ ➔ นำ {step1} - {add_v} = <b>{X}</b><br>
                    <b>ตอบ: {X}</b></span>"""
                else:
                    sm, sp, rv = random.randint(1000, 3000), random.randint(200, 800), random.randint(500, 1500)
                    fm = sm - sp + rv
                    q = f"<b>{name}</b>นำเงินไปซื้อ<b>{item}</b> <b>{sp:,}</b> บาท จากนั้นแม่ให้เพิ่มอีก <b>{rv:,}</b> บาท ทำให้มีเงิน <b>{fm:,}</b> บาท <br>ตอนแรกมีเงินกี่บาท?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (คิดย้อนกลับ):</b><br>
                    <b>ขั้นตอนที่ 1: เริ่มจากยอดเงินปัจจุบัน</b><br>
                    - ตอนนี้มีเงินสุทธิ: {fm:,} บาท<br>
                    <b>ขั้นตอนที่ 2: ย้อนเหตุการณ์ 'แม่ให้เงิน'</b><br>
                    - แม่ให้เพิ่มแปลว่าบวก ถ้าย้อนกลับต้องเอาไป <b>ลบออก</b>: {fm:,} - {rv:,} = <b>{fm - rv:,} บาท</b><br>
                    <b>ขั้นตอนที่ 3: ย้อนเหตุการณ์ 'ซื้อของ'</b><br>
                    - ซื้อของแปลว่าจ่ายไป ถ้าย้อนกลับต้องเอาไป <b>บวกคืน</b>: {fm - rv:,} + {sp:,} = <b>{sm:,} บาท</b><br>
                    <b>ตอบ: {sm:,} บาท</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "โปรโมชั่นแลกของ":
                snack = random.choice(SNACKS)
                if is_challenge:
                    exch = random.choice([3, 4, 5]); start_bottles = random.randint(20, 40)
                    total_drank = start_bottles; empties = start_bottles
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
                        - เมื่อคำนวณการแลกซองเปล่าไปเรื่อยๆ จนกว่าจะแลกต่อไม่ได้ จะพบว่าเหลือเศษซองเปล่าตอนจบ <b>{empties} ซอง</b><br>
                        <b>ขั้นตอนที่ 2: ใช้ทริคการยืมของเพื่อน</b><br>
                        - เนื่องจากโปรโมชั่นต้องใช้ {exch} ซอง และตอนนี้เขาขาดอีกแค่ 1 ซอง เขาจึงขอยืมเพื่อนมา 1 ซอง (รวมกับที่มีอยู่เป็น {exch} ซองพอดีเป๊ะ)<br>
                        <b>ขั้นตอนที่ 3: แลกของและคืนของ</b><br>
                        - นำ {exch} ซองนี้ไปแลก จะได้กินฟรีอีก 1 ชิ้น! <br>
                        - และเมื่อกินเสร็จ จะมีซองเปล่าเหลือจากชิ้นนี้ 1 ซอง จึงนำไป <b>'คืนเพื่อน'</b> ได้พอดีไม่มีหนี้สิน!<br>
                        - รวมได้กินทั้งหมด <b>{total_drank} ชิ้น</b><br>
                        <b>ตอบ: {total_drank} ชิ้น</b></span>"""
                    else:
                        sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                        <b>ขั้นตอนที่ 1: นำของเดิมไปแลกเป็นทอดๆ ตามปกติ</b><br>
                        - เมื่อคำนวณการแลกซองเปล่าไปเรื่อยๆ จนกว่าจะแลกต่อไม่ได้ จะพบว่าเหลือเศษซองเปล่าตอนจบ <b>{empties} ซอง</b><br>
                        <b>ขั้นตอนที่ 2: เช็กเงื่อนไขการยืมของเพื่อน</b><br>
                        - เนื่องจากเขาขาดซองเปล่าอีกหลายซอง จึงไม่เข้าเงื่อนไขที่จะสามารถยืม 1 ซองเพื่อไปแลกแล้วมีคืนได้ (ถ้าขาดแค่ 1 ซองเป๊ะๆ ถึงจะทำทริคนี้ได้)<br>
                        - ดังนั้นจึงแลกต่อไม่ได้แล้ว รวมได้กินทั้งหมด <b>{total_drank} ชิ้น</b><br>
                        <b>ตอบ: {total_drank} ชิ้น</b></span>"""
                else:
                    exch = random.randint(5, 8); start_bottles = random.randint(30, 60)
                    total_drank = start_bottles; empties = start_bottles
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

            # ---------------------------------------------------------
            elif actual_sub_t == "ตรรกะการจับมือ (ทักทาย)":
                loc = random.choice(LOCS)
                if is_challenge:
                    n_a = random.randint(10, 15); n_b = random.randint(10, 15); ans = n_a * n_b
                    q = f"ในงานกิจกรรมที่<b>{loc}</b> มีเด็กชาย <b>{n_a}</b> คน และเด็กหญิง <b>{n_b}</b> คน<br>ถ้า <b>'เด็กชายทุกคนต้องจับมือกับเด็กหญิงทุกคน'</b> (ไม่จับมือกับเพศเดียวกัน) จะมีการจับมือเกิดขึ้นทั้งหมดกี่ครั้ง?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (กฎการคูณแบบข้ามกลุ่ม Bipartite):</b><br>
                    ข้อนี้ไม่ได้จับมือรวมกันทั้งหมด แต่เป็นการเชื่อมโยงระหว่าง 2 กลุ่มที่แยกกัน!<br>
                    <b>ขั้นตอนที่ 1: ดูมุมมองจากเด็กชาย 1 คน</b><br>
                    - เด็กชาย 1 คน จะต้องเดินไปจับมือทำความรู้จักเด็กหญิงให้ครบทั้ง {n_b} คน (จะเกิดการจับมือขึ้น {n_b} ครั้ง)<br>
                    <b>ขั้นตอนที่ 2: ดูมุมมองในภาพรวม</b><br>
                    - เนื่องจากในงานมีเด็กชายทั้งหมด {n_a} คน ดังนั้นเหตุการณ์ในขั้นตอนที่ 1 จะเกิดขึ้นซ้ำๆ กัน<br>
                    <b>ขั้นตอนที่ 3: ใช้การคูณเพื่อหาคำตอบ</b><br>
                    - นำจำนวนคนทั้งสองกลุ่มมาคูณกัน: {n_a} คน × {n_b} คน = <b>{ans:,} ครั้ง</b><br>
                    <b>ตอบ: {ans:,} ครั้ง</b></span>"""
                else:
                    n = random.randint(10, 20); ans = sum(range(1, n))
                    q = f"ในการจัดกิจกรรม มีเด็ก <b>{n}</b> คน หากเด็กทุกคนจับมือทำความรู้จักกันให้ครบทุกคน จะมีการจับมือเกิดขึ้นทั้งหมดกี่ครั้ง?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1:</b> คนที่ 1 เดินไปจับมือกับคนอื่นทุกคน จะเกิดการจับ {n-1} ครั้ง<br>
                    <b>ขั้นตอนที่ 2:</b> คนที่ 2 เดินไปจับคนอื่น (แต่ไม่ต้องจับคนที่ 1 แล้วเพราะจับไปแล้ว) จะเกิดการจับ {n-2} ครั้ง<br>
                    <b>ขั้นตอนที่ 3:</b> จำนวนจะลดหลั่นลงไปเรื่อยๆ ทีละ 1 จนถึงคนสุดท้ายที่ไม่มีใครให้จับเพิ่ม<br>
                    <b>ขั้นตอนที่ 4:</b> นำตัวเลขมาบวกกัน: {' + '.join(str(x) for x in range(n-1, 0, -1))} = <b>{ans} ครั้ง</b><br>
                    <b>ตอบ: {ans} ครั้ง</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "หยิบของในที่มืด":
                item = random.choice(ITEMS)
                if is_challenge:
                    c1, c2, c3 = random.randint(10, 20), random.randint(10, 20), random.randint(10, 20)
                    arr = sorted([c1, c2, c3], reverse=True); ans = arr[0] + arr[1] + 1
                    q = f"ในกล่องทึบมี<b>{item}</b>สีแดง <b>{c1}</b> ชิ้น, สีน้ำเงิน <b>{c2}</b> ชิ้น, และสีเขียว <b>{c3}</b> ชิ้น<br>หากหลับตาหยิบ ต้องหยิบออกมา<b>อย่างน้อยที่สุดกี่ชิ้น</b> จึงจะมั่นใจ 100% ว่าจะได้ <b>'ครบทั้ง 3 สี อย่างน้อยสีละ 1 ชิ้น'</b> แน่นอน?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (หลักการดวงซวยที่สุดขั้นสูง):</b><br>
                    เพื่อให้มั่นใจ 100% ว่าจะได้ครบทุกสี ต้องคิดกรณีที่โชคร้ายที่สุด คือหยิบได้สีที่มีจำนวนเยอะๆ ออกมาจนเกลี้ยงกล่องก่อน!<br>
                    <b>ขั้นตอนที่ 1: หาสีที่จำนวนเยอะที่สุด 2 อันดับแรก</b><br>
                    - สีที่มีจำนวนเยอะที่สุด 2 ลำดับแรกคือสีที่มี <b>{arr[0]} ชิ้น</b> และ <b>{arr[1]} ชิ้น</b><br>
                    <b>ขั้นตอนที่ 2: จำลองความโชคร้าย</b><br>
                    - โชคร้ายสุดๆ คือหยิบได้แค่ 2 สีนี้ออกมาหมดเกลี้ยงกล่องเลย: {arr[0]} + {arr[1]} = <b>{arr[0]+arr[1]} ชิ้น</b> (ตอนนี้มีของเต็มมือ แต่มีแค่ 2 สีเท่านั้น)<br>
                    <b>ขั้นตอนที่ 3: หยิบเพื่อปิดจ๊อบ</b><br>
                    - ในกล่องตอนนี้จะเหลือแค่ 'สีที่ 3' ล้วนๆ ดังนั้นการหยิบชิ้นต่อไป (บวก 1) จะการันตีร้อยเปอร์เซ็นต์ว่าได้สีครบ 3 สีแน่นอน!<br>
                    - คำนวณ: {arr[0]+arr[1]} + 1 = <b>{ans} ชิ้น</b><br>
                    <b>ตอบ: {ans} ชิ้น</b></span>"""
                else:
                    c1, c2, c3, c4 = random.randint(15, 30), random.randint(15, 30), random.randint(15, 30), random.randint(5, 15)
                    c_total = c1+c2+c3; target_color = "สีเหลือง"
                    q = f"ในกล่องทึบมี<b>{item}</b>สีแดง <b>{c1}</b> ชิ้น, สีน้ำเงิน <b>{c2}</b> ชิ้น, สีเขียว <b>{c3}</b> ชิ้น, สีเหลือง <b>{c4}</b> ชิ้น<br>ต้องหยิบ<b>อย่างน้อยกี่ชิ้น</b> จึงจะมั่นใจ 100% ว่าจะได้<b>{target_color}</b>อย่างน้อย 1 ชิ้น?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (หลักการดวงซวยที่สุด):</b><br>
                    <b>ขั้นตอนที่ 1: จำลองความโชคร้าย</b><br>
                    - กรณีโชคร้ายที่สุด คือเราอยากได้{target_color} แต่มือเจ้ากรรมดันหยิบได้สีอื่นจนหมดเกลี้ยงกล่องก่อน<br>
                    - สีอื่นรวมกันมี: {c1} + {c2} + {c3} = <b>{c_total} ชิ้น</b><br>
                    <b>ขั้นตอนที่ 2: หยิบเพื่อปิดจ๊อบ</b><br>
                    - เมื่อสีอื่นหมดกล่องแล้ว ของชิ้นต่อไปที่เราจะหยิบ (บวกเพิ่ม 1) จะการันตีว่าเป็น{target_color}แน่นอน 100%<br>
                    - คำนวณ: {c_total} + 1 = <b>{c_total+1} ชิ้น</b><br>
                    <b>ตอบ: {c_total+1} ชิ้น</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "แผนภาพความชอบ":
                n1, n2, n3 = random.sample(SNACKS, 3)
                if is_challenge:
                    tot = random.randint(150, 200)
                    only_A, only_B, only_C = random.randint(10, 20), random.randint(10, 20), random.randint(10, 20)
                    A_B, B_C, A_C = random.randint(5, 10), random.randint(5, 10), random.randint(5, 10); all_3 = random.randint(3, 8)
                    neither = random.randint(5, 15)
                    like_A = only_A + A_B + A_C + all_3
                    like_B = only_B + A_B + B_C + all_3
                    like_C = only_C + A_C + B_C + all_3
                    real_tot = only_A + only_B + only_C + A_B + B_C + A_C + all_3 + neither
                    
                    q = f"สำรวจนักเรียน <b>{real_tot}</b> คน พบว่ามีคนชอบ <b>{n1} {like_A} คน</b>, ชอบ <b>{n2} {like_B} คน</b>, และชอบ <b>{n3} {like_C} คน</b><br>โดยมีคนที่ชอบ {n1}และ{n2} (แต่ไม่ชอบ{n3}) <b>{A_B} คน</b>, ชอบ {n2}และ{n3} (แต่ไม่ชอบ{n1}) <b>{B_C} คน</b>, ชอบ {n1}และ{n3} (แต่ไม่ชอบ{n2}) <b>{A_C} คน</b><br>และคนที่ชอบทั้ง 3 อย่างมี <b>{all_3} คน</b> จงหาว่ามีนักเรียนกี่คนที่ <b>'ไม่ชอบ'</b> ขนมทั้ง 3 ชนิดนี้เลย?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (แผนภาพเวนน์ 3 วง):</b><br>
                    <b>ขั้นตอนที่ 1: หาคนที่ชอบอย่างใดอย่างหนึ่งล้วนๆ แบบเพียวๆ</b><br>
                    - ชอบ {n1} ล้วนๆ = ยอดคนชอบ {n1} - (ยอดที่ซ้อนทับกับวงอื่น) ➔ {like_A} - ({A_B}+{A_C}+{all_3}) = <b>{only_A} คน</b><br>
                    - ชอบ {n2} ล้วนๆ = ยอดคนชอบ {n2} - (ยอดที่ซ้อนทับกับวงอื่น) ➔ {like_B} - ({A_B}+{B_C}+{all_3}) = <b>{only_B} คน</b><br>
                    - ชอบ {n3} ล้วนๆ = ยอดคนชอบ {n3} - (ยอดที่ซ้อนทับกับวงอื่น) ➔ {like_C} - ({A_C}+{B_C}+{all_3}) = <b>{only_C} คน</b><br>
                    <b>ขั้นตอนที่ 2: รวมคนที่ชอบขนม (ทุกส่วนย่อยในวงกลมบวกกัน)</b><br>
                    - {only_A} + {only_B} + {only_C} + {A_B} + {B_C} + {A_C} + {all_3} = <b>{real_tot - neither} คน</b> (นี่คือคนที่ชอบอย่างน้อย 1 ชนิด)<br>
                    <b>ขั้นตอนที่ 3: หาคนที่ไม่ชอบเลย (คนที่อยู่นอกวงกลม)</b><br>
                    - นำยอดคนทั้งหมด ลบยอดรวมคนที่ชอบขนม ➔ {real_tot} - {real_tot - neither} = <b>{neither} คน</b><br>
                    <b>ตอบ: {neither} คน</b></span>"""
                else:
                    tot = random.randint(100, 200); both = random.randint(20, 50)
                    only_a = random.randint(10, 20); only_b = random.randint(10, 20)
                    l_a = only_a + both; l_b = only_b + both
                    neither = tot - (only_a + only_b + both)
                    q = f"สำรวจนักเรียน <b>{tot}</b> คน พบว่าชอบ<b>{n1}</b> <b>{l_a}</b> คน, ชอบ<b>{n2}</b> <b>{l_b}</b> คน, และชอบทั้งสองอย่าง <b>{both}</b> คน <br>มีกี่คนที่ไม่ชอบกินขนมทั้งสองชนิดนี้เลย?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: หาคนที่ชอบชนิดเดียวล้วนๆ</b><br>
                    - ชอบ {n1} อย่างเดียว: นำคนชอบ {n1} ลบตรงกลาง ➔ {l_a} - {both} = <b>{only_a} คน</b><br>
                    - ชอบ {n2} อย่างเดียว: นำคนชอบ {n2} ลบตรงกลาง ➔ {l_b} - {both} = <b>{only_b} คน</b><br>
                    <b>ขั้นตอนที่ 2: รวมคนที่ชอบขนม</b><br>
                    - นำยอดทั้ง 3 ส่วนมาบวกกัน: {only_a} + {only_b} + {both} = <b>{only_a + only_b + both} คน</b><br>
                    <b>ขั้นตอนที่ 3: หาคนที่ไม่ชอบเลย</b><br>
                    - นำคนทั้งหมดลบคนที่ชอบขนม: {tot} - {only_a + only_b + both} = <b>{neither} คน</b><br>
                    <b>ตอบ: {neither} คน</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "ผลบวกจำนวนเรียงกัน (Gauss)":
                if is_challenge:
                    even = random.choice([True, False]); N = random.choice([50, 100, 200])
                    if even:
                        ans = (N//2) * (N//2 + 1)
                        q = f"จงหาผลบวกของ <b>'จำนวนคู่'</b> ทุกจำนวน ตั้งแต่ 1 ถึง {N} <br>( 2 + 4 + 6 + ... + {N} = ? )"
                        sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (ผลบวกเกาส์แบบกระโดด):</b><br>
                        <b>ขั้นตอนที่ 1: หาจำนวนตัวเลขทั้งหมดในอนุกรม</b><br>
                        - ตั้งแต่ 1 ถึง {N} มีเลขคู่ทั้งหมดครึ่งหนึ่ง คือ {N} ÷ 2 = <b>{N//2} ตัว</b><br>
                        <b>ขั้นตอนที่ 2: ใช้หลักการจับคู่หัว-ท้าย</b><br>
                        - ผลบวกของ 1 คู่ (ตัวแรกสุด + ตัวหลังสุด) = 2 + {N} = <b>{N+2}</b><br>
                        - เรามีเลข {N//2} ตัว นำมาจับคู่กัน 2 ตัว จะได้ {N//2} ÷ 2 = <b>{(N//2)/2} คู่</b><br>
                        <b>ขั้นตอนที่ 3: หาผลรวมทั้งหมด</b><br>
                        - นำผลบวก 1 คู่ × จำนวนคู่ทั้งหมด ➔ {N+2} × {(N//2)/2} = <b>{ans:,}</b><br>
                        <b>ตอบ: {ans:,}</b></span>"""
                    else:
                        ans = (N//2) ** 2
                        q = f"จงหาผลบวกของ <b>'จำนวนคี่'</b> ทุกจำนวน ตั้งแต่ 1 ถึง {N-1} <br>( 1 + 3 + 5 + ... + {N-1} = ? )"
                        sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (ผลบวกเกาส์แบบกระโดด):</b><br>
                        <b>ขั้นตอนที่ 1: หาจำนวนตัวเลขทั้งหมดในอนุกรม</b><br>
                        - ตั้งแต่ 1 ถึง {N-1} มีเลขคี่ทั้งหมดครึ่งหนึ่งของ {N} คือ <b>{N//2} ตัว</b><br>
                        <b>ขั้นตอนที่ 2: ใช้หลักการจับคู่หัว-ท้าย</b><br>
                        - ผลบวกของ 1 คู่ (ตัวแรกสุด + ตัวหลังสุด) = 1 + {N-1} = <b>{N}</b><br>
                        - เรามีเลข {N//2} ตัว นำมาจับคู่กัน 2 ตัว จะได้ {N//2} ÷ 2 = <b>{(N//2)/2} คู่</b><br>
                        <b>ขั้นตอนที่ 3: หาผลรวมทั้งหมด (หรือใช้สูตรลัดเลขคี่ = จำนวนตัว²)</b><br>
                        - นำผลบวก 1 คู่ × จำนวนคู่ทั้งหมด ➔ {N} × {(N//2)/2} = {N//2} × {N//2} = <b>{ans:,}</b><br>
                        <b>ตอบ: {ans:,}</b></span>"""
                else:
                    n = random.choice([100, 200, 500])
                    ans = (n * (n + 1)) // 2
                    q = f"จงหาผลบวกของตัวเลขเรียงลำดับตั้งแต่ 1 ถึง {n} <br>( 1 + 2 + 3 + ... + {n} = ? )"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (หลักการจับคู่ของเกาส์):</b><br>
                    <b>ขั้นตอนที่ 1: หาผลบวกของการจับคู่หัว-ท้าย</b><br>
                    - นำตัวเลขน้อยสุด + ตัวเลขมากสุด: 1 + {n} = <b>{n+1}</b> (ทุกคู่ที่จับเข้าหากันจะได้ยอดนี้เสมอ)<br>
                    <b>ขั้นตอนที่ 2: หาจำนวนคู่ทั้งหมด</b><br>
                    - มีตัวเลขทั้งหมด {n} ตัว จัดเป็นคู่ๆ (หาร 2) จะได้ {n} ÷ 2 = <b>{n//2} คู่</b><br>
                    <b>ขั้นตอนที่ 3: หาผลบวกทั้งหมด</b><br>
                    - นำผลบวก 1 คู่ × จำนวนคู่ทั้งหมด: {n+1} × {n//2} = <b>{ans:,}</b><br>
                    <b>ตอบ: {ans:,}</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "เศษส่วนของที่เหลือ":
                item = random.choice(ITEMS)
                f1_n, f1_d = random.choice([(2,5), (3,5), (1,4), (3,4), (2,7)]); f2_n, f2_d = random.choice([(1,3), (2,3), (1,2), (3,8), (1,4)]); k = random.choice([50, 100, 150, 200])
                lcm_den = f1_d * f2_d; tot = k * lcm_den; spent1 = (tot * f1_n) // f1_d; rem1 = tot - spent1; spent2 = (rem1 * f2_n) // f2_d; ans = rem1 - spent2
                f1_html = get_vertical_fraction(f1_n, f1_d); f2_html = get_vertical_fraction(f2_n, f2_d)
                
                q = f"<b>{name}</b> มีเงินอยู่ {tot:,} บาท นำไปซื้อขนม {f1_html} ของเงินทั้งหมด และนำไปซื้อ<b>{item}</b>อีก {f2_html} <b>ของเงินที่เหลือ</b> <br>จงหาว่าตอนนี้ <b>{name}</b> เหลือเงินกี่บาท?"
                sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                ข้อนี้มีจุดหลอกตรงคำว่า <b>"ของเงินที่เหลือ"</b> ต้องหักเงินออกให้เสร็จทีละรอบก่อนครับ!<br>
                <b>ขั้นตอนที่ 1: คำนวณก้อนแรก (ซื้อขนม)</b><br>
                - ซื้อไป {get_vertical_fraction(f1_n, f1_d, is_bold=False)} ของเงินทั้งหมด ({tot:,} บาท)<br>
                - คำนวณ: ({f1_n} × {tot:,}) ÷ {f1_d} = <b>{spent1:,} บาท</b><br>
                - <u>เงินคงเหลือรอบแรก</u> = {tot:,} - {spent1:,} = <b>{rem1:,} บาท</b><br>
                <b>ขั้นตอนที่ 2: คำนวณก้อนที่สอง (ซื้อ{item})</b><br>
                - ซื้อไป {get_vertical_fraction(f2_n, f2_d, is_bold=False)} <b>ของเงินที่เหลือ</b> (ซึ่งก็คือ {rem1:,} บาท)<br>
                - คำนวณ: ({f2_n} × {rem1:,}) ÷ {f2_d} = <b>{spent2:,} บาท</b><br>
                <b>ขั้นตอนที่ 3: หาเงินคงเหลือสุทธิ</b><br>
                - นำเงินคงเหลือรอบแรกลบด้วยเงินที่ใช้ไปรอบสอง: {rem1:,} - {spent2:,} = <b>{ans:,} บาท</b><br>
                <b>ตอบ: {ans:,} บาท</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "ปริศนาตัวเลขซ่อนแอบ":
                a = random.randint(1, 4); b = random.randint(a + 2, 9); diff = b - a; k = diff * 9; sum_val = a + b
                if is_challenge:
                    q = f"A และ B เป็นเลขโดดที่ต่างกัน กำหนดสมการ <b>BA - AB = {k}</b> และ <b>A + B = {sum_val}</b> <br>จงหาผลคูณของ <b>A × B</b> ?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (รหัสสลับหลัก):</b><br>
                    <b>ขั้นตอนที่ 1: ใช้กฎของเลขสลับหลัก</b><br>
                    - ผลต่างของจำนวน 2 หลักที่สลับหลักกัน (BA - AB) จะมีค่าเท่ากับ 'ผลต่างของเลขโดด × 9' เสมอ!<br>
                    - ดังนั้นเราหาระยะห่างระหว่างเลข B กับ A ได้โดย: B - A = {k} ÷ 9 = <b>{diff}</b><br>
                    <b>ขั้นตอนที่ 2: แก้สมการหาค่า A และ B</b><br>
                    - เรารู้ว่า ผลบวกของเลขโดด = {sum_val} และ ผลต่าง = {diff}<br>
                    - หาตัวเลขที่มากกว่า (B) = (ผลบวก + ผลต่าง) ÷ 2 ➔ ({sum_val} + {diff}) ÷ 2 = <b>{b}</b><br>
                    - หาตัวเลขที่น้อยกว่า (A) = ผลบวก - ตัวที่มากกว่า ➔ {sum_val} - {b} = <b>{a}</b><br>
                    <b>ขั้นตอนที่ 3: หาผลคูณตามที่โจทย์สั่ง</b><br>
                    - นำ {a} × {b} = <b>{a*b}</b><br>
                    <b>ตอบ: {a*b}</b></span>"""
                else:
                    q = f"A และ B เป็นเลขโดดที่ต่างกัน กำหนด <b>BA - {k} = AB</b> และ <b>A + B = {sum_val}</b> <br>จงหาว่าจำนวนสองหลัก <b>AB</b> คือจำนวนใด?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: จัดรูปสมการ</b><br>
                    - ย้ายข้างสมการ จะได้ BA - AB = {k}<br>
                    <b>ขั้นตอนที่ 2: ใช้กฎของเลขสลับหลัก</b><br>
                    - ผลต่างของ BA สลับหลักกับ AB มีค่าเท่ากับ (B - A) × 9 เสมอ!<br>
                    - จะได้ความห่างของเลขโดด: B - A = {k} ÷ 9 = <b>{diff}</b><br>
                    <b>ขั้นตอนที่ 3: หาค่าเลขโดด</b><br>
                    - ผลบวก={sum_val}, ผลต่าง={diff} <br>
                    - หา B: ({sum_val} + {diff}) ÷ 2 = <b>{b}</b><br>
                    - หา A: {sum_val} - {b} = <b>{a}</b><br>
                    <b>ตอบ: จำนวน AB คือ {a}{b}</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "การตัดเชือกพับทบ":
                name = random.choice(NAMES)
                if is_challenge:
                    f = random.randint(3, 5); c = random.randint(3, 6); ans = (2**f) * c + 1
                    q = f"<b>{name}</b> นำเชือกมาพับทบครึ่งซ้อนกันไปเรื่อยๆ จำนวน <b>{f} ครั้ง</b> จากนั้นใช้กรรไกรตัดเชือกให้ขาดออก <b>{c} รอยตัด</b> <br>เมื่อคลี่เชือกทั้งหมดออกมา จะได้เศษเชือกชิ้นเล็กชิ้นน้อยรวมทั้งหมดกี่เส้น?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (สูตรความหนาเชือก):</b><br>
                    <b>ขั้นตอนที่ 1: หาความหนาของเชือกหลังจากพับ</b><br>
                    - การพับครึ่ง 1 ครั้ง ความหนาของเชือกจะเพิ่มขึ้นเป็น 2 เท่า (คิดเป็น 2 ยกกำลัง)<br>
                    - พับ {f} ครั้ง = นำ 2 มาคูณกัน {f} ครั้ง ➔ <b>{2**f} ชั้น</b><br>
                    <b>ขั้นตอนที่ 2: หาจำนวนเส้นที่ได้เพิ่มจากการตัด</b><br>
                    - การใช้กรรไกรตัด 1 รอยตรงกลางเชือก จะทำให้เกิดเชือกเส้นใหม่เพิ่มขึ้นเท่ากับ "จำนวนชั้น"<br>
                    - ดังนั้น ตัด {c} รอย = ได้เชือกเพิ่มมา {2**f} × {c} = <b>{(2**f)*c} เส้น</b><br>
                    <b>ขั้นตอนที่ 3: รวมเชือกเส้นตั้งต้น</b><br>
                    - นำจำนวนเส้นที่ถูกตัดเพิ่ม ไปบวกกับเชือกเส้นเดิมก่อนพับอีก 1 เส้น: {(2**f)*c} + 1 = <b>{ans} เส้น</b><br>
                    <b>ตอบ: {ans} เส้น</b></span>"""
                else:
                    f, c = 2, random.randint(2, 4); ans = (2**f) * c + 1
                    q = f"<b>{name}</b>นำเชือกมาพับทบครึ่ง <b>{f}</b> ครั้ง จากนั้นตัดให้ขาด <b>{c}</b> รอยตัด <br>เมื่อคลี่ออกมาจะได้เชือกทั้งหมดกี่เส้น?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: หาความหนา</b><br>
                    - พับ {f} ครั้ง เกิดความหนา = 2 ยกกำลัง {f} = <b>{2**f} ชั้น</b><br>
                    <b>ขั้นตอนที่ 2: หาเส้นที่ถูกตัด</b><br>
                    - ตัด {c} รอย ได้เส้นเพิ่ม = {2**f} × {c} = <b>{(2**f)*c} เส้น</b><br>
                    <b>ขั้นตอนที่ 3: รวมเส้นตั้งต้น</b><br>
                    - รวมกับเส้นตั้งต้นที่มีอยู่แล้ว 1 เส้น: {(2**f)*c} + 1 = <b>{ans} เส้น</b><br>
                    <b>ตอบ: {ans} เส้น</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "อายุข้ามเวลาขั้นสูง":
                n1, n2, n3 = random.sample(NAMES, 3)
                if is_challenge:
                    age1, age2, age3 = random.randint(15, 20), random.randint(18, 25), random.randint(22, 30); current_sum = age1 + age2 + age3
                    past_years = random.randint(5, 10); past_sum = current_sum - (3 * past_years)
                    future_years = random.randint(5, 10); future_sum = current_sum + (3 * future_years)
                    q = f"ปัจจุบัน {n1}, {n2}, และ {n3} มีอายุรวมกัน <b>{current_sum} ปี</b> <br>ถ้าเมื่อ <b>{past_years} ปีที่แล้ว</b> ทั้งสามคนมีอายุรวมกัน <b>{past_sum} ปี</b><br>จงหาว่า <b>อีก {future_years} ปีข้างหน้า</b> ทั้งสามคนจะมีอายุรวมกันกี่ปี?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (การบวกอายุเป็นกลุ่ม):</b><br>
                    โจทย์ข้อนี้เป็นตัวหลอก! ให้ข้อมูลอดีตมาเพื่อสร้างความสับสน เราสามารถข้ามไปคิดเรื่องอนาคตได้เลย<br>
                    <b>ขั้นตอนที่ 1: วิเคราะห์การเติบโตในอนาคต</b><br>
                    - อีก {future_years} ปีข้างหน้า <b>ทุกคน (ทั้ง 3 คน)</b> จะมีอายุเพิ่มขึ้นพร้อมๆ กันคนละ {future_years} ปี<br>
                    <b>ขั้นตอนที่ 2: หาอายุรวมที่เพิ่มขึ้นของกลุ่ม</b><br>
                    - นำ {future_years} ปี × 3 คน = <b>อายุเพิ่มขึ้นรวม {3*future_years} ปี</b><br>
                    <b>ขั้นตอนที่ 3: หาผลรวมในอนาคต</b><br>
                    - นำอายุรวมปัจจุบัน ไปบวกกับ อายุรวมที่เพิ่มขึ้น: {current_sum} + {3*future_years} = <b>{future_sum} ปี</b><br>
                    <b>ตอบ: {future_sum} ปี</b></span>"""
                else:
                    age1, age2 = random.randint(15, 20), random.randint(18, 25); current_sum = age1 + age2
                    past_years = random.randint(3, 8); past_sum = current_sum - (2 * past_years)
                    q = f"ปัจจุบันพี่น้อง 2 คนคือ {n1} กับ {n2} มีอายุรวมกัน <b>{current_sum}</b> ปี <br>จงหาว่าเมื่อ <b>{past_years}</b> ปีที่แล้ว ทั้งสองคนมีอายุรวมกันกี่ปี?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: หาอายุรวมที่ลดลง</b><br>
                    - ย้อนเวลาไป {past_years} ปี <b>ทุกคน (ทั้ง 2 คน)</b> จะมีอายุน้อยลงคนละ {past_years} ปี<br>
                    - หักอายุออกรวม = 2 × {past_years} = <b>{2*past_years} ปี</b><br>
                    <b>ขั้นตอนที่ 2: หายอดรวมในอดีต</b><br>
                    - นำอายุรวมปัจจุบันตั้ง ลบด้วยอายุที่ลดลง: {current_sum} - {2*past_years} = <b>{past_sum} ปี</b><br>
                    <b>ตอบ: {past_sum} ปี</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "ความเร็ววิ่งสวนทาง":
                veh = random.choice(VEHICLES)
                if is_challenge:
                    v1, v2 = random.choice([45, 55, 65]), random.choice([45, 55, 65]); start_diff = random.randint(1, 2); t = random.randint(2, 4)
                    adv_d = v1 * start_diff; meet_d = (v1 + v2) * t; total_d = adv_d + meet_d
                    q = f"{veh}สองคันอยู่ห่างกัน <b>{total_d:,} กิโลเมตร</b> <br>คันแรก (วิ่งด้วยความเร็ว <b>{v1} กม./ชม.</b>) ออกเดินทางไปก่อน <b>{start_diff} ชั่วโมง</b><br>จากนั้นคันที่สอง (วิ่งด้วยความเร็ว <b>{v2} กม./ชม.</b>) จึงเริ่มวิ่งสวนทางเข้าหาคันแรก<br>หลังจากคันที่สองเริ่มออกตัว ต้องใช้เวลากี่ชั่วโมง ทั้งสองคันจึงจะวิ่งมาเจอกัน?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (หักระยะทางล่วงหน้า):</b><br>
                    <b>ขั้นตอนที่ 1: หาระยะทางที่คันแรกแอบวิ่งไปก่อน</b><br>
                    - สูตร ระยะทาง = ความเร็ว × เวลา ➔ {v1} × {start_diff} = <b>{adv_d} กม.</b><br>
                    <b>ขั้นตอนที่ 2: หาระยะทางที่เหลืออยู่ตอนคันที่สองเพิ่งเริ่มออกตัว</b><br>
                    - นำระยะทางทั้งหมด - ระยะทางล่วงหน้า: {total_d} - {adv_d} = <b>{meet_d} กม.</b><br>
                    <b>ขั้นตอนที่ 3: คำนวณเวลาวิ่งเข้าหากัน</b><br>
                    - เมื่อวิ่งเข้าหากัน ความเร็วจะเสริมกัน (ความเร็วรวม) = {v1} + {v2} = <b>{v1+v2} กม./ชม.</b><br>
                    - สูตร เวลา = ระยะทาง ÷ ความเร็วรวม ➔ {meet_d} ÷ {v1+v2} = <b>{t} ชั่วโมง</b><br>
                    <b>ตอบ: {t} ชั่วโมง</b></span>"""
                else:
                    v1, v2 = random.choice([20, 30, 40]), random.choice([20, 30, 40]); t = random.randint(2, 4); d = (v1 + v2) * t
                    q = f"{veh}สองคันอยู่ห่างกัน <b>{d:,} กิโลเมตร</b> กำลังวิ่งสวนทางเข้าหากัน <br>ถ้าคันแรกวิ่งเร็ว <b>{v1} กม./ชม.</b> คันที่สองวิ่งเร็ว <b>{v2} กม./ชม.</b> <br>ต้องใช้เวลาอีกกี่ชั่วโมง ทั้งสองจึงจะวิ่งมาเจอกันพอดี?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: หาความเร็วรวม</b><br>
                    - เมื่อวิ่งสวนทางเข้าหากัน ความเร็วจะถูกนำมาบวกกัน: {v1} + {v2} = <b>{v1 + v2} กม./ชม.</b><br>
                    <b>ขั้นตอนที่ 2: หาเวลา</b><br>
                    - สูตร เวลา = ระยะทาง ÷ ความเร็ว ➔ {d:,} ÷ {v1 + v2} = <b>{t} ชั่วโมง</b><br>
                    <b>ตอบ: {t} ชั่วโมง</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "งานและเวลา (Work)":
                action = random.choice(WORK_ACTIONS)
                if is_challenge:
                    n1, n2, n3 = random.sample(NAMES, 3); pairs = [(10, 12, 15, 4), (12, 15, 20, 5), (6, 10, 15, 3), (12, 24, 8, 4)]
                    w1, w2, w3, ans = random.choice(pairs)
                    f1 = get_vertical_fraction(1, w1); f2 = get_vertical_fraction(1, w2); f3 = get_vertical_fraction(1, w3)
                    lcm_val = lcm_multiple(w1, w2, w3)
                    sum_num = (lcm_val//w1) + (lcm_val//w2) + (lcm_val//w3)
                    q = f"ในการ<b>{action}</b> หากให้ <b>{n1}</b> ทำคนเดียวจะเสร็จใน {w1} วัน, <b>{n2}</b> ทำคนเดียวเสร็จใน {w2} วัน, และ <b>{n3}</b> ทำคนเดียวเสร็จใน {w3} วัน<br>จงหาว่าถ้าทั้งสามคน 'ช่วยกันทำพร้อมกัน' งานนี้จะเสร็จภายในเวลากี่วัน?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (สมการอัตราการทำงานรวม):</b><br>
                    เปลี่ยนจำนวนวันให้เป็น "งานที่ทำได้ใน 1 วัน" (เศษส่วน)<br>
                    <b>ขั้นตอนที่ 1: หาผลงานใน 1 วันของแต่ละคน</b><br>
                    - {n1} = {f1}, {n2} = {f2}, {n3} = {f3} ของงานทั้งหมด<br>
                    <b>ขั้นตอนที่ 2: นำผลงานใน 1 วันมาบวกกัน (โดยการทำตัวส่วนให้เท่ากัน)</b><br>
                    - {f1} + {f2} + {f3} (หา ค.ร.น. ของตัวส่วน {w1}, {w2}, {w3} ได้เท่ากับ {lcm_val})<br>
                    - แปลงเศษส่วน: {get_vertical_fraction(lcm_val//w1, lcm_val, is_bold=False)} + {get_vertical_fraction(lcm_val//w2, lcm_val, is_bold=False)} + {get_vertical_fraction(lcm_val//w3, lcm_val, is_bold=False)} = <b>{get_vertical_fraction(sum_num, lcm_val)}</b><br>
                    - ทอนเป็นเศษส่วนอย่างต่ำ จะได้ผลลัพธ์คือ <b>{get_vertical_fraction(1, ans)}</b> ของงานทั้งหมด<br>
                    <b>ขั้นตอนที่ 3: พลิกกลับเศษเป็นส่วนเพื่อหาจำนวนวัน</b><br>
                    - แสดงว่า 1 วัน 3 คนช่วยกันทำได้ {get_vertical_fraction(1, ans, is_bold=False)} งาน ดังนั้นต้องใช้เวลา <b>{ans} วัน</b> งานจึงจะเสร็จ 100%<br>
                    <b>ตอบ: {ans} วัน</b></span>"""
                else:
                    pairs = [(3,6,2), (4,12,3), (6,12,4), (10,15,6)]; w1, w2, ans = random.choice(pairs); n1, n2 = random.sample(NAMES, 2)
                    q = f"ในการ<b>{action}</b> หากให้ <b>{n1}</b> ทำคนเดียวจะเสร็จใน {w1} วัน แต่ถ้าให้ <b>{n2}</b> ทำคนเดียวจะเสร็จใน {w2} วัน <br>จงหาว่าถ้าช่วยกันทำพร้อมกัน จะเสร็จภายในเวลากี่วัน?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: ใช้สูตรลัด 2 คนช่วยกันทำงาน</b><br>
                    - สูตร: (เวลาคนแรก × เวลาคนที่สอง) ÷ (เวลาคนแรก + เวลาคนที่สอง)<br>
                    <b>ขั้นตอนที่ 2: แทนค่าตัวเลขลงในสูตร</b><br>
                    - ด้านบน (คูณ): {w1} × {w2} = {w1*w2}<br>
                    - ด้านล่าง (บวก): {w1} + {w2} = {w1+w2}<br>
                    - นำมาหารกัน: {w1*w2} ÷ {w1+w2} = <b>{ans} วัน</b><br>
                    <b>ตอบ: {ans} วัน</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "ระฆังและไฟกะพริบ (ค.ร.น.)":
                item_word = random.choice(["สัญญาณไฟ", "นาฬิกาปลุก", "ระฆัง"])
                if is_challenge:
                    l1, l2, l3, l4 = random.sample([10, 15, 20, 30, 45, 60], 4)
                    lcm = lcm_multiple(l1, l2, l3, l4)
                    ans_min = lcm // 60; ans_sec = lcm % 60
                    text_ans = f"{ans_min} นาที" if ans_sec == 0 else f"{ans_min} นาที {ans_sec} วินาที"
                    q = f"<b>{item_word} 4 ชิ้น</b> ทำงานด้วยจังหวะที่ต่างกัน ดังนี้:<br>ชิ้นที่ 1 ดังทุกๆ {l1} วินาที, ชิ้นที่ 2 ดังทุกๆ {l2} วินาที, ชิ้นที่ 3 ดังทุกๆ {l3} วินาที, และชิ้นที่ 4 ดังทุกๆ {l4} วินาที <br>ถ้าเพิ่งดังพร้อมกันไป อีกกี่นาทีข้างหน้าจึงจะดังพร้อมกันอีกครั้ง?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (หา ค.ร.น. ขั้นสูง):</b><br>
                    โจทย์ที่มีคำว่า "เกิดขึ้นพร้อมกันอีกครั้ง" ให้ใช้การหา ค.ร.น. (คูณร่วมน้อย)<br>
                    <b>ขั้นตอนที่ 1: ตั้งหารสั้นเพื่อหา ค.ร.น.</b><br>
                    - นำตัวเลข {l1}, {l2}, {l3}, {l4} มาหา ค.ร.น. จะได้รอบเวลาที่ลงตัวพร้อมกันคือ <b>{lcm} วินาที</b><br>
                    <b>ขั้นตอนที่ 2: แปลงหน่วยวินาทีเป็นนาทีให้เรียบร้อย</b><br>
                    - 1 นาที มี 60 วินาที ให้นำ {lcm} ÷ 60<br>
                    - จะได้ผลลัพธ์เท่ากับ <b>{text_ans}</b> พอดี<br>
                    <b>ตอบ: {text_ans}</b></span>"""
                else:
                    l1, l2, l3 = random.sample([10, 12, 15, 20, 30], 3); lcm = lcm_multiple(l1, l2, l3)
                    q = f"{item_word} 3 ชิ้น ทำงานด้วยจังหวะต่างกัน ชิ้นแรกดังทุกๆ {l1} วินาที, ชิ้นที่สอง {l2} วินาที และชิ้นที่สาม {l3} วินาที <br>ถ้าเพิ่งดังพร้อมกันไป อีกกี่วินาทีข้างหน้าจึงจะดังพร้อมกันอีกครั้ง?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: วิเคราะห์โจทย์</b><br>
                    - โจทย์ประเภท 'เกิดขึ้นพร้อมกันอีกครั้ง' ให้หา ค.ร.น. (ตัวคูณร่วมน้อย)<br>
                    <b>ขั้นตอนที่ 2: ตั้งหารสั้น</b><br>
                    - นำรอบเวลาทั้งหมด ({l1}, {l2}, {l3}) มาหา ค.ร.น. จะได้ผลลัพธ์เท่ากับ <b>{lcm}</b><br>
                    <b>ตอบ: อีก {lcm} วินาที</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "นาฬิกาเดินเพี้ยน":
                if is_challenge:
                    days_map = {"พฤหัสบดี": 3, "ศุกร์": 4, "เสาร์": 5}; end_day = random.choice(list(days_map.keys())); days = days_map[end_day]
                    gain_m = random.randint(3, 12); total_gain = days * gain_m
                    carry_h = total_gain // 60; final_m = total_gain % 60; final_h = 8 + carry_h
                    q = f"นาฬิกาเรือนหนึ่งทำงานผิดปกติ โดยจะเดิน <b>'เร็วเกินไป' วันละ {gain_m} นาที</b><br>ถ้า<b>{name}</b>ตั้งเวลานาฬิกาเรือนนี้ให้ตรงเป๊ะในตอน <b>08:00 น. ของวันจันทร์</b><br>จงหาว่าเมื่อเวลาจริงดำเนินไปถึง <b>08:00 น. ของวัน{end_day}</b> นาฬิกาเรือนนี้จะชี้บอกเวลาใด?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step (คำนวณความคลาดเคลื่อนสะสม):</b><br>
                    <b>ขั้นตอนที่ 1: หาจำนวนวันที่ผ่านไปทั้งหมด</b><br>
                    - จาก 08:00 น. วันจันทร์ ถึง 08:00 น. วัน{end_day} นับเวลาที่ผ่านไปได้ <b>{days} วันพอดีเป๊ะ</b><br>
                    <b>ขั้นตอนที่ 2: หาเวลาที่นาฬิกาเดินเพี้ยนไปทั้งหมดสะสม</b><br>
                    - เดินเร็วขึ้นวันละ {gain_m} นาที × {days} วัน = <b>เดินเร็วนำหน้าเวลาจริงไป {total_gain} นาที</b><br>
                    <b>ขั้นตอนที่ 3: คำนวณเวลาที่จะแสดงบนหน้าปัด</b><br>
                    - แปลงหน่วยนาทีที่เกินมาให้เป็นชั่วโมง: นำ {total_gain} นาที ÷ 60 จะได้ <b>{carry_h} ชั่วโมง กับอีก {final_m} นาที</b><br>
                    - นำไปบวกเพิ่มจากเวลาจริง: 08:00 น. + {carry_h} ชั่วโมง {final_m} นาที = <b>{final_h:02d}:{final_m:02d} น.</b><br>
                    <b>ตอบ: เวลา {final_h:02d}:{final_m:02d} น.</b></span>"""
                else:
                    fast_min = random.randint(3, 8); start_h = 8; passed_hours = random.randint(5, 12); end_h = start_h + passed_hours; total_fast = fast_min * passed_hours
                    q = f"นาฬิกาเรือนหนึ่งเดินเร็วไป <b>{fast_min} นาที ในทุกๆ 1 ชั่วโมง</b> <br>ตั้งเวลาตรงตอน <b>0{start_h}:00 น.</b> เมื่อเวลาจริงผ่านไปถึง <b>{end_h}:00 น.</b> นาฬิกาจะแสดงเวลาใด?"
                    sol = f"""<span style='color:#2c3e50;'><b>วิธีคิดวิเคราะห์แบบ Step-by-Step:</b><br>
                    <b>ขั้นตอนที่ 1: หาจำนวนชั่วโมงที่ผ่านไป</b><br>
                    - นำเวลาสิ้นสุด ลบ เวลาเริ่มต้น: {end_h} - {start_h} = <b>{passed_hours} ชั่วโมง</b><br>
                    <b>ขั้นตอนที่ 2: หาเวลาที่นาฬิกาเดินเร็วเกินไปทั้งหมด</b><br>
                    - เดินเร็วชั่วโมงละ {fast_min} นาที × {passed_hours} ชั่วโมง = <b>{total_fast} นาที</b><br>
                    <b>ขั้นตอนที่ 3: รวมเวลาแสดงผล</b><br>
                    - นำเวลาที่เดินเกิน ไปบวกเพิ่มกับเวลาจริง จะได้ <b>{end_h}:{total_fast:02d} น.</b><br>
                    <b>ตอบ: {end_h}:{total_fast:02d} น.</b></span>"""

            # ---------------------------------------------------------
            else:
                q = f"โจทย์หัวข้อ <b>{actual_sub_t}</b> เกิดข้อผิดพลาดในการโหลด"
                sol = "N/A"

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
    html = f"""<!DOCTYPE html><html lang="th"><head><meta charset="utf-8"><style>@page {{ size: A4; margin: 15mm; }} body {{ font-family: 'Sarabun', sans-serif; padding: 20px; color: #333; line-height: 1.6; }} .q-box {{ margin-bottom: {q_margin}; padding: 10px; page-break-inside: avoid; font-size: 20px; }} .sol-text {{ background: #f9f9f9; border-left: 5px solid #8e44ad; padding: 15px; margin-top: 10px; font-size: 18px; }} .workspace {{ height: {ws_height}; border: 1px dashed #ccc; margin: 10px 0; background: #fcfcfc; }}</style></head><body><div style="text-align:center; margin-bottom:20px;"><h2>{title}</h2><p>{sub_t} ({level})</p></div>"""
    for i, item in enumerate(questions, 1):
        html += f'<div class="q-box"><b>ข้อที่ {i}.</b> {item["question"]}'
        if is_key: html += f'<div class="sol-text">{item["solution"]}</div>'
        else: html += f'<div class="workspace"></div><div style="font-weight:bold; font-size: 20px;">ตอบ: ............................</div>'
        html += '</div>'
    return html + "</body></html>"

def generate_cover_html(level, sub_t, num_q, brand_name, is_challenge):
    theme_color = "#8e44ad" if not is_challenge else "#c0392b"
    badge_text = "🔥 ULTIMATE CHALLENGE MODE" if is_challenge else "(TMC Edition)"
    
    return f"""<!DOCTYPE html><html lang="th"><head><meta charset="utf-8">
    <style>
        .cover-inner {{ width: 100%; height: 100%; padding: 40px; box-sizing: border-box; text-align: center; position: relative; border: 15px solid {theme_color}; background: white; }}
        .title-box {{ margin-top: 80px; }}
        .title {{ font-size: 65px; color: #2c3e50; font-weight: bold; margin: 0; line-height: 1.2; }}
        .grade-badge {{ font-size: 40px; background-color: #f1c40f; color: #333; padding: 15px 50px; border-radius: 50px; display: inline-block; font-weight: bold; margin-top: 30px; }}
        .topic {{ font-size: 42px; color: #34495e; margin-top: 70px; font-weight: bold; }}
        .sub-topic {{ font-size: 32px; color: {theme_color}; margin-top: 10px; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);}}
        .icons {{ font-size: 110px; margin: 60px 0; }}
        .details-badge {{ background-color: {theme_color}; color: white; display: inline-block; padding: 15px 40px; border-radius: 15px; font-size: 32px; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}}
        .footer {{ position: absolute; bottom: 40px; left: 0; width: 100%; text-align: center; font-size: 22px; color: #7f8c8d; }}
    </style></head><body>
    <div class="cover-inner">
        <div class="title-box">
            <h1 class="title">ข้อสอบวิเคราะห์คณิตศาสตร์</h1>
            <div class="grade-badge">{level}</div>
        </div>
        <div class="topic">เรื่อง: {sub_t}</div>
        <div class="sub-topic">{badge_text}</div>
        <div class="icons">{'⚔️ 🧠 🏆 🚀' if is_challenge else '🏆 🥇 🧠 💡'}</div>
        <div class="details-badge">รวมทั้งหมด {num_q} ข้อ (พร้อมเฉลยละเอียด)</div>
        <div class="footer"><b>ออกแบบและจัดทำโดย:</b> {brand_name}</div>
    </div>
    </body></html>"""

# --- Sidebar ---
st.sidebar.title("⚙️ ตั้งค่าระบบ")
selected_level = st.sidebar.selectbox("🏆 ระดับชั้น:", list(comp_db.keys()))
selected_sub = st.sidebar.selectbox("📝 หัวข้อ:", comp_db[selected_level] + ["🌟 สุ่มรวมทุกแนวแข่งขัน"])
num_input = st.sidebar.number_input("🔢 จำนวนข้อ:", 1, 100, 10)
is_challenge = st.sidebar.toggle("🔥 โหมด Challenge (ระดับโอลิมปิก)", False)
spacing_level = st.sidebar.select_slider("↕️ ความสูงของพื้นที่ทดเลข:", options=["แคบ", "ปานกลาง", "กว้าง", "กว้างพิเศษ"], value="กว้าง")
if spacing_level == "แคบ": q_margin, ws_height = "15px", "100px"
elif spacing_level == "ปานกลาง": q_margin, ws_height = "20px", "180px"
elif spacing_level == "กว้าง": q_margin, ws_height = "30px", "280px"
else: q_margin, ws_height = "40px", "400px"
brand_name = st.sidebar.text_input("🏷️ แบรนด์:", "บ้านทีเด็ด")
include_cover = st.sidebar.checkbox("🎨 สร้างหน้าปก", value=True)

if st.sidebar.button("🚀 สร้างข้อสอบทันที", type="primary", use_container_width=True):
    with st.spinner("ประมวลผลตรรกะและจัดทำไฟล์..."):
        qs = generate_questions_logic(selected_level, selected_sub, num_input, is_challenge)
        html_w = create_page(selected_level, selected_sub, qs, False, q_margin, ws_height, brand_name, is_challenge)
        html_k = create_page(selected_level, selected_sub, qs, True, q_margin, ws_height, brand_name, is_challenge)
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
    st.success(f"✅ โค้ดสมบูรณ์เต็มรูปแบบ! อัปเกรดความละเอียดแบบ Step-by-step และแก้โครงสร้างเศษส่วนแนวตั้งครบ 100% แล้วครับ")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📄 โหลดเฉพาะโจทย์", data=st.session_state['worksheet_html'], file_name=f"{st.session_state['filename_base']}_Worksheet.html", mime="text/html", use_container_width=True)
        st.download_button("🔑 โหลดเฉพาะเฉลย", data=st.session_state['answerkey_html'], file_name=f"{st.session_state['filename_base']}_AnswerKey.html", mime="text/html", use_container_width=True)
    with c2:
        st.download_button("📚 โหลดรวมเล่ม E-Book", data=st.session_state['ebook_html'], file_name=f"{st.session_state['filename_base']}_Full_EBook.html", mime="text/html", use_container_width=True)
        st.download_button("🗂️ โหลดแพ็กเกจ (.zip)", data=st.session_state['zip_data'], file_name=f"{st.session_state['filename_base']}.zip", mime="application/zip", use_container_width=True)
    st.markdown("---")
    components.html(st.session_state['ebook_html'], height=800, scrolling=True)
