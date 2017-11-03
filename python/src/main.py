#その日が何曜日かを判定する関数Weekdy_judge
def Weekday_judge(date):
	import datetime as dt
	new_date=dt.datetime.strptime(date,"%Y/%m/%d")
	#月曜日~日曜日:0~6
	weekday=new_date.weekday()
	return weekday
	
#1週間経ったかを判定し、週合計労働時間Total_weekを0にする関数Check_aweek
def Check_aweek(date, weekday):
	global Total_week
	global keep_week_day
	day = date.split("/")
	'''
	weekdayには0~6の整数(月曜日~日曜日)が代入されている。
	keep_week_dayには最後に読み込んだ曜日と日付が代入されている。
	'''
	if keep_week_day[0] >= weekday:
		Total_week=0
	elif keep_week_day[1]+7 <= int(day[2]):
		Total_week=0
	else:
		pass
	keep_week_day[0] = weekday
	keep_week_day[1] = int(day[2])
	return 0

#法定内残業時間数(時)、法定外残業時間数(時)、深夜残業時間数(時)、所定休日労働時間数(時)、法定休日労働時間数(時)を計算してmainに渡す関数Calculation
def Calculation(time, weekday, output_data):
	global Total_week
	over_24oclock = 0		#24時以降の労働時間
	total_day = 0			#1日の労働時間
	unemployed_time = 0	#不就労働時間
	
	time = time.split()
	for i in range(len(time)):
		time[i] = time[i].split("-")
		time1 = list(map(float, time[i][0].split(":")))
		time2 = list(map(float, time[i][1].split(":")))
		start = time1[0] + time1[1]/60
		end = time2[0] + time2[1]/60
		total_day += (end - start)
		#22時以降の勤務を確認
		if end > 22.00:	
			output_data[2] += Night_overtime(start, end)
			#24時以降の勤務を確認
			if end >24.00:
				over_24oclock += Check_over24(start, end)
		#不就労働時間を確認
		if (start >= 8.00 and end <= 12.00):
			unemployed_time += (4.00-(end-start))
		if (start >= 13.00 and end <= 16.00):
			unemployed_time += (3.00-(end-start))		
	Total_week += total_day
	#月〜木曜日
	if weekday <4:	
		#週40時間以内の勤務の場合
		if Total_week <40:
			output_data = Check_overtime(total_day, output_data, unemployed_time)
		#週40時間を超過した勤務の場合
		else:
			output_data[1] += (Total_week - 40)
			total_day -= (Total_week - 40)
			output_data = Check_overtime(total_day, output_data, unemployed_time)
	#金曜日
	elif weekday == 4:
			#24時以降に勤務がある場合
			if over_24oclock !=0:
				Total_week -= over_24oclock	#24時以降は所定休日労働時間なので、週の労働時間からは省く
				#週40時間以内の勤務の場合
				if Total_week < 40:
					output_data[3] += over_24oclock
					total_day -= over_24oclock
					output_data = Check_overtime(total_day, output_data, unemployed_time)
				#週40時間を超過した勤務の場合
				else:
					output_data[3] += over_24oclock
					total_day -= over_24oclock
					output_data[1] += (Total_week - 40)
					total_day -= (Total_week - 40)	
					output_data = Check_overtime(total_day, output_data, unemployed_time)			
			#24時以降に勤務がない場合
			else:
				#週40時間以内の勤務の場合
				if Total_week <40:
					output_data = Check_overtime(total_day, output_data, unemployed_time)
				#週40時間を超過した勤務の場合
				else:
					output_data[1] += (Total_week - 40)
					total_day -= (Total_week - 40)
					output_data = Check_overtime(total_day, output_data, unemployed_time)
	#土曜日
	elif weekday == 5:
		#24時以降に勤務がある場合
		if over_24oclock !=0:
			output_data[4] += over_24oclock
			output_data[3] += (total_day - over_24oclock)
		#24時以降に勤務がない場合
		else:
			output_data[3] += total_day
	#日曜日
	elif weekday == 6: 
		output_data[4] += total_day
	
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
		total_over24 += (end-24.00)
	#開始時刻が24時以降の場合
	else:
		total_over24 += (end - start)
	return total_over24


#法定内/法定外残業時間を確認する関数Check_overtime
def Check_overtime(total, output_data, unemployed):
	#勤務時間が7時間以上8時間以内の場合
	if total >7.00 and total <= 8.00:
		output_data[0] += (total - 7.00 + unemployed)
	#勤務時間が8時間以上の場合
	elif total > 8.00:
		output_data[0] += (1.00+unemployed)
		output_data[1] += (total - 8.00)
	#勤務時間が7時間未満で不就労働時間がある場合
	elif total <= 7.00 and unemployed!=0:
		output_data[0] += unemployed
	else:
		pass
	return output_data

#前の月のYYYY/MM文字列を作成する関数Mk_last_month
def Mk_last_month(date):
	global Check_bug
	a = date.split("/")
	a[1] = int(a[1])
	if a[1] == 1:
		last_month = a[0]+"/12"
	
	elif a[1] <= 12:
		a[1] = str(a[1]-1)
		last_month = a[0]+"/"+a[1].zfill(2)
	else:
		Check_bug = False
	return last_month

#前の月の労働時間を計算する関数Count_LMWT
def Count_LMWT(time):
	global Total_week
	total = 0
	time = time.split()
	for i in range(len(time)):
		time[i] = time[i].split("-")
		time1 = list(map(float, time[i][0].split(":")))
		time2 = list(map(float, time[i][1].split(":")))
		start = time1[0] + time1[1]/60
		end = time2[0] + time2[1]/60
		total += (end - start)
	Total_week += total
	return 0


Total_week=0				#週合計労働時間
keep_week_day=[0, 0]		#最後に読み込んだ[曜日,日付]
Check_bug=True			#バグ
def main():
	import sys
	global Check_bug
	global keep_week_day
	data_line={}
	#入力データの読み込み
	try:
		a=input().strip("\n")
		data_line[0] = a
		i=1
		while True:
			a=input().strip("\n")
			data_line[i] = a.split(" ",1)
			i+=1
	except EOFError:
		pass

	#output_data : 法定内残業時間数(時)、法定外残業時間数(時)、深夜残業時間数(時)、所定休日労働時間数(時)、法定休日労働時間数(時)
	output_data=[0, 0, 0, 0, 0]
	now_month = data_line[0]
	last_month=Mk_last_month(now_month)
	i=1
	while i<len(data_line):
		weekday=Weekday_judge(data_line[i][0])
		#対象月の場合
		if now_month in data_line[i][0]:
			Check_aweek(data_line[i][0], weekday)
			output_data = Calculation(data_line[i][1], weekday, output_data)
		#前月だった場合、週合計労働時間のみ取得する
		elif last_month in data_line[i][0]:
			keep_week_day[0] = weekday
			Count_LMWT(data_line[i][1])
		else:
			Check_bug=False
		i += 1
	
	#計算結果の出力
	for i in range(len(output_data)):
		print(round(output_data[i]))
	
	#終了コードの設定
	if Check_bug:
		sys.exit(0)
	else:
		sys.exit(1)

	
if __name__ == "__main__":
	main()
