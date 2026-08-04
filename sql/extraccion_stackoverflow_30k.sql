/*
-- PROYECTO: Sistema de Clasificación de Soporte Técnico (NLP)
-- ARCHIVO: extraccion_stackoverflow_30k.sql
-- DESCRIPCIÓN: Extracción balanceada de 30,000 publicaciones de Stack Overflow 
-- (3,000 registros por categoría) utilizando Data Explorer / T-SQL.
-- PLATAFORMA: Stack Exchange Data Explorer (SEDE)
*/

SELECT * FROM (
    SELECT TOP 3000 Title + ' ' + Body AS texto_completo, 'Frontend' AS categoria
    FROM Posts
    WHERE Id > 70000000
      AND (Tags LIKE '%<reactjs>%' OR Tags LIKE '%<html>%' OR Tags LIKE '%<css>%' OR Tags LIKE '%<javascript>%')
      AND PostTypeId = 1 AND AnswerCount > 0
    ORDER BY ViewCount DESC
) AS f

UNION ALL

SELECT * FROM (
    SELECT TOP 3000 Title + ' ' + Body AS texto_completo, 'Backend' AS categoria
    FROM Posts
    WHERE Id > 70000000
      AND (Tags LIKE '%<node.js>%' OR Tags LIKE '%<django>%' OR Tags LIKE '%<spring-boot>%' OR Tags LIKE '%<express>%')
      AND PostTypeId = 1 AND AnswerCount > 0
    ORDER BY ViewCount DESC
) AS b

UNION ALL

SELECT * FROM (
    SELECT TOP 3000 Title + ' ' + Body AS texto_completo, 'Bases de Datos' AS categoria
    FROM Posts
    WHERE Id > 70000000
      AND (Tags LIKE '%<sql>%' OR Tags LIKE '%<mysql>%' OR Tags LIKE '%<postgresql>%' OR Tags LIKE '%<mongodb>%')
      AND PostTypeId = 1 AND AnswerCount > 0
    ORDER BY ViewCount DESC
) AS bd

UNION ALL

SELECT * FROM (
    SELECT TOP 3000 Title + ' ' + Body AS texto_completo, 'Cloud' AS categoria
    FROM Posts
    WHERE Id > 70000000
      AND (Tags LIKE '%<docker>%' OR Tags LIKE '%<kubernetes>%' OR Tags LIKE '%<aws>%' OR Tags LIKE '%<azure>%')
      AND PostTypeId = 1 AND AnswerCount > 0
    ORDER BY ViewCount DESC
) AS c

UNION ALL

SELECT * FROM (
    SELECT TOP 3000 Title + ' ' + Body AS texto_completo, 'Ciberseguridad' AS categoria
    FROM Posts
    WHERE Id > 70000000
      AND (Tags LIKE '%<security>%' OR Tags LIKE '%<encryption>%' OR Tags LIKE '%<authentication>%' OR Tags LIKE '%<ssl>%')
      AND PostTypeId = 1 AND AnswerCount > 0
    ORDER BY ViewCount DESC
) AS cs

UNION ALL

SELECT * FROM (
    SELECT TOP 3000 Title + ' ' + Body AS texto_completo, 'Data Science' AS categoria
    FROM Posts
    WHERE Id > 70000000
      AND (Tags LIKE '%<machine-learning>%' OR Tags LIKE '%<pandas>%' OR Tags LIKE '%<scikit-learn>%' OR Tags LIKE '%<nlp>%')
      AND PostTypeId = 1 AND AnswerCount > 0
    ORDER BY ViewCount DESC
) AS ds

UNION ALL

SELECT * FROM (
    SELECT TOP 3000 Title + ' ' + Body AS texto_completo, 'Matematicas' AS categoria
    FROM Posts
    WHERE Id > 70000000
      AND (Tags LIKE '%<math>%' OR Tags LIKE '%<algorithm>%' OR Tags LIKE '%<linear-algebra>%' OR Tags LIKE '%<graph-theory>%')
      AND PostTypeId = 1 AND AnswerCount > 0
    ORDER BY ViewCount DESC
) AS m

UNION ALL

SELECT * FROM (
    SELECT TOP 3000 Title + ' ' + Body AS texto_completo, 'UX/UI' AS categoria
    FROM Posts
    WHERE Id > 70000000
      AND (Tags LIKE '%<user-interface>%' OR Tags LIKE '%<ux>%' OR Tags LIKE '%<ui-design>%' OR Tags LIKE '%<css-animations>%')
      AND PostTypeId = 1 AND AnswerCount > 0
    ORDER BY ViewCount DESC
) AS ux

UNION ALL

SELECT * FROM (
    SELECT TOP 3000 Title + ' ' + Body AS texto_completo, 'Desarrollo Movil' AS categoria
    FROM Posts
    WHERE Id > 70000000
      AND (Tags LIKE '%<android>%' OR Tags LIKE '%<ios>%' OR Tags LIKE '%<flutter>%' OR Tags LIKE '%<react-native>%')
      AND PostTypeId = 1 AND AnswerCount > 0
    ORDER BY ViewCount DESC
) AS mov

UNION ALL

SELECT * FROM (
    SELECT TOP 3000 Title + ' ' + Body AS texto_completo, 'QA y Testing' AS categoria
    FROM Posts
    WHERE Id > 70000000
      AND (Tags LIKE '%<unit-testing>%' OR Tags LIKE '%<selenium>%' OR Tags LIKE '%<jest>%' OR Tags LIKE '%<pytest>%')
      AND PostTypeId = 1 AND AnswerCount > 0
    ORDER BY ViewCount DESC
) AS qa;
