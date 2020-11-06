-- MariaDB dump 10.17  Distrib 10.4.13-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: TrabajoTerminal
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
  `especialista` varchar(8) NOT NULL,
  `fechaAp` date DEFAULT NULL,
  `resultadoFinal` int(11) DEFAULT NULL,
  PRIMARY KEY (`cveAcceso`),
  KEY `paciente` (`paciente`),
  KEY `especialista` (`especialista`),
  CONSTRAINT `ap_screening_ibfk_1` FOREIGN KEY (`paciente`) REFERENCES `paciente` (`nomUsuario`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `ap_screening_ibfk_2` FOREIGN KEY (`especialista`) REFERENCES `especialista` (`nomUsuario`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ap_screening`
--

LOCK TABLES `ap_screening` WRITE;
/*!40000 ALTER TABLE `ap_screening` DISABLE KEYS */;
INSERT INTO `ap_screening` VALUES ('abcde12345','SocorroMaR','Saúl_MDo','2020-12-08',24);
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
  PRIMARY KEY (`cveAcceso`,`cveTema`),
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
  `unidadMedica` varchar(100) NOT NULL,
  `cedulaMedicaG` varchar(8) NOT NULL,
  `Especialidad` varchar(40) DEFAULT NULL,
  `numPacientes` int(11) DEFAULT NULL,
  PRIMARY KEY (`nomUsuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `especialista`
--

LOCK TABLES `especialista` WRITE;
/*!40000 ALTER TABLE `especialista` DISABLE KEYS */;
INSERT INTO `especialista` VALUES ('Lupita_8','Guadalupe Ruíz Zarate','GRZ123L8','ruizza-guadalupe@hotmail.com','ISSSTE','76543210','Otología',8),('Saúl_MDo','Saúl Mendoza Domínguez','S1aul92M','saul_mendom@gmail.com','IMSS','01234567','optometría',10);
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
  `preguntaBin` varbinary(8000) DEFAULT NULL,
  `tipo` enum('Texto','Imagen','Audio') DEFAULT NULL,
  PRIMARY KEY (`idReactivo`)
) ENGINE=InnoDB AUTO_INCREMENT=176 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pregunta`
--

LOCK TABLES `pregunta` WRITE;
/*!40000 ALTER TABLE `pregunta` DISABLE KEYS */;
INSERT INTO `pregunta` VALUES (86,'¿En qué año nació?',NULL,'Texto'),(87,'¿Cuál es el nombre completo de la persona de la fotografía y cuál es su parentesco con ella? \n  Escriba la respuesta en una sola línea, separada por coma y espacio. Ejemplo: \'Luz López Cano, madre\'',NULL,'Imagen'),(88,'¿Cuál es o era el nombre completo de su madre?',NULL,'Texto'),(89,'¿Cuál es o era el nombre completo de su padre?',NULL,'Texto'),(90,'¿Cuántos hijos tuvo?',NULL,'Texto'),(91,'¿En qué año nació?',NULL,'Texto'),(92,'¿Cuál es el nombre completo de la persona de la fotografía y cuál es su parentesco con ella? \n  Escriba la respuesta en una sola línea, separada por coma y espacio. Ejemplo: \'Luz López Cano, madre\'',NULL,'Imagen'),(93,'¿Cuál es o era el nombre completo de su madre?',NULL,'Texto'),(94,'¿Cuál es o era el nombre completo de su padre?',NULL,'Texto'),(95,'¿Cuántos hijos tuvo?',NULL,'Texto'),(96,'¿En dónde fue tomada la siguiente foto?',NULL,'Imagen'),(97,'¿En qué año se casó?',NULL,'Texto'),(98,'¿Recuerda el nombre de esta canción?',NULL,'Audio'),(99,'¿Cuál es el nombre de su primera mascota?',NULL,'Texto'),(100,'¿Cuántos nietos tiene?',NULL,'Texto'),(101,'¿Cuál es el nombre de la última mascota que tuvo o la última que ha adquirido?',NULL,'Texto'),(102,'¿Cuál es el nombre completo de su primer hijo/a?',NULL,'Texto'),(103,'¿En qué año nació su primer/a hijo/a?',NULL,'Texto'),(104,'¿Cuál era su juego favorito durante su infancia?',NULL,'Texto'),(105,'¿Cuál era su mayor temor cuando era niño?',NULL,'Texto'),(106,'¿A dónde fue en su primer viaje fuera de la Ciudad de México?',NULL,'Texto'),(107,'¿Cuál fue el último lugar al que viajó?',NULL,'Texto'),(108,'¿Cuál es el nombre completo de su esposo/a?',NULL,'Texto'),(109,'¿Cuál es el primer juguete que recuerda haber tenido?',NULL,'Texto'),(110,'¿Cuál es su estación del año favorita?',NULL,'Texto'),(111,'¿Cuál es su libro favorito?',NULL,'Texto'),(112,'¿En qué ciudad reside actualmente?',NULL,'Texto'),(113,'¿Cuál fue su primer empleo?',NULL,'Texto'),(114,'¿Quién es su autor de libros favorito?',NULL,'Texto'),(115,'¿Por qué es importante este objeto para usted?',NULL,'Imagen'),(116,'¿En qué año se estrenó su película favorita?',NULL,'Texto'),(117,'¿Cuál es su equipo de fútbol favorito?',NULL,'Texto'),(118,'¿Cuál es su banda de música favorita?',NULL,'Texto'),(119,'¿En qué año trabajó en el siguiente lugar?',NULL,'Imagen'),(120,'¿En qué año nació su último nieto?',NULL,'Texto'),(121,'¿Qué deporte practicaba cuando era jóven?\n  Sólo una opción es correcta.',NULL,'Texto'),(122,'¿Qué quería ser de grande cuando era niño?',NULL,'Texto'),(123,'¿Qué canción bailó en su boda como primer baile de esposos?',NULL,'Texto'),(124,'¿En qué año se jubiló?',NULL,'Texto'),(125,'¿En que trabajó?\n  Sólo una opción es correcta.',NULL,'Texto'),(126,'¿Cuál era el nombre completo de su abuelo paterno?',NULL,'Texto'),(127,'¿En qué año comenzó a trabajar?',NULL,'Texto'),(128,'¿En dónde fue su primer trabajo?',NULL,'Texto'),(129,'¿Cuál es el nombre de su hermano/a mayor?',NULL,'Texto'),(130,'¿Cuántos hermanos tiene?',NULL,'Texto'),(131,'¿A quién le pertenece esta voz?',NULL,'Audio'),(132,'Esta canción fue muy conocida durante su infancia, ¿Cuál es el nombre de esta canción?',NULL,'Audio'),(133,'¿Cómo se llama la persona de la foto?',NULL,'Imagen'),(134,'¿En qué año se tomó esta fotografía?',NULL,'Imagen'),(135,'¿Cuál es el título de esta canción?',NULL,'Audio'),(136,'¿De qué es este sonido?',NULL,'Audio'),(137,'¿Qué es lo primero que hace al despertar?',NULL,'Texto'),(138,'¿Quién le regaló este objeto?',NULL,'Imagen'),(139,'¿Quién le escribió esta carta o escrito?',NULL,'Imagen'),(140,'¿Cuál es su género de películas favorito?',NULL,'Texto'),(141,'¿A qué época pertenece la ropa que se muestra en la fotografía?',NULL,'Imagen'),(142,'¿Cuál es el género de música que más escucha?',NULL,'Texto'),(143,'¿A dónde se fue de luna de miel?',NULL,'Texto'),(144,'¿Qué es lo último que hace antes de dormir?',NULL,'Texto'),(145,'¿Qué película estaba de moda en los años 60\'s?',NULL,'Texto'),(146,'¿Cuál era su materia favorita en la primaria?',NULL,'Texto'),(147,'¿Cuál es su instrumento musical favorito?',NULL,'Texto'),(148,'¿A qué animal le tiene más miedo?',NULL,'Texto'),(149,'¿Identifica la relación entre las dos personas de la fotografía? \n  Por ejemplo, indique si son \'Madre e hija\', de entre las opciones propuestas.',NULL,'Imagen'),(150,'¿Cuál es el nombre de su mejor amigo de la infancia?',NULL,'Texto'),(151,'¿Cuál es su planta favorita?',NULL,'Texto'),(152,'Seleccione el nombre que pertenezca a un integrante de su familia',NULL,'Texto'),(153,'¿Cuál es el nombre de esta canción?',NULL,'Audio'),(154,'¿Cuál era el nombre de su abuela materna?',NULL,'Texto'),(155,'¿Quién canta la siguiente canción?',NULL,'Audio'),(156,'¿En dónde se encontraba durante el temblor de 1985?',NULL,'Texto'),(157,'¿Cuál es su platillo de comida favorito?',NULL,'Texto'),(158,'¿Cuál es su postre favorito?',NULL,'Texto'),(159,'¿Cuál es su color favorito?',NULL,'Texto'),(160,'¿En qué año conoció al amor de su vida?',NULL,'Texto'),(161,'¿Cuántos años tiene?',NULL,'Texto'),(162,'¿Cuál era un juego que más jugaba durante su infancia?',NULL,'Texto'),(163,'¿En dónde vive actualmente?',NULL,'Texto'),(164,'¿Con quién vive actualmente?\n  Escriba sólo parentesco separado por coma y espacio.',NULL,'Texto'),(165,'¿Quién cuida de usted?\n  Escriba sólo el parentesco.',NULL,'Texto'),(166,'¿Cuál fue su primer trabajo?',NULL,'Texto'),(167,'¿En dónde vivió durante su infancia?\n  Seleccione sólo una opción.',NULL,'Texto'),(168,'¿En qué año se descubrió América?',NULL,'Texto'),(169,'¿En qué año terminó la Segunda Guerra Mundial?',NULL,'Texto'),(170,'¿En qué año se cayeron las torres gemelas?',NULL,'Texto'),(171,'¿A qué suceso importante pertenece esta fotografía?',NULL,'Imagen'),(172,'¿Qué actores eran famosos en la época de oro mexicano?',NULL,'Texto'),(173,'¿En qué año comenzó la Primera Guerra Mundial?',NULL,'Texto'),(174,'¿En qué año fue el mayor terremoto en México?',NULL,'Texto'),(175,'¿Qué día se celebra Noche Buena?',NULL,'Texto');
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
  `respuestaImg` varbinary(8000) DEFAULT NULL,
  `puntajeReactivo` int(11) DEFAULT NULL,
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
INSERT INTO `screening` VALUES (1,'abcde12345','1a2b3c4d5e','0',1),(2,'abcde12345',NULL,'12345',1);
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

-- Dump completed on 2020-11-05 19:04:51
