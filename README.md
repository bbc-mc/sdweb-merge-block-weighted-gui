# Merge Block Weighted - GUI

- This is Extension for [AUTOMATIC1111's Stable Diffusion Web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- Implementation GUI of [Merge Block Weighted] (https://note.com/kohya_ss/n/n9a485a066d5b) idea by kohya_ss
   - change some part of script to adjust for AUTO1111, basic method is not changed.



# Recent Update

- 2022/12/25: Add new feature and new UI
  
   - Read "README" [English](README_each.md)/[日本語](README_each.ja.md)

# 

# What is this

![](misc/bw01-1.png)

## How to Install

- Go to `Extensions` tab on your web UI
- `Install from URL` with this repo URL
- Install
- Restart Web UI

## How to use

### Select `model_A` and `model_B`, and input `Output model name`

![](misc/bw02.png)

- if checkpoint is updated, push `Reload Checkpoint` button to reload Dropdown choises.

### Set merge ratio for each block of U-Net

- Select Presets by Dropdown
  
  ![](misc/bw08.png)
  
  You can manage presets on tsv file (tab separated file) at `extention/<this extension>/csv/preset.tsv`
  ![](misc/bw06.png)

- or Input at GUI Slider

![](misc/bw03.png)

- "INxx" is input blocks. 12 blocks

- "M00" is middle block. 1 block

- "OUTxx" is output blocks. 12 blocks

![](misc/bw04.png)

- You can write your weights in "Textbox" and "Apply block weight from text"
  
   - Weights must have 25 values and comma separated

### Setting values

![](misc/bw05.png)

- set "base_alpha"

| base_alpha |                                                                   |
| ---------- | ----------------------------------------------------------------- |
| 0          | merged model uses (Text Encoder、Auto Encoder) 100% from `model_A` |
| 1          | marged model uses (Text Encoder、Auto Encoder) 100% from `model_B` |

### Other settings

| Settings                     |                                                                |
| ---------------------------- | -------------------------------------------------------------- |
| verbose console output       | Check true, if want to see some additional info on CLI         |
| Allow overwrite output-model | Check true, if allow overwrite model file which has same name. |

- Merged output is saved in normal "Model" folder.

## Other function

### Save Merge Log

- save log about operated merge, as below,
  ![](misc/bw07.png)

- log is saved at `extension/<this extension>/csv/history.tsv`

## Sample/Example

- kohya_ss さんのテストを再現してみる
  
   - Compare SD15 and WD13 / Stable Diffusion 1.5 と WD 1.3 の結果を見る
      - ※元記事は SD14 を使用 (WD13はSD14ベース)
   - see also [Stable DiffusionのモデルをU-Netの深さに応じて比率を変えてマージする｜Kohya S.｜note](https://note.com/kohya_ss/n/n9a485a066d5b)

- 準備する/マージして作るモデルは、以下の通り / Prepare models as below,
  
  | Model Name      |                                                                   |
  | --------------- | ----------------------------------------------------------------- |
  | sd-v1.5-pruned  | Stable Diffusion v1.5                                             |
  | wd-v1.3-float32 | wd v1.3-float32                                                   |
  | SD15-WD13-ws50  | 通常マージしたもの<br>SD15 + WD13, 0.5 # Weighted sum 0.5                  |
  | bw-merge1-2-2   | Merge Block Weighted<br>SD15 and WD13. base_alpha=1<br>weightは後述1 |
  | bw-merge2-2-2   | Merge Block Weighted<br>SD15 and WD13. base_alpha=0<br>weightは後述2 |

- テスト用のGeneration Info, Seedは 1～4 の4つ
  
  ```
  masterpiece, best quality, beautiful anime girl, school uniform, strong rim light, intense shadows, highly detailed, cinematic lighting, taken by Canon EOS 5D Simga Art Lens 50mm f1.8 ISO 100 Shutter Speed 1000
  Negative prompt: lowres, bad anatomy, bad hands, error, missing fingers, cropped, worst quality, low quality, normal quality, jpeg artifacts, blurry
  Steps: 40, Sampler: Euler a, CFG scale: 7, Seed: 1, Face restoration: CodeFormer, Size: 512x512, Batch size: 4
  ```

### result (x/y)

![](misc/xy_plus-0000-40-7_1.png)

- 変化傾向は、
  
   - bw-merge1 で、顔立ちがややアニメ化 (sd15-wd13-ws50と比較して)
   - bw-merge2 で、ややリアル風（特に seed=3 の目が良い）

- おおまかに見て、kohya_ss さんの結果と同様の方向性になった。実装は問題ないと判断する

### 後述1: weight1

```
1, 0.9166666667, 0.8333333333, 0.75, 0.6666666667,
0.5833333333, 0.5, 0.4166666667, 0.3333333333, 0.25, 0.1666666667,
0.0833333333,
0,
0.0833333333,0.1666666667,0.25,0.3333333333,0.4166666667,0.5,
0.5833333333,0.6666666667,0.75,0.8333333333,0.9166666667,1.0
```

### 後述2: weight2

```
0,0.0833333333,0.1666666667,0.25,0.3333333333,0.4166666667,0.5,
0.5833333333,0.6666666667,0.75,0.8333333333,0.9166666667,
1.0,
0.9166666667, 0.8333333333, 0.75, 0.6666666667,
0.5833333333, 0.5, 0.4166666667, 0.3333333333, 0.25, 0.1666666667,
0.0833333333, 0
```

## Special Thanks

- kohya_ss, [Stable DiffusionのモデルをU-Netの深さに応じて比率を変えてマージする｜Kohya S.｜note](https://note.com/kohya_ss/n/n9a485a066d5b)
