consulta_NVVs = """SELECT DISTINCT [DIMACO_NEW].[dbo].[MAEEDO].[NUDO] FROM [DIMACO_NEW].[dbo].[MAEEDO] WITH (NOLOCK)
                INNER JOIN [DIMACO_NEW].[dbo].[MAEDDO] ON [MAEEDO].[IDMAEEDO] = [MAEDDO].[IDMAEEDO]
                WHERE SUDO = '000' 
                AND [DIMACO_NEW].[dbo].[MAEEDO].[TIDO] = 'NVV'
                AND [DIMACO_NEW].[dbo].[MAEEDO].[NUDO] LIKE 'V%'
                AND ESDO <> 'C'
                AND [DIMACO_NEW].[dbo].[MAEEDO].[NUDO] NOT IN {}
                AND [DIMACO_NEW].[dbo].[MAEEDO].[IDMAEEDO] IN 
                    (SELECT [IDMAEEDO] FROM [DIMACO_NEW].[dbo].[MAEDDO] WITH (NOLOCK)
                    WHERE CAPRCO1 > (CAPREX1 + CAPRAD1)
                    AND TIDO = 'NVV'
                    AND SULIDO = '000'
                    AND LILG<>'IM')
                AND [DIMACO_NEW].[dbo].[MAEEDO].[IDMAEEDO] IN (
					SELECT DISTINCT IDMAEEDO FROM [DIMACO_NEW].[dbo].[MAEEDOOB] WITH (NOLOCK)
					WHERE MOTIVO='2.' OR MOTIVO='4.')
                ORDER BY [DIMACO_NEW].[dbo].[MAEEDO].[NUDO];"""

consulta_maeedo = "SELECT * FROM [DIMACO_NEW].[dbo].[MAEEDO] WITH (NOLOCK) WHERE NUDO = %s AND TIDO = 'NVV';"

consulta_maeen = """SELECT * FROM [DIMACO_NEW].[dbo].[MAEEN] WITH (NOLOCK)
                INNER JOIN [DIMACO_NEW].[dbo].[MAEEDO] on [DIMACO_NEW].[dbo].[MAEEN].[KOEN] = [DIMACO_NEW].[dbo].[MAEEDO].[ENDO]
                WHERE [DIMACO_NEW].[dbo].[MAEEDO].[NUDO] = %s
                AND [DIMACO_NEW].[dbo].[MAEEN].[TIPOSUC]='P';"""

consulta_maeedoob = """SELECT * FROM [DIMACO_NEW].[dbo].[MAEEDOOB] WITH (NOLOCK)
                INNER JOIN [DIMACO_NEW].[dbo].[MAEEDO] on [DIMACO_NEW].[dbo].[MAEEDOOB].[IDMAEEDO] = [DIMACO_NEW].[dbo].[MAEEDO].[IDMAEEDO]
                WHERE [DIMACO_NEW].[dbo].[MAEEDO].[NUDO] = %s;"""

consulta_tabfu = """SELECT DISTINCT NOKOFU FROM [DIMACO_NEW].[dbo].[TABFU] WITH (NOLOCK)
                INNER JOIN [DIMACO_NEW].[dbo].[MAEDDO] on [DIMACO_NEW].[dbo].[TABFU].[KOFU] = [DIMACO_NEW].[dbo].[MAEDDO].[KOFULIDO]
                WHERE [DIMACO_NEW].[dbo].[MAEDDO].[NUDO] = %s
                AND [DIMACO_NEW].[dbo].[MAEDDO].[TIDO] = 'NVV';"""

consulta_guia_despacho = """SELECT DISTINCT TIDO, NUDO, FEEMLI FROM [DIMACO_NEW].[dbo].[MAEDDO] WITH (NOLOCK)
                WHERE NUDOPA = %s
                AND TIDO IN ('FCV', 'GDV')
                AND SULIDO = '000';"""