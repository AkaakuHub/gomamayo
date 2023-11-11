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
    
  is_gomamayo = False
  is_highlevel = False

  for i in range(len(pronounce) - 1):
    # 高次ゴママヨ
    for j in range(min(len(pronounce[i]), len(pronounce[i + 1]))-1):
      if pronounce[i][-2 - j : -1] == pronounce[i + 1][0 : j + 1]:
        is_highlevel = True
        break
        
    # 低次ゴママヨ
    if pronounce[i][-1] == pronounce[i+1][0]:
      is_gomamayo = True

  bool = is_gomamayo or is_highlevel
  res = ""
  if is_highlevel:
    res = "高次ゴママヨです。"
  elif is_gomamayo:
    res = "ゴママヨです。"
  
  return (res if bool else "違います。", pronounce)

if __name__ == '__main__':
  print(judge_gomamayo('ガーリック食った')) # => ('ゴママヨです。', ['ガーリック', 'クッ', 'タ'])
