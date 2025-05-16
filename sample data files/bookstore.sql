-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 30, 2025 at 04:58 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bookstore`
--

-- --------------------------------------------------------

--
-- Table structure for table `author`
--

CREATE TABLE `author` (
  `sno` int(255) NOT NULL,
  `name` text NOT NULL,
  `dob` varchar(100) NOT NULL,
  `years_active` varchar(50) NOT NULL,
  `image` varchar(250) NOT NULL,
  `bio` varchar(5000) NOT NULL,
  `genres` varchar(5000) NOT NULL,
  `awards` varchar(5000) NOT NULL,
  `date` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `author`
--

INSERT INTO `author` (`sno`, `name`, `dob`, `years_active`, `image`, `bio`, `genres`, `awards`, `date`) VALUES
(1, 'William Shakespeare ', 'April 27, 1564', '1585–1613', 'images/auth_William_Shakespeare.jpg', 'The literal GOAT of English Literature', 'Sonnet, Poem, Epitaph, Romance, Comedy, Drama, Novel, Tragedy', 'Lucille Lortel Award for Outstanding Revival', '2025-04-23'),
(2, 'Evelyn Reed', '1905-10-31', '1940–1979', 'images/evelyn_reed.jpg', 'Evelyn Reed (1905–1979) was an American communist and women’s rights activist. She joined the communist movement in 1940 and remained a leading member of the Socialist Workers Party until her death. An active participant in the women’s liberation movement of the 1960s and 1970s, she was a founding member of the Women’s National Abortion Action Coalition.', 'Non-fiction, Feminism, Politics', 'N/A', '2025-04-30'),
(3, 'Jian Li', '', '2010–present', 'images/jian_li.jpg', 'Dr. Jian Li is a Publishing Editor of Physics & Astronomy at Springer, responsible for book and journal projects in the Greater China area. He earned his Ph.D. in theoretical physics from the Institute of Physics, Chinese Academy of Sciences in 2010, and worked as a postdoctoral fellow at the Texas Center for High Temperature Superconductors from 2010 to 2013.', 'Science, Physics, Academic Publishing', 'N/A', '2025-04-30'),
(4, 'Isabelle Moreau', '', '2005–present', 'images/isabelle_moreau.jpg', 'Isabelle Moreau is a leader, coach, and former Director of Marketing at John Wiley & Sons Canada. In 2005, she left her corporate career to travel the world and pursue a path of personal development and coaching, helping others align with their authentic selves.', 'Self-help, Personal Development', 'N/A', '2025-04-30'),
(5, 'Anya Petrova', '', '2018–present', 'images/anya_petrova.jpg', 'Anya Petrova is a Russian journalist and software reviewer with a strong focus on consumer technology. With 6 years of experience in writing about software, she combines her journalistic skills with a deep understanding of technology to deliver engaging and informative content that assists readers in navigating the software landscape.', 'Technology, Journalism', '', '2025-04-30'),
(6, 'Samuel Hayes', '', '2010–present', 'images/samuel_hayes.jpg', 'Dr. Samuel Hayes, Jr. is distinguished as a strategic designer by ministry, military, business, and academic leaders. He is the Founder and President of Samuel Hayes Ministries, Inc. and leads a marriage ministry with his wife, Apostle Dr. Andrea Hayes. He is an international best-selling author, and his books distill insights on relational leadership, global networks, design thinking, marriage, and strategy.', 'Leadership, Strategy, Religion', '', '2025-04-30'),
(7, 'Rachel Hartman', '1972-07-09', '1996–present', 'images/rachel_hartman.jpg', 'Rachel Hartman is an American writer and comic artist, known for her young adult fantasy novels including \"Seraphina\", \"Shadow Scale\", \"Tess of the Road\", and \"In the Serpent\'s Wake\". She holds a BA in Comparative Literature from Washington University in St. Louis and has received several awards for her work.', 'Young Adult, Fantasy', '2012 Cybils Award; 2013 William C. Morris Award', '2025-04-30'),
(8, 'Alistair Blackwood', '', '2015–present', 'images/alistair_blackwood.jpg', 'Alistair Blackwood is a technology and finance enthusiast with a background in AI development and trading. He is known for creating innovative solutions in automated trading systems and contributes content to ForexRobotEasy, focusing on the EASY Scalperology Bot.', 'Technology, Finance, AI', '', '2025-04-30'),
(9, 'Sheena Hutchinson', '', '2013–present', 'images/sheena_hutchinson.jpg', 'Sheena Hutchinson is a New York-born author known for her \"Seraphina\" series. She writes stories that empower and inspire, often focusing on themes of love, destiny, and the supernatural.', 'Paranormal Romance, Young Adult', '', '2025-04-30'),
(10, 'Marcus Thorne', '', '2007–present', 'images/marcus_thorne.jpg', 'Marcus Thorne is a British publisher and director at FatCat Publishing Limited since 2007. He has also authored works on soil science and contributes articles on theology and social issues on Medium.', 'Publishing, Non-fiction, Theology', '', '2025-04-30');

-- --------------------------------------------------------

--
-- Table structure for table `book`
--

CREATE TABLE `book` (
  `sno` int(255) NOT NULL,
  `name` varchar(1000) NOT NULL,
  `author` varchar(500) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `author_id` int(255) NOT NULL,
  `total_sells` int(11) NOT NULL,
  `description` varchar(2500) NOT NULL,
  `category` varchar(100) NOT NULL,
  `image` varchar(300) NOT NULL,
  `date` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `book`
--

INSERT INTO `book` (`sno`, `name`, `author`, `price`, `author_id`, `total_sells`, `description`, `category`, `image`, `date`) VALUES
(1, 'Hamlet', 'William Shakespeare ', 1350.00, 1, 500, 'A powerful tragedy exploring themes of revenge, morality, and madness. Prince Hamlet seeks vengeance on his uncle Claudius, who has murdered his father and married his mother. The play delves into profound questions about life and death.\r\n', 'Tragedy', 'images/book hamlet.jpg', '2025-04-23'),
(2, 'Romeo and Juliet', 'William Shakespeare', 1500.00, 1, 1000, 'A timeless and iconic love story about two young star-crossed lovers from feuding families whose deaths ultimately reconcile their households. The play explores themes of love, passion, fate, and conflict.\r\n', 'Tragedy/Romance', 'images/book rome and juliet.jpg', '2025-04-23'),
(3, 'Macbeth', 'William Shakespeare ', 1800.00, 1, 800, 'A dark and intense tragedy focusing on the destructive nature of ambition and guilt. Macbeth, a Scottish general, is driven by his wife\'s urging and a prophecy to murder King Duncan and seize the throne, leading to a reign of terror and his eventual downfall.\r\n', 'Tragedy', 'images/book macbeth.jpg', '2025-04-23'),
(4, 'A Midsummer Night\'s Dream', 'William Shakespeare ', 1600.00, 1, 700, 'A delightful and enchanting comedy involving the romantic adventures of four young Athenians, a group of amateur actors, and mischievous fairies in a magical forest. The play explores themes of love, illusion, and the power of imagination.\r\n', 'Comedy/Fantasy', 'images/book sleeping in the moonlight.jpg', '2025-04-23'),
(5, 'The Whispering Pines', 'Evelyn Reed', 19.99, 2, 55, 'A chilling mystery set in a remote village where ...', 'Mystery', 'images/1stbook.jpg', '2025-04-30'),
(6, 'Echoes of the Cosmos', 'Jian Li', 24.50, 3, 32, 'A sweeping science fiction epic that follows a gen...', 'Science Fiction', 'images/2ndbook.jfif', '2025-04-30'),
(7, 'The Baker\'s Secret', 'Isabelle Moreau', 16.75, 4, 88, 'A heartwarming historical fiction novel about a sm...', 'Historical Fiction', 'images/3rdbook.jpg', '2025-04-30'),
(8, 'The Serpent\'s Crown', 'Alistair Blackwood', 21.00, 8, 41, 'The first book in a thrilling fantasy series fille...', 'Fantasy', 'images/4book.jpg', '2025-04-30'),
(9, 'City of Lost Dreams', 'Anya Petrova', 18.20, 5, 63, 'A vibrant urban fantasy novel set in a sprawling m...', 'Urban Fantasy', 'images/5thbook.jpg', '2025-04-30'),
(10, 'Beneath Azure Skies', 'Samuel Hayes', 14.99, 6, 95, 'A poignant contemporary romance about two individ...', 'Romance', 'images/6thbook.jpg', '2025-04-30'),
(11, 'The Alchemist\'s Notebook', 'Sheena Hutchinson', 22.75, 9, 28, 'A captivating blend of historical fiction and magi...', 'Magical Realism', 'images/7book.jpg', '2025-04-30');

-- --------------------------------------------------------

--
-- Table structure for table `contact`
--

CREATE TABLE `contact` (
  `sno` int(250) NOT NULL,
  `name` varchar(200) NOT NULL,
  `email` varchar(500) NOT NULL,
  `msg` varchar(5000) NOT NULL,
  `date` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contact`
--

INSERT INTO `contact` (`sno`, `name`, `email`, `msg`, `date`) VALUES
(1, 'Uchhas Saha', 'uchhas.saha@g.bracu.ac.bd', 'This is a feedback that I inserted via localhost', '2025-04-23'),
(3, 'Bruce Wayne', 'brucethomaswayne1915@gmail.com', 'I am Rich!!!', '2025-04-23'),
(4, 'Bruce Wayne', 'brucethomaswayne1915@gmail.com', 'I am Rich!!!', '2025-04-23'),
(5, 'Debo', 'debo@gmail.com', 'Add the books of Uchhas Saha', '2025-04-24'),
(6, 'Debo', 'debo@gmail.com', 'Add the books of Uchhas Saha', '2025-04-24');

-- --------------------------------------------------------

--
-- Table structure for table `publisher`
--

CREATE TABLE `publisher` (
  `sno` int(255) NOT NULL,
  `name` varchar(500) NOT NULL,
  `logo` varchar(1000) NOT NULL,
  `type` varchar(1000) NOT NULL,
  `iimprints` varchar(1500) NOT NULL,
  `books` varchar(5000) NOT NULL,
  `authors` varchar(2000) NOT NULL,
  `link` varchar(500) NOT NULL,
  `loc` varchar(500) NOT NULL,
  `member_since` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `publisher`
--

INSERT INTO `publisher` (`sno`, `name`, `logo`, `type`, `iimprints`, `books`, `authors`, `link`, `loc`, `member_since`) VALUES
(1, 'And Other Stories', 'images/pub and other stories.jpg', 'Literary Fiction and Fiction', 'No Imprints', 'working', 'working', 'https://www.andotherstories.org/', 'London, GB', '2025-04-24');

-- --------------------------------------------------------

--
-- Table structure for table `stationary`
--

CREATE TABLE `stationary` (
  `sno` int(255) NOT NULL,
  `name` varchar(500) NOT NULL,
  `price` int(255) NOT NULL,
  `img_file` varchar(1000) NOT NULL,
  `date` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `stationary`
--

INSERT INTO `stationary` (`sno`, `name`, `price`, `img_file`, `date`) VALUES
(1, 'Ballpoint Pen', 10, 'images/st-ballpoint pen.jpg', '0000-00-00'),
(2, 'Mechanical Pen', 15, 'images/st-mechanical pen.jpg', '0000-00-00'),
(3, 'Pencil', 5, 'images/st-pencil.jpg', '0000-00-00'),
(4, 'Sharpener', 5, 'images/st-sharpener.jpg', '0000-00-00'),
(5, 'Eraser', 5, 'images/st-eraser.jpg', '0000-00-00');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `sno` int(255) NOT NULL,
  `name` varchar(250) NOT NULL,
  `email` varchar(500) NOT NULL,
  `pw` varchar(70) NOT NULL,
  `date` datetime(6) NOT NULL DEFAULT current_timestamp(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`sno`, `name`, `email`, `pw`, `date`) VALUES
(1, 'uchhas', 'uchhas.saha@gmail.com', 'password', '0000-00-00 00:00:00.000000'),
(2, 'uchhas', 'uchhas.saha@g.bracu.ac.bd', 'passlol', '2025-04-12 21:01:07.234650');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `author`
--
ALTER TABLE `author`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `book`
--
ALTER TABLE `book`
  ADD PRIMARY KEY (`sno`),
  ADD KEY `Test` (`author_id`);

--
-- Indexes for table `contact`
--
ALTER TABLE `contact`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `publisher`
--
ALTER TABLE `publisher`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `stationary`
--
ALTER TABLE `stationary`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`sno`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `author`
--
ALTER TABLE `author`
  MODIFY `sno` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `book`
--
ALTER TABLE `book`
  MODIFY `sno` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `contact`
--
ALTER TABLE `contact`
  MODIFY `sno` int(250) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `publisher`
--
ALTER TABLE `publisher`
  MODIFY `sno` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `stationary`
--
ALTER TABLE `stationary`
  MODIFY `sno` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `sno` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `book`
--
ALTER TABLE `book`
  ADD CONSTRAINT `Test` FOREIGN KEY (`author_id`) REFERENCES `author` (`sno`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
