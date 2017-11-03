#その日が何曜日かを判定する関数Weekdy_judge
def Weekday_judge(date):
	import datetime as dt
	new_date=dt.datetime.strptime(date,"%Y/%m/%d")
	#月曜日~日曜日:0~6
	weekday=new_date.weekday()
	return weekday
	
def Calculation(time, weekday, output_data):
	over_24oclock = 0
	total_day = 0
	
	time = time.split()
	for i in range(len(time)):
		time[i] = time[i].split("-")
		time1 = list(map(float, time[i][0].split(":")))
		time2 = list(map(float, time[i][1].split(":")))
		start = time1[0] + time1[1]/60
		end = time2[0] + time2[1]/60
		total_day += (end - start)
		if end > 22.00:			#22時以降の勤務を確認
			output_data[2] += Night_overtime(start, end)
			if end >24.00:		#24時以降の勤務を確認
				over_24oclock += Check_over24(start, end)
	
				
	if weekday <4:		#月〜木曜日
		output_data = Check_overtime(total_day, output_data)
	
	elif weekday == 4:	#金曜日
		#24時以降に勤務がある場合
		if over_24oclock !=0:
			output_data[3] += over_24oclock
			total_day -= over_24oclock
			output_data = Check_overtime(total_day, output_data)
		#24時以降に勤務がない場合
		else:
			output_data = Check_overtime(total_day, output_data)
			
	elif weekday == 5:	#土曜日
		#24時以降に勤務がある場合
		if over_24oclock !=0:
			output_data[4] += over_24oclock
			output_data[3] += (total_day - over_24oclock)
		#24時以降に勤務がない場合
		else:
			output_data[3] += total_day
		
	elif weekday == 6: 	#日曜日
		output_data[4] += total_day
	
	#print(output_data,"    ",total_day)
	
	return output_data

#深夜残業時間数を確認する関数Night_overtime
def Night_overtime(start, end):
	total_night=0
	#開始時刻が22時以前の場合
	if start <22.00:		
		total_night += (end-22.00)
	#開始時刻が22時以降の場合
	else:
		total_night += (end - start)
	return total_night

#24時以降の勤務時間を確認する関数Check_over24
def Check_over24(start, end):
	total_over24=0
	#開始時刻が24時以前の場合
	if start <24.00:		
		total_over24 += (end-22.00)
	#開始時刻が24時以降の場合
	else:
		total_over24 += (end - start)
	return total_over24

#法定内/法定外残業時間を確認する関数Check_overtime
def Check_overtime(total, output_data):
	#勤務時間が7時間以上8時間以内の場合
	if total >7.00 and total < 8.00:
		output_data[0] += (total - 7.00)
	#勤務時間が8時間以上の場合
	elif total > 8.00:
		output_data[0] += 1.00
		output_data[1] += (total - 8.00)
	return output_data
	
def Get_monthend(date):
	d=date.split("/")
	year=int(d[0])
	month=int(d[1])
	if month==2:
		if year%4==0:
			month_end= date+"/29"
			return month_end
		month_end= date+"/28"
		return month_end
	elif month==1 or month==3 or month==5 or month==7 or month==8 or month==10 or month==12:
		month_end= date+"/31"
		return month_end
	else:
		month_end= date+"/30"
		return month_end


def main():
	import sys
	input_data=[]
	data_line={}
	#入力データの読み込み
	input_data.append(input())
	month_end = Get_monthend(input_data[0])
	i=1
	while True:
		input_data.append(input())
		data_line[i] = input_data[i].strip("\n")
		data_line[i] = data_line[i].split(" ",1)
		if data_line[i][0]==month_end:
			break
		i+=1
	#num_dataにデータの数を代入
	num_data = i+1

	#output_data : 法定内残業時間数(時)、法定外残業時間数(時)、深夜残業時間数(時)、所定休日労働時間数(時)、法定休日労働時間数(時)
	output_data=[0, 0, 0, 0, 0]
	i=1
	while i<num_data:
		if input_data[0] in data_line[i][0]:
			weekday=Weekday_judge(data_line[i][0])
			output_data = Calculation(data_line[i][1], weekday, output_data)
		i += 1

	for i in range(len(output_data)):
		print(round(output_data[i]))
	
if __name__ == "__main__":
	main()
