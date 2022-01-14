
var regiones = [
    "Arica y Parinacota",
    "Tarapacá",
    "Antofagasta",
    "Atacama",
    "Coquimbo",
    "Valparaíso",
    "Metropolitana de Santiago",
    "Libertador General Bernardo O'Higgins",
    "Maule",
    "Ñuble",
    "Biobío",
    "La Araucanía",
    "Los Ríos",
    "Los Lagos",
    "Aysén del General Carlos Ibáñez del Campo",
    "Magallanes y la Antártica Chilena"]

var comunas_arica_y_parinacota = [
    "Arica",
    "Camarones",
    "General Lagos",
    "Putre"]

var comunas_tarapaca = [
    "Alto Hospicio",
    "Camiña",
    "Colchane",
    "Huara",
    "Iquique",
    "Pica",
    "Pozo Almonte"]

var comunas_antofagasta = [
    "Antofagasta",
    "Calama",
    "María Elena",
    "Mejillones",
    "Ollagüe",
    "San Pedro de Atacama",
    "Sierra Gorda",
    "Taltal",
    "Tocopilla"]

var comunas_atacama = [
    "Alto del Carmen",
    "Caldera",
    "Chañaral",
    "Copiapó",
    "Diego de Almagro",
    "Freirina",
    "Huasco",
    "Tierra Amarilla",
    "Vallenar"]

var comunas_coquimbo = [
    "Andacollo",
    "Canela",
    "Combarbalá",
    "Coquimbo",
    "Illapel",
    "La Higuera",
    "La Serena",
    "Los Vilos",
    "Monte Patria",
    "Ovalle",
    "Paihuano",
    "Punitaqui",
    "Río Hurtado",
    "Salamanca",
    "Vicuña"]

var comunas_valparaiso = [
"Algarrobo",
"Cabildo",
"Calle Larga",
"Cartagena",
"Casablanca",
"Catemu",
"Concón",
"El Quisco",
"El Tabo",
"Hijuelas",
"Isla de Pascua",
"Juan Fernández",
"La Calera",
"La Cruz",
"La Ligua",
"Limache",
"Llay-Llay",
"Los Andes",
"Nogales",
"Olmué",
"Panquehue",
"Papudo",
"Petorca",
"Puchuncaví",
"Putaendo",
"Quillota",
"Quilpué",
"Quintero",
"Rinconada",
"San Antonio",
"San Esteban",
"San Felipe",
"Santa María",
"Santo Domingo",
"Valparaíso",
"Villa Alemana",
"Viña del Mar",
"Zapallar"]

var comunas_metropolitana = [
"Alhué",
"Buin",
"Calera de Tango",
"Cerrillos",
"Cerro Navia",
"Colina",
"Conchalí",
"Curacaví",
"El Bosque",
"El Monte",
"Estación Central",
"Huechuraba",
"Independencia",
"Isla de Maipo",
"La Cisterna",
"La Florida",
"La Granja",
"La Pintana",
"La Reina",
"Lampa",
"Las Condes",
"Lo Barnechea",
"Lo Espejo",
"Lo Prado",
"Macul",
"Maipú",
"María Pinto",
"Melipilla",
"Ñuñoa",
"Padre Hurtado",
"Paine",
"Pedro Aguirre Cerda",
"Peñaflor",
"Peñalolén",
"Pirque",
"Providencia",
"Pudahuel",
"Puente Alto",
"Quilicura",
"Quinta Normal",
"Recoleta",
"Renca",
"San Bernardo",
"San Joaquín",
"San José de Maipo",
"San Miguel",
"San Pedro",
"San Ramón",
"Santiago",
"Talagante",
"Til Til",
"Vitacura"]

var comunas_ohiggins = [
"Chimbarongo",
"Chépica",
"Codegua",
"Coinco",
"Coltauco",
"Doñihue",
"Graneros",
"La Estrella",
"Las Cabras",
"Litueche",
"Lolol",
"Machalí",
"Malloa",
"Marchihue",
"Mostazal",
"Nancagua",
"Navidad",
"Olivar",
"Palmilla",
"Paredones",
"Peralillo",
"Peumo",
"Pichidegua",
"Pichilemu",
"Placilla",
"Pumanque",
"Quinta de Tilcoco",
"Rancagua",
"Rengo",
"Requínoa",
"San Fernando",
"San Vicente",
"Santa Cruz"]

var comunas_maule = [
"Cauquenes",
"Chanco",
"Colbún",
"Constitución",
"Curepto",
"Curicó",
"Empedrado",
"Hualañé",
"Licantén",
"Linares",
"Longaví",
"Maule",
"Molina",
"Parral",
"Pelarco",
"Pelluhue",
"Pencahue",
"Rauco",
"Retiro",
"Romeral",
"Río Claro",
"Sagrada Familia",
"San Clemente",
"San Javier",
"San Rafael",
"Talca",
"Teno",
"Vichuquén",
"Villa Alegre",
"Yerbas Buenas"]

var comunas_nuble = [
"Bulnes",
"Chillán",
"Chillán Viejo",
"Cobquecura",
"Coelemu",
"Coihueco",
"El Carmen",
"Ninhue",
"Ñiquén",
"Pemuco",
"Pinto",
"Portezuelo",
"Quillón",
"Quirihue",
"Ránquil",
"San Carlos",
"San Fabián",
"San Ignacio",
"San Nicolás",
"Treguaco",
"Yungay"]

var comunas_biobio = [
"Alto Biobío",
"Antuco",
"Arauco",
"Cabrero",
"Cañete",
"Chiguayante",
"Concepción",
"Contulmo",
"Coronel",
"Curanilahue",
"Florida",
"Hualpén",
"Hualqui",
"Laja",
"Lebu",
"Los Álamos",
"Los Ángeles",
"Lota",
"Mulchén",
"Nacimiento",
"Negrete",
"Penco",
"Quilaco",
"Quilleco",
"San Pedro de La Paz",
"San Rosendo",
"Santa Bárbara",
"Santa Juana",
"Talcahuano",
"Tirúa",
"Tomé",
"Tucapel",
"Yumbel"]

var comunas_araucania = [
"Angol",
"Carahue",
"Cholchol",
"Collipulli",
"Cunco",
"Curacautín",
"Curarrehue",
"Ercilla",
"Freire",
"Galvarino",
"Gorbea",
"Lautaro",
"Loncoche",
"Lonquimay",
"Los Sauces",
"Lumaco",
"Melipeuco",
"Nueva Imperial",
"Padre Las Casas",
"Perquenco",
"Pitrufquén",
"Pucón",
"Purén",
"Renaico",
"Saavedra",
"Temuco",
"Teodoro Schmidt",
"Toltén",
"Traiguén",
"Victoria",
"Vilcún",
"Villarrica"]

var comunas_los_rios = [
"Corral",
"Futrono",
"La Unión",
"Lago Ranco",
"Lanco",
"Los Lagos",
"Mariquina",
"Máfil",
"Paillaco",
"Panguipulli",
"Río Bueno",
"Valdivia"]

var comunas_los_lagos = [
"Ancud",
"Calbuco",
"Castro",
"Chaitén",
"Chonchi",
"Cochamó",
"Curaco de Vélez",
"Dalcahue",
"Fresia",
"Frutillar",
"Futaleufú",
"Hualaihué",
"Llanquihue",
"Los Muermos",
"Maullín",
"Osorno",
"Palena",
"Puerto Montt",
"Puerto Octay",
"Puerto Varas",
"Puqueldón",
"Purranque",
"Puyehue",
"Queilén",
"Quellón",
"Quemchi",
"Quinchao",
"Río Negro",
"San Juan de la Costa",
"San Pablo"]

var comunas_aysen = [
"Aysén",
"Chile Chico",
"Cisnes",
"Cochrane",
"Coyhaique",
"Guaitecas",
"Lago Verde",
"OHiggins",
"Río Ibáñez",
"Tortel"]

var comunas_magallanes = [
"Antártica",
"Cabo de Hornos",
"Laguna Blanca",
"Natales",
"Porvenir",
"Primavera",
"Punta Arenas",
"Río Verde",
"San Gregorio",
"Timaukel",
"Torres del Paine"]

var comunas = [comunas_arica_y_parinacota, comunas_tarapaca, comunas_antofagasta, comunas_atacama, comunas_coquimbo, comunas_valparaiso, comunas_metropolitana, comunas_ohiggins,
comunas_maule, comunas_nuble, comunas_biobio, comunas_araucania, comunas_los_rios, comunas_los_lagos, comunas_aysen, comunas_magallanes]