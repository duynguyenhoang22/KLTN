import pandas as pd
import random

# Tập dữ liệu từ vựng để nội suy vào tin nhắn
names = ['Hương', 'Linh', 'Tuấn', 'Mai', 'Thảo', 'Phương', 'Hùng', 'Minh', 'Trang', 'Long', 'Lan', 'Nam', 'Hoa', 'Dũng', 'Quân', 'Nga', 'Hà', 'Khang', 'Vy', 'Oanh', 'Thành', 'Sơn', 'Ngọc', 'Tùng', 'Bình']
banks = ['Vietcombank', 'MB Bank', 'Techcombank', 'BIDV', 'Agribank', 'Vietinbank', 'VPBank', 'ACB', 'TPBank', 'Sacombank']
amounts = ['100k', '200k', '500k', '1 triệu', '2 triệu', '3 triệu', '5 triệu', '10 triệu', '500 ngàn', 'vài trăm', 'một ít']
urls = ['thiepcuoi-online.vn/namhoa', 'shopee-sale-vn.com', 'tiktok-jobs.net', 'zalo-group.club/join', 't.me/hoinhanroi', 'bit.ly/nhanqua', 'drive-google.com/file123', 'tinyurl.com/nhan-thuong']
phones = ['0981234567', '0909998877', '0912345678', '0934567890', '0978123456', '0868123123', '0888999000', '0345678901']
stks = ['123456789', '987654321', '0981234567', '19034567890', '001100223344', '88889999', '68686868', '1122334455']

# Kịch bản lừa đảo (Templates)
templates = [
    # Lừa đảo mượn tiền
    ("{name1} ơi {name2} nè, đang kẹt quá cho mượn tạm {amount} vào {bank} {stk} chiều mai trả nhé.", "Lừa đảo mượn tiền", 0, 0),
    ("Mày ơi tao đang đứng ở cây xăng mà quên mang ví, app ngân hàng thì lỗi. Bắn qua số tài khoản {stk} {bank} {amount} nha, về tao đưa tiền mặt.", "Lừa đảo mượn tiền", 0, 0),
    ("Chị {name1} ơi, mẹ em đang cấp cứu trong viện mà em chưa xoay kịp tiền, chị cho em vay tạm {amount} nhé, tuần sau có lương em trả. STK em {stk} {bank}.", "Lừa đảo mượn tiền", 0, 0),
    ("{name1} à, tớ mới đổi điện thoại nên mất hết app, cậu chuyển khoản hộ tớ {amount} cho người này nhé, stk {stk} {bank}. Tối đi làm về tớ qua đưa tiền mặt.", "Lừa đảo mượn tiền", 0, 0),
    ("Ê {name1}, tài khoản tao bị khóa, mày chuyển giùm tao {amount} vô số tài khoản này {stk} {bank} nha, mai tao trả gấp đôi.", "Lừa đảo mượn tiền", 0, 0),

    # Lừa đảo nhầm số
    ("Chị {name1} ơi mớ rau em để trước cửa rồi nha. Ủa nhầm số, cho em xin lỗi nhé. Chúc chị ngày mới vui vẻ.", "Lừa đảo nhầm số", 0, 0),
    ("Alo anh {name1} nay đi nhậu không? Á chết, nhầm số rồi, xin lỗi anh nha. Mà thấy anh có vẻ hợp cạ, rảnh thì kết bạn zalo số này {phone} giao lưu nhé.", "Lừa đảo nhầm số", 0, 1),
    ("Dạ cô {name1} ơi, cháu giao hoa để ở bảo vệ rồi nhé. Ôi cháu ấn nhầm số, cháu xin lỗi cô ạ. Nhân tiện bên cháu đang có chương trình tặng quà, cô add zalo {phone} để nhận nhé.", "Lừa đảo nhầm số", 0, 1),
    ("Em gửi file báo cáo tháng này anh check nhé. Dạ em nhầm số sếp, phiền anh/chị quá. Số đuôi anh chị đẹp ghê, mình làm quen nhé, zalo em {phone}.", "Lừa đảo nhầm số", 0, 1),
    ("Nay con không về ăn cơm mẹ nhé. Xin lỗi mình nhắn nhầm. Chúc bạn một ngày tốt lành!", "Lừa đảo nhầm số", 0, 0),

    # Lừa đảo việc làm / Đầu tư
    ("{name1} dạo này rảnh không, tớ đang làm thêm cái này thu nhập ổn lắm, ngày {amount}, rảnh thì tớ chỉ cho. Nhắn qua zalo {phone} nha.", "Lừa đảo việc làm", 0, 1),
    ("Ê {name1}, đợt trước mày hỏi vụ đầu tư chứng khoán, tao đang theo nhóm này phím lệnh ok lắm, vào nhóm xem thử {url}", "Lừa đảo đầu tư", 1, 0),
    ("Chị {name1}, bên công ty em đang tuyển CTV gõ văn bản tại nhà, không cọc không phí, rảnh làm bận nghỉ. Chị quan tâm thì nhắn Zalo trưởng phòng em {phone}.", "Lừa đảo việc làm", 0, 1),
    ("Dạo này lạm phát quá bà nhỉ. Tui đang đầu tư bên quỹ này sinh lời đều lắm, bà muốn tìm hiểu thì nhấp vào link này đăng ký nè: {url}", "Lừa đảo đầu tư", 1, 0),
    ("{name1} ơi tao mới kiếm được trang này xem Tiktok cũng có tiền, ngày được {amount} dễ ợt. Mày thử không vô đây nè: {url}", "Lừa đảo việc làm", 1, 0),

    # Lừa đảo link độc hại
    ("{name1} ơi, cuối tuần này tớ cưới, cậu bớt chút thời gian tới dự nhé. Thiệp tớ gửi qua link này {url}, nhớ xem kỹ thời gian địa điểm nha.", "Lừa đảo link độc hại", 1, 0),
    ("Sếp ơi, file hợp đồng bên đối tác gửi em để trên drive nhé, sếp click vào {url} tải về xem giúp em ạ.", "Lừa đảo link độc hại", 1, 0),
    ("Ê mày, hình hôm bữa đi chơi tao up lên đây rồi nha, vào {url} tải về lẹ đi tao sắp xóa.", "Lừa đảo link độc hại", 1, 0),
    ("Anh {name1}, giấy mời họp phụ huynh bé nhà mình em gửi file mềm qua link này {url}, anh tải về xem nhé.", "Lừa đảo link độc hại", 1, 0),
    ("Chị ơi áo chị đặt hôm qua em ship hỏa tốc rồi nha, mã vận đơn chị xem ở đây {url}.", "Lừa đảo link độc hại", 1, 0),

    # Lừa đảo nhờ vả
    ("{name1} đang ở đâu đấy, mua hộ tớ cái thẻ điện thoại Viettel 100k với, lát tớ bắn lại cho.", "Lừa đảo nhờ vả", 0, 0),
    ("Mày ơi, cháu tao đang thi bé khỏe bé ngoan, mày vào link này {url} vote cho nó một phiếu nhé, số báo danh 123.", "Lừa đảo link độc hại", 1, 0),
    ("{name1} ơi tớ đang cần gấp một mã thẻ cào Mobifone 500k để nạp gia hạn gói cước, cậu mua giúp tớ nhắn mã qua đây nhé, chiều tớ trả tiền.", "Lừa đảo nhờ vả", 0, 0),
    ("Anh {name1}, em đang thi thiết kế logo, anh vào bình chọn giúp em với ạ, link đây anh: {url}, nhớ đăng nhập facebook để vote nha.", "Lừa đảo link độc hại", 1, 0),

    # Lừa đảo tình cảm / Quà tặng
    ("Chào bạn, mình thấy số điện thoại của bạn qua hội nhóm, thấy ảnh đại diện dễ thương nên muốn làm quen, add zalo mình nhé {phone}.", "Lừa đảo tình cảm", 0, 1),
    ("Em {name1} phải không? Lâu quá không gặp, em còn nhớ anh không? Nay anh bay về Việt Nam có gửi cho em món quà, rảnh nhắn lại anh nhé.", "Lừa đảo tình cảm", 0, 0),
    ("{name1} ơi, tôi có món quà gửi tặng bạn từ nước ngoài, bạn liên hệ nhân viên hải quan số {phone} để làm thủ tục nhận nhé.", "Lừa đảo nhận quà", 0, 1),
    ("Chúc mừng {name1} nha, số điện thoại của bạn may mắn trúng giải thưởng trị giá 50 triệu từ Shopee, click vào {url} để làm thủ tục nhận thưởng.", "Lừa đảo trúng thưởng", 1, 0)
]

# Quá trình tạo sinh dữ liệu
generated_data = []

# Có thể thiết lập seed để tái lập kết quả cố định
random.seed(42)

for i in range(200):
    template, category, has_url, has_phone = random.choice(templates)
    
    # Random các thông tin
    n1, n2 = random.sample(names, 2)
    bank = random.choice(banks)
    amount = random.choice(amounts)
    url = random.choice(urls)
    phone = random.choice(phones)
    stk = random.choice(stks)
    
    # Điền vào chỗ trống
    content = template.format(name1=n1, name2=n2, bank=bank, amount=amount, url=url, phone=phone, stk=stk)
    
    # Chuẩn bị định dạng giống như file ban đầu
    row = {
        'content': content,
        'label': 1,
        'has_url': has_url,
        'has_phone_number': has_phone,
        'sender_type': 'personal_number',
        'category': category,
        'obfuscation_level': 'LEVEL 0 – Không obfuscation (formal)',
        'data_origin': 'synthetic',
        'source_dataset': 'synthetic_hard_label_1',
        'source_row_id': i
    }
    generated_data.append(row)

# Chuyển đổi thành DataFrame và xuất file
df_hard = pd.DataFrame(generated_data)
output_file = 'hard_negative_label_1.csv'
df_hard.to_csv(output_file, index=False, encoding='utf-8')

print(f"Hoàn tất tạo file: {output_file} với {len(df_hard)} dòng.")