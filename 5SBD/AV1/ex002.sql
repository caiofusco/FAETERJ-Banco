-- ============================================================
-- PARTE 1: PREPARACAO DAS TABELAS BASE
-- (Recria o ambiente do script original antes do cursor)
-- ============================================================

-- Limpa tabelas se existirem
IF OBJECT_ID('tempdb..#PedidosTemp') IS NOT NULL DROP TABLE #PedidosTemp;
IF OBJECT_ID('COMPRAS',    'U') IS NOT NULL DROP TABLE COMPRAS;
IF OBJECT_ID('EXPEDICAO',  'U') IS NOT NULL DROP TABLE EXPEDICAO;
IF OBJECT_ID('PEDIDOS',    'U') IS NOT NULL DROP TABLE PEDIDOS;
IF OBJECT_ID('ESTOQUE',    'U') IS NOT NULL DROP TABLE ESTOQUE;
IF OBJECT_ID('PRODUTOS',   'U') IS NOT NULL DROP TABLE PRODUTOS;
IF OBJECT_ID('CLIENTES',   'U') IS NOT NULL DROP TABLE CLIENTES;

-- Tabela temporaria para carga do arquivo
CREATE TABLE #PedidosTemp (
    CODIGO_PEDIDO    VARCHAR(20),
    DATA_PEDIDO      DATE,
    SKU              VARCHAR(50),
    UPC              VARCHAR(50),
    NOME_PRODUTO     VARCHAR(100),
    QTD              INT,
    VALOR            VARCHAR(50),
    FRETE            VARCHAR(50),
    EMAIL            VARCHAR(100),
    CODIGO_COMPRADOR INT,
    NOME_COMPRADOR   VARCHAR(100),
    ENDERECO         VARCHAR(150),
    CEP              VARCHAR(10),
    UF               VARCHAR(2),
    PAIS             VARCHAR(30)
);

-- Insere os dados do pedidos.txt manualmente (equivalente ao BULK INSERT)
INSERT INTO #PedidosTemp VALUES ('abc123','2024-03-19','brinq456rio','456','quebra-cabeca',1,'43,22','5,32','samir@gmail.com',123,'Samir','Rua Exemplo 1','21212322','RJ','Brasil');
INSERT INTO #PedidosTemp VALUES ('abc123','2024-03-19','brinq789rio','789','jogo',         1,'43,22','5,32','samir@gmail.com',123,'Samir','Rua Exemplo 1','21212322','RJ','Brasil');
INSERT INTO #PedidosTemp VALUES ('abc789','2024-03-20','roupa123rio','123','camisa',        2,'47,25','6,21','teste@gmail.com', 789,'Fulano','Rua Exemplo 2','14784520','RJ','Brasil');
INSERT INTO #PedidosTemp VALUES ('abc741','2024-03-21','brinq789rio','789','jogo',          1,'43,22','5,32','samir@gmail.com',123,'Samir','Rua Exemplo 1','21212322','RJ','Brasil');

-- ============================================================
-- PARTE 2: CRIACAO DAS TABELAS NORMALIZADAS
-- ============================================================

CREATE TABLE CLIENTES (
    ID_CLIENTE INT          PRIMARY KEY,
    NOME       VARCHAR(150),
    EMAIL      VARCHAR(200)
);

CREATE TABLE PRODUTOS (
    ID_PRODUTO   INT IDENTITY PRIMARY KEY,
    SKU          VARCHAR(50),
    UPC          VARCHAR(50),
    NOME_PRODUTO VARCHAR(150)
);

-- STATUS adicionado: NULL = nao processado | 'Atendido' | 'Pendente'
CREATE TABLE PEDIDOS (
    ID_PEDIDO   VARCHAR(50)    PRIMARY KEY,
    DATA_PEDIDO DATE,
    ID_CLIENTE  INT,
    VL_TOTAL    DECIMAL(10,2),
    STATUS      VARCHAR(20)    NULL,
    FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTES(ID_CLIENTE)
);

CREATE TABLE COMPRAS (
    ID_COMPRA  INT IDENTITY PRIMARY KEY,
    ID_PEDIDO  VARCHAR(50),
    ID_PRODUTO INT,
    QTD        INT,
    VL_UNIT    DECIMAL(10,2),
    FOREIGN KEY (ID_PEDIDO)  REFERENCES PEDIDOS(ID_PEDIDO),
    FOREIGN KEY (ID_PRODUTO) REFERENCES PRODUTOS(ID_PRODUTO)
);

CREATE TABLE EXPEDICAO (
    ID_EXPEDICAO INT IDENTITY PRIMARY KEY,
    ID_PEDIDO    VARCHAR(50),
    ENDERECO     VARCHAR(150),
    CEP          VARCHAR(20),
    UF           VARCHAR(10),
    PAIS         VARCHAR(50),
    FRETE        DECIMAL(10,2),
    FOREIGN KEY (ID_PEDIDO) REFERENCES PEDIDOS(ID_PEDIDO)
);

-- Estoque: uma linha por produto com a quantidade disponivel
CREATE TABLE ESTOQUE (
    ID_PRODUTO   INT          PRIMARY KEY,
    QTD_ESTOQUE  INT          NOT NULL DEFAULT 0,
    FOREIGN KEY (ID_PRODUTO) REFERENCES PRODUTOS(ID_PRODUTO)
);

-- ============================================================
-- PARTE 3: CARGA DOS DADOS (mesma logica do script original)
-- ============================================================

INSERT INTO CLIENTES (ID_CLIENTE, NOME, EMAIL)
SELECT DISTINCT p.CODIGO_COMPRADOR, p.NOME_COMPRADOR, p.EMAIL
FROM #PedidosTemp p
LEFT JOIN CLIENTES c ON c.ID_CLIENTE = p.CODIGO_COMPRADOR
WHERE c.ID_CLIENTE IS NULL;

INSERT INTO PRODUTOS (SKU, UPC, NOME_PRODUTO)
SELECT DISTINCT p.SKU, p.UPC, p.NOME_PRODUTO
FROM #PedidosTemp p
LEFT JOIN PRODUTOS pr ON pr.SKU = p.SKU
WHERE pr.SKU IS NULL;

INSERT INTO PEDIDOS (ID_PEDIDO, DATA_PEDIDO, ID_CLIENTE, VL_TOTAL, STATUS)
SELECT DISTINCT
    p.CODIGO_PEDIDO,
    MAX(p.DATA_PEDIDO),
    MAX(p.CODIGO_COMPRADOR),
    SUM(p.QTD * CAST(REPLACE(p.VALOR, ',', '.') AS DECIMAL(10,2)))
        + MAX(CAST(REPLACE(p.FRETE, ',', '.') AS DECIMAL(10,2))),
    NULL  -- STATUS comeca nulo (nao processado)
FROM #PedidosTemp p
LEFT JOIN PEDIDOS pe ON pe.ID_PEDIDO = p.CODIGO_PEDIDO
WHERE pe.ID_PEDIDO IS NULL
GROUP BY p.CODIGO_PEDIDO;

INSERT INTO EXPEDICAO (ID_PEDIDO, ENDERECO, CEP, UF, PAIS, FRETE)
SELECT DISTINCT
    p.CODIGO_PEDIDO, p.ENDERECO, p.CEP, p.UF, p.PAIS,
    CAST(REPLACE(p.FRETE, ',', '.') AS DECIMAL(10,2))
FROM #PedidosTemp p
LEFT JOIN EXPEDICAO e ON e.ID_PEDIDO = p.CODIGO_PEDIDO
WHERE e.ID_PEDIDO IS NULL;

INSERT INTO COMPRAS (ID_PEDIDO, ID_PRODUTO, QTD, VL_UNIT)
SELECT
    p.CODIGO_PEDIDO,
    pr.ID_PRODUTO,
    p.QTD,
    CAST(REPLACE(p.VALOR, ',', '.') AS DECIMAL(10,2))
FROM #PedidosTemp p
INNER JOIN PRODUTOS pr ON p.SKU = pr.SKU
LEFT JOIN COMPRAS c
    ON c.ID_PEDIDO = p.CODIGO_PEDIDO AND c.ID_PRODUTO = pr.ID_PRODUTO
WHERE c.ID_COMPRA IS NULL;

-- ============================================================
-- PARTE 4: POPULANDO O ESTOQUE
-- ============================================================

INSERT INTO ESTOQUE (ID_PRODUTO, QTD_ESTOQUE)
SELECT ID_PRODUTO,
    CASE NOME_PRODUTO
        WHEN 'quebra-cabeca' THEN 5
        WHEN 'jogo'          THEN 1
        WHEN 'camisa'        THEN 0
        ELSE 0
    END
FROM PRODUTOS;

-- ============================================================
-- VERIFICACAO ANTES DO CURSOR
-- ============================================================

PRINT '--- ESTADO INICIAL ---';

SELECT 'PEDIDOS' AS Tabela, ID_PEDIDO, DATA_PEDIDO, VL_TOTAL, STATUS FROM PEDIDOS;

SELECT 'COMPRAS' AS Tabela,
       c.ID_COMPRA, c.ID_PEDIDO, pr.NOME_PRODUTO, c.QTD, c.VL_UNIT
FROM COMPRAS c
INNER JOIN PRODUTOS pr ON pr.ID_PRODUTO = c.ID_PRODUTO
ORDER BY c.ID_PEDIDO;

SELECT 'ESTOQUE INICIAL' AS Tabela,
       e.ID_PRODUTO, pr.NOME_PRODUTO, e.QTD_ESTOQUE
FROM ESTOQUE e
INNER JOIN PRODUTOS pr ON pr.ID_PRODUTO = e.ID_PRODUTO;

-- ============================================================
-- PARTE 5: CURSOR DE ATENDIMENTO DE PEDIDOS
-- ============================================================

DECLARE

    @vIdPedido       VARCHAR(50),


    @vIdProduto      INT,
    @vQtdComprada    INT,
    @vQtdEstoque     INT,


    @vPedidoAtendido BIT;     

DECLARE cur_pedidos CURSOR FOR
    SELECT ID_PEDIDO
    FROM PEDIDOS
    WHERE STATUS IS NULL
    ORDER BY DATA_PEDIDO;

OPEN cur_pedidos;
FETCH NEXT FROM cur_pedidos INTO @vIdPedido;

WHILE @@FETCH_STATUS = 0
BEGIN

    SET @vPedidoAtendido = 1;  

    -- -------------------------------------------------------
    -- Cursor interno: verifica estoque de cada item do pedido
    -- -------------------------------------------------------
    DECLARE cur_itens CURSOR FOR
        SELECT c.ID_PRODUTO, c.QTD
        FROM COMPRAS c
        WHERE c.ID_PEDIDO = @vIdPedido;

    OPEN cur_itens;
    FETCH NEXT FROM cur_itens INTO @vIdProduto, @vQtdComprada;

    WHILE @@FETCH_STATUS = 0
    BEGIN

        SELECT @vQtdEstoque = QTD_ESTOQUE
        FROM ESTOQUE
        WHERE ID_PRODUTO = @vIdProduto;

        IF @vQtdEstoque < @vQtdComprada
        BEGIN
            SET @vPedidoAtendido = 0;  
            PRINT 'Pedido ' + @vIdPedido + ': estoque insuficiente para produto ID '
                  + CAST(@vIdProduto AS VARCHAR) + ' (estoque=' + CAST(@vQtdEstoque AS VARCHAR)
                  + ', necessario=' + CAST(@vQtdComprada AS VARCHAR) + ')';
        END;

        FETCH NEXT FROM cur_itens INTO @vIdProduto, @vQtdComprada;
    END;

    CLOSE cur_itens;
    DEALLOCATE cur_itens;

    -- -------------------------------------------------------
    -- Atualiza status e estoque conforme resultado
    -- -------------------------------------------------------
    IF @vPedidoAtendido = 1
    BEGIN
    
        UPDATE ESTOQUE
        SET QTD_ESTOQUE = QTD_ESTOQUE - c.QTD
        FROM ESTOQUE est
        INNER JOIN COMPRAS c
            ON c.ID_PRODUTO = est.ID_PRODUTO
        WHERE c.ID_PEDIDO = @vIdPedido;

        
        UPDATE PEDIDOS
        SET STATUS = 'Atendido'
        WHERE ID_PEDIDO = @vIdPedido;

        PRINT 'Pedido ' + @vIdPedido + ': ATENDIDO - estoque debitado.';
    END
    ELSE
    BEGIN
   
        UPDATE PEDIDOS
        SET STATUS = 'Pendente'
        WHERE ID_PEDIDO = @vIdPedido;

        PRINT 'Pedido ' + @vIdPedido + ': PENDENTE - estoque insuficiente.';
    END;

    FETCH NEXT FROM cur_pedidos INTO @vIdPedido;
END;

CLOSE cur_pedidos;
DEALLOCATE cur_pedidos;

-- ============================================================
-- VERIFICACAO APOS O CURSOR
-- ============================================================

PRINT '--- ESTADO FINAL ---';

SELECT 'PEDIDOS APOS CURSOR' AS Tabela,
       ID_PEDIDO, DATA_PEDIDO, VL_TOTAL, STATUS
FROM PEDIDOS
ORDER BY DATA_PEDIDO;

SELECT 'ESTOQUE APOS CURSOR' AS Tabela,
       e.ID_PRODUTO, pr.NOME_PRODUTO,
       e.QTD_ESTOQUE AS QTD_ATUAL
FROM ESTOQUE e
INNER JOIN PRODUTOS pr ON pr.ID_PRODUTO = e.ID_PRODUTO;

SELECT
    pe.ID_PEDIDO,
    pe.STATUS,
    pr.NOME_PRODUTO,
    c.QTD         AS QTD_COMPRADA,
    e.QTD_ESTOQUE AS ESTOQUE_RESTANTE
FROM PEDIDOS pe
INNER JOIN COMPRAS  c  ON c.ID_PEDIDO  = pe.ID_PEDIDO
INNER JOIN PRODUTOS pr ON pr.ID_PRODUTO = c.ID_PRODUTO
INNER JOIN ESTOQUE  e  ON e.ID_PRODUTO  = pr.ID_PRODUTO
ORDER BY pe.DATA_PEDIDO, pr.NOME_PRODUTO;
