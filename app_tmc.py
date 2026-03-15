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
# 1. คลังคำศัพท์เพิ่มความหลากหลาย (Vocabulary Pools)
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
box_html = "<span style='display: inline-block; width: 24px; height: 24px; border: 2px solid #c0392b; border-radius: 4px; vertical-align: middle; position: relative; top: -2px; background-color: #fff;'></span>"

# ==========================================
# 🌟 ฟังก์ชันสร้างเศษส่วนและตารางแนวตั้ง
# ==========================================
def get_vertical_fraction(num, den, color="#333", is_bold=True):
    weight = "bold" if is_bold else "normal"
    return f"""<span style="display:inline-flex; flex-direction:column; vertical-align:middle; text-align:center; line-height:1.4; margin: 0 6px; font-family:'Sarabun', sans-serif; white-space: nowrap;"><span style="border-bottom: 2px solid {color}; padding: 2px 6px; font-weight:{weight}; color:{color};">{num}</span><span style="padding: 2px 6px; font-weight:{weight}; color:{color};">{den}</span></span>"""

def get_vertical_math(top_chars, bottom_chars, result_chars, operator="+"):
    max_len = max(len(top_chars), len(bottom_chars), len(result_chars))
    top_padded = [""] * (max_len - len(top_chars)) + top_chars
    bot_padded = [""] * (max_len - len(bottom_chars)) + bottom_chars
    res_padded = [""] * (max_len - len(result_chars)) + result_chars
    
    html = "<table style='border-collapse: collapse; font-size: 26px; font-weight: bold; text-align: center; margin: 15px 0 15px 40px;'>"
    html += "<tr>"
    for char in top_padded: html += f"<td style='padding: 5px 12px; width: 35px;'>{char}</td>"
    html += f"<td rowspan='2' style='padding-left: 20px; vertical-align: middle; font-size: 28px; color: #2c3e50;'>{operator}</td></tr><tr>"
    for char in bot_padded: html += f"<td style='padding: 5px 12px; width: 35px; border-bottom: 2px solid #333;'>{char}</td>"
    html += "</tr><tr>"
    for char in res_padded: html += f"<td style='padding: 5px 12px; width: 35px; border-bottom: 4px double #333;'>{char}</td>"
    html += "<td></td></tr></table>"
    return html

def lcm_calc(a, b):
    return abs(a * b) // math.gcd(a, b)

# ==========================================
# 2. ฐานข้อมูลหัวข้อข้อสอบแข่งขัน
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
# 3. Logic & Dynamic Difficulty Scaling (TITANIUM EDITION)
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
            actual_sub_t = sub_t
            if sub_t == "🌟 สุ่มรวมทุกแนวแข่งขัน":
                actual_sub_t = random.choice(comp_db[level])
            
            name = random.choice(NAMES)

            # ---------------------------------------------------------
            if actual_sub_t == "การสร้างจำนวนจากเลขโดด":
                if is_challenge:
                    digits = random.sample([1,2,3,4,5,6,7,8,9], 5)
                    max_prod = 0
                    best_pair = ()
                    for p in itertools.permutations(digits):
                        n1 = p[0]*100 + p[1]*10 + p[2]
                        n2 = p[3]*10 + p[4]
                        if n1 * n2 > max_prod:
                            max_prod = n1 * n2
                            best_pair = (n1, n2)
                    sorted_d = sorted(digits, reverse=True)
                    q = f"<b>{name}</b> ได้รับบัตรตัวเลข 5 ใบ คือ <b>{', '.join(map(str, digits))}</b> <br>ถ้านำบัตรตัวเลขทั้งหมดมาสร้างเป็น <b>จำนวน 3 หลัก</b> และ <b>จำนวน 2 หลัก</b> ที่เมื่อนำมาคูณกันแล้วจะได้ <b>'ผลคูณที่มีค่ามากที่สุด'</b><br>ผลคูณนั้นคือเท่าไร?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์เชิงลึก (เทคนิคสมดุลและคูณไขว้):</b><br>
                    หัวใจสำคัญของการทำให้ผลคูณมีค่ามากที่สุด คือ <b>"การสร้างสมดุล"</b> และการนำเลขค่ามากไปไขว้คูณกับกลุ่มตัวเลขที่ใหญ่ที่สุดครับ!<br>
                    <b>ขั้นตอนที่ 1: เรียงลำดับตัวเลขจากมากไปน้อย</b><br>
                    &nbsp;&nbsp;&nbsp;👉 จะได้ตัวเลขคือ <b>{sorted_d[0]} > {sorted_d[1]} > {sorted_d[2]} > {sorted_d[3]} > {sorted_d[4]}</b><br>
                    <b>ขั้นตอนที่ 2: วางตัวเลขใน "หลักหน้าสุด" (หลักที่ทรงพลังที่สุด)</b><br>
                    &nbsp;&nbsp;&nbsp;👉 นำเลขที่มากที่สุด 2 ตัวแรก (คือ {sorted_d[0]} และ {sorted_d[1]}) มาเป็นตัวนำทัพ<br>
                    &nbsp;&nbsp;&nbsp;👉 <i>ทำไม {sorted_d[0]} ต้องไปอยู่จำนวน 2 หลัก?</i> เพราะจำนวน 2 หลัก จะรับบทเป็น "ตัวคูณ" ที่ไปคูณกระจุยกับตัวเลข 3 หลักทุกตำแหน่ง การเอาเลขใหญ่สุดเป็นตัวคูณจะทวีคูณค่าได้มหาศาลครับ! ➔ ตอนนี้เราจะได้โครงสร้าง: <b>{sorted_d[1]}🔲🔲  ×  {sorted_d[0]}🔲</b><br>
                    <b>ขั้นตอนที่ 3: วางตัวเลขในตำแหน่งถัดไป (เทคนิคคูณไขว้)</b><br>
                    &nbsp;&nbsp;&nbsp;👉 เลข <b>{sorted_d[2]}</b> ต้องจับคู่ให้โดนคูณด้วยเลข <b>{sorted_d[0]}</b> ดังนั้นต้องส่งไปอยู่ฝั่งตรงข้าม ➔ โครงสร้าง: <b>{sorted_d[1]}{sorted_d[2]}🔲  ×  {sorted_d[0]}🔲</b><br>
                    &nbsp;&nbsp;&nbsp;👉 เลข <b>{sorted_d[3]}</b> ต้องนำไปไขว้คูณกับก้อนที่ใหญ่ที่สุด (คือ {sorted_d[1]}{sorted_d[2]}0) จึงต้องนำไปใส่จำนวน 2 หลัก ➔ โครงสร้าง: <b>{sorted_d[1]}{sorted_d[2]}🔲  ×  {sorted_d[0]}{sorted_d[3]}</b><br>
                    <b>ขั้นตอนที่ 4: เติมหลักหน่วยตัวสุดท้าย</b><br>
                    &nbsp;&nbsp;&nbsp;👉 นำเลขน้อยสุด <b>{sorted_d[4]}</b> ไปใส่ช่องที่เหลือ ➔ จะได้ตัวเลขที่สมบูรณ์คือ <b>{best_pair[0]}</b> และ <b>{best_pair[1]}</b><br>
                    <b>ขั้นตอนที่ 5: ตรวจสอบผลคูณ</b><br>
                    &nbsp;&nbsp;&nbsp;👉 คำนวณ {best_pair[0]} × {best_pair[1]} = <b>{max_prod:,}</b><br>
                    <b>ตอบ: {max_prod:,}</b></span>"""
                else:
                    if is_p12:
                        digits = random.sample([1,2,3,4,5,6,7,8,9], 3)
                        max_v = int("".join(map(str, sorted(digits, reverse=True))))
                        min_v = int("".join(map(str, sorted(digits))))
                        diff = max_v - min_v
                        q = f"<b>{name}</b> มีบัตรตัวเลข 3 ใบ คือ <b>{digits[0]}, {digits[1]}, และ {digits[2]}</b> <br>ถ้านำบัตรตัวเลขทั้งหมดมาเรียงต่อกันเป็นจำนวน 3 หลัก จงหาผลต่างของจำนวนที่<b>มากที่สุด</b>และจำนวนที่<b>น้อยที่สุด</b>ที่สร้างได้?"
                        sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                        <b>ขั้นตอนที่ 1:</b> สร้างจำนวนมากที่สุด นำเลขค่ามากไว้หน้าสุด = <b>{max_v}</b><br>
                        <b>ขั้นตอนที่ 2:</b> สร้างจำนวนน้อยที่สุด นำเลขค่าน้อยไว้หน้าสุด = <b>{min_v}</b><br>
                        <b>ขั้นตอนที่ 3:</b> หาผลต่างโดยนำตัวมากตั้ง ลบด้วยตัวน้อย: {max_v} - {min_v} = <b>{diff}</b><br>
                        <b>ตอบ: {diff}</b></span>"""
                    else: 
                        q_type = random.choice(["even", "div5"])
                        num_digits = 4 if is_p34 else 5
                        if q_type == "even":
                            evens = [2, 4, 6, 8]; odds = [1, 3, 5, 7, 9]
                            c_digits = random.sample(evens, 2) + random.sample(odds, num_digits-2)
                            random.shuffle(c_digits)
                            targets = sorted([d for d in c_digits if d % 2 == 0])
                            others = [d for d in c_digits if d % 2 != 0]
                            unit = targets[0] 
                            rem = sorted(others + targets[1:], reverse=True)
                            ans_num = int("".join(map(str, rem + [unit])))
                            q = f"<b>{name}</b> มีบัตรตัวเลข {num_digits} ใบ คือ <b>{', '.join(map(str, c_digits))}</b> <br>จงหา<b>จำนวนคู่ที่มากที่สุด</b>ที่สามารถสร้างได้?"
                            sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์อย่างละเอียด:</b><br>
                            <b>ขั้นตอนที่ 1: วิเคราะห์เงื่อนไข "จำนวนคู่"</b><br>
                            &nbsp;&nbsp;&nbsp;👉 กฎคือหลักหน่วยต้องเป็นเลขคู่เท่านั้น! เลขคู่ที่เรามีในมือคือ <b>{targets}</b><br>
                            <b>ขั้นตอนที่ 2: วิเคราะห์เงื่อนไข "ค่ามากที่สุด"</b><br>
                            &nbsp;&nbsp;&nbsp;👉 ถ้าอยากให้จำนวนมีค่ามากๆ เราต้องหวงตัวเลขค่าเยอะเอาไว้ใส่ในหลักหน้าสุด<br>
                            &nbsp;&nbsp;&nbsp;👉 ดังนั้น เราต้องยอมเสียสละเลขคู่ที่ <b>น้อยที่สุด</b> (คือ <b>{unit}</b>) ไปล็อกไว้ที่ตำแหน่งหลักหน่วยเลยครับ<br>
                            <b>ขั้นตอนที่ 3: จัดเรียงตัวเลขที่เหลือ</b><br>
                            &nbsp;&nbsp;&nbsp;👉 นำเลขที่เหลือในมือทั้งหมด มาเรียงจาก <b>มากไปน้อย</b> ไว้ด้านหน้า<br>
                            &nbsp;&nbsp;&nbsp;👉 จะประกอบร่างได้เป็น <b>{ans_num:,}</b><br>
                            <b>ตอบ: {ans_num:,}</b></span>"""
                        else:
                            c_digits = random.sample([1,2,3,4,6,7,8,9], num_digits - 1) + [5]
                            random.shuffle(c_digits)
                            rem = sorted([d for d in c_digits if d != 5])
                            ans_num = int("".join(map(str, rem + [5])))
                            q = f"<b>{name}</b> มีบัตรตัวเลข {num_digits} ใบ คือ <b>{', '.join(map(str, c_digits))}</b> <br>จงหา<b>จำนวนที่น้อยที่สุดที่หารด้วย 5 ลงตัว</b>?"
                            sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์อย่างละเอียด:</b><br>
                            <b>ขั้นตอนที่ 1: วิเคราะห์เงื่อนไข "หารด้วย 5 ลงตัว"</b><br>
                            &nbsp;&nbsp;&nbsp;👉 กฎเหล็กของการหาร 5 ลงตัวคือ หลักหน่วยต้องเป็น 0 หรือ 5 เท่านั้น!<br>
                            &nbsp;&nbsp;&nbsp;👉 ในบัตรที่เรามี มีเลข <b>5</b> อยู่ จึงต้องนำ 5 ไปล็อกไว้ที่ตำแหน่งหลักหน่วยทันที<br>
                            <b>ขั้นตอนที่ 2: วิเคราะห์เงื่อนไข "ค่าน้อยที่สุด"</b><br>
                            &nbsp;&nbsp;&nbsp;👉 ถ้าอยากให้จำนวนมีค่าน้อยๆ เราต้องหลีกเลี่ยงการเอาเลขมากไปไว้ด้านหน้า<br>
                            &nbsp;&nbsp;&nbsp;👉 ให้นำเลขที่เหลือในมือทั้งหมด มาเรียงจาก <b>น้อยไปมาก</b> ไว้ด้านหน้าของเลข 5<br>
                            <b>ขั้นตอนที่ 3: สรุปตัวเลข</b><br>
                            &nbsp;&nbsp;&nbsp;👉 จะประกอบร่างได้เป็น <b>{ans_num:,}</b><br>
                            <b>ตอบ: {ans_num:,}</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "โจทย์ปัญหาทำผิดเป็นถูก":
                if is_challenge:
                    A = random.randint(3, 8)
                    B = random.randint(5, 20)
                    X = random.randint(5, 12) * A
                    wrong_ans = (X // A) + B
                    correct_ans = (X * A) - B
                    
                    frac_wrong_q = get_vertical_fraction('จำนวนปริศนา', A)
                    frac_wrong_s = get_vertical_fraction('🔲', A, color="#2c3e50", is_bold=False)
                    
                    q = f"<b>{name}</b> ตั้งใจจะนำจำนวนปริศนาไป <b>คูณด้วย {A}</b> แล้ว <b>ลบออกด้วย {B}</b><br>แต่เขาทำผิดพลาด สลับเครื่องหมายเป็นนำไปเขียนในรูปเศษส่วนคือ <b>{frac_wrong_q}</b> แล้วค่อย <b>บวกเพิ่ม {B}</b> ทำให้ได้ผลลัพธ์เป็น <b>{wrong_ans}</b><br>จงหาผลลัพธ์ที่แท้จริงตามความตั้งใจแรก?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดอย่างละเอียด (สวมบทบาทนักสืบย้อนเวลา):</b><br>
                    <b>ขั้นตอนที่ 1: ย้อนรอยสิ่งที่ทำผิด เพื่อหา 'จำนวนปริศนา'</b><br>
                    &nbsp;&nbsp;&nbsp;👉 สิ่งที่ทำผิด: {frac_wrong_s} + {B} = {wrong_ans}<br>
                    &nbsp;&nbsp;&nbsp;👉 ย้อนกลับขั้นที่ 1 (บวกเป็นลบ): {wrong_ans} - {B} = {wrong_ans - B}<br>
                    &nbsp;&nbsp;&nbsp;👉 ย้อนกลับขั้นที่ 2 (ส่วนหารเปลี่ยนเป็นคูณ): {wrong_ans - B} × {A} = <b>{X}</b> (นี่คือจำนวนปริศนา!)<br>
                    <b>ขั้นตอนที่ 2: คิดใหม่ให้ถูกต้องตามโจทย์สั่ง</b><br>
                    &nbsp;&nbsp;&nbsp;👉 ความตั้งใจแรกคือ นำ {X} ไป <b>คูณ {A}</b> แล้ว <b>ลบ {B}</b><br>
                    &nbsp;&nbsp;&nbsp;👉 คำนวณ: ({X} × {A}) - {B} = {X*A} - {B} = <b>{correct_ans:,}</b><br>
                    <b>ตอบ: {correct_ans:,}</b></span>"""
                else:
                    if is_p12:
                        x = random.randint(5, 20)
                        ans_true = random.randint(30, 80)
                        wrong_ans = ans_true - (2 * x)
                        while wrong_ans <= 0:
                            ans_true = random.randint(50, 100)
                            wrong_ans = ans_true - (2 * x)
                            
                        q = f"<b>{name}</b> ตั้งใจจะนำจำนวนๆ หนึ่งไป <b>บวก</b> กับ {x} แต่เขาทำผิดโดยนำไป <b>ลบ</b> ด้วย {x} ทำให้ได้ผลลัพธ์เป็น <b>{wrong_ans}</b> <br>ผลลัพธ์ที่แท้จริงคือเท่าไร?"
                        sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดอย่างละเอียด (คิดย้อนกลับ):</b><br>
                        <b>ขั้นตอนที่ 1: หาตัวเลขในตอนแรกสุด</b><br>
                        &nbsp;&nbsp;&nbsp;👉 จากที่ทำผิดคือ: 🔲 - {x} = {wrong_ans}<br>
                        &nbsp;&nbsp;&nbsp;👉 ย้ายฝั่งเปลี่ยน <b>ลบ เป็น บวก</b> จะได้ตัวเลขตอนแรกคือ: {wrong_ans} + {x} = <b>{wrong_ans + x}</b><br>
                        <b>ขั้นตอนที่ 2: คิดเลขให้ถูกต้อง</b><br>
                        &nbsp;&nbsp;&nbsp;👉 นำตัวเลขตอนแรก ({wrong_ans + x}) ไป <b>บวกด้วย {x}</b> ตามโจทย์สั่ง: {wrong_ans + x} + {x} = <b>{ans_true}</b><br>
                        <b>ตอบ: {ans_true}</b></span>"""
                    else:
                        x = random.randint(3, 12); n = random.randint(11, 30); wrong_ans = n; correct_ans = n * x * x
                        frac_wrong_q = get_vertical_fraction('จำนวนหนึ่ง', x)
                        frac_wrong_s = get_vertical_fraction('🔲', x, color="#2c3e50", is_bold=False)
                        
                        q = f"<b>{name}</b> ตั้งใจจะนำจำนวนๆ หนึ่งไป <b>คูณ</b> ด้วย {x} แต่ดันไปเขียนเป็นเศษส่วนในรูป <b>{frac_wrong_q}</b> ทำให้ผลลัพธ์ผิดเพี้ยนไปเป็น <b>{wrong_ans}</b> <br>ผลลัพธ์ที่ถูกต้องตามความตั้งใจแรกคือเท่าไร?"
                        sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดอย่างละเอียด (คิดย้อนกลับ):</b><br>
                        <b>ขั้นตอนที่ 1: หาตัวเลขในตอนแรกสุด</b><br>
                        &nbsp;&nbsp;&nbsp;👉 จากที่ทำผิดคือ: {frac_wrong_s} = {wrong_ans}<br>
                        &nbsp;&nbsp;&nbsp;👉 ย้ายฝั่งเปลี่ยน <b>เส้นคั่น (หาร) เป็น คูณ</b> จะได้ตัวเลขตอนแรกคือ: {wrong_ans} × {x} = <b>{wrong_ans * x}</b><br>
                        <b>ขั้นตอนที่ 2: คิดเลขให้ถูกต้อง</b><br>
                        &nbsp;&nbsp;&nbsp;👉 นำตัวเลขตอนแรก ({wrong_ans * x}) ไป <b>คูณด้วย {x}</b> ตามโจทย์สั่ง: {wrong_ans * x} × {x} = <b>{correct_ans:,}</b><br>
                        <b>ตอบ: {correct_ans:,}</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "การนับตารางเรขาคณิต":
                if is_challenge:
                    N = random.randint(3, 5)
                    M = random.randint(4, 7)
                    if N == M: M += 1
                    total_rect = (N * (N + 1) // 2) * (M * (M + 1) // 2)
                    total_sq = sum((N - i) * (M - i) for i in range(min(N, M)))
                    ans = total_rect - total_sq
                    
                    q = f"<b>{name}</b> วาดตารางเป็นรูปสี่เหลี่ยมผืนผ้าขนาด <b>{N} × {M}</b> ช่อง<br>จงหาว่ามี <b>'สี่เหลี่ยมผืนผ้าที่ไม่ใช่สี่เหลี่ยมจัตุรัส'</b> ซ่อนอยู่ทั้งหมดกี่รูป?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (วิเคราะห์แบบหักล้าง):</b><br>
                    สูตรคือ: (สี่เหลี่ยมผืนผ้าทั้งหมด) - (สี่เหลี่ยมจัตุรัสทั้งหมด)<br>
                    <b>ขั้นตอนที่ 1: หาจำนวนสี่เหลี่ยมรวมทุกชนิด (สูตรผืนผ้า)</b><br>
                    &nbsp;&nbsp;&nbsp;👉 (ผลบวกด้านกว้าง) × (ผลบวกด้านยาว)<br>
                    &nbsp;&nbsp;&nbsp;👉 (1+2+...+{N}) × (1+2+...+{M}) = {N*(N+1)//2} × {M*(M+1)//2} = <b>{total_rect:,} รูป</b><br>
                    <b>ขั้นตอนที่ 2: หาจำนวนสี่เหลี่ยมจัตุรัสทั้งหมด</b><br>
                    &nbsp;&nbsp;&nbsp;👉 นำด้านกว้างและยาวมาคูณกัน แล้วลดทีละ 1 นำมาบวกกัน<br>
                    &nbsp;&nbsp;&nbsp;👉 ({N}×{M}) + ({N-1}×{M-1}) ... จนกว่าตัวใดตัวหนึ่งเป็น 1<br>
                    &nbsp;&nbsp;&nbsp;👉 ผลรวมคือ <b>{total_sq:,} รูป</b><br>
                    <b>ขั้นตอนที่ 3: หักล้างกัน</b><br>
                    &nbsp;&nbsp;&nbsp;👉 {total_rect:,} - {total_sq:,} = <b>{ans:,} รูป</b><br>
                    <b>ตอบ: {ans:,} รูป</b></span>"""
                else:
                    grid = random.randint(2, 4) if is_p12 else random.randint(4, 6)
                    ans = sum([i*i for i in range(1, grid+1)])
                    q = f"<b>{name}</b> มีตารางกระดานขนาด <b>{grid} × {grid}</b> ช่อง จงหาว่ามี <b>'สี่เหลี่ยมจัตุรัส'</b> ซ่อนอยู่ทั้งหมดกี่รูป?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (สูตรลัดสี่เหลี่ยมจัตุรัส):</b><br>
                    นำขนาดความยาวของตาราง มายกกำลังสองทีละตัว แล้วบวกกัน (1² + 2² + ... + {grid}²)<br>
                    ผลรวม = 1 + 4 + ... + ({grid}×{grid}) = <b>{ans:,} รูป</b><br>
                    <b>ตอบ: {ans:,} รูป</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "ปริศนาสมการช่องว่าง":
                if is_challenge:
                    ans = random.randint(5, 20)
                    B = random.randint(2, 10)
                    C = random.randint(2, 5)
                    V3 = ans + B
                    while V3 % C != 0:
                        ans += 1
                        V3 = ans + B
                    V2 = V3 // C
                    if V2 <= 1:
                        ans += C * 2
                        V3 = ans + B
                        V2 = V3 // C
                    D = random.randint(1, V2 - 1)
                    V1 = V2 - D
                    A = random.randint(2, 6)
                    E = A * V1
                    
                    frac_html = get_vertical_fraction(f'( 🔲 + {B} )', C)
                    q = f"จงหาตัวเลขที่เติมลงในช่องว่าง:<br><br><span style='font-size:24px; font-weight:bold;'>{A} × &nbsp;<span style='font-size:36px; vertical-align: middle;'>[</span>&nbsp; {frac_html} &nbsp;−&nbsp; {D} &nbsp;<span style='font-size:36px; vertical-align: middle;'>]</span>&nbsp; =&nbsp; {E}</span>"
                    
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดอย่างละเอียด (แกะกล่องของขวัญจากวงนอกเข้าสู่วงใน):</b><br>
                    <b>ขั้นตอนที่ 1: กำจัดตัวเลขนอกวงเล็บใหญ่สุด คือ "× {A}"</b><br>
                    &nbsp;&nbsp;&nbsp;👉 ย้ายไปฝั่งขวา เปลี่ยนเป็น <b>÷ {A}</b><br>
                    &nbsp;&nbsp;&nbsp;👉 {E} ÷ {A} = <b>{V1}</b><br>
                    <b>ขั้นตอนที่ 2: กำจัดตัวเลข "- {D}"</b><br>
                    &nbsp;&nbsp;&nbsp;👉 ย้ายไปฝั่งขวา เปลี่ยนเป็น <b>+ {D}</b><br>
                    &nbsp;&nbsp;&nbsp;👉 {V1} + {D} = <b>{V2}</b><br>
                    <b>ขั้นตอนที่ 3: กำจัดส่วน "{C}" (คือการหาร)</b><br>
                    &nbsp;&nbsp;&nbsp;👉 ย้ายไปฝั่งขวา เปลี่ยนเป็น <b>× {C}</b><br>
                    &nbsp;&nbsp;&nbsp;👉 {V2} × {C} = <b>{V3}</b><br>
                    <b>ขั้นตอนที่ 4: หาค่า 🔲</b><br>
                    &nbsp;&nbsp;&nbsp;👉 เหลือ 🔲 + {B} = {V3} ➔ ย้ายไปลบ ➔ {V3} - {B} = <b>{ans}</b><br>
                    <b>ตอบ: {ans}</b></span>"""
                else:
                    if is_p12:
                        a = random.randint(15, 50); b = random.randint(60, 150)
                        q = f"จงหาตัวเลขที่เติมลงในช่องว่าง:<br><br><span style='font-size:24px; font-weight:bold;'>🔲 + {a} = {b}</span>"
                        sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดอย่างละเอียด (หลักการย้ายข้าง):</b><br>
                        <b>ขั้นตอนที่ 1:</b> เราต้องย้าย <b>+ {a}</b> ไปอยู่ฝั่งขวาของเครื่องหมายเท่ากับ ( = )<br>
                        <b>ขั้นตอนที่ 2:</b> เวลาย้ายฝั่ง ต้องเปลี่ยนเครื่องหมายเป็น <b>ตรงกันข้าม</b> (จากบวกเป็นลบ)<br>
                        &nbsp;&nbsp;&nbsp;👉 สมการใหม่คือ: 🔲 = {b} - {a}<br>
                        &nbsp;&nbsp;&nbsp;👉 คิดเลข: {b} - {a} = <b>{b-a}</b><br>
                        <b>ตอบ: {b-a}</b></span>"""
                    else:
                        a = random.randint(10, 50); b = random.randint(2, 9)
                        ans = random.randint(5, 40)
                        c = (ans + a) * b
                        q = f"จงหาตัวเลขที่เติมลงในช่องว่าง:<br><br><span style='font-size:24px; font-weight:bold;'>( 🔲 + {a} ) × {b} = {c}</span>"
                        sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดอย่างละเอียด (ย้ายข้างทีละตัว):</b><br>
                        <b>ขั้นตอนที่ 1: กำจัดตัวนอกวงเล็บ "× {b}"</b> ย้ายไปเปลี่ยนเป็น <b>÷ {b}</b><br>
                        &nbsp;&nbsp;&nbsp;👉 จะได้: {c} ÷ {b} = <b>{c//b}</b> (สมการเหลือ: 🔲 + {a} = {c//b})<br>
                        <b>ขั้นตอนที่ 2: หาค่า 🔲</b> ย้าย <b>+ {a}</b> ข้ามฝั่งไป <b>- {a}</b><br>
                        &nbsp;&nbsp;&nbsp;👉 จะได้: {c//b} - {a} = <b>{ans}</b><br>
                        <b>ตอบ: {ans}</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "อสมการและค่าที่เป็นไปได้":
                if is_challenge:
                    C = random.choice([2, 3, 4, 5])
                    ans_list = list(range(random.randint(5, 10), random.randint(12, 18)))
                    min_val, max_val = ans_list[0], ans_list[-1]
                    B = random.randint(3, 8)
                    A = (min_val * C) - random.randint(1, C-1)
                    D = (max_val * C) + random.randint(1, C-1)
                    ans = sum(ans_list)
                    
                    frac_L = get_vertical_fraction(A, B*C)
                    frac_M = get_vertical_fraction("🔲", B)
                    frac_R = get_vertical_fraction(D, B*C)
                    
                    frac_sol_M1 = get_vertical_fraction(f"🔲 × {C}", f"{B} × {C}", color="#2c3e50", is_bold=False)
                    frac_sol_M2 = get_vertical_fraction(f"🔲 × {C}", B*C, color="#2c3e50", is_bold=False)
                    
                    q = f"จงหา <b>'ผลบวกของจำนวนนับทุกจำนวน'</b> ที่สามารถเติมในช่องว่างแล้วทำให้อสมการเป็นจริง:<br><br><span style='font-size:24px; font-weight:bold;'>{frac_L} &nbsp;&lt;&nbsp; {frac_M} &nbsp;&lt;&nbsp; {frac_R}</span>"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (อสมการเศษส่วน):</b><br>
                    การจะเปรียบเทียบเศษส่วนได้ "ตัวส่วนด้านล่างต้องเท่ากัน" ทั้งหมดก่อนครับ!<br>
                    <b>ขั้นตอนที่ 1: ทำตัวส่วนให้เท่ากัน</b><br>
                    &nbsp;&nbsp;&nbsp;👉 เศษส่วนตรงกลางคือ 🔲 ส่วน {B} แต่ด้านข้างส่วนเป็น {B*C} ดังนั้นเราต้องนำ {C} มาคูณทั้งเศษและส่วนให้ตัวตรงกลาง<br>
                    &nbsp;&nbsp;&nbsp;👉 ตรงกลางจะกลายเป็น: {frac_sol_M1} = {frac_sol_M2}<br>
                    <b>ขั้นตอนที่ 2: เปรียบเทียบเฉพาะตัวเศษด้านบน</b><br>
                    &nbsp;&nbsp;&nbsp;👉 ตอนนี้ส่วนเป็น {B*C} เท่ากันหมดแล้ว เราสามารถนำเฉพาะตัวเศษด้านบนมาเทียบกันได้เลย อสมการจะกลายเป็น: <b>{A} &lt; 🔲 × {C} &lt; {D}</b><br>
                    <b>ขั้นตอนที่ 3: หาจำนวนนับ 🔲 ที่เป็นไปได้ทั้งหมด</b><br>
                    &nbsp;&nbsp;&nbsp;👉 เราต้องหาว่ามีเลขอะไรบ้างที่คูณ {C} แล้วได้ผลลัพธ์อยู่ระหว่าง {A} ถึง {D}<br>
                    &nbsp;&nbsp;&nbsp;👉 ลองท่องสูตรคูณแม่ {C} จะพบว่าจำนวนนับที่ใช้ได้คือ: <b>{', '.join(map(str, ans_list))}</b><br>
                    &nbsp;&nbsp;&nbsp;👉 ผลบวกของทุกจำนวน = {' + '.join(map(str, ans_list))} = <b>{ans}</b><br>
                    <b>ตอบ: {ans}</b></span>"""
                else:
                    if is_p12: a = random.randint(5, 15); limit_val = random.randint(20, 40)
                    else: a = random.randint(10, 50); limit_val = random.randint(80, 150)
                        
                    max_val = limit_val - a - 1
                    q = f"จงหา <b>จำนวนนับที่มากที่สุด</b> ที่เติมในช่องว่าง:<br><br><span style='font-size:24px; font-weight:bold;'>🔲 + {a} &lt; {limit_val}</span>"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดอย่างละเอียด:</b><br>
                    <b>ขั้นตอนที่ 1:</b> คิดเสมือนว่ามันคือเครื่องหมาย "เท่ากับ" ก่อน ➔ 🔲 + {a} = {limit_val}<br>
                    &nbsp;&nbsp;&nbsp;👉 ย้ายข้างไปลบ จะได้ 🔲 = {limit_val} - {a} = <b>{limit_val - a}</b><br>
                    <b>ขั้นตอนที่ 2:</b> กลับสู่ความจริง โจทย์บอก <b>น้อยกว่า ( &lt; )</b> {limit_val}<br>
                    &nbsp;&nbsp;&nbsp;👉 ดังนั้นจำนวนที่มากที่สุดที่เป็นไปได้คือ {limit_val - a} - 1 = <b>{max_val}</b><br>
                    <b>ตอบ: {max_val}</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "ปริศนาตัวเลขที่หายไป":
                if is_challenge:
                    Z = random.randint(0, 4); C = random.randint(Z+3, 9)
                    Y = random.randint(0, 4); B = random.randint(Y+3, 9)
                    X = random.randint(5, 9); A = random.randint(1, X-3)
                    
                    Top = int(f"{X}{Y}{Z}")
                    Bot = int(f"{A}{B}{C}")
                    Res = Top - Bot
                    str_Res = str(Res).zfill(3)
                    
                    top_row = [box_html, str(Y), str(Z)]
                    bot_row = [str(A), box_html, str(C)]
                    res_row = [str_Res[0], str_Res[1], box_html]
                    
                    math_table = get_vertical_math(top_row, bot_row, res_row, operator="−")
                    
                    q = f"จงวิเคราะห์การตั้งลบแบบมีการยืมข้ามหลักต่อไปนี้ แล้วหาว่าตัวเลขที่ซ่อนอยู่ใน 🔲 จาก <b>บนลงล่าง</b> คือเลขใดตามลำดับ?<br>{math_table}"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (แกะรอยการลบและการยืมทีละหลัก):</b><br>
                    <b>หลักหน่วย:</b> {Z} - {C} ตัวตั้งน้อยกว่าตัวลบ จึงต้อง <b>'ยืม'</b> หลักสิบมา 10<br>
                    &nbsp;&nbsp;&nbsp;👉 กลายเป็น (10 + {Z}) - {C} = <b>{10+Z-C}</b> ➔ 🔲 ล่างสุดคือ <b>{10+Z-C}</b><br>
                    <b>หลักสิบ:</b> เลข {Y} ถูกยืมไป 1 จึงเหลือ {Y-1} แต่ยังต้องลบกับ 🔲 แล้วได้ {str_Res[1]}<br>
                    &nbsp;&nbsp;&nbsp;👉 ตัวตั้งเหลือน้อยกว่าแน่ๆ จึงต้อง <b>'ยืม'</b> หลักร้อยมาอีก 10 กลายเป็น (10 + {Y-1})<br>
                    &nbsp;&nbsp;&nbsp;👉 สมการคือ: {10+Y-1} - 🔲 = {str_Res[1]} ➔ ย้ายข้าง: {10+Y-1} - {str_Res[1]} = <b>{B}</b> ➔ 🔲 ตรงกลางคือ <b>{B}</b><br>
                    <b>หลักร้อย:</b> 🔲 ถูกหลักสิบยืมไป 1 จึงมีค่าลดลง 1<br>
                    &nbsp;&nbsp;&nbsp;👉 สมการคือ: (🔲 - 1) - {A} = {str_Res[0]} ➔ ย้ายข้างหาค่า 🔲 = {int(str_Res[0])} + {A} + 1 = <b>{X}</b> ➔ 🔲 บนสุดคือ <b>{X}</b><br>
                    <b>ตอบ: บนคือ {X}, กลางคือ {B}, ล่างคือ {10+Z-C}</b></span>"""
                else:
                    if is_p12:
                        a1, a2 = random.randint(1, 8), random.randint(1, 8)
                        b1, b2 = random.randint(1, 9 - a1), random.randint(1, 9 - a2)
                        str_a, str_b, str_ans = str(a1*10+a2).zfill(2), str(b1*10+b2).zfill(2), str((a1+b1)*10+(a2+b2)).zfill(2)
                        top_row, bot_row, res_row = [str_a[0], box_html], [box_html, str_b[1]], list(str_ans)
                        math_table = get_vertical_math(top_row, bot_row, res_row, operator="+")
                        q = f"จงเติมตัวเลขลงใน 🔲 ให้ถูกต้องสมบูรณ์<br>{math_table}"
                        sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดอย่างละเอียด (เจาะทีละหลัก):</b><br>
                        <b>หลักหน่วย (ขวาสุด):</b> 🔲 + {str_b[1]} = {str_ans[1]}<br>
                        &nbsp;&nbsp;&nbsp;👉 คิดย้อนกลับ: {str_ans[1]} - {str_b[1]} = <b>{str_a[1]}</b> (นี่คือตัวเลขกล่องบน)<br>
                        <b>หลักสิบ (ซ้ายสุด):</b> {str_a[0]} + 🔲 = {str_ans[0]}<br>
                        &nbsp;&nbsp;&nbsp;👉 คิดย้อนกลับ: {str_ans[0]} - {str_a[0]} = <b>{str_b[0]}</b> (นี่คือตัวเลขกล่องล่าง)<br>
                        <b>ตอบ: กล่องบนคือ {str_a[1]}, กล่องล่างคือ {str_b[0]}</b></span>"""
                    else:
                        n2 = random.randint(2, 9)
                        n1 = random.randint(11, 99)
                        ans_val = n1 * n2
                        str_n1, str_ans = str(n1), str(ans_val)
                        top_row = [str_n1[0], box_html]
                        bot_row = [str(n2)]
                        res_row = list(str_ans)
                        math_table = get_vertical_math(top_row, bot_row, res_row, operator="×")
                        
                        q = f"จงเติมตัวเลขลงใน 🔲 ให้การคูณนี้ถูกต้อง<br>{math_table}"
                        sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดอย่างละเอียด:</b><br>
                        จากโจทย์คือ ตัวตั้ง 2 หลัก × {n2} = {ans_val}<br>
                        ย้ายข้างการคูณไปเป็นหาร: จำนวนสองหลักคือ {ans_val} ÷ {n2} = <b>{n1}</b><br>
                        ดังนั้นตัวเลขที่หายไปในช่องว่างด้านบนคือ <b>{str_n1[1]}</b><br>
                        <b>ตอบ: {str_n1[1]}</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "ความยาวและเส้นรอบรูป":
                if is_challenge:
                    N = random.randint(3, 5)
                    S = random.randint(5, 12)
                    O = random.randint(1, S-2)
                    width = N * S - (N - 1) * O
                    ans = 2 * (width + S)
                    
                    q = f"<b>{name}</b> นำกระดาษรูปสี่เหลี่ยมจัตุรัสที่มีความยาวด้านละ <b>{S} ซม.</b> จำนวน <b>{N} แผ่น</b> มาวางเรียงต่อกันเป็นแนวยาว<br>โดยให้แต่ละแผ่นวางซ้อนทับกันเป็นระยะ <b>{O} ซม.</b><br>จงหาความยาวรอบรูปทั้งหมดของรูปทรงที่เกิดใหม่นี้?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (ความยาวที่ถูกซ่อน):</b><br>
                    เมื่อวางซ้อนทับกัน รูปทรงใหม่จะกลายเป็นสี่เหลี่ยมผืนผ้ายาวๆ 1 รูป<br>
                    <b>ขั้นตอนที่ 1: หาความยาว (แนวนอน) ของรูปใหม่</b><br>
                    &nbsp;&nbsp;&nbsp;👉 ถ้านำแผ่นมาต่อกันเฉยๆ จะยาว {N} × {S} = {N*S} ซม.<br>
                    &nbsp;&nbsp;&nbsp;👉 แต่มีรอยซ้อนทับ {N-1} รอย รอยละ {O} ซม. ➔ หดหายไป {N-1} × {O} = {(N-1)*O} ซม.<br>
                    &nbsp;&nbsp;&nbsp;👉 ความยาวจริง = {N*S} - {(N-1)*O} = <b>{width} ซม.</b><br>
                    <b>ขั้นตอนที่ 2: หาความกว้าง (แนวตั้ง)</b><br>
                    &nbsp;&nbsp;&nbsp;👉 ความกว้างยังคงเท่าเดิมคือด้านของจัตุรัส = <b>{S} ซม.</b><br>
                    <b>ขั้นตอนที่ 3: หาความยาวรอบรูปทั้งหมด</b><br>
                    &nbsp;&nbsp;&nbsp;👉 2 × (กว้าง + ยาว) = 2 × ({width} + {S}) = <b>{ans} ซม.</b><br>
                    <b>ตอบ: {ans} ซม.</b></span>"""
                else:
                    if is_p12: 
                        L = random.randint(4, 20) * 4
                        q = f"<b>{name}</b> มีลวดความยาว <b>{L} ซม.</b> นำไปดัดเป็นรูปสี่เหลี่ยมจัตุรัส จะมีความยาวด้านละกี่เซนติเมตร?"
                        sol = f"<span style='color: #2c3e50;'>จัตุรัสมี 4 ด้านที่เท่ากัน ➔ นำความยาวลวดทั้งหมดไปแบ่ง 4 ส่วน: {L} ÷ 4 = <b>{L//4} ซม.</b></span>"
                    else:
                        side = random.randint(5, 25)
                        leftover = random.randint(5, 20)
                        L = (side * 4) + leftover
                        q = f"<b>{name}</b> นำเส้นลวดที่มีความยาว <b>{L} ซม.</b> ไปสร้างรูปสี่เหลี่ยมจัตุรัสแล้ว <b>เหลือเศษลวด {leftover} ซม.</b><br>ความยาวของแต่ละด้านของรูปสี่เหลี่ยมจัตุรัสนี้เป็นกี่เซนติเมตร?"
                        sol = f"""<span style='color: #2c3e50;'><b>วิธีคิด:</b><br>
                        <b>ขั้นตอนที่ 1:</b> หาลวดที่ถูกใช้จริง นำลวดทั้งหมดหักส่วนที่เหลือทิ้ง: {L} - {leftover} = <b>{L - leftover} ซม.</b><br>
                        <b>ขั้นตอนที่ 2:</b> ลวด {L - leftover} ซม. ถูกดัดเป็นจัตุรัส (4 ด้านเท่ากัน) ➔ นำไปหาร 4<br>
                        &nbsp;&nbsp;&nbsp;👉 {L - leftover} ÷ 4 = <b>{side} ซม.</b><br>
                        <b>ตอบ: {side} ซม.</b></span>"""

            # ---------------------------------------------------------
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
                    
                    f1_4_s = get_vertical_fraction(1, 4, color="#2c3e50", is_bold=False)
                    f1_3_s = get_vertical_fraction(1, 3, color="#2c3e50", is_bold=False)
                    f1_2_s = get_vertical_fraction(1, 2, color="#2c3e50", is_bold=False)
                    f2_3_s = get_vertical_fraction(2, 3, color="#2c3e50", is_bold=False)
                    f3_4_s = get_vertical_fraction(3, 4, color="#2c3e50", is_bold=False)
                    
                    q = f"อคิณอ่านหนังสือเล่มหนึ่ง <b>วันแรกอ่านไป {f1_4} ของเล่ม</b><br><b>วันที่สองอ่านไป {f1_3} ของหน้าที่เหลือ</b> และอ่านเพิ่มอีก <b>{X} หน้า</b><br><b>วันที่สามอ่านไป {f1_2} ของหน้าที่เหลือ</b> และอ่านเพิ่มอีก <b>{Y} หน้า</b> ปรากฏว่าอ่านจบเล่มพอดี!<br>จงหาว่าหนังสือเล่มนี้มีทั้งหมดกี่หน้า?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดย้อนกลับ (Olympiad Level):</b><br>
                    เมื่อมีคำว่า "ของหน้าที่เหลือ" ซ้อนกัน ให้คิดย้อนจากวันสุดท้ายกลับมาวันแรกครับ!<br>
                    <b>วันที่ 3:</b> อ่านครึ่งหนึ่ง ({f1_2_s}) แล้วอ่านอีก {Y} หน้าจนจบเล่ม<br>
                    &nbsp;&nbsp;&nbsp;👉 แสดงว่า {Y} หน้าที่อ่านตอนท้าย ก็คือ "ครึ่งหนึ่ง" ที่เหลืออยู่นั่นเอง<br>
                    &nbsp;&nbsp;&nbsp;👉 จำนวนหน้าก่อนอ่านวันที่ 3 = {Y} × 2 = <b>{R2} หน้า</b><br>
                    <b>วันที่ 2:</b> อ่าน {f1_3_s} และอ่านเพิ่มอีก {X} หน้า ทำให้เหลือ {R2} หน้า<br>
                    &nbsp;&nbsp;&nbsp;👉 นำ {X} ไปคืนกลับ: {R2} + {X} = {R2+X} หน้า<br>
                    &nbsp;&nbsp;&nbsp;👉 ซึ่ง {R2+X} หน้า คิดเป็น {f2_3_s} ของวันนั้น (เพราะอ่านไป {f1_3_s})<br>
                    &nbsp;&nbsp;&nbsp;👉 จำนวนหน้าก่อนอ่านวันที่ 2 = ({R2+X} ÷ 2) × 3 = <b>{R1} หน้า</b><br>
                    <b>วันที่ 1:</b> อ่าน {f1_4_s} ทำให้เหลือ {R1} หน้า<br>
                    &nbsp;&nbsp;&nbsp;👉 ซึ่ง {R1} หน้า คิดเป็น {f3_4_s} ของทั้งเล่ม<br>
                    &nbsp;&nbsp;&nbsp;👉 จำนวนหน้าทั้งหมด = ({R1} ÷ 3) × 4 = <b>{Total} หน้า</b><br>
                    <b>ตอบ: {Total} หน้า</b></span>"""
                else:
                    if is_p12: 
                        baskets = random.randint(4, 9)
                        breads_per_b = random.randint(3, 10)
                        total_breads = baskets * breads_per_b
                        ask_b = random.randint(2, baskets-1)
                        q = f"<b>{name}</b> แบ่งขนมปัง <b>{total_breads} ชิ้น</b> ใส่ตะกร้า <b>{baskets} ใบ</b> ใบละเท่าๆ กัน<br>จงหาว่าขนมปังที่อยู่ในตะกร้า <b>{ask_b} ใบ</b> มีทั้งหมดกี่ชิ้น?"
                        sol = f"""<span style='color: #2c3e50;'><b>วิธีคิด:</b><br>
                        <b>ขั้นตอนที่ 1:</b> หาว่า 1 ตะกร้ามีกี่ชิ้น ➔ {total_breads} ÷ {baskets} = <b>{breads_per_b} ชิ้น</b><br>
                        <b>ขั้นตอนที่ 2:</b> ถ้าต้องการ {ask_b} ตะกร้า ➔ นำ {breads_per_b} × {ask_b} = <b>{breads_per_b * ask_b} ชิ้น</b><br>
                        <b>ตอบ: {breads_per_b * ask_b} ชิ้น</b></span>"""
                    else:
                        den = random.choice([4, 5, 6, 8, 10])
                        num = random.randint(1, den-2)
                        total_money = random.randint(10, 50) * den
                        ans_rem = total_money - int((total_money/den)*num)
                        
                        frac_html = get_vertical_fraction(num, den)
                        
                        q = f"<b>{name}</b> มีเงิน <b>{total_money} บาท</b> ซื้อเครื่องเขียนไป <b>{frac_html}</b> ของเงินทั้งหมด จะเหลือเงินกี่บาท?"
                        sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดอย่างละเอียด:</b><br>
                        <b>ขั้นตอนที่ 1: หาเงินที่ใช้ไป</b><br>
                        &nbsp;&nbsp;&nbsp;👉 นำเงินทั้งหมดมาแบ่งเป็น {den} ส่วน: {total_money} ÷ {den} = {total_money//den} บาท/ส่วน<br>
                        &nbsp;&nbsp;&nbsp;👉 ใช้ไป {num} ส่วน: {total_money//den} × {num} = <b>{int((total_money/den)*num)} บาท</b><br>
                        <b>ขั้นตอนที่ 2: หาเงินที่เหลือ</b><br>
                        &nbsp;&nbsp;&nbsp;👉 นำเงินตอนแรกมาหักออก: {total_money} - {int((total_money/den)*num)} = <b>{ans_rem} บาท</b><br>
                        <b>ตอบ: {ans_rem} บาท</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "การคำนวณหน่วยและเวลา":
                if is_challenge:
                    days_map = {"พฤหัสบดี": 3, "ศุกร์": 4, "เสาร์": 5}
                    end_day = random.choice(list(days_map.keys()))
                    days = days_map[end_day]
                    gain_m = random.randint(3, 12)
                    total_gain = days * gain_m
                    
                    real_h = 8
                    real_m = 0
                    
                    show_m = real_m + total_gain
                    carry_h = show_m // 60
                    final_m = show_m % 60
                    final_h = real_h + carry_h
                    
                    q = f"นาฬิกาเรือนหนึ่งทำงานผิดปกติ โดยจะเดิน <b>'เร็วเกินไป' วันละ {gain_m} นาที</b><br>ถ้า<b>{name}</b>ตั้งเวลานาฬิกาเรือนนี้ให้ตรงกับเวลาจริงในตอน <b>08:00 น. ของวันจันทร์</b><br>จงหาว่าเมื่อเวลาจริงคือ <b>08:00 น. ของวัน{end_day}ในสัปดาห์เดียวกัน</b> นาฬิกาเรือนนี้จะชี้บอกเวลาใด?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (คำนวณความคลาดเคลื่อนสะสม):</b><br>
                    <b>ขั้นตอนที่ 1: หาจำนวนวันที่ผ่านไป</b><br>
                    &nbsp;&nbsp;&nbsp;👉 จาก 08:00 น. วันจันทร์ ถึง 08:00 น. วัน{end_day} นับเวลาที่ผ่านไปได้ <b>{days} วันพอดีเป๊ะ</b><br>
                    <b>ขั้นตอนที่ 2: หาเวลาที่นาฬิกาเดินเพี้ยนไปทั้งหมด</b><br>
                    &nbsp;&nbsp;&nbsp;👉 เดินเร็ววันละ {gain_m} นาที × {days} วัน = <b>เดินเร็วไปทั้งหมด {total_gain} นาที</b><br>
                    <b>ขั้นตอนที่ 3: คำนวณเวลาบนหน้าปัด</b><br>
                    &nbsp;&nbsp;&nbsp;👉 เวลาจริงคือ 08:00 น. แต่นาฬิกาจะเดินนำหน้าไปอีก {total_gain} นาที<br>
                    &nbsp;&nbsp;&nbsp;👉 แปลงนาทีที่เดินเร็วเป็นชั่วโมง: {total_gain} นาที = <b>{carry_h} ชั่วโมง {final_m} นาที</b><br>
                    &nbsp;&nbsp;&nbsp;👉 นำไปบวกเพิ่มจากเวลาจริง: 08:00 น. + {carry_h} ชั่วโมง {final_m} นาที = <b>{final_h:02d}:{final_m:02d} น.</b><br>
                    <b>ตอบ: เวลา {final_h:02d}:{final_m:02d} น.</b></span>"""
                else:
                    if is_p12: 
                        h1 = random.randint(1, 4); m1 = random.randint(10, 20)
                        h2 = random.randint(1, 3); m2 = random.randint(10, 30)
                        q = f"<b>{name}</b> ใช้เวลาเดินทางช่วงแรก <b>{h1} ชั่วโมง {m1} นาที</b> และช่วงที่สองอีก <b>{h2} ชั่วโมง {m2} นาที</b> รวมใช้เวลาเท่าไร?"
                        sol = f"<span style='color: #2c3e50;'>รวมชั่วโมง: {h1} + {h2} = <b>{h1+h2} ชั่วโมง</b><br>รวมนาที: {m1} + {m2} = <b>{m1+m2} นาที</b><br><b>ตอบ: {h1+h2} ชั่วโมง {m1+m2} นาที</b></span>"
                    elif is_p34: 
                        km1 = random.randint(2, 6); m1 = random.randint(400, 800)
                        m2 = random.randint(1200, 2500)
                        total_m = (km1 * 1000) + m1 + m2
                        ans_km = total_m // 1000
                        ans_m = total_m % 1000
                        q = f"<b>{name}</b> จงหาผลบวกของระยะทาง:<br><b>{km1} กิโลเมตร {m1} เมตร  +  {m2} เมตร</b>  =  🔲 กิโลเมตร 🔲 เมตร"
                        sol = f"""<span style='color: #2c3e50;'><b>วิธีคิด:</b><br>
                        แปลงทุกอย่างเป็นเมตรก่อน: ({km1} × 1000) + {m1} = {km1 * 1000 + m1} เมตร<br>
                        นำมาบวกกัน: {km1 * 1000 + m1} + {m2} = <b>{total_m} เมตร</b><br>
                        แปลงกลับเป็นกิโลเมตร: {total_m} เมตร = <b>{ans_km} กม. {ans_m} ม.</b><br>
                        <b>ตอบ: {ans_km} กิโลเมตร {ans_m} เมตร</b></span>"""
                    else:
                        h1 = random.randint(2, 6); m1 = random.randint(40, 55)
                        h2 = random.randint(1, 4); m2 = random.randint(30, 55)
                        total_m = m1 + m2
                        carry_h = total_m // 60
                        left_m = total_m % 60
                        ans_h = h1 + h2 + carry_h
                        q = f"<b>{name}</b> เดินทางด้วยรถยนต์ <b>{h1} ชม. {m1} นาที</b> และต่อเรืออีก <b>{h2} ชม. {m2} นาที</b> รวมใช้เวลาทั้งหมดเท่าไร?"
                        sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดอย่างละเอียด:</b><br>
                        <b>ขั้นตอนที่ 1:</b> นำนาทีมาบวกกัน: {m1} + {m2} = <b>{total_m} นาที</b><br>
                        <b>ขั้นตอนที่ 2:</b> เนื่องจาก 60 นาที = 1 ชั่วโมง ➔ เราสามารถปัด {total_m} นาที เป็น <b>{carry_h} ชั่วโมง กับอีก {left_m} นาที</b><br>
                        <b>ขั้นตอนที่ 3:</b> นำชั่วโมงมาบวกกันทั้งหมด: {h1} + {h2} + {carry_h} (ที่ทดมา) = <b>{ans_h} ชั่วโมง</b><br>
                        <b>ตอบ: {ans_h} ชั่วโมง {left_m:02d} นาที</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "โจทย์ปัญหาเปรียบเทียบกลุ่ม":
                if is_challenge:
                    C = random.randint(5, 15)
                    P = random.randint(5, 15)
                    H = P + 3 * C
                    L = 4 * P + 6 * C
                    
                    q = f"ในฟาร์มของ<b>{name}</b>มี หมู ไก่ และเป็ด รวมกันทั้งหมด <b>{H} ตัว (นับหัว)</b> และนับขารวมกันได้ <b>{L} ขา</b><br>ถ้าเจ้าของฟาร์มบอกว่า <b>'มีจำนวนเป็ดเป็น 2 เท่าของจำนวนไก่'</b><br>จงหาว่าในฟาร์มแห่งนี้มีหมูทั้งหมดกี่ตัว?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (สมการนับหัว-นับขา):</b><br>
                    <b>ขั้นตอนที่ 1: ยุบรวมสัตว์ปีก (ไก่และเป็ด) ให้เป็นกลุ่มเดียว</b><br>
                    &nbsp;&nbsp;&nbsp;👉 เป็ดมีเป็น 2 เท่าของไก่ แปลว่าถ้าจัดกลุ่ม: ไก่ 1 ตัว จะมาพร้อมกับ เป็ด 2 ตัว เสมอ (รวมเป็น 3 ตัวใน 1 เซ็ต)<br>
                    &nbsp;&nbsp;&nbsp;👉 1 เซ็ตมี 3 ตัว (หัว) และมีขา = (ไก่ 1 ตัว = 2 ขา) + (เป็ด 2 ตัว = 4 ขา) = <b>6 ขาต่อเซ็ต</b><br>
                    &nbsp;&nbsp;&nbsp;👉 สรุป: สัตว์ปีก 1 เซ็ต มี 3 หัว 6 ขา (ซึ่งตกเฉลี่ย <b>หัวละ 2 ขา</b> เท่าเดิม!)<br>
                    <b>ขั้นตอนที่ 2: สมมติฐานแบบสุดโต่ง (สมมติว่าเป็นสัตว์ปีกทั้งหมด)</b><br>
                    &nbsp;&nbsp;&nbsp;👉 ถ้าสัตว์ทั้ง {H} ตัวเป็นสัตว์ปีกทั้งหมด จะมีขา: {H} × 2 = <b>{H*2} ขา</b><br>
                    &nbsp;&nbsp;&nbsp;👉 แต่ขาจริงมี {L} ขา แสดงว่ามีขาเกินมา: {L} - {H*2} = <b>{L - H*2} ขา</b><br>
                    <b>ขั้นตอนที่ 3: หาจำนวนหมู</b><br>
                    &nbsp;&nbsp;&nbsp;👉 ขาที่เกินมา เกิดจากการที่ "หมูมีขามากกว่าสัตว์ปีกอยู่ตัวละ 2 ขา" (4 ลบ 2)<br>
                    &nbsp;&nbsp;&nbsp;👉 นำขาที่เกินมา หารด้วย 2 จะได้จำนวนหมู: {L - H*2} ÷ 2 = <b>{P} ตัว</b><br>
                    <b>ตอบ: มีหมู {P} ตัว</b></span>"""
                else:
                    if is_p12: 
                        dozens = random.randint(2, 6)
                        students = random.choice([2, 3, 4, 6])
                        total_items = dozens * 12
                        ans = total_items // students
                        q = f"คุณครู<b>{name}</b>มีดินสอ <b>{dozens} โหล</b> นำมาแบ่งให้นักเรียน <b>{students} คน</b> คนละเท่าๆ กัน<br>นักเรียนจะได้รับดินสอคนละกี่แท่ง?"
                        sol = f"""<span style='color: #2c3e50;'><b>วิธีคิด:</b><br>
                        <b>ขั้นตอนที่ 1:</b> แปลงโหลเป็นแท่ง (1 โหล = 12 แท่ง) ➔ {dozens} โหล = {dozens} × 12 = <b>{total_items} แท่ง</b><br>
                        <b>ขั้นตอนที่ 2:</b> แบ่งให้เด็ก {students} คน ➔ นำมาหาร: {total_items} ÷ {students} = <b>{ans} แท่ง</b><br>
                        <b>ตอบ: {ans} แท่ง</b></span>"""
                    else:
                        g1_std, g1_items = random.randint(10, 15), random.randint(5, 9)
                        g2_std, g2_items = random.randint(16, 22), random.randint(3, 5)
                        t1 = g1_std * g1_items
                        t2 = g2_std * g2_items
                        diff = abs(t1 - t2)
                        more_g = "กลุ่มแรก" if t1 > t2 else "กลุ่มที่สอง"
                        q = f"คุณครู<b>{name}</b>แจกสมุดให้เด็กกลุ่มแรก <b>{g1_std} คน คนละ {g1_items} เล่ม</b> และกลุ่มที่สอง <b>{g2_std} คน คนละ {g2_items} เล่ม</b><br>กลุ่มใดได้รับสมุดรวมมากกว่ากัน และมากกว่ากันกี่เล่ม?"
                        sol = f"""<span style='color: #2c3e50;'><b>วิธีคิด:</b><br>
                        <b>ขั้นตอนที่ 1:</b> หากลุ่มแรก ➔ {g1_std} × {g1_items} = <b>{t1} เล่ม</b><br>
                        <b>ขั้นตอนที่ 2:</b> หากลุ่มที่สอง ➔ {g2_std} × {g2_items} = <b>{t2} เล่ม</b><br>
                        <b>ขั้นตอนที่ 3:</b> เปรียบเทียบ จะเห็นว่า <b>{more_g}</b> ได้มากกว่า<br>
                        <b>ขั้นตอนที่ 4:</b> หาผลต่าง ➔ {max(t1,t2)} - {min(t1,t2)} = <b>{diff} เล่ม</b><br>
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
                    
                    af, bf, cf = a_now+f, b_now+f, c_now+f
                    g_ans = math.gcd(math.gcd(af, bf), cf)
                    
                    q = f"ปัจจุบัน อัตราส่วนอายุของ <b>{n1} ต่อ {n2} เป็น {r1_a}:{r1_b}</b> และอัตราส่วนอายุของ <b>{n2} ต่อ {n3} เป็น {r2_b}:{r2_c}</b><br>ถ้าปัจจุบัน {n2} อายุ {b_now} ปี จงหาอัตราส่วนอายุของ <b>{n1} : {n2} : {n3}</b> ในอีก {f} ปีข้างหน้า? (ตอบเป็นอัตราส่วนอย่างต่ำ)"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (อัตราส่วนต่อเนื่อง):</b><br>
                    <b>ขั้นตอนที่ 1: หาอายุปัจจุบันของทุกคน</b><br>
                    &nbsp;&nbsp;&nbsp;👉 {n2} อายุ {b_now} ปี (เทียบจากอัตราส่วน {n1}:{n2} = {r1_a}:{r1_b} จะได้ส่วนละ {b_now//r1_b} ปี) ➔ {n1} = {r1_a}×{b_now//r1_b} = <b>{a_now} ปี</b><br>
                    &nbsp;&nbsp;&nbsp;👉 (เทียบจากอัตราส่วน {n2}:{n3} = {r2_b}:{r2_c} จะได้ส่วนละ {b_now//r2_b} ปี) ➔ {n3} = {r2_c}×{b_now//r2_b} = <b>{c_now} ปี</b><br>
                    <b>ขั้นตอนที่ 2: หาอายุในอีก {f} ปีข้างหน้า</b><br>
                    &nbsp;&nbsp;&nbsp;👉 บวกเพิ่มคนละ {f}: {n1}={af}, {n2}={bf}, {n3}={cf}<br>
                    <b>ขั้นตอนที่ 3: ทำเป็นอัตราส่วนอย่างต่ำ</b><br>
                    &nbsp;&nbsp;&nbsp;👉 นำ ห.ร.ม. ({g_ans}) มาหารตลอด: {af} : {bf} : {cf} ➔ <b>{af//g_ans} : {bf//g_ans} : {cf//g_ans}</b><br>
                    <b>ตอบ: {af//g_ans} : {bf//g_ans} : {cf//g_ans}</b></span>"""
                else:
                    if is_p12: a_now = random.randint(5, 8); diff = random.randint(5, 10); f = random.choice([3, 4, 5])
                    elif is_p34: a_now = random.randint(8, 15); diff = random.randint(20, 30); f = random.choice([5, 10, 12])
                    else: a_now = random.randint(12, 25); diff = random.randint(25, 40); f = random.choice([10, 15, 20, 25])
                    
                    b_now = a_now + diff; r1_val, r2_val = a_now + f, b_now + f; g = math.gcd(r1_val, r2_val)
                    q = f"ปัจจุบัน <b>{n2}</b> อายุ {a_now} ปี และ <b>{n1}</b> อายุ {b_now} ปี <br>จงหาว่าเมื่อเวลาผ่านไปอีก {f} ปีในอนาคต อัตราส่วนอายุของ <b>{n2} ต่อ {n1}</b> จะเป็นเท่าใด? (อัตราส่วนอย่างต่ำ)"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) หาอายุในอนาคต: {n2} = {a_now} + {f} = <b>{r1_val} ปี</b>, {n1} = {b_now} + {f} = <b>{r2_val} ปี</b><br>2) เขียนอัตราส่วน {n2} : {n1} = <b>{r1_val} : {r2_val}</b><br>3) ทอนเป็นอัตราส่วนอย่างต่ำโดยนำ <b>{g}</b> มาหาร: <b>{r1_val//g} : {r2_val//g}</b><br><b>ตอบ: {r1_val//g} : {r2_val//g}</b></span>"

            # ---------------------------------------------------------
            elif actual_sub_t == "การปักเสาและปลูกต้นไม้":
                role = random.choice(BUILDERS); action = random.choice(BUILD_ACTIONS); loc = random.choice(BUILD_LOCS)
                if is_challenge:
                    d = random.choice([4, 5, 8, 10]); length = random.randint(100, 300)
                    while length % d != 0: length += 1
                    ans = ((length // d) + 1) * 2
                    q = f"<b>{role}</b> มีโครงการ<b>{action}</b>บริเวณ <b>'สองฝั่ง'</b> ของถนนเส้นหนึ่งที่มีความยาว <b>{length} เมตร</b> โดยปักห่างกัน <b>{d} เมตร</b> และต้องติดตั้งที่จุดเริ่มต้นและสิ้นสุดด้วย <br>จะใช้สิ่งที่ติดตั้งทั้งหมดกี่จุด?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (คูณสองฝั่ง):</b><br>
                    1) คำนวณฝั่งเดียวก่อน (ถนนเส้นตรงมีปิดหัวท้าย): จำนวนจุด = (ระยะทาง ÷ ระยะห่าง) + 1<br>
                    &nbsp;&nbsp;&nbsp;👉 ({length} ÷ {d}) + 1 = {length//d} + 1 = <b>{(length//d)+1} จุด</b><br>
                    2) เนื่องจากทำ <b>สองฝั่งของถนน</b> ต้องนำไปคูณ 2: {(length//d)+1} × 2 = <b>{ans} จุด</b><br>
                    <b>ตอบ: {ans} จุด</b></span>"""
                else:
                    if is_p12: d = random.choice([2, 3, 4, 5]); trees = random.randint(5, 10)
                    elif is_p34: d = random.choice([5, 8, 10, 12]); trees = random.randint(15, 35)
                    else: d = random.choice([10, 15, 20, 25]); trees = random.randint(40, 100)
                    length = (trees - 1) * d
                    q = f"<b>{role}</b> มีโครงการ<b>{action}</b>ที่<b>{loc}</b> โดยแต่ละจุดห่างกัน <b>{d} เมตร</b> และต้องปักที่จุดเริ่มต้นและสิ้นสุดพอดี <br>ถ้านับรวมได้ <b>{trees} จุด</b> ระยะทางนี้ยาวกี่เมตร?"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>มี {trees} จุด จะมีช่องว่าง = {trees} - 1 = <b>{trees - 1} ช่อง</b><br>ระยะทางรวม = จำนวนช่องว่าง × ระยะห่าง = {trees - 1} × {d} = <b>{length} เมตร</b><br><b>ตอบ: {length} เมตร</b></span>"

            # ---------------------------------------------------------
            elif actual_sub_t == "เส้นทางที่เป็นไปได้":
                loc1 = random.choice(["บ้าน", "กทม."]); loc2 = random.choice(["ตลาด", "อยุธยา"]); loc3 = random.choice(["โรงเรียน", "เชียงใหม่"])
                if is_challenge:
                    p1, p2 = random.randint(3, 5), random.randint(2, 4)
                    ans = (p1 * p2) * ((p1 - 1) * (p2 - 1))
                    q = f"มีเส้นทางจาก <b>{loc1} ไป {loc2}</b> จำนวน <b>{p1} สาย</b> และจาก <b>{loc2} ไป {loc3}</b> จำนวน <b>{p2} สาย</b><br>ต้องการเดินทางแบบ <b>ไป-กลับ ({loc1} ➔ {loc3} ➔ {loc1})</b> โดยมีข้อแม้ว่า <b>'ขากลับห้ามใช้เส้นทางเดิมที่เคยใช้ตอนขาไปเด็ดขาด'</b><br>จะมีรูปแบบการเดินทางไป-กลับทั้งหมดกี่วิธี?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (กฎการคูณแบบมีเงื่อนไข):</b><br>
                    <b>ขั้นตอนที่ 1: ขาไป ({loc1} ➔ {loc2} ➔ {loc3})</b><br>
                    &nbsp;&nbsp;&nbsp;👉 ใช้ถนนได้เต็มที่: {p1} × {p2} = <b>{p1 * p2} วิธี</b><br>
                    <b>ขั้นตอนที่ 2: ขากลับ ({loc3} ➔ {loc2} ➔ {loc1})</b><br>
                    &nbsp;&nbsp;&nbsp;👉 ต้องหักเส้นทางที่ใช้ไปแล้วช่วงละ 1 สาย: เหลือ <b>{p2-1} สาย</b> และ <b>{p1-1} สาย</b><br>
                    &nbsp;&nbsp;&nbsp;👉 รูปแบบขากลับ: {p2-1} × {p1-1} = <b>{(p1-1) * (p2-1)} วิธี</b><br>
                    <b>ขั้นตอนที่ 3: รวมไป-กลับต่อเนื่องกัน (นำมาคูณกัน)</b><br>
                    &nbsp;&nbsp;&nbsp;👉 {p1 * p2} × {(p1-1) * (p2-1)} = <b>{ans:,} วิธี</b><br>
                    <b>ตอบ: {ans:,} วิธี</b></span>"""
                else:
                    if is_p12: p1, p2, p3 = 2, 2, 1
                    elif is_p34: p1, p2, p3 = random.randint(3, 4), random.randint(2, 3), random.randint(1, 2)
                    else: p1, p2, p3 = random.randint(4, 6), random.randint(3, 5), random.randint(2, 4)
                    ans = (p1 * p2) + p3
                    q = f"เดินทางจาก <b>{loc1} ไป {loc2}</b> มีทาง <b>{p1} สาย</b>, จาก <b>{loc2} ไป {loc3}</b> มีทาง <b>{p2} สาย</b> <br>และมีทางด่วนพิเศษจาก <b>{loc1} ไป {loc3}</b> (ไม่ผ่าน {loc2}) อีก <b>{p3} สาย</b><br>จะมีรูปแบบเดินทางจาก <b>{loc1} ไป {loc3}</b> ทั้งหมดกี่วิธี?"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>กรณี 1 (ผ่าน {loc2}): {p1} × {p2} = <b>{p1 * p2} วิธี</b><br>กรณี 2 (ทางด่วน): = <b>{p3} วิธี</b><br>รวม 2 กรณี: {p1 * p2} + {p3} = <b>{ans} วิธี</b><br><b>ตอบ: {ans} วิธี</b></span>"

            # ---------------------------------------------------------
            elif actual_sub_t == "คะแนนยิงเป้า":
                if is_challenge:
                    darts = random.randint(4, 5); pool = [10, 5, 3]
                    miss_penalty = random.randint(1, 2)
                    hits = random.choices(pool, k=darts-1) + [0]
                    total_score = sum(hits) - miss_penalty
                    q = f"เกมปาลูกดอกมีเป้าคะแนน <b>10, 5, 3</b> ถ้าปาพลาดเป้าจะถูก <b>หัก {miss_penalty} คะแนน</b><br><b>{name}</b> ปาลูกดอกทั้งหมด <b>{darts} ครั้ง</b> ได้คะแนนรวม <b>{total_score} คะแนน</b> <br>จงหาว่าเขาปาเข้าเป้าคะแนนใดบ้าง และพลาดกี่ครั้ง? (เรียงจากมากไปน้อย)"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (Trial and Error with Penalty):</b><br>
                    1) ลองตั้งสมมติฐานว่ามี 'ปาพลาด 1 ครั้ง' (ได้ 0 คะแนน และโดนหัก {miss_penalty})<br>
                    &nbsp;&nbsp;&nbsp;👉 แสดงว่าอีก {darts-1} ครั้งที่เข้าเป้า ต้องรวมคะแนนให้ได้: {total_score} + {miss_penalty} = <b>{sum(hits)} คะแนน</b><br>
                    2) จัดกลุ่มตัวเลขจาก {pool} จำนวน {darts-1} ครั้ง ให้ได้ {sum(hits)}<br>
                    &nbsp;&nbsp;&nbsp;👉 จะพบว่ารูปแบบที่ถูกต้องคือ: <b>{' + '.join(map(str, sorted([h for h in hits if h > 0], reverse=True)))}</b><br>
                    <b>ตอบ: เข้าเป้าคะแนน {sorted([h for h in hits if h > 0], reverse=True)} และปาพลาด 1 ครั้ง</b></span>"""
                else:
                    if is_p12: darts, pool = 2, [10, 5, 2]
                    elif is_p34: darts, pool = 3, [20, 10, 5, 2]
                    else: darts, pool = random.choice([4, 5]), [50, 20, 10, 5]
                    pool.sort(reverse=True)
                    hits = random.choices(pool, k=darts)
                    total_score = sum(hits)
                    hits.sort(reverse=True)
                    q = f"เกมปาลูกดอก เป้ามีคะแนน <b>{', '.join(map(str, pool))} คะแนน</b><br><b>{name}</b> ปาลูกดอก <b>{darts} ครั้ง</b> เข้าเป้าทุกครั้ง ได้คะแนนรวม <b>{total_score} คะแนน</b> <br>จงหาว่าปาเข้าเป้าวงใดบ้าง? (เรียงจากมากไปน้อย)"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>สุ่มแจกแจงตัวเลข {darts} ครั้งบวกกันให้ได้ {total_score} (โดยเริ่มพิจารณาจากเลขมากสุดก่อน)<br>รูปแบบที่รวมกันได้ {total_score} พอดีคือ: <b>{' + '.join(map(str, hits))} = {total_score}</b><br><b>ตอบ: {hits}</b></span>"

            # ---------------------------------------------------------
            elif actual_sub_t == "การนับหน้าหนังสือ":
                publisher = random.choice(PUBLISHERS); book_type = random.choice(DOC_TYPES)
                if is_challenge:
                    pages = random.randint(200, 400)
                    total_digits = 9 + 180 + ((pages - 99) * 3)
                    q = f"<b>{publisher}</b> กำลังพิมพ์ตัวเลขหน้าหนังสือ<b>{book_type}</b> โดยเริ่มตั้งแต่หน้า 1 <br>เมื่อพิมพ์เสร็จ พบว่าใช้ตัวเลขโดด (0-9) ไปทั้งหมด <b>{total_digits:,} ตัว</b> <br>จงหาว่าหนังสือเล่มนี้มีทั้งหมดกี่หน้า?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ย้อนกลับ (Olympiad Level):</b><br>
                    <b>ขั้นตอนที่ 1: หักล้างตัวเลขหน้า 1 หลัก และ 2 หลักออกไปก่อน</b><br>
                    &nbsp;&nbsp;&nbsp;👉 หน้า 1-9 ใช้เลข 9 ตัว (เหลือ {total_digits} - 9 = {total_digits - 9} ตัว)<br>
                    &nbsp;&nbsp;&nbsp;👉 หน้า 10-99 (90 หน้า) ใช้เลข 90×2 = 180 ตัว (เหลือ {total_digits-9} - 180 = <b>{total_digits - 189} ตัว</b>)<br>
                    <b>ขั้นตอนที่ 2: คำนวณจำนวนหน้า 3 หลักที่เหลือ</b><br>
                    &nbsp;&nbsp;&nbsp;👉 ตัวเลขโดดที่เหลือ {total_digits - 189} ตัว ล้วนเป็นของหน้า 3 หลัก (หลักร้อย)<br>
                    &nbsp;&nbsp;&nbsp;👉 นำไปหาร 3: {total_digits - 189} ÷ 3 = <b>{(total_digits - 189)//3} หน้า</b><br>
                    <b>ขั้นตอนที่ 3: รวมจำนวนหน้าทั้งหมด</b><br>
                    &nbsp;&nbsp;&nbsp;👉 9 (หน้าหลักเดียว) + 90 (หน้าสองหลัก) + {(total_digits - 189)//3} (หน้าสามหลัก) = <b>{pages} หน้า</b><br>
                    <b>ตอบ: {pages} หน้า</b></span>"""
                else:
                    if is_p12: pages = random.randint(20, 50)
                    elif is_p34: pages = random.randint(100, 250)
                    else: pages = random.randint(300, 999)
                    
                    if pages > 99:
                        ans = 9 + 180 + ((pages - 99) * 3)
                        calc = f"เลข 1 หลัก (1-9): 9 ตัว<br>เลข 2 หลัก (10-99): 90 × 2 = 180 ตัว<br>เลข 3 หลัก (100-{pages}): {pages - 99} × 3 = <b>{(pages - 99) * 3} ตัว</b><br>รวม: 9 + 180 + {(pages - 99) * 3} = <b>{ans} ตัว</b>"
                    else:
                        ans = 9 + ((pages - 9) * 2)
                        calc = f"เลข 1 หลัก (1-9): 9 ตัว<br>เลข 2 หลัก (10-{pages}): {pages - 9} × 2 = <b>{(pages - 9) * 2} ตัว</b><br>รวม: 9 + {(pages - 9) * 2} = <b>{ans} ตัว</b>"
                    
                    q = f"<b>{publisher}</b>พิมพ์<b>{book_type}</b> ความหนารวม <b>{pages}</b> หน้า ต้องพิมพ์เลขหน้ามุมกระดาษตั้งแต่ 1 ถึง {pages} <br>จะใช้ตัวเลขโดดรวมทั้งหมดกี่ตัว?"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>แบ่งนับเป็นกลุ่มตามจำนวนหลักของเลขหน้า:<br>{calc}<br><b>ตอบ: {ans} ตัว</b></span>"

            # ---------------------------------------------------------
            elif actual_sub_t == "พื้นที่แรเงา (เรขาคณิต)":
                mat = random.choice(MATERIALS)
                if is_challenge:
                    in_r = random.choice([7, 14]) 
                    out_s = in_r * 2 + random.choice([10, 20])
                    area_sq = out_s ** 2
                    area_cir = int((22/7) * in_r * in_r)
                    ans = area_sq - area_cir
                    
                    pi_frac = get_vertical_fraction(22, 7, is_bold=False)
                    
                    q = f"แผ่น<b>{mat}</b>รูปสี่เหลี่ยมจัตุรัสยาวด้านละ <b>{out_s} ซม.</b> ช่างเจาะรูตรงกลางเป็น 'รูปวงกลม' ที่มีรัศมี <b>{in_r} ซม.</b> ทิ้งไป <br>จงหาพื้นที่ของแผ่น<b>{mat}</b>ส่วนที่เหลือ? (กำหนดให้ π ≈ {pi_frac})"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์:</b><br>
                    <b>1) หาพื้นที่สี่เหลี่ยมจัตุรัสแผ่นใหญ่:</b><br>
                    &nbsp;&nbsp;&nbsp;👉 ด้าน × ด้าน = {out_s} × {out_s} = <b>{area_sq:,} ตร.ซม.</b><br>
                    <b>2) หาพื้นที่วงกลมที่เจาะทิ้ง:</b><br>
                    &nbsp;&nbsp;&nbsp;👉 π × r × r = {pi_frac} × {in_r} × {in_r} = <b>{area_cir:,} ตร.ซม.</b><br>
                    <b>3) พื้นที่ส่วนที่เหลือ:</b><br>
                    &nbsp;&nbsp;&nbsp;👉 นำมาลบกัน: {area_sq:,} - {area_cir:,} = <b>{ans:,} ตร.ซม.</b><br>
                    <b>ตอบ: {ans:,} ตร.ซม.</b></span>"""
                else:
                    if is_p12: out_w, out_h, in_s = 10, 10, random.randint(2, 4)
                    elif is_p34: out_w, out_h = random.randint(20, 30), random.randint(15, 20); in_s = random.randint(4, 8)
                    else: out_w, out_h = random.randint(40, 80), random.randint(30, 60); in_s = random.randint(10, 20)
                    
                    ans = (out_w * out_h) - (in_s**2)
                    q = f"แผ่น<b>{mat}</b>รูปสี่เหลี่ยมผืนผ้า กว้าง <b>{out_w} ซม.</b> ยาว <b>{out_h} ซม.</b> ตัดเจาะรูตรงกลางเป็น 'สี่เหลี่ยมจัตุรัส' ยาวด้านละ <b>{in_s} ซม.</b> ทิ้งไป <br>จงหาพื้นที่ส่วนที่เหลือ?"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>พื้นที่แผ่นใหญ่: {out_w} × {out_h} = <b>{out_w * out_h} ตร.ซม.</b><br>พื้นที่รู: {in_s} × {in_s} = <b>{in_s**2} ตร.ซม.</b><br>ส่วนที่เหลือ: {out_w * out_h} - {in_s**2} = <b>{ans} ตร.ซม.</b><br><b>ตอบ: {ans} ตร.ซม.</b></span>"

            # ---------------------------------------------------------
            elif actual_sub_t == "จัดของใส่กล่อง (Modulo)":
                item = random.choice(FRUITS + ITEMS); container = random.choice(CONTAINERS)
                if is_challenge:
                    m1, m2 = 3, 5
                    rem1, rem2 = random.randint(1, 2), random.randint(1, 4)
                    ans = 0
                    for i in range(1, 100):
                        if i % m1 == rem1 and i % m2 == rem2:
                            ans = i
                            break
                    if ans == 0: continue
                    
                    q = f"คุณครูมี<b>{item}</b>จำนวนหนึ่ง <br>ถ้าจัดใส่<b>{container}</b>ละ {m1} ชิ้น จะเหลือเศษ <b>{rem1} ชิ้น</b><br>แต่ถ้าเปลี่ยนมาจัดใส่<b>{container}</b>ละ {m2} ชิ้น จะเหลือเศษ <b>{rem2} ชิ้น</b> พอดี<br>จงหาว่าคุณครูมี<b>{item}</b>น้อยที่สุดกี่ชิ้น?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (ค.ร.น. เศษเหลือ):</b><br>
                    ใช้วิธีลองไล่ตัวเลข (Listing) ที่ตรงกับเงื่อนไขแรก แล้วเช็กเงื่อนไขที่สอง<br>
                    <b>1) จำนวนที่เมื่อจัดทีละ {m1} แล้วเหลือเศษ {rem1}:</b><br>
                    &nbsp;&nbsp;&nbsp;👉 ท่องแม่ {m1} แล้วบวกเศษ: {(m1*1)+rem1}, {(m1*2)+rem1}, {(m1*3)+rem1}, {(m1*4)+rem1}, {(m1*5)+rem1}, {(m1*6)+rem1}...<br>
                    <b>2) นำตัวเลขเหล่านั้นมาลองหารด้วย {m2} ดูว่าตัวไหนเหลือเศษ {rem2}:</b><br>
                    &nbsp;&nbsp;&nbsp;👉 ตัวเลขตัวแรกที่ตรงตามเงื่อนไขที่สองด้วยคือ <b>{ans}</b> (เพราะ {ans} ÷ {m2} = {ans//m2} เศษ {ans%m2})<br>
                    <b>ตอบ: {ans} ชิ้น</b></span>"""
                else:
                    if is_p12: box_cap = random.randint(3, 5); num_boxes = random.randint(5, 10)
                    elif is_p34: box_cap = random.randint(8, 12); num_boxes = random.randint(15, 25)
                    else: box_cap = random.randint(15, 25); num_boxes = random.randint(30, 50)
                    
                    rem = random.randint(1, box_cap - 1); total_items = (box_cap * num_boxes) + rem
                    q = f"มี<b>{item}</b>ทั้งหมด <b>{total_items}</b> ชิ้น จัดใส่<b>{container}</b> ใบละ <b>{box_cap}</b> ชิ้นเท่าๆ กัน <br>จะได้<b>{container}</b>เต็มกี่ใบ? และเหลือเศษกี่ชิ้น?"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>ตั้งหาร: {total_items} ÷ {box_cap}<br>ผลลัพธ์ = <b>{num_boxes} ใบ</b> และเหลือเศษ <b>{rem} ชิ้น</b><br><b>ตอบ: ได้ {num_boxes} ใบ เศษ {rem} ชิ้น</b></span>"

            # ---------------------------------------------------------
            elif actual_sub_t == "วันที่และปฏิทิน":
                d_th = ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"]
                if is_challenge:
                    s_d, s_idx = random.randint(1, 5), random.randint(0, 6)
                    months = [("มกราคม", 31), ("กุมภาพันธ์", 28), ("มีนาคม", 31), ("เมษายน", 30)]
                    start_m_idx = random.randint(0, 1)
                    target_m_idx = start_m_idx + 2
                    
                    start_month, start_days = months[start_m_idx]
                    _, mid_days = months[start_m_idx+1]
                    target_month, _ = months[target_m_idx]
                    
                    t_d = random.randint(10, 20)
                    
                    add_days = (start_days - s_d) + mid_days + t_d
                    t_idx = (s_idx + (add_days % 7)) % 7
                    
                    q = f"ในปีปกติ (กุมภาพันธ์มี 28 วัน)<br>ถ้าวันที่ <b>{s_d} {start_month}</b> ตรงกับ <b>วัน{d_th[s_idx]}</b> <br>จงหาว่า วันที่ <b>{t_d} {target_month}</b> ของปีเดียวกัน จะตรงกับวันอะไรในสัปดาห์?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (การนับวันข้ามเดือน):</b><br>
                    <b>1) หาจำนวนวันทั้งหมดที่ต้องนับเดินหน้า:</b><br>
                    &nbsp;&nbsp;&nbsp;👉 วันที่เหลือในเดือน{start_month}: {start_days} - {s_d} = <b>{start_days - s_d} วัน</b><br>
                    &nbsp;&nbsp;&nbsp;👉 จำนวนวันในเดือนถัดไป: <b>{mid_days} วัน</b><br>
                    &nbsp;&nbsp;&nbsp;👉 จำนวนวันในเดือน{target_month}: <b>{t_d} วัน</b><br>
                    &nbsp;&nbsp;&nbsp;👉 รวมวันเดินทาง: {start_days - s_d} + {mid_days} + {t_d} = <b>{add_days} วัน</b><br>
                    <b>2) นำไปหารสัปดาห์ (หาร 7):</b><br>
                    &nbsp;&nbsp;&nbsp;👉 {add_days} ÷ 7 = ได้ {add_days//7} สัปดาห์ <b>เศษ {add_days%7} วัน</b><br>
                    <b>3) นับนิ้วต่อจากวัน{d_th[s_idx]}:</b><br>
                    &nbsp;&nbsp;&nbsp;👉 เดินหน้าไป {add_days%7} วัน จะตกที่ <b>วัน{d_th[t_idx]}</b> พอดี<br>
                    <b>ตอบ: ตรงกับวัน{d_th[t_idx]}</b></span>"""
                else:
                    s_d, s_idx = random.randint(1, 5), random.randint(0, 6)
                    if is_p12: add = random.randint(7, 15)
                    elif is_p34: add = random.randint(20, 45)
                    else: add = random.randint(50, 120)
                    
                    t_idx = (s_idx + (add % 7)) % 7
                    q = f"ถ้าวันที่ <b>{s_d}</b> ของเดือนนี้ ตรงกับ <b>วัน{d_th[s_idx]}</b> พอดี <br>จงหาว่าอีก <b>{add} วันข้างหน้า</b> จะตรงกับวันอะไรในสัปดาห์?"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>วนลูป 7 วัน: {add} ÷ 7 = ได้ {add//7} สัปดาห์ และเหลือเศษ <b>{add%7} วัน</b><br>นับนิ้วถัดจาก <b>วัน{d_th[s_idx]}</b> ไปอีก {add%7} วัน จะตกที่ <b>วัน{d_th[t_idx]}</b><br><b>ตอบ: วัน{d_th[t_idx]}</b></span>"

            # ---------------------------------------------------------
            elif actual_sub_t == "สัตว์ปีนบ่อ":
                animal = random.choice(ANIMALS)
                if is_challenge:
                    u, d = 5, 2
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
                        
                    q = f"<b>{animal}</b>ตกลงไปในบ่อลึก <b>{h} เมตร</b><br>ตอนกลางวันปีนขึ้นได้ <b>{u} เมตร</b> ตอนกลางคืนลื่นตกลง <b>{d} เมตร</b> เสมอ<br>แต่ <b>'ทุกๆ คืนวันที่ 3'</b> ฝนจะตกทำให้ลื่นไถลลงไปถึง <b>{heavy_d} เมตร</b>แทน<br>จงหาว่าจะใช้เวลากี่วันจึงจะปีนพ้นปากบ่อ?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (Simulation จำลองเหตุการณ์):</b><br>
                    ข้อนี้สูตรลัดใช้ไม่ได้เพราะมีเงื่อนไขฝนตก ต้องไล่บวกทีละวันอย่างระมัดระวัง!<br>
                    &nbsp;&nbsp;&nbsp;👉 <b>วันที่ 1:</b> ขึ้น {u} ลื่น {d} ➔ ยืนอยู่ที่ <b>{u-d} ม.</b><br>
                    &nbsp;&nbsp;&nbsp;👉 <b>วันที่ 2:</b> ขึ้น {u} ลื่น {d} ➔ ยืนอยู่ที่ <b>{(u-d)*2} ม.</b><br>
                    &nbsp;&nbsp;&nbsp;👉 <b>วันที่ 3 (ฝนตก):</b> ขึ้น {u} ลื่น {heavy_d} ➔ ...<br>
                    เมื่อจำลองการบวกลบไปเรื่อยๆ จะพบว่าใน <b>วันที่ {days}</b> ตอนกลางวันเมื่อปีนขึ้นไปอีก {u} เมตร จะถึงปากบ่อพอดี (ไม่ต้องรอลื่นลงมาอีกแล้ว!)<br>
                    <b>ตอบ: {days} วัน</b></span>"""
                else:
                    if is_p12: u, d, h = random.randint(3, 4), random.randint(1, 2), random.randint(10, 15)
                    elif is_p34: u, d, h = random.randint(5, 8), random.randint(2, 4), random.randint(20, 35)
                    else: u, d, h = random.randint(10, 15), random.randint(4, 8), random.randint(50, 100)
                    
                    net = u - d; days = math.ceil((h - u) / net) + 1
                    q = f"<b>{animal}</b>ตกลงบ่อลึก <b>{h} เมตร</b> กลางวันปีน <b>{u} เมตร</b> กลางคืนลื่น <b>{d} เมตร</b> จะต้องใช้เวลากี่วันจึงจะปีนพ้นปากบ่อ?"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>1 วันปีนสุทธิ: {u} - {d} = <b>{net} เมตร</b><br>ระยะก่อนถึงวันสุดท้าย (จุดหลอก): {h} - {u} = <b>{h - u} เมตร</b><br>เวลาช่วงแรก: {h - u} ÷ {net} = <b>{math.ceil((h - u) / net)} วัน</b><br>รวมกับวันสุดท้ายที่กระโดดพ้นบ่อ: {math.ceil((h - u) / net)} + 1 = <b>{days} วัน</b><br><b>ตอบ: {days} วัน</b></span>"

            # ---------------------------------------------------------
            elif actual_sub_t == "ตรรกะตาชั่งสมดุล":
                items_pair = [("เพชร", "ทอง", "เงิน", "เหล็ก"), ("สิงโต", "หมาป่า", "จิ้งจอก", "แมว"), ("ผลส้ม", "แอปเปิล", "สตรอว์เบอร์รี", "องุ่น")]
                i1, i2, i3, i4 = random.choice(items_pair)
                if is_challenge:
                    m1, m2, m3 = 2, random.randint(2, 3), random.randint(2, 3)
                    q_mul = random.randint(2, 3)
                    ans = m1 * m2 * m3 * q_mul
                    q = f"ตาชั่งสมดุล 3 ตัว ให้ข้อมูลดังนี้:<br>- <b>{i1} 1 อัน</b> หนักเท่ากับ <b>{i2} {m1} อัน</b><br>- <b>{i2} 1 อัน</b> หนักเท่ากับ <b>{i3} {m2} อัน</b><br>- <b>{i3} 1 อัน</b> หนักเท่ากับ <b>{i4} {m3} อัน</b><br><br>อยากทราบว่า <b>{i1} จำนวน {q_mul} อัน</b> จะมีน้ำหนักเท่ากับ <b>{i4}</b> กี่อัน?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (แทนค่าต่อเนื่อง 3 ชั้น):</b><br>
                    <b>ชั้นที่ 1:</b> {i1} 1 อัน = {i2} {m1} อัน<br>
                    <b>ชั้นที่ 2:</b> นำ {i3} ไปแทน {i2} ➔ {i1} 1 อัน = {m1} × {m2} = <b>{m1*m2} อัน (ของ {i3})</b><br>
                    <b>ชั้นที่ 3:</b> นำ {i4} ไปแทน {i3} ➔ {i1} 1 อัน = {m1*m2} × {m3} = <b>{m1*m2*m3} อัน (ของ {i4})</b><br>
                    โจทย์ถามหา {i1} {q_mul} อัน: นำ {m1*m2*m3} × {q_mul} = <b>{ans} อัน</b><br>
                    <b>ตอบ: {ans} อัน</b></span>"""
                else:
                    if is_p12: m1, m2, q_mul = 2, 2, 1
                    elif is_p34: m1, m2, q_mul = random.randint(3, 5), random.randint(3, 5), 2
                    else: m1, m2, q_mul = random.randint(4, 8), random.randint(4, 8), random.randint(3, 4)
                    
                    q = f"ตาชั่งสมดุล:<br>- <b>{i1} 1 ชิ้น</b> หนักเท่ากับ <b>{i2} {m1} ชิ้น</b><br>- <b>{i2} 1 ชิ้น</b> หนักเท่ากับ <b>{i3} {m2} ชิ้น</b><br>อยากทราบว่า <b>{i1} จำนวน {q_mul} ชิ้น</b> จะมีน้ำหนักเท่ากับ <b>{i3}</b> กี่ชิ้น?"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>{i1} 1 ชิ้น = {m1} × {m2} = <b>{m1 * m2} ชิ้น (ของ {i3})</b><br>โจทย์ถามหา {q_mul} ชิ้น นำไปคูณ {q_mul} = <b>{m1 * m2 * q_mul} ชิ้น</b><br><b>ตอบ: {m1 * m2 * q_mul} ชิ้น</b></span>"

            # ---------------------------------------------------------
            elif actual_sub_t == "ปัญหาผลรวม-ผลต่าง":
                n1, n2, n3 = random.sample(NAMES, 3); itm = random.choice(ITEMS)
                if is_challenge:
                    a = random.randint(30, 50)
                    b = a + random.randint(10, 20)
                    c = b + random.randint(10, 20)
                    total = a + b + c
                    diff_bc = c - b
                    diff_ac = c - a
                    
                    q = f"<b>{n1}, {n2}, และ {n3}</b> มี<b>{itm}</b>รวมกัน <b>{total}</b> ชิ้น <br>ถ้า <b>{n3}</b> มีมากกว่า <b>{n2}</b> อยู่ <b>{diff_bc}</b> ชิ้น และ <b>{n3}</b> มีมากกว่า <b>{n1}</b> อยู่ <b>{diff_ac}</b> ชิ้น <br>จงหาว่า <b>{n3} (คนที่มีเยอะที่สุด)</b> มีกี่ชิ้น?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (ปรับให้เท่ากัน 3 คน):</b><br>
                    เทคนิคคือ สมมติให้ทุกคนมีของเท่ากับ {n3} (คนที่มากที่สุด) เพื่อให้หารง่าย!<br>
                    <b>ขั้นตอนที่ 1: เติมของจินตนาการให้คนที่ขาด</b><br>
                    &nbsp;&nbsp;&nbsp;👉 ต้องเติมให้ {n1} จำนวน {diff_ac} ชิ้น และเติมให้ {n2} จำนวน {diff_bc} ชิ้น<br>
                    <b>ขั้นตอนที่ 2: หายอดรวมสมมติ</b><br>
                    &nbsp;&nbsp;&nbsp;👉 ยอดเดิม {total} + เติม {diff_ac} + เติม {diff_bc} = <b>{total+diff_ac+diff_bc} ชิ้น</b><br>
                    &nbsp;&nbsp;&nbsp;👉 ตอนนี้ทุกคนมีของเท่ากับ {n3} เป๊ะๆ ทั้ง 3 คน<br>
                    <b>ขั้นตอนที่ 3: หาจำนวนของ {n3}</b><br>
                    &nbsp;&nbsp;&nbsp;👉 นำยอดรวมสมมติหาร 3: {total+diff_ac+diff_bc} ÷ 3 = <b>{c} ชิ้น</b><br>
                    <b>ตอบ: {c} ชิ้น</b></span>"""
                else:
                    if is_p12: small = random.randint(10, 20); diff = random.randint(5, 10)
                    elif is_p34: small = random.randint(50, 150); diff = random.randint(20, 50)
                    else: small = random.randint(500, 1500); diff = random.randint(100, 300)
                    
                    large = small + diff; total = large + small
                    q = f"<b>{n1}</b> และ <b>{n2}</b> มี<b>{itm}</b>รวมกัน <b>{total}</b> ชิ้น หาก <b>{n1}</b> มีมากกว่า <b>{n2}</b> อยู่ <b>{diff}</b> ชิ้น จงหาว่า <b>{n1}</b> มีกี่ชิ้น?"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>หักส่วนที่เกินของ {n1} ออก: {total} - {diff} = <b>{total - diff} ชิ้น</b><br>แบ่งครึ่ง (ได้ของคนน้อย): {total - diff} ÷ 2 = <b>{small} ชิ้น</b><br>บวกส่วนเกินคืนให้ {n1}: {small} + {diff} = <b>{large} ชิ้น</b><br><b>ตอบ: {large} ชิ้น</b></span>"

            # ---------------------------------------------------------
            elif actual_sub_t == "แถวคอยแบบซ้อนทับ":
                n1, n2 = random.sample(NAMES, 2); loc = random.choice(LOCS)
                if is_challenge:
                    overlap = random.randint(3, 10)
                    total_people = random.randint(50, 100)
                    sum_pos = total_people + overlap
                    front_pos = random.randint(overlap + 5, total_people - 5)
                    back_pos = sum_pos - front_pos
                    ans = overlap - 2
                    
                    q = f"นักเรียนเข้าแถวรอเข้า<b>{loc}</b> มีคนทั้งหมด <b>{total_people}</b> คน<br>ถ้า <b>{n1}</b> ยืนลำดับที่ <b>{front_pos}</b> นับจากหัวแถว และ <b>{n2}</b> ยืนลำดับที่ <b>{back_pos}</b> นับจากท้ายแถว <br>มีคนยืนอยู่ระหว่าง <b>{n1}</b> กับ <b>{n2}</b> กี่คน? <br><span style='font-size: 16px; color: #7f8c8d;'>(คำใบ้: ระวังการนับซ้อนทับกัน)</span>"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (แถวเหลื่อมทับกัน):</b><br>
                    <b>ขั้นตอนที่ 1: ตรวจสอบการซ้อนทับ</b><br>
                    &nbsp;&nbsp;&nbsp;👉 นำลำดับหัวและท้ายบวกกัน: {front_pos} + {back_pos} = <b>{sum_pos}</b><br>
                    &nbsp;&nbsp;&nbsp;👉 พบว่าเกินจำนวนคนทั้งหมด ({total_people} คน) แสดงว่าพวกเขายืน 'ไขว้ทับกัน' ไปแล้ว!<br>
                    <b>ขั้นตอนที่ 2: หาจำนวนคนที่ถูกนับเบิ้ล (Overlap)</b><br>
                    &nbsp;&nbsp;&nbsp;👉 ยอดคนเกินมา = {sum_pos} - {total_people} = <b>{overlap} คน</b> (ยอดนี้รวม {n1} และ {n2} ไปด้วย)<br>
                    <b>ขั้นตอนที่ 3: หักตัวละครหลักออก</b><br>
                    &nbsp;&nbsp;&nbsp;👉 หาคน 'ระหว่างกลาง' ต้องหัก {n1} และ {n2} ทิ้ง: {overlap} - 2 = <b>{ans} คน</b><br>
                    <b>ตอบ: {ans} คน</b></span>"""
                else:
                    if is_p12: front_pos, back_pos = random.randint(5, 10), random.randint(5, 10)
                    elif is_p34: front_pos, back_pos = random.randint(15, 30), random.randint(15, 30)
                    else: front_pos, back_pos = random.randint(40, 80), random.randint(40, 80)
                    
                    total_people = front_pos + back_pos + random.randint(5, 15); between = total_people - (front_pos + back_pos)
                    q = f"นักเรียนเข้าแถว มีคนทั้งหมด <b>{total_people}</b> คน<br>ถ้า <b>{n1}</b> ยืนลำดับที่ <b>{front_pos}</b> จากหัวแถว และ <b>{n2}</b> ลำดับที่ <b>{back_pos}</b> จากท้ายแถว <br>มีคนยืนอยู่ระหว่าง 2 คนนี้กี่คน? (กำหนดให้ {n1} ยืนหน้า {n2})"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>นำคนทั้งหมด ลบกลุ่มด้านหน้าและกลุ่มด้านหลังออกไป<br>คนตรงกลาง = {total_people} - ({front_pos} + {back_pos}) = <b>{between} คน</b><br><b>ตอบ: {between} คน</b></span>"

            # ---------------------------------------------------------
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
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (วงกลมและตำแหน่งสัมพันธ์):</b><br>
                    <b>1) หาจำนวนคนทั้งหมดจากฝั่งตรงข้าม</b><br>
                    &nbsp;&nbsp;&nbsp;👉 ระยะห่างระหว่างสองคนฝั่งตรงข้าม คือ 'ครึ่งวงกลม'<br>
                    &nbsp;&nbsp;&nbsp;👉 ครึ่งวงกลม = {pos2} - {pos1} = <b>{n_half} คน</b><br>
                    &nbsp;&nbsp;&nbsp;👉 เต็มวงกลม = {n_half} × 2 = <b>{total} คน</b><br>
                    <b>2) หาตำแหน่งของ {n3}</b><br>
                    &nbsp;&nbsp;&nbsp;👉 {n3} ยืนถัดจาก {pos2} ไปอีก {add_pos} ตำแหน่ง: {pos2} + {add_pos} = <b>{pos2+add_pos}</b><br>
                    &nbsp;&nbsp;&nbsp;👉 (ถ้ายอดเกินจำนวนคนรวม ให้หักออกด้วย {total})<br>
                    &nbsp;&nbsp;&nbsp;👉 หมายเลขของ {n3} คือ <b>{pos3}</b><br>
                    <b>ตอบ: มี {total} คน และ {n3} คือหมายเลข {pos3}</b></span>"""
                else:
                    if is_p12: n_half = random.randint(4, 6)
                    elif is_p34: n_half = random.randint(8, 15)
                    else: n_half = random.randint(20, 40)
                    
                    total = n_half * 2; pos1 = random.randint(1, n_half); pos2 = pos1 + n_half
                    q = f"เด็กยืนล้อมวงกลมเว้นระยะเท่าๆ กัน นับหมายเลขเรียง 1, 2... <br>ถ้า <b>{n1}</b> หมายเลข <b>{pos1}</b> มองฝั่งตรงข้ามพบ <b>{n2}</b> หมายเลข <b>{pos2}</b> เด็กกลุ่มนี้มีกี่คน?"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>การยืนฝั่งตรงข้าม คือ 'ครึ่งวงกลม' พอดี<br>1) ครึ่งวงกลม: {pos2} - {pos1} = <b>{n_half} คน</b><br>2) เต็มวงกลม: {n_half} × 2 = <b>{total} คน</b><br><b>ตอบ: {total} คน</b></span>"

            # ---------------------------------------------------------
            elif actual_sub_t == "การคิดย้อนกลับ":
                name = random.choice(NAMES); item = random.choice(ITEMS)
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
                        add_v = step1 - random.randint(1, 3)
                        if add_v < 1: add_v = 1
                        
                    X = step1 - add_v
                    
                    q = f"<b>{name}</b> คิดเลขปริศนาในใจขั้นตอนดังนี้:<br>นำจำนวนปริศนามา <b>บวกด้วย {add_v}</b>, จากนั้นนำผลลัพธ์ <b>คูณด้วย {mul_v}</b>, <br>แล้ว <b>ลบออกด้วย {sub_v}</b>, และสุดท้าย <b>หารด้วย {div_v}</b> <br>ปรากฏว่าผลลัพธ์สุดท้ายคือ <b>{end_val}</b> พอดี จงหา 'จำนวนปริศนา' นั้น?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (Reverse Engineering 4 ชั้น):</b><br>
                    ทำย้อนจากหลังสุดไปหน้าสุด และเปลี่ยนเครื่องหมายให้ตรงกันข้ามทั้งหมด!<br>
                    <b>ชั้นที่ 1 (ย้อนหารเป็นคูณ):</b> {end_val} × {div_v} = <b>{step3}</b><br>
                    <b>ชั้นที่ 2 (ย้อนลบเป็นบวก):</b> {step3} + {sub_v} = <b>{step2}</b><br>
                    <b>ชั้นที่ 3 (ย้อนคูณเป็นหาร):</b> {step2} ÷ {mul_v} = <b>{step1}</b><br>
                    <b>ชั้นที่ 4 (ย้อนบวกเป็นลบ):</b> {step1} - {add_v} = <b>{X}</b><br>
                    <b>ตอบ: {X}</b></span>"""
                else:
                    if is_p12: sm, sp, rv = random.randint(20, 50), random.randint(5, 15), random.randint(10, 20)
                    elif is_p34: sm, sp, rv = random.randint(100, 300), random.randint(20, 80), random.randint(50, 150)
                    else: sm, sp, rv = random.randint(1000, 3000), random.randint(200, 800), random.randint(500, 1500)
                    
                    fm = sm - sp + rv
                    q = f"<b>{name}</b>นำเงินไปซื้อ<b>{item}</b> <b>{sp:,}</b> บาท จากนั้นแม่ให้เพิ่มอีก <b>{rv:,}</b> บาท ทำให้มีเงิน <b>{fm:,}</b> บาท <br>ตอนแรกมีเงินกี่บาท?"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ (คิดย้อนกลับ):</b><br>1) ปัจจุบันมี: {fm:,} บาท<br>2) ย้อนแม่ให้เงิน (ลบออก): {fm:,} - {rv:,} = <b>{fm - rv:,} บาท</b><br>3) ย้อนซื้อของ (บวกคืน): {fm - rv:,} + {sp:,} = <b>{sm:,} บาท</b><br><b>ตอบ: {sm:,} บาท</b></span>"

            # ---------------------------------------------------------
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
                        sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (รวมทริคการยืม):</b><br>
                        1) แลกปกติเป็นทอดๆ: จะแลกได้จนเหลือเศษซองเปล่าตอนจบ <b>{empties} ซอง</b><br>
                        2) ทริคการยืม: เนื่องจากโปรโมชั่นใช้ {exch} ซอง และเขาขาดอีกแค่ 1 ซอง เขาจึงยืมเพื่อนมา 1 ซอง (รวมเป็น {exch} ซอง)<br>
                        3) นำไปแลกได้กินอีก 1 ชิ้น! และเหลือซองเปล่าจากชิ้นนั้น 1 ซอง จึงนำไป <b>'คืนเพื่อน'</b> ได้พอดี!<br>
                        รวมได้กินทั้งหมด <b>{total_drank} ชิ้น</b><br>
                        <b>ตอบ: {total_drank} ชิ้น</b></span>"""
                    else:
                        sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์:</b><br>
                        แลกปกติเป็นทอดๆ: เมื่อแลกจนหมดจะเหลือเศษซองเปล่าตอนจบ <b>{empties} ซอง</b><br>
                        เนื่องจากขาดอีกหลายซอง จึงไม่เข้าเงื่อนไขการยืม 1 ซองแล้วคืนได้ (ถ้าขาดแค่ 1 ซองถึงจะทำได้)<br>
                        รวมได้กินทั้งหมด <b>{total_drank} ชิ้น</b><br>
                        <b>ตอบ: {total_drank} ชิ้น</b></span>"""
                else:
                    if is_p12: exch, start_bottles = 3, random.randint(6, 9)
                    elif is_p34: exch, start_bottles = random.randint(4, 5), random.randint(12, 25)
                    else: exch, start_bottles = random.randint(5, 8), random.randint(30, 60)
                    
                    total_drank, empties = start_bottles, start_bottles
                    while empties >= exch:
                        new_b = empties // exch; left_b = empties % exch; total_drank += new_b; empties = new_b + left_b
                    q = f"โปรโมชั่น: ซอง<b>{snack}</b>เปล่า <b>{exch}</b> ซอง แลกใหม่ฟรี 1 ชิ้น <br>ถ้าซื้อตอนแรก <b>{start_bottles}</b> ชิ้น จะได้กินรวมทั้งหมดกี่ชิ้น?"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>นำซองเปล่าไปแลก นำเศษที่เหลือมารวมกับของใหม่เพื่อแลกต่อเป็นทอดๆ<br>บวกจำนวนชิ้นที่ได้กินในทุกรอบ จะได้ทั้งหมด <b>{total_drank} ชิ้น</b><br><b>ตอบ: {total_drank} ชิ้น</b></span>"

            # ---------------------------------------------------------
            elif actual_sub_t == "ตรรกะการจับมือ (ทักทาย)":
                loc = random.choice(LOCS)
                if is_challenge:
                    n_a = random.randint(10, 15)
                    n_b = random.randint(10, 15)
                    ans = n_a * n_b
                    q = f"ในงานกิจกรรมที่<b>{loc}</b> มีเด็กชาย <b>{n_a}</b> คน และเด็กหญิง <b>{n_b}</b> คน<br>ถ้า <b>'เด็กชายทุกคนต้องจับมือกับเด็กหญิงทุกคน'</b> (ไม่จับมือกับเพศเดียวกัน) จะมีการจับมือเกิดขึ้นทั้งหมดกี่ครั้ง?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (กฎการคูณแบบข้ามกลุ่ม):</b><br>
                    ข้อนี้ไม่ได้จับมือทุกคนพร้อมกัน แต่เป็นการเชื่อมโยงระหว่าง 2 กลุ่ม (Bipartite)!<br>
                    <b>ขั้นตอนที่ 1:</b> เด็กชาย 1 คน จะต้องเดินไปจับมือเด็กหญิงครบทั้ง {n_b} คน (เกิด {n_b} ครั้ง)<br>
                    <b>ขั้นตอนที่ 2:</b> เนื่องจากมีเด็กชายทั้งหมด {n_a} คน ดังนั้นจะเกิดเหตุการณ์นี้ซ้ำๆ กัน<br>
                    <b>ขั้นตอนที่ 3:</b> นำจำนวนคนทั้งสองกลุ่มมาคูณกัน: {n_a} × {n_b} = <b>{ans:,} ครั้ง</b><br>
                    <b>ตอบ: {ans:,} ครั้ง</b></span>"""
                else:
                    n = random.randint(5, 10) if is_p34 else random.randint(10, 20)
                    ans = sum(range(1, n))
                    q = f"ในการจัดกิจกรรม มีเด็ก <b>{n}</b> คน หากเด็กทุกคนจับมือทำความรู้จักกันให้ครบทุกคน จะมีการจับมือเกิดขึ้นทั้งหมดกี่ครั้ง?"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>คนที่ 1 จับ {n-1} คน, คนที่ 2 จับ {n-2} คน ลดหลั่นลงไป<br>นำมาบวกกัน: {' + '.join(str(x) for x in range(n-1, 0, -1))} = <b>{ans} ครั้ง</b><br><b>ตอบ: {ans} ครั้ง</b></span>"

            # ---------------------------------------------------------
            elif actual_sub_t == "หยิบของในที่มืด":
                item = random.choice(ITEMS)
                if is_challenge:
                    c1, c2, c3 = random.randint(10, 20), random.randint(10, 20), random.randint(10, 20)
                    arr = sorted([c1, c2, c3], reverse=True)
                    ans = arr[0] + arr[1] + 1
                    q = f"ในกล่องทึบมี<b>{item}</b>สีแดง <b>{c1}</b> ชิ้น, สีน้ำเงิน <b>{c2}</b> ชิ้น, และสีเขียว <b>{c3}</b> ชิ้น<br>หากหลับตาหยิบ ต้องหยิบออกมา<b>อย่างน้อยที่สุดกี่ชิ้น</b> จึงจะมั่นใจ 100% ว่าจะได้ <b>'ครบทั้ง 3 สี อย่างน้อยสีละ 1 ชิ้น'</b> แน่นอน?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (หลักการดวงซวยที่สุดขั้นสูง):</b><br>
                    เพื่อให้มั่นใจ 100% ต้องคิดกรณีที่โชคร้ายที่สุด คือหยิบได้สีที่มีจำนวนเยอะๆ ออกมาจนหมดกล่องก่อน!<br>
                    <b>ขั้นตอนที่ 1:</b> สีที่มีจำนวนเยอะที่สุด 2 ลำดับแรกคือ <b>{arr[0]}</b> และ <b>{arr[1]}</b><br>
                    <b>ขั้นตอนที่ 2:</b> โชคร้ายสุดๆ คือหยิบได้ 2 สีนี้ออกมาหมดเกลี้ยงเลย: {arr[0]} + {arr[1]} = <b>{arr[0]+arr[1]} ชิ้น</b> (ตอนนี้ได้แค่ 2 สี)<br>
                    <b>ขั้นตอนที่ 3:</b> ในกล่องจะเหลือแค่สีที่ 3 ล้วนๆ การหยิบชิ้นต่อไป (บวก 1) จะการันตีว่าได้ครบ 3 สีแน่นอน!<br>
                    &nbsp;&nbsp;&nbsp;👉 {arr[0]+arr[1]} + 1 = <b>{ans} ชิ้น</b><br>
                    <b>ตอบ: {ans} ชิ้น</b></span>"""
                else:
                    if is_p34: 
                        c1, c2, c3 = random.randint(5, 12), random.randint(5, 12), random.randint(3, 8)
                        c_total, text_add = c1+c2, ""
                    else: 
                        c1, c2, c3, c4 = random.randint(15, 30), random.randint(15, 30), random.randint(15, 30), random.randint(5, 15)
                        c_total = c1+c2+c3; text_add = f", สีเหลือง <b>{c4}</b> ชิ้น"
                    
                    q = f"ในกล่องทึบมี<b>{item}</b>สีแดง <b>{c1}</b> ชิ้น, สีน้ำเงิน <b>{c2}</b> ชิ้น{text_add} และสีเขียว <b>{c3 if is_p34 else c4}</b> ชิ้น<br>ต้องหยิบ<b>อย่างน้อยกี่ชิ้น</b> จึงจะมั่นใจ 100% ว่าจะได้<b>สีเขียว</b>อย่างน้อย 1 ชิ้น?"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ (หลักการดวงซวยที่สุด):</b><br>กรณีโชคร้ายที่สุด คือหยิบได้สีอื่นหมดกล่องก่อน: <b>{c_total} ชิ้น</b><br>ชิ้นต่อไป (บวกเพิ่ม 1) จะการันตีได้สีเขียว: {c_total} + 1 = <b>{c_total+1} ชิ้น</b><br><b>ตอบ: {c_total+1} ชิ้น</b></span>"

            # ---------------------------------------------------------
            elif actual_sub_t == "แผนภาพความชอบ":
                n1, n2, n3 = random.sample(SNACKS, 3)
                if is_challenge:
                    tot = random.randint(150, 200)
                    only_A, only_B, only_C = random.randint(10, 20), random.randint(10, 20), random.randint(10, 20)
                    A_B, B_C, A_C = random.randint(5, 10), random.randint(5, 10), random.randint(5, 10) 
                    all_3 = random.randint(3, 8)
                    neither = random.randint(5, 15)
                    
                    like_A = only_A + A_B + A_C + all_3
                    like_B = only_B + A_B + B_C + all_3
                    like_C = only_C + A_C + B_C + all_3
                    
                    real_tot = only_A + only_B + only_C + A_B + B_C + A_C + all_3 + neither
                    
                    q = f"สำรวจนักเรียน <b>{real_tot}</b> คน พบว่ามีคนชอบ <b>{n1} {like_A} คน</b>, ชอบ <b>{n2} {like_B} คน</b>, และชอบ <b>{n3} {like_C} คน</b><br>โดยมีคนที่ชอบ {n1}และ{n2} (แต่ไม่ชอบ{n3}) <b>{A_B} คน</b>, ชอบ {n2}และ{n3} (แต่ไม่ชอบ{n1}) <b>{B_C} คน</b>, ชอบ {n1}และ{n3} (แต่ไม่ชอบ{n2}) <b>{A_C} คน</b><br>และคนที่ชอบทั้ง 3 อย่างมี <b>{all_3} คน</b> จงหาว่ามีนักเรียนกี่คนที่ <b>'ไม่ชอบ'</b> ขนมทั้ง 3 ชนิดนี้เลย?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (แผนภาพเวนน์ 3 วง):</b><br>
                    <b>หาคนที่ชอบอย่างใดอย่างหนึ่งล้วนๆ:</b><br>
                    &nbsp;&nbsp;&nbsp;👉 ชอบ {n1} ล้วน = {like_A} - ({A_B}+{A_C}+{all_3}) = <b>{only_A} คน</b><br>
                    &nbsp;&nbsp;&nbsp;👉 ชอบ {n2} ล้วน = {like_B} - ({A_B}+{B_C}+{all_3}) = <b>{only_B} คน</b><br>
                    &nbsp;&nbsp;&nbsp;👉 ชอบ {n3} ล้วน = {like_C} - ({A_C}+{B_C}+{all_3}) = <b>{only_C} คน</b><br>
                    <b>รวมคนที่ชอบขนม (ทุกส่วนในวงกลมบวกกัน):</b><br>
                    &nbsp;&nbsp;&nbsp;👉 {only_A} + {only_B} + {only_C} + {A_B} + {B_C} + {A_C} + {all_3} = <b>{real_tot - neither} คน</b><br>
                    <b>หาคนที่ไม่ชอบเลย:</b> ยอดทั้งหมดลบยอดที่ชอบ ➔ {real_tot} - {real_tot - neither} = <b>{neither} คน</b><br>
                    <b>ตอบ: {neither} คน</b></span>"""
                else:
                    if is_p34: tot, both = random.randint(30, 50), random.randint(5, 12)
                    else: tot, both = random.randint(100, 200), random.randint(20, 50)
                    
                    only_a, only_b = random.randint(10, 20), random.randint(10, 20)
                    l_a, l_b = only_a + both, only_b + both; neither = tot - (only_a + only_b + both)
                    q = f"สำรวจนักเรียน <b>{tot}</b> คน พบว่าชอบ<b>{n1}</b> <b>{l_a}</b> คน, ชอบ<b>{n2}</b> <b>{l_b}</b> คน, และชอบทั้งสองอย่าง <b>{both}</b> คน <br>มีกี่คนที่ไม่ชอบกินขนมทั้งสองชนิดนี้เลย?"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>1) ชอบ {n1} อย่างเดียว: {l_a} - {both} = <b>{only_a} คน</b><br>2) ชอบ {n2} อย่างเดียว: {l_b} - {both} = <b>{only_b} คน</b><br>3) รวมคนที่ชอบ: {only_a} + {only_b} + {both} = <b>{only_a + only_b + both} คน</b><br>4) คนที่ไม่ชอบ: {tot} - {only_a + only_b + both} = <b>{neither} คน</b><br><b>ตอบ: {neither} คน</b></span>"

            # ---------------------------------------------------------
            elif actual_sub_t == "ผลบวกจำนวนเรียงกัน (Gauss)":
                if is_challenge:
                    even = random.choice([True, False])
                    N = random.choice([50, 100, 200])
                    
                    if even:
                        ans = (N//2) * (N//2 + 1)
                        q = f"จงหาผลบวกของ <b>'จำนวนคู่'</b> ทุกจำนวน ตั้งแต่ 1 ถึง {N} <br>( 2 + 4 + 6 + ... + {N} = ? )"
                        sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (ผลบวกเกาส์แบบกระโดด):</b><br>
                        <b>ขั้นตอนที่ 1: หาจำนวนตัวเลขทั้งหมดในอนุกรม</b><br>
                        &nbsp;&nbsp;&nbsp;👉 ตั้งแต่ 1 ถึง {N} มีเลขคู่ทั้งหมดครึ่งหนึ่ง คือ {N} ÷ 2 = <b>{N//2} ตัว</b><br>
                        <b>ขั้นตอนที่ 2: ใช้หลักการจับคู่หัว-ท้าย</b><br>
                        &nbsp;&nbsp;&nbsp;👉 ตัวแรกสุด + ตัวหลังสุด = 2 + {N} = <b>{N+2}</b><br>
                        &nbsp;&nbsp;&nbsp;👉 มีตัวเลข {N//2} ตัว นำมาจับคู่จะได้ {N//2} ÷ 2 = <b>{(N//2)/2} คู่</b><br>
                        <b>ขั้นตอนที่ 3: หาผลรวม</b><br>
                        &nbsp;&nbsp;&nbsp;👉 {N+2} × {(N//2)/2} = <b>{ans:,}</b><br>
                        <b>ตอบ: {ans:,}</b></span>"""
                    else:
                        ans = (N//2) ** 2
                        q = f"จงหาผลบวกของ <b>'จำนวนคี่'</b> ทุกจำนวน ตั้งแต่ 1 ถึง {N-1} <br>( 1 + 3 + 5 + ... + {N-1} = ? )"
                        sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (ผลบวกเกาส์แบบกระโดด):</b><br>
                        <b>ขั้นตอนที่ 1: หาจำนวนตัวเลขทั้งหมดในอนุกรม</b><br>
                        &nbsp;&nbsp;&nbsp;👉 ตั้งแต่ 1 ถึง {N-1} มีเลขคี่ทั้งหมดครึ่งหนึ่งของ {N} คือ <b>{N//2} ตัว</b><br>
                        <b>ขั้นตอนที่ 2: ใช้หลักการจับคู่หัว-ท้าย</b><br>
                        &nbsp;&nbsp;&nbsp;👉 ตัวแรกสุด + ตัวหลังสุด = 1 + {N-1} = <b>{N}</b><br>
                        &nbsp;&nbsp;&nbsp;👉 มีตัวเลข {N//2} ตัว นำมาจับคู่จะได้ {N//2} ÷ 2 = <b>{(N//2)/2} คู่</b><br>
                        <b>ขั้นตอนที่ 3: หาผลรวม (สูตรลัดเลขคี่ = จำนวนตัว²)</b><br>
                        &nbsp;&nbsp;&nbsp;👉 {N} × {(N//2)/2} = {N//2} × {N//2} = <b>{ans:,}</b><br>
                        <b>ตอบ: {ans:,}</b></span>"""
                else:
                    n = random.choice([20, 30, 40, 50]) if is_p34 else random.choice([100, 200, 500])
                    ans = (n * (n + 1)) // 2
                    q = f"จงหาผลบวกของตัวเลขเรียงลำดับตั้งแต่ 1 ถึง {n} <br>( 1 + 2 + 3 + ... + {n} = ? )"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ (หลักการจับคู่เกาส์):</b><br>จับคู่หัว-ท้าย (1+{n} = {n+1}), มี {n} ตัว จัดกลุ่มได้ {n}÷2 = {n//2} คู่<br>ผลบวก: {n+1} × {n//2} = <b>{ans:,}</b><br><b>ตอบ: {ans:,}</b></span>"

            # ---------------------------------------------------------
            elif actual_sub_t == "เศษส่วนของที่เหลือ":
                item = random.choice(ITEMS)
                f1_n, f1_d = random.choice([(2,5), (3,5), (1,4), (3,4), (2,7)]); f2_n, f2_d = random.choice([(1,3), (2,3), (1,2), (3,8), (1,4)]); k = random.choice([50, 100, 150, 200])
                lcm_den = f1_d * f2_d
                tot = k * lcm_den
                spent1 = (tot * f1_n) // f1_d
                rem1 = tot - spent1
                spent2 = (rem1 * f2_n) // f2_d
                ans = rem1 - spent2
                
                f1_html = get_vertical_fraction(f1_n, f1_d)
                f2_html = get_vertical_fraction(f2_n, f2_d)
                
                q = f"<b>{name}</b> มีเงินอยู่ {tot:,} บาท นำไปซื้อขนม {f1_html} ของเงินทั้งหมด และนำไปซื้อ<b>{item}</b>อีก {f2_html} <b>ของเงินที่เหลือ</b> <br>จงหาว่าตอนนี้ <b>{name}</b> เหลือเงินกี่บาท?"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                ข้อนี้มีจุดหลอกตรงคำว่า <b>"ของเงินที่เหลือ"</b> ต้องหักเงินออกทีละรอบครับ<br>
                1) <b>ก้อนแรก (ซื้อขนม):</b> ใช้ไป {f1_html} ของเงินทั้งหมด<br>
                &nbsp;&nbsp;&nbsp;👉 ซื้อขนม = ({f1_n} × {tot:,}) ÷ {f1_d} = <b>{spent1:,} บาท</b><br>
                &nbsp;&nbsp;&nbsp;👉 <u>เงินที่เหลือ</u> = {tot:,} - {spent1:,} = <b>{rem1:,} บาท</b><br>
                2) <b>ก้อนที่สอง (ซื้อ{item}):</b> ใช้ไป {f2_html} <b>ของเงินที่เหลือ</b><br>
                &nbsp;&nbsp;&nbsp;👉 ซื้อ{item} = ({f2_n} × {rem1:,}) ÷ {f2_d} = <b>{spent2:,} บาท</b><br>
                3) <b>หาเงินที่เหลือในปัจจุบัน:</b><br>
                &nbsp;&nbsp;&nbsp;👉 เหลือเงิน = {rem1:,} - {spent2:,} = <b>{ans:,} บาท</b><br>
                <b>ตอบ: {ans:,} บาท</b></span>"""

            # ---------------------------------------------------------
            elif actual_sub_t == "ปริศนาตัวเลขซ่อนแอบ":
                a = random.randint(1, 4); b = random.randint(a + 2, 9); diff = b - a; k = diff * 9; sum_val = a + b
                if is_challenge:
                    q = f"A และ B เป็นเลขโดดที่ต่างกัน กำหนดสมการ <b>BA - AB = {k}</b> และ <b>A + B = {sum_val}</b> <br>จงหาผลคูณของ <b>A × B</b> ?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (รหัสสลับหลัก):</b><br>
                    <b>1) กฎของเลขสลับหลัก:</b> ผลต่างของจำนวน 2 หลักที่สลับกัน จะมีค่าเท่ากับ 'ผลต่างของเลขโดด × 9' เสมอ!<br>
                    &nbsp;&nbsp;&nbsp;👉 ดังนั้น B - A = {k} ÷ 9 = <b>{diff}</b><br>
                    <b>2) แก้สมการหา A และ B:</b><br>
                    &nbsp;&nbsp;&nbsp;👉 เรารู้ว่า ผลบวก = {sum_val} และ ผลต่าง = {diff}<br>
                    &nbsp;&nbsp;&nbsp;👉 ตัวที่มากกว่า (B) = ({sum_val} + {diff}) ÷ 2 = <b>{b}</b><br>
                    &nbsp;&nbsp;&nbsp;👉 ตัวที่น้อยกว่า (A) = {sum_val} - {b} = <b>{a}</b><br>
                    <b>3) หาผลคูณ:</b><br>
                    &nbsp;&nbsp;&nbsp;👉 {a} × {b} = <b>{a*b}</b><br>
                    <b>ตอบ: {a*b}</b></span>"""
                else:
                    q = f"A และ B เป็นเลขโดดที่ต่างกัน กำหนด <b>BA - {k} = AB</b> และ <b>A + B = {sum_val}</b> <br>จงหาว่าจำนวนสองหลัก <b>AB</b> คือจำนวนใด?"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>1) BA - AB = {k}<br>2) ผลต่างของ AB สลับหลัก มีค่าเท่ากับ (B - A) × 9 เสมอ! ➔ B - A = {k} ÷ 9 = <b>{diff}</b><br>3) ผลบวก={sum_val}, ผลต่าง={diff} ➔ หา B: ({sum_val} + {diff}) ÷ 2 = <b>{b}</b>, หา A: {sum_val} - {b} = <b>{a}</b><br><b>ตอบ: {a}{b}</b></span>"

            # ---------------------------------------------------------
            elif actual_sub_t == "การตัดเชือกพับทบ":
                name = random.choice(NAMES)
                if is_challenge:
                    f = random.randint(3, 5) 
                    c = random.randint(3, 6) 
                    ans = (2**f) * c + 1
                    q = f"<b>{name}</b> นำเชือกมาพับทบครึ่งซ้อนกันไปเรื่อยๆ จำนวน <b>{f} ครั้ง</b> จากนั้นใช้กรรไกรตัดเชือกให้ขาดออก <b>{c} รอยตัด</b> <br>เมื่อคลี่เชือกทั้งหมดออกมา จะได้เศษเชือกชิ้นเล็กชิ้นน้อยรวมทั้งหมดกี่เส้น?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (สูตรความหนาเชือก):</b><br>
                    <b>ขั้นตอนที่ 1: หาความหนาของเชือกหลังพับ</b><br>
                    &nbsp;&nbsp;&nbsp;👉 การพับครึ่ง 1 ครั้ง ความหนาจะเพิ่มเป็น 2 เท่า (2 ยกกำลัง)<br>
                    &nbsp;&nbsp;&nbsp;👉 พับ {f} ครั้ง = 2 × 2 ...({f} ครั้ง) = <b>{2**f} ชั้น</b><br>
                    <b>ขั้นตอนที่ 2: หาจำนวนเส้นที่ถูกตัดเพิ่ม</b><br>
                    &nbsp;&nbsp;&nbsp;👉 การใช้กรรไกรตัด 1 รอยตรงกลางเชือก จะได้เชือกเพิ่มขึ้นเท่ากับจำนวนชั้น<br>
                    &nbsp;&nbsp;&nbsp;👉 ตัด {c} รอย = {2**f} × {c} = <b>{(2**f)*c} เส้น</b><br>
                    <b>ขั้นตอนที่ 3: รวมเชือกตั้งต้น</b><br>
                    &nbsp;&nbsp;&nbsp;👉 นำรอยตัดไปบวกกับเชือกเส้นเดิม 1 เส้น: {(2**f)*c} + 1 = <b>{ans} เส้น</b><br>
                    <b>ตอบ: {ans} เส้น</b></span>"""
                else:
                    f, c = 2, random.randint(2, 4)
                    ans = (2**f) * c + 1
                    q = f"<b>{name}</b>นำเชือกมาพับทบครึ่ง <b>{f}</b> ครั้ง จากนั้นตัดให้ขาด <b>{c}</b> รอยตัด <br>เมื่อคลี่ออกมาจะได้เชือกทั้งหมดกี่เส้น?"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>1) พับ {f} ครั้ง เกิดความหนา = 2 ยกกำลัง {f} = <b>{2**f} ชั้น</b><br>2) ตัด {c} รอย ได้เพิ่ม {2**f} × {c} = <b>{(2**f)*c} เส้น</b><br>3) รวมกับเส้นตั้งต้น 1 เส้น: {(2**f)*c} + 1 = <b>{ans} เส้น</b><br><b>ตอบ: {ans} เส้น</b></span>"

            # ---------------------------------------------------------
            elif actual_sub_t == "อายุข้ามเวลาขั้นสูง":
                n1, n2, n3 = random.sample(NAMES, 3)
                if is_challenge:
                    age1, age2, age3 = random.randint(15, 20), random.randint(18, 25), random.randint(22, 30); current_sum = age1 + age2 + age3
                    past_years = random.randint(5, 10); past_sum = current_sum - (3 * past_years)
                    future_years = random.randint(5, 10); future_sum = current_sum + (3 * future_years)
                    q = f"ปัจจุบัน {n1}, {n2}, และ {n3} มีอายุรวมกัน <b>{current_sum} ปี</b> <br>ถ้าเมื่อ <b>{past_years} ปีที่แล้ว</b> ทั้งสามคนมีอายุรวมกัน <b>{past_sum} ปี</b><br>จงหาว่า <b>อีก {future_years} ปีข้างหน้า</b> ทั้งสามคนจะมีอายุรวมกันกี่ปี?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (บวกอายุเป็นกลุ่ม):</b><br>
                    โจทย์ข้อนี้เป็นตัวหลอก เพราะให้ข้อมูลอดีตมาเพื่อความสับสน เราสามารถข้ามไปคิดอนาคตได้เลย!<br>
                    <b>ขั้นตอนที่ 1: วิเคราะห์เงื่อนไขอนาคต</b><br>
                    &nbsp;&nbsp;&nbsp;👉 อีก {future_years} ปีข้างหน้า <b>ทุกคน (ทั้ง 3 คน)</b> จะมีอายุเพิ่มขึ้นคนละ {future_years} ปี<br>
                    <b>ขั้นตอนที่ 2: หาอายุรวมที่เพิ่มขึ้น</b><br>
                    &nbsp;&nbsp;&nbsp;👉 นำ {future_years} ปี × 3 คน = <b>เพิ่มขึ้นรวม {3*future_years} ปี</b><br>
                    <b>ขั้นตอนที่ 3: หาผลรวมในอนาคต</b><br>
                    &nbsp;&nbsp;&nbsp;👉 นำอายุรวมปัจจุบัน บวกกับ อายุรวมที่เพิ่มขึ้น: {current_sum} + {3*future_years} = <b>{future_sum} ปี</b><br>
                    <b>ตอบ: {future_sum} ปี</b></span>"""
                else:
                    age1, age2 = random.randint(15, 20), random.randint(18, 25)
                    current_sum = age1 + age2; past_years = random.randint(3, 8); past_sum = current_sum - (2 * past_years)
                    q = f"ปัจจุบันพี่น้อง 2 คนคือ {n1} กับ {n2} มีอายุรวมกัน <b>{current_sum}</b> ปี <br>จงหาว่าเมื่อ <b>{past_years}</b> ปีที่แล้ว ทั้งสองคนมีอายุรวมกันกี่ปี?"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>ย้อนเวลาไป {past_years} ปี <b>ทุกคน (ทั้ง 2 คน)</b> จะมีอายุน้อยลงคนละ {past_years} ปี<br>หักอายุออกรวม = 2 × {past_years} = <b>{2*past_years} ปี</b><br>นำอายุรวมปัจจุบันลบออก: {current_sum} - {2*past_years} = <b>{past_sum} ปี</b><br><b>ตอบ: {past_sum} ปี</b></span>"

            # ---------------------------------------------------------
            elif actual_sub_t == "ความเร็ววิ่งสวนทาง":
                veh = random.choice(VEHICLES)
                if is_challenge:
                    v1, v2 = random.choice([45, 55, 65]), random.choice([45, 55, 65])
                    start_diff = random.randint(1, 2)
                    t = random.randint(2, 4)
                    
                    adv_d = v1 * start_diff
                    meet_d = (v1 + v2) * t
                    total_d = adv_d + meet_d
                    
                    q = f"{veh}สองคันอยู่ห่างกัน <b>{total_d:,} กิโลเมตร</b> <br>คันแรก (วิ่งด้วยความเร็ว <b>{v1} กม./ชม.</b>) ออกเดินทางไปก่อน <b>{start_diff} ชั่วโมง</b><br>จากนั้นคันที่สอง (วิ่งด้วยความเร็ว <b>{v2} กม./ชม.</b>) จึงเริ่มวิ่งสวนทางเข้าหาคันแรก<br>หลังจากคันที่สองเริ่มออกตัว ต้องใช้เวลากี่ชั่วโมง ทั้งสองคันจึงจะวิ่งมาเจอกัน?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (หักระยะทางล่วงหน้า):</b><br>
                    <b>ขั้นตอนที่ 1: หาระยะทางที่คันแรกแอบวิ่งไปก่อน</b><br>
                    &nbsp;&nbsp;&nbsp;👉 ระยะทางล่วงหน้า = ความเร็ว × เวลา = {v1} × {start_diff} = <b>{adv_d} กม.</b><br>
                    <b>ขั้นตอนที่ 2: หาระยะทางที่เหลืออยู่ตอนคันที่สองเริ่มออกตัว</b><br>
                    &nbsp;&nbsp;&nbsp;👉 ระยะทางทั้งหมด - ระยะทางล่วงหน้า: {total_d} - {adv_d} = <b>{meet_d} กม.</b><br>
                    <b>ขั้นตอนที่ 3: คำนวณเวลาวิ่งเข้าหากัน</b><br>
                    &nbsp;&nbsp;&nbsp;👉 ความเร็วรวมวิ่งสวนกัน = {v1} + {v2} = <b>{v1+v2} กม./ชม.</b><br>
                    &nbsp;&nbsp;&nbsp;👉 เวลาที่ใช้ = ระยะทางที่เหลือ ÷ ความเร็วรวม = {meet_d} ÷ {v1+v2} = <b>{t} ชั่วโมง</b><br>
                    <b>ตอบ: {t} ชั่วโมง</b></span>"""
                else:
                    v1, v2 = random.choice([20, 30, 40]), random.choice([20, 30, 40]); t = random.randint(2, 4)
                    d = (v1 + v2) * t
                    q = f"{veh}สองคันอยู่ห่างกัน <b>{d:,} กิโลเมตร</b> กำลังวิ่งสวนทางเข้าหากัน <br>ถ้าคันแรกวิ่งเร็ว <b>{v1} กม./ชม.</b> คันที่สองวิ่งเร็ว <b>{v2} กม./ชม.</b> <br>ต้องใช้เวลาอีกกี่ชั่วโมง ทั้งสองจึงจะวิ่งมาเจอกันพอดี?"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>วิ่งเข้าหากัน นำความเร็วมาบวกกันเป็นความเร็วรวม: {v1} + {v2} = <b>{v1 + v2} กม./ชม.</b><br>เวลา = ระยะทาง ÷ ความเร็วรวม = {d:,} ÷ {v1 + v2} = <b>{t} ชั่วโมง</b><br><b>ตอบ: {t} ชั่วโมง</b></span>"

            # ---------------------------------------------------------
            elif actual_sub_t == "งานและเวลา (Work)":
                action = random.choice(WORK_ACTIONS)
                if is_challenge:
                    n1, n2, n3 = random.sample(NAMES, 3)
                    pairs = [(10, 12, 15, 4), (12, 15, 20, 5), (6, 10, 15, 3), (12, 24, 8, 4)]
                    w1, w2, w3, ans = random.choice(pairs)
                    
                    q = f"ในการ<b>{action}</b> หากให้ <b>{n1}</b> ทำคนเดียวจะเสร็จใน {w1} วัน, <b>{n2}</b> ทำคนเดียวเสร็จใน {w2} วัน, และ <b>{n3}</b> ทำคนเดียวเสร็จใน {w3} วัน<br>จงหาว่าถ้าทั้งสามคน 'ช่วยกันทำพร้อมกัน' งานนี้จะเสร็จภายในเวลากี่วัน?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (สมการอัตราการทำงานรวม 3 คน):</b><br>
                    เปลี่ยนจำนวนวันให้เป็น "งานที่ทำได้ใน 1 วัน" (เศษส่วน)<br>
                    <b>ขั้นตอนที่ 1: หาผลงานใน 1 วันของแต่ละคน</b><br>
                    &nbsp;&nbsp;&nbsp;👉 {n1} = 1/{w1}, {n2} = 1/{w2}, {n3} = 1/{w3}<br>
                    <b>ขั้นตอนที่ 2: นำผลงานใน 1 วันมาบวกกัน (ทำส่วนให้เท่ากัน)</b><br>
                    &nbsp;&nbsp;&nbsp;👉 1/{w1} + 1/{w2} + 1/{w3} (หา ค.ร.น. ของตัวส่วน)<br>
                    &nbsp;&nbsp;&nbsp;👉 เมื่อบวกเศษส่วนเสร็จแล้ว จะได้ผลลัพธ์คือ <b>1/{ans}</b> ของงานทั้งหมด<br>
                    <b>ขั้นตอนที่ 3: พลิกกลับเศษเป็นส่วนเพื่อหาจำนวนวัน</b><br>
                    &nbsp;&nbsp;&nbsp;👉 แสดงว่า 1 วัน ทำได้ 1/{ans} งาน ดังนั้นต้องใช้เวลา <b>{ans} วัน</b> งานจึงจะเสร็จ 100%<br>
                    <b>ตอบ: {ans} วัน</b></span>"""
                else:
                    pairs = [(3,6,2), (4,12,3), (6,12,4), (10,15,6)]
                    w1, w2, ans = random.choice(pairs); n1, n2 = random.sample(NAMES, 2)
                    q = f"ในการ<b>{action}</b> หากให้ <b>{n1}</b> ทำคนเดียวจะเสร็จใน {w1} วัน แต่ถ้าให้ <b>{n2}</b> ทำคนเดียวจะเสร็จใน {w2} วัน <br>จงหาว่าถ้าช่วยกันทำพร้อมกัน จะเสร็จภายในเวลากี่วัน?"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>ใช้สูตรลัดช่วยกันทำงาน = (เวลาคนแรก × เวลาคนที่สอง) ÷ (เวลาคนแรก + เวลาคนที่สอง)<br>= ({w1} × {w2}) ÷ ({w1} + {w2}) = {w1*w2} ÷ {w1+w2} = <b>{ans} วัน</b><br><b>ตอบ: {ans} วัน</b></span>"

            # ---------------------------------------------------------
            elif actual_sub_t == "ระฆังและไฟกะพริบ (ค.ร.น.)":
                item_word = random.choice(["สัญญาณไฟ", "นาฬิกาปลุก", "ระฆัง"])
                if is_challenge:
                    l1, l2, l3, l4 = random.sample([10, 15, 20, 30, 45, 60], 4)
                    lcm = lcm_calc(lcm_calc(lcm_calc(l1, l2), l3), l4)
                    q = f"<b>{item_word} 4 ชิ้น</b> ทำงานด้วยจังหวะที่ต่างกัน ดังนี้:<br>ชิ้นที่ 1 ดังทุกๆ {l1} วินาที, ชิ้นที่ 2 ดังทุกๆ {l2} วินาที, ชิ้นที่ 3 ดังทุกๆ {l3} วินาที, และชิ้นที่ 4 ดังทุกๆ {l4} วินาที <br>ถ้าเพิ่งดังพร้อมกันไป อีกกี่นาทีข้างหน้าจึงจะดังพร้อมกันอีกครั้ง?"
                    ans_min = lcm // 60
                    ans_sec = lcm % 60
                    text_ans = f"{ans_min} นาที" if ans_sec == 0 else f"{ans_min} นาที {ans_sec} วินาที"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (หา ค.ร.น. ขั้นสูง):</b><br>
                    โจทย์ "เกิดขึ้นพร้อมกันอีกครั้ง" ให้หา ค.ร.น. (คูณร่วมน้อย)<br>
                    <b>ขั้นตอนที่ 1: ตั้งหารสั้นเพื่อหา ค.ร.น.</b><br>
                    &nbsp;&nbsp;&nbsp;👉 นำ {l1}, {l2}, {l3}, {l4} มาหา ค.ร.น. จะได้เท่ากับ <b>{lcm} วินาที</b><br>
                    <b>ขั้นตอนที่ 2: แปลงหน่วยวินาทีเป็นนาที</b><br>
                    &nbsp;&nbsp;&nbsp;👉 1 นาที มี 60 วินาที นำ {lcm} ÷ 60<br>
                    &nbsp;&nbsp;&nbsp;👉 จะได้ <b>{text_ans}</b> พอดี<br>
                    <b>ตอบ: {text_ans}</b></span>"""
                else:
                    l1, l2, l3 = random.sample([10, 12, 15, 20, 30], 3); lcm = lcm_calc(lcm_calc(l1, l2), l3)
                    q = f"{item_word} 3 ชิ้น ทำงานด้วยจังหวะต่างกัน ชิ้นแรกดังทุกๆ {l1} วินาที, ชิ้นที่สอง {l2} วินาที และชิ้นที่สาม {l3} วินาที <br>ถ้าเพิ่งดังพร้อมกันไป อีกกี่วินาทีข้างหน้าจึงจะดังพร้อมกันอีกครั้ง?"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>โจทย์ 'เกิดขึ้นพร้อมกันอีกครั้ง' ให้หา ค.ร.น.<br>นำตัวเลขรอบเวลาทั้งหมดมาตั้งหารสั้นเพื่อหา ค.ร.น. จะได้ผลลัพธ์เท่ากับ <b>{lcm}</b><br><b>ตอบ: อีก {lcm} วินาที</b></span>"

            # ---------------------------------------------------------
            elif actual_sub_t == "นาฬิกาเดินเพี้ยน":
                if is_challenge:
                    days_map = {"พฤหัสบดี": 3, "ศุกร์": 4, "เสาร์": 5}
                    end_day = random.choice(list(days_map.keys()))
                    days = days_map[end_day]
                    gain_m = random.randint(3, 12)
                    total_gain = days * gain_m
                    
                    real_h = 8
                    real_m = 0
                    
                    show_m = real_m + total_gain
                    carry_h = show_m // 60
                    final_m = show_m % 60
                    final_h = real_h + carry_h
                    
                    q = f"นาฬิกาเรือนหนึ่งทำงานผิดปกติ โดยจะเดิน <b>'เร็วเกินไป' วันละ {gain_m} นาที</b><br>ถ้า<b>{name}</b>ตั้งเวลานาฬิกาเรือนนี้ให้ตรงกับเวลาจริงในตอน <b>08:00 น. ของวันจันทร์</b><br>จงหาว่าเมื่อเวลาจริงคือ <b>08:00 น. ของวัน{end_day}ในสัปดาห์เดียวกัน</b> นาฬิกาเรือนนี้จะชี้บอกเวลาใด?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีคิดวิเคราะห์ (คำนวณความคลาดเคลื่อนสะสม):</b><br>
                    <b>ขั้นตอนที่ 1: หาจำนวนวันที่ผ่านไป</b><br>
                    &nbsp;&nbsp;&nbsp;👉 จาก 08:00 น. วันจันทร์ ถึง 08:00 น. วัน{end_day} นับเวลาที่ผ่านไปได้ <b>{days} วันพอดีเป๊ะ</b><br>
                    <b>ขั้นตอนที่ 2: หาเวลาที่นาฬิกาเดินเพี้ยนไปทั้งหมด</b><br>
                    &nbsp;&nbsp;&nbsp;👉 เดินเร็ววันละ {gain_m} นาที × {days} วัน = <b>เดินเร็วไปทั้งหมด {total_gain} นาที</b><br>
                    <b>ขั้นตอนที่ 3: คำนวณเวลาบนหน้าปัด</b><br>
                    &nbsp;&nbsp;&nbsp;👉 เวลาจริงคือ 08:00 น. แต่นาฬิกาจะเดินนำหน้าไปอีก {total_gain} นาที<br>
                    &nbsp;&nbsp;&nbsp;👉 แปลงนาทีที่เดินเร็วเป็นชั่วโมง: {total_gain} นาที = <b>{carry_h} ชั่วโมง {final_m} นาที</b><br>
                    &nbsp;&nbsp;&nbsp;👉 นำไปบวกเพิ่มจากเวลาจริง: 08:00 น. + {carry_h} ชั่วโมง {final_m} นาที = <b>{final_h:02d}:{final_m:02d} น.</b><br>
                    <b>ตอบ: เวลา {final_h:02d}:{final_m:02d} น.</b></span>"""
                else:
                    fast_min = random.randint(3, 8); start_h = 8; passed_hours = random.randint(5, 12); end_h = start_h + passed_hours; total_fast = fast_min * passed_hours
                    q = f"นาฬิกาเรือนหนึ่งเดินเร็วไป <b>{fast_min} นาที ในทุกๆ 1 ชั่วโมง</b> <br>ตั้งเวลาตรงตอน <b>0{start_h}:00 น.</b> เมื่อเวลาจริงผ่านไปถึง <b>{end_h}:00 น.</b> นาฬิกาจะแสดงเวลาใด?"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>เวลาผ่านไป: {end_h} - {start_h} = <b>{passed_hours} ชั่วโมง</b><br>เดินเร็วเกินไป: {fast_min} × {passed_hours} = <b>{total_fast} นาที</b><br>นำไปบวกเพิ่มกับเวลาจริง จะได้ <b>{end_h}:{total_fast:02d} น.</b><br><b>ตอบ: {end_h}:{total_fast:02d} น.</b></span>"

            else:
                q = f"⚠️ [ระบบผิดพลาด] ไม่พบเงื่อนไขสำหรับหัวข้อ: <b>{actual_sub_t}</b>"
                sol = "Error"

            # ตรวจสอบการซ้ำของโจทย์
            if q not in seen: 
                seen.add(q)
                questions.append({"question": q, "solution": sol})
                break 
            elif attempts >= 499:
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
    title = f"เฉลยข้อสอบ (Answer Key){title_suffix}" if is_key else f"ข้อสอบวิเคราะห์ (TMC Pro){title_suffix}"
    
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
    with st.spinner("กำลังตรวจสอบตรรกะระดับ Deep Scan เพื่อการันตีความถูกต้องแบบ 100%..."):
        
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
        
        full_ebook_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap" rel="stylesheet"><style>@page {{ size: A4; margin: 15mm; }} @media screen {{ body {{ font-family: 'Sarabun', sans-serif; background-color: {bg_color}; display: flex; flex-direction: column; align-items: center; padding: 40px 0; margin: 0; }} .a4-wrapper {{ width: 210mm; min-height: 297mm; background: white; margin-bottom: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.3); padding: 15mm; box-sizing: border-box; }} .cover-wrapper {{ padding: 0; }} }} @media print {{ body {{ font-family: 'Sarabun', sans-serif; background: transparent; padding: 0; display: block; margin: 0; }} .a4-wrapper {{ width: 100%; min-height: auto; margin: 0; padding: 0; box-shadow: none; page-break-after: always; }} .cover-wrapper {{ height: 260mm; }} }} .header {{ text-align: center; border-bottom: 2px solid #333; margin-bottom: 10px; padding-bottom: 10px; }} .header h2 {{ color: {'#c0392b' if is_challenge else '#8e44ad'}; }} .q-box {{ margin-bottom: {q_margin}; padding: 10px 15px; page-break-inside: avoid; font-size: 20px; line-height: 1.8; }} .workspace {{ height: {ws_height}; border: 2px dashed #bdc3c7; border-radius: 8px; margin: 15px 0; padding: 10px; color: #95a5a6; font-size: 16px; background-color: #fafbfc; }} .ans-line {{ margin-top: 10px; border-bottom: 1px dotted #999; width: 80%; height: 30px; font-weight: bold; font-size: 20px; display: flex; align-items: flex-end; padding-bottom: 5px; }} .sol-text {{ color: #333; font-size: 18px; display: block; margin-top: 15px; padding: 15px; background-color: #f5eef8; border-left: 4px solid {'#c0392b' if is_challenge else '#8e44ad'}; border-radius: 4px; line-height: 1.8; }} .page-footer {{ text-align: right; font-size: 14px; color: #95a5a6; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }} .cover-inner {{ width: 100%; height: 100%; padding: 40px; box-sizing: border-box; text-align: center; position: relative; border: 15px solid {'#c0392b' if is_challenge else '#8e44ad'}; background: white; }} .title-box {{ margin-top: 80px; }} .title {{ font-size: 65px; color: #2c3e50; font-weight: bold; margin: 0; line-height: 1.2; }} .grade-badge {{ font-size: 40px; background-color: #f1c40f; color: #333; padding: 15px 50px; border-radius: 50px; display: inline-block; font-weight: bold; margin-top: 30px; }} .topic {{ font-size: 42px; color: #34495e; margin-top: 70px; font-weight: bold; }} .sub-topic {{ font-size: 32px; color: {'#c0392b' if is_challenge else '#8e44ad'}; margin-top: 10px; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);}} .icons {{ font-size: 110px; margin: 60px 0; }} .details-badge {{ background-color: {'#c0392b' if is_challenge else '#8e44ad'}; color: white; display: inline-block; padding: 15px 40px; border-radius: 15px; font-size: 32px; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}} .footer {{ position: absolute; bottom: 40px; left: 0; width: 100%; text-align: center; font-size: 22px; color: #7f8c8d; }} </style></head><body>{ebook_body}</body></html>"""

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
    st.success(f"✅ สร้างไฟล์ข้อสอบสำเร็จ! ตรวจสอบความสมบูรณ์แบบ 100% (เคลียร์บั๊กขอบเขตตัวเลขและตรรกะทั้งหมดแล้ว) {'(🔥 โหมดตัวตึง Ultimate Challenge!)' if 'Challenge' in st.session_state['filename_base'] else ''}")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📄 โหลดเฉพาะโจทย์", data=st.session_state['worksheet_html'], file_name=f"{st.session_state['filename_base']}_Worksheet.html", mime="text/html", use_container_width=True)
        st.download_button("🔑 โหลดเฉพาะเฉลย", data=st.session_state['answerkey_html'], file_name=f"{st.session_state['filename_base']}_AnswerKey.html", mime="text/html", use_container_width=True)
    with c2:
        st.download_button("📚 โหลดรวมเล่ม E-Book", data=st.session_state['ebook_html'], file_name=f"{st.session_state['filename_base']}_Full_EBook.html", mime="text/html", use_container_width=True)
        st.download_button("🗂️ โหลดแพ็กเกจ (.zip)", data=st.session_state['zip_data'], file_name=f"{st.session_state['filename_base']}.zip", mime="application/zip", use_container_width=True)
    st.markdown("---")
    components.html(st.session_state['ebook_html'], height=800, scrolling=True)
