import telebot
import random
import time
from datetime import datetime
from collections import defaultdict

TOKEN = '7618979983:AAGDWrAVf6NgNkBTa7dS-kmH0k5BbWHhNw8'
bot = telebot.TeleBot(TOKEN)

# Biến để lưu số phiên hiện tại và tổng hợp số lần quay thử của người dùng
current_session = 1
user_attempts = {}
all_results = []

def increment_session():
    global current_session
    current_session += 1

@bot.message_handler(commands=['quaythu'])
def quay_thu(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    chat_id = message.chat.id

    # Tăng số lần quay thử của người dùng
    if user_id not in user_attempts:
        user_attempts[user_id] = 0
    user_attempts[user_id] += 1

    # Thông báo đang quay thử
    bot.send_message(chat_id, f"🎲 <a href='tg://user?id={user_id}'>{user_name}</a> đang quay thử kết quả xổ số... Chúc Bạn May Mắn! 🎉", parse_mode='HTML')

    # Đợi 5 giây trước khi gửi kết quả
    time.sleep(5)

    # Gọi hàm gửi kết quả
    send_results(chat_id, user_name)

def send_results(chat_id, user_name):
    global all_results
    global current_session  # Đảm bảo biến current_session được sử dụng

    # Tạo kết quả ngẫu nhiên
    date_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    results = {
        "Giải Đặc Biệt": random.randint(10000, 99999),
        "Giải Nhất": random.randint(10000, 99999),
        "Giải Nhì": [random.randint(10000, 99999) for _ in range(2)],
        "Giải Ba": [random.randint(10000, 99999) for _ in range(6)],
        "Giải Tư": [random.randint(10000, 99999) for _ in range(4)],
        "Giải Năm": [random.randint(10000, 99999) for _ in range(6)],
        "Giải Sáu": [random.randint(100, 999) for _ in range(3)],
        "Giải Bảy": [f"{random.randint(0, 99):02}" for _ in range(4)]
    }

    all_results.append(results)  # Lưu kết quả vào danh sách

    # Tạo kết quả định dạng
    result_message = f"🎲 KẾT QUẢ QUAY THỬ XỔ SỐ MIỀN BẮC 🎲\n\n"
    result_message += f"🕒 Ngày giờ: {date_now}\n"
    result_message += f"🔢 Phiên quay thử: #{current_session}\n"  # Hiển thị phiên
    result_message += f"👤 Người quay: {user_name}\n\n"

    # Thêm các giải thưởng vào thông điệp kết quả
    for title, values in results.items():
        if isinstance(values, list):
            result_message += f"{title}: {' - '.join(map(str, values))}\n"
        else:
            result_message += f"{title}: {values}\n"

    result_message += "\nChúc bạn may mắn! 🍀"

    # Gửi kết quả
    bot.send_message(chat_id, result_message)

    # Tăng số phiên lên 1 sau khi gửi kết quả
    increment_session()

@bot.message_handler(commands=['quaythude'])
def quay_thude(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    chat_id = message.chat.id

    try:
        selected_number = message.text.split()[1]

        # Kiểm tra tính hợp lệ của số nhập vào
        if not selected_number.isdigit() or len(selected_number) != 2 or not (0 <= int(selected_number) <= 99):
            bot.send_message(chat_id, "❗ Vui lòng nhập một số hợp lệ từ 00 đến 99. Ví dụ: /quaythude 00")
            return

        # Tạo kết quả mới cho lệnh quay thử
        send_results(chat_id, user_name)

        last_special_number = str(all_results[-1]["Giải Đặc Biệt"])[-2:]

        if selected_number == last_special_number:
            bot.send_message(chat_id, f"🎉 Chúc mừng <a href='tg://user?id={user_id}'>{user_name}</a>! Bạn đã chọn số {selected_number} và trúng giải đặc biệt! 🎉", parse_mode='HTML')
        else:
            bot.send_message(chat_id, f"😢 Chia buồn <a href='tg://user?id={user_id}'>{user_name}</a>! Bạn đã chọn số {selected_number} không trúng giải đặc biệt. Số cuối là {last_special_number}. Chúc Bạn May Mắn Lần Sau! 🍀", parse_mode='HTML')

    except IndexError:
        bot.send_message(chat_id, "❗ Bạn chưa chọn số. Hãy nhập lệnh theo cú pháp: /quaythude xx (vd: /quaythude 00)")

@bot.message_handler(commands=['quaythu_xs'])
def quay_thu_xs(message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id  # Lấy ID người dùng
    chat_id = message.chat.id
    last_two_digits_count = defaultdict(int)

    # Tính số lần xuất hiện của mỗi số cuối trong 100 phiên gần nhất
    recent_results = all_results[-100:]  # Lấy 100 phiên gần nhất
    for result in recent_results:
        for title, values in result.items():
            if isinstance(values, list):
                for value in values:
                    last_two_digits_count[str(value)[-2:].zfill(2)] += 1  # Đảm bảo có hai chữ số
            else:
                last_two_digits_count[str(values)[-2:].zfill(2)] += 1  # Đảm bảo có hai chữ số

    total_count = sum(last_two_digits_count.values())
    sorted_digits = sorted(last_two_digits_count.items(), key=lambda x: x[1], reverse=True)
    
    most_common = sorted_digits[:10]
    least_common = sorted_digits[-10:]

    most_common_message = "🔴 10 Lô Tô Ra Nhiều Nhất🔴:\n" + "\n".join(
        [f"{digit}: {count} lần ({(count / total_count * 100):.2f}%)" for digit, count in most_common]
    )
    
    least_common_message = "🔵 10 Lô Tô Ra Ít Nhất🔵:\n" + "\n".join(
        [f"{digit}: {count} lần ({(count / total_count * 100):.2f}%)" for digit, count in least_common]
    )

    # Tìm tất cả các con lô tô từ 00 đến 99
    all_digits = {f"{i:02}" for i in range(100)}
    appeared_digits = set(last_two_digits_count.keys())
    not_appeared_digits = all_digits - appeared_digits

    not_appeared_message = "⚪ 10 Lô Tô Chưa Về⚪:\n" + "\n".join(list(not_appeared_digits)[:10])

    # Tính tổng số phiên đã có kết quả quay thử
    total_sessions = len(all_results)  # Số phiên quay thử

    # Tạo định dạng tag cho người dùng
    user_mention = f"<a href='tg://user?id={user_id}'>{user_name}</a>"  # Tạo tag với ID người dùng

    # Gửi kết quả cho người dùng với tag
    bot.send_message(chat_id, f"📊 THỐNG KÊ TỶ LỆ Xắc Suất LÔ TÔ \n{most_common_message}\n\n{least_common_message}\n\n{not_appeared_message}\n\nThống Kê Được Lấy Tổng {total_sessions} Phiên # {total_sessions} \n\n👤 {user_mention} hãy theo dõi các con số may mắn! 🎉", parse_mode='HTML')

@bot.message_handler(commands=['quaythu3cang'])
def quay_thu_3cang(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    chat_id = message.chat.id

    try:
        # Lấy số từ lệnh của người dùng
        selected_number = message.text.split()[1]

        # Kiểm tra tính hợp lệ của số nhập vào (chỉ nhận số có ba chữ số)
        if not selected_number.isdigit() or len(selected_number) != 3:
            bot.send_message(chat_id, "❗ Vui lòng nhập một số hợp lệ có ba chữ số. Ví dụ: /quaythu3cang 123")
            return

        # Tạo kết quả mới cho lệnh quay thử
        send_results(chat_id, user_name)

        last_special_number = str(all_results[-1]["Giải Đặc Biệt"])[-3:]

        if selected_number == last_special_number:
            bot.send_message(chat_id, f"🎉 Chúc mừng <a href='tg://user?id={user_id}'>{user_name}</a>! Bạn đã chọn số {selected_number} và trúng giải đặc biệt! 🎉", parse_mode='HTML')
        else:
            bot.send_message(chat_id, f"😢 Chia buồn <a href='tg://user?id={user_id}'>{user_name}</a>! Bạn đã chọn số {selected_number} không trúng giải đặc biệt. Số cuối là {last_special_number}. Chúc Bạn May Mắn Lần Sau! 🍀", parse_mode='HTML')

    except IndexError:
        bot.send_message(chat_id, "❗ Bạn chưa chọn số. Hãy nhập lệnh theo cú pháp: /quaythu3cang xxx (vd: /quaythu3cang 123)")

@bot.message_handler(commands=['quaythulo'])
def quay_thu_lo(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    chat_id = message.chat.id

    try:
        selected_number = message.text.split()[1]

        # Kiểm tra tính hợp lệ của số nhập vào
        if not selected_number.isdigit() or len(selected_number) != 2 or not (0 <= int(selected_number) <= 99):
            bot.send_message(chat_id, "❗ Vui lòng nhập một số hợp lệ từ 00 đến 99. Ví dụ: /quaythulo 00")
            return

        # Tạo kết quả mới cho lệnh quay thử
        send_results(chat_id, user_name)

        match_found = False
        for title, values in all_results[-1].items():
            if isinstance(values, list):
                if selected_number in [str(value)[-2:].zfill(2) for value in values]:
                    match_found = True
                    break

        if match_found:
            bot.send_message(chat_id, f"🎉 Chúc mừng {user_name}! Bạn đã chọn số {selected_number} và trúng lô tô! 🎉")
        else:
            bot.send_message(chat_id, f"😢 Chia buồn {user_name}! Bạn đã chọn số {selected_number} không trúng lô tô. Chúc Bạn May Mắn Lần Sau! 🍀")
    except IndexError:
        bot.send_message(chat_id, "❗ Bạn chưa chọn số. Hãy nhập lệnh theo cú pháp: /quaythulo xx (vd: /quaythulo 00)")

# Chạy bot
if __name__ == '__main__':
    bot.polling(none_stop=True)
