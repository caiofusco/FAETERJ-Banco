CREATE TABLE #PedidosTemp (
    codigoPedido VARCHAR(20),
    dataPedido DATE,
    SKU VARCHAR(50),
    nomeProduto VARCHAR(100),
    qtd INT,
    valor VARCHAR(20),
    frete VARCHAR(20),
    codigoComprador INT
);

BULK INSERT #PedidosTemp
FROM 'C:\SGBD\AV1\pedidos.txt'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ';',
    ROWTERMINATOR = '\n',
    CODEPAGE = '65001'
);

SELECT 
    codigoPedido,
    dataPedido,
    SKU,
    nomeProduto,
    qtd,
    CAST(REPLACE(valor, ',', '.') AS DECIMAL(10,2)) AS valor,
    CAST(REPLACE(frete, ',', '.') AS DECIMAL(10,2)) AS frete,
    codigoComprador
INTO #Pedidos
FROM #PedidosTemp;

SELECT 
    codigoPedido,
    SUM(valor * qtd) + MAX(frete) AS valor_total
INTO #Totais
FROM #Pedidos
GROUP BY codigoPedido;


SELECT 
    codigoPedido,
    valor_total
INTO #Fila
FROM #Totais
ORDER BY valor_total DESC;

-- PEDIDOS
INSERT INTO pedidos (codigoPedido, codigoCliente, valorTotal)
SELECT 
    p.codigoPedido,
    MAX(p.codigoComprador),
    t.valor_total
FROM #Pedidos p
JOIN #Totais t ON t.codigoPedido = p.codigoPedido
GROUP BY p.codigoPedido, t.valor_total;

-- COMPRA
INSERT INTO compra (codigoPedido, SKU, quantidade, valorUnitario)
SELECT 
    codigoPedido,
    SKU,
    qtd,
    valor
FROM #Pedidos;

-- EXPEDIÇÃO (prioridade aplicada)
INSERT INTO expedicao (codigoPedido)
SELECT codigoPedido
FROM #Fila;
