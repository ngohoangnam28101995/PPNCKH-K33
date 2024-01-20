
import pandas as pd
import warnings
import re


class DataReader:
    def __init__(self, filename, columns_use, columns_add, column_adj):

        #Lưu Đường dẫn file
        self.filename = filename
        #Lưu Các cột sử dụng
        self.columns_use = columns_use
        #Lưu Dataframe sử dụng
        self.data = pd.read_csv(self.filename, usecols = self.columns_use)
        #Add Cột mới
        self.add = columns_add
        #Lưu cột chứa tên video
        self.adj = column_adj
        #Gọi lại method để preprocess data
        self.read_and_adjust()
        
    def read_and_adjust(self):
        #Tạo cột Frame (Số lượng frame trên 1 video) (Frame bắt đầu - Frame kết thúc + 1)
        self.data[self.add[2]] = self.data["end frame of the sign (relative to full videos)"] - self.data["start frame of the sign (relative to full videos)"] + 1
        #Tạo cột Signer - Tách từ cột video
        self.data.insert(0, self.add[1], self.data[self.adj].str.split('_').apply(lambda x: x[4]))
        #Tạo cột temp chứa dữ liệu là cột video được split ra
        self.data['temp'] = self.data[self.adj].str.split('-')
        #Tạo cột video name có cấu trúc ASL_2008_01_11-scene-71
        self.data[self.add[0]] = self.data['temp'].apply(lambda x: x[0][:x[0].index('scene')]+ '-' + x[0][x[0].index('scene') : x[0].index('scene') + 5] + '-' + x[0][x[0].index('scene') + 5:])
        self.data[self.add[0]] = self.data[self.add[0]].str.replace('_-', '-')
        #Tìm index các video cần loại (Video chứa không scence phía trước)
        trash_vid = self.data[self.data[self.add[1]].str.startswith('s')].index

        #Tạo cột vid_name theo cấu trúc : Signer + '-session-' + Vid_name +'-'+ start frame +'-'+ end frame +'-'+ 'camera1.mov'
   
        self.data[self.add[0]] = self.data[self.add[1]] + '-session-' + self.data[self.add[0]] \
                                  + '-' + self.data['start frame of the sign (relative to full videos)'].astype(str) \
                                  + '-' + self.data['end frame of the sign (relative to full videos)'].astype(str) \
                                  + '-' + 'camera1.mov'
        
        self.data.drop(columns = ['temp', 'start frame of the sign (relative to full videos)',
                                  'end frame of the sign (relative to full videos)',
                                   self.adj], 
                       inplace = True)
        #Bỏ cột theo index trash video
        self.data.drop(trash_vid, inplace = True)

        #Chuẩn hoá index
        self.data.reset_index(drop = True, inplace = True)

        #Tạo cột text với giá trị empty
        self.data[self.add[3]] = 'Empty'
        
    def get_data(self):
        return self.data