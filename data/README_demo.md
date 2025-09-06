\# 数据说明（UAV 案例）



\## 1. 原始数据（raw/）

\- 02.用户故事及其类类别278条.xls  \*\*TODO: 放置或提供可开源版本\*\*



\## 2. 处理后数据（processed/）

\- User\_story278.csv  

&nbsp; 字段：用户故事, 用户, 需求, 目标, 所属类别

\- RE\_RE.csv  

&nbsp; 字段：需求1, 需求2  （表示 RelatedTo）

\- FRKG\_label.csv  

&nbsp; 字段：Subject, Predicate, Object, SubjectLabels, ObjectLabels, Fuzzy  

&nbsp; 说明：Fuzzy=μ^α（谓词模糊度）。若无则为1。



\## 3. FRKG 三元组（带 μ^α/μ^β）

\- triple\_with\_fuzzy.csv

