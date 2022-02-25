"""
The different choices arrays that are used by django models
and forms throughout the app.
"""

# The choices for the states of an order, for the dispatcher
choices_estados = (
        (0, 'En Preparación'),
        (1, 'Preparado'),
        (2, 'Tubos'),
        (3, 'Cañería'),
        (4, 'Rollos')
)

# The choices for the states of an order. 0-3 for Santa Elena and Concepción
# 10-16 for Colina.
choices_estados_pedido_para_vendedor= (
        (0, 'En Preparación'),
        (1, 'Detenido'),
        (2, 'Preparado incompleto'),
        (3, 'Preparado completo'),
        (10, 'Creado'),
        (11, 'Liberado'),
        (12, 'Andén'),
        (13, 'Picking'),
        (14, 'Despachado'),
        (15, 'Anulado'),
        (16, 'Eliminado'),
)

choices_am_pm = (
        (0, ''),
        (1, 'AM'),
        (2, 'PM')
)

# Ways to dispatch
choices_dispatch_way = (
        ((0, "DIMACO"),
        (1, "EXTERNO"))
)

# The hours for dispatch
horas = (
	("8", "08:00"),
	("9", "09:00"),
	("10", "10:00"),
	("11", "11:00"),
	("12", "12:00"),
	("13", "13:00"),
	("14", "14:00"),
	("15", "15:00"),
	("16", "16:00"),
	("17", "17:00"),
	("18", "18:00")
)


# Regions of Chile for dispatch
regiones = (
        ("0", "----------------------------------------"),
        ("1", "Arica y Parinacota"),
        ("2", "Tarapacá"),
        ("3", "Antofagasta"),
        ("4", "Atacama"),
        ("5", "Coquimbo"),
        ("6", "Valparaíso"),
        ("7", "Metropolitana de Santiago"),
        ("8", "Libertador General Bernardo O'Higgins"),
        ("9", "Maule"),
        ("10", "Ñuble"),
        ("11", "Biobío"),
        ("12", "La Araucanía"),
        ("13", "Los Ríos"),
        ("14", "Los Lagos"),
        ("15", "Aysén del General Carlos Ibáñez del Campo"),
        ("16", "Magallanes y la Antártica Chilena")
)

# Communes per region
comunas_arica_y_parinacota = (
        ("0", "----------------------------------------"),
        ("1", "Arica"),
        ("2", "Camarones"),
        ("3", "General Lagos"),
        ("4", "Putre")
)
comunas_tarapaca = (
        ("0", "----------------------------------------"),
        ("1", "Alto Hospicio"),
        ("2", "Camiña"),
        ("3", "Colchane"),
        ("4", "Huara"),
        ("5", "Iquique"),
        ("6", "Pica"),
        ("7", "Pozo Almonte"),
)
comunas_antofagasta = (
        ("0", "----------------------------------------"),
        ("1", "Antofagasta"),
        ("2", "Calama"),
        ("3", "María Elena"),
        ("4", "Mejillones"),
        ("5", "Ollagüe"),
        ("6", "San Pedro de Atacama"),
        ("7", "Sierra Gorda"),
        ("8", "Taltal"),
        ("9", "Tocopilla"),
)
comunas_atacama = (
        ("0", "----------------------------------------"),
        ("1", "Alto del Carmen"),
        ("2", "Caldera"),
        ("3", "Chañaral"),
        ("4", "Copiapó"),
        ("5", "Diego de Almagro"),
        ("6", "Freirina"),
        ("7", "Huasco"),
        ("8", "Tierra Amarilla"),
        ("9", "Vallenar"),
)
comunas_coquimbo = (
        ("0", "----------------------------------------"),
        ("1", "Andacollo"),
        ("2", "Canela"),
        ("3", "Combarbalá"),
        ("4", "Coquimbo"),
        ("5", "Illapel"),
        ("6", "La Higuera"),
        ("7", "La Serena"),
        ("8", "Los Vilos"),
        ("9", "Monte Patria"),
        ("10", "Ovalle"),
        ("11", "Paihuano"),
        ("12", "Punitaqui"),
        ("13", "Río Hurtado"),
        ("14", "Salamanca"),
        ("15", "Vicuña"),
)
comunas_valparaiso = (
        ("0", "----------------------------------------"),
        ("1", "Algarrobo"),
        ("2", "Cabildo"),
        ("3", "Calle Larga"),
        ("4", "Cartagena"),
        ("5", "Casablanca"),
        ("6", "Catemu"),
        ("7", "Concón"),
        ("8", "El Quisco"),
        ("9", "El Tabo"),
        ("10", "Hijuelas"),
        ("11", "Isla de Pascua"),
        ("12", "Juan Fernández"),
        ("13", "La Calera"),
        ("14", "La Cruz"),
        ("15", "La Ligua"),
        ("16", "Limache"),
        ("17", "Llay-Llay"),
        ("18", "Los Andes"),
        ("19", "Nogales"),
        ("20", "Olmué"),
        ("21", "Panquehue"),
        ("22", "Papudo"),
        ("23", "Petorca"),
        ("24", "Puchuncaví"),
        ("25", "Putaendo"),
        ("26", "Quillota"),
        ("27", "Quilpué"),
        ("28", "Quintero"),
        ("29", "Rinconada"),
        ("30", "San Antonio"),
        ("31", "San Esteban"),
        ("32", "San Felipe"),
        ("33", "Santa María"),
        ("34", "Santo Domingo"),
        ("35", "Valparaíso"),
        ("36", "Villa Alemana"),
        ("37", "Viña del Mar"),
        ("38", "Zapallar"),
)
comunas_metropolitana = (
        ("0", "----------------------------------------"),
        ("1", "Alhué"),
        ("2", "Buin"),
        ("3", "Calera de Tango"),
        ("4", "Cerrillos"),
        ("5", "Cerro Navia"),
        ("6", "Colina"),
        ("7", "Conchalí"),
        ("8", "Curacaví"),
        ("9", "El Bosque"),
        ("10", "El Monte"),
        ("11", "Estación Central"),
        ("12", "Huechuraba"),
        ("13", "Independencia"),
        ("14", "Isla de Maipo"),
        ("15", "La Cisterna"),
        ("16", "La Florida"),
        ("17", "La Granja"),
        ("18", "La Pintana"),
        ("19", "La Reina"),
        ("20", "Lampa"),
        ("21", "Las Condes"),
        ("22", "Lo Barnechea"),
        ("23", "Lo Espejo"),
        ("24", "Lo Prado"),
        ("25", "Macul"),
        ("26", "Maipú"),
        ("27", "María Pinto"),
        ("28", "Melipilla"),
        ("29", "Ñuñoa"),
        ("30", "Padre Hurtado"),
        ("31", "Paine"),
        ("32", "Pedro Aguirre Cerda"),
        ("33", "Peñaflor"),
        ("34", "Peñalolén"),
        ("35", "Pirque"),
        ("36", "Providencia"),
        ("37", "Pudahuel"),
        ("38", "Puente Alto"),
        ("39", "Quilicura"),
        ("40", "Quinta Normal"),
        ("41", "Recoleta"),
        ("42", "Renca"),
        ("43", "San Bernardo"),
        ("44", "San Joaquín"),
        ("45", "San José de Maipo"),
        ("46", "San Miguel"),
        ("47", "San Pedro"),
        ("48", "San Ramón"),
        ("49", "Santiago"),
        ("50", "Talagante"),
        ("51", "Til Til"),
        ("52", "Vitacura"),
)
comunas_ohiggins = (
        ("0", "----------------------------------------"),
        ("1", "Chimbarongo"),
        ("2", "Chépica"),
        ("3", "Codegua"),
        ("4", "Coinco"),
        ("5", "Coltauco"),
        ("6", "Doñihue"),
        ("7", "Graneros"),
        ("8", "La Estrella"),
        ("9", "Las Cabras"),
        ("10", "Litueche"),
        ("11", "Lolol"),
        ("12", "Machalí"),
        ("13", "Malloa"),
        ("14", "Marchihue"),
        ("15", "Mostazal"),
        ("16", "Nancagua"),
        ("17", "Navidad"),
        ("18", "Olivar"),
        ("19", "Palmilla"),
        ("20", "Paredones"),
        ("21", "Peralillo"),
        ("22", "Peumo"),
        ("23", "Pichidegua"),
        ("24", "Pichilemu"),
        ("25", "Placilla"),
        ("26", "Pumanque"),
        ("27", "Quinta de Tilcoco"),
        ("28", "Rancagua"),
        ("29", "Rengo"),
        ("30", "Requínoa"),
        ("31", "San Fernando"),
        ("32", "San Vicente"),
        ("33", "Santa Cruz"),
)
comunas_maule = (
        ("0", "----------------------------------------"),
        ("1", "Cauquenes"),
        ("2", "Chanco"),
        ("3", "Colbún"),
        ("4", "Constitución"),
        ("5", "Curepto"),
        ("6", "Curicó"),
        ("7", "Empedrado"),
        ("8", "Hualañé"),
        ("9", "Licantén"),
        ("10", "Linares"),
        ("11", "Longaví"),
        ("12", "Maule"),
        ("13", "Molina"),
        ("14", "Parral"),
        ("15", "Pelarco"),
        ("16", "Pelluhue"),
        ("17", "Pencahue"),
        ("18", "Rauco"),
        ("19", "Retiro"),
        ("20", "Romeral"),
        ("21", "Río Claro"),
        ("22", "Sagrada Familia"),
        ("23", "San Clemente"),
        ("24", "San Javier"),
        ("25", "San Rafael"),
        ("26", "Talca"),
        ("27", "Teno"),
        ("28", "Vichuquén"),
        ("29", "Villa Alegre"),
        ("30", "Yerbas Buenas"),
)
comunas_nuble = (
        ("0", "----------------------------------------"),
        ("1", "Bulnes"),
        ("2", "Chillán"),
        ("3", "Chillán Viejo"),
        ("4", "Cobquecura"),
        ("5", "Coelemu"),
        ("6", "Coihueco"),
        ("7", "El Carmen"),
        ("8", "Ninhue"),
        ("9", "Ñiquén"),
        ("10", "Pemuco"),
        ("11", "Pinto"),
        ("12", "Portezuelo"),
        ("13", "Quillón"),
        ("14", "Quirihue"),
        ("15", "Ránquil"),
        ("16", "San Carlos"),
        ("17", "San Fabián"),
        ("18", "San Ignacio"),
        ("19", "San Nicolás"),
        ("20", "Treguaco"),
        ("21", "Yungay"),
)
comunas_biobio = (
        ("0", "----------------------------------------"),
        ("1", "Alto Biobío"),
        ("2", "Antuco"),
        ("3", "Arauco"),
        ("4", "Cabrero"),
        ("5", "Cañete"),
        ("6", "Chiguayante"),
        ("7", "Concepción"),
        ("8", "Contulmo"),
        ("9", "Coronel"),
        ("10", "Curanilahue"),
        ("11", "Florida"),
        ("12", "Hualpén"),
        ("13", "Hualqui"),
        ("14", "Laja"),
        ("15", "Lebu"),
        ("16", "Los Álamos"),
        ("17", "Los Ángeles"),
        ("18", "Lota"),
        ("19", "Mulchén"),
        ("20", "Nacimiento"),
        ("21", "Negrete"),
        ("22", "Penco"),
        ("23", "Quilaco"),
        ("24", "Quilleco"),
        ("25", "San Pedro de La Paz"),
        ("26", "San Rosendo"),
        ("27", "Santa Bárbara"),
        ("28", "Santa Juana"),
        ("29", "Talcahuano"),
        ("30", "Tirúa"),
        ("31", "Tomé"),
        ("32", "Tucapel"),
        ("33", "Yumbel"),
)
comunas_araucania = (
        ("0", "----------------------------------------"),
        ("1", "Angol"),
        ("2", "Carahue"),
        ("3", "Cholchol"),
        ("4", "Collipulli"),
        ("5", "Cunco"),
        ("6", "Curacautín"),
        ("7", "Curarrehue"),
        ("8", "Ercilla"),
        ("9", "Freire"),
        ("10", "Galvarino"),
        ("11", "Gorbea"),
        ("12", "Lautaro"),
        ("13", "Loncoche"),
        ("14", "Lonquimay"),
        ("15", "Los Sauces"),
        ("16", "Lumaco"),
        ("17", "Melipeuco"),
        ("18", "Nueva Imperial"),
        ("19", "Padre Las Casas"),
        ("20", "Perquenco"),
        ("21", "Pitrufquén"),
        ("22", "Pucón"),
        ("23", "Purén"),
        ("24", "Renaico"),
        ("25", "Saavedra"),
        ("26", "Temuco"),
        ("27", "Teodoro Schmidt"),
        ("28", "Toltén"),
        ("29", "Traiguén"),
        ("30", "Victoria"),
        ("31", "Vilcún"),
        ("32", "Villarrica"),
)
comunas_los_rios = (
        ("0", "----------------------------------------"),
        ("1", "Corral"),
        ("2", "Futrono"),
        ("3", "La Unión"),
        ("4", "Lago Ranco"),
        ("5", "Lanco"),
        ("6", "Los Lagos"),
        ("7", "Mariquina"),
        ("8", "Máfil"),
        ("9", "Paillaco"),
        ("10", "Panguipulli"),
        ("11", "Río Bueno"),
        ("12", "Valdivia"),
)
comunas_los_lagos = (
        ("0", "----------------------------------------"),
        ("1", "Ancud"),
        ("2", "Calbuco"),
        ("3", "Castro"),
        ("4", "Chaitén"),
        ("5", "Chonchi"),
        ("6", "Cochamó"),
        ("7", "Curaco de Vélez"),
        ("8", "Dalcahue"),
        ("9", "Fresia"),
        ("10", "Frutillar"),
        ("11", "Futaleufú"),
        ("12", "Hualaihué"),
        ("13", "Llanquihue"),
        ("14", "Los Muermos"),
        ("15", "Maullín"),
        ("16", "Osorno"),
        ("17", "Palena"),
        ("18", "Puerto Montt"),
        ("19", "Puerto Octay"),
        ("20", "Puerto Varas"),
        ("21", "Puqueldón"),
        ("22", "Purranque"),
        ("23", "Puyehue"),
        ("24", "Queilén"),
        ("25", "Quellón"),
        ("26", "Quemchi"),
        ("27", "Quinchao"),
        ("28", "Río Negro"),
        ("29", "San Juan de la Costa"),
        ("30", "San Pablo"),
)
comunas_aysen = (
        ("0", "----------------------------------------"),
        ("1", "Aysén"),
        ("2", "Chile Chico"),
        ("3", "Cisnes"),
        ("4", "Cochrane"),
        ("5", "Coyhaique"),
        ("6", "Guaitecas"),
        ("7", "Lago Verde"),
        ("8", "OHiggins"),
        ("9", "Río Ibáñez"),
        ("10", "Tortel"),
)
comunas_magallanes = (
        ("0", "----------------------------------------"),
        ("1", "Antártica"),
        ("2", "Cabo de Hornos"),
        ("3", "Laguna Blanca"),
        ("4", "Natales"),
        ("5", "Porvenir"),
        ("6", "Primavera"),
        ("7", "Punta Arenas"),
        ("8", "Río Verde"),
        ("9", "San Gregorio"),
        ("10", "Timaukel"),
        ("11", "Torres del Paine"),
)
# All the communes arraya in one array, in the same order as the regions array
comunas_todas = [comunas_metropolitana, comunas_arica_y_parinacota, comunas_tarapaca, comunas_antofagasta, comunas_atacama, comunas_coquimbo, comunas_valparaiso, comunas_metropolitana, comunas_ohiggins,
        comunas_maule, comunas_nuble, comunas_biobio, comunas_araucania, comunas_los_rios, comunas_los_lagos, comunas_aysen, comunas_magallanes]


# To pass it to the form so it knows the max number it can accept no matter the region selected
comunas_longest = max (comunas_todas, key=len)