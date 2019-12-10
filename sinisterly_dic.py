#!/usr/bin/python

# Griffin Saiia, Gjs64
# Computer Security
# Underground Market Research
# github: https://github.com/gjbsaiia

login_url = "https://sinister.ly/User-login"
market_url = "https://sinister.ly/Forum-Regular-Sales?page="

# Here we have to map each xpath to a specific attribute we want to track
xpathDic = {
# thread index starts at 6
"user": '/html/body/div[3]/div[2]/table/tbody/tr[2]/td/form/table/tbody/tr[2]/td[2]/input',
"submit": '/html/body/div[3]/div[2]/table/tbody/tr[2]/td/form/table/tbody/tr[5]/td/input',
"password": '/html/body/div[3]/div[2]/table/tbody/tr[2]/td/form/table/tbody/tr[3]/td[2]/input',
"th_mptitle1": '/html/body/div[3]/div[2]/table/tbody/tr[',
"th_mptitle2": ']/td[3]/div/span/span[1]/a',
"th_title1": '/html/body/div[3]/div[2]/table/tbody/tr[',
"th_title2": ']/td[3]/div/span/span/a',
"th_user1": '/html/body/div[3]/div[2]/table/tbody/tr[',
"th_user2": ']/td[3]/div/span/div/a/span',
"th_replies1": '/html/body/div[3]/div[2]/table/tbody/tr[',
"th_replies2": ']/td[5]/a',
"th_views1": '/html/body/div[3]/div[2]/table/tbody/tr[',
"th_views2": ']/td[6]',
"th_rating1": '/html/body/div[3]/div[2]/table/tbody/tr[',
"th_rating2": ']/td[4]/div/ul/li[1]',
"th_time1": '/html/body/div[3]/div[2]/table/tbody/tr[',
"th_time2": ']/td[7]/span/span',
"th_content": '/html/body/div[3]/div[2]/div[5]/div[1]/div[2]/div[2]',
"next_fp": '/html/body/div[3]/div[2]/div[5]/div/a[6]',
"next_rest": '/html/body/div[3]/div[2]/div[5]/div/a[7]',
}
