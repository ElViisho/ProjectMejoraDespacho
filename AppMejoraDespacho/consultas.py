consulta_NVVs = """SELECT DISTINCT [DIMACO_NEW].[dbo].[MAEEDO].[NUDO] FROM [DIMACO_NEW].[dbo].[MAEEDO] WITH (NOLOCK)
                INNER JOIN [DIMACO_NEW].[dbo].[MAEDDO] ON [MAEEDO].[IDMAEEDO] = [MAEDDO].[IDMAEEDO]
                WHERE SUDO = '000' 
                AND [DIMACO_NEW].[dbo].[MAEEDO].[TIDO] = 'NVV'
                AND [DIMACO_NEW].[dbo].[MAEEDO].[NUDO] LIKE 'V%'
                AND ESDO <> 'C'
                AND [DIMACO_NEW].[dbo].[MAEEDO].[IDMAEEDO] IN 
                    (SELECT [IDMAEEDO] FROM [DIMACO_NEW].[dbo].[MAEDDO] WITH(NOLOCK)
                    WHERE CAPRCO1 > (CAPREX1 + CAPRAD1)
                    AND TIDO = 'NVV'
                    AND SULIDO = '000'
                    AND LILG<>'IM')
                ORDER BY [DIMACO_NEW].[dbo].[MAEEDO].[NUDO];"""

consulta_maeedo = "SELECT * FROM [DIMACO_NEW].[dbo].[MAEEDO] WHERE NUDO = %s AND TIDO = 'NVV';"

consulta_maeen = """SELECT * FROM [DIMACO_NEW].[dbo].[MAEEN]
                INNER JOIN [DIMACO_NEW].[dbo].[MAEEDO] on [DIMACO_NEW].[dbo].[MAEEN].[KOEN] = [DIMACO_NEW].[dbo].[MAEEDO].[ENDO]
                WHERE [DIMACO_NEW].[dbo].[MAEEDO].[NUDO] = (
                    SELECT [NUDO] 
                    FROM [DIMACO_NEW].[dbo].[MAEEDO] 
                    WHERE NUDO = %s AND TIDO = 'NVV') AND [DIMACO_NEW].[dbo].[MAEEN].[TIPOSUC]='P';"""

consulta_maeedoob = """SELECT * FROM [DIMACO_NEW].[dbo].[MAEEDOOB]
                INNER JOIN [DIMACO_NEW].[dbo].[MAEEDO] on [DIMACO_NEW].[dbo].[MAEEDOOB].[IDMAEEDO] = [DIMACO_NEW].[dbo].[MAEEDO].[IDMAEEDO]
                WHERE [DIMACO_NEW].[dbo].[MAEEDO].[NUDO] = (
                    SELECT [NUDO]
                    FROM [DIMACO_NEW].[dbo].[MAEEDO] 
                    WHERE NUDO = %s AND TIDO = 'NVV');"""