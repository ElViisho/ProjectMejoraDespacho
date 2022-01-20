"""
The different choices arrays that are used by django models
and forms throughout the app.
"""

# The choices for the states of an order
choices_estados = (
        (0, 'En Preparación'),
        (1, 'Preparado'),
        (2, 'Tubos'),
        (3, 'Cañería'),
        (4, 'Rollos')
)

# Ways to dispatch
choices_dispatch_way = (
        ((0, "DIMACO"),
        (1, "Externo"))
)

# Communes that the Santa Elena office dispatches
comunas_santa_elena = comunas_santa_elena = (
        (0, 'Alhué'),
        (1, 'Buin'),
        (2, 'Calera de Tango'),
        (3, 'Cerrillo'),
        (4, 'Cerro Navia'),
        (5, 'Curacaví'),
        (6, 'El Bosque'),
        (7, 'El Monte'),
        (8, 'Estación Central'),
        (9, 'Isla de Maipo'),
        (10, 'La Cisterna'),
        (11, 'La Florida'),
        (12, 'La Granja'),
        (13, 'La Pintana'),
        (14, 'Lo Espejo'),
        (15, 'Lo Prado'),
        (16, 'Macul'),
        (17, 'Maipú'),
        (18, 'María Pinto'),
        (19, 'Melipilla'),
        (20, 'Padre Hurtado'),
        (21, 'Paine'),
        (22, 'Pedro Aguirre Cerda'),
        (23, 'Peñaflor'),
        (24, 'Peñalolén'),
        (25, 'Pirque'),
        (26, 'Puente Alto'),
        (27, 'Quinta Normal'),
        (28, 'San Bernardo'),
        (29, 'San Joaquín'),
        (30, 'San José de Maipo'),
        (31, 'San Miguel'),
        (32, 'San Pedro'),
        (33, 'San Ramón'),
        (34, 'Talagante'),
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