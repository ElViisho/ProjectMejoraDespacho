"""
The different queries that are done to the Random ERP database
to get the data for the different orders
"""

# Query to get all NVVs that are still active and relevant
query_get_relevant_NVVs = """SELECT DISTINCT [DIMACO_NEW].[dbo].[MAEEDO].[NUDO] FROM [DIMACO_NEW].[dbo].[MAEEDO] WITH (NOLOCK)
                INNER JOIN [DIMACO_NEW].[dbo].[MAEDDO] ON [MAEEDO].[IDMAEEDO] = [MAEDDO].[IDMAEEDO]
                WHERE SUDO = '{}' 
                AND [DIMACO_NEW].[dbo].[MAEEDO].[TIDO] = 'NVV'
                AND [DIMACO_NEW].[dbo].[MAEEDO].[NUDO] LIKE '{}'
                AND ESDO <> 'C'
                AND [DIMACO_NEW].[dbo].[MAEEDO].[NUDO] NOT IN {}
                AND [DIMACO_NEW].[dbo].[MAEEDO].[IDMAEEDO] IN 
                    (SELECT [IDMAEEDO] FROM [DIMACO_NEW].[dbo].[MAEDDO] WITH (NOLOCK)
                    WHERE CAPRCO1 > (CAPREX1 + CAPRAD1)
                    AND TIDO = 'NVV'
                    AND SULIDO = '{}'
                    AND LILG<>'IM')
                AND [DIMACO_NEW].[dbo].[MAEEDO].[IDMAEEDO] IN (
					SELECT DISTINCT IDMAEEDO FROM [DIMACO_NEW].[dbo].[MAEEDOOB] WITH (NOLOCK)
					WHERE MOTIVO='2.' OR MOTIVO='4.')
                ORDER BY [DIMACO_NEW].[dbo].[MAEEDO].[NUDO];"""

# Query to get all the data from the master table (base and most important data) of a specific NVV
query_get_nvv_data = "SELECT [FEEMDO], [ENDO], [VANEDO] FROM [DIMACO_NEW].[dbo].[MAEEDO] WITH (NOLOCK) WHERE NUDO = %s AND TIDO = 'NVV';"

# Query to get the name of the client that is buying the order %s
query_get_client_name = """SELECT [NOKOEN] FROM [DIMACO_NEW].[dbo].[MAEEN] WITH (NOLOCK)
                INNER JOIN [DIMACO_NEW].[dbo].[MAEEDO] on [DIMACO_NEW].[dbo].[MAEEN].[KOEN] = [DIMACO_NEW].[dbo].[MAEEDO].[ENDO]
                WHERE [DIMACO_NEW].[dbo].[MAEEDO].[NUDO] = %s
                AND [DIMACO_NEW].[dbo].[MAEEN].[TIPOSUC]='P';"""

# Query to get the payment condition of the order %s
query_get_payment_condition = """SELECT [CPDO] FROM [DIMACO_NEW].[dbo].[MAEEDOOB] WITH (NOLOCK)
                INNER JOIN [DIMACO_NEW].[dbo].[MAEEDO] on [DIMACO_NEW].[dbo].[MAEEDOOB].[IDMAEEDO] = [DIMACO_NEW].[dbo].[MAEEDO].[IDMAEEDO]
                WHERE [DIMACO_NEW].[dbo].[MAEEDO].[NUDO] = %s;"""

# Query to get the name of the seller that did the order %s
query_get_seller_name = """SELECT DISTINCT [NOKOFU] FROM [DIMACO_NEW].[dbo].[TABFU] WITH (NOLOCK)
                INNER JOIN [DIMACO_NEW].[dbo].[MAEDDO] on [DIMACO_NEW].[dbo].[TABFU].[KOFU] = [DIMACO_NEW].[dbo].[MAEDDO].[KOFULIDO]
                WHERE [DIMACO_NEW].[dbo].[MAEDDO].[NUDO] = %s
                AND [DIMACO_NEW].[dbo].[MAEDDO].[TIDO] = 'NVV';"""

# Query to get the data for the dispatch guide of the order %s
query_get_dispatch_guide = """SELECT DISTINCT [TIDO], [NUDO], [FEEMLI] FROM [DIMACO_NEW].[dbo].[MAEDDO] WITH (NOLOCK)
                WHERE NUDOPA = '{}'
                AND TIDO IN ('FCV', 'GDV');"""