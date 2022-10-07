for i_time, table_name in zip(range(2,range_table), table_list):
                    if i_time == 0 or i_time == 1:

                        ## //*[@id="ata2"]/table/tbody/tr[2]/td[1]/span[2]/a　　指定path
                        ## //*[@id="ata0"]/table/tbody/tr[2]/td[1]/span[3]/a   クリックしたいpath
                        ## //*[@id="ata0"]/table/tbody/tr[3]/td[1]/span[3]/a
  

                        ## //*[@id="ahead2"]/a
                        ## //*[@id="ata2"]/table/tbody/tr[2]/td[1]/span[3]/a
                        ## all_XPATH_time: //*[@id="ata2"]/table/tbody/tr[2]/td[1]/span[2]/a
                        continue
                    else:
                        browser.find_element_by_xpath(f'//*[@id="ahead{i}"]/a').click()
                        wait_time = float('{:.3f}'.format((10- 8) * np.random.rand() + 8))
                        sleep(wait_time)

                        all_XPATH_time = front_path+str(i)+middle_path+str(i_time)+back_path
                        print(f"all_XPATH_time: {all_XPATH_time}")
                        browser.find_element_by_xpath(all_XPATH_time).click()
                        wait_time = float('{:.3f}'.format((10- 9) * np.random.rand() + 9))
                        sleep(wait_time)

                        time_days_value = i + 1
                        front_path_days = XPATH_time_days[0]
                        back_path_days = XPATH_time_days[1]
                        all_XPATH_time_days = front_path_days + str(time_days_value) + back_path_days
                        browser.find_element_by_xpath(all_XPATH_time_days).click()
                        wait_time = float('{:.3f}'.format((12- 10) * np.random.rand() +10))
                        sleep(wait_time)
                        

                        elems_time = browser.find_elements_by_tag_name("tr")
                        values_time = []
                        for elem_time in elems_time:
                            value_time = elem_time.text
                            value_time_s= value_time.split()
                            values_time.append(value_time_s)

                        df_time = pd.DataFrame(values_time)

                        df_time = df_time[1:table_len+1]
                        df_time.columns = ["大当り回数", "時間", "スタート回数"]
                        
                        table_dir = f"/Users/tomoyasu/dev/AIP/save_data/data/{file_name}/time/table_{table_name}"
                        if not os.path.exists(table_dir):
                            os.makedirs(table_dir)

                        df_time.to_csv(f"/Users/tomoyasu/dev/AIP/save_data/data/{file_name}/time/table_{table_name}/{before_text_date}.csv")

                        
                    
                        XPATH_list = '//*[@id="pankuzu"]/li[2]/a'
                        browser.find_element_by_xpath(XPATH_list).click()
                        wait_time = float('{:.3f}'.format((10- 8) * np.random.rand() + 8))
                        sleep(wait_time)
                
                print(f"{i}日目のデータ取得が終わりました。")
            
            # browserを閉じる
            browser.quit()

            start_time = time()

            wait_time = random.randint(500,  700)
            print("10minほどの休憩に入ります...")
            sleep(wait_time)

            rest_time = time() - start_time
            print("休憩時間：",rest_time)

    
        print("--------------------------")
        print("完了....次の機種に移ります...")