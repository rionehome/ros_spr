#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import os
#dictionary_directory_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dictionary')
name = input("作りたい辞書の名前を入力してください:")


file_path = os.path.abspath(__file__)

# Define path
PATH1 = file_path.replace('tools/gram_maker_by_input.py', 'dictionary/cmudict-en-us.dict') # pocketsphinxの元の辞書の絶対パス
PATH2 = file_path.replace('tools/gram_maker_by_input.py', 'dictionary/{}.dict').format(name) # pocketsphinxの作りたい辞書の絶対パス
PATH3 = file_path.replace('tools/gram_maker_by_input.py', 'dictionary/{}.gram').format(name) # pocketsphinxの作りたい文法辞書の絶対パス

if os.path.exists(PATH2):
	print("同じ辞書名が存在します。")
	print("終了")
	print("===============================================================")
else:
	print('文章を入力してください + Enter')
	print('(終了する場合はCtrl-C)')
	print("===============================================================")
	sentence_list = [] # 標準入力した文を格納するリスト
	word_list = [] # 文に含まれている単語を格納するリスト
	try:
		while 1:
			sentence = input() # ファイルに追加する文章を標準入力
			sentence = sentence.lower() # 全文小文字化
			sentence = sentence.rstrip() # 改行コード削除
			sentence_list.append(sentence)

	except KeyboardInterrupt:
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

		# 文法辞書(.gram)に書き込み
		with open(PATH3, "a") as f3:
			f3.write("#JSGF V1.0;\n")
			f3.write("grammar {};\n".format(name))
			f3.write("public <rule> = <command>;\n")
			f3.write("<command> = ")

			start = False
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
