import os
import pandas as pd
from django.core.management.base import BaseCommand
from mainPage.models import Class  # 'myapp'를 실제 앱 이름으로 교체하세요

class Command(BaseCommand):
    help = 'Import CSV data to the Class model'

    def handle(self, *args, **kwargs):
        # 절대 경로로 CSV 파일 경로 지정
        csv_file_path = '/Users/gimnayeong/Documents/GitHub/UnitedNetworking_1/Team1/Team1/management/commands/class_list.csv'

        # CSV 파일 읽기
        df = pd.read_csv(csv_file_path)

        # 빈 값은 0으로 채우기
        df = df.fillna(0)

        # CSV 데이터를 모델에 저장
        for _, row in df.iterrows():
            class_instance = Class(
                center_data_id=int(row['center_data_id']),
                teacher=row['teacher'],
                date=row['date'],
                time=row['time'],
                duration=int(row['duration']),
                detail=row['detail'],
                credit_num=int(row['credit_num']),
                capacity=int(row['capacity']),
                current_people=int(row['current_people']),
                waiting_people=int(row['waiting_people'])
            )
            class_instance.save()

        self.stdout.write(self.style.SUCCESS('Successfully imported data to the Class model'))
