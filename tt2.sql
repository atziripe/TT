-- MariaDB dump 10.17  Distrib 10.4.13-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: tt2
-- ------------------------------------------------------
-- Server version	10.4.13-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `administrador`
--

DROP TABLE IF EXISTS `administrador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `administrador` (
  `nomUsuario` varchar(20) NOT NULL,
  `nombre` varchar(70) DEFAULT NULL,
  `contrasena` varchar(45) DEFAULT NULL,
  `correo` varchar(70) DEFAULT NULL,
  PRIMARY KEY (`nomUsuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administrador`
--

LOCK TABLES `administrador` WRITE;
/*!40000 ALTER TABLE `administrador` DISABLE KEYS */;
INSERT INTO `administrador` VALUES ('Atziri_Pe','Atziri Pérez García','abcd1234','atziri.perez.garcia@gmail,com'),('Emm_MR','Luis Emmanuel Maya Rocha','Peter797','maya.rocha.emmanuel@gmail.com'),('Galilea_ALoEs','Galilea América Loretto Estrada','abcd1234','galilealoes@gmail.com');
/*!40000 ALTER TABLE `administrador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ap_reminiscencia`
--

DROP TABLE IF EXISTS `ap_reminiscencia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ap_reminiscencia` (
  `cveAcceso` varchar(10) NOT NULL,
  `paciente` varchar(20) NOT NULL,
  `fechaAp` date DEFAULT NULL,
  `resultado` int(11) DEFAULT NULL,
  PRIMARY KEY (`cveAcceso`),
  KEY `paciente` (`paciente`),
  CONSTRAINT `ap_reminiscencia_ibfk_1` FOREIGN KEY (`paciente`) REFERENCES `paciente` (`nomUsuario`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ap_reminiscencia`
--

LOCK TABLES `ap_reminiscencia` WRITE;
/*!40000 ALTER TABLE `ap_reminiscencia` DISABLE KEYS */;
INSERT INTO `ap_reminiscencia` VALUES ('12345abcde','MartinGMa','2020-12-10',8);
/*!40000 ALTER TABLE `ap_reminiscencia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ap_screening`
--

DROP TABLE IF EXISTS `ap_screening`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ap_screening` (
  `cveAcceso` varchar(10) NOT NULL,
  `paciente` varchar(20) NOT NULL,
  `fechaAp` date DEFAULT NULL,
  `resultadoFinal` int(11) DEFAULT NULL,
  PRIMARY KEY (`cveAcceso`),
  KEY `paciente` (`paciente`),
  CONSTRAINT `ap_screening_ibfk_1` FOREIGN KEY (`paciente`) REFERENCES `paciente` (`nomUsuario`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ap_screening`
--

LOCK TABLES `ap_screening` WRITE;
/*!40000 ALTER TABLE `ap_screening` DISABLE KEYS */;
INSERT INTO `ap_screening` VALUES ('abcde12345','SocorroMaR','2020-12-08',24);
/*!40000 ALTER TABLE `ap_screening` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cuidador`
--

DROP TABLE IF EXISTS `cuidador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cuidador` (
  `nomUsuario` varchar(20) NOT NULL,
  `nombre` varchar(70) DEFAULT NULL,
  `contrasena` varchar(45) DEFAULT NULL,
  `correo` varchar(70) DEFAULT NULL,
  PRIMARY KEY (`nomUsuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cuidador`
--

LOCK TABLES `cuidador` WRITE;
/*!40000 ALTER TABLE `cuidador` DISABLE KEYS */;
INSERT INTO `cuidador` VALUES ('Gil793','Gilberto Gómez Rodríguez','GiGomez71','gilberto_gr_79@hotmail.com.mx'),('MariaLM','María López Maldonado','MaLoMa33','marialoma@yahoo.com.mx');
/*!40000 ALTER TABLE `cuidador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ent_cogn`
--

DROP TABLE IF EXISTS `ent_cogn`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ent_cogn` (
  `cveAcceso` varchar(10) NOT NULL,
  `cveTema` int(11) NOT NULL,
  `paciente` varchar(20) NOT NULL,
  `fechaAp` date DEFAULT NULL,
  `estado` enum('Superado','No Superado') DEFAULT NULL,
  `tiempo` time DEFAULT NULL,
  PRIMARY KEY (`cveAcceso`),
  KEY `cveTema` (`cveTema`),
  KEY `paciente` (`paciente`),
  CONSTRAINT `ent_cogn_ibfk_1` FOREIGN KEY (`cveTema`) REFERENCES `tema` (`cveTemas`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `ent_cogn_ibfk_2` FOREIGN KEY (`paciente`) REFERENCES `paciente` (`nomUsuario`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ent_cogn`
--

LOCK TABLES `ent_cogn` WRITE;
/*!40000 ALTER TABLE `ent_cogn` DISABLE KEYS */;
INSERT INTO `ent_cogn` VALUES ('12345edcba',1,'SocorroMaR','2020-12-20','Superado','00:50:35');
/*!40000 ALTER TABLE `ent_cogn` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `especialista`
--

DROP TABLE IF EXISTS `especialista`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `especialista` (
  `nomUsuario` varchar(8) NOT NULL,
  `nombre` varchar(70) NOT NULL,
  `contrasena` varchar(50) NOT NULL,
  `correo` varchar(70) NOT NULL,
  `numPacientes` int(11) DEFAULT NULL,
  `datos_generales` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`nomUsuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `especialista`
--

LOCK TABLES `especialista` WRITE;
/*!40000 ALTER TABLE `especialista` DISABLE KEYS */;
INSERT INTO `especialista` VALUES ('Lupita_8','Guadalupe Ruíz Zarate','GRZ123L8','ruizza-guadalupe@hotmail.com',8,'Cedula: 12345, unidad medica: IMSS, especialidad: otología'),('Saúl_MDo','Saúl Mendoza Domínguez','S1aul92M','saul_mendom@gmail.com',10,'Cedula: 54321, unidad medica: ISSSTE, especialidad: optometría');
/*!40000 ALTER TABLE `especialista` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mensaje`
--

DROP TABLE IF EXISTS `mensaje`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mensaje` (
  `cveMensaje` int(11) NOT NULL AUTO_INCREMENT,
  `especialista` varchar(8) NOT NULL,
  `cuidador` varchar(20) NOT NULL,
  `mensaje` varchar(200) DEFAULT NULL,
  `fechaEnvio` date DEFAULT NULL,
  PRIMARY KEY (`cveMensaje`),
  KEY `especialista` (`especialista`),
  KEY `cuidador` (`cuidador`),
  CONSTRAINT `mensaje_ibfk_1` FOREIGN KEY (`especialista`) REFERENCES `especialista` (`nomUsuario`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `mensaje_ibfk_2` FOREIGN KEY (`cuidador`) REFERENCES `cuidador` (`nomUsuario`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mensaje`
--

LOCK TABLES `mensaje` WRITE;
/*!40000 ALTER TABLE `mensaje` DISABLE KEYS */;
INSERT INTO `mensaje` VALUES (3,'Saúl_MDo','MariaLM','Le recomiendo que la paciente tome clonazepam','2020-12-09'),(4,'Lupita_8','Gil793','Es urgente que paciente asista a su sesión de Screening','2020-12-25');
/*!40000 ALTER TABLE `mensaje` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `paciente`
--

DROP TABLE IF EXISTS `paciente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `paciente` (
  `nomUsuario` varchar(20) NOT NULL,
  `especialista` varchar(8) NOT NULL,
  `cuidador` varchar(20) NOT NULL,
  `nombre` varchar(70) NOT NULL,
  `contrasena` varchar(50) NOT NULL,
  `correo` varchar(70) NOT NULL,
  `escolaridad` enum('Ninguna','Primaria','Secundaria','Bachillerato','Licenciatura o superior') NOT NULL,
  `fechaNac` date NOT NULL,
  `sexo` enum('Femenino','Masculino') DEFAULT NULL,
  `fechaIng` date DEFAULT NULL,
  `fechaDiag` date DEFAULT NULL,
  PRIMARY KEY (`nomUsuario`),
  KEY `especialista` (`especialista`),
  KEY `cuidador` (`cuidador`),
  CONSTRAINT `paciente_ibfk_1` FOREIGN KEY (`especialista`) REFERENCES `especialista` (`nomUsuario`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `paciente_ibfk_2` FOREIGN KEY (`cuidador`) REFERENCES `cuidador` (`nomUsuario`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paciente`
--

LOCK TABLES `paciente` WRITE;
/*!40000 ALTER TABLE `paciente` DISABLE KEYS */;
INSERT INTO `paciente` VALUES ('MartinGMa','Lupita_8','Gil793','Martín Gómez Macedo','MaGo48','martin.go.mac@gormail.com','Secundaria','1948-02-18','Masculino','2020-11-25','2018-09-12'),('SocorroMaR','Saúl_MDo','MariaLM','Socorro Maldonado Raya','Soco1234','socorromar@yahoo.com.mx','Bachillerato','1953-09-07','Femenino','2020-11-08','2020-07-15');
/*!40000 ALTER TABLE `paciente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `palabra`
--

DROP TABLE IF EXISTS `palabra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `palabra` (
  `tema` int(11) NOT NULL,
  `cvePalabra` int(11) NOT NULL AUTO_INCREMENT,
  `palabra` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`tema`,`cvePalabra`),
  KEY `cvePalabra` (`cvePalabra`),
  CONSTRAINT `palabra_ibfk_1` FOREIGN KEY (`tema`) REFERENCES `tema` (`cveTemas`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `palabra`
--

LOCK TABLES `palabra` WRITE;
/*!40000 ALTER TABLE `palabra` DISABLE KEYS */;
INSERT INTO `palabra` VALUES (1,1,'perro'),(1,2,'gato'),(2,3,'leopardo'),(2,4,'borrego'),(3,5,'vaso'),(3,6,'traste'),(4,7,'cuchara'),(4,8,'trapeador');
/*!40000 ALTER TABLE `palabra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pregunta`
--

DROP TABLE IF EXISTS `pregunta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pregunta` (
  `idReactivo` int(11) NOT NULL AUTO_INCREMENT,
  `pregunta` varchar(255) DEFAULT NULL,
  `tipo` enum('Texto','Imagen','Audio') DEFAULT NULL,
  `preguntaBin` blob DEFAULT NULL,
  PRIMARY KEY (`idReactivo`)
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pregunta`
--

LOCK TABLES `pregunta` WRITE;
/*!40000 ALTER TABLE `pregunta` DISABLE KEYS */;
INSERT INTO `pregunta` VALUES (1,'¿En qué año nació?','Texto',NULL),(2,'¿Cuál es el nombre completo de la persona de la fotografía y cuál es su parentesco con ella? \n  Escriba la respuesta en una sola línea, separada por coma y espacio. Ejemplo: \'Luz López Cano, madre\'','Imagen',NULL),(3,'¿Cuál es o era el nombre completo de su madre?','Texto',NULL),(4,'¿Cuál es o era el nombre completo de su padre?','Texto',NULL),(5,'¿Cuántos hijos tuvo?','Texto',NULL),(6,'¿En dónde fue tomada la siguiente foto?','Imagen',NULL),(7,'¿En qué año se casó?','Texto',NULL),(8,'¿Recuerda el nombre de esta canción?','Audio',NULL),(9,'¿Cuál es el nombre de su primera mascota?','Texto',NULL),(10,'¿Cuántos nietos tiene?','Texto',NULL),(11,'¿Cuál es el nombre de la última mascota que tuvo o la última que ha adquirido?','Texto',NULL),(12,'¿Cuál es el nombre completo de su primer hijo/a?','Texto',NULL),(13,'¿En qué año nació su primer/a hijo/a?','Texto',NULL),(14,'¿Cuál era su juego favorito durante su infancia?','Texto',NULL),(15,'¿Cuál era su mayor temor cuando era niño?','Texto',NULL),(16,'¿A dónde fue en su primer viaje fuera de la Ciudad de México?','Texto',NULL),(17,'¿Cuál fue el último lugar al que viajó?','Texto',NULL),(18,'¿Cuál es el nombre completo de su esposo/a?','Texto',NULL),(19,'¿Cuál es el primer juguete que recuerda haber tenido?','Texto',NULL),(20,'¿Cuál es su estación del año favorita?','Texto',NULL),(21,'¿Cuál es su libro favorito?','Texto',NULL),(22,'¿En qué ciudad reside actualmente?','Texto',NULL),(23,'¿Cuál fue su primer empleo?','Texto',NULL),(24,'¿Quién es su autor de libros favorito?','Texto',NULL),(25,'¿Por qué es importante este objeto para usted?','Imagen',NULL),(26,'¿En qué año se estrenó su película favorita?','Texto',NULL),(27,'¿Cuál es su equipo de fútbol favorito?','Texto',NULL),(28,'¿Cuál es su banda de música favorita?','Texto',NULL),(29,'¿En qué año trabajó en el siguiente lugar?','Imagen',NULL),(30,'¿En qué año nació su último nieto?','Texto',NULL),(31,'¿Qué deporte practicaba cuando era jóven?\n  Sólo una opción es correcta.','Texto',NULL),(32,'¿Qué quería ser de grande cuando era niño?','Texto',NULL),(33,'¿Qué canción bailó en su boda como primer baile de esposos?','Texto',NULL),(34,'¿En qué año se jubiló?','Texto',NULL),(35,'¿En que trabajó?\n  Sólo una opción es correcta.','Texto',NULL),(36,'¿Cuál era el nombre completo de su abuelo paterno?','Texto',NULL),(37,'¿En qué año comenzó a trabajar?','Texto',NULL),(38,'¿En dónde fue su primer trabajo?','Texto',NULL),(39,'¿Cuál es el nombre de su hermano/a mayor?','Texto',NULL),(40,'¿Cuántos hermanos tiene?','Texto',NULL),(41,'¿A quién le pertenece esta voz?','Audio',NULL),(42,'Esta canción fue muy conocida durante su infancia, ¿Cuál es el nombre de esta canción?','Audio',NULL),(43,'¿Cómo se llama la persona de la foto?','Imagen',NULL),(44,'¿En qué año se tomó esta fotografía?','Imagen',NULL),(45,'¿Cuál es el título de esta canción?','Audio',NULL),(46,'¿De qué es este sonido?','Audio',NULL),(47,'¿Qué es lo primero que hace al despertar?','Texto',NULL),(48,'¿Quién le regaló este objeto?','Imagen',NULL),(49,'¿Quién le escribió esta carta o escrito?','Imagen',NULL),(50,'¿Cuál es su género de películas favorito?','Texto',NULL),(51,'¿A qué época pertenece la ropa que se muestra en la fotografía?','Imagen',NULL),(52,'¿Cuál es el género de música que más escucha?','Texto',NULL),(53,'¿A dónde se fue de luna de miel?','Texto',NULL),(54,'¿Qué es lo último que hace antes de dormir?','Texto',NULL),(55,'¿Qué película estaba de moda en los años 60\'s?','Texto',NULL),(56,'¿Cuál era su materia favorita en la primaria?','Texto',NULL),(57,'¿Cuál es su instrumento musical favorito?','Texto',NULL),(58,'¿A qué animal le tiene más miedo?','Texto',NULL),(59,'¿Identifica la relación entre las dos personas de la fotografía? \n  Por ejemplo, indique si son \'Madre e hija\', de entre las opciones propuestas.','Imagen',NULL),(60,'¿Cuál es el nombre de su mejor amigo de la infancia?','Texto',NULL),(61,'¿Cuál es su planta favorita?','Texto',NULL),(62,'Seleccione el nombre que pertenezca a un integrante de su familia','Texto',NULL),(63,'¿Cuál es el nombre de esta canción?','Audio',NULL),(64,'¿Cuál era el nombre de su abuela materna?','Texto',NULL),(65,'¿Quién canta la siguiente canción?','Audio',NULL),(66,'¿En dónde se encontraba durante el temblor de 1985?','Texto',NULL),(67,'¿Cuál es su platillo de comida favorito?','Texto',NULL),(68,'¿Cuál es su postre favorito?','Texto',NULL),(69,'¿Cuál es su color favorito?','Texto',NULL),(70,'¿En qué año conoció al amor de su vida?','Texto',NULL),(71,'¿Cuántos años tiene?','Texto',NULL),(72,'¿Cuál era un juego que más jugaba durante su infancia?','Texto',NULL),(73,'¿En dónde vive actualmente?','Texto',NULL),(74,'¿Con quién vive actualmente?\n  Escriba sólo parentesco separado por coma y espacio.','Texto',NULL),(75,'¿Quién cuida de usted?\n  Escriba sólo el parentesco.','Texto',NULL),(76,'¿Cuál fue su primer trabajo?','Texto',NULL),(77,'¿En dónde vivió durante su infancia?\n  Seleccione sólo una opción.','Texto',NULL),(78,'¿En qué año se descubrió América?','Texto',NULL),(79,'¿En qué año terminó la Segunda Guerra Mundial?','Texto',NULL),(80,'¿En qué año se cayeron las torres gemelas?','Texto',NULL),(81,'¿A qué suceso importante pertenece esta fotografía?','Imagen',NULL),(82,'¿Qué actores eran famosos en la época de oro mexicano?','Texto',NULL),(83,'¿En qué año comenzó la Primera Guerra Mundial?','Texto',NULL),(84,'¿En qué año fue el mayor terremoto en México?','Texto',NULL),(85,'¿Qué día se celebra Noche Buena?','Texto',NULL);
/*!40000 ALTER TABLE `pregunta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reminiscencia`
--

DROP TABLE IF EXISTS `reminiscencia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reminiscencia` (
  `cveAcceso` varchar(10) NOT NULL,
  `idReactivo` int(11) NOT NULL,
  `respuestaPaciente` varchar(255) DEFAULT NULL,
  `respuestaCuidador` varchar(255) DEFAULT NULL,
  `valoracion` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`cveAcceso`,`idReactivo`),
  KEY `idReactivo` (`idReactivo`),
  CONSTRAINT `reminiscencia_ibfk_1` FOREIGN KEY (`cveAcceso`) REFERENCES `ap_reminiscencia` (`cveAcceso`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `reminiscencia_ibfk_2` FOREIGN KEY (`idReactivo`) REFERENCES `pregunta` (`idReactivo`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reminiscencia`
--

LOCK TABLES `reminiscencia` WRITE;
/*!40000 ALTER TABLE `reminiscencia` DISABLE KEYS */;
INSERT INTO `reminiscencia` VALUES ('12345abcde',1,'1950','1948',0),('12345abcde',3,'Gloria Macedo Ruíz','Gloria Macedo Ruíz',1);
/*!40000 ALTER TABLE `reminiscencia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `screening`
--

DROP TABLE IF EXISTS `screening`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `screening` (
  `idReactivo` int(11) NOT NULL,
  `cveAcceso` varchar(10) NOT NULL,
  `respuestaT` varchar(100) DEFAULT NULL,
  `respuestaImg` blob DEFAULT NULL,
  `puntajeReactivo` int(11) DEFAULT NULL,
  `puntajeMaximo` int(11) DEFAULT 0,
  PRIMARY KEY (`idReactivo`,`cveAcceso`),
  KEY `cveAcceso` (`cveAcceso`),
  CONSTRAINT `screening_ibfk_1` FOREIGN KEY (`cveAcceso`) REFERENCES `ap_screening` (`cveAcceso`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `screening`
--

LOCK TABLES `screening` WRITE;
/*!40000 ALTER TABLE `screening` DISABLE KEYS */;
INSERT INTO `screening` VALUES (1,'abcde12345','1a2b3c4d5e','0',1,1),(2,'abcde12345',NULL,'12345',1,1);
/*!40000 ALTER TABLE `screening` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tema`
--

DROP TABLE IF EXISTS `tema`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tema` (
  `cveTemas` int(11) NOT NULL AUTO_INCREMENT,
  `tema` varchar(20) DEFAULT NULL,
  `dificultad` enum('Facil','Medio','Dificil') DEFAULT NULL,
  PRIMARY KEY (`cveTemas`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tema`
--

LOCK TABLES `tema` WRITE;
/*!40000 ALTER TABLE `tema` DISABLE KEYS */;
INSERT INTO `tema` VALUES (1,'Animales','Facil'),(2,'Animales','Medio'),(3,'Objetos de casa','Facil'),(4,'Objetos de casa','Dificil');
/*!40000 ALTER TABLE `tema` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-02-18 17:08:34
