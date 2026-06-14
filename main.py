import flet as ft

# دیتابیس پیش‌فرض نیروها و سرعت‌ها
TROOP_SPEEDS = {
    "شمشیرزن": 95, "شوالیه": 84, "جنونگر": 110, "مدافع": 70, "نگهبان": 75,
    "دوشمشیره": 110, "شمشیر شکن": 135, "گارد سلطنتی": 92, "گلادیاتور": 115,
    "سگ شکاری": 170, "گرگین": 150, "گاومیش": 110, "فیل": 55, "ببر": 295,
    "کرگدن": 265, "خرس": 335, "کماندار جوان": 120, "زهربان": 100,
    "تیرانداز": 115, "زوبین زن": 105, "شکارچی": 110, "تیر آتشین": 105,
    "عقاب نظر": 140, "یخ زاد": 85, "نخبه": 115, "کولی": 125, "شیردل": 125,
    "مغول": 160, "بربر": 135, "آزتک": 75, "دست دراز": 48, "جالوت": 70,
    "دژکوب": 85, "کوهکش": 500, "زنجیرشکن": 75, "زولو": 70, "سوارکار": 250,
    "بارکش": 400, "سوار تیر انداز": 200, "سوار نظام": 225, "سوار نیزه دار": 260,
    "سوارکار بپرداز": 205, "گاری": 425, "ارابه": 550, "سوار نظام سلطنتی": 225,
    "سایه سوار": 230, "زرهی": 210, "نیزه دار": 100, "دیوار دفاعی": 50,
    "نیزه پرتاپ": 95, "نیزه بلند": 70, "تبرزین دار": 80, "هوپلیت": 80,
    "جاویدان": 145
}

def main(page: ft.Page):
    # تنظیمات ظاهری صفحه موبایل
    page.title = "محاسبه زمان کستل"
    page.theme_mode = ft.ThemeMode.DARK
    page.rtl = True
    page.scroll = "adaptive"
    page.vertical_alignment = ft.MainAxisAlignment.START
    
    # متغیرهای ذخیره اطلاعات
    distance = [0.0]
    army = []

    # ==========================================
    # بخش اول: محاسبه فاصله
    # ==========================================
    fake_troop_dd = ft.Dropdown(
        label="نیروی اتک فیک",
        options=[ft.dropdown.Option(k) for k in TROOP_SPEEDS.keys()],
        border_radius=10,
    )
    
    spin_h = ft.TextField(label="ساعت", value="0", width=90, keyboard_type=ft.KeyboardType.NUMBER)
    spin_m = ft.TextField(label="دقیقه", value="0", width=90, keyboard_type=ft.KeyboardType.NUMBER)
    spin_s = ft.TextField(label="ثانیه", value="0", width=90, keyboard_type=ft.KeyboardType.NUMBER)
    
    lbl_distance = ft.Text("تعداد کاشی: هنوز محاسبه نشده", color=ft.colors.LIGHT_BLUE_200, size=16, weight=ft.FontWeight.BOLD)

    def calc_dist(e):
        if not fake_troop_dd.value:
            page.snack_bar = ft.SnackBar(ft.Text("لطفاً یک نیرو انتخاب کنید!"), bgcolor=ft.colors.RED_700)
            page.snack_bar.open = True
            page.update()
            return
            
        v = TROOP_SPEEDS[fake_troop_dd.value]
        try:
            h, m, s = int(spin_h.value or 0), int(spin_m.value or 0), int(spin_s.value or 0)
        except ValueError:
            return
            
        t = (h * 3600) + (m * 60) + s
        if t > 0:
            d = (v * t) / 2000
            distance[0] = d
            lbl_distance.value = f"تعداد کاشی (D): {d:.2f}"
        page.update()

    # ==========================================
    # بخش دوم: ارتش حریف
    # ==========================================
    enemy_troop_dd = ft.Dropdown(
        label="نوع نیرو",
        options=[ft.dropdown.Option(k) for k in TROOP_SPEEDS.keys()],
        border_radius=10,
    )
    enemy_count_tf = ft.TextField(label="تعداد", keyboard_type=ft.KeyboardType.NUMBER)
    
    army_list = ft.ListView(height=150, spacing=10)

    def update_army_list():
        army_list.controls.clear()
        for item in army:
            army_list.controls.append(
                ft.Container(
                    content=ft.Text(f"{item['name']} | سرعت: {item['speed']} | تعداد: {item['count']}"),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    padding=10,
                    border_radius=8
                )
            )
        page.update()

    def add_troop(e):
        if not enemy_troop_dd.value or not enemy_count_tf.value: return
        try:
            count = int(enemy_count_tf.value)
            if count <= 0: raise ValueError
        except:
            return
            
        army.append({
            "name": enemy_troop_dd.value,
            "speed": TROOP_SPEEDS[enemy_troop_dd.value],
            "count": count
        })
        enemy_count_tf.value = ""
        update_army_list()

    def clear_army(e):
        army.clear()
        update_army_list()

    # ==========================================
    # بخش سوم: نتیجه نهایی
    # ==========================================
    lbl_final_time = ft.Text("00:00:00", size=35, color=ft.colors.AMBER_400, weight=ft.FontWeight.BOLD)

    def calc_final(e):
        if distance[0] == 0.0 or not army:
            page.snack_bar = ft.SnackBar(ft.Text("کاشی‌ها محاسبه نشده یا لیست ارتش خالی است!"), bgcolor=ft.colors.RED_700)
            page.snack_bar.open = True
            page.update()
            return
            
        total_weight = sum(t["speed"] * t["count"] for t in army)
        total_count = sum(t["count"] for t in army)
        v_avg = total_weight / total_count
        
        if distance[0] < 3:
            t_final = 0
        else:
            t_final = ((distance[0] - 3) / v_avg) * 2000
            
        hh = int(t_final // 3600)
        mm = int((t_final % 3600) // 60)
        ss = int(t_final % 60)
        lbl_final_time.value = f"{hh:02d}:{mm:02d}:{ss:02d}"
        page.update()

    # ==========================================
    # چیدمان عناصر در صفحه
    # ==========================================
    page.add(
        ft.Text("۱. اتک فیک", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_400),
        fake_troop_dd,
        ft.Row([spin_h, spin_m, spin_s], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.ElevatedButton("محاسبه تعداد کاشی", on_click=calc_dist, bgcolor=ft.colors.BLUE_700, color=ft.colors.WHITE),
        lbl_distance,
        
        ft.Divider(height=30, color=ft.colors.WHITE24),
        
        ft.Text("۲. ارتش حریف", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_400),
        enemy_troop_dd,
        enemy_count_tf,
        ft.Row([
            ft.ElevatedButton("افزودن نیرو", on_click=add_troop, bgcolor=ft.colors.BLUE_700, color=ft.colors.WHITE),
            ft.ElevatedButton("پاک کردن", on_click=clear_army, bgcolor=ft.colors.RED_700, color=ft.colors.WHITE),
        ]),
        army_list,
        
        ft.Divider(height=30, color=ft.colors.WHITE24),
        
        ft.Text("۳. نتیجه نهایی", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_400),
        ft.ElevatedButton("محاسبه زمان بازگشت", on_click=calc_final, bgcolor=ft.colors.GREEN_700, color=ft.colors.WHITE, width=200),
        ft.Container(content=lbl_final_time, alignment=ft.alignment.center, padding=10),
        
        ft.Divider(height=10, color=ft.colors.TRANSPARENT),
        ft.Text("برنامه نویس: PouriaTbag\nالگوریتم محاسبه: NaCo\nساخته شده توسط اتحاد بزرگ گادفمیلی", 
                size=12, color=ft.colors.WHITE54, text_align=ft.TextAlign.CENTER, width=page.width)
    )

if __name__ == '__main__':
    ft.app(target=main)
