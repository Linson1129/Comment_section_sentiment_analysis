@echo off
REM 运行评论分析脚本，即使报错也继续
python comment_analysis\information_get.py || echo information_get.py 执行出错，继续下一步
python comment_analysis\analysis.py
REM 运行图表生成脚本
python graph\create_graph.py

REM 打开生成的图片（如果有）
start result.png

pause