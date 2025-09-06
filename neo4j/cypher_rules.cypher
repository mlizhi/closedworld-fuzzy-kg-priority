// 导入 FRKG_label.csv（带 Fuzzy 与 Labels）
LOAD CSV WITH HEADERS FROM 'file:///FRKG_label.csv' AS row
WITH row,
     SPLIT(REPLACE(REPLACE(row.SubjectLabels, '[', ''), ']', ''), ',') AS subjectLabels,
     SPLIT(REPLACE(REPLACE(row.ObjectLabels, '[', ''), ']', ''), ',') AS objectLabels
MERGE (s:Entity {name: row.Subject})
CALL apoc.create.addLabels(s, subjectLabels) YIELD node AS sn
MERGE (o:Entity {name: row.Object})
CALL apoc.create.addLabels(o, objectLabels) YIELD node AS on
MERGE (sn)-[r:`Defines`]->(on)
ON CREATE SET r.Fuzzy = COALESCE(toFloat(row.Fuzzy), 1);

// FSTO^siso
CALL apoc.periodic.iterate(
  "MATCH (x)-[r]->(y) MATCH (z)-[p]->(x)
   RETURN x,y,z,r,p,COALESCE(r.Fuzzy,1) AS a,COALESCE(p.Fuzzy,1) AS b",
  "MERGE (z)-[n:Inferred {type:type(r),rule:'FSTO_siso',Fuzzy:a*b}]->(y)",
  {batchSize:1000}
);

// FSTO^simo
CALL apoc.periodic.iterate(
  "MATCH (x)-[r]->(y) MATCH (x)-[p]->(z)
   RETURN x,y,z,r,p,COALESCE(r.Fuzzy,1) AS a,COALESCE(p.Fuzzy,1) AS b",
  "MERGE (z)-[n:Inferred {type:type(r),rule:'FSTO_simo',Fuzzy:a*b}]->(y)",
  {batchSize:1000}
);

// FSTO^miso
CALL apoc.periodic.iterate(
  "MATCH (x)-[r1]->(y) MATCH (z1)-[r2]->(x)
   RETURN x,y,z1,r1,r2,COALESCE(r1.Fuzzy,1)*COALESCE(r2.Fuzzy,1) AS f",
  "MERGE (z1)-[n:Inferred {type:type(r1),rule:'FSTO_miso',Fuzzy:f}]->(y)",
  {batchSize:1000}
);

// FSTO^mimo
CALL apoc.periodic.iterate(
  "MATCH (x)-[r1]->(y) MATCH (z1)-[r2]->(x) MATCH (z2)-[r3]->(y)
   RETURN x,y,z1,z2,r1,r2,r3,
          COALESCE(r1.Fuzzy,1)*COALESCE(r2.Fuzzy,1)*COALESCE(r3.Fuzzy,1) AS f",
  "MERGE (z1)-[n1:Inferred {type:type(r1),rule:'FSTO_mimo',Fuzzy:f}]->(y)
   MERGE (z2)-[n2:Inferred {type:type(r1),rule:'FSTO_mimo',Fuzzy:f}]->(x)",
  {batchSize:1000}
);

// 结果检查
MATCH (n)-[r:Inferred]->(m)
RETURN n.name AS Start, r.rule AS Rule, r.Fuzzy AS Fuzzy, type(r) AS Type, m.name AS End LIMIT 20;

// 统计
MATCH (n)-[r:Inferred]->(m)
RETURN r.type AS RelationshipType, r.rule AS Rule, COUNT(*) AS Count
ORDER BY Count DESC;
