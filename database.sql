CREATE TABLE `users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(100),
  `email` VARCHAR(100),
  `password` VARCHAR(100),
  `image` VARCHAR(100),
  PRIMARY KEY (`id`)
);

INSERT INTO `users` (`username`, `email`, `password`, `image`) VALUES
('Yug Agarwal', 'yugagarwal704@gmail.com', '1234', 'yug.png'),
('Saksham Kotia', 'saksham@example.com', 'shubh@123', 'saksham.jpg'),
('Avisha Agarwal', 'avisha@gmail.com', 'secure@1', 'avisha.jpeg'),
('Rida Geelani', 'rida@gmail.com', 'alphabeta', 'rida.jpeg');
