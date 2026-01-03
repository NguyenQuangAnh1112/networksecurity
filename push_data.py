import os
import sys
import json
from dotenv import load_dotenv
import certifi
import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger


load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

ca = certifi.where()


class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def csv_to_json_converter(self, file_path):
        try:
            # BƯỚC 1: Đọc dữ liệu từ file CSV
            data = pd.read_csv(file_path)

            # BƯỚC 2: Xử lý Index (Chỉ số hàng)
            data.reset_index(drop=True, inplace=True)

            # BƯỚC 3: Chuyển đổi sang JSON (Logic cốt lõi)
            records = list(json.loads(data.T.to_json()).values())

            return records
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def insert_data_mongodb(self, records, database, collection):
        try:
            # BƯỚC 1: Kết nối với MongoDB Client
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)

            # BƯỚC 2: Chọn Database
            self.database = self.mongo_client[database]

            # BƯỚC 3: Chọn Collection (tương đương Table trong SQL)
            self.collection = self.database[collection]

            # BƯỚC 4: Chèn dữ liệu hàng loạt
            self.collection.insert_many(records)
            
            return len(records)
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    # 1. Định nghĩa các tham số đầu vào
    FILE_PATH = "Network_Data/phisingData.csv"
    DATABASE = "TRANSACTION_DB"
    Collection = "NetworkData"

    # 2. Khởi tạo đối tượng (Instance) từ Class đã viết
    network_obj = NetworkDataExtract()

    # 3. Bước TRANSFORM: Đọc CSV và chuyển thành JSON
    records = network_obj.csv_to_json_converter(file_path=FILE_PATH)

    # 4. Bước LOAD: Đẩy dữ liệu lên MongoDB
    no_of_records = network_obj.insert_data_mongodb(records, DATABASE, Collection)

    print(f"Số lượng bản ghi đã chèn: {no_of_records}")