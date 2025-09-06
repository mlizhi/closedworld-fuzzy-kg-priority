// 1) 四类实体（用户故事/用户/需求/目标）
LOAD CSV WITH HEADERS FROM 'file:///User_story278.csv' AS row
MERGE (us:UserStory {id: row.`用户故事`})
MERGE (u:User {name: row.`用户`})
MERGE (r:Requirement {name: row.`需求`})
MERGE (g:Goal {name: COALESCE(row.`目标`, 'NoGoal')});

// 2) 三元组
LOAD CSV WITH HEADERS FROM 'file:///User_story278.csv' AS row
MATCH (us:UserStory {id: row.`用户故事`}) MATCH (g:Goal {name: row.`目标`})
MERGE (us)-[:Defines]->(g);

LOAD CSV WITH HEADERS FROM 'file:///User_story278.csv' AS row
MATCH (u:User {name: row.`用户`}) MATCH (r:Requirement {name: row.`需求`})
MERGE (u)-[:Proposes]->(r);

LOAD CSV WITH HEADERS FROM 'file:///User_story278.csv' AS row
MATCH (g:Goal {name: row.`目标`}) MATCH (r:Requirement {name: row.`需求`})
MERGE (g)-[:Specifies]->(r);

// 3) 需求-需求
LOAD CSV WITH HEADERS FROM 'file:///RE_RE.csv' AS row
WITH row WHERE row.需求1 IS NOT NULL AND row.需求2 IS NOT NULL
MERGE (a:Requirement {name: row.需求1})
MERGE (b:Requirement {name: row.需求2})
MERGE (a)-[:RelatedTo]->(b);

// 4) 名称统一
MATCH (n) WHERE NOT EXISTS(n.name) AND EXISTS(n.id) SET n.name = n.id;

// 5) 导出三元组（示例查询）
MATCH (n)-[r]->(m) RETURN n.name AS Subject, type(r) AS Predicate, m.name AS Object, labels(n) AS SubjectLabels, labels(m) AS ObjectLabels LIMIT 50;
