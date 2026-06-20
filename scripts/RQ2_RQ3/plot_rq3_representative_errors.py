"""Create a slide-ready table of representative RQ3 errors."""

from pathlib import Path
import textwrap

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd


OUTPUT_DIR = Path(__file__).resolve().parent

ROWS = [
    {
        "Nhóm lỗi": "FN chung",
        "Nội dung rút gọn": (
            "Nhận thấy có hành vi lợi dụng tín nhiệm, chiếm đoạt tài sản… "
            "yêu cầu thanh toán gấp… liên hệ [SĐT] để giải quyết."
        ),
        "Nhãn thật": "Smishing (1)",
        "Mô hình dự đoán sai": (
            "CafeBERT; DistilBERT multilingual; TextCNN; TextCNN distilled"
        ),
        "Số MH": 4,
        "Confidence TB": 0.9900,
        "Nhận xét": "Đòi nợ mang văn phong hành chính, không có URL.",
    },
    {
        "Nhóm lỗi": "FN ngân hàng",
        "Nội dung rút gọn": (
            "ACB cảnh báo SMS lừa đảo… không cung cấp USER, MẬT KHẨU, "
            "OTP… truy cập [URL]."
        ),
        "Nhãn thật": "Smishing (1)",
        "Mô hình dự đoán sai": "CafeBERT; TextCNN; TextCNN distilled",
        "Số MH": 3,
        "Confidence TB": 0.9921,
        "Nhận xét": "Cảnh báo ngân hàng có hình thức giống tin hợp lệ.",
    },
    {
        "Nhóm lỗi": "FP có URL",
        "Nội dung rút gọn": (
            "Hội thảo trực tuyến… mời phụ huynh, thí sinh tham gia tại "
            "[URL]. Hotline: [SĐT]."
        ),
        "Nhãn thật": "Hợp lệ (0)",
        "Mô hình dự đoán sai": "DistilBERT multilingual; TextCNN; TextCNN distilled",
        "Số MH": 3,
        "Confidence TB": 0.9802,
        "Nhận xét": "Tin tuyển sinh hợp lệ nhưng có URL và lời kêu gọi.",
    },
    {
        "Nhóm lỗi": "FP external",
        "Nội dung rút gọn": (
            "Sau lần bế tắc vì phá sản, gánh một khoản nợ… "
            "t mới bắt đầu sống kiểu “yolo”."
        ),
        "Nhãn thật": "Hợp lệ (0)",
        "Mô hình dự đoán sai": "TextCNN; TextCNN distilled",
        "Số MH": 2,
        "Confidence TB": 0.7419,
        "Nhận xét": "Ngôn ngữ đời thường ngoài miền chứa từ vựng tài chính.",
    },
]


def wrap(value, width):
    return "\n".join(
        textwrap.wrap(
            str(value),
            width=width,
            break_long_words=False,
            break_on_hyphens=False,
        )
    )


def main():
    df = pd.DataFrame(ROWS)
    df.to_csv(
        OUTPUT_DIR / "rq3_representative_error_table.csv",
        index=False,
        encoding="utf-8-sig",
    )

    display = df.copy()
    display["Nội dung rút gọn"] = display["Nội dung rút gọn"].map(
        lambda x: wrap(x, 43)
    )
    display["Mô hình dự đoán sai"] = (
        display["Mô hình dự đoán sai"]
        .str.replace("DistilBERT multilingual", "DistilBERT-m", regex=False)
        .str.replace("TextCNN distilled", "TextCNN-distilled", regex=False)
        .map(lambda x: wrap(x, 28))
    )
    display["Confidence TB"] = display["Confidence TB"].map(lambda x: f"{x:.4f}")

    columns = [
        "Nhóm lỗi",
        "Nội dung rút gọn",
        "Nhãn thật",
        "Mô hình dự đoán sai",
        "Số MH",
        "Confidence TB",
    ]

    fig, ax = plt.subplots(figsize=(16, 9))
    ax.axis("off")
    header_color = "#304B78"
    fn_color = "#FCE8E6"
    fp_color = "#FFF3E0"
    edge_color = "#A8B2C1"

    left, right = 0.025, 0.975
    bottom, top = 0.18, 0.83
    header_height = 0.105
    row_height = (top - bottom - header_height) / len(display)
    widths = [0.105, 0.35, 0.105, 0.255, 0.075, 0.11]
    x_positions = [left]
    for width in widths:
        x_positions.append(x_positions[-1] + (right - left) * width)

    for col_idx, label in enumerate(columns):
        x0, x1 = x_positions[col_idx], x_positions[col_idx + 1]
        ax.add_patch(
            Rectangle(
                (x0, top - header_height),
                x1 - x0,
                header_height,
                facecolor=header_color,
                edgecolor=edge_color,
                linewidth=1.0,
            )
        )
        ax.text(
            (x0 + x1) / 2,
            top - header_height / 2,
            label,
            ha="center",
            va="center",
            color="white",
            fontsize=11.5,
            weight="bold",
        )

    for row_idx, (_, row) in enumerate(display[columns].iterrows()):
        y1 = top - header_height - row_idx * row_height
        y0 = y1 - row_height
        background = fn_color if row_idx < 2 else fp_color
        for col_idx, value in enumerate(row):
            x0, x1 = x_positions[col_idx], x_positions[col_idx + 1]
            ax.add_patch(
                Rectangle(
                    (x0, y0),
                    x1 - x0,
                    row_height,
                    facecolor=background,
                    edgecolor=edge_color,
                    linewidth=0.9,
                )
            )
            centered = col_idx in (0, 2, 4, 5)
            ax.text(
                (x0 + x1) / 2 if centered else x0 + 0.009,
                (y0 + y1) / 2,
                str(value),
                ha="center" if centered else "left",
                va="center",
                fontsize=10.7,
                linespacing=1.35,
                color="#172033",
                weight="bold" if col_idx == 0 else "normal",
            )

    ax.set_title(
        "Các lỗi dự đoán tiêu biểu trên tập dev",
        fontsize=21,
        weight="bold",
        color="#243B64",
        pad=14,
    )
    fig.text(
        0.5,
        0.105,
        "Confidence TB: trung bình độ tin cậy của các mô hình dự đoán sai. "
        "URL và số điện thoại đã được ẩn.",
        ha="center",
        fontsize=10.5,
        color="#4A5568",
    )
    fig.text(
        0.5,
        0.06,
        "FN: bỏ sót tin nhắn smishing  •  FP: cảnh báo nhầm tin nhắn hợp lệ",
        ha="center",
        fontsize=10.5,
        color="#4A5568",
    )
    fig.tight_layout(rect=[0.01, 0.02, 0.99, 0.95])

    for suffix in ("png", "pdf"):
        fig.savefig(
            OUTPUT_DIR / f"rq3_representative_error_table.{suffix}",
            dpi=300,
            bbox_inches="tight",
            facecolor="white",
        )
    plt.close(fig)


if __name__ == "__main__":
    main()
