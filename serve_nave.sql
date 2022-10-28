-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 28-Out-2022 às 11:29
-- Versão do servidor: 10.4.24-MariaDB
-- versão do PHP: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `serve_nave`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `info_user`
--

CREATE TABLE `info_user` (
  `login` varchar(30) NOT NULL,
  `nome` varchar(255) NOT NULL,
  `nome_s` varchar(255) DEFAULT NULL,
  `sexo` varchar(10) DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `data_nascimento` date NOT NULL,
  `cpf` varchar(255) NOT NULL,
  `cell` varchar(255) NOT NULL,
  `uf` varchar(255) DEFAULT NULL,
  `cidade` varchar(255) DEFAULT NULL,
  `cor` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Extraindo dados da tabela `info_user`
--

INSERT INTO `info_user` (`login`, `nome`, `nome_s`, `sexo`, `email`, `data_nascimento`, `cpf`, `cell`, `uf`, `cidade`, `cor`) VALUES
('euella', 'Rafaella Campos de Araújo da Silva Netto ', 'ella', 'indefinido', 'camposrafaella04@gmail.com', '2006-06-11', '13427150712', '21979426039', 'RJ', 'Rio de Janeiro ', 'preta'),
('subaru3rem', 'Cainã Costa', 'subaru', 'masculino', 'cainancosta6@gmail.com', '2004-10-13', '20637449711', '021975735109', 'RJ', 'Rio de janeiro', 'preta'),
('eu_ella', 'Rafaella Campos de Araujo da Silva Netto', 'Ella ', 'feminino', 'eu_ella@gmail.com', '2006-06-11', '20637449712', '21975735109', 'RJ', 'Rio de janeiro', 'preta');

-- --------------------------------------------------------

--
-- Estrutura da tabela `usuarios`
--

CREATE TABLE `usuarios` (
  `login` varchar(30) NOT NULL,
  `senha` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Extraindo dados da tabela `usuarios`
--

INSERT INTO `usuarios` (`login`, `senha`) VALUES
('euella', 'batatadoce'),
('eu_ella', '123'),
('subaru3rem', '123');

--
-- Índices para tabelas despejadas
--

--
-- Índices para tabela `info_user`
--
ALTER TABLE `info_user`
  ADD UNIQUE KEY `cpf` (`cpf`),
  ADD KEY `login` (`login`);

--
-- Índices para tabela `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`login`);

--
-- Restrições para despejos de tabelas
--

--
-- Limitadores para a tabela `info_user`
--
ALTER TABLE `info_user`
  ADD CONSTRAINT `info_user_ibfk_1` FOREIGN KEY (`login`) REFERENCES `usuarios` (`login`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
