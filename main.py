import MeCab
import alkana
import re
import jaconv

def judge_gomamayo(content):
  mecab = MeCab.Tagger()
  m_result = mecab.parse(content).splitlines()[:-1]
  pronounce = []
  goma_idx = []
  for line in m_result:
    origin = jaconv.kata2hira(line.split("\t")[0])
    # originがひらがなだけならそのまま追加
    if re.compile("[ぁ-ん]+").fullmatch(origin):
      pronounce.append(origin)
    else:
      pro = jaconv.kata2hira(line.split("\t")[1])
      read = jaconv.kata2hira(line.split("\t")[2])
      part = line.split("\t")[4]
      # 「今日は」->「きょうわ」となるようにする
      # 基本はreadを採用だが、「は」を「wa」と呼ぶときは変える
      word = pro if ("助詞" in part) or ("動詞" in part) else read
      alk = alkana.get_kana(word.lower())
      if len(pro) != 0:
        pronounce.append(jaconv.kata2hira(alk) if alk != None else word)
      # 記号等は読みが空白のため除去

  res = "違います。"

  for i in range(len(pronounce) - 1):
    # 高次ゴママヨ
    for j in range(min(len(pronounce[i]), len(pronounce[i + 1]))-1):
      if pronounce[i][-2 - j : -1] == pronounce[i + 1][0 : j + 1]:
        res = "高次ゴママヨです。"
        goma_idx.append(i+0.5)
        break

    # 低次ゴママヨ
    if pronounce[i][-1] == pronounce[i+1][0]:
      res = "ゴママヨです。"
      goma_idx.append(i+0.5)

  # n項ゴママヨの判定
  if len(goma_idx) > 1:
    nominal = 1
    max_nominal = 1
    for i in range(len(goma_idx) - 1):
      if goma_idx[i] + 1 == goma_idx[i+1]:
        nominal += 1
      else:
        max_nominal = max(max_nominal, nominal)
        nominal = 1
    
    max_nominal = max(max_nominal, nominal)

    if max_nominal > 1:
      res = f"{max_nominal}項ゴママヨです。"

  return (res, pronounce)

if __name__ == '__main__':
  print(judge_gomamayo('アリス「モモイ!ざくざくクランチチョコです!!!!ゴマモクで買いましょう!!!!!」'))
