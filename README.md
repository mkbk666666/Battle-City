<!--
 * @Author: mkbk666666 3400835105@qq.com
 * @Date: 2025-03-08 23:28:34
 * @LastEditors: mkbk666666 3400835105@qq.com
 * @LastEditTime: 2025-03-08 23:42:25
 * @FilePath: \pythonProject\README.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# 坦克大战游戏

一个基于Python和Pygame的经典坦克大战游戏。

## 游戏特点

- 经典的坦克大战玩法
- 多种道具系统（生命恢复、速度提升、护盾）
- 关卡进阶系统
- 音效和背景音乐（可选）
- 游戏菜单和暂停功能

## 操作说明

- 方向键：控制坦克移动
- 空格键：发射子弹
- P键：暂停/继续游戏
- R键：游戏结束后重新开始
- ESC键：退出游戏

## 游戏元素

- 绿色坦克：玩家
- 红色坦克：敌人
- 灰色方块：可破坏墙
- 深灰色方块：不可破坏墙
- 道具：
  - 绿色/红色：生命恢复
  - 蓝色/白色：速度提升
  - 黄色/蓝色：护盾

## 安装与运行

1. 确保已安装Python和Pygame
   ```
   pip install pygame
   ```

2. 运行游戏：
   ```
   python 坦克大战.py
   ```

3. (可选) 添加音效：
   创建sounds文件夹并放入以下音效文件以启用游戏音效：
   - shoot.wav：射击音效
   - explosion.wav：爆炸音效
   - hit.wav：击中音效
   - power_up.wav：获得道具音效
   - game_over.wav：游戏结束音效
   - level_up.wav：升级音效
   - background.mp3：背景音乐

   注意：如果没有音效文件，游戏会自动在无声模式下运行。

## 开发信息

- 语言：Python
- 框架：Pygame
- 开发者：[mkbk]

## 未来计划

- 添加更多类型的敌人
- 实现多人游戏模式
- 添加更多类型的武器和子弹
- 设计更多关卡 