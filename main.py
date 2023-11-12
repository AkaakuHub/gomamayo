import MeCab
import alkana

def judge_gomamayo(content):
  mecab = MeCab.Tagger()
  m_result = mecab.parse(content).splitlines()[:-1]
  pronounce = []
  for line in m_result:
    pro = line.split("\t")[1]
    alk = alkana.get_kana(pro.lower())
    if len(pro) != 0:
      pronounce.append(alk if alk != None else pro)
    # ☆等は読みが空白のため除去
 
  res = "違います。"

  for i in range(len(pronounce) - 1):
    # 高次ゴママヨ
    for j in range(min(len(pronounce[i]), len(pronounce[i + 1]))-1):
      if pronounce[i][-2 - j : -1] == pronounce[i + 1][0 : j + 1]:
        res = "高次ゴママヨです。"
        break
        
    # 低次ゴママヨ
    if pronounce[i][-1] == pronounce[i+1][0]:
      res = "ゴママヨです。"
  
  return (res, pronounce)

if __name__ == '__main__':
  print(judge_gomamayo('ガーリック食った')) # => ('ゴママヨです。', ['ガーリック', 'クッ', 'タ'])
