#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import os
#dictionary_directory_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dictionary')
name = input("ノイズを変更したい辞書の名前を入力してください:")
txt_file = input('変更したいノイズ１欄のtxtファイル名を入力してください(.txtは含まず)：') # txtファイルを入力



file_path = os.path.abspath(__file__)

# Define path
PATH1 = file_path.replace('tools/gram_noise_changer.py', 'dictionary/cmudict-en-us.dict') # pocketsphinxの元の辞書の絶対パス
PATH2 = file_path.replace('tools/gram_noise_changer.py', 'dictionary/{}.dict').format(name) # pocketsphinxの作りたい辞書の絶対パス
PATH3 = file_path.replace('tools/gram_noise_changer.py', 'dictionary/{}.gram').format(name) # pocketsphinxの作りたい文法辞書の絶対パス
PATH4 = file_path.replace('tools/gram_noise_changer.py', 'dictionary/noise/{}.txt').format(txt_file) # 用意したノイズファイルの絶対パス

if os.path.exists(PATH2):
    if os.path.exists(PATH4):
        print("===============================================================")
        print("この辞書のノイズを変更します。")
        print("===============================================================")
        word_list = [] # 既存の辞書に含まれている単語を格納するリスト
        noise_list = []
          
        with open(PATH2, 'r') as f2:
            words = f2.readlines()
            for word in words:
                temp_word_list = word.split(' ') 
                word_list.append(temp_word_list[0])
            
        # pocketsphinxの元の辞書の単語のみをリストword1に格納
        with open(PATH1) as f1:
            lines1 = f1.readlines()
        word1 = []
        for l1 in lines1:
            word1.append(l1.split(' ')[0])

        nothing_noises = [] # 辞書になかった単語
        nothing_sentences = []
        write_noises = [] # 辞書に書き込んだ文章

        sentence_noise_list = []
        with open(PATH4, 'r') as f: 
            noises = f.readlines()
            for noise in noises:
                noise = noise.rstrip()
                sentence_noise_list.append(noise)
                
        new_noise_list = []
        for n1 in sentence_noise_list:
            new_noise_list += n1.split(' ')
            
        for n2 in new_noise_list:
            if n2 not in word_list:
                noise_list.append(n2)
        #print(noise_list)            
            
        # 文法辞書(.gram)に書き込み
        with open(PATH3) as f3:
            new_lines = f3.readlines()
            new_lines.pop()

        with open(PATH3, "w") as f3:
            i = 0
            while i < len(new_lines):
                f3.write(new_lines[i])
                i += 1
            f3.write("<noise> = ")
            start = False
            # nothing_noises_flagがtrueだとpocketsphinxの辞書にない単語が存在した、ということ
            nothing_noises_flag = False
            sentence_noise_list = list(set(sentence_noise_list))
            for s in sentence_noise_list:
                if nothing_noises != []:
                    for n in nothing_noises:
                        if n in s:
                            nothing_noises_flag = True
                if nothing_noises_flag == False:         
                    # 新規ノイズの追加        
                    if start == False:
                        start = True
                        f3.write(s)
                    # 2回目以降は文頭に " | " をつける
                    else:
                        f3.write(' | ' + s)
                    write_noises.append(s)
                else:nothing_sentences.append(s)
                
            f3.write(";")
            
                       


        # 単語辞書(.dict)に書き込み
        write_noises_list = []
        ws_list = []
        with open(PATH2, "a") as f2:
            for ws in write_noises:
                ws_list += ws.split(' ')
            for w in ws_list:
                if w not in word1:
                    noise_list.remove(w)
                    nothing_noises.append(w)
            for wsl in ws_list:
                if wsl not in word_list:
                    write_noises_list.append(wsl)

            for w in write_noises_list:
                w_index = word1.index(w)
                f2.write(lines1[w_index])
                if w + '(2)' in word1:
                    w_index = word1.index(w + '(2)')
                    f2.write(lines1[w_index])
                elif w + '(3)' in word1:
                    w_index = word1.index(w + '(3)')
                    f2.write(lines1[w_index])
                elif w + '(4)' in word1:
                    w_index = word1.index(w + '(4)')
                    f2.write(lines1[w_index])
        

        with open(PATH2) as f:
            lines = f.readlines()

        lines = sorted(lines)

        with open(PATH2, 'w') as f2:
            for l in lines:
                f2.write(l)

                
        if nothing_sentences != []:
            print("追加できなかった文章は")
            for j in nothing_sentences:
                print(j)

        # 見つからなかった単語の表示
        if nothing_noises != []:
            print("見つからなかった単語は")
            for j in nothing_noises:
                print(j)

        print("変更終了")
        print("===============================================================")
    else:
        print("ノイズファイル名が存在しません。")
        print("終了")
        print("===============================================================")    
else:
    print("辞書名が存在しません。")
    print("終了")
    print("===============================================================")
