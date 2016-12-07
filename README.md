# MFCC
音をMFCCへ変換する  

```
$python main.py [解析したいWAVのリスト(.txt)] [MFCC次元数(何も入れなければ12次元になります)]

out >>>
  cepstram.csv

```

同じディレクトリ内にMFCCをプロットしたグラフも生成されます(排除)．  
・test.wav から出力 test.png
<div style="text-align: left;">
<img src="https://github.com/Hiroyuky/mfcc/blob/master/test.png" alt="MFCC12testPicture" title="test.png" width="600px">  
</div>

## main.py
mfcc.pyを使う例題的なスクリプト  
解析したいwavデータのリストを記入したテキストファイルを渡す．  

## mfcc.py
wavファイルからMFCCを導出するためのスクリプトです．  

```python
def mfcc(filename, nceps=12):
  ...
  return ceps
```
メインが上記のコードなので，別スクリプトで使用する場合は

```python
import mfcc

mfcc.mfcc(wavdata)
```

で参照できます．  
以下のリンクを参考にしました．  
[メル周波数ケプストラム係数(MFCC)](http://aidiary.hatenablog.com/entry/20120225/1330179868)

## wavlist.txt
soundディレクトリ内のMFCCを抽出したいwavデータのリスト  

```
sound/01.wav
sound/02.wav
...

```

## sound
音をまとめたディレクトリ  
- test.wav
- a.wav

