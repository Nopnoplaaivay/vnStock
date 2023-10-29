import pandas as pd
import numpy as np

# Tạo một DataFrame với dữ liệu giả định về giá cổ phiếu theo từng ngày
np.random.seed(0)
date_range = pd.date_range('2023-10-01', periods=100, freq='D')
prices = np.random.randint(1, 100, size=100)
stock_df = pd.DataFrame({'Date': date_range, 'Price': prices})

# Đặt cột 'Date' làm chỉ mục cho DataFrame
stock_df.set_index('Date', inplace=True)

# In ra dữ liệu ban đầu
print("Dữ liệu ban đầu:")
print(stock_df.head(10))

# Resample theo tuần và tính giá trị trung bình hàng tuần
weekly_resampled = stock_df.resample('W').mean()

# In ra kết quả resample theo tuần
print("\nKết quả resample hàng tuần:")
print(weekly_resampled.head(10))
