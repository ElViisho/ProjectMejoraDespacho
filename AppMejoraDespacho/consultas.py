
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