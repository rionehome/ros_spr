#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import os
import csv

#dictionary_directory_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dictionary')
#q_a_directory_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Q&A')
name = input("作りたい辞書の名前を入力してください:")
csv_file = input('辞書にしたいcsvファイル名を入力してください(.csvは含まず)：') # csvファイルを入力
txt_file = input('加えたいノイズ１欄のtxtファイル名を入力してください(.txtは含まず)：') # txtファイルを入力


file_path = os.path.abspath(__file__)

# Define path
PATH0 = file_path.replace('tools/gram_maker_from_csv.py', 'dictionary/QandA/{}.csv').format(csv_file) # 用意したq&aファイルの絶対パス
PATH1 = file_path.replace('tools/gram_maker_from_csv.py', 'dictionary/cmudict-en-us.dict') # pocketsphinxの元の辞書の絶対パス
PATH2 = file_path.replace('tools/gram_maker_from_csv.py', 'dictionary/{}.dict').format(name) # pocketsphinxの作りたい辞書の絶対パス
PATH3 = file_path.replace('tools/gram_maker_from_csv.py', 'dictionary/{}.gram').format(name) # pocketsphinxの作りたい文法辞書の絶対パス
PATH4 = file_path.replace('tools/gram_maker_from_csv.py', 'dictionary/noise/{}.txt').format(txt_file) # 用意したノイズファイルの絶対パス

if os.path.exists(PATH2):
    print("同じ辞書名が存在します。")
    print("終了")
    print("===============================================================")
else:
    sentence_list = [] # 標準入力した文を格納するリスト
    word_list = [] # 文に含まれている単語を格納するリスト

    with open(PATH0, "r") as f0:
        for line in csv.reader(f0):
            sentence_list.append(str(line[0]))

    new_words_list = []
    for s in sentence_list:
        new_words_list += s.split(' ')
    # 重複している単語を省いてword_listに単語を格納する
    for word in new_words_list:
        if word not in word_list:
            word_list.append(word)

    # pocketsphinxの元の辞書の単語のみをリストword1に格納
    with open(PATH1) as f1:
        lines1 = f1.readlines()
    word1 = []
    for l1 in lines1:
        word1.append(l1.split(' ')[0])

    nothing_words = [] # 辞書になかった単語
    nothing_sentences = []
    write_sentence = [] # 辞書に書き込んだ文章

    for w in word_list:
        if w not in word1:
            nothing_words.append(w)
            
    noise_list = []
    with open(PATH4, 'r') as f: 
        noises = f.readlines()
        for noise in noises:
            noise = noise.rstrip()
            noise_list.append(noise)
        noise_list = list(set(noise_list))
            
    # 文法辞書(.gram)に書き込み
    with open(PATH3, "a") as f3:
        f3.write("#JSGF V1.0;\n")
        f3.write("grammar {};\n".format(name))
        f3.write("public <rule> = <command> | <noise>;\n")
        f3.write("<command> = ")

        start = False
        # nothing_words_flagがtrueだとpocketsphinxの辞書にない単語が存在した、ということ
        nothing_words_flag = False
        for s in sentence_list:
            if nothing_words != []:
                for n in nothing_words:
                    if n in s:
                        nothing_words_flag = True
            if nothing_words_flag == False:
                # 最初の１回目のときのみ、"start == False"
                if start == False:
                    start = True
                    f3.write(s)
                # 2回目以降は文頭に " | " をつける
                else:
                    f3.write(' | ' + s)
                write_sentence.append(s)
            # 知らない単語が含まれた文章のときelseに入り、nothing_sentencesに格納
            else:
                nothing_sentences.append(s)
            nothing_words_flag = False
        f3.write(";\n")
        
        # ノイズの追加
        start = False
        f3.write("<noise> = ")
        for noise in noise_list:
            if start == False:
                start = True
                f3.write(noise)
            # 2回目以降は文頭に " | " をつける
            else:
                f3.write(' | ' + noise)
            write_sentence.append(noise)
        f3.write(";")

    # 単語辞書(.dict)に書き込み
    write_word_list = []
    ws_list = []
    with open(PATH2, "a") as f2:
        for ws in write_sentence:
            ws_list += ws.split(' ')

        for wsl in ws_list:
            if wsl not in write_word_list:
                write_word_list.append(wsl)
                
        # １つ単語の発音は２つ以上あったりする。
        # 例： to T UW   to(2) T IH   to(3) T AH
        
        for w in write_word_list:
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
    if nothing_words != []:
        print("見つからなかった単語は")
        for j in nothing_words:
            print(j)
    print("辞書化終了")
